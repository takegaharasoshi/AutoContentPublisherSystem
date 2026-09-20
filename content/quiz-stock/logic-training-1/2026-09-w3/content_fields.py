# 2026-09-w3 補充: stock_items の 1 問を quiz_stock_items.content_fields(JSON)の dict に変換する共通ヘルパー
#
# generate.py(投入 SQL の生成)と validate.py(実行時同等検証。課題体系 I-033 の同梱)が同じ関数を使うことで、
# 「検証した JSON」と「投入する JSON」が必ず一致する。
from __future__ import annotations

from typing import Any

# 版面・キャプションに出るフィールド。DDL の content_fields(JSON)に入れる 9 項目。
# source_note は quiz_stock_items.source_note カラムへ別途入れるため含めない。
CONTENT_FIELD_NAMES = (
    "hook",
    "hint",
    "question",
    "answer",
    "explanation",
    "coach_comment",
    "tags",
    "summary",
    "illustration_scene",
)


def content_fields_of(item: dict[str, Any]) -> dict[str, Any]:
    """stock_items の 1 問から content_fields の dict を作る。

    Args:
        item: stock_items.ITEMS の要素。

    Returns:
        content_fields カラムに入れる dict(キー順は CONTENT_FIELD_NAMES)。
    """
    return {name: item[name] for name in CONTENT_FIELD_NAMES}
