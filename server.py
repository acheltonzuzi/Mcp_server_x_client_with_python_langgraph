# math_server.py
from mcp.server.fastmcp import FastMCP
mcp = FastMCP(name="My mcp server")
import requests
import asyncio
nomes=[]
@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers"""
    return a + b

@mcp.tool()
def multiply(a: int, b: int) -> int:
    """Multiply two numbers"""
    return a * b

@mcp.tool()
def get_creator() -> str:
    """Get creator informartion"""
    return "Achelton pambo"

@mcp.tool()
def get_kaeso_info() -> str:
    """Get ckaeso reator informartion"""
    return "Kaeso Angola"

@mcp.tool()
def add_to_list(name:str) -> list:
    """Add name to the list and show the list"""
    nomes.append(name)
    print(nomes)
    return nomes

@mcp.tool()
def get_list() -> list:
    """get the list of names"""
    return nomes

if __name__ == "__main__":
    mcp.run(transport="stdio")