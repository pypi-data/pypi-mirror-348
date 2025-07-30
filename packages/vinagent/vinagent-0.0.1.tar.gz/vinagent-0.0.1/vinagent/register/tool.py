import sys
import os
import json
import inspect
import importlib
import logging
from functools import wraps
from typing import Dict, Any, Optional, Callable
import ast
import uuid
from pathlib import Path

sys.path.append(os.path.join(os.getcwd(), "tool_template"))
from .initialize import llm

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ToolManager:
    """Centralized tool management class"""
    def __init__(self, tools_path: Path = Path("templates/tools.json"), is_reset_tools: bool=False):
        self.tools_path = tools_path
        self.is_reset_tools = is_reset_tools
        self.tools_path = Path(tools_path) if isinstance(tools_path, str) else tools_path
        if not self.tools_path.exists():
            self.tools_path.write_text(json.dumps({}, indent=4), encoding="utf-8")

        if self.is_reset_tools:
            self.tools_path.write_text(json.dumps({}, indent=4), encoding="utf-8")

        self._registered_functions: Dict[str, Callable] = {}
        
    def load_tools(self) -> Dict[str, Any]:
        """Load existing tools from JSON"""
        if self.tools_path:
            with open(self.tools_path, "r", encoding="utf-8") as f:
                return json.load(f)
        else:
            return {}

    def save_tools(self, tools: Dict[str, Any]) -> None:
        """Save tools to JSON"""
        with open(self.tools_path, "w", encoding="utf-8") as f:
            json.dump(tools, f, indent=4, ensure_ascii=False)

    def register_function(self, func: Callable, metadata: Dict[str, Any]):
        """Register a function with its metadata"""
        self._registered_functions[func.__name__] = func
        tools = self.load_tools()
        tools[func.__name__] = metadata
        self.save_tools(tools)

    def function_tool(self, func):
        """Decorator to register a function as a tool
        # Example usage:
        @function_tool
        def sample_function(x: int, y: str) -> str:
            '''Sample function for testing'''
            return f"{y}: {x}"
        """

        @wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)

        # Get function metadata
        signature = inspect.signature(func)

        # Try to get module path, fall back to None if not available
        module_path = "__runtime__"

        # Create metadata
        if module_path == "__runtime__":
            metadata = {
                "tool_name": func.__name__,
                "arguments": {
                    name: (
                        str(param.annotation)
                        if param.annotation != inspect.Parameter.empty
                        else "Any"
                    )
                    for name, param in signature.parameters.items()
                },
                "return": (
                    str(signature.return_annotation)
                    if signature.return_annotation != inspect.Signature.empty
                    else "Any"
                ),
                "docstring": (func.__doc__ or "").strip(),
                "module_path": module_path,
                "tool_call_id": "tool_" + str(uuid.uuid4()),
                "is_runtime": module_path == "__runtime__",
            }

            # Register both the function and its metadata
            
            self.register_function(func, metadata)
            logger.info(
                f"Registered tool: {func.__name__} "
                f"({'runtime' if module_path == '__runtime__' else 'file-based'})"
            )
        return wrapper

    def register_tool(self, module_path: str) -> None:
        """Register tools from a module"""
        try:
            module = importlib.import_module(module_path, package=__package__)
            module_source = inspect.getsource(module)
        except (ImportError, ValueError) as e:
            raise ValueError(f"Failed to load module {module_path}: {str(e)}")

        prompt = (
            "Analyze this module and return a list of tools in JSON format:"
            "- Module code:"
            f"{module_source}"
            "Format: Let's return a list of json format without further explaination and without ```json characters markdown and keep module_path unchange."
            "[{{"
            '"tool_name": "The function",'
            '"arguments": "A dictionary of keyword-arguments to execute tool. Let\'s keep default value if it was set",'
            '"return": "Return value of this tool",'
            '"docstring": "Docstring of this tool",'
            '"dependencies": "List of libraries need to run this tool",'
            f'"module_path": "{module_path}"'
            "}}]"
        )

        response = llm.invoke(prompt)

        try:
            new_tools = ast.literal_eval(response.content.strip())
        except (ValueError, SyntaxError) as e:
            raise ValueError(f"Invalid tool format from LLM: {str(e)}")

        tools = self.load_tools()
        for tool in new_tools:
            tool["module_path"] = module_path
            tools[tool["tool_name"]] = tool
            tools[tool["tool_name"]]["tool_call_id"] = "tool_" + str(uuid.uuid4())
            logger.info(f"Registered {tool['tool_name']}:\n{tool}")

        self.save_tools(tools)
        logger.info(f"Completed registration for module {module_path}")

    def tool_calling(self, task: str) -> Any:
        """Execute a tool based on task description"""
        tools = self.load_tools()

        prompt = f"""
        Select a tool for this task from available tools:
        - Task: {task}
        - Available tools: {json.dumps(tools)}
        
        Return format: Only return dictionary without explaination and do not need bounded in ```python``` or ```json```
        {{
            "tool_name": "The function",
            "arguments": "A dictionary of keyword-arguments to execute tool_name",
            "module_path": "module_path to import this tool"
        }}
        """

        response = llm.invoke(prompt).content
        tool_data = self.extract_json(response)

        if not tool_data or "None" in tool_data:
            return llm.invoke(task).content

        try:
            tool_call = json.loads(tool_data)
            func_name = tool_call["tool_name"]
            arguments = tool_call["arguments"]
            module_path = tool_call["module_path"]

            if func_name in globals():
                return globals()[func_name](**arguments)

            module = importlib.import_module(module_path, package=__package__)
            func = getattr(module, func_name)
            return func(**arguments)
        except (json.JSONDecodeError, ImportError, AttributeError) as e:
            logging.error(f"Tool execution failed: {str(e)}")
            return None

    def extract_json(self, text: str) -> Optional[str]:
        """Extract first valid JSON object from text"""
        stack = []
        start = text.find("{")
        if start == -1:
            return None

        for i in range(start, len(text)):
            if text[i] == "{":
                stack.append("{")
            elif text[i] == "}":
                stack.pop()
                if not stack:
                    return text[start : i + 1]
        return None

    @staticmethod
    def _extract_json(text: str) -> Optional[str]:
        """Extract first valid JSON object from text using stack-based parsing"""
        start = text.find("{")
        if start == -1:
            return None

        stack = []
        for i in range(start, len(text)):
            if text[i] == "{":
                stack.append("{")
            elif text[i] == "}":
                stack.pop()
                if not stack:
                    return text[start : i + 1]
        return None
