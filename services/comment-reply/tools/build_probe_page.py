"""Build a standalone, locally browsable HTML report from probe results."""

from __future__ import annotations

import argparse
import html
import json
import re
import sys
from pathlib import Path
from typing import Any


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


def _summary_table(metrics: dict[str, Any], patterns: list[dict[str, Any]]) -> str:
    cells = ['<div class="table-wrap"><table class="summary-table"><thead><tr><th>指標</th>']
    cells.extend(f"<th>{_h(p['label'])}</th>" for p in patterns)
    cells.append("<th>合格ライン</th></tr></thead><tbody>")
    for heading, entries in SECTIONS:
        cells.append(f'<tr class="group"><th colspan="{len(patterns) + 2}">{_h(heading)}</th></tr>')
        for key, name in entries:
            cells.append(f"<tr><th>{_h(name)}</th>")
            for pattern in patterns:
                item = metrics["patterns"][pattern["id"]]["metrics"][key]
                cells.append(f"<td>{_h(item['value'])} {_badge(item['pass'])}</td>")
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


def _failure_detail(items: dict[str, Any]) -> str:
    """不合格の指標の内訳（どの種別・何件で落ちたか）を短く書く。"""
    parts = []
    kind = items["L1_kind"]
    if kind["pass"] is False:
        low = [f"{_kind(k)} {v['count']}/{v['total']}" for k, v in kind["by_kind"].items()
               if v["total"] and v["rate"] is not None and v["rate"] < .8 and k not in
               {"q_yesno", "q_multi", "q_open"}]
        parts.append("L1① で 80% 未満: " + ("・".join(low) if low else f"全体 {kind['value']}"))
    phrasing = items["L1_phrasing"]
    if phrasing["pass"] is False:
        over = [f"{_kind(k)} {v['count']}/{v['total']}" for k, v in phrasing["by_kind"].items()
                if v["rate"] > .5]
        parts.append("L1② で 50% 超: " + "・".join(over))
    for key in ("L2_one_liner", "L2_opener"):
        if items[key]["pass"] is False:
            item = items[key]
            parts.append(f"{METRIC_NAMES[key]} {item['total'] - item['count']} 件")
    for key in ("P1", "P2", "P7", "L2_conflict", "L2_proximity", "L2_emoji"):
        if items[key]["pass"] is False:
            parts.append(f"{METRIC_NAMES[key]} {items[key]['count']} 件")
    return " / ".join(parts)


