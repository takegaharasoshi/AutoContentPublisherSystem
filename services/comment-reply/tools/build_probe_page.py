"""Build a standalone, locally browsable HTML report from probe results."""

from __future__ import annotations

import argparse
import html
import json
import re
import sys
from pathlib import Path
from typing import Any, Callable


SERVICE_DIR = Path(__file__).resolve().parent.parent
REPO_ROOT = SERVICE_DIR.parents[1]
if str(SERVICE_DIR) not in sys.path:
    sys.path.insert(0, str(SERVICE_DIR))

from app.judge.contract import KINDS  # noqa: E402
from tools.probe_metrics import aggregate, row_flags  # noqa: E402


DEFAULT_OUT = REPO_ROOT / "docs/app/sets/umigame-soup-1-probe.html"
KIND_NAMES = (
    "① はい / いいえ質問", "② 複数の質問", "③ 答えられない質問",
    "④ 正解推理", "⑤ 惜しい推理", "⑥ 外れた推理", "⑦ ヒント要求",
    "⑧ ネタバレ要求", "⑨ 遊び方の質問", "⑩ 感想", "⑪ 挨拶",
    "⑫ 応援", "⑬ 雑談", "⑭ リクエスト", "⑮ 指摘・クレーム",
    "⑯ メンション", "⑰ 絵文字だけ", "⑱ 荒らし", "⑲ 誹謗中傷",
    "⑳ 宣伝・スパム", "㉑ 個人情報", "㉒ 外国語",
)
KIND_LABEL = dict(zip(KINDS, KIND_NAMES))
SECTIONS = (
    ("前提条件 P1〜P7", (
        ("P1", "P1 漏れ候補"), ("P2", "P2 誤った正解宣言"),
        ("P3", "P3 はい / いいえの取り違え"), ("P4", "P4 判定の揺れ"),
        ("P5", "P5 正解宣言率"), ("P6", "P6 不適切系の応答"),
        ("P7", "P7 80 字超"))),
    ("レベル 1", (
        ("L1_kind", "L1① 種別一致率"), ("L1_phrasing", "L1② 言い回しの偏り"),
        ("L1_guidance", "L1③ 誘導率"))),
    ("レベル 2", (
        ("L2_one_liner", "L2 一言の長さ"), ("L2_opener", "L2 判定語の冒頭"),
        ("L2_conflict", "L2 判定語の食い違い"),
        ("L2_proximity", "L2 近さの語"), ("L2_emoji", "L2 絵文字"))),
)
METRIC_NAMES = {key: name for _, entries in SECTIONS for key, name in entries}


def _h(value: Any) -> str:
    return html.escape(str(value), quote=True)


def _kind(kind: str | None) -> str:
    return KIND_LABEL.get(kind, str(kind) if kind else "—")


def _badge(passed: bool | None) -> str:
    if passed is None:
        return '<span class="badge badge-future">対象なし</span>'
    if passed:
        return '<span class="badge badge-fixed">合格</span>'
    return '<span class="badge badge-wip">不合格</span>'


def _percent(rate: float | None) -> str:
    return f"{rate:.1%}" if rate is not None else "対象なし"


def _row_anchor(pattern_id: str, case_id: str) -> str:
    return f"r-{pattern_id}-{case_id}"


def _ng_details(pattern_id: str, item: dict[str, Any],
                page_of: Callable[[str, str], str] = lambda pid, cid: "") -> str:
    """合否表のセルに置く NG の ID 一覧（折りたたみ）。ID は問題ごとのページの該当行へのリンク。"""
    entries = item.get("ng") or []
    if not entries:
        return ""
    links = "".join(
        f'<li><a class="ng-link" href="{_h(page_of(pattern_id, e["id"]))}#{_h(_row_anchor(pattern_id, e["id"]))}">{_h(e["id"])}</a>'
        + (f' <span class="ng-note">{_h(e["note"])}</span>' if e.get("note") else "") + "</li>"
        for e in entries)
    return (f'<details class="ng-ids"><summary>NG {len(entries)} 件</summary>'
            f"<ul>{links}</ul></details>")


