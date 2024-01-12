from datetime import date, timedelta, datetime, time

from weight_tracker.auth import oauth_session


def weight_readings(range_start: date | None, range_end: date | None):
    for start_date, end_date in _chunked_date_ranges(range_start, range_end):
        session = oauth_session()
        response = session.get(
            f"https://api.fitbit.com/1/user/-/body/log/weight/date/{start_date.isoformat()}/{end_date.isoformat()}.json"
        )
        response.raise_for_status()
        for reading in response.json()["weight"]:
            yield reading


# Fitbit doesn't let us request more than 30 days at a time, so chunk this up into start/end pairs no more
# than 30 days long
def _chunked_date_ranges(start_date: date | None, end_date: date | None):
    if end_date is None:
        end_date = date.today()
    if start_date is None:
        start_date = end_date - timedelta(days=365)

    if end_date - start_date > timedelta(days=30):
        yield end_date - timedelta(days=30), end_date
        yield from _chunked_date_ranges(start_date, end_date - timedelta(days=31))
    else:
        yield start_date, end_date


def reading_datetime(reading):
    return datetime.combine(
        date.fromisoformat(reading["date"]), time.fromisoformat(reading["time"])
    )
