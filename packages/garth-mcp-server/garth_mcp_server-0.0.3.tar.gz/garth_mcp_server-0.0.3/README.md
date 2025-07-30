# Garmin Connect MCP server

Based on [garth](https://github.com/matin/garth)

![image](https://github.com/user-attachments/assets/14221e6f-5f65-4c21-bc7a-2147c1c9efc1)

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
        "GARTH_TOKEN": "<output of `uvx garth login`>"
      }
    }
  }
}
```

Make sure the path for the `uvx` command is fully scoped as MCP doesn't
use the same PATH your shell does. On macOS, it's typically
`/Users/{user}/.local/bin/uvx`.

## Tools

- sleep
- stress
