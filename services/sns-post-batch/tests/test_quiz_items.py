"""Tests for quiz item repository functions."""

import json
from unittest.mock import Mock

from app.quiz_items import fetch_quiz_item


def test_fetch_quiz_item_parses_content_fields() -> None:
    cursor = Mock()
    cursor.fetchone.return_value = (
        "問題文",
        "答え",
        json.dumps({"hook": "つかみ"}, ensure_ascii=False),
    )
    item = fetch_quiz_item(cursor, 17)
    assert item is not None
    assert item.question_text == "問題文"
    assert item.answer_text == "答え"
    assert item.content_fields == {"hook": "つかみ"}
    assert "WHERE generation_run_id = %s LIMIT 1" in cursor.execute.call_args.args[0]
    assert cursor.execute.call_args.args[1] == (17,)


def test_fetch_quiz_item_returns_none_without_row() -> None:
    cursor = Mock()
    cursor.fetchone.return_value = None
    assert fetch_quiz_item(cursor, 17) is None
