"""承認済みの事前動画と背景を S3・ローカル DB・Aurora へ反映する。"""

from __future__ import annotations

import argparse
import datetime
from pathlib import Path
import subprocess
import sys
from typing import Any, Iterable

import boto3

from common import (
    BASE,
    DURATIONS,
    ROOT,
    SET_CODE,
    WORK,
    load_json,
    local_connection,
    utc_now,
)


class ManifestValidationError(ValueError):
    """承認対象のビルド生成物が publish 条件を満たさないことを表す。"""

    def __init__(self, errors: Iterable[str]) -> None:
        self.errors = list(errors)
        super().__init__(" / ".join(self.errors))


def _sql_literal(value: str) -> str:
    """生成 SQL 用の MySQL 文字列リテラルを返す。"""
    return "'" + value.replace("\\", "\\\\").replace("'", "''") + "'"


def parse_approved_file(path: Path) -> list[str]:
    """空行とコメントを除き、承認済み content_key を読み取る。"""
    return [
        line.strip()
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip() and not line.lstrip().startswith("#")
    ]


def _artifact_path(value: str, base: Path) -> Path:
    """manifest のリポジトリ相対パスを安全な絶対パスにする。"""
    path = Path(value)
    resolved = path.resolve() if path.is_absolute() else (base / path).resolve()
    try:
        resolved.relative_to(base.resolve())
    except ValueError as exc:
        raise ValueError(f"生成物パスがツーリング外を指しています: {value}") from exc
    return resolved


def validate_manifest(
    manifest: dict[str, Any],
    approved: Iterable[str],
    *,
    base: Path = BASE,
) -> list[dict[str, Any]]:
    """承認対象を一括検査し、publish 用の正規化済み情報を返す。

    S3 や DB に触れる前に全件を検査するため、1 件の欠落で部分 publish にならない。

    Raises:
        ManifestValidationError: 台帳またはローカル生成物に不備がある場合。
    """
    approved_keys = list(approved)
    errors: list[str] = []
    if len(approved_keys) != len(set(approved_keys)):
        errors.append("承認ファイルに重複した content_key があります")
    targets: list[dict[str, Any]] = []
    for content_key in approved_keys:
        record = manifest.get(content_key)
        if not isinstance(record, dict):
            errors.append(f"{content_key}: manifest に存在しません")
            continue
        if record.get("content_key") != content_key:
            errors.append(f"{content_key}: manifest 内の content_key が一致しません")
        audio_asset_id = record.get("audio_asset_id")
        if not isinstance(audio_asset_id, int):
            errors.append(
                f"{content_key}: audio_asset_id がありません"
                "（--no-bgm は publish 不可）"
            )
        bgm_s3_key = record.get("bgm_s3_key")
        if not isinstance(bgm_s3_key, str) or not bgm_s3_key:
            errors.append(f"{content_key}: bgm_s3_key がありません")
        durations = record.get("durations")
        if not isinstance(durations, dict) or not durations:
            errors.append(f"{content_key}: ビルド済み尺がありません")
            continue
        normalized_durations: dict[str, dict[str, Any]] = {}
        for duration, detail in durations.items():
            if duration not in DURATIONS or not isinstance(detail, dict):
                errors.append(f"{content_key}: 不正な尺記録です: {duration}")
                continue
            video_value = detail.get("video")
            if not isinstance(video_value, str):
                errors.append(f"{content_key} {duration}: video パスがありません")
                continue
            try:
                video_path = _artifact_path(video_value, base)
            except ValueError as exc:
                errors.append(f"{content_key} {duration}: {exc}")
                continue
            if not video_path.is_file():
                errors.append(f"{content_key} {duration}: MP4 がありません: {video_path}")
            normalized_durations[duration] = {**detail, "video_path": video_path}
        background_path = base / "work" / "backgrounds" / f"{content_key}.png"
        if not background_path.is_file():
            errors.append(f"{content_key}: 背景 PNG がありません: {background_path}")
        targets.append(
            {
                **record,
                "content_key": content_key,
                "durations": normalized_durations,
                "background_path": background_path,
            }
        )
    if errors:
        raise ManifestValidationError(errors)
    return targets


