"""Generic HTTP helpers for the Instagram Graph API."""

from __future__ import annotations

from collections.abc import Callable, Mapping
from dataclasses import dataclass
import json
import logging
import random
import socket
import time
from typing import Any
import urllib.error
import urllib.parse
import urllib.request


GRAPH_API_VERSION = "v25.0"
GRAPH_API_BASE_URL = f"https://graph.facebook.com/{GRAPH_API_VERSION}"
REQUEST_TIMEOUT_SECONDS = 30
RATE_LIMIT_CODES = {4, 17, 32, 613}

logger = logging.getLogger(__name__)


class InstagramApiError(Exception):
    """Base class for classified Instagram Graph API failures."""

    def __init__(
        self,
        message: str,
        *,
        status: int | None = None,
        code: int | None = None,
        subcode: int | None = None,
        response: dict[str, Any] | None = None,
        headers: Mapping[str, str] | None = None,
    ) -> None:
        super().__init__(message)
        self.status = status
        self.code = code
        self.subcode = subcode
        self.message = message
        self.response = _sanitize_payload(response)
        self.headers = {
            str(key).lower(): str(value) for key, value in (headers or {}).items()
        }


class InstagramRequestFailed(InstagramApiError):
    """Raised for a general Graph API request error."""


class InstagramRateLimited(InstagramApiError):
    """Raised when the Graph API applies a rate limit."""


class InstagramInvalidMetric(InstagramApiError):
    """Raised when an insights metric is unsupported or invalid."""


class InstagramObjectUnavailable(InstagramApiError):
    """Raised when a Graph API object does not exist or cannot be read."""


class InstagramInsightsUnavailable(InstagramApiError):
    """Raised when Meta withholds insights for a media below its privacy threshold.

    Meta returns ``(#10) Not enough viewers for the media to show insights`` for
    media whose audience is too small to disclose metrics. The media exists and
    the token is valid, so this is a permanent property of that media rather
    than a fault; callers skip it instead of counting a failure.
    """


class InstagramTransportError(InstagramApiError):
    """Raised for network failures and malformed successful responses."""


@dataclass(frozen=True)
class GraphResponse:
    """Decoded Graph API response with normalized headers and usage data."""

    payload: dict[str, Any]
    headers: dict[str, str]
    app_usage: dict[str, Any] | None


def _sanitize_payload(value: Any) -> Any:
    """Remove access tokens from diagnostic response data."""
    if isinstance(value, dict):
        return {
            str(key): (
                "***" if str(key).lower() == "access_token" else _sanitize_payload(item)
            )
            for key, item in value.items()
        }
    if isinstance(value, list):
        return [_sanitize_payload(item) for item in value]
    return value


def _redact_token(value: Any, access_token: str | None) -> Any:
    """Redact the request token wherever an error response echoed it."""
    if not access_token:
        return _sanitize_payload(value)
    if isinstance(value, dict):
        return {
            str(key): _redact_token(item, access_token)
            for key, item in value.items()
        }
    if isinstance(value, list):
        return [_redact_token(item, access_token) for item in value]
    if isinstance(value, str):
        return value.replace(access_token, "***")
    return value


def _decode_json_object(raw_body: Any) -> dict[str, Any]:
    """Decode a response body and require a JSON object."""
    if isinstance(raw_body, bytes):
        raw_body = raw_body.decode("utf-8")
    value = json.loads(raw_body)
    if not isinstance(value, dict):
        raise ValueError("Instagram API response must be a JSON object")
    return value


def _normalized_headers(source: Any) -> dict[str, str]:
    """Return response headers with lowercase keys."""
    headers = getattr(source, "headers", None)
    if headers is None:
        return {}
    try:
        items = headers.items()
    except AttributeError:
        return {}
    return {str(key).lower(): str(value) for key, value in items}


def _parse_app_usage(headers: Mapping[str, str]) -> dict[str, Any] | None:
    """Best-effort parse the X-App-Usage header."""
    raw_usage = headers.get("x-app-usage")
    if raw_usage is None:
        return None
    try:
        usage = json.loads(raw_usage)
    except (TypeError, json.JSONDecodeError):
        return None
    return usage if isinstance(usage, dict) else None


