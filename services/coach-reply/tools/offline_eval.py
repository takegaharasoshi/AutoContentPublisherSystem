#!/usr/bin/env python3
"""Evaluate the judge against saved comments (calls the real Anthropic API)."""

from __future__ import annotations

import argparse
import json
import os
import sys
from collections import defaultdict
from dataclasses import replace
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path


sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app import judge  # noqa: E402
from app.config import JUDGE_EFFORTS, Config  # noqa: E402
from app.snapshot_store import snapshot_from_answer  # noqa: E402


REPO_ROOT = Path(__file__).resolve().parents[3]
DATA = REPO_ROOT / "poc/logic-training-reply-eval/data"
LABELS = ("correct", "alt", "wrong", "other", "unanswered")


REPLY_RULES = ("high", "any")
REVIEW_LABELS = ("wrong", "other", "unanswered")
# Haiku 5.5 (prompts up to 100K tokens), USD per million tokens. Cache write 1.25x, read 0.1x.
PRICE_PER_MTOK = {"input_tokens": 0.10, "cache_creation_input_tokens": 0.125,
                  "cache_read_input_tokens": 0.01, "output_tokens": 0.50}


def would_reply(prediction: dict | None, rule: str = "high") -> bool:
    """Apply a reply gate: "high" is the online gate, "any" also replies at low confidence."""
    if rule not in REPLY_RULES:
        raise ValueError(f"unknown reply rule: {rule}")
    if not prediction or prediction.get("verdict") != "correct":
        return False
    return rule == "any" or prediction.get("confidence") == "high"


def aggregate_results(rows: list[dict], rule: str = "high") -> dict:
    """Summarize labels, false replies, recall and failures without any API call."""
    table = {label: {"reply": 0, "no_reply": 0} for label in LABELS}
    false_replies = []
    review_replies = []
    failed = 0
    for row in rows:
        label = row["label"]
        if label not in table:
            raise ValueError(f"unknown evaluation label: {label}")
        prediction = row.get("prediction")
        reply = would_reply(prediction, rule)
        table[label]["reply" if reply else "no_reply"] += 1
        if prediction is None:
            failed += 1
        if reply and label in REVIEW_LABELS:
            item = {
                "label": label, "media_id": row["media_id"], "comment_id": row["comment_id"],
                "comment_text": row["comment_text"], "answer_text": row["answer_text"],
                "question_text": row.get("question_text"),
                "confidence": prediction["confidence"], "reason": prediction["reason"],
            }
            review_replies.append(item)
            if label in {"wrong", "other"}:
                false_replies.append(item)
    total_correct = sum(table["correct"].values())
    return {
        "rule": rule, "table": table,
        "false_reply_count": len(false_replies), "false_replies": false_replies,
        "review_replies": review_replies,
        "correct_replied": table["correct"]["reply"], "correct_total": total_correct,
        "correct_recall": table["correct"]["reply"] / total_correct if total_correct else None,
        "judge_failures": failed,
    }


def print_summary(summary: dict) -> None:
    """Print the evaluation table and each false reply with its short rationale."""
    print(f"返信の条件: {summary.get('rule', 'high')}")
    print("label        返す  返さない")
    for label, counts in summary["table"].items():
        print(f"{label:12} {counts['reply']:5} {counts['no_reply']:9}")
    print(f"誤返信(wrong・other への返す): {summary['false_reply_count']}")
    for row in summary["false_replies"]:
        print(json.dumps(row, ensure_ascii=False))
    recall = summary["correct_recall"]
    ratio = f"{recall:.1%}" if recall is not None else "N/A"
    print(f"正解の拾えた割合: {summary['correct_replied']}/{summary['correct_total']} ({ratio})")
    print(f"判定の失敗件数: {summary['judge_failures']}")


def total_usage(usage: list[dict]) -> dict:
    """Sum per-request token usage and estimate the Haiku 5.5 cost in USD."""
    totals = {key: sum(int(u.get(key, 0) or 0) for u in usage) for key in PRICE_PER_MTOK}
    cost = sum(totals[key] * price for key, price in PRICE_PER_MTOK.items()) / 1_000_000
    return {"requests": len(usage), **totals, "cost_usd": round(cost, 6)}


def print_usage(totals: dict, comments: int) -> None:
    """Print token totals and the estimated cost per comment."""
    print(f"リクエスト数: {totals['requests']}  入力: {totals['input_tokens']}"
          f"  キャッシュ書込: {totals['cache_creation_input_tokens']}"
          f"  キャッシュ読込: {totals['cache_read_input_tokens']}  出力: {totals['output_tokens']}")
    per = totals["cost_usd"] / comments if comments else 0.0
    print(f"費用の目安: ${totals['cost_usd']:.4f}（コメント 1 件あたり ${per:.6f}・"
          "Haiku 5.5 の単価〔入力 $0.10 / 出力 $0.50 / 100 万トークン〕で概算）")