def _built_at_text(built_at: datetime.datetime | str) -> str:
    """datetime または文字列を SQL 用 UTC DATETIME 文字列へ揃える。"""
    if isinstance(built_at, datetime.datetime):
        return built_at.strftime("%Y-%m-%d %H:%M:%S")
    return built_at


def generate_aurora_sql(
    targets: Iterable[dict[str, Any]], built_at: datetime.datetime | str
) -> str:
    """content_key と BGM の S3 キーだけに依存する Aurora UPDATE を生成する。"""
    timestamp = _built_at_text(built_at)
    lines = [
        "-- S3 アップロード成功後に Aurora へ適用する。",
        "-- 適用後の更新行数が承認件数と一致することを確認する。",
        "-- WHERE は環境非依存の content_key + set_code で解決する。",
    ]
    for target in targets:
        content_key = str(target["content_key"])
        assignments = []
        for duration in DURATIONS:
            if duration in target["durations"]:
                key = f"assets/{SET_CODE}/prebuilt/{content_key}_{duration}.mp4"
                assignments.append(f"r.video_s3_key_{duration} = {_sql_literal(key)}")
        bgm_s3_key = str(target["bgm_s3_key"])
        bgm_s3_literal = _sql_literal(bgm_s3_key)
        assignments.extend(
            [
                "r.video_audio_asset_id = (SELECT a.id FROM audio_assets a "
                "WHERE a.set_id = r.set_id AND "
                f"a.s3_key = {bgm_s3_literal})",
                f"r.video_built_at = {_sql_literal(timestamp)}",
            ]
        )
        lines.append(
            "UPDATE ranking_stock_items r "
            "JOIN batch_sets b ON b.id = r.set_id SET "
            + ", ".join(assignments)
            + f" WHERE b.set_code = {_sql_literal(SET_CODE)}"
            + f" AND r.content_key = {_sql_literal(content_key)}"
            + " AND EXISTS (SELECT 1 FROM audio_assets a "
            + "WHERE a.set_id = r.set_id AND "
            + f"a.s3_key = {bgm_s3_literal});"
        )
    return "\n".join(lines) + "\n"


def _s3_uploads(targets: Iterable[dict[str, Any]], bucket: str) -> None:
    """検査済み生成物を規定キーへアップロードする。"""
    client = boto3.client("s3")
    for target in targets:
        content_key = target["content_key"]
        for duration, detail in target["durations"].items():
            key = f"assets/{SET_CODE}/prebuilt/{content_key}_{duration}.mp4"
            client.upload_file(str(detail["video_path"]), bucket, key)
            print(f"uploaded s3://{bucket}/{key}")
        background_key = f"assets/{SET_CODE}/prebuilt/{content_key}_bg.png"
        client.upload_file(str(target["background_path"]), bucket, background_key)
        print(f"uploaded s3://{bucket}/{background_key}")


def _update_local_database(
    targets: Iterable[dict[str, Any]], built_at: datetime.datetime
) -> None:
    """検査済み対象をローカル MySQL の 1 トランザクションで更新する。"""
    connection = local_connection()
    try:
        with connection.cursor() as cursor:
            for target in targets:
                assignments = []
                parameters: list[Any] = []
                for duration in DURATIONS:
                    if duration in target["durations"]:
                        assignments.append(f"r.video_s3_key_{duration} = %s")
                        parameters.append(
                            f"assets/{SET_CODE}/prebuilt/"
                            f"{target['content_key']}_{duration}.mp4"
                        )
                assignments.extend(
                    ["r.video_audio_asset_id = %s", "r.video_built_at = %s"]
                )
                parameters.extend(
                    [
                        target["audio_asset_id"],
                        built_at,
                        SET_CODE,
                        target["content_key"],
                    ]
                )
                cursor.execute(
                    "UPDATE ranking_stock_items r "
                    "JOIN batch_sets b ON b.id = r.set_id SET "
                    + ", ".join(assignments)
                    + " WHERE b.set_code = %s AND r.content_key = %s",
                    tuple(parameters),
                )
                if cursor.rowcount != 1:
                    raise RuntimeError(
                        f"ローカル DB の更新行数が 1 ではありません: "
                        f"{target['content_key']} ({cursor.rowcount})"
                    )
        connection.commit()
    except Exception:
        connection.rollback()
        raise
    finally:
        connection.close()


