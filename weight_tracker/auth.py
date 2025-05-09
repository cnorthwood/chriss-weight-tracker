import os

from requests_oauthlib import OAuth2Session


def start_login():
    oauth_session = OAuth2Session(
        os.environ["FITBIT_CLIENT_ID"],
        redirect_uri=os.environ.get("FITBIT_REDIRECT_URI", "http://localhost:3000"),
        scope=["weight"]
    )
    auth_url, state = oauth_session.authorization_url("https://www.fitbit.com/oauth2/authorize")

    return oauth_session, auth_url


def complete_login(oauth_session: OAuth2Session, response_url: str):
    oauth_session.fetch_token(
       "https://api.fitbit.com/oauth2/token",
       authorization_response=response_url,
       client_secret=os.environ["FITBIT_CLIENT_SECRET"],
   )