def classify_graph_error(
    status: int | None,
    code: int | dict[str, Any] | None = None,
    subcode: int | None = None,
    message: str | None = None,
    response: dict[str, Any] | None = None,
    headers: Mapping[str, str] | None = None,
) -> InstagramApiError:
    """Classify an HTTP/Graph error into a stable exception type."""
    if isinstance(code, dict):
        if response is None:
            response = code
        code, extracted_subcode, extracted_message = _error_details(code)
        if subcode is None:
            subcode = extracted_subcode
        if message is None:
            message = extracted_message
    elif response is not None and code is None:
        code, extracted_subcode, extracted_message = _error_details(response)
        if subcode is None:
            subcode = extracted_subcode
        if message is None:
            message = extracted_message
    safe_message = message or (
        f"Instagram API returned HTTP status {status}"
        if status is not None
        else "Instagram API request failed"
    )
    lowered = safe_message.lower()
    error_type: type[InstagramApiError]
    if status == 429 or code in RATE_LIMIT_CODES:
        error_type = InstagramRateLimited
    elif code == 10 and "not enough viewers" in lowered:
        # Graph code 10 is the generic "permission denied", so match the message
        # too: a genuine permission error must stay a failure, not a skip.
        error_type = InstagramInsightsUnavailable
    elif (
        (status == 400 and code == 100 and subcode == 33)
        or "does not exist" in lowered
        or "cannot be loaded" in lowered
    ):
        error_type = InstagramObjectUnavailable
    elif (
        (status == 400 and code == 100 and subcode != 33)
        or "metric" in lowered
    ):
        error_type = InstagramInvalidMetric
    else:
        error_type = InstagramRequestFailed
    return error_type(
        safe_message,
        status=status,
        code=code,
        subcode=subcode,
        response=response,
        headers=headers,
    )


def _error_details(
    payload: dict[str, Any] | None,
) -> tuple[int | None, int | None, str | None]:
    """Extract Graph error code, subcode, and message."""
    if not isinstance(payload, dict):
        return None, None, None
    error = payload.get("error")
    if not isinstance(error, dict):
        return None, None, None
    code = error.get("code")
    subcode = error.get("error_subcode")
    message = error.get("message")
    return (
        code if isinstance(code, int) and not isinstance(code, bool) else None,
        subcode
        if isinstance(subcode, int) and not isinstance(subcode, bool)
        else None,
        message if isinstance(message, str) else None,
    )


def get_json(
    path: str,
    params: Mapping[str, str],
    *,
    urlopen: Any = urllib.request.urlopen,
) -> GraphResponse:
    """Send a Graph API GET request and return its decoded JSON object."""
    filtered_params = {
        key: value for key, value in params.items() if value is not None
    }
    access_token = filtered_params.get("access_token")
    query = urllib.parse.urlencode(filtered_params)
    request = urllib.request.Request(
        f"{GRAPH_API_BASE_URL}{path}?{query}",
        method="GET",
    )
    try:
        response = urlopen(request, timeout=REQUEST_TIMEOUT_SECONDS)
    except urllib.error.HTTPError as exc:
        headers = _normalized_headers(exc)
        try:
            payload = _decode_json_object(exc.read())
        except (
            AttributeError,
            OSError,
            TypeError,
            UnicodeDecodeError,
            json.JSONDecodeError,
            ValueError,
        ):
            payload = None
        payload = _redact_token(payload, access_token)
        code, subcode, message = _error_details(payload)
        raise classify_graph_error(
            exc.code,
            code,
            subcode,
            message,
            payload,
            headers,
        ) from exc
    except (urllib.error.URLError, TimeoutError, socket.timeout, OSError) as exc:
        raise InstagramTransportError(
            f"Instagram API transport failed: {type(exc).__name__}"
        ) from exc

    try:
        headers = _normalized_headers(response)
        status = getattr(response, "status", getattr(response, "code", None))
        try:
            payload = _decode_json_object(response.read())
        except (
            AttributeError,
            OSError,
            TimeoutError,
            socket.timeout,
            urllib.error.URLError,
            TypeError,
            UnicodeDecodeError,
            json.JSONDecodeError,
            ValueError,
        ) as exc:
            raise InstagramTransportError(
                "Instagram API returned an unreadable JSON response",
                status=status if isinstance(status, int) else None,
            ) from exc
    finally:
        close = getattr(response, "close", None)
        if callable(close):
            close()

    if isinstance(status, int) and status >= 400:
        payload = _redact_token(payload, access_token)
        code, subcode, message = _error_details(payload)
        raise classify_graph_error(
            status,
            code,
            subcode,
            message,
            payload,
            headers,
        )
    return GraphResponse(
        payload=payload,
        headers=headers,
        app_usage=_parse_app_usage(headers),
    )


