"""logic-training-1 の対象抽出と Remotion 動画ビルドを実行する。"""

from __future__ import annotations

import argparse
import os
from pathlib import Path
import shutil
import struct
import subprocess
import sys
from typing import Any, Iterable

from common import (
    BASE,
    REMOTION_DIR,
    ROOT,
    SET_CODE,
    WORK,
    dump_json,
    fetch_unbuilt_items,
    load_json,
    local_connection,
    resolve_slots,
    utc_now,
)


SCRIPTS_DIR = REMOTION_DIR / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from spec import COMPOSITION_ID, STILL_FRAMES  # noqa: E402


FONT_FILES = ("NotoSansJP-Regular.otf", "NotoSansJP-Bold.otf")
FONT_SOURCE = (
    ROOT / "content" / "video-build" / "pref-ranking-1"
    / "remotion" / "public" / "fonts"
)
COACH_FILES = (
    "coach_hook.png",
    "coach_question.png",
    "coach_think.png",
    "coach_answer.png",
)
PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"


class PropsValidationError(ValueError):
    """ストック行を Remotion props へ変換できないことを表す。"""

    def __init__(self, errors: Iterable[str]) -> None:
        self.errors = list(errors)
        super().__init__(" / ".join(self.errors))


def validate_props_input(item: dict[str, Any], slot: dict[str, Any]) -> list[str]:
    """props 組み立てに必要な値を検査する純関数。"""
    errors: list[str] = []
    question = item.get("question_text")
    if not isinstance(question, str) or not question.strip():
        errors.append("question_text が空です")

    fields = item.get("content_fields")
    if not isinstance(fields, dict):
        errors.append("content_fields がオブジェクトではありません")
        fields = {}
    hint = fields.get("hint")
    if not isinstance(hint, str) or not hint.strip():
        errors.append("content_fields.hint が空です")

    for key in ("slot_code", "slot_label", "slot_hook"):
        value = slot.get(key)
        if not isinstance(value, str) or not value.strip():
            errors.append(f"slot.{key} が空です")
    return errors


def build_props(
    item: dict[str, Any],
    slot: dict[str, Any],
    *,
    illustration_src: str,
    illustration_width: int,
    illustration_height: int,
) -> dict[str, Any]:
    """ストック行から Remotion の ``QuizProps`` を組み立てる。"""
    errors = validate_props_input(item, slot)
    if errors:
        raise PropsValidationError(errors)
    return {
        "slotCode": slot["slot_code"],
        "slotLabel": slot["slot_label"],
        "slotHook": slot["slot_hook"],
        "question": item["question_text"],
        "hint": item["content_fields"]["hint"],
        "illustrationSrc": illustration_src,
        "illustrationWidth": illustration_width,
        "illustrationHeight": illustration_height,
    }


def resolve_bgm_source(item: dict[str, Any], *, rebuild: bool) -> int | None:
    """既存 BGM を引き継ぐか、新規 LRU 選曲を行うか決める。"""
    if not rebuild:
        return None
    existing_id = item.get("video_audio_asset_id")
    if existing_id is None:
        raise ValueError("再ビルド元の video_audio_asset_id が NULL です")
    return int(existing_id)


def select_items(
    items: list[dict[str, Any]], item_ids: list[int] | None
) -> list[dict[str, Any]]:
    """CLI で指定された stock item のみに対象を絞る。"""
    if not item_ids:
        return list(items)
    requested = set(item_ids)
    known = {int(item["id"]) for item in items}
    unknown = sorted(requested - known)
    if unknown:
        values = ", ".join(str(item_id) for item_id in unknown)
        raise ValueError(f"対象一覧にない quiz_stock_items.id です: {values}")
    return [item for item in items if int(item["id"]) in requested]


def filter_by_slots(
    items: list[dict[str, Any]],
    slots: dict[tuple[str, str], dict[str, str]],
    slot_codes: list[str] | None,
) -> list[dict[str, Any]]:
    """CLI で指定されたスロットの対象のみに絞る。

    昼（noon）が凍結中のように、稼働スロットだけを再ビルドしたい場合に使う。
    """
    if not slot_codes:
        return list(items)
    requested = set(slot_codes)
    known = {slot["slot_code"] for slot in slots.values()}
    unknown = sorted(requested - known)
    if unknown:
        values = ", ".join(unknown)
        raise ValueError(f"prompt_configs にない slot_code です: {values}")
    return [
        item
        for item in items
        if _slot_for(item, slots)["slot_code"] in requested
    ]


