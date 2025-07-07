# Home Assistant Automation Management MCP server

This project is used to manage automations in Home Assistant by Model Context Protocol (MCP).

The solution is to wrap an FTP client in it, to list/read/write YAML files.

Then use API to trigger reload.

# Use Guide
1. Install [uv](https://github.com/astral-sh/uv) and [npm](https://docs.npmjs.com/downloading-and-installing-node-js-and-npm) if not already installed.

2. Install FTP server in Home Assistant  
   Settings -> Addons -> FTP -> Install

3. Configure FTP server username and password, enable operation permission and folder permission.  
   Settings -> Addons -> FTP -> Configuration

4. Get Long Live Token  
   User -> Security -> Long Live Token -> Create

5. Test FTP connection

6. Download this repo, configure environment file  
   ```bash
   git clone https://github.com/cavemancave/hass-automation-mcp.git
   cp .env.example .env
   # change .env
   ```

7. Change path in `claude_desktop_config.json`, test it by inspector  
   ```bash
   npx @modelcontextprotocol/inspector --config claude_desktop_config.json --server hass-automation-mcp
   ```
   Connect -> list tools -> list files -> config/ -> run tool

8. Merge `claude_desktop_config.json` into your LLM configuration

# Trouble Shooting

## Test FTP connection

```bash
yadang@yadang-ubuntu:~$ ftp 192.168.1.22
Connected to 192.168.1.22.
220 Welcome to the Hass.io FTP service.
Name (192.168.1.22:yadang): yadang
331 Please specify the password.
Password: 
230 Login successful.
Remote system type is UNIX.
Using binary mode to transfer files.
ftp> ls
229 Entering Extended Passive Mode (|||30009|)
150 Here comes the directory listing.
drwxr-xr-x    2 ftp      ftp          4096 Jun 25 16:12 addons
drwxr-xr-x    2 ftp      ftp          4096 Jun 25 16:12 backup
drwxr-xr-x    9 ftp      ftp          4096 Jul 04 14:11 config
......
226 Directory send OK.
ftp> cd config
250 Directory successfully changed.
ftp> ls
229 Entering Extended Passive Mode (|||30002|)
150 Here comes the directory listing.
-rw-r--r--    1 ftp      ftp             8 Jun 25 16:45 .HA_VERSION
drwxr-xr-x    2 ftp      ftp          4096 Jun 25 16:45 .cloud
drwxr-xr-x    3 ftp      ftp          4096 Jul 07 07:36 .storage
-rw-r--r--    1 ftp      ftp           260 Jul 04 14:11 automations.yaml
......
226 Directory send OK.
ftp> get automations.yaml
local: automations.yaml remote: automations.yaml
229 Entering Extended Passive Mode (|||30004|)
150 Opening BINARY mode data connection for automations.yaml (260 bytes).
100% |*********************************************************************|   260        4.50 MiB/s    00:00 ETA
226 Transfer complete.
260 bytes received in 00:00 (729.61 KiB/s)
ftp> quit
221
```