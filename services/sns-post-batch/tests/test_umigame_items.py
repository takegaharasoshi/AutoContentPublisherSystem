"""Tests for umigame item retrieval and fact sheet decoding."""

import json
from unittest.mock import Mock

import pytest

from app.umigame_items import fetch_umigame_item


@pytest.mark.parametrize(
    "facts",
    [["事実"], json.dumps(["事実"], ensure_ascii=False),
     json.dumps(["事実"], ensure_ascii=False).encode("utf-8")],
)
def test_fetch_umigame_item_parses_fact_sheet(facts: object) -> None:
    cursor = Mock()
    cursor.fetchone.return_value = (
        4, "001-problem", "問題文", "真相", facts, "ルール", "フック", "本文",
    )
    item = fetch_umigame_item(cursor, 17)
    assert item is not None
    assert item.id == 4
    assert item.content_key == "001-problem"
    assert item.fact_sheet == ["事実"]
    assert item.caption == "本文"
    assert "FROM umigame_items" in cursor.execute.call_args.args[0]
    assert cursor.execute.call_args.args[1] == (17,)


def test_fetch_umigame_item_returns_none_without_row() -> None:
    cursor = Mock()
    cursor.fetchone.return_value = None
    assert fetch_umigame_item(cursor, 17) is None


@pytest.mark.parametrize("facts", ["broken", "{}", "[]", '[" "]', b"\xff"])
def test_fetch_umigame_item_rejects_invalid_fact_sheet(facts: object) -> None:
    cursor = Mock()
    cursor.fetchone.return_value = (
        4, "001-problem", "問題文", "真相", facts, "ルール", "フック", "本文",
    )
    with pytest.raises(RuntimeError, match="fact_sheet"):
        fetch_umigame_item(cursor, 17)