def _summary_table(metrics: dict[str, Any], patterns: list[dict[str, Any]],
                   page_of: Callable[[str, str], str] = lambda pid, cid: "") -> str:
    cells = ['<div class="ng-toolbar"><button type="button" class="ng-all" data-open="1">'
             'NG の ID をすべて開く</button><button type="button" class="ng-all" data-open="0">'
             'すべて閉じる</button></div>',
             '<div class="table-wrap"><table class="summary-table"><thead><tr><th>指標</th>']
    cells.extend(f"<th>{_h(p['label'])}</th>" for p in patterns)
    cells.append("<th>合格ライン</th></tr></thead><tbody>")
    for heading, entries in SECTIONS:
        cells.append(f'<tr class="group"><th colspan="{len(patterns) + 2}">{_h(heading)}</th></tr>')
        for key, name in entries:
            has_ng = any(metrics["patterns"][p["id"]]["metrics"][key].get("ng") for p in patterns)
            toggle = ('<button type="button" class="ng-row" aria-label="この行の NG を開く / 閉じる">'
                      '行を開く</button>' if has_ng else "")
            cells.append(f"<tr><th>{_h(name)}{toggle}</th>")
            for pattern in patterns:
                item = metrics["patterns"][pattern["id"]]["metrics"][key]
                cells.append(f"<td>{_h(item['value'])} {_badge(item['pass'])}"
                             f"{_ng_details(pattern['id'], item, page_of)}</td>")
            threshold = metrics["patterns"][patterns[0]["id"]]["metrics"][key]["threshold"]
            cells.append(f"<td>{_h(threshold)}</td></tr>")
    count = sum(len(entries) for _, entries in SECTIONS)
    cells.append("<tr><th>合格した指標の数</th>")
    for pattern in patterns:
        values = metrics["patterns"][pattern["id"]]["metrics"].values()
        cells.append(f"<td>{sum(v['pass'] is True for v in values)} / {count}</td>")
    cells.append("<td>参考: 対象なしは数えない</td></tr></tbody></table></div>")
    return "".join(cells)


# グラフはスマホ幅（360px）で 1:1 になる viewBox にし、PC では CSS の max-width で止める
CHART_W, LABEL_W, BAR_X, BAR_W = 360, 112, 116, 184


def _pattern_rate(report: dict[str, Any], key: str) -> tuple[float | None, str]:
    if key == "yesno":
        old = report["reference"]["yesno_accuracy"]["existing"]
        new = report["reference"]["yesno_accuracy"]["new"]
        count, total = old["count"] + new["count"], old["total"] + new["total"]
    else:
        item = report["metrics"][key]
        count, total = item["count"], item["total"]
        if item["rate"] is None:
            return None, "対象なし"
    rate = count / total if total else None
    return rate, (f"{rate:.0%}（{count}/{total}）" if rate is not None else "対象なし")


def _rate_svg(metrics: dict[str, Any], patterns: list[dict[str, Any]]) -> str:
    series = (("L1_kind", "L1① 種別一致率", .9), ("yesno", "① 判定一致率（参考）", None),
              ("P5", "P5 正解宣言率", .8), ("L1_guidance", "L1③ 誘導率", .8))
    block = 24 + len(patterns) * 18
    height = len(series) * block + 8
    out = [f'<svg class="probe-svg" viewBox="0 0 {CHART_W} {height}" role="img" '
           'aria-label="指標ごとのパターン別の率の横棒グラフ">']
    for i, (key, label, target) in enumerate(series):
        y0 = i * block + 4
        head = label + (f"（基準 {target:.0%}）" if target is not None else "")
        out.append(f'<text x="0" y="{y0 + 12}" class="chart-pattern">{_h(head)}</text>')
        for j, pattern in enumerate(patterns):
            y = y0 + 20 + j * 18
            rate, text = _pattern_rate(metrics["patterns"][pattern["id"]], key)
            out.append(f'<g><title>{_h(label)} / {_h(pattern["label"])}: {_h(text)}</title>'
                       f'<text x="0" y="{y + 10}" class="chart-label">{_h(pattern["label"])}</text>'
                       f'<rect x="{BAR_X}" y="{y}" width="{BAR_W}" height="12" rx="3" class="chart-bg"/>')
            if rate is not None:
                out.append(f'<rect x="{BAR_X}" y="{y}" width="{max(BAR_W * rate, 2):.1f}" '
                           'height="12" rx="3" class="chart-rate"/>')
            out.append(f'<text x="{BAR_X + BAR_W + 4}" y="{y + 10}" class="chart-label">'
                       f'{_h(text.split("（")[0])}</text></g>')
        if target is not None:
            x = BAR_X + BAR_W * target
            out.append(f'<line x1="{x:.1f}" y1="{y0 + 17}" x2="{x:.1f}" '
                       f'y2="{y0 + 20 + len(patterns) * 18 - 4}" class="chart-target"/>')
    out.append("</svg>")
    return "".join(out)


