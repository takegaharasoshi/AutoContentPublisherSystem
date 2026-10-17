"""Tests for SNS posting processing behavior."""

import datetime
from io import BytesIO
import json
from typing import Any
import urllib.error
import urllib.parse
from unittest.mock import ANY, Mock

import pytest

import app.instagram_api as instagram_api
import app.processing as processing
from acps_shared import InstagramRequestFailed
from app.instagram_api import InstagramResultUnknown
from app.models import CaptionTemplate, GeneratedMediaRef, Post, SnsAccount


class _FakeHttpResponse:
    """Minimal urlopen response returning a JSON payload."""

    status = 200

    def __init__(self, payload: dict) -> None:
        self._body = json.dumps(payload).encode()

    def __enter__(self):
        return self

    def __exit__(self, *args) -> None:
        return None

    def read(self) -> bytes:
        return self._body

    def close(self) -> None:
        return None


def _account(account_id: int = 1, platform: str = "instagram") -> SnsAccount:
    """Build a simple SNS account."""
    return SnsAccount(account_id, platform, f"account-{account_id}", "Account")


def _media(file_format: str = "jpg") -> GeneratedMediaRef:
    """Build a generated media reference."""
    s3_key = "videos/test.mp4" if file_format == "mp4" else "images/test.jpg"
    return GeneratedMediaRef(20, "media-bucket", s3_key, file_format)


def _run(monkeypatch, accounts, get_post, **overrides):
    """Run processing with common API and persistence fakes."""
    cursor = Mock()
    connection = Mock()
    generated_media = overrides.pop("generated_media", _media())
    stories_enabled = overrides.pop("stories_enabled", False)
    problem_snapshot_enabled = overrides.pop("problem_snapshot_enabled", False)
    caption_text = overrides.pop("caption_text", None)
    urlopen = overrides.pop("urlopen", Mock())
    sleep = overrides.pop("sleep", Mock())
    monkeypatch.setattr(processing, "get_post", get_post)
    monkeypatch.setattr(processing, "create_pending_post", Mock(return_value=101))
    monkeypatch.setattr(processing, "ensure_post_media", Mock())
    monkeypatch.setattr(processing, "update_post_snapshot", Mock())
    monkeypatch.setattr(processing, "update_post_container_created", Mock())
    monkeypatch.setattr(processing, "update_post_failed", Mock())
    monkeypatch.setattr(processing, "update_post_unconfirmed", Mock())
    monkeypatch.setattr(processing, "update_post_success", Mock())
    monkeypatch.setattr(processing, "get_secret_string", lambda name: '{"access_token":"token","ig_user_id":"ig"}')
    monkeypatch.setattr(processing, "generate_presigned_url", lambda *args, **kwargs: "https://signed")
    monkeypatch.setattr(processing, "create_container", lambda *args, **kwargs: ("container", {"id": "container"}))
    monkeypatch.setattr(processing, "poll_container_status", lambda *args, **kwargs: {"status_code": "FINISHED"})
    monkeypatch.setattr(processing, "publish_container", lambda *args, **kwargs: ("post", {"id": "post"}))
    for name, value in overrides.items():
        monkeypatch.setattr(processing, name, value)

    result = processing.process_target_generation_run(
        cursor,
        connection,
        set_id=1,
        generation_run_id=2,
        sns_accounts=accounts,
        caption_template=CaptionTemplate(3, "caption"),
        generated_media=generated_media,
        stories_enabled=stories_enabled,
        problem_snapshot_enabled=problem_snapshot_enabled,
        env_name="prod",
        set_code="set-a",
        s3_bucket="configured-bucket",
        s3_client=Mock(),
        urlopen=urlopen,
        caption_text=caption_text,
        sleep=sleep,
    )
    return result, cursor, connection


def test_processing_creates_and_publishes_new_post(monkeypatch) -> None:
    """A new account is linked to the media and reaches success."""
    states = iter([None, Post(101, "success", "container", "post")])
    result, cursor, connection = _run(
        monkeypatch, [_account()], lambda *args, **kwargs: next(states)
    )

    assert result.accounts_processed == 1
    assert result.all_accounts_success
    processing.create_pending_post.assert_called_once_with(
        cursor,
        set_id=1,
        generation_run_id=2,
        sns_account_id=1,
        media_type="feed_image",
    )
    processing.ensure_post_media.assert_called_once_with(
        cursor,
        post_id=101,
        generated_media_id=20,
    )
    processing.update_post_snapshot.assert_called_once_with(
        cursor,
        101,
        caption_template_id=3,
        caption_text="caption",
        media_type="feed_image",
    )
    assert connection.commit.call_count == 3


def test_processing_uses_preexpanded_caption_for_snapshot_and_api(monkeypatch) -> None:
    """The caption built once by orchestration is reused unchanged."""
    states = iter([None, Post(101, "success", "container", "post")])
    create_container = Mock(return_value=("container", {"id": "container"}))
    _, cursor, _ = _run(
        monkeypatch,
        [_account()],
        lambda *args, **kwargs: next(states),
        caption_text="展開後の答えです",
        create_container=create_container,
    )
    processing.update_post_snapshot.assert_called_once_with(
        cursor,
        101,
        caption_template_id=3,
        caption_text="展開後の答えです",
        media_type="feed_image",
    )
    assert create_container.call_args.args[3] == "展開後の答えです"


