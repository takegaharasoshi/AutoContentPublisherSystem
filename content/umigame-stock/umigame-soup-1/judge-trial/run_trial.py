"""21-6b 判定モジュールの試走 CLI。"""

from __future__ import annotations

import argparse
import ast
import json
import math
import statistics
import sys
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Any

import pattern1_luna
import pattern2_jev
import templates
from judge_contract import HERE, KINDS, JudgeResult, Problem, load_problem


DATA_DIR = HERE / "data"
WORK_DIR = HERE / "work"
CACHE_PATH = WORK_DIR / "trial_results.json"
REPORT_PATH = WORK_DIR / "trial_report.md"
EVAL_PATH = DATA_DIR / "eval_problems.json"
COMMON_PATH = DATA_DIR / "common_cases.json"
CORE_PATH = HERE.parent / "batch-01" / "leak_count.py"
GUESS_KINDS = {"guess_correct", "guess_close", "guess_wrong"}
QUESTION_KINDS = {"q_yesno", "q_multi", "q_open"}
RESTRICTED_KINDS = {"troll", "abuse", "spam", "personal_info"}
GROUPS = {
    "質問系 ①〜③": QUESTION_KINDS,
    "推理系 ④〜⑥": GUESS_KINDS,
    "その他 ⑦〜㉒": set(KINDS) - QUESTION_KINDS - GUESS_KINDS,
}



# 金額の試算に使う単価（USD / 100 万トークン）。luna は公開情報（2026-09-27 時点）で、請求画面での確認が必要。
# luna の推論トークンは出力として課金される前提。Jev は出力無料（アイデア記録 umigame-yesno-jev.md）。
PRICE_USD_PER_M = {"luna_input": 0.10, "luna_output": 0.50, "jev_input": 0.042}
USD_JPY = 150  # 円換算の仮レート
MONTHLY_COMMENTS = 6000  # 月あたりのコメント数の見込み（アイデア記録の試算と同じ）


def _cost(total_usd: float, count: int) -> dict:
    per = total_usd / count if count else 0.0
    return {"total_usd": total_usd, "per_comment_usd": per, "monthly_usd": per * MONTHLY_COMMENTS}


def _format_cost(method: str, cost: dict) -> str:
    return (
        f"{method} 金額（試算）: 合計 ${cost['total_usd']:.4f} / 1 件あたり ${cost['per_comment_usd']:.6f}"
        f" / 月 {MONTHLY_COMMENTS:,} 件で ${cost['monthly_usd']:.3f}（約 {cost['monthly_usd'] * USD_JPY:.0f} 円）"
    )


RELEVANCE_WORDS = ("関係", "重要", "大事")


def answer_matches(row: dict) -> bool:
    """期待判定と実判定が一致するか（「〜は関係ある？」への「いいえ」は「関係ありません」と同義に扱う）。

    batch-01/probe_test.py の ``judge`` と同じ同義の扱い（セット別設計書 5.1 の 21-4a 知見）。
    """
    if row["expected_answer"] == row["answer"]:
        return True
    return (
        row["expected_answer"] == "irrelevant"
        and row["answer"] == "no"
        and any(word in row.get("comment_text", "") for word in RELEVANCE_WORDS)
    )


def load_core_words(path: Path = CORE_PATH) -> dict[str, list[str]]:
    """leak_count.py の CORE を AST で取り出す。対象ファイルは実行しない。"""
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    for node in tree.body:
        if isinstance(node, (ast.Assign, ast.AnnAssign)):
            targets = node.targets if isinstance(node, ast.Assign) else [node.target]
            if any(isinstance(target, ast.Name) and target.id == "CORE" for target in targets):
                value = ast.literal_eval(node.value)
                if not isinstance(value, dict):
                    break
                return {str(no): list(words) for no, words in value.items()}
    raise ValueError(f"{path} にリテラルの CORE 定義がありません")


def _read_json(path: Path, description: str) -> Any:
    if not path.is_file():
        raise FileNotFoundError(f"{description} がありません: {path}")
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ValueError(f"{path} の JSON が不正です: {exc}") from exc