def write_review(path: Path, rows: list[dict], effort: str | None) -> int:
    """Write a Markdown list of replies to wrong/other/unanswered labels for human review."""
    summary_any = aggregate_results(rows, "any")
    items = summary_any["review_replies"]
    lines = [f"# 運用者が返していないコメントへ「返す」と判定した一覧（effort {effort or '?'}）", "",
             "返信の条件「correct なら自信低も返す」で返す全件。「自信高だけ」でも返すものは"
             " confidence が high の行。ラベルは運用者が手で返していた時期の実際の返信から付けたもの。", ""]
    for label in REVIEW_LABELS:
        group = [item for item in items if item["label"] == label]
        lines += [f"## ラベル {label}（{len(group)} 件）", ""]
        for n, item in enumerate(group, 1):
            gate = "自信高だけでも返す" if item["confidence"] == "high" else "自信低も返すときだけ"
            lines += [
                f"### {label}-{n}（{gate}）", "",
                f"- 問題: {item['question_text']}",
                f"- 用意した答え: {item['answer_text']}",
                f"- コメント: {item['comment_text']}",
                f"- 判定: correct / {item['confidence']} — {item['reason']}",
                f"- media_id / comment_id: {item['media_id']} / {item['comment_id']}", "",
            ]
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")
    return len(items)


def report(rows: list[dict], usage: dict | None, review_out: Path | None, effort: str | None) -> None:
    """Print both reply rules, usage and write the review list when requested."""
    for rule in REPLY_RULES:
        print_summary(aggregate_results(rows, rule))
        print()
    if usage is not None:
        print_usage(usage, len(rows))
    if review_out is not None:
        count = write_review(review_out, rows, effort)
        print(f"確認用の一覧: {review_out}（{count} 件）")


def evaluate_media(
    rows: list[dict], answer: dict | None, config: Config, api_key: str,
    usage: list[dict] | None = None,
) -> list[dict]:
    """Judge one complete media group; retain one output record per input row."""
    try:
        if answer is None:
            raise ValueError("answer missing")
        snapshot = snapshot_from_answer(answer)
        results = judge.judge_comments(
            snapshot, [{"id": row["comment_id"], "text": row["comment_text"]} for row in rows],
            config=config, api_key=api_key, usage=usage,
        )
    except Exception:
        results = {}
    return [{
        **row, "prediction": results.get(row["comment_id"]), "effort": config.judge_effort,
        "would_reply": would_reply(results.get(row["comment_id"])),
        "would_reply_any": would_reply(results.get(row["comment_id"]), "any"),
    } for row in rows]


def main(argv: list[str] | None = None) -> None:
    """Read saved inputs, process media in four workers and save all predictions."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--eval", type=Path, default=DATA / "eval.jsonl")
    parser.add_argument("--answers", type=Path, default=DATA / "answers.json")
    parser.add_argument("--out", type=Path, default=DATA / "eval_result.jsonl")
    parser.add_argument("--limit-media", type=int)
    parser.add_argument("--effort", choices=sorted(JUDGE_EFFORTS),
                        help="override JUDGE_EFFORT for this evaluation only")
    parser.add_argument("--review-out", type=Path,
                        help="write the Markdown list of replies to wrong/other/unanswered labels")
    parser.add_argument("--summary-from", type=Path,
                        help="re-summarize a saved result file without calling the API")
    args = parser.parse_args(argv)
    if args.summary_from is not None:
        with args.summary_from.open(encoding="utf-8") as stream:
            saved = [json.loads(line) for line in stream if line.strip()]
        report(saved, None, args.review_out, saved[0].get("effort") if saved else None)
        return
    if args.limit_media is not None and args.limit_media < 1:
        parser.error("--limit-media must be positive")
    api_key = os.environ.get("ANTHROPIC_API_KEY", "")
    if not api_key.strip():
        parser.error("ANTHROPIC_API_KEY is required")
    with args.eval.open(encoding="utf-8") as stream:
        rows = [json.loads(line) for line in stream if line.strip()]
    answers = {str(answer["media_id"]): answer
               for answer in json.loads(args.answers.read_text(encoding="utf-8"))}
    grouped: dict[str, list[dict]] = defaultdict(list)
    for row in rows:
        if row["label"] not in LABELS:
            parser.error("evaluation data contains an unknown label")
        grouped[str(row["media_id"])].append(row)
    media_ids = list(grouped)[:args.limit_media]
    config = Config.from_env()
    if args.effort is not None:
        config = replace(config, judge_effort=args.effort)
    by_media = {}
    usage: list[dict] = []
    with ThreadPoolExecutor(max_workers=4) as pool:
        futures = {pool.submit(evaluate_media, grouped[mid], answers.get(mid), config, api_key, usage): mid
                   for mid in media_ids}
        for future in as_completed(futures):
            by_media[futures[future]] = future.result()
    results = [row for mid in media_ids for row in by_media[mid]]
    args.out.parent.mkdir(parents=True, exist_ok=True)
    with args.out.open("w", encoding="utf-8") as stream:
        for row in results:
            stream.write(json.dumps(row, ensure_ascii=False) + "\n")
    print(f"モデル: {config.judge_model}  effort: {config.judge_effort}")
    report(results, total_usage(usage), args.review_out, config.judge_effort)


if __name__ == "__main__":
    main()
