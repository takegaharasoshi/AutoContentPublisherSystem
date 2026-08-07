"""Tests for SNS posting processing behavior."""

from unittest.mock import ANY, Mock

import app.processing as processing
from app.instagram_api import InstagramRequestFailed, InstagramResultUnknown
from app.models import CaptionTemplate, GeneratedMediaRef, Post, SnsAccount


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
    caption_text = overrides.pop("caption_text", None)
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
        env_name="prod",
        set_code="set-a",
        s3_bucket="configured-bucket",
        s3_client=Mock(),
        urlopen=Mock(),
        caption_text=caption_text,
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
            InstagramRequestFailed("invalid image", {"error": "bad"}),
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
        side_effect=InstagramRequestFailed("invalid video", {"error": "bad"})
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
            InstagramRequestFailed("invalid story", {"error": "bad"}),
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