def load_cases(only: list[str] | None = None) -> list[dict[str, Any]]:
    """評価ケースと共通ケースを読み込み、共通ケースを問題へ順番に割り当てる。"""
    problems = _read_json(EVAL_PATH, "評価問題一覧 data/eval_problems.json")
    common = _read_json(COMMON_PATH, "共通ケース data/common_cases.json")
    if not isinstance(problems, dict) or not problems:
        raise ValueError(f"{EVAL_PATH} は問題番号をキーにしたオブジェクトで指定してください")
    if not isinstance(common, list):
        raise ValueError(f"{COMMON_PATH} はケース配列で指定してください")

    available = [str(no) for no in problems]
    if only:
        wanted = set(only)
        unknown = [no for no in only if no not in available]
        if unknown:
            raise ValueError(f"--only の問題が {EVAL_PATH} にありません: {', '.join(unknown)}")
        selected = [no for no in available if no in wanted]
    else:
        selected = available
    if not selected:
        raise ValueError("試走対象の問題がありません")

    cases: list[dict[str, Any]] = []
    for no in selected:
        items = problems[no]
        if not isinstance(items, list):
            raise ValueError(f"{EVAL_PATH} の {no} はケース配列で指定してください")
        for entry in items:
            cases.append(_normalize_case(entry, no, source="eval"))
    for index, entry in enumerate(common):
        no = selected[index % len(selected)]
        cases.append(_normalize_case(entry, no, source="common"))

    seen: set[str] = set()
    for case in cases:
        case_id = case["id"]
        if case_id in seen:
            raise ValueError(f"ケース id は全体で一意にしてください: {case_id}")
        seen.add(case_id)
    return cases


def _normalize_case(entry: Any, no: str, *, source: str) -> dict[str, Any]:
    if not isinstance(entry, dict):
        raise ValueError(f"{source} ケースはオブジェクトで指定してください: {entry!r}")
    required = {"id", "text", "kind"}
    missing = required - entry.keys()
    if missing:
        raise ValueError(f"{source} ケースに必須項目がありません: {', '.join(sorted(missing))}")
    kind = entry["kind"]
    if kind not in KINDS:
        raise ValueError(f"ケース {entry['id']} の kind が不正です: {kind}")
    answer = entry.get("answer")
    if kind == "q_yesno" and answer not in {"yes", "no", "irrelevant"}:
        raise ValueError(f"q_yesno ケース {entry['id']} の answer は yes/no/irrelevant が必要です")
    return {
        "id": str(entry["id"]),
        "no": str(no),
        "comment_text": str(entry["text"]),
        "expected_kind": kind,
        "expected_answer": answer,
        "source": source,
    }


def _row_from_result(case: dict[str, Any], result: JudgeResult, problem: Problem) -> dict[str, Any]:
    return {
        **case,
        "problem_text": problem.problem_text,
        "kind": result.kind,
        "answer": result.answer,
        "reply": result.reply,
        "method": result.method,
        "debug": result.debug,
    }


def _cache_key(case_id: str, method: str) -> str:
    return f"{case_id}::{method}"


def _error_row(case: dict[str, Any], method: str, problem: Problem, exc: Exception) -> dict[str, Any]:
    return {
        **case,
        "problem_text": problem.problem_text,
        "kind": "error",
        "answer": None,
        "reply": None,
        "method": method,
        "debug": {"error": str(exc)},
    }


def _run_one(
    case: dict[str, Any],
    method: str,
    problem: Problem,
    api_keys: dict[str, str],
    options: dict[str, Any],
) -> dict[str, Any]:
    try:
        if method == "p1":
            result = pattern1_luna.judge(
                case["id"],
                case["comment_text"],
                problem,
                api_key=api_keys["p1"],
                model=options["model"],
                effort=options["effort"],
                max_tokens=options["max_tokens"],
            )
        else:
            result = pattern2_jev.judge(
                case["id"],
                case["comment_text"],
                problem,
                api_key=api_keys["p2"],
                t_point=options["t_point"],
                t_close=options["t_close"],
                t_quality=options["t_quality"],
                t_answer=options["t_answer"],
            )
        return _row_from_result(case, result, problem)
    except Exception as exc:  # noqa: BLE001 - 他ケースを止めずに失敗を保存
        return _error_row(case, method, problem, exc)


def _is_correct_declaration(reply: str | None) -> bool:
    return bool(reply and reply.startswith("正解です"))


def _is_judgment_opener(reply: str | None) -> bool:
    return bool(reply and reply.startswith(("はい", "いいえ", "関係", "正解")))


def _accuracy(correct: int, total: int) -> dict[str, Any]:
    return {"correct": correct, "total": total, "rate": correct / total if total else None}