def test_processing_creates_and_publishes_reel(monkeypatch) -> None:
    """MP4 media uses the reel container and longer polling settings."""
    states = iter([None, Post(101, "success", "container", "post")])
    create_container = Mock(return_value=("container", {"id": "container"}))
    poll_container_status = Mock(return_value={"status_code": "FINISHED"})
    result, cursor, _ = _run(
        monkeypatch,
        [_account()],
        lambda *args, **kwargs: next(states),
        generated_media=_media("mp4"),
        create_container=create_container,
        poll_container_status=poll_container_status,
    )

    assert result == processing.ProcessingResult(1, True)
    processing.create_pending_post.assert_called_once_with(
        cursor,
        set_id=1,
        generation_run_id=2,
        sns_account_id=1,
        media_type="reel",
    )
    create_container.assert_called_once_with(
        "token",
        "ig",
        "https://signed",
        "caption",
        media_type="reel",
        urlopen=ANY,
    )
    poll_container_status.assert_called_once_with(
        "token",
        "container",
        urlopen=ANY,
        max_attempts=60,
        poll_interval_seconds=10.0,
    )


def test_processing_skips_terminal_post(monkeypatch) -> None:
    """Success, failed, and unknown terminal states make no API attempt."""
    terminal = Post(101, "failed", None, None)
    states = iter([terminal, terminal])
    result, _, connection = _run(
        monkeypatch, [_account()], lambda *args, **kwargs: next(states)
    )

    assert result == processing.ProcessingResult(0, False)
    connection.commit.assert_not_called()


def test_processing_resumes_container_created_post_without_new_container(
    monkeypatch,
) -> None:
    """A saved container ID is polled and published directly."""
    states = iter(
        [
            Post(101, "container_created", "saved-container", None),
            Post(101, "success", "saved-container", "post"),
        ]
    )
    create_container = Mock()
    presign = Mock()
    result, _, _ = _run(
        monkeypatch,
        [_account()],
        lambda *args, **kwargs: next(states),
        create_container=create_container,
        generate_presigned_url=presign,
    )

    assert result == processing.ProcessingResult(1, True)
    create_container.assert_not_called()
    presign.assert_not_called()


def test_processing_marks_clear_failure_and_continues_to_next_account(monkeypatch) -> None:
    """One clear API error does not block another account."""
    states = iter(
        [
            None,
            None,
            Post(101, "failed", None, None),
            Post(102, "success", "container", "post"),
        ]
    )
    create_container = Mock(
        side_effect=[
            InstagramRequestFailed("invalid image", response={"error": "bad"}),
            ("container", {"id": "container"}),
        ]
    )
    result, _, _ = _run(
        monkeypatch,
        [_account(1), _account(2)],
        lambda *args, **kwargs: next(states),
        create_container=create_container,
    )

    assert result == processing.ProcessingResult(2, False)
    assert processing.update_post_failed.call_count == 1
    assert processing.update_post_failed.call_args.kwargs == {
        "error_message": "invalid image",
        "api_response": {"error": "bad"},
    }
    assert processing.update_post_success.call_count == 1


def test_processing_records_container_error_reason(monkeypatch, caplog) -> None:
    """A container ERROR reason reaches the log and posts.api_response."""
    payload = {"status_code": "ERROR", "status": "Error: video too long (2207026)"}
    urlopen = Mock(
        return_value=_FakeHttpResponse(payload),
    )
    states = iter([None, Post(101, "failed", "container", None)])
    caplog.set_level("ERROR", logger=processing.__name__)

    result, _, _ = _run(
        monkeypatch,
        [_account()],
        lambda *args, **kwargs: next(states),
        poll_container_status=lambda token, container_id, **kwargs: (
            instagram_api.poll_container_status(
                token, container_id, urlopen=urlopen, max_attempts=1
            )
        ),
    )

    assert result == processing.ProcessingResult(1, False)
    kwargs = processing.update_post_failed.call_args.kwargs
    assert kwargs["api_response"] == {
        "final": payload,
        "first_error": {
            "stage": "poll", "container_id": "container", "response": payload,
        },
        "container_check": None,
    }
    assert urlopen.call_count == 2
    assert kwargs["error_message"].endswith("（作成から 1 回やり直し済み）")
    assert "Error: video too long (2207026)" in kwargs["error_message"]
    assert "Error: video too long (2207026)" in caplog.text


def test_processing_marks_unknown_result_as_unconfirmed(monkeypatch) -> None:
    """A transport failure is recorded as published_unconfirmed."""
    states = iter([None, Post(101, "published_unconfirmed", None, None)])
    result, _, _ = _run(
        monkeypatch,
        [_account()],
        lambda *args, **kwargs: next(states),
        publish_container=lambda *args, **kwargs: (_ for _ in ()).throw(
            InstagramResultUnknown("timed out", {"error": "unknown"})
        ),
    )

    assert result == processing.ProcessingResult(1, False)
    assert processing.update_post_unconfirmed.call_count == 1


def test_processing_leaves_post_pending_when_secret_lookup_fails(monkeypatch) -> None:
    """Unexpected secret errors do not convert the post to a terminal state."""
    states = iter([None, Post(101, "pending", None, None)])
    result, _, _ = _run(
        monkeypatch,
        [_account()],
        lambda *args, **kwargs: next(states),
        get_secret_string=lambda name: (_ for _ in ()).throw(RuntimeError("secret")),
    )

    assert result == processing.ProcessingResult(1, False)
    processing.update_post_failed.assert_not_called()
    processing.update_post_unconfirmed.assert_not_called()


def test_processing_counts_unsupported_platform_but_leaves_state_nonterminal(
    monkeypatch,
) -> None:
    """Unsupported platforms are logged and left for future support."""
    pending = Post(101, "pending", None, None)
    states = iter([None, pending])
    get_secret = Mock()
    result, _, _ = _run(
        monkeypatch,
        [_account(platform="threads")],
        lambda *args, **kwargs: next(states),
        get_secret_string=get_secret,
    )

    assert result == processing.ProcessingResult(1, False)
    get_secret.assert_not_called()
    processing.update_post_success.assert_not_called()


