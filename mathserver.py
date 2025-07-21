from mcp.server.fastmcp import FastMCP
mcp=FastMCP("Math")

@mcp.tool()
def add(a:int,b:int)->int:
    """add a and b
    Args:
        a(int): 1st integer
        
        b(int): 2nd integer
    return:
        
        int: output_int    """
    return a+b

@mcp.tool()
def multiply(a:int,b:int)->int:
    """multiply a and b
    Args:
        a(int): 1st integer
        
        b(int): 2nd integer
    return:
        
        int: output_int    """
    return a*b

if __name__=="__main__":
    mcp.run(transport="stdio")
