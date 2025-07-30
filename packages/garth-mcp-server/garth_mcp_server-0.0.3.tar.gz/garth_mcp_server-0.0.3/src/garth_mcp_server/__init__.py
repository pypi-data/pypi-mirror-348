import os
from datetime import date
from functools import wraps

import garth
from mcp.server.fastmcp import FastMCP


__version__ = "0.0.3"

server = FastMCP("Garth - Garmin Connect", dependencies=["garth"], version=__version__)


def requires_garth_session(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        token = os.getenv("GARTH_TOKEN")
        if not token:
            return "You must set the GARTH_TOKEN environment variable to use this tool"
        garth.client.loads(token)
        return func(*args, **kwargs)

    return wrapper


@server.tool()
@requires_garth_session
def get_nightly_sleep(
    end_date: date | None = None, nights: int = 1
) -> str | list[garth.SleepData]:
    """
    Get sleep stats for a given date and number of nights.
    If no date is provided, the current date will be used.
    If no nights are provided, 1 night will be used.
    """
    sleep_data = garth.SleepData.list(end_date, nights)
    for night in sleep_data:
        del night.sleep_movement
    return sleep_data


@server.tool()
@requires_garth_session
def get_daily_stress(
    end_date: date | None = None, days: int = 1
) -> str | list[garth.DailyStress]:
    """
    Get daily stress data for a given date and number of days.
    If no date is provided, the current date will be used.
    If no days are provided, 1 day will be used.
    """
    return garth.DailyStress.list(end_date, days)


def main():
    server.run()


if __name__ == "__main__":
    main()
