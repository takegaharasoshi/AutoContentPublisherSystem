"""Tests for caption placeholder expansion."""

from unittest.mock import Mock

import pytest

import app.captions as captions
from app.models import PreviousUmigameTruth, QuizItem, RankingItem, UmigameItem


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


def _umigame_item(**updates: object) -> UmigameItem:
    fields: dict[str, object] = {
        "id": 4,
        "content_key": "001-problem",
        "problem_text": "なぜ？",
        "truth": "真相",
        "fact_sheet": ["事実"],
        "core_points": ["要点"],
        "judge_criteria": {"points": [{"hit": "当てた", "touch": "触れた"}], "errors": []},
        "core_words": {"words": ["核心"], "except": []},
        "reveal_text": "開示する真相",
        "rule_text": "質問してね",
        "hook": "解けるかな？",
        "caption": "本文 #AIart",
    }
    fields.update(updates)
    return UmigameItem(**fields)


def test_build_caption_passes_through_without_reading_items(monkeypatch) -> None:
    quiz_fetch = Mock()
    ranking_fetch = Mock()
    umigame_fetch = Mock()
    monkeypatch.setattr(captions, "fetch_quiz_item", quiz_fetch)
    monkeypatch.setattr(captions, "fetch_ranking_item", ranking_fetch)
    monkeypatch.setattr(captions, "fetch_umigame_item", umigame_fetch)
    assert captions.build_caption(Mock(), 3, "固定文 #AI生成") == "固定文 #AI生成"
    quiz_fetch.assert_not_called()
    ranking_fetch.assert_not_called()
    umigame_fetch.assert_not_called()


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
    monkeypatch.setattr(captions, "fetch_umigame_item", lambda cursor, run_id: None)
    with pytest.raises(
        RuntimeError,
        match="quiz_items or ranking_items or umigame_items.*generation_run_id=8",
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


def test_build_caption_expands_umigame_placeholders_in_fetch_order(monkeypatch) -> None:
    calls: list[str] = []

    def no_quiz(*args):
        calls.append("quiz")
        return None

    def no_ranking(*args):
        calls.append("ranking")
        return None

    def get_umigame(*args):
        calls.append("umigame")
        return _umigame_item()

    monkeypatch.setattr(captions, "fetch_quiz_item", no_quiz)
    monkeypatch.setattr(captions, "fetch_ranking_item", no_ranking)
    monkeypatch.setattr(captions, "fetch_umigame_item", get_umigame)

    assert captions.build_caption(
        Mock(), 8, "{{caption}}\n{{problem_text}}\n{{hook}}\n{{rule_text}}"
    ) == "本文 #AIart\nなぜ？\n解けるかな？\n質問してね"
    assert calls == ["quiz", "ranking", "umigame"]


@pytest.mark.parametrize("token", ["answer", "result_list"])
def test_build_caption_rejects_other_family_token_for_umigame(
    monkeypatch, token: str
) -> None:
    monkeypatch.setattr(captions, "fetch_quiz_item", lambda *args: None)
    monkeypatch.setattr(captions, "fetch_ranking_item", lambda *args: None)
    monkeypatch.setattr(captions, "fetch_umigame_item", lambda *args: _umigame_item())
    with pytest.raises(RuntimeError, match=token):
        captions.build_caption(Mock(), 8, "{{" + token + "}}")


@pytest.mark.parametrize("family", ["quiz", "ranking"])
def test_build_caption_rejects_umigame_token_for_other_family(
    monkeypatch, family: str
) -> None:
    monkeypatch.setattr(
        captions, "fetch_quiz_item",
        lambda *args: _quiz_item() if family == "quiz" else None,
    )
    monkeypatch.setattr(
        captions, "fetch_ranking_item",
        lambda *args: _ranking_item() if family == "ranking" else None,
    )
    umigame_fetch = Mock()
    monkeypatch.setattr(captions, "fetch_umigame_item", umigame_fetch)
    with pytest.raises(RuntimeError, match="caption"):
        captions.build_caption(Mock(), 8, "{{caption}}")
    umigame_fetch.assert_not_called()


def test_build_caption_rejects_unknown_umigame_like_token_without_fetch(
    monkeypatch,
) -> None:
    umigame_fetch = Mock()
    monkeypatch.setattr(captions, "fetch_umigame_item", umigame_fetch)
    with pytest.raises(RuntimeError, match="fact_sheet"):
        captions.build_caption(Mock(), 8, "{{fact_sheet}}")
    umigame_fetch.assert_not_called()


TRUTH_TEMPLATE = "{{caption}}{{prev_truth_block}}"


def _patch_umigame(monkeypatch, previous: object) -> Mock:
    monkeypatch.setattr(captions, "fetch_quiz_item", lambda *args: None)
    monkeypatch.setattr(captions, "fetch_ranking_item", lambda *args: None)
    monkeypatch.setattr(captions, "fetch_umigame_item", lambda *args: _umigame_item())
    fetch_previous = Mock(return_value=previous)
    monkeypatch.setattr(captions, "fetch_previous_umigame_truth", fetch_previous)
    return fetch_previous


def test_build_caption_appends_previous_truth_block(monkeypatch) -> None:
    fetch_previous = _patch_umigame(
        monkeypatch, PreviousUmigameTruth("55年目の年賀状", "男は中学3年の春、\n2人は会っていない。")
    )
    cursor = Mock()
    assert captions.build_caption(cursor, 8, TRUTH_TEMPLATE, set_id=5) == (
        "本文 #AIart\n\n\n\n"
        "――― 前回の問題「55年目の年賀状」の真相（ネタバレ注意）―――\n"
        "・\n・\n・\n・\n"
        "【真相】\n"
        "男は中学3年の春、\n2人は会っていない。"
    )
    fetch_previous.assert_called_once_with(cursor, 5, 8)


def test_build_caption_omits_block_on_first_post(monkeypatch) -> None:
    _patch_umigame(monkeypatch, None)
    assert captions.build_caption(Mock(), 8, TRUTH_TEMPLATE, set_id=5) == "本文 #AIart"


def test_build_caption_does_not_read_previous_without_token(monkeypatch) -> None:
    fetch_previous = _patch_umigame(monkeypatch, None)
    assert captions.build_caption(Mock(), 8, "{{caption}}", set_id=5) == "本文 #AIart"
    fetch_previous.assert_not_called()


def test_build_caption_requires_set_id_for_previous_truth(monkeypatch) -> None:
    _patch_umigame(monkeypatch, None)
    with pytest.raises(RuntimeError, match="set_id is required"):
        captions.build_caption(Mock(), 8, TRUTH_TEMPLATE)


def test_build_caption_rejects_caption_over_limit(monkeypatch) -> None:
    _patch_umigame(monkeypatch, PreviousUmigameTruth("題", "あ" * 2200))
    with pytest.raises(RuntimeError, match="exceeds the limit"):
        captions.build_caption(Mock(), 8, TRUTH_TEMPLATE, set_id=5)


def test_build_caption_accepts_caption_at_limit(monkeypatch) -> None:
    _patch_umigame(monkeypatch, PreviousUmigameTruth("題", "x"))
    base = captions.build_caption(Mock(), 8, TRUTH_TEMPLATE, set_id=5)
    filler = "あ" * (captions.MAX_CAPTION_LENGTH - len(base) + 1)
    _patch_umigame(monkeypatch, PreviousUmigameTruth("題", filler))
    caption = captions.build_caption(Mock(), 8, TRUTH_TEMPLATE, set_id=5)
    assert len(caption) == captions.MAX_CAPTION_LENGTH


@pytest.mark.parametrize("family", ["quiz", "ranking"])
def test_build_caption_rejects_previous_truth_for_other_family(
    monkeypatch, family: str
) -> None:
    monkeypatch.setattr(
        captions, "fetch_quiz_item",
        lambda *args: _quiz_item() if family == "quiz" else None,
    )
    monkeypatch.setattr(
        captions, "fetch_ranking_item",
        lambda *args: _ranking_item() if family == "ranking" else None,
    )
    fetch_previous = Mock()
    monkeypatch.setattr(captions, "fetch_previous_umigame_truth", fetch_previous)
    with pytest.raises(RuntimeError, match="prev_truth_block"):
        captions.build_caption(Mock(), 8, "{{hook}}{{prev_truth_block}}", set_id=5)
    fetch_previous.assert_not_called()


@pytest.mark.parametrize(
    "family, template, expected",
    [
        ("quiz", "{{hook}}\n" + "い" * 2300, "この問題、解ける？\n" + "い" * 2300),
        ("ranking", "{{title}}", "住みたい都道府県ランキング"),
    ],
)
def test_build_caption_leaves_other_sets_unchanged(
    monkeypatch, family: str, template: str, expected: str
) -> None:
    monkeypatch.setattr(
        captions, "fetch_quiz_item",
        lambda *args: _quiz_item() if family == "quiz" else None,
    )
    monkeypatch.setattr(
        captions, "fetch_ranking_item",
        lambda *args: _ranking_item() if family == "ranking" else None,
    )
    fetch_previous = Mock()
    monkeypatch.setattr(captions, "fetch_previous_umigame_truth", fetch_previous)
    assert captions.build_caption(Mock(), 8, template, set_id=5) == expected
    fetch_previous.assert_not_called()
