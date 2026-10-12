"""Tests for umigame item retrieval and JSON decoding."""

import json
from unittest.mock import Mock

import pytest

from app.models import PreviousUmigameTruth
from app.umigame_items import fetch_previous_umigame_truth, fetch_umigame_item


CRITERIA = {"points": [{"hit": "当てた", "touch": "触れた"}], "errors": ["誤り"]}
CORE_WORDS = {"words": ["核心", "秘密"], "except": ["秘密の遊び方"]}


@pytest.mark.parametrize(
    "facts, core_points, judge_criteria, core_words",
    [
        (["事実"], ["要点"], CRITERIA, CORE_WORDS),
        (
            json.dumps(["事実"], ensure_ascii=False),
            json.dumps(["要点"], ensure_ascii=False),
            json.dumps(CRITERIA, ensure_ascii=False),
            json.dumps(CORE_WORDS, ensure_ascii=False),
        ),
        (
            json.dumps(["事実"], ensure_ascii=False).encode("utf-8"),
            json.dumps(["要点"], ensure_ascii=False).encode("utf-8"),
            json.dumps(CRITERIA, ensure_ascii=False).encode("utf-8"),
            json.dumps(CORE_WORDS, ensure_ascii=False).encode("utf-8"),
        ),
    ],
)
def test_fetch_umigame_item_parses_json_fields(
    facts: object, core_points: object, judge_criteria: object, core_words: object
) -> None:
    cursor = Mock()
    cursor.fetchone.return_value = (
        4, "001-problem", "問題文", "真相", facts, core_points, judge_criteria, core_words,
        "開示する真相", "ルール", "フック", "本文",
    )
    item = fetch_umigame_item(cursor, 17)
    assert item is not None
    assert item.id == 4
    assert item.content_key == "001-problem"
    assert item.fact_sheet == ["事実"]
    assert item.core_points == ["要点"]
    assert item.judge_criteria == CRITERIA
    assert item.core_words == CORE_WORDS
    assert item.reveal_text == "開示する真相"
    assert item.caption == "本文"
    assert "FROM umigame_items" in cursor.execute.call_args.args[0]
    assert "core_points, judge_criteria, core_words" in cursor.execute.call_args.args[0]
    assert cursor.execute.call_args.args[1] == (17,)


def test_fetch_umigame_item_returns_none_without_row() -> None:
    cursor = Mock()
    cursor.fetchone.return_value = None
    assert fetch_umigame_item(cursor, 17) is None


@pytest.mark.parametrize("facts", ["broken", "{}", "[]", '[" "]', b"\xff"])
def test_fetch_umigame_item_rejects_invalid_fact_sheet(facts: object) -> None:
    cursor = Mock()
    cursor.fetchone.return_value = (
        4, "001-problem", "問題文", "真相", facts, ["要点"], CRITERIA,
        CORE_WORDS,
        "開示する真相", "ルール", "フック", "本文",
    )
    with pytest.raises(RuntimeError, match="fact_sheet"):
        fetch_umigame_item(cursor, 17)


@pytest.mark.parametrize("core_points", ["broken", "{}", "[]", '[" "]', b"\xff"])
def test_fetch_umigame_item_rejects_invalid_core_points(core_points: object) -> None:
    cursor = Mock()
    cursor.fetchone.return_value = (
        4, "001-problem", "問題文", "真相", ["事実"], core_points, CRITERIA,
        CORE_WORDS,
        "開示する真相", "ルール", "フック", "本文",
    )
    with pytest.raises(RuntimeError, match="core_points"):
        fetch_umigame_item(cursor, 17)


def test_fetch_umigame_item_keeps_null_judge_fields() -> None:
    cursor = Mock()
    cursor.fetchone.return_value = (
        4, "001-problem", "問題文", "真相", ["事実"], None, None,
        None, None, "ルール", "フック", "本文",
    )
    item = fetch_umigame_item(cursor, 17)
    assert item is not None
    assert item.core_points is None
    assert item.judge_criteria is None
    assert item.core_words is None
    assert item.reveal_text is None