def _maximum_numeric_usage(usage: Mapping[str, Any] | None) -> float | None:
    """Return the maximum non-boolean numeric value in a usage mapping."""
    if usage is None:
        return None
    values = [
        float(value)
        for value in usage.values()
        if isinstance(value, (int, float)) and not isinstance(value, bool)
    ]
    return max(values) if values else None


def _estimated_regain_delay(headers: Mapping[str, str]) -> float | None:
    """Extract an estimated regain time in minutes and return capped seconds."""
    raw_value = headers.get("x-business-use-case-usage")
    if raw_value is None:
        return None
    try:
        payload = json.loads(raw_value)
    except (TypeError, json.JSONDecodeError):
        return None

    def find(value: Any) -> float | None:
        if isinstance(value, dict):
            candidate = value.get("estimated_time_to_regain_access")
            if (
                isinstance(candidate, (int, float))
                and not isinstance(candidate, bool)
                and candidate >= 0
            ):
                return float(candidate)
            for item in value.values():
                found = find(item)
                if found is not None:
                    return found
        elif isinstance(value, list):
            for item in value:
                found = find(item)
                if found is not None:
                    return found
        return None

    minutes = find(payload)
    return min(minutes * 60.0, 300.0) if minutes is not None else None


class RateLimitGuard:
    """Apply proactive usage waits and bounded retry backoff to API calls."""

    def __init__(
        self,
        *,
        usage_threshold: float = 90.0,
        sleep: Callable[[float], None] = time.sleep,
        max_attempts: int = 4,
    ) -> None:
        if max_attempts < 1:
            raise ValueError("max_attempts must be at least 1")
        self.usage_threshold = usage_threshold
        self.sleep = sleep
        self.max_attempts = max_attempts
        self._last_app_usage: dict[str, Any] | None = None

    def call(self, request_callable: Callable[[], GraphResponse]) -> GraphResponse:
        """Call a request with usage-based throttling and bounded retries."""
        maximum_usage = _maximum_numeric_usage(self._last_app_usage)
        if maximum_usage is not None and maximum_usage >= self.usage_threshold:
            logger.warning(
                "Instagram API usage is above threshold; waiting 60 seconds: usage=%s",
                maximum_usage,
            )
            self.sleep(60.0)

        delays = (5.0, 15.0, 45.0)
        for attempt in range(self.max_attempts):
            try:
                response = request_callable()
                self._last_app_usage = response.app_usage
                return response
            except InstagramApiError as exc:
                retryable = isinstance(
                    exc, (InstagramRateLimited, InstagramTransportError)
                ) or (
                    isinstance(exc, InstagramRequestFailed)
                    and exc.status is not None
                    and exc.status >= 500
                )
                if not retryable or attempt + 1 >= self.max_attempts:
                    raise
                estimated_delay = _estimated_regain_delay(exc.headers)
                if estimated_delay is None:
                    delay_index = min(attempt, len(delays) - 1)
                    estimated_delay = delays[delay_index] * random.uniform(0.8, 1.2)
                logger.warning(
                    "Instagram API request will be retried: attempt=%s delay=%.1f",
                    attempt + 1,
                    estimated_delay,
                )
                self.sleep(estimated_delay)

        raise AssertionError("unreachable")
