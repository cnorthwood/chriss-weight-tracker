from datetime import date, datetime, timedelta

from requests_oauthlib import OAuth2Session

from weight_tracker.db import last_reading_date, insert_reading

WEIGHT_DATA_POINTS_URL = "https://health.googleapis.com/v4/users/me/dataTypes/weight/dataPoints"


def add_readings_to_database(oauth_session: OAuth2Session):
    if last_reading_date() == date.today():
        return

    # We always re-fetch the day of the last reading we have, relying on the database to skip duplicates
    range_start = last_reading_date() or date.today() - timedelta(days=365)
    for reading_time, weight_kg in weight_readings(oauth_session, range_start):
        insert_reading(reading_time, weight_kg)


def weight_readings(oauth_session: OAuth2Session, range_start: date):
    page_token = None
    while True:
        params = {
            # Civil (local) time, to match how readings have always been stored
            "filter": f'weight.sample_time.civil_time >= "{range_start.isoformat()}T00:00:00"',
        }
        if page_token:
            params["pageToken"] = page_token

        response = oauth_session.get(WEIGHT_DATA_POINTS_URL, params=params)
        response.raise_for_status()
        body = response.json()

        for data_point in body.get("dataPoints", []):
            yield _civil_datetime(data_point), data_point["weight"]["weightGrams"] / 1000

        page_token = body.get("nextPageToken")
        if not page_token:
            return


def _civil_datetime(data_point) -> datetime:
    civil_time = data_point["weight"]["sampleTime"]["civilTime"]
    day, time = civil_time["date"], civil_time["time"]
    # Zero-valued fields are omitted from the response, and we only store to the second
    return datetime(
        day["year"],
        day["month"],
        day["day"],
        time.get("hours", 0),
        time.get("minutes", 0),
        time.get("seconds", 0),
    )
