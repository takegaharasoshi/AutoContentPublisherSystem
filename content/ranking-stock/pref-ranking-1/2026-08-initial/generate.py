"""Generate the review sheet and SQL for the prefecture-ranking stock batch."""

from __future__ import annotations

import html
import json
from pathlib import Path
from typing import Any

import validate
from stock_items import ITEMS


BASE_DIR = Path(__file__).resolve().parent
REVIEW_PATH = BASE_DIR / "review.md"
REVIEW_HTML_PATH = BASE_DIR / "review.html"
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

## 前提: 表示文言フィールドの使われ方

5 つのフィールドは**出る場所がそれぞれ違う**。どこに出るかでレビューの重みが変わるため、
判断の前提として下表を確認すること（正は
[ranking-prebuilt.html](../../../../docs/app/generators/ranking-prebuilt.html) セクション 8.2 と
[pref-ranking-1.html](../../../../docs/app/sets/pref-ranking-1.html) セクション 5）。

| フィールド | 動画の版面 | キャプション | 補足 |
| --- | --- | --- | --- |
| `title` | タイトル帯（**1 行に収める制約**あり） | 【〜 TOP5】の見出し | ナレーション `intro` でも読み上げる |
| `hook` | 出ない | **1 行目** | フィード・リール面でプレビュー表示される唯一の行。ここで止まるか決まる |
| `trivia` | 出ない | 結果一覧の下の本文 | 「続きを読む」を開いた読者だけが読む |
| `subtitle` | **両尺の序盤に常設**（全国平均プレート。5 位の行が出るまで） | 出ない | 固定ラベルは付かないため、それ自体で完結した 1 行にする。ナレーションでは読まない |
| `bg_motif` | 出ない（間接） | 出ない | ビルド時に imagegen へ渡す背景イラストの指示文。視聴者は完成した絵しか見ない |
| `source_display` | **最下部の出典行帯に常設**（両尺・全編） | `※出典:` 行 | 画面とキャプションの両方に出る唯一のフィールド。単位の基準もここで示す |

版面の順位行（県名・数値）とキャプションの `result_list` は `data/*.json` から機械整形するため
手書きしない。レビュー対象は上表のテキストとナレーション台本。

ナレーション cue の構成（17-3 で見直し）: `intro` の直後に視聴者へ予想を促す **`teaser`（煽り）**
を全ネタ必須で置く。5〜2 位は呼び込みと県名を 1 本にまとめた `r5`〜`r2`（「まずは5位、埼玉県！」の形）、
1 位のみタメ（`r1_call`）と発表（`r1_name`）を分ける。締めは 20 秒版が `outro`
（「みんなはわかったかな？」= 全ネタ共通。`teaser` の答え合わせ）、30 秒版が **`closing`**
（結果総覧 3.0s + 締め 2.0s をまたぐ 1 本。県名の羅列ではなくネタの含意を口語で言い切る）。
モーラ数は暫定見積もりで、確定は 17-4 の VOICEVOX 実測による予算検査。
"""
    sections = [review_markdown_item(item, data) for item, data in items_and_data]
    return header + "\n" + "\n".join(sections)


def build_review_html(items_and_data: list[tuple[dict[str, Any], dict[str, Any]]]) -> str:
    """Build a self-contained HTML review sheet.

    Args:
        items_and_data: Source items paired with their data JSON.

    Returns:
        Complete UTF-8 HTML document for local browser review.
    """
    toc_items = []
    sections = []
    for item, data in items_and_data:
        entries = ranking_entries(data)
        first_name = validate.PREFECTURE_BY_CODE[entries[0]["pref_code"]].name
        item_id = f"item-{item['no']}"
        toc_items.append(
            f'<li><a href="#{html.escape(item_id, quote=True)}">'
            f"{html.escape(item['no'])} {html.escape(item['title'])}"
            f"（1位: {html.escape(first_name)}）</a></li>"
        )
        sections.append(review_html_item(item, data, item_id))

    return f"""<!doctype html>
