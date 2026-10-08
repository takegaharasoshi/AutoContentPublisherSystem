"""Sweep stage-B thresholds and test consensus rules over a cached probe run (21-6d11).

全件プローブの results.json に残った判定（段 B の要点ごとの hit / close、段 B2 の矛盾確率）から、
Jev・Decisions の閾値を変えたときの正解宣言と ⑤ / ⑥ の分かれ方を再計算する。
「正解宣言は 2 方式の合意を必須にする」場合の P2（誤った正解宣言）と P5（正解推理の宣言率）も、
方式の組み合わせごとに数える。どちらも判定レベルの集計で、返信文の冒頭語で数える probe_metrics の
P2 とは数え方が異なる。閾値と合意ルールは決めない（21-6e）。

T_POINT を下げると、段 B2 を呼んでいないケースが正解宣言の候補に入る。``--fill-b2`` を付けると
その分だけ段 B2 を実 API で取り、``sweep_b2_cache.json`` に貯める（付けないときは「B2 未取得」と数える）。
"""

from __future__ import annotations

import argparse
import itertools
import json
import os
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import Any


SERVICE_DIR = Path(__file__).resolve().parent.parent
if str(SERVICE_DIR) not in sys.path:
    sys.path.insert(0, str(SERVICE_DIR))

METHOD_ROWS = {"luna": "luna-1b", "jev": "jev-2b", "decisions": "dec-2c"}
STAGED = ("jev", "decisions")
T_POINTS = (0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9)
T_CLOSES = (0.1, 0.15, 0.2, 0.25, 0.3, 0.4, 0.5)
T_CONTRADICTS = (0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9)
DEFAULTS = {"t_point": 0.5, "t_close": 0.25, "t_contradict": 0.5}


def _acceptable_correct(case: dict[str, Any]) -> bool:
    return case["expected_kind"] == "guess_correct" or "guess_correct" in case.get("accept_kinds", [])


def judgements(results: dict[str, Any]) -> dict[str, dict[str, dict[str, Any]]]:
    """Return {method: {case_id: judgement}} from the pattern rows that ran each method."""
    found: dict[str, dict[str, dict[str, Any]]] = {}
    for method, pattern in METHOD_ROWS.items():
        rows = results["rows"].get(pattern, [])
        found[method] = {
            row["case_id"]: judgement for row in rows
            if (judgement := (row["record"].get("judgements") or {}).get(method))
        }
    return found


def staged_items(results: dict[str, Any], method: str) -> list[dict[str, Any]]:
    """Return cases whose staged judgement reached stage B, with the path to recompute."""
    cases = {case["id"]: case for case in results["cases"]}
    items = []
    for case_id, judgement in judgements(results)[method].items():
        debug = judgement.get("debug") or {}
        probabilities = debug.get("probabilities") or {}
        points = probabilities.get("B")
        if not points:
            continue
        kind = judgement.get("kind")
        all_default = all(v["hit"] >= DEFAULTS["t_point"] for v in points.values())
        # 段 B に来た経路: 推理（guess）か、はい / いいえ質問（q_yesno）か。
        if debug.get("major") == "guess" or kind == "guess_wrong" or (
                kind == "guess_close" and not all_default):
            path = "guess"
        elif debug.get("guess_demoted") and kind in {"guess_close", "guess_wrong"}:
            path = "guess"
        else:
            path = "q_yesno"
        items.append({
            "id": case_id, "no": cases[case_id]["no"], "text": cases[case_id]["text"],
            "expected_kind": cases[case_id]["expected_kind"],
            "acceptable_correct": _acceptable_correct(cases[case_id]),
            "kind": kind, "path": path, "points": points,
            "b2": probabilities.get("B2"),
        })
    return items


def declared(item: dict[str, Any], t_point: float, t_contradict: float) -> bool | None:
    """True / False for a correct declaration, or None when stage B2 was never asked."""
    if not all(v["hit"] >= t_point for v in item["points"].values()):
        return False
    if item["b2"] is None:
        return None
    return item["b2"] < t_contradict