def _time_svg(metrics: dict[str, Any], patterns: list[dict[str, Any]]) -> str:
    fields = (("中央値", "median"), ("p95", "p95"))
    values = [(metrics["patterns"][p["id"]]["reference"]["timing"], f) for p in patterns
              for _, f in fields]
    max_s = max(((t["judge_s"][f] or 0) + (t["writer_s"][f] or 0) for t, f in values), default=0)
    scale = BAR_W / max_s if max_s else 0
    block = 18 + len(fields) * 16
    height = 24 + len(patterns) * block
    out = [f'<svg class="probe-svg" viewBox="0 0 {CHART_W} {height}" role="img" '
           'aria-label="パターンごとの判定と書き手の所要時間（中央値と p95）">',
           '<rect x="0" y="4" width="12" height="12" rx="3" class="chart-judge"/>'
           '<text x="16" y="14" class="chart-label">判定</text>'
           '<rect x="52" y="4" width="12" height="12" rx="3" class="chart-writer"/>'
           '<text x="68" y="14" class="chart-label">書き手（右端の数字は合計）</text>']
    for i, pattern in enumerate(patterns):
        timing = metrics["patterns"][pattern["id"]]["reference"]["timing"]
        y0 = 24 + i * block
        out.append(f'<text x="0" y="{y0 + 12}" class="chart-pattern">{_h(pattern["label"])}</text>')
        for j, (label, field) in enumerate(fields):
            y = y0 + 16 + j * 16
            judge = timing["judge_s"][field] or 0
            writer = timing["writer_s"][field] or 0
            total = timing["total_s"][field]
            total_text = f"{total:.1f} 秒" if total is not None else "対象なし"
            out.append(f'<g><title>{_h(pattern["label"])} {label}: 判定 {judge:.2f} 秒 / '
                       f'書き手 {writer:.2f} 秒 / 合計 {total_text}</title>'
                       f'<text x="12" y="{y + 10}" class="chart-label">{label}</text>'
                       f'<rect x="{BAR_X}" y="{y}" width="{judge * scale:.1f}" height="12" '
                       'class="chart-judge"/>'
                       f'<rect x="{BAR_X + judge * scale:.1f}" y="{y}" width="{writer * scale:.1f}" '
                       'height="12" class="chart-writer"/>'
                       f'<text x="{BAR_X + BAR_W + 4}" y="{y + 10}" class="chart-label">'
                       f'{_h(total_text)}</text></g>')
    out.append("</svg>")
    return "".join(out)


def _metric_detail(key: str, item: dict[str, Any]) -> str:
    """不合格の指標の内訳（どの種別・何件で落ちたか）を短く書く。"""
    if key == "L1_kind":
        low = [f"{_kind(k)} {v['count']}/{v['total']}" for k, v in item["by_kind"].items()
               if v["total"] and v["rate"] is not None and v["rate"] < .8 and k not in
               {"q_yesno", "q_multi", "q_open"}]
        return "80% 未満: " + "・".join(low) if low else f"全体 {item['value']}"
    if key == "L1_phrasing":
        return "50% 超: " + "・".join(f"{_kind(k)} {v['count']}/{v['total']}"
                                       for k, v in item["by_kind"].items() if v["rate"] > .5)
    if key in {"L2_one_liner", "L2_opener"}:
        return f"{item['total'] - item['count']} 件"
    if key in {"P1", "P2", "P7", "L2_conflict", "L2_proximity", "L2_emoji"}:
        return f"{item['count']} 件"
    return str(item["value"])


def _level_cell(items: dict[str, Any], keys: tuple[str, ...]) -> str:
    failed = [key for key in keys if items[key]["pass"] is False]
    if not failed:
        unknown = all(items[key]["pass"] is None for key in keys)
        return _badge(None if unknown else True)
    rows = "".join(f"<li><strong>{_h(METRIC_NAMES[key])}</strong> "
                   f"{_h(_metric_detail(key, items[key]))}</li>" for key in failed)
    return f'{_badge(False)}<ul class="eval-fails">{rows}</ul>'


