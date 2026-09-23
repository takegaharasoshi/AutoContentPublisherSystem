"""承認済み MP4 と背景原画を S3・ローカル DB・Aurora へ反映する。"""

from __future__ import annotations

import argparse
import datetime as dt
import os
from pathlib import Path
import subprocess
import sys
from typing import Any, Iterable

from build import validate_probe
from common import (
    HERE,
    ROOT,
    SET_CODE,
    WORK,
    background_s3_key,
    load_items,
    load_manifest,
    select_items,
    video_s3_key,
)


SQL_PATH = WORK / "update_prebuilt.sql"
VERIFY_SQL_PATH = WORK / "verify_prebuilt.sql"
AURORA_SCRIPT = (
    ROOT / "content" / "ranking-stock" / "pref-ranking-1"
    / "common" / "apply_aurora.py"
)


class ManifestValidationError(ValueError):
    """publish 前の一括検査エラー。"""

    def __init__(self, errors: Iterable[str]) -> None:
        self.errors = list(errors)
        super().__init__(" / ".join(self.errors))


def parse_approved_file(path: Path) -> list[str]:
    """空行と # コメントを除いた content_key 一覧を返す。"""
    return [
        line.strip()
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip() and not line.lstrip().startswith("#")
    ]


def _artifact_path(value: object, work: Path) -> Path | None:
    if not isinstance(value, str) or not value:
        return None
    path = Path(value)
    resolved = path.resolve() if path.is_absolute() else (work / path).resolve()
    try:
        resolved.relative_to(work.resolve())
    except ValueError as exc:
        raise ValueError(f"生成物パスが work 外を指しています: {value}") from exc
    return resolved


def inspect_manifest(
    manifest: dict[str, Any], approved: Iterable[str], *, base: Path = HERE
) -> tuple[list[dict[str, Any]], list[str]]:
    """承認対象を全件検査し、可能な計画と全エラーを同時に返す。"""
    keys = list(approved)
    errors: list[str] = []
    targets: list[dict[str, Any]] = []
    if len(keys) != len(set(keys)):
        errors.append("承認ファイルに重複した content_key があります")
    work = base / "work"
    for key in keys:
        record = manifest.get(key)
        if not isinstance(record, dict):
            errors.append(f"{key}: manifest に存在しません")
            continue
        if record.get("content_key") != key:
            errors.append(f"{key}: manifest 内の content_key が一致しません")
        try:
            video_path = _artifact_path(record.get("video"), work)
            background_path = _artifact_path(record.get("background_png"), work)
        except ValueError as exc:
            errors.append(f"{key}: {exc}")
            continue
        if video_path is None:
            errors.append(f"{key}: video パスがありません")
        elif not video_path.is_file():
            errors.append(f"{key}: MP4 がありません: {video_path}")
        if background_path is None:
            errors.append(f"{key}: background_png パスがありません")
        elif not background_path.is_file():
            errors.append(f"{key}: 背景原画 PNG がありません: {background_path}")
        probe = record.get("probe")
        if not isinstance(probe, dict):
            errors.append(f"{key}: probe がありません")
        else:
            probe_errors = validate_probe(probe)
            if probe.get("valid") is not True:
                probe_errors.append("manifest の probe.valid が true ではありません")
            errors.extend(f"{key}: {error}" for error in dict.fromkeys(probe_errors))
        bgm = record.get("bgm")
        if not isinstance(bgm, dict):
            errors.append(f"{key}: BGM 記録がありません")
            bgm = {}
        if bgm.get("provisional") is True:
            errors.append(f"{key}: 暫定 BGM のため publish できません")
        if not isinstance(bgm.get("s3_key"), str) or not bgm.get("s3_key"):
            errors.append(f"{key}: BGM の s3_key がありません")
        if not isinstance(record.get("built_at"), str) or not record.get("built_at"):
            errors.append(f"{key}: built_at がありません")
        targets.append(
            {
                **record,
                "content_key": key,
                "video_path": video_path,
                "background_path": background_path,
                "bgm": bgm,
            }
        )
    return targets, errors


def validate_manifest(
    manifest: dict[str, Any], approved: Iterable[str], *, base: Path = HERE
) -> list[dict[str, Any]]:
    """publish 条件を満たした対象だけを返し、不備は一括例外にする。"""
    targets, errors = inspect_manifest(manifest, approved, base=base)
    if errors:
        raise ManifestValidationError(errors)
    return targets


def _sql_literal(value: str) -> str:
    return "'" + value.replace("\\", "\\\\").replace("'", "''") + "'"


def _mysql_datetime(value: str) -> str:
    try:
        parsed = dt.datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return value
    if parsed.tzinfo is not None:
        parsed = parsed.astimezone(dt.timezone.utc).replace(tzinfo=None)
    return parsed.strftime("%Y-%m-%d %H:%M:%S")


