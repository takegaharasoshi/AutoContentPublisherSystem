"""Apply a generated INSERT script to Aurora through the RDS Data API.

The Data API takes one statement per call, so the script is split on
semicolons that sit outside single-quoted strings (``source_note`` contains
newlines and punctuation, and a naive ``split(";")`` corrupts it).

Aurora Serverless v2 auto-pauses; the first call after a pause returns
``DatabaseResumingException``. Each statement is retried on that error.

Usage:
    python3 common/apply_aurora.py <batch-dir>/insert_ranking_stock.sql [--dry-run]

The cluster and secret ARNs are discovered with the AWS CLI unless
``AURORA_CLUSTER_ARN`` / ``AURORA_SECRET_ARN`` are set.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import time
from pathlib import Path

RESUME_WAIT_SECONDS = 20
RESUME_ATTEMPTS = 6


def discover_arn(command: list[str]) -> str:
    """Return a single ARN from an AWS CLI query.

    Args:
        command: AWS CLI argument list producing one text value.

    Returns:
        The resolved ARN.
    """
    result = subprocess.run(command, capture_output=True, text=True, timeout=120)
    if result.returncode != 0:
        raise SystemExit(f"ARN discovery failed: {result.stderr.strip()}")
    return result.stdout.split()[0]


def resolve_endpoints() -> tuple[str, str]:
    """Resolve the Aurora cluster ARN and the credentials secret ARN.

    Returns:
        The cluster ARN and the secret ARN.
    """
    cluster = os.environ.get("AURORA_CLUSTER_ARN") or discover_arn(
        [
            "aws", "rds", "describe-db-clusters",
            "--query", "DBClusters[0].DBClusterArn",
            "--output", "text",
        ]
    )
    secret = os.environ.get("AURORA_SECRET_ARN") or discover_arn(
        [
            "aws", "secretsmanager", "list-secrets",
            "--query", "SecretList[?contains(Name,'db/credentials')].ARN",
            "--output", "text",
        ]
    )
    return cluster, secret


def split_statements(sql: str) -> list[str]:
    """Split SQL on semicolons outside single-quoted strings.

    Args:
        sql: Whole script text.

    Returns:
        Executable statements with leading comment lines removed.
    """
    statements: list[str] = []
    current: list[str] = []
    in_string = False
    index = 0
    while index < len(sql):
        char = sql[index]
        if in_string:
            if char == "\\":
                current.append(sql[index : index + 2])
                index += 2
                continue
            if char == "'":
                in_string = False
        elif char == "'":
            in_string = True
        elif char == ";":
            statements.append("".join(current))
            current = []
            index += 1
            continue
        current.append(char)
        index += 1
    statements.append("".join(current))

    cleaned: list[str] = []
    for statement in statements:
        # 先頭のコメント行は空行を挟んで複数ブロック続くことがある（ファイル冒頭の
        # 説明 + 各 INSERT の連番コメント）ため、変化しなくなるまで剥がす。
        body = statement.strip()
        while True:
            stripped = re.sub(r"^(--[^\n]*\n?)+", "", body).strip()
            if stripped == body:
                break
            body = stripped
        if body:
            cleaned.append(body)
    return cleaned


def execute(cluster: str, secret: str, sql: str) -> int:
    """Run one statement, retrying while the cluster resumes.

    Args:
        cluster: Aurora cluster ARN.
        secret: Credentials secret ARN.
        sql: Single SQL statement.

    Returns:
        Number of records the statement updated.
    """
    for attempt in range(1, RESUME_ATTEMPTS + 1):
        result = subprocess.run(
            [
                "aws", "rds-data", "execute-statement",
                "--resource-arn", cluster,
                "--secret-arn", secret,
                "--database", "acps",
                "--sql", sql,
                "--output", "json",
            ],
            capture_output=True,
            text=True,
            timeout=180,
        )
        if result.returncode == 0:
            return json.loads(result.stdout).get("numberOfRecordsUpdated", 0)
        if "DatabaseResuming" in result.stderr:
            print(f"  Aurora resuming, retrying in {RESUME_WAIT_SECONDS}s ({attempt})")
            time.sleep(RESUME_WAIT_SECONDS)
            continue
        raise SystemExit(f"failed:\n{result.stderr}\n---\n{sql[:400]}")
    raise SystemExit("cluster did not resume")


def main() -> int:
    """Entry point.

    Returns:
        Process exit code.
    """
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("sql_path", type=Path, help="generated INSERT script")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="print the statement count and the first line of each, without executing",
    )
    args = parser.parse_args()

    statements = split_statements(args.sql_path.read_text(encoding="utf-8"))
    print(f"{len(statements)} statements in {args.sql_path.name}")
    if args.dry_run:
        for number, statement in enumerate(statements, start=1):
            print(f"  [{number}] {statement.splitlines()[0][:100]}")
        return 0

    cluster, secret = resolve_endpoints()
    total = 0
    for number, statement in enumerate(statements, start=1):
        updated = execute(cluster, secret, statement)
        total += updated
        print(f"  [{number}/{len(statements)}] updated={updated}")
    print(f"total records updated: {total}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
