
import os
from dotenv import load_dotenv
from ftplib import FTP
from typing import List
from mcp.server.fastmcp import FastMCP

# Load environment variables from .env file if present
load_dotenv()

FTP_HOST = os.getenv("HA_FTP_HOST")
FTP_USER = os.getenv("HA_FTP_USER")
FTP_PASS = os.getenv("HA_FTP_PASS")

def get_ftp() -> FTP:
    ftp = FTP()
    ftp.connect(FTP_HOST)
    ftp.login(FTP_USER, FTP_PASS)
    return ftp

def ftp_list_files(path: str) -> List[str]:
    """List files in a given FTP directory."""
    ftp = get_ftp()
    try:
        ftp.cwd(path)
        files = ftp.nlst()  # List files in the current directory
    except Exception as e:
        print(f"Error listing files in {path}: {e}")
        files = []
    finally:
        ftp.quit()
    return files

def ftp_cat_file(path: str, file: str) -> str:
    """Retrieve the content of a file from the FTP server."""
    ftp = get_ftp()
    file_path = f"{path}/{file}"
    try:
        with open(file, 'wb') as local_file:
            ftp.retrbinary(f"RETR {file_path}", local_file.write)
        with open(file, 'r') as local_file:
            content = local_file.read()
    except Exception as e:
        print(f"Error retrieving file {file_path}: {e}")
        content = ""
    finally:
        ftp.quit()
    return content

# Initialize FastMCP server
mcp = FastMCP("Home Assistant Automation Tools")

@mcp.tool()
async def list_files(path: str) -> str:
    """Get file lists for a specific path.

    Args:
        path: path to list (e.g. config/)
    """
    files = ftp_list_files(path)
    if not files:
        return f"No files found in {path}"
    return "\n".join(files)

@mcp.tool()
async def cat_file(path: str, file: str) -> str:
    """View the file content.

    Args:
        path: path of the file (e.g. config/)
        file: name of the file to view (e.g. automations.yaml)
    """
    content = ftp_cat_file(path, file)
    if not content:
        return f"File {file} not found in {path}"
    return content

if __name__ == "__main__":
    # Initialize and run the server
    mcp.run(transport='stdio')