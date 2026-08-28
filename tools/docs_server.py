#!/usr/bin/env python3
"""docs/ を HTTP 配信する簡易サーバー（Tailscale 経由のスマホ閲覧用）。

HTML 設計書・計画書はそのまま配信する。Markdown は text/plain で返す
（Phase 18 で計画・記録も HTML 化済み。現役ドキュメントに .md は無く、_archive の旧設計書閲覧用に残置）。
"""

from __future__ import annotations

import argparse
import functools
import http.server
from pathlib import Path

DOCS_DIR = Path(__file__).resolve().parent.parent / "docs"

_CHARSET_TYPES = frozenset(
    {"text/html", "text/css", "text/javascript", "application/javascript"}
)


class DocsRequestHandler(http.server.SimpleHTTPRequestHandler):
    """Markdown を text/plain で返し、テキスト系に UTF-8 を明示するハンドラ。"""

    def guess_type(self, path: str) -> str:
        """レスポンスの Content-Type を決定する。

        Args:
            path: 配信対象のファイルパス。

        Returns:
            Content-Type ヘッダに設定する文字列。
        """
        if path.endswith(".md"):
            return "text/plain; charset=utf-8"
        ctype = super().guess_type(path)
        if ctype in _CHARSET_TYPES:
            return f"{ctype}; charset=utf-8"
        return ctype


def main() -> None:
    """コマンドライン引数を解釈してサーバーを起動する。"""
    parser = argparse.ArgumentParser(description="設計書（docs/）を HTTP 配信する")
    parser.add_argument("--port", type=int, default=8765, help="待ち受けポート")
    parser.add_argument(
        "--bind",
        default="127.0.0.1",
        help="待ち受けアドレス（既定はループバックのみ）",
    )
    parser.add_argument(
        "--root",
        type=Path,
        default=DOCS_DIR,
        help="配信ルート（既定は docs/。レビュー HTML 等を見せるときだけ別ポートで指定する）",
    )
    args = parser.parse_args()

    root = args.root.resolve()
    handler = functools.partial(DocsRequestHandler, directory=str(root))
    with http.server.ThreadingHTTPServer((args.bind, args.port), handler) as httpd:
        print(f"serving {root} on http://{args.bind}:{args.port}/", flush=True)
        httpd.serve_forever()


if __name__ == "__main__":
    main()
