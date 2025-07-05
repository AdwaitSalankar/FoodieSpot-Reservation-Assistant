from typing import Callable, Dict, Any
import inspect
import json

class ToolRegistry:
    def __init__(self):
        self.tools = {}
    
    def register_tool(self, name: str, description: str, parameters: Dict[str, Any], function: Callable):
        self.tools[name] = {
            "description": description,
            "parameters": parameters,
            "function": function
        }
    
    def get_tools_description(self) -> str:
        tools_desc = []
        for name, tool in self.tools.items():
            params = json.dumps(tool["parameters"], indent=2)
            tools_desc.append(f"{name}: {tool['description']}\nParameters: {params}")
        return "\n\n".join(tools_desc)
    
    def execute_tool(self, tool_name: str, parameters: Dict[str, Any]):
        if tool_name not in self.tools:
            raise ValueError(f"Tool {tool_name} not found")
        
        tool = self.tools[tool_name]
        func = tool["function"]
        
        # Verify parameters
        sig = inspect.signature(func)
        required_params = [
            p.name for p in sig.parameters.values() 
            if p.default == inspect.Parameter.empty
        ]
        
        missing_params = [p for p in required_params if p not in parameters]
        if missing_params:
            raise ValueError(f"Missing required parameters: {missing_params}")
        
        return func(**parameters)