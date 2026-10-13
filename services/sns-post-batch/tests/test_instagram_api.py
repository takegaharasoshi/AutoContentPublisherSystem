"""Tests for the SNS posting Instagram Graph API operations."""

from __future__ import annotations

from io import BytesIO
import json
import urllib.error
import urllib.parse

import pytest

from acps_shared import (
    InstagramApiError,
    InstagramRequestFailed,
    InstagramTransportError,
)
import app.instagram_api as instagram_api


class FakeResponse:
    """Minimal HTTP response fake."""

    def __init__(self, payload: dict, status: int = 200) -> None:
        self.payload = payload
        self.status = status
        self.closed = False

    def read(self) -> bytes:
        """Return the encoded JSON body."""
        return json.dumps(self.payload).encode("utf-8")

    def close(self) -> None:
        """Record response cleanup."""
        self.closed = True


def _recording_urlopen(responses: list[object]):
    """Build a fake urlopen that records requests and timeouts."""
    calls: list[tuple[object, int]] = []

    def urlopen(request, *, timeout: int):
        calls.append((request, timeout))
        response = responses.pop(0)
        if isinstance(response, BaseException):
            raise response
        return response

    urlopen.calls = calls
    return urlopen


def _http_error(path: str, status: int, payload: dict) -> urllib.error.HTTPError:
    """Build a Graph API HTTP error with a JSON body."""
    return urllib.error.HTTPError(
        f"https://graph.facebook.com/v25.0{path}",
        status,
        "bad request",
        {},
        BytesIO(json.dumps(payload).encode("utf-8")),
    )


def test_create_container_posts_expected_graph_parameters() -> None:
    """Feed image creation uses the shared v25 endpoint and form POST."""
    urlopen = _recording_urlopen([FakeResponse({"id": "container"})])

    assert instagram_api.create_container(
        "token",
        "ig-user",
        "https://s3.example/image.jpg",
        "caption #tag",
        urlopen=urlopen,
    ) == ("container", {"id": "container"})

    request, timeout = urlopen.calls[0]
    assert timeout == 30
    assert request.full_url == "https://graph.facebook.com/v25.0/ig-user/media"
    assert request.get_method() == "POST"
    assert request.get_header("Content-type") == "application/x-www-form-urlencoded"
    assert urllib.parse.parse_qs(request.data.decode()) == {
        "access_token": ["token"],
        "image_url": ["https://s3.example/image.jpg"],
        "caption": ["caption #tag"],
    }


def test_create_container_posts_reel_graph_parameters() -> None:
    """Reel creation sends the required video fields without cover overrides."""
    urlopen = _recording_urlopen([FakeResponse({"id": "container"})])

    assert instagram_api.create_container(
        "token",
        "ig-user",
        "https://s3.example/video.mp4",
        "caption #tag",
        media_type="reel",
        urlopen=urlopen,
    ) == ("container", {"id": "container"})

    request, _ = urlopen.calls[0]
    values = urllib.parse.parse_qs(request.data.decode())
    assert values == {
        "access_token": ["token"],
        "media_type": ["REELS"],
        "video_url": ["https://s3.example/video.mp4"],
        "share_to_feed": ["true"],
        "caption": ["caption #tag"],
    }
    assert "image_url" not in values
    assert "cover_url" not in values
    assert "thumb_offset" not in values


def test_create_container_posts_story_without_caption_or_feed_options() -> None:
    """Story creation sends only the Graph API fields supported for stories."""
    urlopen = _recording_urlopen([FakeResponse({"id": "story-container"})])

    assert instagram_api.create_container(
        "token",
        "ig-user",
        "https://s3.example/video.mp4",
        media_type="story",
        urlopen=urlopen,
    ) == ("story-container", {"id": "story-container"})

    request, _ = urlopen.calls[0]
    values = urllib.parse.parse_qs(request.data.decode())
    assert values == {
        "access_token": ["token"],
        "media_type": ["STORIES"],
        "video_url": ["https://s3.example/video.mp4"],
    }
    assert "caption" not in values
    assert "share_to_feed" not in values
    assert "cover_url" not in values
    assert "thumb_offset" not in values


def test_create_container_rejects_unknown_media_type() -> None:
    """Unsupported media types are rejected before an API request is sent."""
    with pytest.raises(ValueError, match="Unsupported Instagram media type"):
        instagram_api.create_container(
            "token",
            "ig-user",
            "https://s3.example/media",
            "caption",
            media_type="unknown",
        )


def test_create_container_missing_id_is_shared_request_failure() -> None:
    """A successful response without a container ID carries its payload."""
    payload = {"unexpected": "value"}
    with pytest.raises(InstagramRequestFailed) as caught:
        instagram_api.create_container(
            "token",
            "ig-user",
            "https://image",
            urlopen=_recording_urlopen([FakeResponse(payload)]),
        )

    assert str(caught.value) == "Instagram container response did not include an id"
    assert caught.value.response == payload


