"""Generate the review sheet and SQL for the prefecture-ranking stock batch."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import validate
from stock_items import ITEMS


BASE_DIR = Path(__file__).resolve().parent
REVIEW_PATH = BASE_DIR / "review.md"
SQL_PATH = BASE_DIR / "insert_ranking_stock.sql"


def format_value(value: int | float) -> str:
    """Format a ranking value with thousands separators.

    Args:
        value: JSON numeric ranking value.

    Returns:
        A comma-separated representation retaining a decimal part when present.
    """
    return format(value, ",")


def source_note(data: dict[str, Any]) -> str:
    """Build the source note stored in the database.

    Args:
        data: Parsed item data JSON.

    Returns:
        Source metadata followed by the source-note evidence text.
    """
    meta = data["meta"]
    return (
        f"出典: {meta['source_name']} / データ年: {meta['data_year_label']} / "
        f"取得日: {meta['retrieved_on']} / URL: {meta['url']}\n"
        f"{data['source_note_text']}"
    )


def ranking_entries(data: dict[str, Any]) -> list[dict[str, Any]]:
    """Return TOP5 entries ordered by rank.

    Args:
        data: Parsed item data JSON.

    Returns:
        The five ranking entries in ascending rank order.
    """
    return sorted(data["ranking_data"]["entries"], key=lambda entry: entry["rank"])


def canonical_ranking_data(data: dict[str, Any]) -> dict[str, Any]:
    """Build ranking_data with the database's required JSON key order.

    Args:
        data: Parsed item data JSON.

    Returns:
        Ranking JSON with rank, prefecture code, and value only.
    """
    return {
        "entries": [
            {
                "rank": entry["rank"],
                "pref_code": entry["pref_code"],
                "value": entry["value"],
            }
            for entry in ranking_entries(data)
        ]
    }


def result_list(data: dict[str, Any]) -> str:
    """Mechanically build the five-line display result list.

    Args:
        data: Parsed item data JSON.

    Returns:
        Lines in the ``1位 宮崎県 3,478円`` display format.
    """
    suffix = data["meta"]["suffix"]
    return "\n".join(
        "{rank}位 {name} {value}{suffix}".format(
            rank=entry["rank"],
            name=validate.PREFECTURE_BY_CODE[entry["pref_code"]].name,
            value=format_value(entry["value"]),
            suffix=suffix,
        )
        for entry in ranking_entries(data)
    )


def sql_literal(value: str) -> str:
    """Escape a string for a MySQL single-quoted literal.

    Args:
        value: Unicode text to place in a SQL literal.

    Returns:
        Safely escaped text without surrounding quotes.
    """
    return value.replace("\\", "\\\\").replace("'", "\\'")


def json_text(value: Any) -> str:
    """Serialize JSON in its one-line database representation."""
    return json.dumps(value, ensure_ascii=False, separators=(",", ":"))


def review_markdown_item(item: dict[str, Any], data: dict[str, Any]) -> str:
    """Render one item section of the human review sheet.

    Args:
        item: Single-source display and narration fields.
        data: Verified data fields for the item.

    Returns:
        Markdown section for one stock item.
    """
    meta = data["meta"]
    entries = ranking_entries(data)
    sixth = data["full_ranking"][5]
    content_key = f"{item['no']}-{item['slug']}"
    lines = [
        f"## {item['no']} {item['title']}（{content_key}）",
        "",
        f"- 出典: {meta['source_name']}",
        f"- データ年: {meta['data_year_label']}",
        f"- 取得日: {meta['retrieved_on']}",
        f"- URL: {meta['url']}",
        f"- 全国値: {meta['nationwide']}{meta['suffix']}",
        "",
        "| 順位 | 都道府県 | 値 |",
        "| --- | --- | ---: |",
    ]
    for entry in entries:
        name = validate.PREFECTURE_BY_CODE[entry["pref_code"]].name
        lines.append(
            f"| {entry['rank']}位 | {name} | "
            f"{format_value(entry['value'])}{meta['suffix']} |"
        )
    lines.append(
        f"| 6位 | {sixth['pref_name']} | "
        f"{format_value(sixth['value'])}{meta['suffix']} |"
    )
    lines.extend(
        [
            "",
            f"- hook: {item['hook']}",
            f"- trivia: {item['trivia']}",
            f"- subtitle: {item['subtitle']}",
            f"- bg_motif: {item['bg_motif']}",
            f"- source_display: {item['source_display']}",
            "",
            "### 20 秒版ナレーション",
            "",
        ]
    )
    lines.extend(
        f"- `{cue}`: {item['narration']['20s'][cue]}"
        for cue in validate.NARRATION_KEYS_20S
    )
    lines.extend(["", "### 30 秒版ナレーション", ""])
    lines.extend(
        f"- `{cue}`: {item['narration']['30s'][cue]}"
        for cue in validate.NARRATION_KEYS_30S
    )
    lines.extend(
        ["", "### Cue モーラ数", "", "| 尺 | cue | モーラ数/上限 |", "| --- | --- | ---: |"]
    )
    for duration, keys, limits in (
        ("20s", validate.NARRATION_KEYS_20S, validate.LIMITS_20S),
        ("30s", validate.NARRATION_KEYS_30S, validate.LIMITS_30S),
    ):
        for cue in keys:
            mora = validate.estimate_mora(item["narration"][duration][cue])
            lines.append(f"| {duration} | {cue} | {mora}/{limits[cue]} |")
    lines.extend(["", "### source_note", "", source_note(data), ""])
    return "\n".join(lines)


def build_review(items_and_data: list[tuple[dict[str, Any], dict[str, Any]]]) -> str:
    """Build the complete review Markdown document.

    Args:
        items_and_data: Source items paired with their data JSON.

    Returns:
        Complete review sheet text.
    """
    header = """# 都道府県ランキングストック 初期投入レビュー

