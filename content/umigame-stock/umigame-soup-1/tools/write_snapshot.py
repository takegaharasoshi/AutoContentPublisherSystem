"""Manually write missing umigame problem snapshots for successful reels.

By default this command only lists eligible posts. Pass ``--apply`` to upload
the snapshots to S3 and record their keys in Aurora.
"""

from __future__ import annotations

import argparse
import datetime
import json
import os
import subprocess
import sys
import tempfile
import time
from pathlib import Path
from typing import Any, Sequence


DATABASE = "acps"
CONTENT_TYPE = "application/json; charset=utf-8"
RESUME_WAIT_SECONDS = 20
RESUME_ATTEMPTS = 6

SELECT_CANDIDATES_SQL = """
SELECT p.platform_post_id AS media_id,
       p.generation_run_id AS generation_run_id,
       ui.id AS item_id,
       ui.content_key AS content_key,
       p.posted_at AS posted_at,
       ui.problem_text AS problem_text,
       ui.truth AS truth,
       ui.fact_sheet AS fact_sheet,
       ui.core_points AS core_points,
       ui.judge_criteria AS judge_criteria,
       ui.reveal_text AS reveal_text,
       ui.rule_text AS rule_text,
       (SELECT pc.prompt_text
          FROM prompt_configs pc
         WHERE pc.set_id = p.set_id AND pc.is_active = 1
         ORDER BY pc.id LIMIT 1) AS master_rules
FROM posts p
JOIN batch_sets bs ON bs.id = p.set_id
JOIN umigame_items ui
  ON ui.set_id = p.set_id
 AND ui.generation_run_id = p.generation_run_id
 AND ui.snapshot_s3_key IS NULL
JOIN post_media pm ON pm.post_id = p.id AND pm.display_order = 0
JOIN generated_media gm
  ON gm.id = pm.generated_media_id
 AND gm.set_id = p.set_id
 AND gm.generation_run_id = p.generation_run_id
WHERE bs.set_code = :set_code
  AND p.status = 'success'
  AND p.media_type = 'reel'
  AND p.platform_post_id IS NOT NULL
  AND LOWER(TRIM(gm.file_format)) = 'mp4'
ORDER BY p.posted_at, p.id
""".strip()


class SnapshotToolError(RuntimeError):
    """Raised when an AWS CLI operation or snapshot validation fails."""


def _run_command(
    command: list[str], *, timeout: int = 180
) -> subprocess.CompletedProcess:
    """Run one AWS CLI command and raise a useful error on failure.

    Args:
        command: Complete AWS CLI argument vector.
        timeout: Maximum time to wait for the command.

    Returns:
        The completed subprocess result.
    """
    result = subprocess.run(
        command,
        capture_output=True,
        text=True,
        timeout=timeout,
    )
    if result.returncode != 0:
        detail = result.stderr.strip() or result.stdout.strip()
        raise SnapshotToolError(f"AWS CLI command failed: {detail}")
    return result


def resolve_endpoints() -> tuple[str, str]:
    """Resolve the Aurora cluster and credentials secret ARNs.

    The environment variable overrides and AWS CLI discovery follow
    ``content/ranking-stock/pref-ranking-1/common/apply_aurora.py``.

    Returns:
        The Aurora cluster ARN and credentials secret ARN.
    """
    cluster = os.environ.get("AURORA_CLUSTER_ARN")
    if not cluster:
        cluster_result = _run_command(
            [
                "aws",
                "rds",
                "describe-db-clusters",
                "--query",
                "DBClusters[0].DBClusterArn",
                "--output",
                "text",
            ],
            timeout=120,
        )
        cluster = cluster_result.stdout.split()[0]

    secret = os.environ.get("AURORA_SECRET_ARN")
    if not secret:
        secret_result = _run_command(
            [
                "aws",
                "secretsmanager",
                "list-secrets",
                "--query",
                "SecretList[?contains(Name,'db/credentials')].ARN",
                "--output",
                "text",
            ],
            timeout=120,
        )
        secret = secret_result.stdout.split()[0]
    return cluster, secret