def test_resolve_poll_settings_uses_reel_and_image_defaults() -> None:
    """Reels receive the longer processing polling window."""
    assert instagram_api.resolve_poll_settings("reel") == instagram_api.PollSettings(
        60, 10.0
    )
    assert instagram_api.resolve_poll_settings(
        "feed_image"
    ) == instagram_api.PollSettings(10, 3.0)
    assert instagram_api.resolve_poll_settings("story") == instagram_api.PollSettings(
        60, 10.0
    )


def test_publish_container_posts_expected_graph_parameters() -> None:
    """Publishing uses media_publish and returns the platform post ID."""
    urlopen = _recording_urlopen([FakeResponse({"id": "post"})])

    assert instagram_api.publish_container(
        "token", "ig-user", "container", urlopen=urlopen
    ) == ("post", {"id": "post"})

    request, timeout = urlopen.calls[0]
    assert timeout == 30
    assert request.full_url == (
        "https://graph.facebook.com/v25.0/ig-user/media_publish"
    )
    assert request.get_method() == "POST"
    assert urllib.parse.parse_qs(request.data.decode()) == {
        "access_token": ["token"],
        "creation_id": ["container"],
    }


def test_create_container_http_error_is_shared_api_error() -> None:
    """A normal Graph HTTP error propagates with its shared type and response."""
    urlopen = _recording_urlopen(
        [_http_error("/ig-user/media", 400, {"error": {"message": "invalid image"}})]
    )

    with pytest.raises(InstagramRequestFailed) as raised:
        instagram_api.create_container(
            "token", "ig-user", "https://image", "caption", urlopen=urlopen
        )

    assert str(raised.value) == "invalid image"
    assert raised.value.response == {"error": {"message": "invalid image"}}
    assert len(urlopen.calls) == 1


def test_duplicate_publish_http_error_is_result_unknown() -> None:
    """A duplicate publish response may mean that the post already exists."""
    urlopen = _recording_urlopen(
        [
            _http_error(
                "/ig-user/media_publish",
                400,
                {"error": {"message": "Media has already been published"}},
            )
        ]
    )

    with pytest.raises(instagram_api.InstagramResultUnknown) as raised:
        instagram_api.publish_container(
            "token", "ig-user", "container", urlopen=urlopen
        )

    assert raised.value.response == {
        "error": {"message": "Media has already been published"}
    }
    assert len(urlopen.calls) == 1


def test_non_duplicate_publish_api_error_propagates_as_shared_error() -> None:
    """A clear API rejection is not converted to an unknown result."""
    urlopen = _recording_urlopen(
        [
            _http_error(
                "/ig-user/media_publish",
                400,
                {"error": {"message": "invalid creation_id"}},
            )
        ]
    )

    with pytest.raises(InstagramApiError, match="invalid creation_id"):
        instagram_api.publish_container(
            "token", "ig-user", "container", urlopen=urlopen
        )
    assert len(urlopen.calls) == 1


@pytest.mark.parametrize(
    "transport_error", [urllib.error.URLError("offline"), TimeoutError()]
)
def test_publish_container_transport_error_is_result_unknown(
    transport_error: BaseException,
) -> None:
    """A network failure after a publish request makes the result unknown."""
    urlopen = _recording_urlopen([transport_error])

    with pytest.raises(instagram_api.InstagramResultUnknown) as raised:
        instagram_api.publish_container(
            "token", "ig-user", "container", urlopen=urlopen
        )

    assert raised.value.response is None
    assert len(urlopen.calls) == 1


def test_publish_container_unreadable_response_is_result_unknown() -> None:
    """A response read failure after publishing is also an unknown result."""
    response = FakeResponse({})
    response.read = lambda: (_ for _ in ()).throw(TimeoutError("read failed"))
    urlopen = _recording_urlopen([response])

    with pytest.raises(instagram_api.InstagramResultUnknown) as raised:
        instagram_api.publish_container(
            "token", "ig-user", "container", urlopen=urlopen
        )

    assert isinstance(raised.value.__cause__, InstagramTransportError)
    assert raised.value.response is None


@pytest.mark.parametrize(
    "payload",
    [
        {"error": {"message": "This media is a duplicate"}},
        {"message": "Media has already been published"},
        {"error_description": "Already been published"},
    ],
)
def test_duplicate_message_in_success_response_is_result_unknown(payload: dict) -> None:
    """Duplicate messages in a 2xx body remain unconfirmed results."""
    with pytest.raises(instagram_api.InstagramResultUnknown):
        instagram_api.publish_container(
            "token",
            "ig-user",
            "container",
            urlopen=_recording_urlopen([FakeResponse(payload)]),
        )


def test_publish_container_missing_id_is_shared_request_failure() -> None:
    """A 2xx publish response without an ID is a known request failure."""
    payload = {"status": "ok"}
    with pytest.raises(InstagramRequestFailed) as raised:
        instagram_api.publish_container(
            "token",
            "ig-user",
            "container",
            urlopen=_recording_urlopen([FakeResponse(payload)]),
        )

    assert str(raised.value) == "Instagram publish response did not include an id"
    assert raised.value.response == payload


