from functools import lru_cache
import os
from time import time

from requests_oauthlib import OAuth2Session

from weight_tracker.db import load_token, save_token


def _save_token_with_expiry(token):
    token["expires_at"] = time() + token["expires_in"]
    save_token("fitbit", token)


def login():
    client_id = os.environ["FITBIT_CLIENT_ID"]
    client_secret = os.environ["FITBIT_CLIENT_SECRET"]
    oauth = OAuth2Session(
        client_id, redirect_uri="https://localhost:3000", scope=["weight"]
    )
    auth_url, state = oauth.authorization_url("https://www.fitbit.com/oauth2/authorize")
    print(f"Now visit {auth_url} and copy the URL you are redirected to")
    response_url = input("Paste the redirect URL here: ")
    token = oauth.fetch_token(
        "https://api.fitbit.com/oauth2/token",
        authorization_response=response_url,
        client_secret=client_secret,
    )
    _save_token_with_expiry(token)


@lru_cache
def oauth_session():
    client_id = os.environ["FITBIT_CLIENT_ID"]
    client_secret = os.environ["FITBIT_CLIENT_SECRET"]
    token = load_token("fitbit")
    if token is None:
        raise Exception("There is no saved token, run --login first")

    token["expires_in"] = token["expires_at"] - time()
    oauth = OAuth2Session(
        client_id,
        token=token,
        auto_refresh_url="https://api.fitbit.com/oauth2/token",
        auto_refresh_kwargs={"client_id": client_id, "client_secret": client_secret},
        token_updater=_save_token_with_expiry
    )
    return oauth
