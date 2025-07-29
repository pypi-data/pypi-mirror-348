from typing import Dict, Any

def example_tool(param1: str, param2: float = None) -> Dict[str, Any]:
    """Example tool implementation"""
    try:
        # Tool logic here
        result = f"Processed {param1} with {param2 if param2 else 'default'}"
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}

def get_tool_info() -> Dict[str, Any]:
    """Return tool information"""
    return {
        "name": "my_tool.example",
        "description": "Example tool for MCP server",
        "parameters": {
            "param1": {"type": "string", "required": True},
            "param2": {"type": "number", "required": False}
        }
    }

def handle_request(params: Dict[str, Any]) -> Dict[str, Any]:
    """Handle MCP request"""
    if params.get("method") == "describe":
        return get_tool_info()
    
    if all(k in params for k in ["param1"]):
        return example_tool(params["param1"], params.get("param2"))
    
    return {
        "error": "Invalid parameters",
        "expected": get_tool_info()
    }
