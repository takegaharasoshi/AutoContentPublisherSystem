"""Tests for the runtime-only prebuilt quiz video generator."""

from __future__ import annotations

import datetime
import json
from unittest.mock import Mock

import pytest

from app.generators import GeneratorContext
from app.generators import quiz_prebuilt as quiz
from app.models import PromptConfig


def _parameters() -> str:
    return json.dumps(
        {
            "slots": [
                {
                    "from_jst_hour": 0,
                    "quiz_type": "L3",
                    "difficulty": "standard",
                    "slot_code": "noon",
                    "slot_label": "昼の脳みそトレ",
                    "slot_hook": "30秒で解けたら天才",
                }
            ]
        }
    )


def _fields(**updates: object) -> dict[str, object]:
    fields: dict[str, object] = {
        "hook": "推定できる？",
        "hint": "一人あたりから考えよう",
        "question": "日本にある信号機の数を推定してください。",
        "answer": "約20万基（目安）",
        "explanation": "前提から順に分解して概算します。",
        "coach_comment": "推定ルートが大切！",
        "tags": ["脳トレ", "推定", "クイズ"],
        "summary": "日本の信号機数を推定",
        "illustration_scene": "文字のない明るい街角の風景",
    }
    fields.update(updates)
    return fields


def _stock_row(
    *,
    fields: dict[str, object] | None = None,
    audio_asset_id: int | None = 77,
    last_used_at: datetime.datetime | None = None,
) -> tuple[object, ...]:
    return (
        91,
        "日本にある信号機の数を推定してください。",
        "約20万基（目安）",
        json.dumps(fields or _fields(), ensure_ascii=False),
        "assets/logic-training-1/prebuilt/noon-007.mp4",
        audio_asset_id,
        last_used_at,
    )


class Cursor:
    """Cursor fake for the prebuilt generator's fixed query sequence."""

    def __init__(
        self,
        *,
        stock_row: tuple[object, ...] | None = None,
        unbuilt_count: int = 0,
    ) -> None:
        self.stock_row = _stock_row() if stock_row is None else stock_row
        self.unbuilt_count = unbuilt_count
        self.calls: list[tuple[str, tuple[object, ...]]] = []
        self.current = ""

    def execute(self, sql: str, params: tuple[object, ...]) -> None:
        self.calls.append((sql, params))
        self.current = sql

    def fetchone(self) -> tuple[object, ...] | None:
        if "COUNT(*)" in self.current:
            return (self.unbuilt_count,)
        if "FROM quiz_stock_items" in self.current:
            return self.stock_row
        raise AssertionError(f"Unexpected fetchone: {self.current}")


def _context(cursor: Cursor) -> GeneratorContext:
    return GeneratorContext(
        prompt_config=PromptConfig(5, 9, "unused", None, _parameters()),
        cursor=cursor,
        s3_client=Mock(),
        s3_bucket="bucket",
        scheduled_at=datetime.datetime(2026, 8, 7, tzinfo=datetime.timezone.utc),
        generation_run_id=123,
    )


def test_generate_fetches_prebuilt_video_and_stages_history_and_lru(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    cursor = Cursor()
    get_object = Mock(return_value=b"prebuilt-mp4")
    monkeypatch.setattr(quiz, "get_object", get_object)
    used_at = datetime.datetime(2026, 8, 7, 3, 4, 5)
    monkeypatch.setattr(quiz, "now_utc", lambda: used_at)

    context = _context(cursor)
    result = quiz.generate(context)

    assert result.media[0].content == b"prebuilt-mp4"
    assert result.media[0].file_format == "mp4"
    assert result.media[0].width == 1080
    assert result.media[0].height == 1920
    assert result.media[0].duration_seconds == 16
    assert result.media[0].audio_asset_id == 77
    assert result.intermediates == []
    get_object.assert_called_once_with(
        "bucket", "assets/logic-training-1/prebuilt/noon-007.mp4", client=context.s3_client
    )
    queries = [call[0] for call in cursor.calls]
    assert "video_s3_key IS NOT NULL" in queries[0]
    assert "INSERT INTO quiz_items" in queries[2]
    assert "use_count = use_count + 1" in queries[3]
    assert cursor.calls[3][1] == (used_at, 91)
    assert all("UPDATE audio_assets" not in query for query in queries)


def test_generate_fails_when_no_built_stock_exists() -> None:
    cursor = Cursor()
    cursor.stock_row = None
    with pytest.raises(RuntimeError, match="No built active quiz stock item"):
        quiz.generate(_context(cursor))


def test_generate_warns_for_unbuilt_and_reused_stock(
    monkeypatch: pytest.MonkeyPatch,
    caplog: pytest.LogCaptureFixture,
) -> None:
    cursor = Cursor(
        stock_row=_stock_row(last_used_at=datetime.datetime(2026, 8, 1)),
        unbuilt_count=2,
    )
    monkeypatch.setattr(quiz, "get_object", lambda *args, **kwargs: b"video")

    quiz.generate(_context(cursor))

    assert "being reused" in caplog.text
    assert "remain unbuilt" in caplog.text


def test_generate_fails_for_missing_baked_audio() -> None:
    cursor = Cursor(stock_row=_stock_row(audio_asset_id=None))
    with pytest.raises(RuntimeError, match="video_audio_asset_id is required"):
        quiz.generate(_context(cursor))


def test_generate_propagates_s3_error(monkeypatch: pytest.MonkeyPatch) -> None:
    cursor = Cursor()
    monkeypatch.setattr(
        quiz,
        "get_object",
        Mock(side_effect=RuntimeError("NoSuchKey")),
    )
    with pytest.raises(RuntimeError, match="NoSuchKey"):
        quiz.generate(_context(cursor))
    assert not any("INSERT INTO quiz_items" in call[0] for call in cursor.calls)


def test_generate_fails_for_invalid_caption_fields() -> None:
    cursor = Cursor(stock_row=_stock_row(fields=_fields(hint="")))
    with pytest.raises(RuntimeError, match="content_fields.hint is required"):
        quiz.generate(_context(cursor))


def test_generate_accepts_long_caption_only_fields(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """キャプション専用フィールドは版面に出ないため長さを縛らない。

    2026-09-04 夜の停止（answer_text 37 字）の再発防止。
    """
    long_answer = "1本目の両端と2本目の片端に同時点火。1本目が尽きたら2本目の残り端に点火"
    row = list(_stock_row(fields=_fields(
        answer=long_answer,
        explanation="順を追って説明します。" * 12,
        coach_comment="手順そのものが答えになる問題は落ち着いて順に追おう！",
    )))
    row[2] = long_answer
    monkeypatch.setattr(quiz, "get_object", lambda *args, **kwargs: b"video")

    cursor = Cursor(stock_row=tuple(row))
    result = quiz.generate(_context(cursor))

    assert len(long_answer) > 30
    assert result.media[0].content == b"video"
    insert = next(call for call in cursor.calls if "INSERT INTO quiz_items" in call[0])
    assert long_answer in insert[1]


def test_generate_still_enforces_question_length() -> None:
    """question_text は版面に焼き込まれるため上限を維持する。"""
    row = list(_stock_row())
    row[1] = "あ" * 91
    with pytest.raises(RuntimeError, match="question_text exceeds 90"):
        quiz.generate(_context(Cursor(stock_row=tuple(row))))


def test_generate_still_requires_non_empty_answer() -> None:
    row = list(_stock_row())
    row[2] = "  "
    with pytest.raises(RuntimeError, match="answer_text is required"):
        quiz.generate(_context(Cursor(stock_row=tuple(row))))