def _png_size(path: Path) -> tuple[int, int]:
    """PNG の IHDR チャンクからピクセル寸法を読む。"""
    header = path.read_bytes()[:24]
    if (
        len(header) < 24
        or header[:8] != PNG_SIGNATURE
        or header[12:16] != b"IHDR"
    ):
        raise RuntimeError(f"PNG ではありません: {path}")
    width, height = struct.unpack(">II", header[16:24])
    if width == 0 or height == 0:
        raise RuntimeError(f"PNG の寸法が不正です: {path}")
    return int(width), int(height)


def _container_path(path: Path) -> str:
    """リポジトリ内のホストパスを /repo マウント上へ変換する。"""
    relative = path.resolve().relative_to(ROOT.resolve())
    return (Path("/repo") / relative).as_posix()


def _run_command(command: list[str], label: str) -> subprocess.CompletedProcess[str]:
    """外部コマンドを実行し、失敗時に末尾の診断を含む例外を送出する。"""
    print(f"\n=== {label}\n$ {' '.join(command)}", flush=True)
    try:
        completed = subprocess.run(
            command, capture_output=True, text=True, check=False
        )
    except FileNotFoundError as exc:
        raise RuntimeError(f"{label} を起動できません: {exc}") from exc
    output = (completed.stdout + completed.stderr).strip()
    tail = "\n".join(output.splitlines()[-20:])
    if completed.returncode != 0:
        raise RuntimeError(
            f"{label} が失敗しました（{completed.returncode}）:\n{tail}"
        )
    if tail:
        print(tail, flush=True)
    return completed


def _docker(
    image: str,
    inner: list[str],
    *,
    entrypoint: str | None = None,
) -> list[str]:
    """リポジトリと AWS 設定を共有する docker run コマンドを組む。"""
    command = [
        "docker",
        "run",
        "--rm",
        "-v",
        f"{ROOT}:/repo",
        "-v",
        f"{Path.home()}/.aws:/aws-config:ro",
        "-w",
        _container_path(REMOTION_DIR),
        "-e",
        "HOME=/tmp",
        "-e",
        f"S3_BUCKET_NAME={os.environ.get('S3_BUCKET_NAME', '')}",
        "-e",
        "AWS_SHARED_CREDENTIALS_FILE=/aws-config/credentials",
        "-e",
        "AWS_CONFIG_FILE=/aws-config/config",
        "-e",
        "AWS_DEFAULT_REGION=ap-northeast-1",
        "--user",
        f"{os.getuid()}:{os.getgid()}",
    ]
    if entrypoint is not None:
        command.extend(("--entrypoint", entrypoint))
    return command + [image] + inner


def _stage_fonts() -> None:
    """姉妹セットのフォントを、存在しない場合だけ配置する。"""
    destination = REMOTION_DIR / "public" / "fonts"
    destination.mkdir(parents=True, exist_ok=True)
    for name in FONT_FILES:
        target = destination / name
        if target.is_file():
            continue
        source = FONT_SOURCE / name
        if not source.is_file():
            raise RuntimeError(f"フォントがありません: {source}")
        shutil.copyfile(source, target)
        print(f"font staged: {name}")


def _stage_coaches(ffmpeg_image: str, *, skip: bool, dry_run: bool) -> None:
    """不足時に限りコーチ立ち絵をコンテナ内で取得する。"""
    coach_dir = REMOTION_DIR / "public" / "coach"
    if skip or dry_run or all((coach_dir / name).is_file() for name in COACH_FILES):
        return
    _run_command(
        _docker(
            ffmpeg_image,
            ["scripts/fetch_assets.py"],
            entrypoint="python",
        ),
        "コーチ立ち絵の取得",
    )


