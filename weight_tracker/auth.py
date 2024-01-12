from functools import lru_cache
import os

from requests_oauthlib import OAuth2Session


@lru_cache
def oauth_session():
    client_id = os.environ["FITBIT_CLIENT_ID"]
    client_secret = os.environ["FITBIT_CLIENT_SECRET"]
    oauth = OAuth2Session(client_id, redirect_uri="https://localhost:3000", scope=["weight"])
    auth_url, state = oauth.authorization_url("https://www.fitbit.com/oauth2/authorize")
    print(f"Now visit {auth_url} and copy the URL you are redirected to")
    response_url = input("Paste the redirect URL here: ")
    oauth.fetch_token("https://api.fitbit.com/oauth2/token",
                      authorization_response=response_url,
                      client_secret=client_secret)
    return oauth