def test_processing_does_not_create_story_when_disabled(monkeypatch) -> None:
    """An MP4 retains the single-reel API flow when stories are disabled."""
    states = iter([None, Post(101, "success", "container", "post")])
    create_container = Mock(return_value=("reel-container", {"id": "reel-container"}))

    result, _, _ = _run(
        monkeypatch,
        [_account()],
        lambda *args, **kwargs: next(states),
        generated_media=_media("mp4"),
        create_container=create_container,
        stories_enabled=False,
    )

    assert result == processing.ProcessingResult(1, True)
    assert create_container.call_count == 1
    assert processing.create_pending_post.call_args_list[0].kwargs["media_type"] == "reel"


def test_processing_posts_story_after_successful_reel(monkeypatch) -> None:
    """An enabled reel publishes its story only after the reel reaches success."""
    states = iter(
        [
            None,
            None,
            Post(101, "success", "reel-container", "reel-post"),
            Post(102, "success", "story-container", "story-post"),
        ]
    )
    create_container = Mock(
        side_effect=[
            ("reel-container", {"id": "reel-container"}),
            ("story-container", {"id": "story-container"}),
        ]
    )
    publish_container = Mock(
        side_effect=[
            ("reel-post", {"id": "reel-post"}),
            ("story-post", {"id": "story-post"}),
        ]
    )

    result, cursor, _ = _run(
        monkeypatch,
        [_account()],
        lambda *args, **kwargs: next(states),
        generated_media=_media("mp4"),
        stories_enabled=True,
        create_pending_post=Mock(side_effect=[101, 102]),
        create_container=create_container,
        publish_container=publish_container,
    )

    assert result == processing.ProcessingResult(1, True)
    assert [call.kwargs["media_type"] for call in processing.create_pending_post.call_args_list] == [
        "reel",
        "story",
    ]
    assert processing.ensure_post_media.call_count == 2
    processing.update_post_snapshot.assert_called_once_with(
        cursor,
        101,
        caption_template_id=3,
        caption_text="caption",
        media_type="reel",
    )
    assert create_container.call_args_list[0].args == (
        "token",
        "ig",
        "https://signed",
        "caption",
    )
    assert create_container.call_args_list[1].args == (
        "token",
        "ig",
        "https://signed",
    )
    assert create_container.call_args_list[1].kwargs["media_type"] == "story"


def test_processing_posts_story_after_previously_successful_reel(monkeypatch) -> None:
    """A terminal successful reel still triggers its missing enabled story."""
    states = iter(
        [
            Post(101, "success", "reel-container", "reel-post"),
            None,
            Post(101, "success", "reel-container", "reel-post"),
            Post(102, "success", "story-container", "story-post"),
        ]
    )
    create_container = Mock(return_value=("story-container", {"id": "story-container"}))

    result, _, _ = _run(
        monkeypatch,
        [_account()],
        lambda *args, **kwargs: next(states),
        generated_media=_media("mp4"),
        stories_enabled=True,
        create_pending_post=Mock(return_value=102),
        create_container=create_container,
    )

    assert result == processing.ProcessingResult(1, True)
    processing.create_pending_post.assert_called_once()
    assert processing.create_pending_post.call_args.kwargs["media_type"] == "story"
    processing.update_post_snapshot.assert_not_called()
    assert create_container.call_args.args == ("token", "ig", "https://signed")


def test_processing_does_not_create_story_when_reel_fails(monkeypatch) -> None:
    """A failed reel leaves no pending story row behind."""
    states = iter([None, Post(101, "failed", None, None)])
    create_container = Mock(
        side_effect=InstagramRequestFailed("invalid video", response={"error": "bad"})
    )

    result, _, _ = _run(
        monkeypatch,
        [_account()],
        lambda *args, **kwargs: next(states),
        generated_media=_media("mp4"),
        stories_enabled=True,
        create_container=create_container,
    )

    assert result == processing.ProcessingResult(1, False)
    processing.create_pending_post.assert_called_once()
    assert processing.create_pending_post.call_args.kwargs["media_type"] == "reel"


def test_processing_keeps_reel_success_when_story_fails(monkeypatch) -> None:
    """A story failure is isolated but makes the account result unsuccessful."""
    states = iter(
        [
            None,
            None,
            Post(101, "success", "reel-container", "reel-post"),
            Post(102, "failed", None, None),
        ]
    )
    create_container = Mock(
        side_effect=[
            ("reel-container", {"id": "reel-container"}),
            InstagramRequestFailed("invalid story", response={"error": "bad"}),
        ]
    )

    result, _, _ = _run(
        monkeypatch,
        [_account()],
        lambda *args, **kwargs: next(states),
        generated_media=_media("mp4"),
        stories_enabled=True,
        create_pending_post=Mock(side_effect=[101, 102]),
        create_container=create_container,
    )

    assert result == processing.ProcessingResult(1, False)
    assert processing.update_post_success.call_count == 1
    assert processing.update_post_success.call_args.args[1] == 101
    assert processing.update_post_failed.call_count == 1
    assert processing.update_post_failed.call_args.args[1] == 102


def test_processing_does_not_create_story_for_feed_image(monkeypatch) -> None:
    """The stories switch applies only to reels, never image feed posts."""
    states = iter([None, Post(101, "success", "container", "post")])

    result, _, _ = _run(
        monkeypatch,
        [_account()],
        lambda *args, **kwargs: next(states),
        stories_enabled=True,
    )

    assert result == processing.ProcessingResult(1, True)
    processing.create_pending_post.assert_called_once()
    assert processing.create_pending_post.call_args.kwargs["media_type"] == "feed_image"