@pytest.mark.parametrize("criteria", [
    "broken", b"\xff", "[]", "{}", {"points": [], "errors": []},
    {"points": [{"hit": "", "touch": "触れた"}], "errors": []},
    {"points": [{"hit": "当てた", "touch": "触れた"}], "errors": ["a"] * 4},
])
def test_fetch_umigame_item_rejects_invalid_judge_criteria(criteria: object) -> None:
    cursor = Mock()
    cursor.fetchone.return_value = (
        4, "001-problem", "問題文", "真相", ["事実"], ["要点"], criteria,
        CORE_WORDS,
        "開示する真相", "ルール", "フック", "本文",
    )
    with pytest.raises(RuntimeError, match="judge_criteria"):
        fetch_umigame_item(cursor, 17)


@pytest.mark.parametrize("value", [
    "broken", b"\xff", "[]", "{}",
    {"words": ["核心"]}, {"except": []},
    {"words": [], "except": []}, {"words": "核心", "except": []},
    {"words": ["核心"], "except": None}, {"words": ["核心"], "except": "例外"},
    {"words": ["核心", "核心"], "except": []},
    {"words": ["核心"], "except": ["例外", "例外"]},
    {"words": ["核心"], "except": [], "extra": []},
    *({"words": [word], "except": []} for word in ("", " ", "核\n心", "核\r心", 1, None, [])),
    *({"words": ["核心"], "except": [word]} for word in ("", " ", "例\n外", "例\r外", 1, None, [])),
])
def test_fetch_umigame_item_rejects_invalid_core_words(value: object) -> None:
    cursor = Mock()
    cursor.fetchone.return_value = (
        4, "001-problem", "問題文", "真相", ["事実"], ["要点"], CRITERIA,
        value, "開示する真相", "ルール", "フック", "本文",
    )
    with pytest.raises(RuntimeError, match="core_words"):
        fetch_umigame_item(cursor, 17)


@pytest.mark.parametrize("excepts", [[], ["遊び方"]])
def test_fetch_umigame_item_accepts_bytearray_core_words(excepts) -> None:
    cursor = Mock()
    value = {"words": ["遊び", "鬼"], "except": excepts}
    cursor.fetchone.return_value = (
        4, "001-problem", "問題文", "真相", ["事実"], ["要点"], CRITERIA,
        bytearray(json.dumps(value, ensure_ascii=False).encode("utf-8")),
        "開示する真相", "ルール", "フック", "本文",
    )
    assert fetch_umigame_item(cursor, 17).core_words == value


def test_fetch_previous_umigame_truth_uses_latest_success_in_set() -> None:
    cursor = Mock()
    cursor.fetchone.return_value = ("前回の題", "前回の真相")
    previous = fetch_previous_umigame_truth(cursor, 5, 17)
    assert previous == PreviousUmigameTruth("前回の題", "前回の真相")
    sql, params = cursor.execute.call_args.args
    assert "p.status = 'success'" in sql
    assert "p.set_id = %s" in sql
    assert "p.generation_run_id <> %s" in sql
    assert "ORDER BY p.posted_at DESC, p.id DESC LIMIT 1" in sql
    assert params == (5, 17)


def test_fetch_previous_umigame_truth_returns_none_on_first_post() -> None:
    cursor = Mock()
    cursor.fetchone.return_value = None
    assert fetch_previous_umigame_truth(cursor, 5, 17) is None


@pytest.mark.parametrize("row", [(None, "真相"), ("題", " "), ("題", None)])
def test_fetch_previous_umigame_truth_rejects_missing_fields(row: tuple) -> None:
    cursor = Mock()
    cursor.fetchone.return_value = row
    with pytest.raises(RuntimeError, match="previous post is missing"):
        fetch_previous_umigame_truth(cursor, 5, 17)