def point_sweep(items: list[dict[str, Any]], total_correct: int,
                t_contradict: float = DEFAULTS["t_contradict"]) -> list[dict[str, Any]]:
    """Correct declarations per T_POINT (P2 = wrong declarations, P5 = rate over label ④)."""
    table = []
    for t_point in T_POINTS:
        outcomes = [(x, declared(x, t_point, t_contradict)) for x in items]
        yes = [x for x, d in outcomes if d]
        true = sum(x["expected_kind"] == "guess_correct" for x in yes)
        table.append({
            "t_point": t_point,
            "wrong_correct": sum(not x["acceptable_correct"] for x in yes),
            "true_declared": true, "total_correct": total_correct,
            "p5": true / total_correct if total_correct else None,
            "b2_missing": sum(d is None for _, d in outcomes),
            "wrong_ids": sorted(x["id"] for x in yes if not x["acceptable_correct"]),
        })
    return table


def contradict_sweep(items: list[dict[str, Any]], total_correct: int,
                     t_point: float = DEFAULTS["t_point"]) -> list[dict[str, Any]]:
    """Correct declarations per T_CONTRADICT at the default T_POINT."""
    table = []
    for t_contradict in T_CONTRADICTS:
        yes = [x for x in items if declared(x, t_point, t_contradict)]
        true = sum(x["expected_kind"] == "guess_correct" for x in yes)
        table.append({
            "t_contradict": t_contradict,
            "wrong_correct": sum(not x["acceptable_correct"] for x in yes),
            "true_declared": true, "total_correct": total_correct,
            "p5": true / total_correct if total_correct else None,
        })
    return table