def generate_update_sql(targets: Iterable[dict[str, Any]]) -> str:
    """環境非依存の content_key・set_code・BGM S3 key で UPDATE を生成する。"""
    lines = [
        "-- umigame-soup-1 prebuilt 動画の反映 SQL",
        "-- S3 アップロード後、ローカル MySQL と Aurora の両方へ適用する。",
        "",
    ]
    for target in targets:
        key = str(target["content_key"])
        bgm_key = str(target["bgm"]["s3_key"])
        built_at = _mysql_datetime(str(target["built_at"]))
        lines.append(
            "UPDATE umigame_stock_items u "
            "JOIN batch_sets b ON b.id = u.set_id "
            f"AND b.set_code = {_sql_literal(SET_CODE)} "
            "JOIN audio_assets a ON a.set_id = u.set_id "
            f"AND a.s3_key = {_sql_literal(bgm_key)} "
            f"SET u.video_s3_key = {_sql_literal(video_s3_key(key))}, "
            "u.video_audio_asset_id = a.id, "
            f"u.video_built_at = {_sql_literal(built_at)} "
            f"WHERE u.content_key = {_sql_literal(key)};"
        )
    return "\n".join(lines) + "\n"


def _run(
    command: list[str], label: str, *, input_text: str | None = None
) -> subprocess.CompletedProcess[str]:
    try:
        completed = subprocess.run(
            command, input=input_text, capture_output=True, text=True, check=False
        )
    except FileNotFoundError as exc:
        raise RuntimeError(f"{label} を起動できません: {exc}") from exc
    if completed.returncode != 0:
        detail = "\n".join(
            (completed.stdout + completed.stderr).strip().splitlines()[-12:]
        )
        raise RuntimeError(f"{label} が失敗しました（{completed.returncode}）:\n{detail}")
    if completed.stdout.strip():
        print(completed.stdout.strip())
    return completed


def _upload(targets: Iterable[dict[str, Any]], bucket: str) -> None:
    for target in targets:
        key = str(target["content_key"])
        for source, destination in (
            (target["video_path"], video_s3_key(key)),
            (target["background_path"], background_s3_key(key)),
        ):
            _run(
                ["aws", "s3", "cp", str(source), f"s3://{bucket}/{destination}"],
                f"S3 upload {key}",
            )


def _verification_sql() -> str:
    return (
        "SELECT COUNT(*) AS video_built_count FROM umigame_stock_items u "
        "JOIN batch_sets b ON b.id = u.set_id "
        f"WHERE b.set_code = {_sql_literal(SET_CODE)} "
        "AND u.video_s3_key IS NOT NULL;"
    )


def _apply_databases(sql: str) -> None:
    mysql = [
        "docker", "exec", "-i", "acps-mysql", "mysql",
        "-uapp", "-ppassword", "acps",
    ]
    _run(mysql, "ローカル MySQL UPDATE", input_text=sql)
    query = _verification_sql()
    print("ローカル MySQL 件数確認 SELECT:", query)
    _run([*mysql, "-N", "-e", query], "ローカル MySQL 件数確認")
    _run([sys.executable, str(AURORA_SCRIPT), str(SQL_PATH)], "Aurora UPDATE")
    VERIFY_SQL_PATH.write_text(query + "\n", encoding="utf-8")
    print("Aurora 件数確認 SELECT:", query)
    _run(
        [sys.executable, str(AURORA_SCRIPT), str(VERIFY_SQL_PATH)],
        "Aurora 件数確認",
    )


def _print_plan(targets: Iterable[dict[str, Any]], bucket: str) -> None:
    for target in targets:
        key = str(target["content_key"])
        print(f"upload: {target['video_path']} -> s3://{bucket}/{video_s3_key(key)}")
        print(
            f"upload: {target['background_path']} -> "
            f"s3://{bucket}/{background_s3_key(key)}"
        )
    print(f"SQL: {SQL_PATH}")


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--approved", type=Path, default=WORK / "approved.txt")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--batch", default="batch-01")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    try:
        approved = parse_approved_file(args.approved)
        if not approved:
            raise ManifestValidationError(["承認済み content_key がありません"])
        select_items(load_items(args.batch), approved)
        manifest = load_manifest()
        targets, errors = inspect_manifest(manifest, approved)
    except (OSError, ValueError) as exc:
        print(f"エラー: {exc}", file=sys.stderr)
        return 1

    sql = generate_update_sql(targets)
    SQL_PATH.parent.mkdir(parents=True, exist_ok=True)
    SQL_PATH.write_text(sql, encoding="utf-8")
    bucket = os.environ.get("S3_BUCKET_NAME", "$S3_BUCKET_NAME")
    _print_plan(targets, bucket)
    if errors:
        print("検査エラー:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
    if args.dry_run:
        print("\n生成 SQL:\n" + sql)
        if errors:
            print("dry-run: 本実行なら副作用の前に上記検査で停止します", file=sys.stderr)
            return 1
        print("dry-run: 検査 OK。S3・DB・aws・docker は呼び出していません")
        return 0
    if errors:
        print("副作用を開始せず停止しました", file=sys.stderr)
        return 1
    if bucket == "$S3_BUCKET_NAME":
        print("エラー: 本実行には S3_BUCKET_NAME が必要です", file=sys.stderr)
        return 1
    try:
        _upload(targets, bucket)
        _apply_databases(sql)
    except RuntimeError as exc:
        print(f"エラー: {exc}", file=sys.stderr)
        return 1
    print(f"{len(targets)} 件を publish しました")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
