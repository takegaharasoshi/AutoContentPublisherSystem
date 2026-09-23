#!/usr/bin/env python3
"""docs/ を HTTP 配信する簡易サーバー（Tailscale 経由のスマホ閲覧用）。

HTML 設計書・計画書はそのまま配信する。Markdown は text/plain で返す
（Phase 18 で計画・記録も HTML 化済み。現役ドキュメントに .md は無く、_archive の旧設計書閲覧用に残置）。
"""

from __future__ import annotations

import argparse
import functools
import http.server
import os
from pathlib import Path
import re

DOCS_DIR = Path(__file__).resolve().parent.parent / "docs"

_CHARSET_TYPES = frozenset(
    {"text/html", "text/css", "text/javascript", "application/javascript"}
)

_RANGE_RE = re.compile(r"bytes=(\d*)-(\d*)")


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

    def send_head(self):  # type: ignore[override]
        """単一の ``Range: bytes=`` 要求に 206 で応える（それ以外は既定動作）。

        iOS Safari は Range に 206 で応えないサーバーの MP4 を再生しないため、
        レビュー HTML の動画（``content/**/work/videos/``）をスマホで見るのに要る。
        """
        range_header = self.headers.get("Range", "")
        path = self.translate_path(self.path)
        match = _RANGE_RE.fullmatch(range_header.strip())
        if not match or not os.path.isfile(path):
            return super().send_head()
        size = os.path.getsize(path)
        start_text, end_text = match.groups()
        if start_text:
            start = int(start_text)
            end = min(int(end_text), size - 1) if end_text else size - 1
        elif end_text:
            start, end = max(size - int(end_text), 0), size - 1
        else:
            return super().send_head()
        if start >= size or start > end:
            self.send_response(416)
            self.send_header("Content-Range", f"bytes */{size}")
            self.end_headers()
            return None
        body = open(path, "rb")
        body.seek(start)
        self._range_remaining = end - start + 1
        self.send_response(206)
        self.send_header("Content-Type", self.guess_type(path))
        self.send_header("Accept-Ranges", "bytes")
        self.send_header("Content-Range", f"bytes {start}-{end}/{size}")
        self.send_header("Content-Length", str(self._range_remaining))
        self.end_headers()
        return body

    def copyfile(self, source, outputfile) -> None:  # type: ignore[override]
        """Range 応答では要求された長さだけ送る。"""
        remaining = getattr(self, "_range_remaining", None)
        if remaining is None:
            super().copyfile(source, outputfile)
            return
        self._range_remaining = None
        while remaining > 0:
            chunk = source.read(min(64 * 1024, remaining))
            if not chunk:
                break
            outputfile.write(chunk)
            remaining -= len(chunk)

    def end_headers(self) -> None:
        """キャッシュ禁止のヘッダを足してからヘッダを閉じる。

        既定の ``SimpleHTTPRequestHandler`` は ``Cache-Control`` を返さないため、
        スマホのブラウザーが ``Last-Modified`` からの経験則でキャッシュを効かせ、
        ``style.css`` を更新しても古い版が使われ続けることがある
        （24-3 の実機確認で発生。24-1・24-2 の CSS が端末に届いていなかった）。
        設計書は閲覧専用・ローカル配信のみのため、常に再取得させる。
        """
        self.send_header("Cache-Control", "no-store, no-cache, must-revalidate")
        self.send_header("Pragma", "no-cache")
        self.send_header("Expires", "0")
        super().end_headers()


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