def test_processing_writes_snapshot_after_reel_commit_before_story(monkeypatch) -> None:
    states = iter(
        [None, None, Post(101, "success", "reel", "reel-post"),
         Post(102, "success", "story", "story-post")]
    )
    events: list[str] = []
    posted_at = datetime.datetime(2026, 9, 26, 11, 0, 12)
    update_success = Mock(side_effect=lambda *args, **kwargs: (
        events.append("reel-success" if args[1] == 101 else "story-success")
        or posted_at
    ))
    def snapshot_after_commit(cursor, connection, **kwargs):
        assert connection.commit.call_count == 3
        events.append("snapshot")

    write_snapshot = Mock(side_effect=snapshot_after_commit)

    result, cursor, connection = _run(
        monkeypatch,
        [_account()],
        lambda *args, **kwargs: next(states),
        generated_media=_media("mp4"),
        stories_enabled=True,
        problem_snapshot_enabled=True,
        create_pending_post=Mock(side_effect=[101, 102]),
        update_post_success=update_success,
        write_problem_snapshot=write_snapshot,
    )

    assert result == processing.ProcessingResult(1, True)
    assert events == ["reel-success", "snapshot", "story-success"]
    write_snapshot.assert_called_once_with(
        cursor,
        connection,
        set_id=1,
        set_code="set-a",
        generation_run_id=2,
        media_id="post",
        posted_at=posted_at,
        s3_bucket="configured-bucket",
        s3_client=ANY,
    )


def test_processing_does_no_snapshot_io_when_flag_is_false(monkeypatch) -> None:
    states = iter([None, Post(101, "success", "container", "post")])
    write_snapshot = Mock()
    result, cursor, _ = _run(
        monkeypatch,
        [_account()],
        lambda *args, **kwargs: next(states),
        generated_media=_media("mp4"),
        problem_snapshot_enabled=False,
        write_problem_snapshot=write_snapshot,
    )
    assert result == processing.ProcessingResult(1, True)
    write_snapshot.assert_not_called()
    cursor.execute.assert_not_called()


def test_processing_does_not_snapshot_feed_image_even_when_enabled(monkeypatch) -> None:
    states = iter([None, Post(101, "success", "container", "post")])
    write_snapshot = Mock()
    result, _, _ = _run(
        monkeypatch,
        [_account()],
        lambda *args, **kwargs: next(states),
        problem_snapshot_enabled=True,
        write_problem_snapshot=write_snapshot,
    )
    assert result == processing.ProcessingResult(1, True)
    write_snapshot.assert_not_called()


def test_processing_preserves_success_after_snapshot_failure(
    monkeypatch, caplog
) -> None:
    states = iter([None, Post(101, "success", "container", "post")])
    write_snapshot = Mock(side_effect=RuntimeError("S3 failed"))
    result, _, connection = _run(
        monkeypatch,
        [_account()],
        lambda *args, **kwargs: next(states),
        generated_media=_media("mp4"),
        problem_snapshot_enabled=True,
        write_problem_snapshot=write_snapshot,
    )
    assert result == processing.ProcessingResult(1, True)
    processing.update_post_success.assert_called_once()
    assert connection.commit.call_count == 3
    connection.rollback.assert_called_once()
    assert "問題スナップショットの出力に失敗" in caplog.text


def test_processing_does_not_snapshot_failed_reel(monkeypatch) -> None:
    states = iter([None, Post(101, "failed", None, None)])
    write_snapshot = Mock()
    result, _, _ = _run(
        monkeypatch,
        [_account()],
        lambda *args, **kwargs: next(states),
        generated_media=_media("mp4"),
        problem_snapshot_enabled=True,
        create_container=Mock(side_effect=InstagramRequestFailed("bad", response=None)),
        write_problem_snapshot=write_snapshot,
    )
    assert result == processing.ProcessingResult(1, False)
    write_snapshot.assert_not_called()


def _http_error(payload: dict, status: int = 400) -> urllib.error.HTTPError:
    """Build a real Graph HTTP error for the recording urlopen mock."""
    return urllib.error.HTTPError(
        "https://graph.facebook.com/v25.0/ig/media",
        status,
        "bad request",
        {},
        BytesIO(json.dumps(payload).encode()),
    )


def _run_graph_flow(
    monkeypatch: pytest.MonkeyPatch,
    responses: list[Any],
    **overrides: Any,
) -> tuple[processing.ProcessingResult, Mock, Mock]:
    """Exercise real SNS/shared HTTP handling with mocked DB persistence."""
    final_status = overrides.pop("final_status", "success")
    initial_post = overrides.pop("initial_post", None)
    states = iter([initial_post, Post(101, final_status, None, None)])
    get_post = overrides.pop("get_post", lambda *args, **kwargs: next(states))
    urlopen = Mock(side_effect=[
        _FakeHttpResponse(value) if isinstance(value, dict) else value
        for value in responses
    ])
    sleep = Mock()
    result, _, _ = _run(
        monkeypatch,
        [_account()],
        get_post,
        generated_media=_media("mp4"),
        create_container=instagram_api.create_container,
        poll_container_status=instagram_api.poll_container_status,
        publish_container=instagram_api.publish_container,
        resolve_poll_settings=lambda media_type: instagram_api.PollSettings(1, 0),
        urlopen=urlopen,
        sleep=sleep,
        **overrides,
    )
    return result, urlopen, sleep


