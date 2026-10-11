"""Refresh the Instagram access token on a scheduled invocation."""

from __future__ import annotations

import json
import logging
import os
import time
from collections.abc import Mapping
from datetime import datetime, timedelta, timezone
from typing import Any, Callable
from urllib import error, parse, request


LOGGER = logging.getLogger(__name__)
# Lambda の既定（WARNING）では INFO が出ないため、app 配下のロガーを INFO にする。
logging.getLogger("app").setLevel(logging.INFO)
DEFAULT_REFRESH_API_BASE = "https://graph.instagram.com"
HTTP_TIMEOUT_SECONDS = 30
HTTP_RETRIES = 2
INITIAL_BACKOFF_SECONDS = 2.0


def _http_error_detail(exc: error.HTTPError, token: str, url: str) -> str:
    """Return a short, sanitized error detail from a Graph API response."""
    try:
        payload = json.loads(exc.read().decode("utf-8"))
    except Exception:
        return ""
    if not isinstance(payload, Mapping) or not isinstance(payload.get("error"), Mapping):
        return ""

    details = []
    for key in ("type", "message"):
        value = payload["error"].get(key)
        if isinstance(value, str) and value:
            for url_form in {url, parse.quote(url, safe=""), parse.quote_plus(url)}:
                value = value.replace(url_form, "[URL]")
            for token_form in {token, parse.quote(token, safe=""), parse.quote_plus(token)}:
                value = value.replace(token_form, "[REDACTED]")
            details.append(f"{key}={value}")
    return " ".join(details)[:200]


def _get_json_with_retry(
    url: str,
    *,
    token: str,
    opener: Callable[..., Any],
) -> dict[str, Any]:
    """GET a JSON object, retrying rate limits and server errors twice."""
    try:
        req = request.Request(url, method="GET")
    except Exception:
        raise RuntimeError("Token refresh API request could not be prepared") from None

    for attempt in range(HTTP_RETRIES + 1):
        try:
            with opener(req, timeout=HTTP_TIMEOUT_SECONDS) as response:
                raw_body = response.read()
            break
        except error.HTTPError as exc:
            if (exc.code == 429 or 500 <= exc.code <= 599) and attempt < HTTP_RETRIES:
                exc.close()
                time.sleep(INITIAL_BACKOFF_SECONDS * 2**attempt)
                continue
            detail = _http_error_detail(exc, token, req.full_url)
            status = exc.code
            exc.close()
            LOGGER.error("Token refresh API failed: status=%s%s", status,
                         f" {detail}" if detail else "")
            raise RuntimeError("Token refresh API request failed") from None
        except error.URLError:
            raise RuntimeError("Token refresh API connection failed") from None
        except Exception:
            raise RuntimeError("Token refresh API request failed") from None
    else:
        raise RuntimeError("Token refresh API request failed")

    try:
        payload = json.loads(raw_body.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError):
        raise RuntimeError("Token refresh API returned invalid JSON") from None
    if not isinstance(payload, dict):
        raise RuntimeError("Token refresh API response must be a JSON object")
    return payload


def refresh_token(
    secret_arn: str,
    refresh_api_base: str = DEFAULT_REFRESH_API_BASE,
    *,
    client: Any = None,
    now: Callable[[], datetime] | None = None,
    opener: Callable[..., Any] | None = None,
) -> dict[str, Any]:
    """Refresh and store the token while preserving every other secret field.

    Args:
        secret_arn: Secrets Manager ARN containing the comment reply credentials.
        refresh_api_base: Instagram Graph API base URL.
        client: Optional Secrets Manager client, primarily for tests.
        now: Optional UTC clock function, primarily for tests.
        opener: Optional urllib opener, primarily for tests.

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
    # 本番面は 21-7 で初回投入するまで空のため、失敗にせず更新を見送る。
    if not token.strip():
        LOGGER.info("Token refresh skipped: ig_access_token is not set")
        return {"skipped": "token_not_set"}

    query = parse.urlencode({
        "grant_type": "ig_refresh_token",
        "access_token": token,
    })
    url = f"{refresh_api_base.rstrip('/')}/refresh_access_token?{query}"
    payload = _get_json_with_retry(url, token=token, opener=opener or request.urlopen)

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
    """Refresh the comment reply token for a scheduled Lambda invocation."""
    secret_arn = os.environ.get("SECRET_ARN")
    if not secret_arn:
        raise ValueError("SECRET_ARN is required")
    refresh_api_base = os.environ.get("REFRESH_API_BASE", DEFAULT_REFRESH_API_BASE)
    return refresh_token(secret_arn, refresh_api_base)