def _median_p95_max(values: list[float]) -> dict[str, float | None]:
    if not values:
        return {"median": None, "p95": None, "max": None}
    ordered = sorted(values)
    return {
        "median": statistics.median(ordered),
        "p95": ordered[max(0, math.ceil(0.95 * len(ordered)) - 1)],
        "max": max(ordered),
    }


def aggregate_results(
    results: list[dict[str, Any]], core: dict[str, list[str]] | None = None
) -> dict[str, Any]:
    """一方式分の一致率・運用品質メトリクスを計算する。"""
    core = load_core_words() if core is None else core
    total = len(results)
    matches = [row for row in results if row["expected_kind"] == row["kind"]]
    by_kind: dict[str, dict[str, Any]] = {}
    for kind in KINDS:
        expected = [row for row in results if row["expected_kind"] == kind]
        by_kind[kind] = _accuracy(sum(row["kind"] == kind for row in expected), len(expected))
    groups = {
        name: _accuracy(
            sum(row["expected_kind"] == row["kind"] for row in results if row["expected_kind"] in kinds),
            sum(row["expected_kind"] in kinds for row in results),
        )
        for name, kinds in GROUPS.items()
    }
    error_counts = Counter(
        (row["expected_kind"], row["kind"])
        for row in results
        if row["expected_kind"] != row["kind"]
    )
    top_errors = [
        {"expected": expected, "actual": actual, "count": count}
        for (expected, actual), count in error_counts.most_common(10)
    ]

    q_cases = [row for row in results if row["expected_kind"] == "q_yesno"]
    q_correct = sum(
        row["kind"] == "q_yesno" and answer_matches(row) for row in q_cases
    )
    p3_cases = [row for row in q_cases if row["expected_answer"] in {"yes", "no"}]
    p3 = sum(
        row["kind"] == "q_yesno"
        and row["answer"] in {"yes", "no"}
        and row["answer"] != row["expected_answer"]
        for row in p3_cases
    )
    p4_values = {"no", "irrelevant", "unknown"}
    p4_cases = [row for row in q_cases if row["expected_answer"] in p4_values]
    p4 = sum(
        row["kind"] == "q_yesno"
        and row["answer"] in p4_values
        and not answer_matches(row)
        for row in p4_cases
    )

    wrong_correct_declarations = sum(
        row["expected_kind"] != "guess_correct"
        and bool(row["reply"] and row["reply"].startswith("正解です"))
        for row in results
    )
    correct_expectations = [row for row in results if row["expected_kind"] == "guess_correct"]
    correct_declarations = sum(_is_correct_declaration(row["reply"]) for row in correct_expectations)

    restricted_expected = [row for row in results if row["expected_kind"] in RESTRICTED_KINDS]
    restricted_judgment = sum(_is_judgment_opener(row["reply"]) for row in restricted_expected)
    troll_abuse = [row for row in results if row["expected_kind"] in {"troll", "abuse"}]
    troll_abuse_template = sum(
        row["reply"] == templates.pick(row["expected_kind"], row["id"]) for row in troll_abuse
    )
    no_reply_expected = [row for row in results if row["expected_kind"] in templates.NO_REPLY_KINDS]
    no_reply_sent = sum(bool(row["reply"]) for row in no_reply_expected)
    ordinary = [row for row in results if row["expected_kind"] not in RESTRICTED_KINDS]
    ordinary_restricted = sum(row["kind"] in RESTRICTED_KINDS for row in ordinary)

    too_long = [row for row in results if row["reply"] is not None and len(row["reply"]) > 80]
    phrasing: dict[str, dict[str, Any]] = {}
    for kind in KINDS:
        cases = [row for row in results if row["expected_kind"] == kind]
        if len(cases) >= 5:
            counts = Counter(row["reply"] if row["reply"] is not None else "<NO_REPLY>" for row in cases)
            phrase, count = min(counts.items(), key=lambda entry: (-entry[1], entry[0]))
            phrasing[kind] = {"phrase": phrase, "count": count, "total": len(cases), "rate": count / len(cases)}

    leaks = []
    for row in results:
        reply = row["reply"]
        if row["kind"] == "guess_correct" or not reply:
            continue
        if reply.startswith("正解です"):
            continue
        words = [word for word in core.get(row["no"], []) if word in reply and word not in row["comment_text"]]
        if words:
            leaks.append({"id": row["id"], "no": row["no"], "words": words, "reply": reply})

    errors = []
    for row in results:
        kind_wrong = row["expected_kind"] != row["kind"]
        answer_wrong = (
            row["expected_kind"] == "q_yesno"
            and row["kind"] == "q_yesno"
            and not answer_matches(row)
        )
        if kind_wrong or answer_wrong:
            errors.append(row)

    method = results[0]["method"] if results else ""
    result: dict[str, Any] = {
        "method": method,
        "kind": {
            "total": total,
            "correct": len(matches),
            "rate": len(matches) / total if total else None,
            "groups": groups,
            "by_kind": by_kind,
            "top_errors": top_errors,
        },
        "q_yesno": {
            "accuracy": _accuracy(q_correct, len(q_cases)),
            "p3_yes_no_confusions": _accuracy(p3, len(p3_cases)),
            "p4_no_irrelevant_unknown_drift": _accuracy(p4, len(p4_cases)),
        },
        "p2_wrong_correct_declarations": wrong_correct_declarations,
        "p5_correct_declaration_rate": _accuracy(correct_declarations, len(correct_expectations)),
        "p6": {
            "restricted_judgment_openers": restricted_judgment,
            "troll_abuse_template_rate": _accuracy(troll_abuse_template, len(troll_abuse)),
            "spam_personal_info_replied": no_reply_sent,
            "ordinary_as_restricted_rate": _accuracy(ordinary_restricted, len(ordinary)),
        },
        "p7_over_80_chars": len(too_long),
        "phrasing": phrasing,
        "leaks": leaks,
        "errors": errors,
    }

    if method == "p1":
        latencies = [float(row.get("debug", {}).get("latency_s", 0) or 0) for row in results]
        completion = [int(row.get("debug", {}).get("completion_tokens", 0) or 0) for row in results]
        reasoning = [int(row.get("debug", {}).get("reasoning_tokens", 0) or 0) for row in results]
        prompt = [int(row.get("debug", {}).get("prompt_tokens", 0) or 0) for row in results]
        cost_p1 = (sum(prompt) * PRICE_USD_PER_M["luna_input"] + sum(completion) * PRICE_USD_PER_M["luna_output"]) / 1e6
        result["p1"] = {
            "finish_length": sum(row.get("debug", {}).get("finish_reason") == "length" for row in results),
            "errors": sum(row["kind"] == "error" for row in results),
            "latency_s": _median_p95_max(latencies),
            "completion_tokens": {"max": max(completion, default=0), "average": statistics.mean(completion) if completion else 0},
            "reasoning_tokens": {"max": max(reasoning, default=0), "average": statistics.mean(reasoning) if reasoning else 0},
            "prompt_tokens": sum(prompt),
            "cost": _cost(cost_p1, len(results)),
        }
    elif method == "p2":
        latencies = [float(row.get("debug", {}).get("latency_s", 0) or 0) for row in results]
        result["p2"] = {
            "input_tokens": sum(int(row.get("debug", {}).get("input_tokens", 0) or 0) for row in results),
            "cost": _cost(
                sum(int(row.get("debug", {}).get("input_tokens", 0) or 0) for row in results)
                * PRICE_USD_PER_M["jev_input"] / 1e6,
                len(results),
            ),
            "latency_s": {
                "median": statistics.median(latencies) if latencies else None,
                "max": max(latencies) if latencies else None,
            },
        }
    return result