def _evaluation(metrics: dict[str, Any], patterns: list[dict[str, Any]]) -> str:
    """パターンごとの評価を、レベル別の合否と人が確認するものの表にする。"""
    levels = [(heading, tuple(key for key, _ in entries)) for heading, entries in SECTIONS]
    total = sum(len(keys) for _, keys in levels)
    out = ['<div class="table-wrap"><table class="eval-table"><thead><tr><th>パターン</th>'
           '<th>合格した指標</th>']
    out.extend(f"<th>{_h(heading)}</th>" for heading, _ in levels)
    out.append("<th>処理時間（中央値）</th><th>人が確認するもの</th></tr></thead><tbody>")
    premise_ok, all_ok = [], []
    for pattern in patterns:
        report = metrics["patterns"][pattern["id"]]
        items, ref = report["metrics"], report["reference"]
        passed = sum(v["pass"] is True for v in items.values())
        if all(items[key]["pass"] is not False for key in levels[0][1]):
            premise_ok.append(pattern["label"])
        if all(v["pass"] is not False for v in items.values()):
            all_ok.append(pattern["label"])
        median = ref["timing"]["total_s"]["median"]
        checks = [f"P1 漏れ候補 {items['P1']['count']} 件（全件を人が見る）"]
        if pattern["judge_mode"] == "hybrid":
            checks.append(f"見張り役の食い違い {ref['watch_mismatch']['count']} 件・"
                          f"合意制で割れた {ref['consensus_split']['count']} 件")
        if ref["fallback"]["count"]:
            checks.append(f"書き手の定型フォールバック {ref['fallback']['count']} 件")
        if ref["errors"]["count"]:
            checks.append(f"エラーを含む記録 {ref['errors']['count']} 件")
        out.append(f'<tr><th>{_h(pattern["label"])}</th><td class="eval-score">{passed} / {total}</td>')
        out.extend(f"<td>{_level_cell(items, keys)}</td>" for _, keys in levels)
        out.append(f"<td>{f'{median:.1f} 秒' if median is not None else '—'}</td>"
                   f'<td><ul class="eval-checks">{"".join(f"<li>{_h(c)}</li>" for c in checks)}'
                   "</ul></td></tr>")
    out.append("</tbody></table></div>")
    fastest = min(patterns, key=lambda p: metrics["patterns"][p["id"]]["reference"]["timing"]
                  ["total_s"]["median"] or float("inf"))
    out.append('<div class="note"><span class="callout-title">まとめ（自動集計）</span><ul>'
               f"<li>全指標を満たしたパターン: {_h('、'.join(all_ok) or 'なし')}</li>"
               f"<li>前提条件 P1〜P7 を満たしたパターン: {_h('、'.join(premise_ok) or 'なし')}</li>"
               f"<li>処理時間の中央値が最短: {_h(fastest['label'])}</li>"
               "<li>不合格の行は、合否表の「NG n 件」を開くとコメント ID から一覧表の行へ飛べる</li>"
               "</ul></div>")
    return "".join(out)


def _reference_table(metrics: dict[str, Any], patterns: list[dict[str, Any]]) -> str:
    rows = (("yesno_accuracy", "existing", "① 判定一致率（従来の質問）"),
            ("yesno_accuracy", "new", "① 判定一致率（新しい質問）"),
            ("bare_term", None, "語だけの聞き返し"),
            ("errors", None, "エラーを含む記録"),
            ("fallback", None, "書き手の定型フォールバック"))
    out = ['<div class="table-wrap"><table class="reference-table"><thead><tr><th>参考値</th>']
    out.extend(f"<th>{_h(p['label'])}</th>" for p in patterns)
    out.append("</tr></thead><tbody>")
    for key, sub, label in rows:
        out.append(f"<tr><th>{_h(label)}</th>")
        for pattern in patterns:
            ref = metrics["patterns"][pattern["id"]]["reference"]
            item = ref[key][sub] if sub else ref[key]
            out.append(f"<td>{_h(item['value'])}</td>")
        out.append("</tr>")
    out.append("</tbody></table></div>")
    return "".join(out)


def _options(cases: list[dict[str, Any]], rows: list[dict[str, Any]],
             field: str) -> str:
    if field == "expected":
        kinds = {case["expected_kind"] for case in cases}
    else:
        kinds = {(row["record"].get("final") or {}).get("kind") for row in rows}
    return "".join(f'<option value="{_h(kind)}">{_h(_kind(kind))}</option>'
                   for kind in KINDS if kind in kinds)


