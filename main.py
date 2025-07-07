from typing import Any
import httpx
from mcp.server.fastmcp import FastMCP

# Initialize FastMCP server
mcp = FastMCP("Home Assistant Automation Tools")

@mcp.tool()
async def list_files(path: str) -> str:
    """Get file lists for a specific path.

    Args:
        path: path to list (e.g. config/)
    """
    
    return f"stub file lists{path}"

@mcp.tool()
async def cat_file(path: str, file: str) -> str:
    """View the file content.

    Args:
        path: path of the file (e.g. config/)
        file: name of the file to view (e.g. automation.yaml)
    """
    filewithpath = f"{path}/{file}"
    return f"stub file content for {filewithpath}"

if __name__ == "__main__":
    # Initialize and run the server
    mcp.run(transport='stdio')