def _apply_aurora(sql_path: Path) -> None:
    """共通の Data API 適用スクリプトで生成 SQL を Aurora へ反映する。"""
    script = (
        ROOT / "content" / "ranking-stock" / SET_CODE
        / "common" / "apply_aurora.py"
    )
    completed = subprocess.run(
        [sys.executable, str(script), str(sql_path)], check=False
    )
    if completed.returncode != 0:
        raise RuntimeError(f"Aurora 反映に失敗しました（終了コード {completed.returncode}）")


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--approved-file", type=Path, default=WORK / "approved.txt",
        help="1 行 1 content_key の承認ファイル",
    )
    parser.add_argument("--bucket", required=True, help="アップロード先 S3 バケット")
    parser.add_argument("--dry-run", action="store_true", help="S3・DB を変更せず予定だけ表示する")
    # Aurora 反映は既定で行う（ユーザー Fix 2026-08-12）。S3 とローカル DB だけ更新されて
    # Aurora が取り残される片肺状態を作らないため。SQL だけ欲しいときに --no-aurora を使う。
    parser.add_argument(
        "--no-aurora", dest="aurora", action="store_false",
        help="Aurora へ適用せず SQL の生成だけ行う",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    """承認対象を全件検査してから publish する。"""
    args = _parser().parse_args(argv)
    try:
        approved = parse_approved_file(args.approved_file)
        if not approved:
            raise ManifestValidationError(["承認済み content_key がありません"])
        manifest = load_json(WORK / "build_manifest.json", {})
        if not isinstance(manifest, dict):
            raise ManifestValidationError(["build_manifest.json がオブジェクトではありません"])
        targets = validate_manifest(manifest, approved)
    except (OSError, ValueError) as exc:
        print(f"エラー: {exc}", file=sys.stderr)
        return 1

    built_at = utc_now()
    sql_path = WORK / "update_prebuilt.sql"
    sql_path.parent.mkdir(parents=True, exist_ok=True)
    sql_path.write_text(generate_aurora_sql(targets, built_at), encoding="utf-8")
    for target in targets:
        content_key = target["content_key"]
        updated_columns = []
        for duration, detail in target["durations"].items():
            key = f"assets/{SET_CODE}/prebuilt/{content_key}_{duration}.mp4"
            print(
                f"upload: {detail['video_path']} -> "
                f"s3://{args.bucket}/{key}"
            )
            updated_columns.append(f"video_s3_key_{duration}")
        background_key = f"assets/{SET_CODE}/prebuilt/{content_key}_bg.png"
        print(
            f"upload: {target['background_path']} -> "
            f"s3://{args.bucket}/{background_key}"
        )
        print(
            f"DB UPDATE: set_code={SET_CODE}, content_key={content_key}, "
            f"columns={','.join(updated_columns)}, "
            f"video_audio_asset_id={target['audio_asset_id']}, video_built_at=<UTC>"
        )
    if args.dry_run:
        print(f"dry-run: S3・DB は変更していません。Aurora SQL: {sql_path}")
        return 0

    try:
        _s3_uploads(targets, args.bucket)
        _update_local_database(targets, built_at)
        if args.aurora:
            _apply_aurora(sql_path)
        else:
            print(
                "Aurora へは未反映です（--no-aurora）。次を実行してください:\n"
                f"python content/ranking-stock/{SET_CODE}/common/"
                f"apply_aurora.py {sql_path}"
            )
    except Exception as exc:
        print(f"エラー: {exc}", file=sys.stderr)
        return 1
    print(f"{len(targets)} 件を publish しました")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