def _request_paths(urlopen: Mock) -> list[str]:
    """Return the last path component of every outgoing HTTP request."""
    return [
        urllib.parse.urlsplit(call.args[0].full_url).path.rsplit("/", 1)[-1]
        for call in urlopen.call_args_list
    ]


def _publish_ids(urlopen: Mock) -> list[str]:
    """Read actual creation_id form fields to detect container replacement."""
    return [
        urllib.parse.parse_qs(call.args[0].data.decode())["creation_id"][0]
        for call in urlopen.call_args_list
        if call.args[0].full_url.endswith("/media_publish")
    ]


def test_create_transient_error_recreates_and_succeeds(monkeypatch) -> None:
    """A transient creation error gets one fresh container and keeps history."""
    payload = {"error": {"message": "try again", "code": 100, "is_transient": True}}
    result, api, sleep = _run_graph_flow(monkeypatch, [
        _http_error(payload), {"id": "new"},
        {"status_code": "FINISHED"}, {"id": "post"},
    ])

    assert result == processing.ProcessingResult(1, True)
    assert _request_paths(api) == ["media", "media", "new", "media_publish"]
    assert _publish_ids(api) == ["new"]
    processing.update_post_container_created.assert_called_once_with(
        ANY, 101, platform_container_id="new",
    )
    assert processing.update_post_success.call_args.kwargs == {
        "platform_post_id": "post",
        "api_response": {
            "final": None,
            "first_error": {
                "stage": "create", "container_id": None, "response": payload,
            },
            "container_check": None,
        },
    }
    sleep.assert_not_called()


@pytest.mark.parametrize("code", [1, 2])
def test_create_service_error_without_flag_retries(monkeypatch, code: int) -> None:
    """Graph codes 1 and 2 qualify even without is_transient."""
    result, api, sleep = _run_graph_flow(monkeypatch, [
        _http_error({"error": {"code": code}}),
        {"id": "new"}, {"status_code": "FINISHED"}, {"id": "post"},
    ])
    assert result.all_accounts_success
    assert _request_paths(api).count("media") == 2
    sleep.assert_not_called()


@pytest.mark.parametrize("stage", ["create", "poll", "publish"])
@pytest.mark.parametrize(
    "status,code", [(400, 4), (400, 17), (400, 32), (400, 613), (429, 2)],
)
def test_rate_limit_without_flag_never_retries(
    monkeypatch, stage: str, status: int, code: int,
) -> None:
    """Rate limits stay failed at every stage without an explicit true flag."""
    payload = {"error": {"message": "rate limited", "code": code}}
    responses = []
    if stage != "create":
        responses.append({"id": "container"})
    if stage == "publish":
        responses.append({"status_code": "FINISHED"})
    responses.append(_http_error(payload, status))
    result, api, sleep = _run_graph_flow(monkeypatch, responses, final_status="failed")

    assert not result.all_accounts_success
    assert api.call_count == len(responses)
    assert processing.update_post_failed.call_args.kwargs == {
        "error_message": "rate limited", "api_response": payload,
    }
    processing.update_post_unconfirmed.assert_not_called()
    sleep.assert_not_called()


@pytest.mark.parametrize("stage", ["create", "poll", "publish"])
def test_explicitly_transient_rate_limit_uses_stage_recovery(
    monkeypatch, stage: str,
) -> None:
    """is_transient true also allows recovery of a rate-limit exception."""
    payload = {"error": {"code": 4, "is_transient": True}}
    responses = []
    if stage != "create":
        responses.append({"id": "old"})
    if stage == "publish":
        responses.append({"status_code": "FINISHED"})
    responses.append(_http_error(payload, 429))
    if stage != "publish":
        responses.append({"id": "new"})
    responses.extend([{"status_code": "FINISHED"}, {"id": "post"}])
    result, api, sleep = _run_graph_flow(monkeypatch, responses)

    assert result.all_accounts_success
    assert _publish_ids(api) == (["old", "old"] if stage == "publish" else ["new"])
    saved = processing.update_post_success.call_args.kwargs["api_response"]
    assert saved["first_error"]["stage"] == stage
    if stage == "publish":
        sleep.assert_called_once_with(10.0)
    else:
        sleep.assert_not_called()


@pytest.mark.parametrize("stage", ["create", "poll"])
@pytest.mark.parametrize("failure", ["timeout", "connection", "body"])
def test_pre_publish_transport_error_recreates(
    monkeypatch, stage: str, failure: str,
) -> None:
    """Timeouts, connection failures, and read failures retry before publish."""
    if failure == "body":
        failure_response = _FakeHttpResponse({})
        failure_response.read = Mock(side_effect=TimeoutError("body unreadable"))
        message = "Instagram API returned an unreadable JSON response"
    elif failure == "connection":
        failure_response = urllib.error.URLError("offline")
        message = "Instagram API transport failed: URLError"
    else:
        failure_response = TimeoutError("timeout")
        message = "Instagram API transport failed: TimeoutError"
    responses = [{"id": "old"}] if stage == "poll" else []
    responses.extend([
        failure_response, {"id": "new"}, {"status_code": "FINISHED"}, {"id": "post"},
    ])
    result, api, sleep = _run_graph_flow(monkeypatch, responses)

    assert result.all_accounts_success
    assert _request_paths(api).count("media") == 2
    assert _publish_ids(api) == ["new"]
    assert processing.update_post_success.call_args.kwargs["api_response"] == {
        "final": None,
        "first_error": {
            "stage": stage,
            "container_id": "old" if stage == "poll" else None,
            "response": {"transport_error": message},
        },
        "container_check": None,
    }
    sleep.assert_not_called()


