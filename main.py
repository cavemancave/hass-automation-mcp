import os
from dotenv import load_dotenv
from ftplib import FTP
from typing import List
import requests
from mcp.server.fastmcp import FastMCP

# Load environment variables from .env file if present
load_dotenv()

FTP_HOST = os.getenv("HA_FTP_HOST")
FTP_USER = os.getenv("HA_FTP_USER")
FTP_PASS = os.getenv("HA_FTP_PASS")
HA_URL = os.getenv("HA_URL")
HA_TOKEN = os.getenv("HA_TOKEN")

FTP_TMP_DIR = "ftp_tmp"
os.makedirs(FTP_TMP_DIR, exist_ok=True)

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

def ftp_read_file(path: str, file: str) -> str:
    """Retrieve the content of a file from the FTP server."""
    ftp = get_ftp()
    file_path = f"{path}/{file}"
    local_file_path = os.path.join(FTP_TMP_DIR, file)
    try:
        with open(local_file_path, 'wb') as local_file:
            ftp.retrbinary(f"RETR {file_path}", local_file.write)
        with open(local_file_path, 'r') as local_file:
            content = local_file.read()
    except Exception as e:
        print(f"Error retrieving file {file_path}: {e}")
        content = ""
    finally:
        ftp.quit()
    return content

def ftp_write_file(path: str, file: str, content: str) -> bool:
    """Write content to a file on the FTP server."""
    ftp = get_ftp()
    file_path = f"{path}/{file}"
    local_file_path = os.path.join(FTP_TMP_DIR, file)
    try:
        with open(local_file_path, 'w') as local_file:
            local_file.write(content)
        with open(local_file_path, 'rb') as local_file:
            ftp.storbinary(f"STOR {file_path}", local_file)
        return True
    except Exception as e:
        print(f"Error writing file {file_path}: {e}")
        return False
    finally:
        ftp.quit()
        

# Check all the YAML config files are valid 
# via POST /api/config/core/check_config
def check_config() -> bool:
    """Check if the Home Assistant configuration is valid."""
    
    headers = {
        "Authorization": f"Bearer {HA_TOKEN}",
        "Content-Type": "application/json",
    }
    try:
        response = requests.post(f"{HA_URL}/api/config/core/check_config", headers=headers)
        if response.status_code == 200:
            return True
        else:
            print(f"Configuration check failed: {response.text}")
            return False
    except Exception as e:
        print(f"Error checking configuration: {e}")
        return False

#  Reload automation YAML files via POST /api/services/automation/reload
def reload_automations() -> bool:
    """Reload automations in Home Assistant."""
    
    headers = {
        "Authorization": f"Bearer {HA_TOKEN}",
        "Content-Type": "application/json",
    }
    try:
        response = requests.post(f"{HA_URL}/api/services/automation/reload", headers=headers)
        if response.status_code == 200:
            return True
        else:
            print(f"Failed to reload automations: {response.text}")
            return False
    except Exception as e:
        print(f"Error reloading automations: {e}")
        return False


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
async def read_file(path: str, file: str) -> str:
    """View the file content.

    Args:
        path: path of the file (e.g. config/)
        file: name of the file to view (e.g. automations.yaml)
    """
    content = ftp_read_file(path, file)
    if not content:
        return f"File {file} not found in {path}"
    return content

@mcp.tool()
async def write_file(path: str, file: str, content: str) -> str:
    """Write content to a file.

    Args:
        path: path of the file (e.g. config/)
        file: name of the file to write (e.g. automations.yaml)
        content: content to write to the file
    """
    success = ftp_write_file(path, file, content)
    if success:
        return f"File {file} written successfully to {path}"
    else:
        return f"Failed to write file {file} to {path}"             

@mcp.tool()
async def check_config() -> str:
    """Check if the Home Assistant configuration is valid."""
    if check_config():
        return "Configuration is valid."
    else:
        return "Configuration is invalid."
    
@mcp.tool()
async def reload_automations() -> str:
    """Reload automations in Home Assistant."""
    if reload_automations():
        return "Automations reloaded successfully."
    else:
        return "Failed to reload automations."

 
if __name__ == "__main__":
    # Initialize and run the server
    mcp.run(transport='stdio')