def _execute_statement(
    cluster_arn: str,
    secret_arn: str,
    sql: str,
    parameters: list[dict[str, Any]],
) -> dict[str, Any]:
    """Execute one Aurora Data API statement, retrying during resume.

    Args:
        cluster_arn: Aurora cluster ARN.
        secret_arn: Credentials secret ARN.
        sql: One SQL statement using named Data API parameters.
        parameters: RDS Data API parameter objects.

    Returns:
        Parsed JSON response from the RDS Data API.

    Raises:
        SnapshotToolError: If the statement fails or the cluster does not resume.
    """
    command = [
        "aws",
        "rds-data",
        "execute-statement",
        "--resource-arn",
        cluster_arn,
        "--secret-arn",
        secret_arn,
        "--database",
        DATABASE,
        "--sql",
        sql,
        "--parameters",
        json.dumps(parameters, ensure_ascii=False),
        "--format-records-as",
        "JSON",
        "--output",
        "json",
    ]
    for attempt in range(1, RESUME_ATTEMPTS + 1):
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=180,
        )
        if result.returncode == 0:
            try:
                response = json.loads(result.stdout)
            except json.JSONDecodeError as exc:
                raise SnapshotToolError("Aurora returned invalid JSON") from exc
            if not isinstance(response, dict):
                raise SnapshotToolError("Aurora returned an invalid response")
            return response
        if "DatabaseResumingException" in result.stderr:
            print(
                f"Aurora resuming; retrying in {RESUME_WAIT_SECONDS}s "
                f"({attempt}/{RESUME_ATTEMPTS})",
                file=sys.stderr,
            )
            time.sleep(RESUME_WAIT_SECONDS)
            continue
        raise SnapshotToolError(
            f"Aurora statement failed: {result.stderr.strip()}"
        )
    raise SnapshotToolError("Aurora cluster did not resume")


def _formatted_records(response: dict[str, Any]) -> list[dict[str, Any]]:
    """Decode the formattedRecords value returned by the Data API.

    Args:
        response: Parsed RDS Data API response.

    Returns:
        Formatted result records.
    """
    records = response.get("formattedRecords", "[]")
    if isinstance(records, str):
        try:
            records = json.loads(records)
        except json.JSONDecodeError as exc:
            raise SnapshotToolError("Aurora returned invalid formattedRecords") from exc
    if not isinstance(records, list) or any(
        not isinstance(record, dict) for record in records
    ):
        raise SnapshotToolError("Aurora returned an invalid record list")
    return records


def _string_parameter(name: str, value: str | None) -> dict[str, Any]:
    """Build one string parameter for the RDS Data API.

    Args:
        name: Named SQL parameter without a leading colon.
        value: String value, or ``None`` for SQL NULL.

    Returns:
        An RDS Data API parameter object.
    """
    if value is None:
        return {"name": name, "value": {"isNull": True}}
    return {"name": name, "value": {"stringValue": value}}


def fetch_candidates(
    cluster_arn: str,
    secret_arn: str,
    set_code: str,
    media_id: str | None,
) -> list[dict[str, Any]]:
    """Fetch successful reel posts whose umigame snapshot is missing.

    Args:
        cluster_arn: Aurora cluster ARN.
        secret_arn: Credentials secret ARN.
        set_code: Batch set code to inspect.
        media_id: Optional platform media ID filter.

    Returns:
        Candidate rows from Aurora.
    """
    sql = SELECT_CANDIDATES_SQL
    parameters = [_string_parameter("set_code", set_code)]
    if media_id is not None:
        sql = sql.replace(
            "ORDER BY p.posted_at, p.id",
            "AND p.platform_post_id = :media_id\nORDER BY p.posted_at, p.id",
        )
        parameters.append(_string_parameter("media_id", media_id))
    response = _execute_statement(
        cluster_arn,
        secret_arn,
        sql,
        parameters,
    )
    return _formatted_records(response)


def _decode_json_column(name: str, value: Any) -> Any:
    """Decode one JSON column like the SNS batch's umigame item repository.

    Args:
        name: Database column name used in error messages.
        value: Value returned by the Data API.

    Returns:
        Parsed JSON value, or the original value if already decoded.

    Raises:
        RuntimeError: If the column is not valid UTF-8 or JSON.
    """
    if isinstance(value, (bytes, bytearray)):
        try:
            value = value.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise RuntimeError(f"umigame_items.{name} is invalid UTF-8") from exc
    if isinstance(value, str):
        try:
            return json.loads(value)
        except json.JSONDecodeError as exc:
            raise RuntimeError(f"umigame_items.{name} is invalid JSON") from exc
    return value


def _parse_posted_at(value: Any) -> str:
    """Format the post timestamp as a UTC ISO 8601 value ending in ``Z``.

    Args:
        value: Data API timestamp or datetime object.

    Returns:
        UTC timestamp in the same format as ``problem_snapshot.py``.
    """
    if isinstance(value, str):
        try:
            posted_at = datetime.datetime.fromisoformat(
                value.replace("Z", "+00:00")
            )
        except ValueError as exc:
            raise RuntimeError("posts.posted_at is not a valid timestamp") from exc
    elif isinstance(value, datetime.datetime):
        posted_at = value
    else:
        raise RuntimeError("posts.posted_at is missing or is not a timestamp")

    if posted_at.tzinfo is None:
        posted_at = posted_at.replace(tzinfo=datetime.timezone.utc)
    return posted_at.astimezone(datetime.timezone.utc).isoformat().replace(
        "+00:00", "Z"
    )


