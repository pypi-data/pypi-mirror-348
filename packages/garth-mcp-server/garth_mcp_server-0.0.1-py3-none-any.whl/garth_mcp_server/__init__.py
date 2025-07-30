import os

import garth
from mcp.server.fastmcp import FastMCP


__version__ = "0.0.1"

mcp = FastMCP("Garth - Garmin Connect", dependencies=["garth"], version=__version__)


@mcp.tool()
def get_username() -> str:
    """
    Get my Garmin Connect username
    """
    token = os.getenv("GARTH_TOKEN")

    if not token:
        return "No token found"

    try:
        garth.client.loads(token)

        return f"your username is {garth.client.username}"
    except Exception as e:
        return f"Failed to resume session: {str(e)}"


def main():
    mcp.run()


if __name__ == "__main__":
    main()
