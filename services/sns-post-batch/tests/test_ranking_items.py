"""Tests for ranking item repository functions."""

import json
from unittest.mock import Mock

import pytest

from app.ranking_items import fetch_ranking_item


@pytest.mark.parametrize(
    "raw_fields",
    [
        json.dumps({"hook": "つかみ"}, ensure_ascii=False),
        json.dumps({"hook": "つかみ"}, ensure_ascii=False).encode("utf-8"),
        {"hook": "つかみ"},
    ],
)
def test_fetch_ranking_item_parses_content_fields(raw_fields: object) -> None:
    cursor = Mock()
    cursor.fetchone.return_value = ("ランキング題", raw_fields)

    item = fetch_ranking_item(cursor, 17)

    assert item is not None
    assert item.title == "ランキング題"
    assert item.content_fields == {"hook": "つかみ"}
    assert "WHERE generation_run_id = %s LIMIT 1" in cursor.execute.call_args.args[0]
    assert cursor.execute.call_args.args[1] == (17,)


def test_fetch_ranking_item_returns_none_without_row() -> None:
    cursor = Mock()
    cursor.fetchone.return_value = None
    assert fetch_ranking_item(cursor, 17) is None


@pytest.mark.parametrize(
    "raw_fields, message",
    [("{", "invalid JSON"), ("[]", "must be a JSON object")],
)
def test_fetch_ranking_item_rejects_invalid_content_fields(
    raw_fields: str,
    message: str,
) -> None:
    cursor = Mock()
    cursor.fetchone.return_value = ("ランキング題", raw_fields)
    with pytest.raises(RuntimeError, match=message):
        fetch_ranking_item(cursor, 17)
