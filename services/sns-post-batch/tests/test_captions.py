"""Tests for caption placeholder expansion."""

from unittest.mock import Mock

import pytest

import app.captions as captions
from app.models import QuizItem, RankingItem


def _quiz_item(**field_updates: object) -> QuizItem:
    fields: dict[str, object] = {
        "hook": "この問題、解ける？",
        "explanation": "順番に整理すると解けます。",
        "coach_comment": "ひらめきが大切！",
    }
    fields.update(field_updates)
    return QuizItem("問題文です", "答えです", fields)


def _ranking_item(**field_updates: object) -> RankingItem:
    fields: dict[str, object] = {
        "hook": "あなたの県は何位？",
        "result_list": "1位 A県\n2位 B県",
        "trivia": "地域差があります。",
        "source_display": "総務省統計",
    }
    fields.update(field_updates)
    return RankingItem("住みたい都道府県ランキング", fields)


def test_build_caption_passes_through_without_reading_items(monkeypatch) -> None:
    quiz_fetch = Mock()
    ranking_fetch = Mock()
    monkeypatch.setattr(captions, "fetch_quiz_item", quiz_fetch)
    monkeypatch.setattr(captions, "fetch_ranking_item", ranking_fetch)
    assert captions.build_caption(Mock(), 3, "固定文 #AI生成") == "固定文 #AI生成"
    quiz_fetch.assert_not_called()
    ranking_fetch.assert_not_called()


def test_build_caption_expands_all_supported_placeholders(monkeypatch) -> None:
    fetch = Mock(return_value=_quiz_item())
    monkeypatch.setattr(captions, "fetch_quiz_item", fetch)
    ranking_fetch = Mock()
    monkeypatch.setattr(captions, "fetch_ranking_item", ranking_fetch)
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
    ranking_fetch.assert_not_called()


def test_build_caption_requires_item_for_placeholder(monkeypatch) -> None:
    monkeypatch.setattr(captions, "fetch_quiz_item", lambda cursor, run_id: None)
    monkeypatch.setattr(captions, "fetch_ranking_item", lambda cursor, run_id: None)
    with pytest.raises(
        RuntimeError,
        match="quiz_items or ranking_items.*generation_run_id=8",
    ):
        captions.build_caption(Mock(), 8, "{{answer}}")


def test_build_caption_rejects_missing_or_empty_source(monkeypatch) -> None:
    monkeypatch.setattr(
        captions,
        "fetch_quiz_item",
        lambda cursor, run_id: _quiz_item(explanation=" "),
    )
    monkeypatch.setattr(captions, "fetch_ranking_item", Mock())
    with pytest.raises(RuntimeError, match="explanation"):
        captions.build_caption(Mock(), 8, "{{explanation}}")


def test_build_caption_rejects_unknown_lowercase_token_without_db_read(
    monkeypatch,
) -> None:
    fetch = Mock()
    monkeypatch.setattr(captions, "fetch_quiz_item", fetch)
    ranking_fetch = Mock()
    monkeypatch.setattr(captions, "fetch_ranking_item", ranking_fetch)
    with pytest.raises(RuntimeError, match="anser"):
        captions.build_caption(Mock(), 8, "答え: {{anser}}")
    fetch.assert_not_called()
    ranking_fetch.assert_not_called()


def test_build_caption_expands_all_ranking_placeholders(monkeypatch) -> None:
    quiz_fetch = Mock(return_value=None)
    ranking_fetch = Mock(return_value=_ranking_item())
    monkeypatch.setattr(captions, "fetch_quiz_item", quiz_fetch)
    monkeypatch.setattr(captions, "fetch_ranking_item", ranking_fetch)
    cursor = Mock()
    template = "{{hook}}\n{{title}}\n{{result_list}}\n{{trivia}}\n{{source_display}}"

    assert captions.build_caption(cursor, 8, template) == (
        "あなたの県は何位？\n住みたい都道府県ランキング\n"
        "1位 A県\n2位 B県\n地域差があります。\n総務省統計"
    )
    quiz_fetch.assert_called_once_with(cursor, 8)
    ranking_fetch.assert_called_once_with(cursor, 8)


def test_build_caption_rejects_ranking_token_for_quiz_item(monkeypatch) -> None:
    monkeypatch.setattr(
        captions, "fetch_quiz_item", lambda cursor, run_id: _quiz_item()
    )
    ranking_fetch = Mock()
    monkeypatch.setattr(captions, "fetch_ranking_item", ranking_fetch)
    with pytest.raises(RuntimeError, match="result_list"):
        captions.build_caption(Mock(), 8, "{{result_list}}")
    ranking_fetch.assert_not_called()


def test_build_caption_rejects_quiz_token_for_ranking_item(monkeypatch) -> None:
    monkeypatch.setattr(captions, "fetch_quiz_item", lambda cursor, run_id: None)
    monkeypatch.setattr(
        captions, "fetch_ranking_item", lambda cursor, run_id: _ranking_item()
    )
    with pytest.raises(RuntimeError, match="answer"):
        captions.build_caption(Mock(), 8, "{{answer}}")