レビュー観点:

1. データの正しさ（出典の実在・データ年・県換算の再計算・TOP5 の順位）
2. 表現（下位を晒していないか・煽りすぎていないか・出典表記とキャプション注記の妥当性）
3. 既存ストックとの重複（同一テーマ・同一出典の近接）
4. フォーマット適合（文字数・cue 台本の長さ・bg_motif の妥当性）

承認後に Claude がローカル MySQL と Aurora へ INSERT します。
"""
    sections = [review_markdown_item(item, data) for item, data in items_and_data]
    return header + "\n" + "\n".join(sections)


def sql_item(item: dict[str, Any], data: dict[str, Any]) -> str:
    """Build one INSERT statement.

    Args:
        item: Single-source display and narration fields.
        data: Verified data fields for the item.

    Returns:
        SQL comment and INSERT statement for the item.
    """
    fields = {
        "hook": item["hook"],
        "trivia": item["trivia"],
        "source_display": item["source_display"],
        "result_list": result_list(data),
        "value_suffix": data["meta"]["suffix"],
        "subtitle": item["subtitle"],
        "bg_motif": item["bg_motif"],
    }
    values = {
        "content_key": f"{item['no']}-{item['slug']}",
        "format": item["format"],
        "title": item["title"],
        "content_fields": json_text(fields),
        "ranking_data": json_text(canonical_ranking_data(data)),
        "narration": json_text(item["narration"]),
        "source_note": source_note(data),
    }
    return """-- {no}
INSERT INTO ranking_stock_items
    (set_id, content_key, format, title, content_fields, ranking_data, narration, source_note, is_active)
VALUES
    ((SELECT id FROM batch_sets WHERE set_code = 'pref-ranking-1'), '{content_key}', '{format}', '{title}',
     '{content_fields}', '{ranking_data}', '{narration}', '{source_note}', 1);
""".format(no=item["no"], **{key: sql_literal(value) for key, value in values.items()})


def build_sql(items_and_data: list[tuple[dict[str, Any], dict[str, Any]]]) -> str:
    """Build the complete SQL import script.

    Args:
        items_and_data: Source items paired with their data JSON.

    Returns:
        Complete SQL text.
    """
    header = """-- 都道府県ランキングストック初期投入（10 件。レビュー承認後に実行）
-- 生成元: content/ranking-stock/pref-ranking-1/2026-08-initial/stock_items.py（単一ソース）
-- 適用先: ローカル MySQL / Aurora(acps)
-- set_id は set_code から解決するため両環境共通で実行できる。
-- content_key はセット内一意のため、二重投入はユニークキー違反で落ちる（安全側）。

"""
    return header + "\n".join(sql_item(item, data) for item, data in items_and_data)


def main() -> int:
    """Validate the batch, then generate both derived files."""
    errors = validate.validate_items()
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1

    items_and_data = [(item, validate.load_data(item["data"])) for item in ITEMS]
    REVIEW_PATH.write_text(build_review(items_and_data), encoding="utf-8")
    SQL_PATH.write_text(build_sql(items_and_data), encoding="utf-8")
    print(f"Generated: {REVIEW_PATH.name}, {SQL_PATH.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
