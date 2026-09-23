"""imagegen の背景原画を Remotion 用 1080x1920 JPEG に正規化する。"""

from __future__ import annotations

import argparse
import sys
from typing import Any

from common import WORK, load_items, select_items
from scripts.prepare_assets import prepare_background


def intake_backgrounds(items: list[dict[str, Any]]) -> list[str]:
    """対象背景を中央クロップの cover で JPEG 化する。"""
    raw = WORK / "backgrounds" / "raw"
    output = WORK / "backgrounds"
    missing = [
        str(item["content_key"])
        for item in items
        if not (raw / f"{item['content_key']}.png").is_file()
    ]
    if missing:
        raise ValueError("背景原画 PNG がありません: " + ", ".join(missing))
    output.mkdir(parents=True, exist_ok=True)
    completed: list[str] = []
    for item in items:
        key = str(item["content_key"])
        prepare_background(raw / f"{key}.png", output / f"{key}.jpg")
        completed.append(key)
    return completed


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--batch", default="batch-01")
    parser.add_argument("--content-key", action="append", dest="content_keys")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    try:
        targets = select_items(load_items(args.batch), args.content_keys)
        completed = intake_backgrounds(targets)
    except (OSError, ValueError) as exc:
        print(f"エラー: {exc}", file=sys.stderr)
        return 1
    print(f"{len(completed)} 件の背景を正規化しました: {WORK / 'backgrounds'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