def test_poll_container_status_retries_until_finished(monkeypatch) -> None:
    """Polling waits through intermediate states and returns the final JSON."""
    urlopen = _recording_urlopen(
        [
            FakeResponse({"status_code": "IN_PROGRESS"}),
            FakeResponse({"status_code": "FINISHED"}),
        ]
    )
    sleep = []
    monkeypatch.setattr(instagram_api.time, "sleep", sleep.append)

    assert instagram_api.poll_container_status(
        "token",
        "container",
        urlopen=urlopen,
        max_attempts=2,
        poll_interval_seconds=3,
    ) == {"status_code": "FINISHED"}
    assert sleep == [3]
    assert len(urlopen.calls) == 2
    request, timeout = urlopen.calls[0]
    assert timeout == 30
    assert request.get_method() == "GET"
    assert request.full_url.startswith("https://graph.facebook.com/v25.0/container?")
    query = urllib.parse.parse_qs(urllib.parse.urlsplit(request.full_url).query)
    assert query == {"fields": ["status_code,status"], "access_token": ["token"]}


def test_poll_container_status_uses_reel_interval(monkeypatch) -> None:
    """The resolved reel settings wait ten seconds between checks."""
    urlopen = _recording_urlopen(
        [
            FakeResponse({"status_code": "IN_PROGRESS"}),
            FakeResponse({"status_code": "FINISHED"}),
        ]
    )
    sleep = []
    monkeypatch.setattr(instagram_api.time, "sleep", sleep.append)
    settings = instagram_api.resolve_poll_settings("reel")

    assert instagram_api.poll_container_status(
        "token",
        "container",
        urlopen=urlopen,
        max_attempts=settings.max_attempts,
        poll_interval_seconds=settings.interval_seconds,
    ) == {"status_code": "FINISHED"}
    assert sleep == [10.0]


def test_poll_container_status_error_is_shared_failure() -> None:
    """An explicit ERROR status stops polling and carries its response."""
    urlopen = _recording_urlopen([FakeResponse({"status_code": "ERROR"})])

    with pytest.raises(InstagramRequestFailed) as raised:
        instagram_api.poll_container_status(
            "token", "container", urlopen=urlopen, max_attempts=10
        )

    assert str(raised.value) == "Instagram container processing returned ERROR"
    assert raised.value.response == {"status_code": "ERROR"}
    assert len(urlopen.calls) == 1


def test_poll_container_status_error_includes_reason() -> None:
    """The ERROR reason from the status field is kept in message and response."""
    payload = {
        "status_code": "ERROR",
        "status": "Error: Media upload has failed with error code 2207026",
        "id": "container",
    }
    urlopen = _recording_urlopen([FakeResponse(payload)])

    with pytest.raises(InstagramRequestFailed) as raised:
        instagram_api.poll_container_status(
            "token", "container", urlopen=urlopen, max_attempts=10
        )

    assert str(raised.value) == (
        "Instagram container processing returned ERROR: "
        "Error: Media upload has failed with error code 2207026"
    )
    assert raised.value.response == payload
    assert len(urlopen.calls) == 1


def test_poll_container_status_limit_preserves_attempt_and_sleep_counts(
    monkeypatch,
) -> None:
    """Polling sleeps only between attempts and returns the last payload."""
    urlopen = _recording_urlopen(
        [FakeResponse({"status_code": "IN_PROGRESS"}) for _ in range(3)]
    )
    sleeps: list[float] = []
    monkeypatch.setattr(instagram_api.time, "sleep", sleeps.append)

    with pytest.raises(InstagramRequestFailed) as raised:
        instagram_api.poll_container_status(
            "token",
            "container",
            urlopen=urlopen,
            max_attempts=3,
            poll_interval_seconds=2.5,
        )

    assert str(raised.value) == (
        "Instagram container did not reach FINISHED within the polling limit"
    )
    assert raised.value.response == {"status_code": "IN_PROGRESS"}
    assert len(urlopen.calls) == 3
    assert sleeps == [2.5, 2.5]


def test_poll_container_status_api_and_transport_errors_are_shared() -> None:
    """Shared HTTP and transport failures propagate from a poll request."""
    api_urlopen = _recording_urlopen(
        [_http_error("/container", 400, {"error": {"message": "invalid container"}})]
    )
    with pytest.raises(InstagramRequestFailed, match="invalid container"):
        instagram_api.poll_container_status("token", "container", urlopen=api_urlopen)
    assert len(api_urlopen.calls) == 1

    transport_urlopen = _recording_urlopen([urllib.error.URLError("offline")])
    with pytest.raises(InstagramTransportError):
        instagram_api.poll_container_status(
            "token", "container", urlopen=transport_urlopen
        )
    assert len(transport_urlopen.calls) == 1