def test_poll_error_recreates_and_succeeds(monkeypatch, caplog) -> None:
    """An ERROR replaces the saved container and logs its original reason."""
    payload = {"status_code": "ERROR", "status": "first processing error"}
    result, api, sleep = _run_graph_flow(monkeypatch, [
        {"id": "old"}, payload, {"id": "new"},
        {"status_code": "FINISHED"}, {"id": "post"},
    ])

    assert result.all_accounts_success
    assert _request_paths(api) == ["media", "old", "media", "new", "media_publish"]
    assert [
        call.kwargs["platform_container_id"]
        for call in processing.update_post_container_created.call_args_list
    ] == ["old", "new"]
    assert processing.update_post_success.call_args.kwargs["api_response"] == {
        "final": None,
        "first_error": {
            "stage": "poll", "container_id": "old", "response": payload,
        },
        "container_check": None,
    }
    assert any(
        record.levelname == "WARNING"
        and "container_id=old" in record.message
        and "first processing error" in record.message
        for record in caplog.records
    )
    sleep.assert_not_called()


def test_poll_error_twice_fails_after_one_recreation(monkeypatch) -> None:
    """The second ERROR is final, retaining the first and last error bodies."""
    first = {"status_code": "ERROR", "status": "first error"}
    final = {"status_code": "ERROR", "status": "last error"}
    result, api, sleep = _run_graph_flow(monkeypatch, [
        {"id": "old"}, first, {"id": "new"}, final,
    ], final_status="failed")

    assert not result.all_accounts_success
    assert _request_paths(api) == ["media", "old", "media", "new"]
    assert processing.update_post_failed.call_args.kwargs == {
        "error_message": (
            "Instagram container processing returned ERROR: last error"
            "（作成から 1 回やり直し済み）"
        ),
        "api_response": {
            "final": final,
            "first_error": {
                "stage": "poll", "container_id": "old", "response": first,
            },
            "container_check": None,
        },
    }
    sleep.assert_not_called()


@pytest.mark.parametrize("status_code", ["IN_PROGRESS", "EXPIRED"])
def test_poll_limit_or_expired_fails_without_recreation(
    monkeypatch, status_code: str,
) -> None:
    """A polling limit or EXPIRED must not start a new processing window."""
    payload = {"status_code": status_code}
    result, api, sleep = _run_graph_flow(monkeypatch, [
        {"id": "container"}, payload,
    ], final_status="failed")

    assert not result.all_accounts_success
    assert _request_paths(api) == ["media", "container"]
    assert processing.update_post_failed.call_args.kwargs["api_response"] == payload
    saved = processing.update_post_failed.call_args.kwargs
    assert "やり直し済み" not in saved["error_message"]
    sleep.assert_not_called()


@pytest.mark.parametrize("first_stage", ["create", "poll"])
def test_creation_and_polling_share_one_recovery_budget(
    monkeypatch, first_stage: str,
) -> None:
    """A retry spent in either pre-publish stage cannot be spent in the other."""
    create_error = {"error": {"code": 2}}
    poll_error = {"status_code": "ERROR"}
    if first_stage == "create":
        responses = [_http_error(create_error), {"id": "new"}, poll_error]
        first, final, container_id = create_error, poll_error, None
    else:
        responses = [{"id": "old"}, poll_error, _http_error(create_error)]
        first, final, container_id = poll_error, create_error, "old"
    result, api, _ = _run_graph_flow(monkeypatch, responses, final_status="failed")

    assert not result.all_accounts_success
    assert _request_paths(api).count("media") == 2
    assert _publish_ids(api) == []
    assert processing.update_post_failed.call_args.kwargs["api_response"] == {
        "final": final,
        "first_error": {
            "stage": first_stage, "container_id": container_id, "response": first,
        },
        "container_check": None,
    }


def test_resumed_container_can_recreate_once_after_poll_error(monkeypatch) -> None:
    """An SFN restart starts with a fresh in-memory retry allowance."""
    payload = {"status_code": "ERROR"}
    result, api, _ = _run_graph_flow(monkeypatch, [
        payload, {"id": "new"}, {"status_code": "FINISHED"}, {"id": "post"},
    ], initial_post=Post(101, "container_created", "saved", None))

    assert result.all_accounts_success
    assert _request_paths(api) == ["saved", "media", "new", "media_publish"]
    processing.create_pending_post.assert_not_called()
    saved = processing.update_post_success.call_args.kwargs["api_response"]
    assert saved["first_error"] == {
        "stage": "poll", "container_id": "saved", "response": payload,
    }


def test_publish_transient_error_checks_published_without_resending(
    monkeypatch,
) -> None:
    """PUBLISHED confirms publication but leaves the missing media ID unresolved."""
    first = {"error": {"code": 2, "message": "publish busy", "is_transient": True}}
    check = {"status_code": "PUBLISHED", "status": "Published"}
    result, api, sleep = _run_graph_flow(monkeypatch, [
        {"id": "container"}, {"status_code": "FINISHED"}, _http_error(first), check,
    ], final_status="published_unconfirmed")

    assert not result.all_accounts_success
    assert _request_paths(api) == ["media", "container", "media_publish", "container"]
    assert _publish_ids(api) == ["container"]
    sleep.assert_called_once_with(10.0)
    assert processing.update_post_unconfirmed.call_args.kwargs == {
        "error_message": "PUBLISHED 確認済み: publish busy",
        "api_response": {
            "final": first,
            "first_error": {
                "stage": "publish", "container_id": "container", "response": first,
            },
            "container_check": check,
        },
    }