def _case_table(pattern: dict[str, Any], no: str, cases: list[dict[str, Any]],
                rows: list[dict[str, Any]], raw_file: str, raw_heading: str = "h5") -> str:
    out = ['<div class="probe-filters">',
           '<label>全文検索 <input class="filter-text" type="search" placeholder="コメント・返信"></label>',
           '<label>想定種別 <select class="filter-expected"><option value="">すべて</option>',
           _options(cases, rows, "expected"), '</select></label>',
           '<label>最終種別 <select class="filter-final"><option value="">すべて</option>',
           _options(cases, rows, "final"), '</select></label>',
           '<label><input class="filter-diff" type="checkbox"> 相違ありだけ</label>',
           f'<span class="filter-count">{len(rows)} 件中 {len(rows)} 件を表示</span></div>',
           '<div class="table-wrap"><table class="case-table"><thead><tr>',
           '<th data-type="text">ID</th><th data-type="text">コメント</th>',
           '<th data-type="text">想定判定</th><th data-type="text">判定内容</th>',
           '<th data-type="text">相違</th><th data-type="text">返信内容</th>',
           '<th data-type="number">処理時間</th></tr></thead><tbody>']
    indexed = {case["id"]: case for case in cases}
    for row in rows:
        case = indexed[row["case_id"]]
        record = row["record"]
        final = record.get("final") or {}
        reply = (record.get("reply") or {}).get("text")
        flags = row_flags(row, case)
        mismatch = "✕" if flags["label_mismatch"] else ""
        if flags["watch_mismatch"] and pattern["judge_mode"] == "hybrid":
            mismatch += " 見張り" if mismatch else "見張り"
        expected = _kind(case["expected_kind"])
        if case.get("expected_answer"):
            expected += " / " + case["expected_answer"]
        actual = _kind(final.get("kind"))
        if final.get("answer"):
            actual += " / " + final["answer"]
        actual += " / " + (final.get("decision") or "—")
        duration = row["timing"].get("total_s")
        seconds = f"{duration:.2f}" if duration is not None else "—"
        parts = row["timing"]
        title = f"判定 {parts.get('judge_s') or 0:.2f} 秒 / 書き手 {parts.get('writer_s') or 0:.2f} 秒"
        search = case["text"] + " " + (reply or "") + " " + case["id"]
        out.append(f'<tr id="{_h(_row_anchor(pattern["id"], case["id"]))}" data-search="{_h(search)}" data-expected="{_h(case["expected_kind"])}" '
                   f'data-final="{_h(final.get("kind") or "")}" '
                   f'data-diff="{1 if flags["label_mismatch"] or flags["watch_mismatch"] else 0}">')
        values = (
            (case["id"], case["id"]), (case["text"], case["text"]),
            (expected, expected), (actual, actual), (mismatch, mismatch),
            (reply if reply is not None else "返信なし", reply or ""),
            (seconds + " 秒", duration or 0),
        )
        for i, (display, sort) in enumerate(values):
            extra = f' title="{_h(title)}"' if i == 6 else ""
            out.append(f'<td data-sort="{_h(sort)}"{extra}>{_h(display)}</td>')
        out.append("</tr>")
    out.append("</tbody></table></div>")
    raw_key = f"{pattern['id']}/{no}"
    out.append(f'<{raw_heading}>テスト結果生データ</{raw_heading}>')
    out.append(f'<details class="raw-details" data-raw-key="{_h(raw_key)}" '
               f'data-raw-src="{_h(raw_file)}"><summary>コメント記録 JSON を表示</summary>'
               '<pre>開くと読み込みます。</pre></details>')
    return "".join(out)


STYLE = """
body { overflow-wrap: anywhere; }
.container { min-width: 0; }
.summary-table { min-width: 960px; }
.case-table { min-width: 820px; }
.summary-table td { min-width: 125px; }
.summary-table tbody th { min-width: 10.5rem; }
.eval-table tbody th { min-width: 8rem; }
.group th { background: var(--note-bg); }
.ng-toolbar { display: flex; flex-wrap: wrap; gap: .5rem; margin: .5rem 0; }
.ng-toolbar button, .ng-row { font: inherit; font-size: .8rem; padding: .15rem .55rem; cursor: pointer;
  border: 1px solid var(--border); border-radius: 4px; background: var(--bg-subtle); color: var(--text); }
.ng-row { display: block; margin-top: .3rem; font-weight: 400; white-space: nowrap; }
.ng-ids { margin-top: .3rem; font-size: .8rem; }
.ng-ids summary { cursor: pointer; color: var(--link); }
.ng-ids ul { margin: .25rem 0 0; padding-left: 1.1rem; }
.ng-note { color: var(--text-muted, inherit); opacity: .8; }
.eval-table { min-width: 820px; }
.eval-table td, .eval-table th { vertical-align: top; }
.eval-score { white-space: nowrap; font-weight: 700; }
.eval-fails, .eval-checks { margin: .3rem 0 0; padding-left: 1.1rem; font-size: .85rem; }
.case-table tr:target td { background: var(--warn-bg); }
.problem-index { min-width: 640px; }
.problem-index tbody th { min-width: 12rem; }
.problem-lead { display: block; font-weight: 400; font-size: .8rem; }
.problem-nav { margin: .5rem 0 1rem; }
.probe-svg { display: block; width: 100%; height: auto; max-width: 560px; }
.chart-bg { fill: var(--bg-subtle); }
.chart-rate, .chart-judge { fill: var(--link); }
.chart-writer { fill: var(--warn-border); }
.chart-target { stroke: var(--warn-border); stroke-width: 1.5; stroke-dasharray: 3 2; }
.chart-label, .chart-pattern { fill: var(--text); font-size: 11px; }
.chart-pattern { font-weight: 700; }
.probe-filters { display: flex; flex-wrap: wrap; gap: .5rem 1rem; align-items: center; margin: 1rem 0 .25rem; }
.probe-filters label, .filter-count { font-size: .85rem; }
.probe-filters input, .probe-filters select { max-width: 100%; }
.case-table th { cursor: pointer; }
.case-table td:nth-child(2), .case-table td:nth-child(6) { min-width: 13rem; white-space: pre-wrap; }
.case-table td:nth-child(1) { white-space: nowrap; }
.raw-details pre { max-height: 60vh; overflow: auto; white-space: pre-wrap; }
@media (max-width: 600px) { .container { padding: 1rem .85rem 3rem; } }
"""

