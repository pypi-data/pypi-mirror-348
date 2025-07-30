# server.py
from mcp.server.fastmcp import FastMCP
from api.schedule_query_api import query_schedule

# Create an MCP server
mcp = FastMCP("schedule_manage")

# Add an addition tool
@mcp.tool()
async def schedule_query(tt: str) -> str:
    """查询本人的日程事项信息
    
    Args:
        tt: 令牌
    
    Returns:
        str: 日程事项列表
    
    """
    return query_schedule(tt)

if __name__ == "__main__":
    mcp.run(transport='stdio')