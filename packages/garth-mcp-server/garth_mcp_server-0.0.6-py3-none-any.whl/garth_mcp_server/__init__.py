import os
from datetime import date
from functools import wraps

import garth
from mcp.server.fastmcp import FastMCP


__version__ = "0.0.6"

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
def get_connectapi_endpoint(endpoint: str) -> str | dict | None:
    """
    Get the data from a given Garmin Connect API endpoint.
    This is a generic tool that can be used to get data from any Garmin Connect API endpoint.
    """
    return garth.connectapi(endpoint)


@server.tool()
@requires_garth_session
def nightly_sleep(
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
def daily_stress(
    end_date: date | None = None, days: int = 1
) -> str | list[garth.DailyStress]:
    """
    Get daily stress data for a given date and number of days.
    If no date is provided, the current date will be used.
    If no days are provided, 1 day will be used.
    """
    return garth.DailyStress.list(end_date, days)


@server.tool()
@requires_garth_session
def weekly_stress(
    end_date: date | None = None, weeks: int = 1
) -> str | list[garth.WeeklyStress]:
    """
    Get weekly stress data for a given date and number of weeks.
    If no date is provided, the current date will be used.
    If no weeks are provided, 1 week will be used.
    """
    return garth.WeeklyStress.list(end_date, weeks)


@server.tool()
@requires_garth_session
def daily_intensity_minutes(
    end_date: date | None = None, days: int = 1
) -> str | list[garth.DailyIntensityMinutes]:
    """
    Get daily intensity minutes data for a given date and number of days.
    If no date is provided, the current date will be used.
    If no days are provided, 1 day will be used.
    """
    return garth.DailyIntensityMinutes.list(end_date, days)


@server.tool()
@requires_garth_session
def monthly_activity_summary(month: int, year: int) -> str | dict | None:
    """
    Get the monthly activity summary for a given month and year.
    """
    return garth.connectapi(f"mobile-gateway/calendar/year/{year}/month/{month}")


@server.tool()
@requires_garth_session
def snapshot(from_date: date, to_date: date) -> str | dict | None:
    """
    Get the snapshot for a given date range. This is a good starting point for
    getting data for a given date range. It can be used in combination with
    the get_connectapi_endpoint tool to get data from any Garmin Connect API
    endpoint.
    """
    return garth.connectapi(f"mobile-gateway/snapshot/detail/v2/{from_date}/{to_date}")


def main():
    server.run()


if __name__ == "__main__":
    main()
