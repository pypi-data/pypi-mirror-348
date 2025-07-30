# Garmin Connect MCP server

based on [garth](https://github.com/matin/garth)

## Install

```json
{
  "mcpServers": {
    "Garth - Garmin Connect": {
      "command": "uvx",
      "args": [
        "garth-mcp-server"
      ],
      "env": {
        "GARTH_TOKEN": "<GARTH_TOKEN_STRING from garth.client.dumps()>"
      }
    }
  }
}
```

## Usage

![image](https://github.com/user-attachments/assets/91581e3f-327e-4b01-9d8b-4fdb1f8e58fe)
