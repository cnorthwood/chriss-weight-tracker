from datetime import date

from weight_tracker.auth import oauth_session


def weight_info(start_date: date, end_date: date):
    session = oauth_session()
    response = session.get(
        f"https://api.fitbit.com/1/user/-/body/log/weight/date/{start_date.isoformat()}/{end_date.isoformat()}.json"
    )
    response.raise_for_status()
    return response.json()
