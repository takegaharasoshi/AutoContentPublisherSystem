#!/usr/bin/env python3
"""Evaluate the judge against saved comments (calls the real Anthropic API)."""

from __future__ import annotations

import argparse
import json
import os
import sys
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path


sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app import judge  # noqa: E402
from app.config import Config  # noqa: E402
from app.snapshot_store import snapshot_from_answer  # noqa: E402


REPO_ROOT = Path(__file__).resolve().parents[3]
DATA = REPO_ROOT / "poc/logic-training-reply-eval/data"
LABELS = ("correct", "alt", "wrong", "other", "unanswered")


def would_reply(prediction: dict | None) -> bool:
    """Apply the exact online reply gate."""
    return bool(prediction and prediction.get("verdict") == "correct"
                and prediction.get("confidence") == "high")


def aggregate_results(rows: list[dict]) -> dict:
    """Summarize labels, false replies, recall and failures without any API call."""
    table = {label: {"reply": 0, "no_reply": 0} for label in LABELS}
    false_replies = []
    failed = 0
    for row in rows:
        label = row["label"]
        if label not in table:
            raise ValueError(f"unknown evaluation label: {label}")
        prediction = row.get("prediction")
        reply = would_reply(prediction)
        table[label]["reply" if reply else "no_reply"] += 1
        if prediction is None:
            failed += 1
        if reply and label in {"wrong", "other"}:
            false_replies.append({
                "media_id": row["media_id"], "comment_id": row["comment_id"],
                "comment_text": row["comment_text"], "answer_text": row["answer_text"],
                "reason": prediction["reason"],
            })
    total_correct = sum(table["correct"].values())
    return {
        "table": table, "false_reply_count": len(false_replies), "false_replies": false_replies,
        "correct_replied": table["correct"]["reply"], "correct_total": total_correct,
        "correct_recall": table["correct"]["reply"] / total_correct if total_correct else None,
        "judge_failures": failed,
    }


def print_summary(summary: dict) -> None:
    """Print the evaluation table and each false reply with its short rationale."""
    print("label        返す  返さない")
    for label, counts in summary["table"].items():
        print(f"{label:12} {counts['reply']:5} {counts['no_reply']:9}")
    print(f"誤返信: {summary['false_reply_count']}")
    for row in summary["false_replies"]:
        print(json.dumps(row, ensure_ascii=False))
    recall = summary["correct_recall"]
    ratio = f"{recall:.1%}" if recall is not None else "N/A"
    print(f"正解の拾えた割合: {summary['correct_replied']}/{summary['correct_total']} ({ratio})")
    print(f"判定の失敗件数: {summary['judge_failures']}")


def evaluate_media(rows: list[dict], answer: dict | None, config: Config, api_key: str) -> list[dict]:
    """Judge one complete media group; retain one output record per input row."""
    try:
        if answer is None:
            raise ValueError("answer missing")
        snapshot = snapshot_from_answer(answer)
        results = judge.judge_comments(
            snapshot, [{"id": row["comment_id"], "text": row["comment_text"]} for row in rows],
            config=config, api_key=api_key,
        )
    except Exception:
        results = {}
    return [{
        **row, "prediction": results.get(row["comment_id"]),
        "would_reply": would_reply(results.get(row["comment_id"])),
    } for row in rows]


def main(argv: list[str] | None = None) -> None:
    """Read saved inputs, process media in four workers and save all predictions."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--eval", type=Path, default=DATA / "eval.jsonl")
    parser.add_argument("--answers", type=Path, default=DATA / "answers.json")
    parser.add_argument("--out", type=Path, default=DATA / "eval_result.jsonl")
    parser.add_argument("--limit-media", type=int)
    args = parser.parse_args(argv)
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
    by_media = {}
    with ThreadPoolExecutor(max_workers=4) as pool:
        futures = {pool.submit(evaluate_media, grouped[mid], answers.get(mid), config, api_key): mid
                   for mid in media_ids}
        for future in as_completed(futures):
            by_media[futures[future]] = future.result()
    results = [row for mid in media_ids for row in by_media[mid]]
    args.out.parent.mkdir(parents=True, exist_ok=True)
    with args.out.open("w", encoding="utf-8") as stream:
        for row in results:
            stream.write(json.dumps(row, ensure_ascii=False) + "\n")
    print_summary(aggregate_results(results))


if __name__ == "__main__":
    main()
