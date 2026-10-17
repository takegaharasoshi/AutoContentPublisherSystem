"""Instagram Graph API operations used by the SNS posting batch."""

from __future__ import annotations

import time
import urllib.request
from dataclasses import dataclass
from typing import Any

from acps_shared import (
    InstagramApiError,
    InstagramRateLimited,
    InstagramRequestFailed,
    InstagramTransportError,
    get_json,
    post_form,
)

from .media_types import MEDIA_TYPE_FEED_IMAGE, MEDIA_TYPE_REEL, MEDIA_TYPE_STORY


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
    if media_type in {MEDIA_TYPE_REEL, MEDIA_TYPE_STORY}:
        return PollSettings(REEL_POLL_MAX_ATTEMPTS, REEL_POLL_INTERVAL_SECONDS)
    return PollSettings(
        FEED_IMAGE_POLL_MAX_ATTEMPTS,
        FEED_IMAGE_POLL_INTERVAL_SECONDS,
    )


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


def _is_duplicate_publish_message(message: str | None) -> bool:
    """Return whether an error message indicates a duplicate publish."""
    if message is None:
        return False
    lowered = message.lower()
    return any(
        phrase in lowered
        for phrase in ("already been published", "media has already", "duplicate")
    )


def is_transient_api_error(exc: InstagramApiError) -> bool:
    """Identify transient Graph failures without changing shared classification."""
    if isinstance(exc, InstagramTransportError):
        return False
    response = exc.response
    error = response.get("error") if isinstance(response, dict) else None
    if isinstance(error, dict) and error.get("is_transient") is True:
        return True
    if isinstance(exc, InstagramRateLimited):
        return False
    code = error.get("code") if isinstance(error, dict) else exc.code
    return type(code) is int and code in {1, 2}


def create_container(
    access_token: str,
    ig_user_id: str,
    media_url: str,
    caption: str | None = None,
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
    elif media_type == MEDIA_TYPE_STORY:
        values = {
            "media_type": "STORIES",
            "video_url": media_url,
            "access_token": access_token,
        }
    else:
        raise ValueError(f"Unsupported Instagram media type: {media_type}")

    response = post_form(
        f"/{ig_user_id}/media",
        values,
        urlopen=urlopen,
    ).payload
    container_id = response.get("id")
    if container_id is None:
        raise InstagramRequestFailed(
            "Instagram container response did not include an id",
            response=response,
        )
    return str(container_id), response


def get_container_status(
    access_token: str,
    container_id: str,
    *,
    urlopen: Any = urllib.request.urlopen,
) -> dict[str, Any]:
    """Read a container status once, without polling or retrying."""
    return get_json(
        f"/{container_id}",
        {"fields": "status_code,status", "access_token": access_token},
        urlopen=urlopen,
    ).payload


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
        response = get_container_status(
            access_token,
            container_id,
            urlopen=urlopen,
        )
        last_response = response
        status_code = response.get("status_code")
        if status_code == "FINISHED":
            return response
        if status_code in {"ERROR", "EXPIRED"}:
            # status carries Meta's reason text (e.g. "Error: ... (2207026)").
            reason = response.get("status")
            message = f"Instagram container processing returned {status_code}"
            if reason:
                message = f"{message}: {reason}"
            raise InstagramRequestFailed(message, response=response)
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
    try:
        response = post_form(
            f"/{ig_user_id}/media_publish",
            {"creation_id": container_id, "access_token": access_token},
            urlopen=urlopen,
        ).payload
    except InstagramTransportError as exc:
        raise InstagramResultUnknown(str(exc), response=exc.response) from exc
    except InstagramApiError as exc:
        if _is_duplicate_publish_message(exc.message):
            raise InstagramResultUnknown(exc.message, response=exc.response) from exc
        raise

    response_message = _response_message(response)
    if _is_duplicate_publish_message(response_message):
        raise InstagramResultUnknown(
            response_message or "Instagram publish result is unknown",
            response=response,
        )
    post_id = response.get("id")
    if post_id is None:
        raise InstagramRequestFailed(
            "Instagram publish response did not include an id",
            response=response,
        )
    return str(post_id), response