def close_sweep(items: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Split guess-path cases (not all points hit at the default) into ⑤ / ⑥ per T_CLOSE.

    段 A1b の格下げ（コアに触れない推理を質問へ戻す）も T_CLOSE を使うが、格下げ後の段 A2 は
    再計算できないので含めない。
    """
    pool = [x for x in items if x["path"] == "guess"
            and not all(v["hit"] >= DEFAULTS["t_point"] for v in x["points"].values())
            and x["expected_kind"] in {"guess_close", "guess_wrong"}]
    table = []
    for t_close in T_CLOSES:
        close = [x for x in pool if max(v["close"] for v in x["points"].values()) >= t_close]
        table.append({
            "t_close": t_close, "pool": len(pool),
            "close_label_close": sum(x["expected_kind"] == "guess_close" for x in close),
            "close_as_wrong": sum(x["expected_kind"] == "guess_close" and x not in close for x in pool),
            "wrong_as_close": sum(x["expected_kind"] == "guess_wrong" for x in close),
            "label_close": sum(x["expected_kind"] == "guess_close" for x in pool),
            "label_wrong": sum(x["expected_kind"] == "guess_wrong" for x in pool),
        })
    return table


def consensus(results: dict[str, Any]) -> list[dict[str, Any]]:
    """P2 / P5 when a correct declaration needs every method in the combination to agree."""
    found = judgements(results)
    cases = results["cases"]
    total_correct = sum(case["expected_kind"] == "guess_correct" for case in cases)
    methods = [m for m in METHOD_ROWS if found[m]]
    table = []
    for size in range(1, len(methods) + 1):
        for combo in itertools.combinations(methods, size):
            yes, split = [], 0
            for case in cases:
                votes = [(found[m].get(case["id"]) or {}).get("kind") == "guess_correct" for m in combo]
                if all(votes):
                    yes.append(case)
                elif any(votes):
                    split += 1
            true = sum(case["expected_kind"] == "guess_correct" for case in yes)
            table.append({
                "combo": "+".join(combo),
                "wrong_correct": sum(not _acceptable_correct(case) for case in yes),
                "true_declared": true, "total_correct": total_correct,
                "p5": true / total_correct if total_correct else None,
                "split": split,
                "wrong_ids": sorted(case["id"] for case in yes if not _acceptable_correct(case)),
            })
    return table


def fill_b2(items: list[dict[str, Any]], method: str, cache: dict[str, float],
            workers: int) -> None:
    """Ask stage B2 for cases that become candidates at the lowest T_POINT."""
    from app.judge import decisions, jev  # noqa: PLC0415
    from tools.local_trial import _load_stock_problem  # noqa: PLC0415

    todo = [x for x in items if x["b2"] is None and x["id"] not in cache
            and declared(x, min(T_POINTS), DEFAULTS["t_contradict"]) is None]
    if todo:
        key_name = "TYPESAFE_API_KEY" if method == "jev" else "OPENAI_API_KEY"
        api_key = os.environ.get(key_name, "")
        if not api_key:
            raise SystemExit(f"missing {key_name}")
        problems = {no: _load_stock_problem(no) for no in {x["no"] for x in todo}}

        def ask(item: dict[str, Any]) -> float:
            state = jev.contradiction_state(problems[item["no"]], item["text"])
            questions = {"contradict": jev.CONTRADICTION_QUESTION}
            if method == "jev":
                debug = {"input_tokens": 0, "output_tokens": 0, "latency_s": 0.0, "calls": 0}
                answers = jev._record_call(api_key, state, questions, debug)
            else:
                debug = {"input_tokens": 0, "output_tokens": 0, "latency_s": 0.0, "calls": 0,
                         "confidence": {}, "refusals": {"count": 0, "names": []}}
                answers = decisions._record_call(api_key, state, questions, debug, "B2")
            return jev._noul_true(answers["contradict"])

        with ThreadPoolExecutor(max_workers=workers) as pool:
            for item, value in zip(todo, pool.map(ask, todo)):
                cache[item["id"]] = value
    for item in items:
        if item["b2"] is None and item["id"] in cache:
            item["b2"] = cache[item["id"]]


def _pct(value: float | None) -> str:
    return "—" if value is None else f"{value:.1%}"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--probe", type=Path, required=True, help="directory with results.json")
    parser.add_argument("--fill-b2", action="store_true",
                        help="call stage B2 for cases that only become candidates at a lower T_POINT")
    parser.add_argument("--workers", type=int, default=4)
    args = parser.parse_args(argv)
    results = json.loads((args.probe / "results.json").read_text(encoding="utf-8"))
    total_correct = sum(case["expected_kind"] == "guess_correct" for case in results["cases"])
    cache_path = args.probe / "sweep_b2_cache.json"
    cache = json.loads(cache_path.read_text(encoding="utf-8")) if cache_path.is_file() else {}
    report: dict[str, Any] = {"total_cases": len(results["cases"]), "total_correct": total_correct}
    for method in STAGED:
        items = staged_items(results, method)
        if not items:
            continue
        method_cache = cache.setdefault(method, {})
        if args.fill_b2:
            fill_b2(items, method, method_cache, args.workers)
        else:
            for item in items:
                if item["b2"] is None and item["id"] in method_cache:
                    item["b2"] = method_cache[item["id"]]
        report[method] = {
            "stage_b_cases": len(items),
            "t_point": point_sweep(items, total_correct),
            "t_contradict": contradict_sweep(items, total_correct),
            "t_close": close_sweep(items),
        }
    report["consensus"] = consensus(results)
    cache_path.write_text(json.dumps(cache, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (args.probe / "sweep.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n",
                                          encoding="utf-8")

    print(f"cases={report['total_cases']} label④={total_correct}")
    for method in STAGED:
        if method not in report:
            continue
        data = report[method]
        print(f"\n## {method}（段 B に来たケース {data['stage_b_cases']}）")
        print("T_POINT | 誤った正解宣言 | 正解推理の宣言 | P5 | B2 未取得")
        for row in data["t_point"]:
            print(f"{row['t_point']:.1f} | {row['wrong_correct']} | {row['true_declared']}/"
                  f"{row['total_correct']} | {_pct(row['p5'])} | {row['b2_missing']}")
        print("T_CONTRADICT | 誤った正解宣言 | 正解推理の宣言 | P5")
        for row in data["t_contradict"]:
            print(f"{row['t_contradict']:.1f} | {row['wrong_correct']} | {row['true_declared']}/"
                  f"{row['total_correct']} | {_pct(row['p5'])}")
        print("T_CLOSE | ⑤ を ⑤ | ⑤ を ⑥ に落とす | ⑥ を ⑤ に上げる | 母数（⑤ / ⑥）")
        for row in data["t_close"]:
            print(f"{row['t_close']:.2f} | {row['close_label_close']} | {row['close_as_wrong']} | "
                  f"{row['wrong_as_close']} | {row['label_close']} / {row['label_wrong']}")
    print("\n## 合意ルール（組み合わせの全方式が ④ のときだけ正解宣言）")
    print("組み合わせ | P2 誤った正解宣言 | 正解推理の宣言 | P5 | 割れ")
    for row in report["consensus"]:
        print(f"{row['combo']} | {row['wrong_correct']} | {row['true_declared']}/{row['total_correct']} | "
              f"{_pct(row['p5'])} | {row['split']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
