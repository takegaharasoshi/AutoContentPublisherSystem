"""Tests for umigame item retrieval and JSON decoding."""

import json
from unittest.mock import Mock

import pytest

from app.umigame_items import fetch_umigame_item


CRITERIA = {"points": [{"hit": "当てた", "touch": "触れた"}], "errors": ["誤り"]}


@pytest.mark.parametrize(
    "facts, core_points, judge_criteria",
    [
        (["事実"], ["要点"], CRITERIA),
        (
            json.dumps(["事実"], ensure_ascii=False),
            json.dumps(["要点"], ensure_ascii=False),
            json.dumps(CRITERIA, ensure_ascii=False),
        ),
        (
            json.dumps(["事実"], ensure_ascii=False).encode("utf-8"),
            json.dumps(["要点"], ensure_ascii=False).encode("utf-8"),
            json.dumps(CRITERIA, ensure_ascii=False).encode("utf-8"),
        ),
    ],
)
def test_fetch_umigame_item_parses_json_fields(
    facts: object, core_points: object, judge_criteria: object
) -> None:
    cursor = Mock()
    cursor.fetchone.return_value = (
        4, "001-problem", "問題文", "真相", facts, core_points, judge_criteria,
        "開示する真相", "ルール", "フック", "本文",
    )
    item = fetch_umigame_item(cursor, 17)
    assert item is not None
    assert item.id == 4
    assert item.content_key == "001-problem"
    assert item.fact_sheet == ["事実"]
    assert item.core_points == ["要点"]
    assert item.judge_criteria == CRITERIA
    assert item.reveal_text == "開示する真相"
    assert item.caption == "本文"
    assert "FROM umigame_items" in cursor.execute.call_args.args[0]
    assert "core_points, judge_criteria" in cursor.execute.call_args.args[0]
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
        "開示する真相", "ルール", "フック", "本文",
    )
    with pytest.raises(RuntimeError, match="fact_sheet"):
        fetch_umigame_item(cursor, 17)


@pytest.mark.parametrize("core_points", ["broken", "{}", "[]", '[" "]', b"\xff"])
def test_fetch_umigame_item_rejects_invalid_core_points(core_points: object) -> None:
    cursor = Mock()
    cursor.fetchone.return_value = (
        4, "001-problem", "問題文", "真相", ["事実"], core_points, CRITERIA,
        "開示する真相", "ルール", "フック", "本文",
    )
    with pytest.raises(RuntimeError, match="core_points"):
        fetch_umigame_item(cursor, 17)


def test_fetch_umigame_item_keeps_null_judge_fields() -> None:
    cursor = Mock()
    cursor.fetchone.return_value = (
        4, "001-problem", "問題文", "真相", ["事実"], None, None,
        None, "ルール", "フック", "本文",
    )
    item = fetch_umigame_item(cursor, 17)
    assert item is not None
    assert item.core_points is None
    assert item.judge_criteria is None
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
        "開示する真相", "ルール", "フック", "本文",
    )
    with pytest.raises(RuntimeError, match="judge_criteria"):
        fetch_umigame_item(cursor, 17)