def test_publish_finished_resends_same_container_and_succeeds(monkeypatch) -> None:
    """Only FINISHED allows one resend, always with the original creation_id."""
    first = {"error": {"code": 2, "message": "publish busy"}}
    check = {"status_code": "FINISHED"}
    result, api, sleep = _run_graph_flow(monkeypatch, [
        {"id": "container"}, {"status_code": "FINISHED"},
        _http_error(first), check, {"id": "post"},
    ])

    assert result.all_accounts_success
    assert _request_paths(api) == [
        "media", "container", "media_publish", "container", "media_publish",
    ]
    assert _publish_ids(api) == ["container", "container"]
    processing.update_post_container_created.assert_called_once()
    assert processing.update_post_success.call_args.kwargs["api_response"] == {
        "final": None,
        "first_error": {
            "stage": "publish", "container_id": "container", "response": first,
        },
        "container_check": check,
    }
    sleep.assert_called_once_with(10.0)


@pytest.mark.parametrize("failure", ["transient", "duplicate", "transport", "body"])
def test_publish_resend_unknown_result_stops_without_second_check(
    monkeypatch, failure: str,
) -> None:
    """Transient, duplicate, and transport failures after resend stay unconfirmed."""
    first = {"error": {"code": 2, "message": "first publish error"}}
    check = {"status_code": "FINISHED"}
    final = None
    if failure == "transient":
        final = {"error": {"code": 1, "message": "last publish error"}}
        response = _http_error(final)
        message = "last publish error"
    elif failure == "duplicate":
        final = {"error": {"code": 2, "message": "Media has already been published"}}
        response = _http_error(final)
        message = "Media has already been published"
    elif failure == "body":
        response = _FakeHttpResponse({})
        response.read = Mock(side_effect=TimeoutError("body"))
        message = "Instagram API returned an unreadable JSON response"
    else:
        response = TimeoutError("timeout")
        message = "Instagram API transport failed: TimeoutError"
    result, api, sleep = _run_graph_flow(monkeypatch, [
        {"id": "container"}, {"status_code": "FINISHED"},
        _http_error(first), check, response,
    ], final_status="published_unconfirmed")

    assert not result.all_accounts_success
    assert _request_paths(api) == [
        "media", "container", "media_publish", "container", "media_publish",
    ]
    assert _publish_ids(api) == ["container", "container"]
    assert processing.update_post_unconfirmed.call_args.kwargs == {
        "error_message": message + "（公開を 1 回再送済み）",
        "api_response": {
            "final": final,
            "first_error": {
                "stage": "publish", "container_id": "container", "response": first,
            },
            "container_check": check,
        },
    }
    processing.update_post_failed.assert_not_called()
    sleep.assert_called_once_with(10.0)


def test_publish_resend_permanent_error_fails(monkeypatch) -> None:
    """A definite rejection of the resend is failed, with its final response."""
    first = {"error": {"code": 2}}
    final = {"error": {"code": 190, "message": "access denied"}}
    check = {"status_code": "FINISHED"}
    result, api, sleep = _run_graph_flow(monkeypatch, [
        {"id": "container"}, {"status_code": "FINISHED"},
        _http_error(first), check, _http_error(final),
    ], final_status="failed")

    assert not result.all_accounts_success
    assert _publish_ids(api) == ["container", "container"]
    assert _request_paths(api).count("media") == 1
    assert processing.update_post_failed.call_args.kwargs == {
        "error_message": "access denied（公開を 1 回再送済み）",
        "api_response": {
            "final": final,
            "first_error": {
                "stage": "publish", "container_id": "container", "response": first,
            },
            "container_check": check,
        },
    }
    processing.update_post_unconfirmed.assert_not_called()
    sleep.assert_called_once_with(10.0)


@pytest.mark.parametrize(
    "failure", ["api", "transient_api", "transport", "unexpected"],
)
def test_publish_check_failure_is_unconfirmed_without_retry(
    monkeypatch, failure: str,
) -> None:
    """Every failed check stops recovery and records the last failure."""
    first = {"error": {"code": 2, "message": "publish error"}}
    final = None
    if failure in {"api", "transient_api"}:
        final = {"error": {
            "code": 2 if failure == "transient_api" else 190,
            "message": "check error",
        }}
        response = _http_error(final)
        message = "check error"
    elif failure == "transport":
        response = TimeoutError("timeout")
        message = "Instagram API transport failed: TimeoutError"
    else:
        response = RuntimeError("unexpected check error")
        message = "unexpected check error"
    result, api, sleep = _run_graph_flow(monkeypatch, [
        {"id": "container"}, {"status_code": "FINISHED"}, _http_error(first), response,
    ], final_status="published_unconfirmed")

    assert not result.all_accounts_success
    assert _request_paths(api) == ["media", "container", "media_publish", "container"]
    assert processing.update_post_unconfirmed.call_args.kwargs == {
        "error_message": message,
        "api_response": {
            "final": final,
            "first_error": {
                "stage": "publish", "container_id": "container", "response": first,
            },
            "container_check": None,
        },
    }
    sleep.assert_called_once_with(10.0)


@pytest.mark.parametrize("status_code", ["ERROR", "EXPIRED", "IN_PROGRESS", None])
def test_publish_check_other_status_is_unconfirmed(
    monkeypatch, status_code: str | None,
) -> None:
    """A check that cannot establish FINISHED or PUBLISHED cannot be retried."""
    first = {"error": {"code": 2, "message": "publish error"}}
    check = {"status_code": status_code}
    result, api, sleep = _run_graph_flow(monkeypatch, [
        {"id": "container"}, {"status_code": "FINISHED"}, _http_error(first), check,
    ], final_status="published_unconfirmed")

    assert not result.all_accounts_success
    assert _publish_ids(api) == ["container"]
    assert api.call_count == 4
    assert processing.update_post_unconfirmed.call_args.kwargs["api_response"] == {
        "final": first,
        "first_error": {
            "stage": "publish", "container_id": "container", "response": first,
        },
        "container_check": check,
    }
    sleep.assert_called_once_with(10.0)