def _select_bgm(
    connection: Any,
    slot_code: str,
    *,
    existing_id: int | None = None,
) -> tuple[int, str]:
    """必須 SE を確認し、既存 ID または時間帯別 LRU で BGM を解決する。"""
    with connection.cursor() as cursor:
        cursor.execute("SELECT id FROM batch_sets WHERE set_code = %s", (SET_CODE,))
        set_row = cursor.fetchone()
        if set_row is None:
            raise RuntimeError(f"batch_sets がありません: {SET_CODE}")
        set_id = int(set_row[0])
        cursor.execute(
            "SELECT s3_key FROM audio_assets WHERE set_id = %s "
            "AND asset_type = 'se' AND is_active = 1",
            (set_id,),
        )
        se_keys = {str(row[0]) for row in cursor.fetchall()}
        required_se = {
            f"audio/{SET_CODE}/se/countdown_tick.m4a",
            f"audio/{SET_CODE}/se/answer_chime.m4a",
        }
        if not required_se <= se_keys:
            raise RuntimeError("必須 SE が audio_assets に登録されていません")
        if existing_id is None:
            cursor.execute(
                "SELECT id, s3_key FROM audio_assets WHERE set_id = %s "
                "AND asset_type = 'bgm' AND is_active = 1 "
                "AND (time_slot = %s OR time_slot IS NULL) "
                "ORDER BY last_used_at ASC, id ASC LIMIT 1",
                (set_id, slot_code),
            )
        else:
            cursor.execute(
                "SELECT id, s3_key FROM audio_assets WHERE id = %s",
                (existing_id,),
            )
        row = cursor.fetchone()
    if row is None:
        if existing_id is None:
            raise RuntimeError(f"スロット {slot_code} 用の有効な BGM がありません")
        raise RuntimeError(
            f"引き継ぎ用 BGM が見つかりません: audio_asset_id={existing_id}"
        )
    return int(row[0]), str(row[1])


def _record_bgm_use(connection: Any, bgm_id: int) -> None:
    """動画完成後にだけ BGM の LRU 使用日時を記録する。"""
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                "UPDATE audio_assets SET last_used_at = %s WHERE id = %s",
                (utc_now(), bgm_id),
            )
            if cursor.rowcount != 1:
                raise RuntimeError(f"BGM の使用日時を更新できません: {bgm_id}")
        connection.commit()
    except Exception:
        connection.rollback()
        raise


def _render(props_path: Path, output_path: Path, image: str) -> None:
    """Remotion コンテナで無音の 16 秒動画をレンダリングする。"""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    _run_command(
        _docker(
            image,
            [
                "npx",
                "remotion",
                "render",
                "src/index.ts",
                COMPOSITION_ID,
                _container_path(output_path),
                f"--props={_container_path(props_path)}",
                "--concurrency=3",
                "--timeout=120000",
            ],
        ),
        "Remotion レンダリング（映像のみ）",
    )


def _mix_audio(
    silent_path: Path,
    bgm_s3_key: str,
    output_path: Path,
    stills_dir: Path,
    image: str,
) -> None:
    """ffmpeg コンテナで音声を付け、レビュー用スチルを抽出する。"""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    stills_dir.mkdir(parents=True, exist_ok=True)
    _run_command(
        _docker(
            image,
            [
                "scripts/mix_audio.py",
                "--video",
                _container_path(silent_path),
                "--bgm-key",
                bgm_s3_key,
                "--output",
                _container_path(output_path),
                "--stills-dir",
                _container_path(stills_dir),
            ],
            entrypoint="python",
        ),
        "音声ミックス・スチル抽出",
    )


def _parser() -> argparse.ArgumentParser:
    """ビルド用 CLI パーサーを返す。"""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--rebuild",
        action="store_true",
        help="ビルド済み行を既存 BGM のまま再ビルドする",
    )
    parser.add_argument(
        "--item",
        action="append",
        type=int,
        metavar="ID",
        help="対象 quiz_stock_items.id（複数指定可）",
    )
    parser.add_argument("--list", action="store_true", help="対象一覧を表示して終了する")
    parser.add_argument(
        "--slot",
        action="append",
        metavar="SLOT_CODE",
        help="対象スロット（morning / noon / night。複数指定可）",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="props 生成まで行いレンダリングを省略する",
    )
    parser.add_argument(
        "--skip-assets",
        action="store_true",
        help="コーチ立ち絵の S3 再取得を省略する",
    )
    return parser


def _slot_for(
    item: dict[str, Any],
    slots: dict[tuple[str, str], dict[str, str]],
) -> dict[str, str]:
    """ストック行に対応する一意なスロットを返す。"""
    key = (item["quiz_type"], item["difficulty"])
    slot = slots.get(key)
    if slot is None:
        raise RuntimeError(
            f"stock item {item['id']} のスロットが一意に決まりません: {key}"
        )
    return slot


def _relative(path: Path) -> str:
    """台帳へ保存する BASE 相対 POSIX パスを返す。"""
    return path.relative_to(BASE).as_posix()