def build_snapshot(row: dict[str, Any], set_code: str) -> dict[str, Any]:
    """Validate a candidate and build its problem snapshot in canonical order.

    Validation mirrors ``umigame_items.py`` and ``problem_snapshot.py``.

    Args:
        row: Candidate row returned by Aurora.
        set_code: Set code to store in the snapshot.

    Returns:
        Snapshot mapping with keys in the service's insertion order.

    Raises:
        RuntimeError: If required problem data or the active prompt is invalid.
    """
    fact_sheet = _decode_json_column("fact_sheet", row.get("fact_sheet"))
    if (
        not isinstance(fact_sheet, list)
        or not fact_sheet
        or any(not isinstance(fact, str) or not fact.strip() for fact in fact_sheet)
    ):
        raise RuntimeError(
            "umigame_items.fact_sheet must be a non-empty array of strings"
        )

    core_points = row.get("core_points")
    if core_points is not None:
        core_points = _decode_json_column("core_points", core_points)
        if (
            not isinstance(core_points, list)
            or not 1 <= len(core_points) <= 3
            or any(
                not isinstance(point, str) or not point.strip()
                for point in core_points
            )
        ):
            raise RuntimeError(
                "umigame_items.core_points must be an array of 1 to 3 non-empty strings"
            )

    judge_criteria = row.get("judge_criteria")
    if judge_criteria is not None:
        judge_criteria = _decode_json_column("judge_criteria", judge_criteria)
        if not isinstance(judge_criteria, dict):
            raise RuntimeError("umigame_items.judge_criteria must be an object")
        points = judge_criteria.get("points")
        errors = judge_criteria.get("errors")
        if (
            not isinstance(points, list)
            or core_points is None
            or len(points) != len(core_points)
            or any(
                not isinstance(point, dict)
                or any(
                    not isinstance(point.get(key), str) or not point[key].strip()
                    for key in ("hit", "touch")
                )
                for point in points
            )
            or not isinstance(errors, list)
            or len(errors) > 3
            or any(not isinstance(error, str) or not error.strip() for error in errors)
        ):
            raise RuntimeError(
                "umigame_items.judge_criteria must match core_points and contain "
                "valid points and errors"
            )

    reveal_text = row.get("reveal_text")
    if (
        not isinstance(core_points, list)
        or not core_points
        or not isinstance(judge_criteria, dict)
        or not isinstance(reveal_text, str)
        or not reveal_text.strip()
    ):
        raise RuntimeError(
            "umigame_items.core_points / judge_criteria / reveal_text is NULL or "
            "empty; "
            "apply V013 and V014 and update the umigame_stock_items rows before "
            "publishing snapshots"
        )

    master_rules = row.get("master_rules")
    if not isinstance(master_rules, str) or not master_rules.strip():
        raise RuntimeError(
            "Active prompt_configs.prompt_text is missing for this set"
        )

    return {
        "schema_version": 3,
        "set_code": set_code,
        "media_id": row["media_id"],
        "content_key": row["content_key"],
        "posted_at": _parse_posted_at(row.get("posted_at")),
        "problem_text": row["problem_text"],
        "truth": row["truth"],
        "fact_sheet": fact_sheet,
        "core_points": core_points,
        "judge_criteria": judge_criteria,
        "reveal_text": reveal_text,
        "rule_text": row["rule_text"],
        "master_rules": master_rules,
    }


def _default_bucket() -> str:
    """Derive the production image bucket from the caller's AWS account ID.

    Returns:
        Production image bucket name.
    """
    result = _run_command(
        [
            "aws",
            "sts",
            "get-caller-identity",
            "--query",
            "Account",
            "--output",
            "text",
        ],
        timeout=60,
    )
    account_id = result.stdout.strip()
    if not account_id:
        raise SnapshotToolError("AWS STS returned an empty account ID")
    return f"acps-prod-images-{account_id}"


def _put_object(bucket: str, key: str, body: bytes) -> None:
    """Upload snapshot bytes to S3 through the AWS CLI.

    Args:
        bucket: Destination bucket.
        key: Destination object key.
        body: UTF-8 JSON body.
    """
    with tempfile.TemporaryDirectory(prefix="umigame-snapshot-") as temp_dir:
        body_path = Path(temp_dir) / "snapshot.json"
        body_path.write_bytes(body)
        _run_command(
            [
                "aws",
                "s3api",
                "put-object",
                "--bucket",
                bucket,
                "--key",
                key,
                "--body",
                str(body_path),
                "--content-type",
                CONTENT_TYPE,
            ],
            timeout=180,
        )


