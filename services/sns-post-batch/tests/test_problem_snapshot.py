"""Tests for the published problem snapshot artifact."""

from __future__ import annotations

import datetime
import json
from unittest.mock import Mock

import pytest

import app.problem_snapshot as snapshot
from app.models import UmigameItem


POSTED_AT = datetime.datetime(2026, 9, 26, 11, 0, 12)


def _item() -> UmigameItem:
    return UmigameItem(
        42, "001-lighthouse-letter", "なぜ？", "真相です", ["事実１", "事実２"],
        "質問のルール", "フック", "本文 #AIart",
    )


def _write(cursor: Mock, connection: Mock) -> bool:
    return snapshot.write_problem_snapshot(
        cursor,
        connection,
        set_id=9,
        set_code="umigame-soup-1",
        generation_run_id=123,
        media_id="17912345678901234",
        posted_at=POSTED_AT,
        s3_bucket="bucket",
        s3_client=Mock(),
    )


def test_write_problem_snapshot_puts_schema_then_updates_db(monkeypatch) -> None:
    cursor = Mock()
    cursor.fetchone.return_value = ("固定プロンプト",)
    connection = Mock()
    events: list[str] = []
    item_fetch = Mock(return_value=_item())
    monkeypatch.setattr(snapshot, "fetch_umigame_item", item_fetch)
    put = Mock(side_effect=lambda *args, **kwargs: events.append("put"))
    monkeypatch.setattr(snapshot, "put_object", put)
    saved_at = datetime.datetime(2026, 9, 26, 11, 0, 13)
    monkeypatch.setattr(snapshot, "now_utc", lambda: saved_at)
    cursor.execute.side_effect = lambda *args: events.append("sql")
    connection.commit.side_effect = lambda: events.append("commit")

    assert _write(cursor, connection)

    item_fetch.assert_called_once_with(cursor, 123)
    assert "WHERE set_id = %s AND is_active = 1 ORDER BY id LIMIT 1" in (
        cursor.execute.call_args_list[0].args[0]
    )
    assert cursor.execute.call_args_list[0].args[1] == (9,)
    assert events == ["sql", "put", "sql", "commit"]
    assert put.call_args.args[0:2] == (
        "bucket", "assets/umigame-soup-1/problems/17912345678901234.json"
    )
    assert put.call_args.kwargs["content_type"] == "application/json; charset=utf-8"
    body = put.call_args.args[2]
    assert isinstance(body, bytes)
    assert b"\\u" not in body
    assert json.loads(body.decode("utf-8")) == {
        "schema_version": 1,
        "set_code": "umigame-soup-1",
        "media_id": "17912345678901234",
        "content_key": "001-lighthouse-letter",
        "posted_at": "2026-09-26T11:00:12Z",
        "problem_text": "なぜ？",
        "truth": "真相です",
        "fact_sheet": ["事実１", "事実２"],
        "rule_text": "質問のルール",
        "master_rules": "固定プロンプト",
    }
    assert "UPDATE umigame_items SET snapshot_s3_key" in (
        cursor.execute.call_args_list[1].args[0]
    )
    assert cursor.execute.call_args_list[1].args[1] == (
        "assets/umigame-soup-1/problems/17912345678901234.json", saved_at, 42
    )


def test_write_problem_snapshot_skips_run_without_item(monkeypatch) -> None:
    cursor = Mock()
    connection = Mock()
    monkeypatch.setattr(snapshot, "fetch_umigame_item", Mock(return_value=None))
    put = Mock()
    monkeypatch.setattr(snapshot, "put_object", put)

    assert not _write(cursor, connection)
    cursor.execute.assert_not_called()
    put.assert_not_called()
    connection.commit.assert_not_called()


@pytest.mark.parametrize("prompt_row", [None, (None,), (" ",)])
def test_write_problem_snapshot_requires_active_prompt(monkeypatch, prompt_row) -> None:
    cursor = Mock()
    cursor.fetchone.return_value = prompt_row
    connection = Mock()
    monkeypatch.setattr(snapshot, "fetch_umigame_item", Mock(return_value=_item()))
    put = Mock()
    monkeypatch.setattr(snapshot, "put_object", put)
    with pytest.raises(RuntimeError, match="prompt_configs"):
        _write(cursor, connection)
    put.assert_not_called()
    assert cursor.execute.call_count == 1


def test_write_problem_snapshot_does_not_update_db_after_s3_failure(
    monkeypatch,
) -> None:
    cursor = Mock()
    cursor.fetchone.return_value = ("固定プロンプト",)
    connection = Mock()
    monkeypatch.setattr(snapshot, "fetch_umigame_item", Mock(return_value=_item()))
    monkeypatch.setattr(
        snapshot, "put_object", Mock(side_effect=RuntimeError("S3 failed"))
    )
    with pytest.raises(RuntimeError, match="S3 failed"):
        _write(cursor, connection)
    assert cursor.execute.call_count == 1
    connection.commit.assert_not_called()


def test_write_problem_snapshot_propagates_db_update_failure(monkeypatch) -> None:
    cursor = Mock()
    cursor.fetchone.return_value = ("固定プロンプト",)
    cursor.execute.side_effect = [None, RuntimeError("DB failed")]
    connection = Mock()
    monkeypatch.setattr(snapshot, "fetch_umigame_item", Mock(return_value=_item()))
    put = Mock()
    monkeypatch.setattr(snapshot, "put_object", put)
    with pytest.raises(RuntimeError, match="DB failed"):
        _write(cursor, connection)
    put.assert_called_once()
    connection.commit.assert_not_called()


def test_posted_at_normalizes_aware_offset_to_utc() -> None:
    posted_at = datetime.datetime(
        2026, 9, 26, 20, 0, 12,
        tzinfo=datetime.timezone(datetime.timedelta(hours=9)),
    )
    assert snapshot._posted_at_utc(posted_at) == "2026-09-26T11:00:12Z"
