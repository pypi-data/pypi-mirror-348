import os
from datetime import date

import garth
from mcp.server.fastmcp import FastMCP


__version__ = "0.0.2"

server = FastMCP("Garth - Garmin Connect", dependencies=["garth"], version=__version__)


@server.tool()
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


@server.tool()
def get_sleep_stats(
    end_date: date | None = None, nights: int = 1
) -> str | list[garth.SleepData]:
    """
    Get sleep stats for a given date and number of nights.
    If no date is provided, the current date will be used.
    If no nights are provided, 1 night will be used.
    """
    token = os.getenv("GARTH_TOKEN")

    if not token:
        return "No token found"

    try:
        garth.client.loads(token)

        sleep_data = garth.SleepData.list(end_date, nights)

        for night in sleep_data:
            del night.sleep_movement

        return sleep_data
    except Exception as e:
        return f"Failed to get sleep stats: {str(e)}"


def main():
    server.run()


if __name__ == "__main__":
    main()
