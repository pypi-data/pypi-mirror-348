from typing import Dict, Any
from mcp_services.watch_service import WatchService

watch_service = WatchService()

def get_tool_info() -> Dict[str, Any]:
    """返回工具信息"""
    return {
        "name": "watch_query",
        "description": "手表信息查询工具",
        "parameters": {
            "brand": {"type": "string", "required": True},
            "model": {"type": "string", "required": False}
        }
    }

def search(brand: str, model: str = None) -> Dict[str, Any]:
    """查询手表信息"""
    results = watch_service.query_watches(brand, model)
    if not results:
        return {"error": "Watch not found"}
    
    if len(results) == 1:
        return results[0]
    return {"results": results}

def handle_request(params: Dict[str, Any]) -> Dict[str, Any]:
    """处理fetch风格请求"""
    if params.get("method") == "describe":
        return get_tool_info()
    
    if "brand" in params:
        return search(params["brand"], params.get("model"))
    
    return {
        "error": "Invalid parameters",
        "expected": get_tool_info()
    }
