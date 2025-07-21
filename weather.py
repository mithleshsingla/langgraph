from mcp.server.fastmcp import FastMCP
mcp=FastMCP("weather")

@mcp.tool()
async def get_weather(location:str)->str:
    """get weather at location"""
    return "raining"

if __name__=="__main__":
    mcp.run(transport="streamable-http")

