"""Upload approved prebuilt videos and atomically stage their DB registration."""

from __future__ import annotations

import argparse
import subprocess
from pathlib import Path

from common import SET_CODE, WORK, load_json, local_connection, utc_now


def _sql_literal(value: str) -> str:
    """Return a MySQL single-quoted literal for generated Aurora SQL."""
    return "'" + value.replace("\\", "\\\\").replace("'", "''") + "'"


def _approved_ids(path: Path) -> list[int]:
    """Read one approved stock_item_id per non-comment line."""
    return [
        int(line.strip())
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip() and not line.lstrip().startswith("#")
    ]


def main() -> None:
    """Create upload commands and register only fully built, approved rows."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--approved-file", required=True, type=Path)
    parser.add_argument("--bucket", required=True)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    manifest = load_json(WORK / "build_manifest.json", {})
    approved = _approved_ids(args.approved_file)
    built_at = utc_now().strftime("%Y-%m-%d %H:%M:%S")
    updates: list[tuple[int, str, int, str, str]] = []
    commands: list[list[str]] = []
    for stock_id in approved:
        record = manifest.get(str(stock_id))
        video = WORK / "videos" / f"{stock_id}.mp4"
        illustration = WORK / "illustrations" / f"{stock_id}.png"
        if record is None or not video.is_file() or not illustration.is_file():
            raise RuntimeError(f"Approved stock item is not fully built: {stock_id}")
        base_key = f"assets/{SET_CODE}/prebuilt/{stock_id}"
        commands.extend(
            [
                ["aws", "s3", "cp", str(video), f"s3://{args.bucket}/{base_key}.mp4"],
                [
                    "aws", "s3", "cp", str(illustration),
                    f"s3://{args.bucket}/{base_key}_illustration.png",
                ],
            ]
        )
        question_text = record.get("question_text")
        bgm_s3_key = record.get("bgm_s3_key")
        if not isinstance(question_text, str) or not question_text:
            raise RuntimeError(f"Build manifest has no question_text: {stock_id}")
        if not isinstance(bgm_s3_key, str) or not bgm_s3_key:
            raise RuntimeError(f"Build manifest has no bgm_s3_key: {stock_id}")
        updates.append(
            (
                stock_id,
                f"{base_key}.mp4",
                int(record["audio_asset_id"]),
                question_text,
                bgm_s3_key,
            )
        )
    shell_lines = ["#!/usr/bin/env bash", "set -euo pipefail", *[" ".join(command) for command in commands]]
    WORK.mkdir(parents=True, exist_ok=True)
    (WORK / "upload_prebuilt.sh").write_text("\n".join(shell_lines) + "\n", encoding="utf-8")
    sql_lines = [
        "-- Apply this file to Aurora after successful S3 upload.",
        "-- Confirm that the affected row count after applying equals the approved item count.",
    ]
    for _stock_id, key, _audio_id, question_text, bgm_s3_key in updates:
        sql_lines.append(
            "UPDATE quiz_stock_items q "
            "JOIN batch_sets b ON b.id = q.set_id "
            f"SET q.video_s3_key = {_sql_literal(key)}, "
            "q.video_audio_asset_id = (SELECT a.id FROM audio_assets a "
            f"WHERE a.set_id = q.set_id AND a.s3_key = {_sql_literal(bgm_s3_key)}), "
            f"q.video_built_at = {_sql_literal(built_at)} "
            f"WHERE b.set_code = {_sql_literal(SET_CODE)} "
            f"AND q.question_text = {_sql_literal(question_text)};"
        )
    (WORK / "update_prebuilt.sql").write_text("\n".join(sql_lines) + "\n", encoding="utf-8")
    if args.dry_run:
        print(f"dry run: wrote {len(commands)} upload commands and no DB updates")
        return
    for command in commands:
        subprocess.run(command, check=True)
    connection = local_connection()
    try:
        with connection.cursor() as cursor:
            for stock_id, key, audio_id, _question_text, _bgm_s3_key in updates:
                cursor.execute(
                    "UPDATE quiz_stock_items SET video_s3_key = %s, "
                    "video_audio_asset_id = %s, video_built_at = %s WHERE id = %s",
                    (key, audio_id, built_at, stock_id),
                )
                if cursor.rowcount != 1:
                    raise RuntimeError(f"Stock item not found: {stock_id}")
        connection.commit()
    except Exception:
        connection.rollback()
        raise
    finally:
        connection.close()
    print(f"uploaded and registered {len(updates)} approved prebuilt videos")


if __name__ == "__main__":
    main()
