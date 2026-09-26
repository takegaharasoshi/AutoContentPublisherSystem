"""Tests for the prebuilt umigame video generator."""

from __future__ import annotations

import datetime
import json
from unittest.mock import Mock

import pytest

from app.generators import GeneratorContext
from app.generators import umigame_prebuilt as umigame
from app.models import PromptConfig


def _stock_row(**updates: object) -> tuple[object, ...]:
    item: dict[str, object] = {
        "id": 91,
        "content_key": "001-lighthouse-letter",
        "problem_text": "問題文",
        "truth": "真相",
        "fact_sheet": json.dumps(["確定事実", "別の事実"], ensure_ascii=False),
        "rule_text": "質問のルール",
        "caption": "本文 #AIart",
        "hook": "なぜでしょう？",
        "video_s3_key": "assets/umigame-soup-1/prebuilt/001.mp4",
        "video_audio_asset_id": 77,
        "use_count": 0,
    }
    item.update(updates)
    return tuple(item.values())


class Cursor:
    """Record SQL and simulate its LRU selection for built, active rows."""

    def __init__(self, rows: list[tuple[object, ...]] | None = None) -> None:
        self.rows = [_stock_row()] if rows is None else rows
        self.calls: list[tuple[str, tuple[object, ...]]] = []

    def execute(self, sql: str, params: tuple[object, ...]) -> None:
        self.calls.append((sql, params))

    def fetchone(self) -> tuple[object, ...] | None:
        assert "FROM umigame_stock_items" in self.calls[-1][0]
        return self.rows[0] if self.rows else None


def _context(cursor: Cursor, parameters: str | None = None) -> GeneratorContext:
    return GeneratorContext(
        prompt_config=PromptConfig(
            5, 9, "unused", None,
            '{"duration_seconds": 24}' if parameters is None else parameters,
        ),
        cursor=cursor,
        s3_client=Mock(),
        s3_bucket="bucket",
        scheduled_at=datetime.datetime(2026, 9, 26, tzinfo=datetime.UTC),
        generation_run_id=123,
    )


def test_generate_fetches_video_and_stages_stock_and_history(monkeypatch) -> None:
    cursor = Cursor()
    context = _context(cursor)
    fetch_video = Mock(return_value=b"mp4 bytes")
    monkeypatch.setattr(umigame, "get_object", fetch_video)
    used_at = datetime.datetime(2026, 9, 26, 11, 0, 1)
    monkeypatch.setattr(umigame, "now_utc", lambda: used_at)

    result = umigame.generate(context)

    assert len(result.media) == 1
    assert result.media[0].content == b"mp4 bytes"
    assert result.media[0].file_format == "mp4"
    assert (result.media[0].width, result.media[0].height) == (1080, 1920)
    assert result.media[0].duration_seconds == 24
    assert result.media[0].audio_asset_id == 77
    assert result.intermediates == []
    fetch_video.assert_called_once_with(
        "bucket", "assets/umigame-soup-1/prebuilt/001.mp4",
        client=context.s3_client,
    )
    assert cursor.calls[1][1] == (used_at, 91)
    assert cursor.calls[2][1] == (
        9, 123, 91, "001-lighthouse-letter", "問題文", "真相",
        '["確定事実", "別の事実"]', "質問のルール", "なぜでしょう？",
        "本文 #AIart",
    )


def test_first_use_follows_id_order_before_any_reuse(monkeypatch) -> None:
    # Simulate the DB returning the first row after applying the SQL's order.
    # IDs reflect INSERT order; a used row must follow every unused row.
    rows = [
        _stock_row(id=12, content_key="012-second"),
        _stock_row(id=13, content_key="013-third"),
        _stock_row(id=2, content_key="002-used", use_count=1),
    ]
    cursor = Cursor(rows)
    monkeypatch.setattr(umigame, "get_object", lambda *args, **kwargs: b"mp4")

    umigame.generate(_context(cursor))

    query = " ".join(cursor.calls[0][0].split())
    assert "WHERE set_id = %s AND is_active = 1 AND video_s3_key IS NOT NULL" in query
    assert "ORDER BY last_used_at IS NULL DESC, last_used_at ASC, id ASC" in query
    assert query.endswith("LIMIT 1 FOR UPDATE")
    assert cursor.calls[1][1][1] == 12
    assert cursor.calls[2][1][3] == "012-second"


@pytest.mark.parametrize(
    "parameters",
    ["{}", "", "null", "[]", "not json", '{"duration_seconds": 20}',
     '{"duration_seconds": "24"}', '{"duration_seconds": true}',
     '{"duration_seconds": 24, "slots": []}'],
)
def test_generate_rejects_invalid_parameters_before_query(parameters: str) -> None:
    cursor = Cursor()
    with pytest.raises(RuntimeError, match="parameters|duration_seconds"):
        umigame.generate(_context(cursor, parameters))
    assert cursor.calls == []


def test_generate_fails_when_no_built_stock_exists() -> None:
    with pytest.raises(RuntimeError, match="No built active umigame stock item"):
        umigame.generate(_context(Cursor([])))


@pytest.mark.parametrize(
    "field", ["problem_text", "truth", "rule_text", "hook", "caption", "content_key"]
)
def test_generate_rejects_blank_required_field(field: str) -> None:
    with pytest.raises(RuntimeError, match=field):
        umigame.generate(_context(Cursor([_stock_row(**{field: "  "})])))


@pytest.mark.parametrize(
    "updates, message",
    [
        ({"video_s3_key": ""}, "video_s3_key"),
        ({"video_audio_asset_id": None}, "video_audio_asset_id"),
    ],
)
def test_generate_rejects_invalid_video_reference(
    updates: dict[str, object], message: str
) -> None:
    with pytest.raises(RuntimeError, match=message):
        umigame.generate(_context(Cursor([_stock_row(**updates)])))


@pytest.mark.parametrize(
    "value",
    [None, "{}", "[]", '["valid", ""]', '["valid", 2]', "broken",
     b'["valid", ""]', b"\xff", ["valid", None]],
)
def test_generate_rejects_invalid_fact_sheet(value: object) -> None:
    with pytest.raises(RuntimeError, match="fact_sheet"):
        umigame.generate(_context(Cursor([_stock_row(fact_sheet=value)])))


@pytest.mark.parametrize("value", [["事実"], b'["\xe4\xba\x8b\xe5\xae\x9f"]'])
def test_generate_accepts_decoded_fact_sheet(monkeypatch, value: object) -> None:
    monkeypatch.setattr(umigame, "get_object", lambda *args, **kwargs: b"mp4")
    cursor = Cursor([_stock_row(fact_sheet=value)])
    umigame.generate(_context(cursor))
    assert json.loads(cursor.calls[2][1][6]) == ["事実"]


def test_generate_fails_when_s3_download_fails_without_staging_db(monkeypatch) -> None:
    cursor = Cursor()
    monkeypatch.setattr(
        umigame, "get_object", Mock(side_effect=RuntimeError("S3 missing"))
    )
    with pytest.raises(RuntimeError, match="S3 missing"):
        umigame.generate(_context(cursor))
    assert len(cursor.calls) == 1


def test_generate_warns_when_reusing_stock(monkeypatch, caplog) -> None:
    monkeypatch.setattr(umigame, "get_object", lambda *args, **kwargs: b"mp4")
    umigame.generate(_context(Cursor([_stock_row(use_count=1)])))
    assert "being reused" in caplog.text