<html lang="ja">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>都道府県ランキングストック 初期投入レビュー（第 1 バッチ 10 件）</title>
<style>
:root {{
  --page: #f6f4ef;
  --surface: #fffdf8;
  --text: #292824;
  --muted: #6b6861;
  --line: #d9d4ca;
  --accent: #315f58;
  --accent-soft: #e4efeb;
  --rank-one: #fff1c7;
  --near-limit: #fff3e4;
  --code: #f1eee7;
}}
@media (prefers-color-scheme: dark) {{
  :root {{
    --page: #1d201f;
    --surface: #272a28;
    --text: #eeeae1;
    --muted: #c1bbb0;
    --line: #4b504b;
    --accent: #9bcdbf;
    --accent-soft: #2e4840;
    --rank-one: #4b4123;
    --near-limit: #4c3928;
    --code: #353834;
  }}
}}
* {{ box-sizing: border-box; }}
body {{
  margin: 0;
  background: var(--page);
  color: var(--text);
  font-family: -apple-system, BlinkMacSystemFont, "Hiragino Kaku Gothic ProN",
    "Yu Gothic", sans-serif;
  line-height: 1.75;
}}
main {{ max-width: 960px; margin: 0 auto; padding: 2rem 1.25rem 4rem; }}
h1, h2, h3 {{ line-height: 1.35; }}
h1 {{ font-size: clamp(1.55rem, 4vw, 2.1rem); margin: 0 0 1rem; }}
h2 {{ margin: 0; font-size: 1.45rem; }}
h3 {{ font-size: 1.08rem; margin: 1.5rem 0 .65rem; }}
a {{ color: var(--accent); }}
.lead, .toc, section {{ background: var(--surface); border: 1px solid var(--line); border-radius: 10px; }}
.lead {{ padding: 1.1rem 1.25rem; margin-bottom: 1rem; }}
.lead ol {{ margin-bottom: 0; }}
.toc {{ padding: 1rem 1.25rem; margin: 1rem 0 1.5rem; }}
.toc h2 {{ font-size: 1.15rem; }}
.toc ol {{ columns: 2; gap: 2rem; padding-left: 1.4rem; margin-bottom: 0; }}
section {{ padding: 1.25rem; margin: 1.25rem 0; break-inside: avoid; }}
.section-head {{ display: flex; gap: .75rem; align-items: center; flex-wrap: wrap; }}
.content-key {{ color: var(--muted); font-size: .8rem; word-break: break-all; }}
.check {{ margin-left: auto; white-space: nowrap; }}
.back {{ font-size: .9rem; }}
table {{ width: 100%; border-collapse: collapse; margin: .6rem 0; }}
th, td {{ border-bottom: 1px solid var(--line); padding: .48rem .6rem; text-align: left; }}
.table-wrap {{ overflow-x: auto; }}
.field-usage {{ font-size: .92rem; }}
.field-usage code {{ white-space: nowrap; }}
th {{ color: var(--muted); font-weight: 600; }}
td:last-child, th:last-child {{ text-align: right; white-space: nowrap; }}
tr.rank-one {{ background: var(--rank-one); font-weight: 700; }}
.reference {{ color: var(--muted); font-size: .9rem; margin: .5rem 0 0; }}
.source, .fields {{ background: var(--code); border-radius: 7px; padding: .8rem 1rem; }}
dl {{ margin: 0; }}
dt {{ color: var(--muted); font-weight: 700; margin-top: .55rem; }}
dt:first-child {{ margin-top: 0; }}
dd {{ margin: 0; overflow-wrap: anywhere; }}
.narrations {{ display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 1rem; }}
.narration {{ border: 1px solid var(--line); border-radius: 7px; overflow: hidden; }}
.narration h3 {{ margin: 0; padding: .6rem .8rem; background: var(--accent-soft); }}
.cue {{ display: grid; grid-template-columns: 6.8rem 1fr auto; gap: .5rem; padding: .55rem .7rem; border-top: 1px solid var(--line); }}
.cue.near-limit {{ background: var(--near-limit); }}
.cue-name {{ font-family: ui-monospace, monospace; font-size: .82rem; color: var(--muted); }}
.cue-budget {{ font-size: .82rem; white-space: nowrap; color: var(--muted); }}
details {{ margin-top: 1.25rem; }}
summary {{ cursor: pointer; color: var(--accent); font-weight: 700; }}
pre {{ white-space: pre-wrap; overflow-wrap: anywhere; background: var(--code); padding: .9rem; border-radius: 7px; }}
@media (max-width: 700px) {{
  .toc ol {{ columns: 1; }}
  .narrations {{ grid-template-columns: 1fr; }}
  .cue {{ grid-template-columns: 5.8rem 1fr; }}
  .cue-budget {{ grid-column: 2; }}
}}
@media print {{
  body {{ background: #fff; color: #000; font-size: 10pt; }}
  main {{ max-width: none; padding: 0; }}
  .lead, .toc, section {{ border-color: #aaa; box-shadow: none; }}
  a {{ color: #000; text-decoration: none; }}
}}
</style>
</head>
<body>
<main>
<header class="lead">
<h1>都道府県ランキングストック 初期投入レビュー（第 1 バッチ 10 件）</h1>
<p>承認後に Claude がローカル MySQL と Aurora へ INSERT します。</p>
<h2>レビュー観点</h2>
<ol>
<li>データの正しさ（出典の実在・データ年・県換算の再計算・TOP5 の順位）</li>
<li>表現（下位を晒していないか・煽りすぎていないか・出典表記とキャプション注記の妥当性）</li>
<li>既存ストックとの重複（同一テーマ・同一出典の近接）</li>
<li>フォーマット適合（文字数・cue 台本の長さ・bg_motif の妥当性）</li>
</ol>
<h2>前提: 表示文言フィールドの使われ方</h2>
<p>5 つのフィールドは<strong>出る場所がそれぞれ違う</strong>。どこに出るかでレビューの重みが変わるため、
判断の前提として下表を確認すること（正は方式設計書 <code>ranking-prebuilt.html</code> セクション 8.2 と
セット別設計書 <code>pref-ranking-1.html</code> セクション 5）。</p>
<div class="table-wrap">
<table class="field-usage">
<thead><tr><th>フィールド</th><th>動画の版面</th><th>キャプション</th><th>補足</th></tr></thead>
<tbody>
<tr><td><code>title</code></td><td>タイトル帯（<strong>1 行に収める制約</strong>あり）</td><td>【〜 TOP5】の見出し</td><td>ナレーション <code>intro</code> でも読み上げる</td></tr>
<tr><td><code>hook</code></td><td>出ない</td><td><strong>1 行目</strong></td><td>フィード・リール面でプレビュー表示される唯一の行。ここで止まるか決まる</td></tr>
<tr><td><code>trivia</code></td><td>出ない</td><td>結果一覧の下の本文</td><td>「続きを読む」を開いた読者だけが読む</td></tr>
<tr><td><code>subtitle</code></td><td><strong>両尺の序盤に常設</strong>（全国平均プレート。5 位の行が出るまで）</td><td>出ない</td><td>固定ラベルは付かないため、それ自体で完結した 1 行にする。ナレーションでは読まない</td></tr>
<tr><td><code>bg_motif</code></td><td>出ない（間接）</td><td>出ない</td><td>ビルド時に imagegen へ渡す背景イラストの指示文。視聴者は完成した絵しか見ない</td></tr>
<tr><td><code>source_display</code></td><td><strong>最下部の出典行帯に常設</strong>（両尺・全編）</td><td><code>※出典:</code> 行</td><td>画面とキャプションの両方に出る唯一のフィールド。単位の基準もここで示す</td></tr>
</tbody>
</table>
</div>
<p>版面の順位行（県名・数値）とキャプションの <code>result_list</code> は <code>data/*.json</code> から
機械整形するため手書きしない。レビュー対象は上表のテキストとナレーション台本。</p>
<p>ナレーション cue の構成（17-3 で見直し）: <code>intro</code> の直後に視聴者へ予想を促す
<strong><code>teaser</code>（煽り）</strong>を全ネタ必須で置く。5〜2 位は呼び込みと県名を 1 本にまとめた
<code>r5</code>〜<code>r2</code>（「まずは5位、埼玉県！」の形）、1 位のみタメ（<code>r1_call</code>）と
発表（<code>r1_name</code>）を分ける。締めは 20 秒版が <code>outro</code>（「みんなはわかったかな？」=
全ネタ共通。<code>teaser</code> の答え合わせ）、30 秒版が <strong><code>closing</code></strong>
（結果総覧 3.0s + 締め 2.0s をまたぐ 1 本。県名の羅列ではなくネタの含意を口語で言い切る）。
モーラ数は暫定見積もりで、確定は 17-4 の VOICEVOX 実測による予算検査。</p>
</header>
<nav class="toc" id="toc" aria-label="目次">
<h2>目次</h2>
<ol>{''.join(toc_items)}</ol>
</nav>
{''.join(sections)}
</main>
</body>
</html>
"""


def review_html_item(item: dict[str, Any], data: dict[str, Any], item_id: str) -> str:
    """Render one item section for the self-contained HTML review sheet.

    Args:
        item: Single-source display and narration fields.
        data: Verified data fields for the item.
        item_id: HTML fragment identifier for the item section.

    Returns:
        Escaped HTML section for one stock item.
    """
    meta = data["meta"]
    entries = ranking_entries(data)
    sixth = data["full_ranking"][5]
    content_key = f"{item['no']}-{item['slug']}"
    ranking_rows = []
    for entry in entries:
        name = validate.PREFECTURE_BY_CODE[entry["pref_code"]].name
        row_class = ' class="rank-one"' if entry["rank"] == 1 else ""
        ranking_rows.append(
            f"<tr{row_class}><td>{entry['rank']}位</td><td>{html.escape(name)}</td>"
            f"<td>{html.escape(format_value(entry['value']))}"
            f"{html.escape(meta['suffix'])}</td></tr>"
        )
    fields = (
        ("hook", item["hook"]),
        ("trivia", item["trivia"]),
        ("subtitle", item["subtitle"]),
        ("bg_motif", item["bg_motif"]),
        ("source_display", item["source_display"]),
    )
    field_html = "".join(
        f"<dt>{html.escape(label)}</dt><dd>{html.escape(value)}</dd>"
        for label, value in fields
    )
    url = str(meta["url"])
    source_html = (
        f"<dt>出典名</dt><dd>{html.escape(str(meta['source_name']))}</dd>"
        f"<dt>データ年</dt><dd>{html.escape(str(meta['data_year_label']))}</dd>"
        f"<dt>取得日</dt><dd>{html.escape(str(meta['retrieved_on']))}</dd>"
        f"<dt>URL</dt><dd><a class=\"source-link\" href=\"{html.escape(url, quote=True)}\">"
        f"{html.escape(url)}</a></dd>"
        f"<dt>全国値</dt><dd>{html.escape(format_value(meta['nationwide']))}"
        f"{html.escape(str(meta['suffix']))}</dd>"
    )
    narrations = "".join(
        narration_html(
            duration,
            item["narration"][duration],
            keys,
            limits,
        )
        for duration, keys, limits in (
            ("20s", validate.NARRATION_KEYS_20S, validate.LIMITS_20S),
            ("30s", validate.NARRATION_KEYS_30S, validate.LIMITS_30S),
        )
    )
    return f"""
<section id="{html.escape(item_id, quote=True)}">
<div class="section-head">
<h2>{html.escape(item['no'])} {html.escape(item['title'])}</h2>
<span class="content-key">{html.escape(content_key)}</span>
<label class="check"><input type="checkbox"> 確認した</label>
<a class="back" href="#toc">目次へ戻る</a>
</div>
<h3>TOP5</h3>
<table>
<thead><tr><th>順位</th><th>都道府県</th><th>値</th></tr></thead>
<tbody>{''.join(ranking_rows)}</tbody>
</table>
<p class="reference">（参考）6位 {html.escape(str(sixth['pref_name']))} {html.escape(format_value(sixth['value']))}{html.escape(str(meta['suffix']))}</p>
<h3>出典</h3>
<div class="source"><dl>{source_html}</dl></div>
<h3>表示文言</h3>
<div class="fields"><dl>{field_html}</dl></div>
<h3>ナレーション</h3>
<div class="narrations">{narrations}</div>
<details>
<summary>source_note を表示</summary>
<pre>{html.escape(source_note(data))}</pre>
</details>
</section>
"""


def narration_html(
    duration: str,
    cues: dict[str, str],
    keys: tuple[str, ...],
    limits: dict[str, int],
) -> str:
    """Render one duration's narration cues.

    Args:
        duration: Video duration key.
        cues: Narration cue texts.
        keys: Cue order.
        limits: Mora limit by cue.

    Returns:
        Escaped HTML narration card.
    """
    rows = []
    for cue in keys:
        text = cues[cue]
        mora = validate.estimate_mora(text)
        limit = limits[cue]
        near_limit = " near-limit" if mora * 10 >= limit * 9 else ""
        rows.append(
            f'<div class="cue{near_limit}"><span class="cue-name">'
            f"{html.escape(cue)}</span><span>{html.escape(text)}</span>"
            f'<span class="cue-budget">{mora}/{limit}</span></div>'
        )
    label = "20 秒版" if duration == "20s" else "30 秒版"
    return f'<div class="narration"><h3>{label}</h3>{"".join(rows)}</div>'


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
        # value_prefix は「年間」の類の数値の前置き。不要なネタは null（17-4a 追加）
        "value_prefix": data["meta"].get("prefix"),
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
    """Validate the batch, then generate all derived files."""
    errors = validate.validate_items()
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1

    items_and_data = [(item, validate.load_data(item["data"])) for item in ITEMS]
    REVIEW_PATH.write_text(build_review(items_and_data), encoding="utf-8")
    REVIEW_HTML_PATH.write_text(build_review_html(items_and_data), encoding="utf-8")
    SQL_PATH.write_text(build_sql(items_and_data), encoding="utf-8")
    print(f"Generated: {REVIEW_PATH.name}, {REVIEW_HTML_PATH.name}, {SQL_PATH.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
