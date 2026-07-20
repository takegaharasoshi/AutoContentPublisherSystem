"""Tests for the standard-library Instagram Graph API client."""

from __future__ import annotations

from io import BytesIO
import json
import urllib.error
import urllib.parse

import pytest

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


def test_create_container_posts_expected_graph_parameters() -> None:
    """Container creation uses the v21.0 media endpoint and timeout."""
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
    assert request.full_url == "https://graph.facebook.com/v21.0/ig-user/media"
    assert urllib.parse.parse_qs(request.data.decode()) == {
        "access_token": ["token"],
        "image_url": ["https://s3.example/image.jpg"],
        "caption": ["caption #tag"],
    }


def test_publish_container_posts_expected_graph_parameters() -> None:
    """Publishing uses media_publish and returns the platform post ID."""
    urlopen = _recording_urlopen([FakeResponse({"id": "post"})])

    assert instagram_api.publish_container(
        "token", "ig-user", "container", urlopen=urlopen
    ) == ("post", {"id": "post"})

    request, timeout = urlopen.calls[0]
    assert timeout == 30
    assert request.full_url == (
        "https://graph.facebook.com/v21.0/ig-user/media_publish"
    )
    assert urllib.parse.parse_qs(request.data.decode()) == {
        "access_token": ["token"],
        "creation_id": ["container"],
    }


def test_http_error_is_a_clear_request_failure_with_response_json() -> None:
    """A normal Graph HTTP error is classified as failed."""
    error = urllib.error.HTTPError(
        "https://graph.facebook.com/v21.0/ig-user/media",
        400,
        "bad request",
        {},
        BytesIO(b'{"error":{"message":"invalid image"}}'),
    )
    urlopen = _recording_urlopen([error])

    with pytest.raises(instagram_api.InstagramRequestFailed) as raised:
        instagram_api.create_container(
            "token", "ig-user", "https://image", "caption", urlopen=urlopen
        )

    assert str(raised.value) == "invalid image"
    assert raised.value.response == {"error": {"message": "invalid image"}}


def test_duplicate_publish_http_error_is_result_unknown() -> None:
    """A duplicate publish response may mean that the post already exists."""
    error = urllib.error.HTTPError(
        "https://graph.facebook.com/v21.0/ig-user/media_publish",
        400,
        "bad request",
        {},
        BytesIO(b'{"error":{"message":"Media has already been published"}}'),
    )
    urlopen = _recording_urlopen([error])

    with pytest.raises(instagram_api.InstagramResultUnknown) as raised:
        instagram_api.publish_container(
            "token", "ig-user", "container", urlopen=urlopen
        )

    assert raised.value.response == {
        "error": {"message": "Media has already been published"}
    }


@pytest.mark.parametrize("transport_error", [urllib.error.URLError("offline"), TimeoutError()])
def test_transport_error_is_result_unknown(transport_error: BaseException) -> None:
    """No HTTP response means the publish result cannot be known."""
    urlopen = _recording_urlopen([transport_error])

    with pytest.raises(instagram_api.InstagramResultUnknown) as raised:
        instagram_api.create_container(
            "token", "ig-user", "https://image", "caption", urlopen=urlopen
        )

    assert raised.value.response is None


def test_poll_container_status_retries_until_finished(monkeypatch) -> None:
    """Polling waits through intermediate states and returns the final JSON."""
    urlopen = _recording_urlopen(
        [FakeResponse({"status_code": "IN_PROGRESS"}), FakeResponse({"status_code": "FINISHED"})]
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
    query = urllib.parse.parse_qs(urllib.parse.urlsplit(request.full_url).query)
    assert query == {"fields": ["status_code"], "access_token": ["token"]}


def test_poll_container_status_error_is_clear_failure() -> None:
    """An explicit ERROR status stops polling and is failed."""
    urlopen = _recording_urlopen([FakeResponse({"status_code": "ERROR"})])

    with pytest.raises(instagram_api.InstagramRequestFailed) as raised:
        instagram_api.poll_container_status(
            "token", "container", urlopen=urlopen, max_attempts=10
        )

    assert raised.value.response == {"status_code": "ERROR"}
    assert len(urlopen.calls) == 1


def test_poll_container_status_limit_is_clear_failure(monkeypatch) -> None:
    """Exhausting polling attempts is a known failure without publishing."""
    urlopen = _recording_urlopen(
        [FakeResponse({"status_code": "IN_PROGRESS"}) for _ in range(3)]
    )
    monkeypatch.setattr(instagram_api.time, "sleep", lambda _: None)

    with pytest.raises(instagram_api.InstagramRequestFailed) as raised:
        instagram_api.poll_container_status(
            "token",
            "container",
            urlopen=urlopen,
            max_attempts=3,
            poll_interval_seconds=0,
        )

    assert raised.value.response == {"status_code": "IN_PROGRESS"}
    assert len(urlopen.calls) == 3