def _format_rate(value: dict[str, Any]) -> str:
    rate = value["rate"]
    return f"{value['correct']}/{value['total']} ({rate:.1%})" if rate is not None else "0/0 (対象なし)"


def summary_lines(metrics: dict[str, Any]) -> list[str]:
    """標準出力と Markdown レポートで共用する集計文。"""
    kind = metrics["kind"]
    lines = [f"種別ラベル一致率: {kind['correct']}/{kind['total']} ({kind['rate']:.1%})" if kind["total"] else "種別ラベル一致率: 0/0 (対象なし)"]
    for name, value in kind["groups"].items():
        lines.append(f"  {name}: {_format_rate(value)}")
    lines.append("種別ごとの一致数 / 件数:")
    for code, value in kind["by_kind"].items():
        if value["total"]:
            lines.append(f"  {code}: {value['correct']}/{value['total']}")
    lines.append("誤りの内訳 (期待 → 実際、上位):")
    if kind["top_errors"]:
        lines.extend(f"  {row['expected']} → {row['actual']}: {row['count']}" for row in kind["top_errors"])
    else:
        lines.append("  なし")
    q = metrics["q_yesno"]
    lines.extend(
        [
            f"q_yesno 判定一致率: {_format_rate(q['accuracy'])}",
            f"P3 はい/いいえ取り違え: {_format_rate(q['p3_yes_no_confusions'])}",
            f"P4 いいえ/関係ありません/unknown の揺れ: {_format_rate(q['p4_no_irrelevant_unknown_drift'])}",
            f"P2 誤った正解宣言: {metrics['p2_wrong_correct_declarations']} 件",
            f"P5 正解宣言率: {_format_rate(metrics['p5_correct_declaration_rate'])}",
            f"P6 ⑱〜㉑で判定語始まり: {metrics['p6']['restricted_judgment_openers']} 件",
            f"P6 ⑱⑲ 定型返信率: {_format_rate(metrics['p6']['troll_abuse_template_rate'])}",
            f"P6 ⑳㉑ 返信件数: {metrics['p6']['spam_personal_info_replied']} 件",
            f"P6 通常コメントを⑱〜㉑と判定: {_format_rate(metrics['p6']['ordinary_as_restricted_rate'])}",
            f"P7 80 字超の返信: {metrics['p7_over_80_chars']} 件",
        ]
    )
    if metrics["phrasing"]:
        lines.append("言い回し (種別ごとの最頻返信文占有率、5 件以上):")
        for code, value in metrics["phrasing"].items():
            lines.append(f"  {code}: {value['count']}/{value['total']} ({value['rate']:.1%}) {value['phrase']}")
    if metrics["method"] == "p1":
        if metrics["leaks"]:
            lines.append(f"P1 漏れ候補: {len(metrics['leaks'])} 件")
            lines.extend(
                f"  {row['id']} ({row['no']}) 語={','.join(row['words'])} 返信={row['reply']}"
                for row in metrics["leaks"]
            )
        else:
            lines.append("P1 漏れ候補: 0 件")
    if "p1" in metrics:
        p1 = metrics["p1"]
        latency = p1["latency_s"]
        lines.extend(
            [
                f"p1 finish_reason=length: {p1['finish_length']} 件",
                f"p1 error: {p1['errors']} 件",
                f"p1 latency 秒 中央値 / p95 / 最大: {latency['median']:.3f} / {latency['p95']:.3f} / {latency['max']:.3f}" if latency["median"] is not None else "p1 latency 秒: 対象なし",
                f"p1 completion_tokens 最大 / 平均: {p1['completion_tokens']['max']} / {p1['completion_tokens']['average']:.1f}",
                f"p1 reasoning_tokens 最大 / 平均: {p1['reasoning_tokens']['max']} / {p1['reasoning_tokens']['average']:.1f}",
                f"p1 prompt_tokens 合計: {p1['prompt_tokens']}",
                _format_cost("p1", p1["cost"]),
            ]
        )
    if "p2" in metrics:
        p2 = metrics["p2"]
        latency = p2["latency_s"]
        lines.extend(
            [
                f"p2 Jev 総 input_tokens: {p2['input_tokens']}",
                _format_cost("p2", p2["cost"]),
                f"p2 1 コメント latency 秒 中央値 / 最大: {latency['median']:.3f} / {latency['max']:.3f}" if latency["median"] is not None else "p2 latency 秒: 対象なし",
            ]
        )
    return lines


