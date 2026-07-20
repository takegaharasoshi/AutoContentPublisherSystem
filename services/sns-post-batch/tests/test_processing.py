"""Tests for SNS posting processing behavior."""

from unittest.mock import Mock

import app.processing as processing
from app.instagram_api import InstagramRequestFailed, InstagramResultUnknown
from app.models import CaptionTemplate, GeneratedImageRef, Post, SnsAccount


def _account(account_id: int = 1, platform: str = "instagram") -> SnsAccount:
    """Build a simple SNS account."""
    return SnsAccount(account_id, platform, f"account-{account_id}", "Account")


def _image() -> GeneratedImageRef:
    """Build a generated image reference."""
    return GeneratedImageRef(20, "image-bucket", "images/test.jpg")


def _run(monkeypatch, accounts, get_post, **overrides):
    """Run processing with common API and persistence fakes."""
    cursor = Mock()
    connection = Mock()
    monkeypatch.setattr(processing, "get_post", get_post)
    monkeypatch.setattr(processing, "create_pending_post", Mock(return_value=101))
    monkeypatch.setattr(processing, "ensure_post_image", Mock())
    monkeypatch.setattr(processing, "update_post_caption", Mock())
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
        generated_image=_image(),
        env_name="prod",
        set_code="set-a",
        s3_bucket="configured-bucket",
        s3_client=Mock(),
        urlopen=Mock(),
    )
    return result, cursor, connection


def test_processing_creates_and_publishes_new_post(monkeypatch) -> None:
    """A new account is linked to the image and reaches success."""
    states = iter([None, Post(101, "success", "container", "post")])
    result, cursor, connection = _run(
        monkeypatch, [_account()], lambda *args: next(states)
    )

    assert result.accounts_processed == 1
    assert result.all_accounts_success
    processing.create_pending_post.assert_called_once_with(
        cursor,
        set_id=1,
        generation_run_id=2,
        sns_account_id=1,
    )
    processing.ensure_post_image.assert_called_once_with(
        cursor,
        post_id=101,
        generated_image_id=20,
    )
    processing.update_post_caption.assert_called_once_with(
        cursor,
        101,
        caption_template_id=3,
        caption_text="caption",
    )
    assert connection.commit.call_count == 3


def test_processing_skips_terminal_post(monkeypatch) -> None:
    """Success, failed, and unknown terminal states make no API attempt."""
    terminal = Post(101, "failed", None, None)
    states = iter([terminal, terminal])
    result, _, connection = _run(monkeypatch, [_account()], lambda *args: next(states))

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
        lambda *args: next(states),
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
        lambda *args: next(states),
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
        lambda *args: next(states),
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
        lambda *args: next(states),
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
        lambda *args: next(states),
        get_secret_string=get_secret,
    )

    assert result == processing.ProcessingResult(1, False)
    get_secret.assert_not_called()
    processing.update_post_success.assert_not_called()