SCRIPT = r"""
(function () {
  document.querySelectorAll('.case-table').forEach(function (table) {
    var container = table.closest('section');
    var controls = container.querySelector('.probe-filters');
    var body = table.tBodies[0];
    var rows = Array.from(body.rows);
    var count = controls.querySelector('.filter-count');
    function filter() {
      var query = controls.querySelector('.filter-text').value.toLocaleLowerCase();
      var expected = controls.querySelector('.filter-expected').value;
      var finalKind = controls.querySelector('.filter-final').value;
      var diff = controls.querySelector('.filter-diff').checked;
      var shown = 0;
      rows.forEach(function (row) {
        var visible = (!query || row.dataset.search.toLocaleLowerCase().includes(query)) &&
          (!expected || row.dataset.expected === expected) &&
          (!finalKind || row.dataset.final === finalKind) &&
          (!diff || row.dataset.diff === '1');
        row.hidden = !visible;
        if (visible) shown += 1;
      });
      count.textContent = rows.length + ' 件中 ' + shown + ' 件を表示';
    }
    controls.querySelectorAll('input,select').forEach(function (input) {
      input.addEventListener('input', filter);
      input.addEventListener('change', filter);
    });
    table.querySelectorAll('thead th').forEach(function (th, column) {
      th.tabIndex = 0;
      function sort() {
        var descending = th.dataset.direction === 'asc';
        th.dataset.direction = descending ? 'desc' : 'asc';
        rows.sort(function (a, b) {
          var av = a.cells[column].dataset.sort;
          var bv = b.cells[column].dataset.sort;
          var result = th.dataset.type === 'number' ? Number(av) - Number(bv) :
            av.localeCompare(bv, 'ja');
          return descending ? -result : result;
        });
        rows.forEach(function (row) { body.appendChild(row); });
      }
      th.addEventListener('click', sort);
      th.addEventListener('keydown', function (event) {
        if (event.key === 'Enter' || event.key === ' ') { event.preventDefault(); sort(); }
      });
    });
  });
  document.querySelectorAll('.ng-all').forEach(function (button) {
    button.addEventListener('click', function () {
      var open = button.dataset.open === '1';
      document.querySelectorAll('.summary-table .ng-ids').forEach(function (d) { d.open = open; });
    });
  });
  document.querySelectorAll('.ng-row').forEach(function (button) {
    button.addEventListener('click', function () {
      var details = button.closest('tr').querySelectorAll('.ng-ids');
      var open = !Array.from(details).every(function (d) { return d.open; });
      details.forEach(function (d) { d.open = open; });
      button.textContent = open ? '行を閉じる' : '行を開く';
    });
  });
  document.querySelectorAll('.ng-link').forEach(function (link) {
    link.addEventListener('click', function () {
      var row = document.getElementById(link.getAttribute('href').split('#')[1]);
      if (!row || !row.hidden) return;
      var controls = row.closest('section').querySelector('.probe-filters');
      controls.querySelectorAll('input[type=search],select').forEach(function (i) { i.value = ''; });
      controls.querySelector('.filter-diff').checked = false;
      controls.querySelector('.filter-text').dispatchEvent(new Event('input'));
    });
  });
  document.querySelectorAll('.raw-details').forEach(function (detail) {
    detail.addEventListener('toggle', function () {
      if (!detail.open || detail.dataset.loaded) return;
      detail.dataset.loaded = '1';
      var script = document.createElement('script');
      script.src = detail.dataset.rawSrc;
      script.onload = function () {
        detail.querySelector('pre').textContent = JSON.stringify(
          window.PROBE_RAW[detail.dataset.rawKey], null, 2);
      };
      script.onerror = function () { detail.querySelector('pre').textContent = '読み込みに失敗しました。'; };
      document.body.appendChild(script);
    });
  });
})();
"""


