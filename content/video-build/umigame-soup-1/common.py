"""umigame-soup-1 動画ビルドツールの共通定数と入出力。"""

from __future__ import annotations

import importlib.util
import json
import os
from pathlib import Path
import tempfile
from typing import Any, Iterable


SET_CODE = "umigame-soup-1"
HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
WORK = HERE / "work"
REMOTION_DIR = HERE / "remotion"
ASSETS_DIR = HERE / "assets"
MANIFEST_PATH = WORK / "manifest.json"

FPS = 30
TOTAL_FRAMES = 720
NARRATION_START = 15
NARRATION_GAP = 36
NARRATION_BUDGET_SECONDS = 21.0


def _stock_path(batch: str) -> Path:
    """指定バッチの正本ファイルを返す。"""
    if not batch or Path(batch).name != batch:
        raise ValueError(f"不正な batch 名です: {batch}")
    path = ROOT / "content" / "umigame-stock" / SET_CODE / batch / "stock_items.py"
    if not path.is_file():
        raise ValueError(f"ストックがありません: {path}")
    return path


def load_items(batch: str = "batch-01") -> list[dict[str, Any]]:
    """``stock_items.py`` の ITEMS を読み、content_key の一意性を検査する。"""
    path = _stock_path(batch)
    spec = importlib.util.spec_from_file_location(
        f"umigame_stock_{batch.replace('-', '_')}", path
    )
    if spec is None or spec.loader is None:
        raise RuntimeError(f"ストックを読み込めません: {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    items = getattr(module, "ITEMS", None)
    if not isinstance(items, list):
        raise ValueError(f"ITEMS が配列ではありません: {path}")
    keys: list[str] = []
    for index, item in enumerate(items, start=1):
        if not isinstance(item, dict):
            raise ValueError(f"ITEMS[{index}] が dict ではありません")
        key = item.get("content_key")
        if not isinstance(key, str) or not key:
            raise ValueError(f"ITEMS[{index}].content_key がありません")
        keys.append(key)
    duplicates = sorted({key for key in keys if keys.count(key) > 1})
    if duplicates:
        raise ValueError(f"content_key が重複しています: {', '.join(duplicates)}")
    return items


def select_items(
    items: Iterable[dict[str, Any]], content_keys: Iterable[str] | None
) -> list[dict[str, Any]]:
    """指定キーだけを正本順で返し、未知キーはエラーにする。"""
    values = list(items)
    if content_keys is None:
        return values
    requested = list(dict.fromkeys(content_keys))
    known = {str(item.get("content_key")) for item in values}
    unknown = sorted(set(requested) - known)
    if unknown:
        raise ValueError(f"未知の content_key です: {', '.join(unknown)}")
    selected = set(requested)
    return [item for item in values if item["content_key"] in selected]


def video_s3_key(content_key: str) -> str:
    """完成 MP4 の S3 キーを返す。"""
    return f"assets/{SET_CODE}/prebuilt/{content_key}.mp4"


def background_s3_key(content_key: str) -> str:
    """背景原画 PNG の S3 キーを返す。"""
    return f"assets/{SET_CODE}/prebuilt/{content_key}_bg.png"


def load_manifest(path: Path = MANIFEST_PATH) -> dict[str, Any]:
    """manifest を読み、未作成なら空オブジェクトを返す。"""
    if not path.is_file():
        return {}
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"manifest は JSON オブジェクトにしてください: {path}")
    return value


def save_manifest(manifest: dict[str, Any], path: Path = MANIFEST_PATH) -> None:
    """manifest を同一ディレクトリ内の一時ファイル経由でアトミック保存する。"""
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary = tempfile.mkstemp(
        prefix=f".{path.name}.", suffix=".tmp", dir=str(path.parent)
    )
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8") as stream:
            json.dump(manifest, stream, ensure_ascii=False, indent=2)
            stream.write("\n")
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
    except Exception:
        try:
            os.unlink(temporary)
        except FileNotFoundError:
            pass
        raise


def write_json(path: Path, value: Any) -> None:
    """UTF-8・末尾改行付きで JSON を書く。"""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
