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
from app.reply import templates  # noqa: E402
from tools.probe_metrics import (  # noqa: E402
    CORRECT_OPENERS, PHRASING_MIN_CASES, QUESTION_KINDS, RELEVANCE_WORDS,
    aggregate, apply_labels, pair_key, row_flags,
)


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
# 答え・判定経路の内部コードを、一覧表では日本語で出す（生データ JSON はコードのまま）
ANSWER_LABEL = {
    "yes": "はい", "no": "いいえ", "irrelevant": "関係ない",
}
DECISION_LABEL = {
    "luna": "luna の判定", "jev": "Jev の判定",
    "jev_fallback_luna": "Jev 失敗のため luna の判定",
    "consensus_ok": "正解宣言（luna・Jev とも正解）",
    "consensus_split": "正解宣言を保留（luna だけ正解）",
}
SECTIONS = (
    ("前提条件 P1〜P7", (
        ("P1", "P1 漏れ候補"), ("P2", "P2 誤った正解宣言"),
        ("P3", "P3 はい / いいえの取り違え"), ("P4", "P4 判定の揺れ"),
        ("P5", "P5 正解宣言率"), ("P6", "P6 不適切系の応答"),
        ("P7", "P7 80 字超"))),
    ("レベル 1", (
        ("L1_kind", "L1① 種別一致率（全体）"),
        ("L1_kind_each", "L1① 種別一致率（質問以外の各種別）"),
        ("L1_phrasing", "L1② 言い回しの偏り"),
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


_CODE_RE = re.compile(r"\b[a-z][a-z_]*\b")


def _ja_note(note: str) -> str:
    """NG の注記に含まれる種別・答えの内部コードを日本語にする。"""
    def label(match: re.Match[str]) -> str:
        code = match.group(0)
        if code in KIND_LABEL:
            return KIND_LABEL[code]
        return ANSWER_LABEL.get(code, code)
    return _CODE_RE.sub(label, note)


def _answer(answer: str | None) -> str:
    return ANSWER_LABEL.get(answer, str(answer) if answer else "—")


def _decision(decision: str | None) -> str:
    return DECISION_LABEL.get(decision, str(decision) if decision else "—")


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
        + (f' <span class="ng-note">{_h(_ja_note(str(e["note"])))}</span>' if e.get("note") else "") + "</li>"
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
                value = _ja_note(item["value"]) if key == "L1_kind_each" else item["value"]
                cells.append(f"<td>{_h(value)} {_badge(item['pass'])}"
                             f"{_ng_details(pattern['id'], item, page_of)}</td>")
            threshold = metrics["patterns"][patterns[0]["id"]]["metrics"][key]["threshold"]
            cells.append(f"<td>{_h(threshold)}</td></tr>")
            if key == "L1_kind_each":
                cells.append(_kind_rows(metrics, patterns, page_of))
    count = sum(len(entries) for _, entries in SECTIONS)
    cells.append("<tr><th>合格した指標の数</th>")
    for pattern in patterns:
        values = metrics["patterns"][pattern["id"]]["metrics"].values()
        cells.append(f"<td>{sum(v['pass'] is True for v in values)} / {count}</td>")
    cells.append("<td>参考: 対象なしは数えない</td></tr></tbody></table></div>")
    return "".join(cells)


def _kind_rows(metrics: dict[str, Any], patterns: list[dict[str, Any]],
               page_of: Callable[[str, str], str]) -> str:
    """L1①（質問以外の各種別）の内訳を種別ごとに 1 行ずつ出す（合格指標の数には数えない）。"""
    first = metrics["patterns"][patterns[0]["id"]]["metrics"]["L1_kind_each"]
    rows = []
    for kind in first.get("kinds", {}):
        entries = [metrics["patterns"][p["id"]]["metrics"]["L1_kind_each"]["kinds"][kind]
                   for p in patterns]
        toggle = ('<button type="button" class="ng-row" aria-label="この行の NG を開く / 閉じる">'
                  '行を開く</button>' if any(e["ng"] for e in entries) else "")
        cells = [f'<tr class="sub-row"><th>{_h(_kind(kind))}{toggle}</th>']
        for pattern, entry in zip(patterns, entries):
            value = (f"{entry['rate']:.1%}（{entry['count']}/{entry['total']}）"
                     if entry["rate"] is not None else "対象なし")
            cells.append(f"<td>{_h(value)} {_badge(entry['pass'])}"
                         f"{_ng_details(pattern['id'], entry, page_of)}</td>")
        cells.append("<td>80% 以上</td></tr>")
        rows.append("".join(cells))
    return "".join(rows)


REVIEW_CORE = r"""
function reviewMetrics(data, acceptedKeys) {
  var accepted = acceptedKeys instanceof Set ? acceptedKeys : new Set(acceptedKeys || []);
  function percent(rate) {
    if (rate === null || rate === undefined) return '対象なし';
    var scaled = rate * 100 * 10;
    var base = Math.floor(scaled);
    var fraction = scaled - base;
    var rounded = fraction === 0.5 ? (base % 2 === 0 ? base : base + 1) : Math.round(scaled);
    return (rounded / 10).toFixed(1) + '%';
  }
  function rateValue(count, total) {
    return total ? percent(count / total) + '（' + count + '/' + total + '）' : '対象なし';
  }
  function metric(value, pass) { return {value: value, pass: pass}; }
  function answerMatches(item) {
    return item.expected_answer === item.answer ||
      (item.expected_answer === 'irrelevant' && item.answer === 'no' && item.relevance);
  }
  var output = {};
  data.pattern_ids.forEach(function (patternId) {
    var rows = data.rows[patternId].map(function (source) {
      var row = Object.assign({}, source);
      if (row.pair_key && accepted.has(row.pair_key)) {
        row.expected_kind = row.kind;
        row.expected_answer = row.kind === 'q_yesno' ? row.answer : null;
      }
      return row;
    });
    var total = rows.length;
    var q = rows.filter(function (x) { return x.expected_kind === 'q_yesno'; });
    var p3Cases = q.filter(function (x) { return x.expected_answer === 'yes' || x.expected_answer === 'no'; });
    var p3Items = p3Cases.filter(function (x) {
      return x.kind === 'q_yesno' && (x.answer === 'yes' || x.answer === 'no') &&
        x.answer !== x.expected_answer;
    });
    var p3ByProblem = {};
    p3Items.forEach(function (x) { p3ByProblem[x.no] = (p3ByProblem[x.no] || 0) + 1; });
    var maxP3Problem = Math.max.apply(null, [0].concat(Object.keys(p3ByProblem).map(function (k) {
      return p3ByProblem[k];
    })));
    var p4Cases = q.filter(function (x) {
      return x.expected_answer === 'no' || x.expected_answer === 'irrelevant';
    });
    var p4Items = p4Cases.filter(function (x) {
      return x.kind === 'q_yesno' && (x.answer === 'no' || x.answer === 'irrelevant') &&
        !answerMatches(x);
    });
    var wrongCorrect = rows.filter(function (x) {
      return x.expected_kind !== 'guess_correct' && x.correct_opener;
    }).length;
    var correct = rows.filter(function (x) { return x.expected_kind === 'guess_correct'; });
    var declared = correct.filter(function (x) { return x.correct_opener; }).length;
    var kindStats = {};
    data.kinds.forEach(function (kind) {
      var selected = rows.filter(function (x) { return x.expected_kind === kind; });
      var matched = selected.filter(function (x) { return x.kind === kind; }).length;
      kindStats[kind] = {count: matched, total: selected.length,
        rate: selected.length ? matched / selected.length : null};
    });
    var kindCount = rows.filter(function (x) { return x.kind === x.expected_kind; }).length;
    var allRate = total ? kindCount / total : null;
    var lowKinds = data.kinds.filter(function (kind) {
      var entry = kindStats[kind];
      return data.question_kinds.indexOf(kind) < 0 && entry.rate !== null && entry.rate < 0.8;
    });
    var nonQuestionRates = data.kinds.filter(function (kind) {
      return data.question_kinds.indexOf(kind) < 0 && kindStats[kind].rate !== null;
    }).map(function (kind) { return kindStats[kind].rate; });
    var phrasing = [];
    data.kinds.forEach(function (kind) {
      if (data.no_reply_kinds.indexOf(kind) >= 0 || kind === 'guess_correct') return;
      var selected = rows.filter(function (x) { return x.expected_kind === kind; });
      if (selected.length >= data.phrasing_min_cases) {
        var counts = {};
        selected.forEach(function (x) {
          var key = String(x.phrase_id);
          counts[key] = (counts[key] || 0) + 1;
        });
        var count = Math.max.apply(null, Object.keys(counts).map(function (key) { return counts[key]; }));
        phrasing.push({count: count, total: selected.length, rate: count / selected.length});
      }
    });
    var phraseRate = phrasing.length ? Math.max.apply(null, phrasing.map(function (x) { return x.rate; })) : null;
    var guidance = rows.filter(function (x) {
      return x.expected_kind === 'q_multi' || x.expected_kind === 'q_open';
    });
    var guided = guidance.filter(function (x) {
      return (x.kind === 'q_multi' || x.kind === 'q_open') && x.reply_present;
    }).length;
    var pattern = {passCount: 0, yesno: {}};
    pattern.P2 = metric(wrongCorrect + ' 件', wrongCorrect === 0);
    pattern.P3 = metric(p3Items.length + ' 件 / ' + p3Cases.length + ' 件', p3Cases.length ?
      (p3Items.length <= 0.03 * p3Cases.length && maxP3Problem <= 2) : null);
    var p4Rate = p4Cases.length ? p4Items.length / p4Cases.length : null;
    pattern.P4 = metric(p4Rate === null ? '対象なし' : rateValue(p4Items.length, p4Cases.length),
      p4Rate === null ? null : p4Rate <= 0.1);
    var p5Rate = correct.length ? declared / correct.length : null;
    pattern.P5 = metric(p5Rate === null ? '対象なし' : rateValue(declared, correct.length),
      p5Rate === null ? null : p5Rate >= 0.8);
    pattern.L1_kind = metric(allRate === null ? '対象なし' : rateValue(kindCount, total),
      allRate === null ? null : allRate >= 0.9);
    var kindEachValue = lowKinds.map(function (kind) {
      var entry = kindStats[kind];
      return data.kind_labels[kind] + ' ' + percent(entry.rate) + '（' + entry.count + '/' + entry.total + '）';
    }).join('・');
    if (!lowKinds.length) kindEachValue = nonQuestionRates.length ?
      '最低 ' + percent(Math.min.apply(null, nonQuestionRates)) : '対象なし';
    pattern.L1_kind_each = metric(kindEachValue, nonQuestionRates.length ? lowKinds.length === 0 : null);
    pattern.L1_kind_each.kinds = {};
    data.kinds.forEach(function (kind) {
      if (data.question_kinds.indexOf(kind) >= 0) return;
      var entry = kindStats[kind];
      pattern.L1_kind_each.kinds[kind] = {
        value: entry.rate === null ? '対象なし' : rateValue(entry.count, entry.total),
        pass: entry.rate === null ? null : entry.rate >= 0.8
      };
    });
    pattern.L1_phrasing = metric(phraseRate === null ? '対象なし' : '最大 ' + percent(phraseRate),
      phraseRate === null ? null : phrasing.every(function (x) { return x.rate <= 0.5; }));
    var guidanceRate = guidance.length ? guided / guidance.length : null;
    pattern.L1_guidance = metric(guidanceRate === null ? '対象なし' : rateValue(guided, guidance.length),
      guidanceRate === null ? null : guidanceRate >= 0.8);
    ['existing', 'new'].forEach(function (name) {
      var isNew = name === 'new';
      var selected = q.filter(function (x) { return x.case_b === isNew; });
      var matched = selected.filter(function (x) { return x.kind === 'q_yesno' && !(
        x.kind === 'q_yesno' && x.expected_kind === 'q_yesno' && !answerMatches(x));
      }).length;
      pattern.yesno[name] = {value: rateValue(matched, selected.length)};
    });
    data.fixed[patternId] && Object.keys(data.fixed[patternId]).forEach(function (key) {
      pattern[key] = data.fixed[patternId][key];
    });
    var metricKeys = data.metric_keys;
    pattern.passCount = metricKeys.filter(function (key) { return pattern[key].pass === true; }).length;
    output[patternId] = pattern;
  });
  return output;
}
"""


REVIEW_RECALCULATED = (
    "P2", "P3", "P4", "P5", "L1_kind", "L1_kind_each", "L1_phrasing", "L1_guidance",
)
REVIEW_FIXED = ("P1", "P6", "P7", "L2_one_liner", "L2_opener", "L2_conflict",
                "L2_proximity", "L2_emoji")


def _review_data(results: dict[str, Any], metrics: dict[str, Any]) -> dict[str, Any]:
    """ブラウザーで数え直すための、ラベルに依存しない事実を組み立てる。"""
    cases = {case["id"]: case for case in results["cases"]}
    patterns = results["meta"]["patterns"]
    review_rows: dict[str, list[dict[str, Any]]] = {}
    pairs: dict[str, dict[str, Any]] = {}
    for pattern in patterns:
        pattern_id = pattern["id"]
        phrases: dict[str, int] = {}
        facts = []
        for row in results["rows"].get(pattern_id, []):
            case = cases[row["case_id"]]
            record = row["record"]
            final = record.get("final") or {}
            reply = (record.get("reply") or {}).get("text")
            kind, answer = final.get("kind"), final.get("answer")
            labeled = apply_labels({"kind": kind, "answer": answer,
                                    "comment_text": case["text"]}, case)
            flags = row_flags(row, case)
            phrase = "<NO_REPLY>" if reply is None else reply
            if phrase not in phrases:
                phrases[phrase] = len(phrases)
            key = pair_key(row["case_id"], kind, answer) if flags["label_mismatch"] else None
            facts.append({
                "expected_kind": labeled["expected_kind"],
                "expected_answer": labeled["expected_answer"],
                "kind": kind, "answer": answer,
                "relevance": any(word in case["text"] for word in RELEVANCE_WORDS),
                "correct_opener": bool(reply and reply.startswith(CORRECT_OPENERS)),
                "reply_present": bool(reply), "phrase_id": phrases[phrase],
                "case_b": "-b" in case["id"], "no": case["no"], "pair_key": key,
            })
            if key is not None:
                pair = pairs.get(key)
                if pair is None:
                    pair = {"key": key, "case_id": case["id"], "no": case["no"],
                            "kind": kind, "answer": answer,
                            "expected_kind": labeled["expected_kind"],
                            "expected_answer": labeled["expected_answer"], "rows": 0}
                    pairs[key] = pair
                pair["rows"] += 1
        review_rows[pattern_id] = facts
    fixed = {
        pattern["id"]: {
            key: {"value": metrics["patterns"][pattern["id"]]["metrics"][key]["value"],
                  "pass": metrics["patterns"][pattern["id"]]["metrics"][key]["pass"]}
            for key in REVIEW_FIXED
        }
        for pattern in patterns
    }
    return {
        "run_at": results["meta"]["run_at"],
        "kinds": list(KINDS), "kind_labels": KIND_LABEL,
        "question_kinds": sorted(QUESTION_KINDS),
        "no_reply_kinds": sorted(templates.NO_REPLY_KINDS),
        "phrasing_min_cases": PHRASING_MIN_CASES,
        "pattern_ids": [pattern["id"] for pattern in patterns],
        "rows": review_rows, "pairs": list(pairs.values()), "fixed": fixed,
        "metric_keys": [key for _, entries in SECTIONS for key, _ in entries],
    }


def _review_cell(value: str, passed: bool | None, *, metric: str | None = None,
                 kind: str | None = None, yesno: str | None = None,
                 pattern: str | None = None) -> str:
    pass_token = "null" if passed is None else "true" if passed else "false"
    attrs = f' data-initial-value="{_h(value)}" data-initial-pass="{pass_token}"'
    if metric:
        attrs += f' data-review-metric="{_h(metric)}"'
    if kind:
        attrs += f' data-review-kind="{_h(kind)}"'
    if yesno:
        attrs += f' data-review-yesno="{_h(yesno)}"'
    if pattern:
        attrs += f' data-review-pattern="{_h(pattern)}"'
    return f'<td{attrs}><span class="review-value">{_h(value)}</span> {_badge(passed)}</td>'


def _human_review_table(metrics: dict[str, Any], patterns: list[dict[str, Any]],
                        pairs_total: int) -> str:
    """人間チェック後の集計を即時反映する表を出力する。"""
    out = ['<div class="human-review-toolbar" id="human-review-toolbar">',
           f'<strong class="review-count">確認済み 0 / {pairs_total} 組（許容 0・不可 0）</strong>',
           '<button type="button" class="review-export">書き出す</button>',
           '<button type="button" class="review-import">読み込む</button>',
           '<input class="review-file" type="file" accept="application/json">',
           '<button type="button" class="review-reset">すべて未確認に戻す</button>',
           '<span class="review-status" role="status"></span></div>',
           '<div class="table-wrap"><table class="summary-table human-review-table"><thead><tr><th>指標</th>']
    out.extend(f"<th>{_h(pattern['label'])}</th>" for pattern in patterns)
    out.append("<th>合格ライン</th></tr></thead><tbody>")
    for heading, entries in SECTIONS:
        out.append(f'<tr class="group"><th colspan="{len(patterns) + 2}">{_h(heading)}</th></tr>')
        for key, name in entries:
            note = '<small class="review-machine-note">機械判定のまま</small>' if key in REVIEW_FIXED else ""
            out.append(f"<tr><th>{_h(name)}{note}</th>")
            for pattern in patterns:
                item = metrics["patterns"][pattern["id"]]["metrics"][key]
                value = _ja_note(item["value"]) if key == "L1_kind_each" else item["value"]
                out.append(_review_cell(value, item["pass"], metric=key,
                                        pattern=pattern["id"]))
            threshold = metrics["patterns"][patterns[0]["id"]]["metrics"][key]["threshold"]
            out.append(f"<td>{_h(threshold)}</td></tr>")
            if key == "L1_kind_each":
                for kind in KINDS:
                    if kind in QUESTION_KINDS:
                        continue
                    out.append(f'<tr class="sub-row"><th>{_h(_kind(kind))}</th>')
                    for pattern in patterns:
                        entry = metrics["patterns"][pattern["id"]]["metrics"][key]["kinds"][kind]
                        value = (f"{entry['rate']:.1%}（{entry['count']}/{entry['total']}）"
                                 if entry["rate"] is not None else "対象なし")
                        out.append(_review_cell(value, entry["pass"], kind=kind,
                                                pattern=pattern["id"]))
                    out.append("<td>80% 以上</td></tr>")
    out.append('<tr class="group"><th colspan="' + str(len(patterns) + 2) + '">参考</th></tr>')
    for sub, label in (("existing", "① 判定一致率（従来の質問）"),
                       ("new", "① 判定一致率（新しい質問）")):
        out.append(f"<tr><th>{_h(label)}</th>")
        for pattern in patterns:
            item = metrics["patterns"][pattern["id"]]["reference"]["yesno_accuracy"][sub]
            out.append(_review_cell(item["value"], None, yesno=sub,
                                    pattern=pattern["id"]))
        out.append("<td>参考</td></tr>")
    count = sum(len(entries) for _, entries in SECTIONS)
    out.append('<tr><th>合格した指標の数</th>')
    for pattern in patterns:
        values = metrics["patterns"][pattern["id"]]["metrics"].values()
        passed = sum(value["pass"] is True for value in values)
        out.append(f'<td data-review-passcount="1" data-review-pattern="{_h(pattern["id"])}" '
                   f'data-initial-value="{passed} / {count}">'
                   f'<span class="review-value">{passed} / {count}</span></td>')
    out.append("<td>参考: 対象なしは数えない</td></tr></tbody></table></div>")
    return "".join(out)


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
    if key == "L1_kind_each":
        return "80% 未満: " + "・".join(f"{_kind(k)} {v['rate']:.1%}（{v['count']}/{v['total']}）"
                                         for k, v in item["by_kind"].items())
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
           '<label><input class="filter-unchecked" type="checkbox"> 未確認の相違だけ</label>',
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
        mismatch_display = mismatch
        if flags["watch_mismatch"] and pattern["judge_mode"] == "hybrid":
            mismatch_display += " 見張り" if mismatch_display else "見張り"
        review_key = pair_key(case["id"], final.get("kind"), final.get("answer"))
        expected = _kind(case["expected_kind"])
        if case.get("expected_answer"):
            expected += " / " + _answer(case["expected_answer"])
        actual = _kind(final.get("kind"))
        if final.get("answer"):
            actual += " / " + _answer(final["answer"])
        actual += " / " + _decision(final.get("decision"))
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
            (expected, expected), (actual, actual),
            (reply if reply is not None else "返信なし", reply or ""),
            (seconds + " 秒", duration or 0),
        )
        for i, (display, sort) in enumerate(values[:4]):
            out.append(f'<td data-sort="{_h(sort)}">{_h(display)}</td>')
        review_select = (f'<select class="review-select" data-pair="{_h(review_key)}" '
                         'aria-label="この組の人間チェック"><option value="">未確認</option>'
                         '<option value="accept">許容</option><option value="reject">不可</option></select>'
                         if flags["label_mismatch"] else "")
        out.append(f'<td data-sort="{_h(mismatch_display)}">{_h(mismatch_display)}{review_select}</td>')
        for i, (display, sort) in enumerate(values[4:], start=5):
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
.sub-row th { padding-left: 1.6rem; font-weight: normal; }
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
.case-table tr[data-review-decision="accept"] td { background: rgba(40, 150, 80, .2); }
.case-table tr[data-review-decision="reject"] td { background: rgba(210, 60, 60, .2); }
.review-select { max-width: 6.5rem; margin-left: .35rem; font: inherit; font-size: .8rem; }
.review-page-status, .review-toolbar { display: flex; flex-wrap: wrap; gap: .5rem 1rem; align-items: center; margin: .75rem 0; }
.review-toolbar button { font: inherit; padding: .25rem .6rem; cursor: pointer; }
.review-status { font-size: .85rem; color: var(--text-muted, inherit); }
.review-machine-note { display: block; font-size: .75rem; font-weight: 400; color: var(--text-muted, inherit); }
.human-review-table td.changed { background: var(--warn-bg); }
.human-review-toolbar { display: flex; flex-wrap: wrap; gap: .5rem; align-items: center; margin: .75rem 0; }
.human-review-toolbar button { font: inherit; padding: .25rem .6rem; cursor: pointer; }
.human-review-toolbar input[type=file] { display: none; }
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
      var unchecked = controls.querySelector('.filter-unchecked').checked;
      var shown = 0;
      rows.forEach(function (row) {
        var review = row.querySelector('.review-select');
        var visible = (!query || row.dataset.search.toLocaleLowerCase().includes(query)) &&
          (!expected || row.dataset.expected === expected) &&
          (!finalKind || row.dataset.final === finalKind) &&
          (!diff || row.dataset.diff === '1') &&
          (!unchecked || (review && !review.value));
        row.hidden = !visible;
        if (visible) shown += 1;
      });
      table._probeFilter = filter;
      count.textContent = rows.length + ' 件中 ' + shown + ' 件を表示';
    }
    controls.querySelectorAll('input,select').forEach(function (input) {
      input.addEventListener('input', filter);
      input.addEventListener('change', filter);
    });
    table._probeFilter = filter;
    filter();
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
      controls.querySelector('.filter-unchecked').checked = false;
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


REVIEW_CLIENT = r"""
(function () {
  var dataNode = document.getElementById('review-data');
  var pageStatus = document.getElementById('problem-review-status');
  var data = null;
  try { if (dataNode) data = JSON.parse(dataNode.textContent); } catch (error) { data = null; }
  var runAt = data ? data.run_at : (pageStatus ? pageStatus.dataset.runAt : '');
  if (!runAt) return;
  var storageKey = 'umigame-probe-review/' + runAt;
  var status = document.querySelector('.review-status');
  var storageAvailable = true;
  var decisions = {};
  var pairs = data ? data.pairs : [];
  var pairKeys = new Set(pairs.map(function (pair) { return pair.key; }));
  function showStorageError() {
    storageAvailable = false;
    if (status) status.textContent = 'この開き方では保存できません';
    if (pageStatus) pageStatus.querySelector('.review-status').textContent =
      'この開き方では保存できません';
  }
  function validMap(value) {
    var result = {};
    if (!value || typeof value !== 'object' || Array.isArray(value)) return result;
    Object.keys(value).forEach(function (key) {
      var entry = value[key];
      if (entry && (entry.decision === 'accept' || entry.decision === 'reject')) {
        result[key] = {decision: entry.decision, at: entry.at || new Date().toISOString()};
      }
    });
    return result;
  }
  function load() {
    try {
      var raw = window.localStorage.getItem(storageKey);
      decisions = raw ? validMap(JSON.parse(raw)) : {};
    } catch (error) {
      decisions = {};
      showStorageError();
    }
  }
  function save() {
    try { window.localStorage.setItem(storageKey, JSON.stringify(decisions)); }
    catch (error) { showStorageError(); }
  }
  function setDecision(key, value, at) {
    if (!value) delete decisions[key];
    else decisions[key] = {decision: value, at: at || new Date().toISOString()};
    save();
  }
  function applyBadge(cell, passed) {
    var badge = document.createElement('span');
    badge.className = 'badge ' + (passed === null || passed === undefined ? 'badge-future' :
      (passed ? 'badge-fixed' : 'badge-wip'));
    badge.textContent = passed === null || passed === undefined ? '対象なし' :
      (passed ? '合格' : '不合格');
    cell.appendChild(document.createTextNode(' '));
    cell.appendChild(badge);
  }
  function renderCell(cell, value, passed, hasBadge) {
    cell.replaceChildren();
    var span = document.createElement('span');
    span.className = 'review-value';
    span.textContent = value;
    cell.appendChild(span);
    var isChanged = String(value) !== cell.dataset.initialValue ||
      (hasBadge && String(passed) !== cell.dataset.initialPass);
    cell.classList.toggle('changed', isChanged);
    if (hasBadge) applyBadge(cell, passed);
  }
  function renderProblem() {
    if (!pageStatus) return;
    var selects = Array.from(document.querySelectorAll('.review-select'));
    var keys = new Set(selects.map(function (select) { return select.dataset.pair; }));
    var accept = 0, reject = 0;
    selects.forEach(function (select) {
      var decision = decisions[select.dataset.pair];
      select.value = decision ? decision.decision : '';
      var row = select.closest('tr');
      if (row) {
        row.dataset.reviewDecision = select.value;
      }
    });
    keys.forEach(function (key) {
      var decision = decisions[key];
      if (decision && decision.decision === 'accept') accept += 1;
      if (decision && decision.decision === 'reject') reject += 1;
    });
    var confirmed = accept + reject;
    pageStatus.querySelector('.review-count').textContent = 'このページの組: 確認済み ' +
      confirmed + ' / ' + keys.size + ' 組（許容 ' + accept + '・不可 ' + reject + '）';
  }
  function renderSummary() {
    if (!data || typeof window.reviewMetrics !== 'function') return;
    var confirmed = 0, accept = 0, reject = 0;
    pairs.forEach(function (pair) {
      var decision = decisions[pair.key];
      if (decision) {
        confirmed += 1;
        if (decision.decision === 'accept') accept += 1;
        if (decision.decision === 'reject') reject += 1;
      }
    });
    var count = document.querySelector('#human-review-toolbar .review-count');
    if (count) count.textContent = '確認済み ' + confirmed + ' / ' + pairs.length +
      ' 組（許容 ' + accept + '・不可 ' + reject + '）';
    var accepted = new Set(pairs.filter(function (pair) {
      return decisions[pair.key] && decisions[pair.key].decision === 'accept';
    }).map(function (pair) { return pair.key; }));
    var calculated = window.reviewMetrics(data, accepted);
    document.querySelectorAll('[data-review-metric]').forEach(function (cell) {
      var pattern = calculated[cell.dataset.reviewPattern];
      var item = pattern && pattern[cell.dataset.reviewMetric];
      if (item) renderCell(cell, item.value, item.pass, true);
    });
    document.querySelectorAll('[data-review-kind]').forEach(function (cell) {
      var pattern = calculated[cell.dataset.reviewPattern];
      var item = pattern && pattern.L1_kind_each.kinds[cell.dataset.reviewKind];
      if (item) renderCell(cell, item.value, item.pass, true);
    });
    document.querySelectorAll('[data-review-yesno]').forEach(function (cell) {
      var pattern = calculated[cell.dataset.reviewPattern];
      var item = pattern && pattern.yesno[cell.dataset.reviewYesno];
      if (item) renderCell(cell, item.value, null, true);
    });
    document.querySelectorAll('[data-review-passcount]').forEach(function (cell) {
      var pattern = calculated[cell.dataset.reviewPattern];
      if (!pattern) return;
      var value = pattern.passCount + ' / ' + data.metric_keys.length;
      cell.replaceChildren();
      var span = document.createElement('span');
      span.className = 'review-value';
      span.textContent = value;
      cell.appendChild(span);
      cell.classList.toggle('changed', value !== cell.dataset.initialValue);
    });
  }
  function render() {
    renderProblem();
    renderSummary();
    document.querySelectorAll('.case-table').forEach(function (table) {
      if (table._probeFilter) table._probeFilter();
    });
  }
  load();
  document.querySelectorAll('.review-select').forEach(function (select) {
    select.addEventListener('change', function () {
      setDecision(select.dataset.pair, select.value);
      render();
    });
  });
  window.addEventListener('storage', function (event) {
    if (event.key !== storageKey && event.key !== null) return;
    try { decisions = event.newValue ? validMap(JSON.parse(event.newValue)) : {}; }
    catch (error) { decisions = {}; }
    render();
  });
  var toolbar = document.getElementById('human-review-toolbar');
  if (toolbar && data) {
    toolbar.querySelector('.review-export').addEventListener('click', function () {
      var exported = {
        run_at: data.run_at, exported_at: new Date().toISOString(), pairs_total: pairs.length,
        decisions: pairs.map(function (pair) {
          var decision = decisions[pair.key];
          return {key: pair.key, case_id: pair.case_id, no: pair.no, kind: pair.kind,
            answer: pair.answer, expected_kind: pair.expected_kind,
            expected_answer: pair.expected_answer,
            decision: decision ? decision.decision : 'unchecked',
            decided_at: decision ? decision.at : null};
        })
      };
      var blob = new Blob([JSON.stringify(exported, null, 2)], {type: 'application/json'});
      var link = document.createElement('a');
      link.href = URL.createObjectURL(blob);
      link.download = 'probe-review-' + String(data.run_at).slice(0, 10) + '.json';
      document.body.appendChild(link);
      link.click();
      link.remove();
      setTimeout(function () { URL.revokeObjectURL(link.href); }, 0);
    });
    var fileInput = toolbar.querySelector('.review-file');
    toolbar.querySelector('.review-import').addEventListener('click', function () { fileInput.click(); });
    fileInput.addEventListener('change', function () {
      var file = fileInput.files && fileInput.files[0];
      if (!file) return;
      var reader = new FileReader();
      reader.onload = function () {
        try {
          var imported = JSON.parse(String(reader.result));
          if (!imported || !Array.isArray(imported.decisions)) throw new Error('invalid');
          if (imported.run_at !== data.run_at &&
              !window.confirm('実行日時が異なります。読み込みますか？')) return;
          var unknown = 0;
          imported.decisions.forEach(function (entry) {
            if (!entry || !pairKeys.has(entry.key)) { unknown += 1; return; }
            if (entry.decision === 'accept' || entry.decision === 'reject') {
              decisions[entry.key] = {decision: entry.decision,
                at: entry.decided_at || new Date().toISOString()};
            } else if (entry.decision === 'unchecked') delete decisions[entry.key];
          });
          save();
          render();
          if (status && storageAvailable) {
            status.textContent = '読み込み完了（未知のキー ' + unknown + ' 件を無視）';
          }
        } catch (error) {
          if (status) status.textContent = 'JSON を読み込めませんでした';
        } finally { fileInput.value = ''; }
      };
      reader.readAsText(file, 'UTF-8');
    });
    toolbar.querySelector('.review-reset').addEventListener('click', function () {
      if (!window.confirm('この実行の人間チェックをすべて未確認に戻しますか？')) return;
      decisions = {};
      save();
      render();
    });
  }
  render();
})();
"""


def _head(title: str, assets: str) -> list[str]:
    return ['<!DOCTYPE html><html lang="ja"><head><meta charset="UTF-8">',
            '<meta name="viewport" content="width=device-width, initial-scale=1.0">',
            f'<title>{_h(title)} | AutoContentPublisherSystem</title>',
            f'<link rel="stylesheet" href="{assets}assets/style.css">',
            '<style>', STYLE, '</style></head><body><div class="container">']


def _tail() -> list[str]:
    return ['<script>', SCRIPT, REVIEW_CLIENT, '</script></div></body></html>\n']


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
    indexed = {case["id"]: case for case in results["cases"]}
    problem_pairs = set()
    for pattern in patterns:
        for row in results["rows"].get(pattern["id"], []):
            if row["no"] != no:
                continue
            case = indexed[row["case_id"]]
            if row_flags(row, case)["label_mismatch"]:
                final = row["record"].get("final") or {}
                problem_pairs.add(pair_key(case["id"], final.get("kind"), final.get("answer")))
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
        '<p>合否と評価はサマリーページにある。共通ケースは問題に順番に割り振っている。</p>'
        '<p>「判定内容」は 種別 / 答え / どの判定を採用したか の順。答えは はい / いいえ / 関係ない の 3 値で、'
        '真相と確定事実のどちらからも決められないとき（Jev は確信度が足りないとき）は「関係ない」になる。</p></div>',
        f'<div class="review-page-status" id="problem-review-status" data-run-at="{_h(results["meta"]["run_at"])}">'
        f'<strong class="review-count">このページの組: 確認済み 0 / {len(problem_pairs)} 組（許容 0・不可 0）</strong>'
        f'<a href="../{_h(summary_name)}#human-review">サマリーの人間チェック</a>'
        '<span class="review-status" role="status"></span></div>',
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
    review_data = _review_data(results, metrics)
    review_json = json.dumps(review_data, ensure_ascii=False, separators=(",", ":"))
    review_json = review_json.replace("</", "<\\/")
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
        '<li><a href="#human-review">人間チェック後のサマリー</a></li>',
        '<li><a href="#problems">2. 問題ごとのページ</a></li></ul></nav>',
        '<h2 id="summary">1. サマリー</h2>',
        '<h3>合否表</h3>',
        _summary_table(metrics, patterns,
                       lambda pid, cid: f"{out.stem}/{case_no.get(cid, '')}.html"),
        '<h3 id="human-review">人間チェック後のサマリー</h3>',
        _human_review_table(metrics, patterns, len(review_data["pairs"])),
        '<script type="application/json" id="review-data">', review_json, '</script>',
        '<script>', REVIEW_CORE, 'window.reviewMetrics = reviewMetrics;', '</script>',
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