def _case_error_lines(errors: list[dict[str, Any]]) -> list[str]:
    if not errors:
        return ["誤りケース: なし"]
    lines = [f"誤りケース: {len(errors)} 件"]
    for row in errors:
        expected = row["expected_kind"]
        if expected == "q_yesno":
            expected += f" / {row['expected_answer']}"
        actual = row["kind"]
        if row["kind"] == "q_yesno":
            actual += f" / {row['answer']}"
        lines.append(
            "  "
            + " | ".join(
                [
                    f"id={row['id']}",
                    f"problem={row['problem_text']}",
                    f"comment={row['comment_text']}",
                    f"expected={expected}",
                    f"actual={actual}",
                    f"reply={row['reply'] if row['reply'] is not None else '<NO_REPLY>'}",
                ]
            )
        )
    return lines


def _load_cache() -> dict[str, dict[str, Any]]:
    if not CACHE_PATH.is_file():
        return {}
    cache = _read_json(CACHE_PATH, "試走キャッシュ")
    if not isinstance(cache, dict) or not isinstance(cache.get("results"), dict):
        raise ValueError(f"{CACHE_PATH} の形式が不正です")
    return cache["results"]


def _save_cache(results: dict[str, dict[str, Any]]) -> None:
    WORK_DIR.mkdir(parents=True, exist_ok=True)
    temp = CACHE_PATH.with_suffix(".json.tmp")
    temp.write_text(json.dumps({"version": 1, "results": results}, ensure_ascii=False, indent=2), encoding="utf-8")
    temp.replace(CACHE_PATH)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="21-6b 判定モジュールを評価データで試走します")
    parser.add_argument("--methods", nargs="+", choices=("p1", "p2"), default=("p1", "p2"))
    parser.add_argument("--only", nargs="+", metavar="NO", help="試走する問題番号 (例: U01 U12)")
    parser.add_argument("--workers", type=int, default=6)
    parser.add_argument("--from-cache", action="store_true", help="API を呼ばずキャッシュ済み結果だけで集計")
    parser.add_argument("--t-point", type=float, default=pattern2_jev.T_POINT)
    parser.add_argument("--t-close", type=float, default=pattern2_jev.T_CLOSE)
    parser.add_argument("--t-quality", type=float, default=pattern2_jev.T_QUALITY)
    parser.add_argument("--t-answer", type=float, default=pattern2_jev.T_ANSWER)
    parser.add_argument("--model", default="gpt-6-luna")
    parser.add_argument("--effort", default="xhigh")
    parser.add_argument("--max-tokens", type=int, default=1200)
    parser.add_argument("--secret-id", default=pattern1_luna.DEFAULT_SECRET_ID)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.workers < 1:
        raise SystemExit("--workers は 1 以上を指定してください")
    cases = load_cases(args.only)
    nos = list(dict.fromkeys(case["no"] for case in cases))
    problems = {no: load_problem(no) for no in nos}
    cache_results = _load_cache()
    methods = list(dict.fromkeys(args.methods))
    selected_keys = {
        _cache_key(case["id"], method)
        for case in cases
        for method in methods
    }

    if args.from_cache:
        missing = sorted(selected_keys - cache_results.keys())
        if missing:
            raise FileNotFoundError(
                f"--from-cache で必要な結果がありません: {', '.join(missing[:12])}"
            )
    else:
        api_keys: dict[str, str] = {}
        if "p1" in methods:
            api_keys["p1"] = pattern1_luna.load_api_key(args.secret_id)
        if "p2" in methods:
            import os

            api_keys["p2"] = os.environ.get("TYPESAFE_API_KEY", "")
            if not api_keys["p2"]:
                raise SystemExit("TYPESAFE_API_KEY がありません（例: bash -ic 'python run_trial.py ...'）")
        options = {
            "model": args.model,
            "effort": args.effort,
            "max_tokens": args.max_tokens,
            "t_point": args.t_point,
            "t_close": args.t_close,
            "t_quality": args.t_quality,
            "t_answer": args.t_answer,
        }
        jobs = [(case, method) for case in cases for method in methods]
        with ThreadPoolExecutor(max_workers=args.workers) as pool:
            futures = {
                pool.submit(_run_one, case, method, problems[case["no"]], api_keys, options): (case, method)
                for case, method in jobs
            }
            for future in as_completed(futures):
                case, method = futures[future]
                key = _cache_key(case["id"], method)
                cache_results[key] = future.result()
        _save_cache(cache_results)

    WORK_DIR.mkdir(parents=True, exist_ok=True)
    report_lines = ["# 21-6b 判定試走レポート", ""]
    for method in methods:
        rows = [cache_results[_cache_key(case["id"], method)] for case in cases]
        metrics = aggregate_results(rows)
        heading = f"方式 {method} ({len(rows)} ケース)"
        print(heading)
        print("\n".join(summary_lines(metrics)))
        print("\n".join(_case_error_lines(metrics["errors"])))
        report_lines.extend([f"## {heading}", ""])
        report_lines.extend(f"- {line}" for line in summary_lines(metrics))
        report_lines.append("")
        report_lines.append("### 誤りケース")
        report_lines.append("")
        report_lines.extend(f"- {line.strip()}" for line in _case_error_lines(metrics["errors"]))
        report_lines.append("")
    REPORT_PATH.write_text("\n".join(report_lines), encoding="utf-8")
    print(f"キャッシュ: {CACHE_PATH}")
    print(f"レポート: {REPORT_PATH}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (FileNotFoundError, ValueError, RuntimeError) as exc:
        print(f"エラー: {exc}", file=sys.stderr)
        raise SystemExit(2) from exc