def _record_snapshot(
    cluster_arn: str,
    secret_arn: str,
    item_id: int,
    key: str,
) -> int:
    """Record a successfully uploaded key in Aurora if it is still missing.

    Args:
        cluster_arn: Aurora cluster ARN.
        secret_arn: Credentials secret ARN.
        item_id: umigame_items primary key.
        key: S3 key that was uploaded.

    Returns:
        Number of updated records.
    """
    written_at = datetime.datetime.now(datetime.timezone.utc).replace(tzinfo=None)
    response = _execute_statement(
        cluster_arn,
        secret_arn,
        "UPDATE umigame_items "
        "SET snapshot_s3_key = :snapshot_key, "
        "snapshot_written_at = CAST(:snapshot_written_at AS DATETIME) "
        "WHERE id = :item_id AND snapshot_s3_key IS NULL",
        [
            _string_parameter("snapshot_key", key),
            _string_parameter(
                "snapshot_written_at",
                written_at.isoformat(sep=" ", timespec="microseconds"),
            ),
            {"name": "item_id", "value": {"longValue": item_id}},
        ],
    )
    try:
        return int(response.get("numberOfRecordsUpdated", 0))
    except (TypeError, ValueError) as exc:
        raise SnapshotToolError("Aurora returned an invalid update count") from exc


def _display_posted_at(value: Any) -> str:
    """Format a candidate timestamp for the dry-run listing.

    Args:
        value: Timestamp returned from Aurora.

    Returns:
        Readable timestamp string.
    """
    if isinstance(value, datetime.datetime):
        return value.isoformat(sep=" ")
    return "" if value is None else str(value)


def main(argv: Sequence[str] | None = None) -> int:
    """List missing snapshots or write them when ``--apply`` is provided.

    Args:
        argv: Optional command-line arguments, used by tests.

    Returns:
        Exit status: 1 if any candidate fails, otherwise 0.
    """
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--set-code", default="umigame-soup-1")
    parser.add_argument("--media-id", help="only process this platform media ID")
    parser.add_argument("--bucket", help="S3 bucket; defaults to the prod image bucket")
    parser.add_argument(
        "--apply",
        action="store_true",
        help="upload snapshots and update Aurora; default is list-only",
    )
    args = parser.parse_args(argv)

    try:
        cluster_arn, secret_arn = resolve_endpoints()
        rows = fetch_candidates(
            cluster_arn,
            secret_arn,
            args.set_code,
            args.media_id,
        )
    except Exception as exc:
        print(f"ERROR: failed to load snapshot candidates: {exc}", file=sys.stderr)
        return 1

    ready: list[tuple[dict[str, Any], dict[str, Any]]] = []
    failures = 0
    for row in rows:
        media_id = row.get("media_id", "<unknown>")
        try:
            snapshot = build_snapshot(row, args.set_code)
            ready.append((row, snapshot))
        except Exception as exc:
            failures += 1
            print(f"ERROR media_id={media_id}: {exc}", file=sys.stderr)

    if not args.apply:
        print("media_id\tgeneration_run_id\tcontent_key\tposted_at")
        for row, _snapshot in ready:
            print(
                "\t".join(
                    str(value)
                    for value in (
                        row.get("media_id", ""),
                        row.get("generation_run_id", ""),
                        row.get("content_key", ""),
                        _display_posted_at(row.get("posted_at")),
                    )
                )
            )
        return 1 if failures else 0

    if not ready:
        return 1 if failures else 0

    try:
        bucket = args.bucket or _default_bucket()
    except Exception as exc:
        print(f"ERROR: failed to resolve S3 bucket: {exc}", file=sys.stderr)
        return 1

    for row, snapshot in ready:
        media_id = row["media_id"]
        key = f"assets/{args.set_code}/problems/{media_id}.json"
        try:
            body = json.dumps(snapshot, ensure_ascii=False).encode("utf-8")
            _put_object(bucket, key, body)
            updated = _record_snapshot(
                cluster_arn,
                secret_arn,
                int(row["item_id"]),
                key,
            )
            if updated != 1:
                raise SnapshotToolError(
                    "snapshot_s3_key was no longer NULL; uploaded object was not "
                    "recorded in Aurora"
                )
            print(f"Wrote media_id={media_id} key={key}")
        except Exception as exc:
            failures += 1
            print(f"ERROR media_id={media_id}: {exc}", file=sys.stderr)

    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
