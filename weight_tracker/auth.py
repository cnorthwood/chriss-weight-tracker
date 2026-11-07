import logging
import os
from urllib.parse import urlparse

from requests_oauthlib import OAuth2Session

logger = logging.getLogger(__name__)

AUTHORIZE_URL = "https://accounts.google.com/o/oauth2/v2/auth"
TOKEN_URL = "https://oauth2.googleapis.com/token"
SCOPES = ["https://www.googleapis.com/auth/googlehealth.health_metrics_and_measurements.readonly"]


def _log_token_response(response):
    # oauthlib hides the real cause of failures behind generic errors (e.g. "missing_token"), so keep the raw
    # response around. Successful responses contain tokens, so only log the body when the request failed.
    if not response.ok:
        logger.error("Token endpoint returned %s: %s", response.status_code, response.text)
    return response


def _redirect_uri():
    redirect_uri = os.environ.get("GOOGLE_REDIRECT_URI", "http://localhost:3000/")
    if urlparse(redirect_uri).hostname in ("localhost", "127.0.0.1"):
        # oauthlib refuses to parse an http:// callback unless told otherwise. That is only acceptable when the
        # callback never leaves this machine, so only relax it for a loopback redirect URI.
        os.environ.setdefault("OAUTHLIB_INSECURE_TRANSPORT", "1")
    return redirect_uri


def start_login(state=None):
    oauth_session = OAuth2Session(
        os.environ["GOOGLE_CLIENT_ID"],
        redirect_uri=_redirect_uri(),
        state=state,
        scope=SCOPES,
    )
    oauth_session.register_compliance_hook("access_token_response", _log_token_response)
    auth_url, state = oauth_session.authorization_url(AUTHORIZE_URL)

    return oauth_session, auth_url, state


def complete_login(oauth_session: OAuth2Session, response_url: str):
    oauth_session.fetch_token(
        TOKEN_URL,
        authorization_response=response_url,
        client_secret=os.environ["GOOGLE_CLIENT_SECRET"],
    )