def main(argv: list[str] | None = None) -> int:
    """対象を最後まで処理し、失敗をまとめて報告する。"""
    args = _parser().parse_args(argv)
    if not args.dry_run and not os.environ.get("S3_BUCKET_NAME"):
        print("エラー: S3_BUCKET_NAME が必要です", file=sys.stderr)
        return 1

    try:
        connection = local_connection()
    except Exception as exc:
        print(f"エラー: ローカル DB へ接続できません: {exc}", file=sys.stderr)
        return 1

    try:
        try:
            slots = resolve_slots(connection)
            items = select_items(
                fetch_unbuilt_items(connection, rebuild=args.rebuild),
                args.item,
            )
            items = filter_by_slots(items, slots, args.slot)
        except Exception as exc:
            print(f"エラー: 対象を解決できません: {exc}", file=sys.stderr)
            return 1

        if args.list:
            try:
                for item in items:
                    slot = _slot_for(item, slots)
                    print(
                        f"{item['id']}\t{item['content_key']}\t"
                        f"{slot['slot_code']}\t{item['question_text']}"
                    )
            except Exception as exc:
                print(f"エラー: 対象を表示できません: {exc}", file=sys.stderr)
                return 1
            print(f"対象: {len(items)} 件")
            return 0

        try:
            manifest = load_json(WORK / "build_manifest.json", {})
            if not isinstance(manifest, dict):
                raise RuntimeError(
                    "work/build_manifest.json は JSON オブジェクトにしてください"
                )
            _stage_fonts()
            remotion_image = os.environ.get("REMOTION_IMAGE", "remotion-render")
            ffmpeg_image = os.environ.get(
                "FFMPEG_IMAGE", "image-batch:ffmpeg-check"
            )
            _stage_coaches(
                ffmpeg_image,
                skip=args.skip_assets,
                dry_run=args.dry_run,
            )
        except Exception as exc:
            print(f"エラー: ビルド資材を準備できません: {exc}", file=sys.stderr)
            return 1

        failures: list[str] = []
        for item in items:
            stock_id = int(item["id"])
            illustration = WORK / "illustrations" / f"{stock_id}.png"
            if not illustration.is_file():
                print(f"{stock_id}: illustration missing; skipped")
                continue
            try:
                slot = _slot_for(item, slots)
                staged = (
                    REMOTION_DIR / "public" / "illustrations" / f"{stock_id}.png"
                )
                staged.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(illustration, staged)
                width, height = _png_size(staged)
                props_path = WORK / "props" / f"{stock_id}.json"
                props = build_props(
                    item,
                    slot,
                    illustration_src=f"illustrations/{stock_id}.png",
                    illustration_width=width,
                    illustration_height=height,
                )
                dump_json(props_path, props)
                if args.dry_run:
                    print(f"{stock_id}: props 生成 OK（dry-run）")
                    continue

                existing_id = resolve_bgm_source(item, rebuild=args.rebuild)
                bgm_id, bgm_s3_key = _select_bgm(
                    connection,
                    slot["slot_code"],
                    existing_id=existing_id,
                )
                silent_path = WORK / "silent" / f"{stock_id}.mp4"
                video_path = WORK / "videos" / f"{stock_id}.mp4"
                stills_dir = WORK / "cuts"
                _render(props_path, silent_path, remotion_image)
                _mix_audio(
                    silent_path,
                    bgm_s3_key,
                    video_path,
                    stills_dir,
                    ffmpeg_image,
                )
                if not args.rebuild:
                    _record_bgm_use(connection, bgm_id)

                stills = {
                    key: _relative(stills_dir / f"{stock_id}_{key}.png")
                    for key in STILL_FRAMES
                }
                manifest[str(stock_id)] = {
                    "audio_asset_id": bgm_id,
                    "bgm_s3_key": bgm_s3_key,
                    "content_key": item["content_key"],
                    "question_text": item["question_text"],
                    "slot_code": slot["slot_code"],
                    "hint": props["hint"],
                    "renderer": "remotion",
                    "props": _relative(props_path),
                    "video": _relative(video_path),
                    "stills": stills,
                }
                dump_json(WORK / "build_manifest.json", manifest)
                print(f"{stock_id}: built with BGM {bgm_id}")
            except Exception as exc:
                failures.append(f"{stock_id}: {exc}")

        if failures:
            print("\n失敗一覧:", file=sys.stderr)
            for failure in failures:
                print(f"- {failure}", file=sys.stderr)
            return 1
        print(f"完了: {len(items)} 件")
        return 0
    finally:
        connection.close()


if __name__ == "__main__":
    raise SystemExit(main())
