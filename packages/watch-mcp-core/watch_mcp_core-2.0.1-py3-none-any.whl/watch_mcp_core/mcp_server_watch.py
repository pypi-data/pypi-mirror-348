from mcp.server.fastmcp import FastMCP
from mcp_services.watch_service import WatchService, WatchItem
import json
from pathlib import Path

# Create an MCP server
mcp = FastMCP("Watch-Price-Query")
watch_service = WatchService()

@mcp.tool()
def add_watch(watch: WatchItem):
    """Add a new watch to the database"""
    return watch_service.add_watch(watch)

@mcp.tool()
def query_watches(brand: str, model: str = None):
    """Query watches by brand (required) and optionally by model"""
    return watch_service.query_watches(brand, model)

@mcp.resource('http://localhost/mcp-config')  # 使用完整URL格式
def get_config():
    """Return MCP service configuration"""
    config_path = Path(__file__).parent / 'manifest.json'
    with open(config_path) as f:
        return json.load(f)

if __name__ == "__main__":
    print("Watch Price Query Server running")
    mcp.run(transport='stdio')  # 使用标准IO传输方式