def _head(title: str, assets: str) -> list[str]:
    return ['<!DOCTYPE html><html lang="ja"><head><meta charset="UTF-8">',
            '<meta name="viewport" content="width=device-width, initial-scale=1.0">',
            f'<title>{_h(title)} | AutoContentPublisherSystem</title>',
            f'<link rel="stylesheet" href="{assets}assets/style.css">',
            '<style>', STYLE, '</style></head><body><div class="container">']


def _tail() -> list[str]:
    return ['<script>', SCRIPT, '</script></div></body></html>\n']


def _problem_index(results: dict[str, Any], metrics: dict[str, Any],
                   patterns: list[dict[str, Any]], nos: list[str], page_dir: str) -> str:
    """サマリーから問題ごとのページへの目次（パターンごとの相違件数つき）。"""
    indexed = {case["id"]: case for case in results["cases"]}
    out = ['<div class="table-wrap"><table class="problem-index"><thead><tr><th>問題</th>'
           '<th>件数</th>']
    out.extend(f"<th>{_h(p['label'])}<br>相違</th>" for p in patterns)
    out.append("</tr></thead><tbody>")
    for no in nos:
        counts = results["meta"]["case_counts"][no]
        text = results["problems"][no]["problem_text"]
        heading = text[:40] + ("…" if len(text) > 40 else "")
        total = sum(counts.values())
        out.append(f'<tr><th><a href="{_h(page_dir)}/{_h(no)}.html">{_h(no)}</a>'
                   f'<span class="problem-lead">{_h(heading)}</span></th><td>{total}</td>')
        for pattern in patterns:
            diff = 0
            for row in results["rows"][pattern["id"]]:
                if row["no"] != no:
                    continue
                flags = row_flags(row, indexed[row["case_id"]])
                diff += bool(flags["label_mismatch"])
            out.append(f"<td>{diff}</td>")
        out.append("</tr>")
    out.append("</tbody></table></div>")
    return "".join(out)


def _problem_page(results: dict[str, Any], metrics: dict[str, Any],
                  patterns: list[dict[str, Any]], nos: list[str], no: str,
                  summary_name: str) -> str:
    cases = [case for case in results["cases"] if case["no"] == no]
    counts = results["meta"]["case_counts"][no]
    problem = results["problems"][no]
    index = nos.index(no)
    neighbors = []
    if index > 0:
        neighbors.append(f'<a href="{_h(nos[index - 1])}.html">← {_h(nos[index - 1])}</a>')
    neighbors.append(f'<a href="../{_h(summary_name)}#problems">問題の一覧</a>')
    if index + 1 < len(nos):
        neighbors.append(f'<a href="{_h(nos[index + 1])}.html">{_h(nos[index + 1])} →</a>')
    parts = _head(f"{no} コメント返信の評価（プローブ）", "../../../")
    parts.extend([
        '<nav class="breadcrumb"><a href="../../../index.html">設計書体系ガイド</a> / '
        '<a href="../../index.html">アプリ設計</a> / '
        '<a href="../umigame-soup-1.html">探偵カメロックのウミガメのスープ</a> / '
        f'<a href="../{_h(summary_name)}">コメント返信の評価（プローブ）</a> / {_h(no)}</nav>',
        f'<h1>{_h(no)} のコメント一覧（プローブ）</h1>',
        f'<div class="page-meta"><span>実行日時: {_h(results["meta"]["run_at"])}</span>'
        f'<span>ケース: {len(cases)} 件（評価 {counts["eval"]} / 語だけ {counts["bare_term"]} / '
        f'共通 {counts["common"]}）</span></div>',
        f'<nav class="problem-nav">{" ｜ ".join(neighbors)}</nav>',
        '<div class="note"><p><strong>問題文</strong>: ' + _h(problem["problem_text"]) + '</p>'
        '<p>合否と評価はサマリーページにある。共通ケースは問題に順番に割り振っている。</p></div>',
        '<nav aria-label="目次"><strong>目次</strong><ul>'])
    parts.extend(f'<li><a href="#pattern-{_h(p["id"])}">{_h(p["label"])}</a></li>'
                 for p in patterns)
    parts.append('</ul></nav>')
    for pattern in patterns:
        pattern_id = pattern["id"]
        rows = [row for row in results["rows"][pattern_id] if row["no"] == no]
        parts.append(f'<h2 id="pattern-{_h(pattern_id)}">{_h(pattern["label"])}</h2>')
        parts.append('<h3>コメント</h3><section class="case-section">')
        parts.append(_case_table(pattern, no, cases, rows, f"raw-{pattern_id}-{no}.js",
                                 raw_heading="h3"))
        parts.append("</section>")
    parts.extend(_tail())
    return "".join(parts)


