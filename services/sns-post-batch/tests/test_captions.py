"""Tests for caption placeholder expansion."""

from unittest.mock import Mock

import pytest

import app.captions as captions
from app.models import QuizItem


def _quiz_item(**field_updates: object) -> QuizItem:
    fields: dict[str, object] = {
        "hook": "この問題、解ける？",
        "explanation": "順番に整理すると解けます。",
        "coach_comment": "ひらめきが大切！",
    }
    fields.update(field_updates)
    return QuizItem("問題文です", "答えです", fields)


def test_build_caption_passes_through_without_reading_quiz_item(monkeypatch) -> None:
    fetch = Mock()
    monkeypatch.setattr(captions, "fetch_quiz_item", fetch)
    assert captions.build_caption(Mock(), 3, "固定文 #AI生成") == "固定文 #AI生成"
    fetch.assert_not_called()


def test_build_caption_expands_all_supported_placeholders(monkeypatch) -> None:
    fetch = Mock(return_value=_quiz_item())
    monkeypatch.setattr(captions, "fetch_quiz_item", fetch)
    cursor = Mock()
    template = (
        "{{hook}}\n{{question}}\n答え: {{answer}}\n"
        "{{explanation}}\n{{coach_comment}}"
    )
    assert captions.build_caption(cursor, 8, template) == (
        "この問題、解ける？\n問題文です\n答え: 答えです\n"
        "順番に整理すると解けます。\nひらめきが大切！"
    )
    fetch.assert_called_once_with(cursor, 8)


def test_build_caption_requires_quiz_item_for_placeholder(monkeypatch) -> None:
    monkeypatch.setattr(captions, "fetch_quiz_item", lambda cursor, run_id: None)
    with pytest.raises(RuntimeError, match="quiz_items row is required"):
        captions.build_caption(Mock(), 8, "{{answer}}")


def test_build_caption_rejects_missing_or_empty_source(monkeypatch) -> None:
    monkeypatch.setattr(
        captions,
        "fetch_quiz_item",
        lambda cursor, run_id: _quiz_item(explanation=" "),
    )
    with pytest.raises(RuntimeError, match="explanation"):
        captions.build_caption(Mock(), 8, "{{explanation}}")


def test_build_caption_rejects_unknown_lowercase_token_without_db_read(
    monkeypatch,
) -> None:
    fetch = Mock()
    monkeypatch.setattr(captions, "fetch_quiz_item", fetch)
    with pytest.raises(RuntimeError, match="anser"):
        captions.build_caption(Mock(), 8, "答え: {{anser}}")
    fetch.assert_not_called()