def _evaluation(metrics: dict[str, Any], patterns: list[dict[str, Any]]) -> str:
    def score(key: str, item: dict[str, Any]) -> tuple[float, ...]:
        passed = 1.0 if item["pass"] is True else 0.0
        if key == "P6":
            details = item["details"]
            return (passed, -details["restricted_openers"],
                    details["template_rate"] if details["template_rate"] is not None else 1.0,
                    -details["no_reply_violation"],
                    -(details["ordinary_rate"] or 0))
        if key in {"P5", "L1_kind", "L1_guidance", "L2_one_liner", "L2_opener"}:
            return (passed, item["rate"] or 0)
        if key in {"P3", "P4", "L1_phrasing"}:
            return (passed, -(item["rate"] or 0))
        return (passed, -item["count"])

    lines = ["<ul>"]
    all_pass = []
    for pattern in patterns:
        items = metrics["patterns"][pattern["id"]]["metrics"]
        failed = [METRIC_NAMES[key] for key, value in items.items() if value["pass"] is False]
        if all(value["pass"] is True for value in items.values()):
            all_pass.append(pattern["label"])
        failed_text = "、".join(failed) if failed else "なし"
        detail = _failure_detail(items)
        lines.append(f"<li>{_h(pattern['label'])}: 不合格 {_h(failed_text)}"
                     + (f"（{_h(detail)}）" if detail else "") + "</li>")
    passed_text = "、".join(all_pass) if all_pass else "なし"
    lines.append(f"<li>全指標を満たしたパターン: {_h(passed_text)}</li>")
    for key, name in METRIC_NAMES.items():
        values = []
        for pattern in patterns:
            item = metrics["patterns"][pattern["id"]]["metrics"][key]
            if item["rate"] is None and key not in {"P1", "P2", "P6", "P7",
                                                     "L2_conflict", "L2_proximity", "L2_emoji"}:
                continue
            values.append((score(key, item), pattern["label"]))
        if values:
            best = max(score for score, _ in values)
            winners = "、".join(label for score, label in values if score == best)
            lines.append(f"<li>{_h(name)}の最良: {_h(winners)}</li>")
    for pattern in patterns:
        report = metrics["patterns"][pattern["id"]]
        leaks = report["metrics"]["P1"]["count"]
        lines.append(f"<li>{_h(pattern['label'])}: P1 漏れ候補 {leaks} 件（人が全件確認）</li>")
        if pattern["judge_mode"] == "hybrid":
            ref = report["reference"]
            lines.append(f"<li>{_h(pattern['label'])}: 見張り役の食い違い "
                         f"{ref['watch_mismatch']['count']} 件、合意制で割れた "
                         f"{ref['consensus_split']['count']} 件</li>")
    lines.append("</ul>")
    return "".join(lines)


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
                rows: list[dict[str, Any]], raw_file: str) -> str:
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
        out.append(f'<tr data-search="{_h(search)}" data-expected="{_h(case["expected_kind"])}" '
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
    out.append('<h5>テスト結果生データ</h5>')
    out.append(f'<details class="raw-details" data-raw-key="{_h(raw_key)}" '
               f'data-raw-src="{_h(raw_file)}"><summary>コメント記録 JSON を表示</summary>'
               '<pre>開くと読み込みます。</pre></details>')
    return "".join(out)


STYLE = """
body { overflow-wrap: anywhere; }
.container { min-width: 0; }
.summary-table, .case-table { min-width: 820px; }
.summary-table td { min-width: 125px; }
.group th { background: var(--note-bg); }
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


def build_page(results: dict[str, Any], out: Path) -> Path:
    """Recompute metrics and write deterministic HTML and lazy raw JS files."""
    out = Path(out)
    metrics = aggregate(results)
    patterns = results["meta"]["patterns"]
    cases = results["cases"]
    nos = results["meta"]["problems"]
    for value in [*(p["id"] for p in patterns), *nos]:
        if not re.fullmatch(r"[A-Za-z0-9_-]+", value):
            raise ValueError(f"unsafe pattern or problem id: {value!r}")
    raw_dir = out.parent / out.stem
    raw_dir.mkdir(parents=True, exist_ok=True)
    for old in raw_dir.glob("raw-*.js"):
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
            path = raw_dir / f"raw-{pattern['id']}-{no}.js"
            path.write_text("window.PROBE_RAW = window.PROBE_RAW || {};\n"
                            + "window.PROBE_RAW[" + assignment + data + ";\n", encoding="utf-8")
    count = len(cases)
    count_details = "、".join(
        f"{no}: 評価 {results['meta']['case_counts'][no]['eval']} / "
        f"語だけ {results['meta']['case_counts'][no]['bare_term']} / "
        f"共通 {results['meta']['case_counts'][no]['common']}"
        for no in nos
    )
    parts = ['<!DOCTYPE html><html lang="ja"><head><meta charset="UTF-8">',
             '<meta name="viewport" content="width=device-width, initial-scale=1.0">',
             '<title>コメント返信の評価（プローブ） | AutoContentPublisherSystem</title>',
             '<link rel="stylesheet" href="../../assets/style.css">',
             '<style>', STYLE, '</style></head><body><div class="container">',
             '<nav class="breadcrumb"><a href="../../index.html">設計書体系ガイド</a> / '
             '<a href="../index.html">アプリ設計</a> / '
             '<a href="umigame-soup-1.html">探偵カメロックのウミガメのスープ</a> / '
             'コメント返信の評価（プローブ）</nav>',
             '<h1>コメント返信の評価（プローブ）</h1>',
             f'<div class="page-meta"><span>実行日時: {_h(results["meta"]["run_at"])}</span>'
             f'<span>問題: {_h("・".join(nos))}</span><span>ケース: {count} 件</span></div>',
             '<div class="note"><p>21-6d1 の様式確認用サンプル。'
             f'問題 {len(nos)} 問、{count} ケース、実行日時 {_h(results["meta"]["run_at"])}。'
             f'PROMPT_VERSION {_h(results["meta"]["prompt_version"])}、'
             f'luna_model {_h(results["meta"]["luna_model"])}。</p>'
             f'<p>件数の内訳: {_h(count_details)}。</p>'
             '<p>判定 API はケースごとに各方式を 1 回呼んでパターン間で使い回し、'
             '書き手だけパターンごとに呼んだ。件数が少なく、1 件で合否が割れる。</p></div>',
             '<nav aria-label="目次"><strong>目次</strong><ul>',
             '<li><a href="#summary">1. サマリー</a></li>',
             '<li><a href="#patterns">2. パターン別の結果</a><ul>']
    for pattern in patterns:
        parts.append(f'<li><a href="#pattern-{_h(pattern["id"])}">{_h(pattern["label"])}</a><ul>')
        for no in nos:
            parts.append(f'<li><a href="#problem-{_h(pattern["id"])}-{_h(no)}">{_h(no)}</a></li>')
        parts.append("</ul></li>")
    parts.extend(['</ul></li></ul></nav>', '<h2 id="summary">1. サマリー</h2>',
                  '<h3>合否表</h3>', _summary_table(metrics, patterns),
                  '<p>L1② は設計書 5.1.1 どおり、返事が 20 件以上ある種別だけで数える'
                  '（返信しない ⑳㉑ と、開示文が 1 つに決まる ④ は除く）。サンプルでは'
                  '① 以外の種別が 5 件前後しかなく、1 件の変化で合否が割れる。</p>',
                  '<h3>主要な率</h3>', _rate_svg(metrics, patterns),
                  '<p>縦の点線は合格ライン。① 判定一致率は参考値なので基準線は置かない。棒に触れると件数が出る。</p>',
                  '<h3>処理時間</h3>', _time_svg(metrics, patterns),
                  '<p>中央値と p95 はそれぞれ判定・書き手・合計から個別に算出。'
                  '積み上げた内訳と合計の数値は一致しない場合がある。</p>',
                  '<h3>評価</h3>', _evaluation(metrics, patterns),
                  '<h3>参考の数値</h3>', _reference_table(metrics, patterns),
                  '<h2 id="patterns">2. パターン別の結果</h2>'])
    for pattern in patterns:
        pattern_id = pattern["id"]
        report = metrics["patterns"][pattern_id]
        failed = [METRIC_NAMES[key] for key, value in report["metrics"].items()
                  if value["pass"] is False]
        parts.append(f'<h3 id="pattern-{_h(pattern_id)}">{_h(pattern["label"])}</h3>')
        parts.append(f'<p>不合格: {_h("、".join(failed) if failed else "なし")}</p>')
        for no in nos:
            problem_text = results["problems"][no]["problem_text"]
            heading = problem_text[:60] + ("…" if len(problem_text) > 60 else "")
            parts.append(f'<h4 id="problem-{_h(pattern_id)}-{_h(no)}">{_h(no)} '
                         f'{_h(heading)}</h4>')
            parts.append('<h5>コメント</h5>')
            parts.append('<section class="case-section">')
            selected_cases = [case for case in cases if case["no"] == no]
            selected_rows = [row for row in results["rows"][pattern_id] if row["no"] == no]
            raw_file = f"{out.stem}/raw-{pattern_id}-{no}.js"
            parts.append(_case_table(pattern, no, selected_cases, selected_rows, raw_file))
            parts.append("</section>")
    parts.append('<script>')
    parts.append(SCRIPT)
    parts.append('</script></div></body></html>\n')
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