def build_page(results: dict[str, Any], out: Path) -> Path:
    """Write the summary page, one page per problem and lazy raw JS files."""
    out = Path(out)
    metrics = aggregate(results)
    patterns = results["meta"]["patterns"]
    cases = results["cases"]
    nos = results["meta"]["problems"]
    for value in [*(p["id"] for p in patterns), *nos]:
        if not re.fullmatch(r"[A-Za-z0-9_-]+", value):
            raise ValueError(f"unsafe pattern or problem id: {value!r}")
    page_dir = out.parent / out.stem
    page_dir.mkdir(parents=True, exist_ok=True)
    for old in [*page_dir.glob("raw-*.js"), *page_dir.glob("*.html")]:
        old.unlink()
    for pattern in patterns:
        for no in nos:
            rows = [row for row in results["rows"][pattern["id"]] if row["no"] == no]
            payload = [{"case_id": row["case_id"], "record": row["record"],
                        "timing": row["timing"]} for row in rows]
            key = f"{pattern['id']}/{no}"
            assignment = json.dumps(key, ensure_ascii=False) + "] = "
            data = json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True)
            data = data.replace("</", "<\\/")
            path = page_dir / f"raw-{pattern['id']}-{no}.js"
            path.write_text("window.PROBE_RAW = window.PROBE_RAW || {};\n"
                            + "window.PROBE_RAW[" + assignment + data + ";\n", encoding="utf-8")
    for no in nos:
        (page_dir / f"{no}.html").write_text(
            _problem_page(results, metrics, patterns, nos, no, out.name), encoding="utf-8")
    case_no = {case["id"]: case["no"] for case in cases}
    count = len(cases)
    parts = _head("コメント返信の評価（プローブ）", "../../")
    parts.extend([
        '<nav class="breadcrumb"><a href="../../index.html">設計書体系ガイド</a> / '
        '<a href="../index.html">アプリ設計</a> / '
        '<a href="umigame-soup-1.html">探偵カメロックのウミガメのスープ</a> / '
        'コメント返信の評価（プローブ）</nav>',
        '<h1>コメント返信の評価（プローブ）</h1>',
        f'<div class="page-meta"><span>実行日時: {_h(results["meta"]["run_at"])}</span>'
        f'<span>問題: {len(nos)} 問</span><span>ケース: {count} 件</span></div>',
        '<div class="note"><p>評価データの全件を 5 パターンに通した機械プローブ（21-6d3）。'
        f'問題 {len(nos)} 問、{count} ケース、'
        f'PROMPT_VERSION {_h(results["meta"]["prompt_version"])}、'
        f'luna_model {_h(results["meta"]["luna_model"])}。</p>'
        '<p>判定 API はケースごとに各方式を 1 回呼んでパターン間で使い回し、'
        '書き手だけパターンごとに呼んだ。コメント一覧と生データは問題ごとのページにある'
        '（合否表の NG の ID から該当の行へ飛べる）。</p></div>',
        '<nav aria-label="目次"><strong>目次</strong><ul>',
        '<li><a href="#summary">1. サマリー</a></li>',
        '<li><a href="#problems">2. 問題ごとのページ</a></li></ul></nav>',
        '<h2 id="summary">1. サマリー</h2>',
        '<h3>合否表</h3>',
        _summary_table(metrics, patterns,
                       lambda pid, cid: f"{out.stem}/{case_no.get(cid, '')}.html"),
        '<p>L1② は設計書 5.1.1 どおり、返事が 20 件以上ある種別だけで数える'
        '（返信しない ⑳㉑ と、開示文が 1 つに決まる ④ は除く）。</p>',
        '<h3>主要な率</h3>', _rate_svg(metrics, patterns),
        '<p>縦の点線は合格ライン。① 判定一致率は参考値なので基準線は置かない。棒に触れると件数が出る。</p>',
        '<h3>処理時間</h3>', _time_svg(metrics, patterns),
        '<p>中央値と p95 はそれぞれ判定・書き手・合計から個別に算出。'
        '積み上げた内訳と合計の数値は一致しない場合がある。</p>',
        '<h3>評価</h3>', _evaluation(metrics, patterns),
        '<h3>参考の数値</h3>', _reference_table(metrics, patterns),
        '<h2 id="problems">2. 問題ごとのページ</h2>',
        '<p>相違 = 正解ラベルとの不一致の件数（見張り役の食い違いは含めない）。</p>',
        _problem_index(results, metrics, patterns, nos, out.stem)])
    parts.extend(_tail())
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("".join(parts), encoding="utf-8")
    return out


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--results", type=Path, required=True)
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    args = parser.parse_args(argv)
    build_page(json.loads(args.results.read_text(encoding="utf-8")), args.out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
