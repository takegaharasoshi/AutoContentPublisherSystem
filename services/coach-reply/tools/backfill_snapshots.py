#!/usr/bin/env python3
"""Backfill missing logic-training-1 snapshots; dry-run unless --apply is set."""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import time
from pathlib import Path
from typing import Any


sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.config import Config  # noqa: E402
from app.snapshot_store import snapshot_from_answer  # noqa: E402


DB = "acps"
# Keep this SELECT identical to collect.py cmd_answers (no DB writes).
ANSWERS_SQL = """
SELECT p.platform_post_id AS media_id, p.posted_at, q.quiz_type, q.difficulty,
       q.question_text, q.answer_text, q.content_fields
FROM posts p
JOIN batch_sets b ON b.id = p.set_id
JOIN quiz_items q ON q.set_id = p.set_id AND q.generation_run_id = p.generation_run_id
WHERE b.set_code = 'logic-training-1' AND p.status = 'success' AND p.platform_post_id IS NOT NULL
ORDER BY p.posted_at"""


def aurora_execute(sql: str = ANSWERS_SQL) -> list[dict]:
    """Use collect.py's CLI ARN discovery and resume retries for one SELECT."""
    def discover(command: list[str]) -> str:
        return subprocess.run(
            command, capture_output=True, text=True, timeout=60, check=True,
        ).stdout.split()[0]

    cluster = os.environ.get("AURORA_CLUSTER_ARN") or discover([
        "aws", "rds", "describe-db-clusters", "--query", "DBClusters[0].DBClusterArn",
        "--output", "text",
    ])
    secret = os.environ.get("AURORA_SECRET_ARN") or discover([
        "aws", "secretsmanager", "list-secrets", "--query",
        "SecretList[?contains(Name,'db/credentials')].ARN", "--output", "text",
    ])
    command = [
        "aws", "rds-data", "execute-statement", "--resource-arn", cluster,
        "--secret-arn", secret, "--database", DB, "--sql", sql,
        "--format-records-as", "JSON", "--output", "json",
    ]
    for attempt in range(8):
        result = subprocess.run(command, capture_output=True, text=True, timeout=180)
        if result.returncode == 0:
            return json.loads(json.loads(result.stdout).get("formattedRecords", "[]"))
        if ("DatabaseResumingException" in result.stderr
                or "Communications link failure" in result.stderr):
            print(f"DB resuming, retry {attempt + 1}", file=sys.stderr)
            time.sleep(20)
            continue
        raise SystemExit(result.stderr.strip())
    raise SystemExit("DB did not resume")


def backfill(
    answers: list[dict], bucket: str, prefix: str, *, apply: bool = False,
    client: Any = None,
) -> dict[str, int]:
    """Count missing keys, optionally creating each once with a conditional PUT."""
    if client is None:
        import boto3

        client = boto3.client("s3")
    counts = {"posts": 0, "existing": 0, "missing": 0, "written": 0}
    seen: set[str] = set()
    for answer in answers:
        media_id = str(answer["media_id"])
        if media_id in seen:
            continue
        seen.add(media_id)
        counts["posts"] += 1
        key = f"{prefix}{media_id}.json"
        try:
            client.head_object(Bucket=bucket, Key=key)
        except Exception as exc:
            if str(getattr(exc, "response", {}).get("Error", {}).get("Code")) not in {
                "404", "NoSuchKey", "NotFound",
            }:
                raise
        else:
            counts["existing"] += 1
            continue
        counts["missing"] += 1
        if not apply:
            continue
        snapshot = snapshot_from_answer(answer)
        try:
            client.put_object(
                Bucket=bucket, Key=key, IfNoneMatch="*", ContentType="application/json",
                Body=json.dumps(snapshot, ensure_ascii=False).encode("utf-8"),
            )
        except Exception as exc:
            if str(getattr(exc, "response", {}).get("Error", {}).get("Code")) not in {
                "PreconditionFailed", "412",
            }:
                raise
            # A concurrent posting batch has already supplied the snapshot.
            counts["existing"] += 1
            counts["missing"] -= 1
        else:
            counts["written"] += 1
    return counts


def main(argv: list[str] | None = None) -> None:
    """Parse the opt-in write flag and print only aggregate counts."""
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--dry-run", action="store_true", help="件数のみ（既定）")
    mode.add_argument("--apply", action="store_true", help="未作成キーを S3 に書く")
    parser.add_argument("--bucket", default=os.environ.get("ASSETS_BUCKET", ""))
    parser.add_argument("--prefix", default=os.environ.get("PROBLEMS_PREFIX", Config.problems_prefix))
    args = parser.parse_args(argv)
    if not args.bucket:
        parser.error("--bucket or ASSETS_BUCKET is required")
    if not args.prefix or args.prefix.startswith("/") or not args.prefix.endswith("/"):
        parser.error("--prefix must be a relative S3 prefix ending in /")
    counts = backfill(aurora_execute(), args.bucket, args.prefix, apply=args.apply)
    print(json.dumps({"mode": "apply" if args.apply else "dry-run", **counts}))


if __name__ == "__main__":
    main()
