"""Refresh the Instagram access token on a scheduled invocation."""

from __future__ import annotations

import json
import logging
import os
from datetime import datetime, timedelta, timezone
from typing import Any, Callable

from app import graph_api


LOGGER = logging.getLogger(__name__)
# Lambda の既定（WARNING）では INFO が出ないため、app 配下のロガーを INFO にする。
logging.getLogger("app").setLevel(logging.INFO)
DEFAULT_REFRESH_API_BASE = "https://graph.instagram.com"


def refresh_token(
    secret_arn: str,
    refresh_api_base: str = DEFAULT_REFRESH_API_BASE,
    *,
    client: Any = None,
    now: Callable[[], datetime] | None = None,
) -> dict[str, Any]:
    """Refresh and store the token while preserving every other secret field.

    Args:
        secret_arn: Secrets Manager ARN containing the coach reply credentials.
        refresh_api_base: Instagram Graph API base URL.
        client: Optional Secrets Manager client, primarily for tests.
        now: Optional UTC clock function, primarily for tests.

    Returns:
        The new expiration timestamp and the API-provided lifetime in seconds,
        or ``{"skipped": "token_not_set"}`` when no token has been stored yet.

    Raises:
        ValueError: If the secret ARN is missing or the token is not a string.
        RuntimeError: If the Graph API response or request is invalid.
    """
    if not secret_arn:
        raise ValueError("SECRET_ARN is required")
    if client is None:
        import boto3

        client = boto3.client("secretsmanager")

    result = client.get_secret_value(SecretId=secret_arn)
    secret_string = result.get("SecretString")
    if not isinstance(secret_string, str):
        raise ValueError("SecretString must contain a JSON object")
    secret_data = json.loads(secret_string)
    if not isinstance(secret_data, dict):
        raise ValueError("SecretString must contain a JSON object")

    token = secret_data.get("ig_access_token", "")
    if not isinstance(token, str):
        raise ValueError("ig_access_token must be a string")
    # Secret の初回投入前は、失敗にせず更新を見送る。
    if not token.strip():
        LOGGER.info("Token refresh skipped: ig_access_token is not set")
        return {"skipped": "token_not_set"}

    payload = graph_api.refresh_token(token, base_url=refresh_api_base)

    new_token = payload.get("access_token")
    expires_in = payload.get("expires_in")
    if not isinstance(new_token, str) or not new_token.strip():
        raise RuntimeError("Token refresh API response lacks access_token")
    if isinstance(expires_in, bool) or not isinstance(expires_in, int) or expires_in <= 0:
        raise RuntimeError("Token refresh API response has invalid expires_in")

    current_time = (now or (lambda: datetime.now(timezone.utc)))()
    if current_time.tzinfo is None:
        current_time = current_time.replace(tzinfo=timezone.utc)
    expires_at = current_time.astimezone(timezone.utc) + timedelta(seconds=expires_in)
    token_expires_at = expires_at.strftime("%Y-%m-%dT%H:%M:%SZ")
    secret_data["ig_access_token"] = new_token
    secret_data["token_expires_at"] = token_expires_at

    client.put_secret_value(
        SecretId=secret_arn,
        SecretString=json.dumps(secret_data, ensure_ascii=False),
    )
    LOGGER.info("Token refresh succeeded: token_expires_at=%s expires_in=%s",
                token_expires_at, expires_in)
    return {"token_expires_at": token_expires_at, "expires_in": expires_in}


def lambda_handler(event: Any, context: Any) -> dict[str, Any]:
    """Refresh the coach reply token for a scheduled Lambda invocation."""
    secret_arn = os.environ.get("SECRET_ARN")
    if not secret_arn:
        raise ValueError("SECRET_ARN is required")
    refresh_api_base = os.environ.get("REFRESH_API_BASE", DEFAULT_REFRESH_API_BASE)
    return refresh_token(secret_arn, refresh_api_base)
