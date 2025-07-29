import os
import json
import base64
import logging
import requests
import time
from authlib.integrations.requests_client import OAuth2Session

from eocube import ROCS_DISCOVERY_URL, EOCUBE_CLI_CLIENT_ID

has_keyring = False
try:
    import keyring

    has_keyring = True
except ImportError as e:
    has_keyring = False

log = logging.getLogger("eocube.auth")


class EOCubeAuthException(Exception):
    pass


def _is_token_valid(token):
    try:
        payload_part = token.split(".")[1]
        # Padding base64 dacă lipsește
        padded = payload_part + "=" * (-len(payload_part) % 4)
        payload = json.loads(base64.urlsafe_b64decode(padded.encode()))
        exp = payload.get("exp")
        return exp and time.time() < exp - 30
    except Exception as e:
        log.error("⚠️ Error validating token:", e)
        return False


def get_token():
    if "ROCS_AAI_REFRESH_TOKEN" in os.environ:
        access_token = os.environ["ROCS_AAI_ACCESS_TOKEN"]
        refresh_token = os.environ["ROCS_AAI_REFRESH_TOKEN"]
    elif has_keyring:
        access_token = keyring.get_password("eocube-cli", "access-token")
        refresh_token = keyring.get_password("eocube-cli", "offline-refresh-token")
    else:
        raise NotImplementedError("Could not retrieve tokens")

    if access_token and _is_token_valid(access_token):
        log.info("✅ Found valid access token in keyring")
        return access_token
    else:
        log.warning("No token found")

    if not refresh_token:
        raise EOCubeAuthException(
            "❌ No refresh token. Please login: `eocube auth login`"
        )

    # Facem refresh cu authlib
    metadata = requests.get(ROCS_DISCOVERY_URL).json()
    token_url = metadata["token_endpoint"]

    log.warning("🔄 Token expired or missing. Trying to refresh ...")

    session = OAuth2Session(
        client_id=EOCUBE_CLI_CLIENT_ID, client_secret=None  # public client
    )

    token = session.refresh_token(token_url, refresh_token=refresh_token)

    new_access_token = token["access_token"]
    new_refresh_token = token.get("refresh_token", refresh_token)

    keyring.set_password("eocube-cli", "access-token", new_access_token)
    keyring.set_password("eocube-cli", "offline-refresh-token", new_refresh_token)

    return new_access_token
