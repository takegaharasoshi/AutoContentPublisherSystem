"""Sweep the Jev stage-B2 contradiction threshold over a cached probe run (21-6d3c).

段 B が ④ の候補（Jev の判定 = guess_correct）になったケースだけに段 B2 の問いを投げ、
閾値ごとに「誤った正解宣言（正解ラベルが ④ 以外）」と「本物の正解推理を ⑤ に落とした件数」を数える。
判定レベルの集計（返信文の冒頭語で数える probe_metrics の P2 とは数え方が異なる）。
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import Any


SERVICE_DIR = Path(__file__).resolve().parent.parent
if str(SERVICE_DIR) not in sys.path:
    sys.path.insert(0, str(SERVICE_DIR))

from app.judge import jev  # noqa: E402
from tools.local_trial import _load_stock_problem  # noqa: E402


THRESHOLDS = (0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9)


def candidates(results: dict[str, Any]) -> list[dict[str, Any]]:
    """Return Jev guess_correct cases with labels and the hybrid luna kind."""
    cases = {case["id"]: case for case in results["cases"]}
    hybrid = {row["case_id"]: row for row in results["rows"].get("hybrid-1d", [])}
    found = []
    for row in results["rows"]["jev-2b"]:
        judgement = row["record"]["judgements"].get("jev") or {}
        if judgement.get("kind") != "guess_correct":
            continue
        case = cases[row["case_id"]]
        luna_kind = ((hybrid.get(row["case_id"]) or {}).get("record", {})
                     .get("judgements", {}).get("luna") or {}).get("kind")
        found.append({"id": case["id"], "no": case["no"], "text": case["text"],
                      "expected_kind": case["expected_kind"],
                      "points": judgement["debug"]["probabilities"].get("B", {}),
                      "luna_kind": luna_kind})
    return found


def ask(api_key: str, item: dict[str, Any], problem_cache: dict[str, Any]) -> float:
    debug = {"input_tokens": 0, "output_tokens": 0, "latency_s": 0.0, "calls": 0}
    problem = problem_cache[item["no"]]
    answers = jev._record_call(api_key, jev.contradiction_state(problem, item["text"]),
                               {"contradict": jev.CONTRADICTION_QUESTION}, debug)
    return jev._noul_true(answers["contradict"])


def sweep(items: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Count outcomes per threshold; None means the check is off (21-6d3 baseline)."""
    table = []
    for threshold in (None, *THRESHOLDS):
        demoted = [x for x in items if threshold is not None and x["contradiction"] >= threshold]
        kept = [x for x in items if x not in demoted]
        table.append({
            "threshold": threshold,
            "wrong_correct": sum(x["expected_kind"] != "guess_correct" for x in kept),
            "true_correct_demoted": sum(x["expected_kind"] == "guess_correct" for x in demoted),
            "true_correct_kept": sum(x["expected_kind"] == "guess_correct" for x in kept),
            # hybrid: luna が ④ で Jev も ④ のときだけ consensus_ok。Jev が落とすと consensus_split（保留）
            "hybrid_split": sum(x["luna_kind"] == "guess_correct" for x in demoted),
            "hybrid_split_true": sum(x["luna_kind"] == "guess_correct"
                                     and x["expected_kind"] == "guess_correct" for x in demoted),
            "hybrid_split_wrong": sum(x["luna_kind"] == "guess_correct"
                                      and x["expected_kind"] != "guess_correct" for x in demoted),
        })
    return table


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--probe", type=Path,
                        default=SERVICE_DIR / "work/probe/full-20261003")
    parser.add_argument("--workers", type=int, default=4)
    args = parser.parse_args(argv)
    if not 1 <= args.workers <= 4:
        parser.exit(2, "workers must be 1..4 (429 対策)\n")
    api_key = os.environ.get("TYPESAFE_API_KEY", "")
    out = args.probe / "contradiction_sweep.json"
    cached = (json.loads(out.read_text(encoding="utf-8")) if out.is_file() else {})
    results = json.loads((args.probe / "results.json").read_text(encoding="utf-8"))
    items = candidates(results)
    problems = {no: _load_stock_problem(no) for no in {x["no"] for x in items}}
    todo = [x for x in items if x["id"] not in cached.get("probabilities", {})]
    if todo and not api_key:
        parser.exit(2, "missing TYPESAFE_API_KEY\n")
    probabilities = dict(cached.get("probabilities", {}))
    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        for item, value in zip(todo, pool.map(lambda x: ask(api_key, x, problems), todo)):
            probabilities[item["id"]] = value
    for item in items:
        item["contradiction"] = probabilities[item["id"]]
    table = sweep(items)
    out.write_text(json.dumps({"probabilities": probabilities, "items": items, "table": table},
                              ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"candidates={len(items)} (label ④ {sum(x['expected_kind'] == 'guess_correct' for x in items)}"
          f" / other {sum(x['expected_kind'] != 'guess_correct' for x in items)})")
    print("id | label | luna | points | contradiction | text")
    for item in sorted(items, key=lambda x: (x["expected_kind"], -x["contradiction"])):
        points = "/".join(f"{v:.2f}" for v in item["points"].values())
        print(f"{item['id']} | {item['expected_kind']} | {item['luna_kind']} | {points} | "
              f"{item['contradiction']:.2f} | {item['text']}")
    print("threshold | wrong_correct | true_correct_demoted | hybrid_split (true / wrong)")
    for row in table:
        label = "off" if row["threshold"] is None else f"{row['threshold']:.1f}"
        print(f"{label} | {row['wrong_correct']} | {row['true_correct_demoted']} | "
              f"{row['hybrid_split']} ({row['hybrid_split_true']} / {row['hybrid_split_wrong']})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
