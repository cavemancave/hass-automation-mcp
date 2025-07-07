# Home Assistant Automation Control MCP server

this project is used to control automation in home assistant by model context protocol(MCP)

solution is to wrap a ftp client in it, to list, cat, write, yaml files.

then use api to trigger reload.

## Manual Debug test
npx @modelcontextprotocol/inspector --config claude_desktop_config.json --server hass-automation-mcp