def test_publish_permanent_error_fails_without_check(monkeypatch) -> None:
    """A definite API error retains the legacy raw error JSON."""
    payload = {"error": {"code": 190, "message": "access denied"}}
    result, api, sleep = _run_graph_flow(monkeypatch, [
        {"id": "container"}, {"status_code": "FINISHED"}, _http_error(payload),
    ], final_status="failed")

    assert not result.all_accounts_success
    assert _request_paths(api) == ["media", "container", "media_publish"]
    assert processing.update_post_failed.call_args.kwargs == {
        "error_message": "access denied", "api_response": payload,
    }
    sleep.assert_not_called()


@pytest.mark.parametrize("failure", ["transport", "body", "duplicate"])
def test_publish_unknown_result_never_checks_or_recreates(
    monkeypatch, failure: str,
) -> None:
    """Transport and duplicate results keep their existing unconfirmed path."""
    payload = None
    if failure == "duplicate":
        payload = {"error": {
            "code": 2,
            "is_transient": True,
            "message": "Media has already been published",
        }}
        response = _http_error(payload)
    elif failure == "body":
        response = _FakeHttpResponse({})
        response.read = Mock(side_effect=TimeoutError("body"))
    else:
        response = TimeoutError("timeout")
    result, api, sleep = _run_graph_flow(monkeypatch, [
        {"id": "container"}, {"status_code": "FINISHED"}, response,
    ], final_status="published_unconfirmed")

    assert not result.all_accounts_success
    assert _request_paths(api) == ["media", "container", "media_publish"]
    saved = processing.update_post_unconfirmed.call_args.kwargs
    assert saved["api_response"] == payload
    processing.update_post_failed.assert_not_called()
    sleep.assert_not_called()


def test_story_and_reel_have_independent_recreation_budgets(monkeypatch) -> None:
    """Each posts row can recreate once, even after the reel spent its retry."""
    reel_error = {"status_code": "ERROR", "status": "reel error"}
    story_error = {"status_code": "ERROR", "status": "story error"}
    states = iter([
        None, None,
        Post(101, "success", "new-reel", "reel-post"),
        Post(102, "success", "new-story", "story-post"),
    ])
    result, api, sleep = _run_graph_flow(monkeypatch, [
        {"id": "old-reel"}, reel_error, {"id": "new-reel"},
        {"status_code": "FINISHED"}, {"id": "reel-post"},
        {"id": "old-story"}, story_error, {"id": "new-story"},
        {"status_code": "FINISHED"}, {"id": "story-post"},
    ], stories_enabled=True, get_post=lambda *args, **kwargs: next(states),
        create_pending_post=Mock(side_effect=[101, 102]))

    assert result == processing.ProcessingResult(1, True)
    assert _publish_ids(api) == ["new-reel", "new-story"]
    creates = [
        call.args[0] for call in api.call_args_list
        if call.args[0].full_url.endswith("/media")
    ]
    values = [urllib.parse.parse_qs(request.data.decode()) for request in creates]
    assert [value["media_type"] for value in values] == [
        ["REELS"], ["REELS"], ["STORIES"], ["STORIES"],
    ]
    assert all("caption" not in value for value in values[2:])
    assert [
        call.args[1] for call in processing.update_post_success.call_args_list
    ] == [101, 102]
    for call, container_id, response in zip(
        processing.update_post_success.call_args_list,
        ["old-reel", "old-story"], [reel_error, story_error],
    ):
        assert call.kwargs["api_response"] == {
            "final": None,
            "first_error": {
                "stage": "poll", "container_id": container_id, "response": response,
            },
            "container_check": None,
        }
    sleep.assert_not_called()


@pytest.mark.parametrize("succeeds", [True, False])
def test_creation_and_publish_recovery_keep_first_error_and_both_budgets(
    monkeypatch, succeeds: bool,
) -> None:
    """One row can use both independent budgets while retaining its first error."""
    first = {"status_code": "ERROR", "status": "original processing error"}
    publish_error = {"error": {"code": 2, "message": "publish busy"}}
    final = {"error": {"code": 2, "message": "last publish error"}}
    check = {"status_code": "FINISHED"}
    result, api, sleep = _run_graph_flow(monkeypatch, [
        {"id": "old"}, first, {"id": "new"}, {"status_code": "FINISHED"},
        _http_error(publish_error), check,
        {"id": "post"} if succeeds else _http_error(final),
    ], final_status="success" if succeeds else "published_unconfirmed")

    assert result.all_accounts_success is succeeds
    assert _request_paths(api) == [
        "media", "old", "media", "new", "media_publish", "new", "media_publish",
    ]
    assert _publish_ids(api) == ["new", "new"]
    update = (processing.update_post_success if succeeds
              else processing.update_post_unconfirmed)
    assert update.call_args.kwargs["api_response"] == {
        "final": None if succeeds else final,
        "first_error": {"stage": "poll", "container_id": "old", "response": first},
        "container_check": check,
    }
    if not succeeds:
        assert update.call_args.kwargs["error_message"] == (
            "last publish error（作成から 1 回やり直し済み）（公開を 1 回再送済み）"
        )
    sleep.assert_called_once_with(10.0)
