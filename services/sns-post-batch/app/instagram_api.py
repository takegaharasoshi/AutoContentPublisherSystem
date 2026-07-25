"""Minimal Instagram Graph API client for the SNS posting batch."""

from __future__ import annotations

import json
import socket
import time
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from typing import Any

from .media_types import MEDIA_TYPE_FEED_IMAGE, MEDIA_TYPE_REEL


GRAPH_API_BASE_URL = "https://graph.facebook.com/v21.0"
REQUEST_TIMEOUT_SECONDS = 30
FEED_IMAGE_POLL_MAX_ATTEMPTS = 10
FEED_IMAGE_POLL_INTERVAL_SECONDS = 3.0
# Reel processing measured 33.5 seconds in 14-8; allow up to 10 minutes.
REEL_POLL_MAX_ATTEMPTS = 60
REEL_POLL_INTERVAL_SECONDS = 10.0


@dataclass(frozen=True)
class PollSettings:
    """Polling limits appropriate for an Instagram media type."""

    max_attempts: int
    interval_seconds: float


def resolve_poll_settings(media_type: str) -> PollSettings:
    """Return the polling settings for a post media type."""
    if media_type == MEDIA_TYPE_REEL:
        return PollSettings(REEL_POLL_MAX_ATTEMPTS, REEL_POLL_INTERVAL_SECONDS)
    return PollSettings(
        FEED_IMAGE_POLL_MAX_ATTEMPTS,
        FEED_IMAGE_POLL_INTERVAL_SECONDS,
    )


class InstagramRequestFailed(Exception):
    """Raised when Instagram returned a clear request failure."""

    def __init__(self, message: str, response: dict[str, Any] | None = None) -> None:
        super().__init__(message)
        self.response = response


class InstagramResultUnknown(Exception):
    """Raised when the result cannot be determined because no response arrived."""

    def __init__(self, message: str, response: dict[str, Any] | None = None) -> None:
        super().__init__(message)
        self.response = response


def _response_message(response: Any) -> str | None:
    """Extract the useful error message from a Graph API response."""
    if not isinstance(response, dict):
        return None
    error = response.get("error")
    if isinstance(error, dict) and isinstance(error.get("message"), str):
        return error["message"]
    for key in ("message", "error_description"):
        if isinstance(response.get(key), str):
            return response[key]
    return None


def _decode_response(response: Any) -> dict[str, Any]:
    """Decode a response body as a JSON object."""
    raw_body = response.read()
    if isinstance(raw_body, bytes):
        raw_body = raw_body.decode("utf-8")
    value = json.loads(raw_body)
    if not isinstance(value, dict):
        raise ValueError("Instagram API response must be a JSON object")
    return value


def _read_http_error_response(error: urllib.error.HTTPError) -> dict[str, Any] | None:
    """Best-effort decode of an HTTP error response body."""
    try:
        raw_body = error.read()
        if isinstance(raw_body, bytes):
            raw_body = raw_body.decode("utf-8")
        value = json.loads(raw_body)
    except (
        AttributeError,
        OSError,
        TypeError,
        UnicodeDecodeError,
        json.JSONDecodeError,
    ):
        return None
    return value if isinstance(value, dict) else None


def _request_json(
    request: urllib.request.Request,
    *,
    urlopen: Any,
    operation: str,
    duplicate_is_unknown: bool = False,
    transport_failure_is_unknown: bool = False,
) -> dict[str, Any]:
    """Send one request and classify transport and HTTP failures.

    ``transport_failure_is_unknown`` must only be set for the publish call:
    a network failure before a publish request is ever sent cannot have
    posted anything, so it is a clear failure, not an unconfirmed result.
    """
    try:
        response = urlopen(request, timeout=REQUEST_TIMEOUT_SECONDS)
    except urllib.error.HTTPError as exc:
        response_json = _read_http_error_response(exc)
        message = _response_message(response_json) or str(exc)
        if duplicate_is_unknown and _is_duplicate_publish_message(message):
            raise InstagramResultUnknown(message, response=response_json) from exc
        raise InstagramRequestFailed(message, response=response_json) from exc
    except (urllib.error.URLError, TimeoutError, socket.timeout) as exc:
        if transport_failure_is_unknown:
            raise InstagramResultUnknown(str(exc)) from exc
        raise InstagramRequestFailed(str(exc)) from exc

    try:
        response_json = _decode_response(response)
    except (
        AttributeError,
        OSError,
        TimeoutError,
        socket.timeout,
        urllib.error.URLError,
    ) as exc:
        if transport_failure_is_unknown:
            raise InstagramResultUnknown(str(exc)) from exc
        raise InstagramRequestFailed(str(exc)) from exc
    except (TypeError, UnicodeDecodeError, json.JSONDecodeError, ValueError) as exc:
        raise InstagramRequestFailed(
            f"Instagram API returned invalid JSON for {operation}",
            response=None,
        ) from exc
    finally:
        close = getattr(response, "close", None)
        if callable(close):
            close()

    status = getattr(response, "status", getattr(response, "code", None))
    if isinstance(status, int) and status >= 400:
        message = _response_message(response_json) or (
            f"Instagram API returned HTTP status {status}"
        )
        if duplicate_is_unknown and _is_duplicate_publish_message(message):
            raise InstagramResultUnknown(message, response=response_json)
        raise InstagramRequestFailed(message, response=response_json)

    return response_json


