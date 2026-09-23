"""ストックの背景イラスト用プロンプトを 1 問 1 ファイルで書き出す。"""

from __future__ import annotations

import argparse
import sys
from typing import Any

from common import WORK, load_items, select_items


def export_prompts(items: list[dict[str, Any]]) -> list[str]:
    """対象ストックの ``illustration_prompt`` を改変せずに書き出す。"""
    output = WORK / "prompts"
    output.mkdir(parents=True, exist_ok=True)
    written: list[str] = []
    for item in items:
        prompt = item.get("illustration_prompt")
        if not isinstance(prompt, str) or not prompt.strip():
            raise ValueError(f"{item['content_key']}: illustration_prompt がありません")
        key = str(item["content_key"])
        (output / f"{key}.txt").write_text(prompt.rstrip("\n") + "\n", encoding="utf-8")
        written.append(key)
    return written


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--batch", default="batch-01")
    parser.add_argument("--content-key", action="append", dest="content_keys")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    try:
        targets = select_items(load_items(args.batch), args.content_keys)
        keys = export_prompts(targets)
    except (OSError, ValueError) as exc:
        print(f"エラー: {exc}", file=sys.stderr)
        return 1
    print(f"{len(keys)} 件のプロンプトを書き出しました: {WORK / 'prompts'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
