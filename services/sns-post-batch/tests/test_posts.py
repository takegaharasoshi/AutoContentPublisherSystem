"""Tests for post repository functions."""

import datetime
import json
from unittest.mock import Mock

import pymysql
import pytest

import app.posts as posts
from app.models import Post


def test_get_post_maps_row() -> None:
    """A post row is converted to a Post model."""
    cursor = Mock()
    cursor.fetchone.return_value = (4, "container_created", "container", None)

    assert posts.get_post(cursor, 2, 3) == Post(
        4, "container_created", "container", None
    )
    cursor.execute.assert_called_once_with(
        "SELECT id, status, platform_container_id, platform_post_id FROM posts "
        "WHERE generation_run_id = %s AND sns_account_id = %s",
        (2, 3),
    )


def test_get_post_returns_none_when_missing() -> None:
    """An absent post is represented by None."""
    cursor = Mock()
    cursor.fetchone.return_value = None

    assert posts.get_post(cursor, 2, 3) is None


def test_create_pending_post_inserts_and_returns_id() -> None:
    """A new post uses the pending state."""
    cursor = Mock(lastrowid=11)

    assert posts.create_pending_post(
        cursor,
        set_id=1,
        generation_run_id=2,
        sns_account_id=3,
    ) == 11
    cursor.execute.assert_called_once_with(
        "INSERT INTO posts "
        "(set_id, generation_run_id, sns_account_id, status) "
        "VALUES (%s, %s, %s, 'pending')",
        (1, 2, 3),
    )


def test_create_pending_post_fetches_duplicate_id() -> None:
    """A uniqueness conflict returns the existing post ID."""
    cursor = Mock()
    cursor.execute.side_effect = [
        pymysql.err.IntegrityError(1062, "duplicate"),
        None,
    ]
    cursor.fetchone.return_value = (12,)

    assert posts.create_pending_post(
        cursor,
        set_id=1,
        generation_run_id=2,
        sns_account_id=3,
    ) == 12
    assert cursor.execute.call_args_list[-1].args == (
        "SELECT id FROM posts "
        "WHERE generation_run_id = %s AND sns_account_id = %s",
        (2, 3),
    )


def test_create_pending_post_reraises_non_duplicate_integrity_error() -> None:
    """Unexpected integrity errors are not treated as idempotent."""
    cursor = Mock()
    cursor.execute.side_effect = pymysql.err.IntegrityError(1452, "foreign key")

    with pytest.raises(pymysql.err.IntegrityError):
        posts.create_pending_post(
            cursor,
            set_id=1,
            generation_run_id=2,
            sns_account_id=3,
        )


def test_update_post_caption_allows_null_template() -> None:
    """A caption without a configured template is persisted as empty text."""
    cursor = Mock()

    posts.update_post_caption(
        cursor,
        5,
        caption_template_id=None,
        caption_text="",
    )

    cursor.execute.assert_called_once_with(
        "UPDATE posts SET caption_template_id = %s, "
        "caption_text_snapshot = %s WHERE id = %s",
        (None, "", 5),
    )


def test_post_state_updates_use_expected_values(monkeypatch) -> None:
    """Container, failure, unknown, and success transitions are persisted."""
    cursor = Mock()
    fixed_now = datetime.datetime(2026, 7, 19)
    monkeypatch.setattr(posts, "now_utc", lambda: fixed_now)

    posts.update_post_container_created(
        cursor, 5, platform_container_id="container"
    )
    posts.update_post_failed(
        cursor,
        5,
        error_message="failed",
        api_response={"error": "x"},
    )
    posts.update_post_unconfirmed(
        cursor,
        5,
        error_message="unknown",
        api_response=None,
    )
    posts.update_post_success(
        cursor,
        5,
        platform_post_id="post",
        api_response={"id": "post"},
    )

    assert cursor.execute.call_args_list[0].args == (
        "UPDATE posts SET status = 'container_created', "
        "platform_container_id = %s WHERE id = %s",
        ("container", 5),
    )
    assert cursor.execute.call_args_list[1].args[1] == (
        "failed",
        json.dumps({"error": "x"}),
        5,
    )
    assert cursor.execute.call_args_list[2].args[1] == ("unknown", None, 5)
    assert cursor.execute.call_args_list[3].args[1] == (
        "post",
        json.dumps({"id": "post"}),
        fixed_now,
        5,
    )