def _is_duplicate_publish_message(message: str | None) -> bool:
    """Return whether an error message indicates a duplicate publish."""
    if message is None:
        return False
    lowered = message.lower()
    return any(
        phrase in lowered
        for phrase in ("already been published", "media has already", "duplicate")
    )


def _post_request(path: str, values: dict[str, str]) -> urllib.request.Request:
    """Build a form-encoded Graph API POST request."""
    return urllib.request.Request(
        f"{GRAPH_API_BASE_URL}{path}",
        data=urllib.parse.urlencode(values).encode("utf-8"),
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        method="POST",
    )


def create_container(
    access_token: str,
    ig_user_id: str,
    media_url: str,
    caption: str,
    *,
    media_type: str = MEDIA_TYPE_FEED_IMAGE,
    urlopen: Any = urllib.request.urlopen,
) -> tuple[str, dict[str, Any]]:
    """Create an Instagram media container."""
    if media_type == MEDIA_TYPE_FEED_IMAGE:
        values = {
            "image_url": media_url,
            "caption": caption,
            "access_token": access_token,
        }
    elif media_type == MEDIA_TYPE_REEL:
        # Use Instagram's default first-frame cover for generated reels.
        values = {
            "media_type": "REELS",
            "video_url": media_url,
            "share_to_feed": "true",
            "caption": caption,
            "access_token": access_token,
        }
    else:
        raise ValueError(f"Unsupported Instagram media type: {media_type}")

    request = _post_request(
        f"/{ig_user_id}/media",
        values,
    )
    response = _request_json(
        request,
        urlopen=urlopen,
        operation="create_container",
    )
    container_id = response.get("id")
    if container_id is None:
        raise InstagramRequestFailed(
            "Instagram container response did not include an id",
            response=response,
        )
    return str(container_id), response


def poll_container_status(
    access_token: str,
    container_id: str,
    *,
    urlopen: Any = urllib.request.urlopen,
    max_attempts: int = FEED_IMAGE_POLL_MAX_ATTEMPTS,
    poll_interval_seconds: float = FEED_IMAGE_POLL_INTERVAL_SECONDS,
) -> dict[str, Any]:
    """Poll a media container until it is ready for publishing."""
    last_response: dict[str, Any] | None = None
    for attempt in range(max_attempts):
        query = urllib.parse.urlencode(
            {"fields": "status_code", "access_token": access_token}
        )
        request = urllib.request.Request(
            f"{GRAPH_API_BASE_URL}/{container_id}?{query}",
            method="GET",
        )
        response = _request_json(
            request,
            urlopen=urlopen,
            operation="poll_container_status",
        )
        last_response = response
        status_code = response.get("status_code")
        if status_code == "FINISHED":
            return response
        if status_code == "ERROR":
            raise InstagramRequestFailed(
                "Instagram container processing returned ERROR",
                response=response,
            )
        if attempt + 1 < max_attempts:
            time.sleep(poll_interval_seconds)

    raise InstagramRequestFailed(
        "Instagram container did not reach FINISHED within the polling limit",
        response=last_response,
    )


def publish_container(
    access_token: str,
    ig_user_id: str,
    container_id: str,
    *,
    urlopen: Any = urllib.request.urlopen,
) -> tuple[str, dict[str, Any]]:
    """Publish an Instagram media container."""
    request = _post_request(
        f"/{ig_user_id}/media_publish",
        {"creation_id": container_id, "access_token": access_token},
    )
    response = _request_json(
        request,
        urlopen=urlopen,
        operation="publish_container",
        duplicate_is_unknown=True,
        transport_failure_is_unknown=True,
    )
    response_message = _response_message(response)
    if _is_duplicate_publish_message(response_message):
        raise InstagramResultUnknown(response_message or "Instagram publish result is unknown", response=response)
    post_id = response.get("id")
    if post_id is None:
        raise InstagramRequestFailed(
            "Instagram publish response did not include an id",
            response=response,
        )
    return str(post_id), response
