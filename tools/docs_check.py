#!/usr/bin/env python3
"""設計書 HTML（docs/）の機械検証ツール。

Phase 24-1 で新設。アーカイブ（``docs/_archive/``）を除く現役 HTML について、
次の 3 つを確認する。

1. 対象ページと表の件数（実行時に再集計する。固定の期待件数は持たない）
2. リンク / アンカーの整合（相対 href・src の参照先ファイルと ``#id`` の実在）
3. 指定幅でのページ全体の横はみ出し（ヘッドレス Chrome で実測）

横はみ出し判定はヘッドレスブラウザーを使う。使えない環境ではその旨を出力し、
静的チェックのみで終了する（未確認を合格扱いにしない）。

使い方::

    python3 tools/docs_check.py                        # 全チェック
    python3 tools/docs_check.py --no-browser           # 静的チェックのみ
    python3 tools/docs_check.py --baseline HEAD        # 既存不備と今回の差分を区別
    python3 tools/docs_check.py --widths 360,768       # 幅を指定
"""

from __future__ import annotations

import argparse
import html
import http.server
import json
import os
import posixpath
import re
import shutil
import socketserver
import subprocess
import sys
import threading
import time
from dataclasses import dataclass
from html.parser import HTMLParser
from pathlib import Path
from typing import Iterable, Sequence
from urllib.parse import unquote, urlsplit

REPO_ROOT = Path(__file__).resolve().parent.parent
EXCLUDED_DIRS = {"_archive"}
DEFAULT_WIDTHS = (360, 390, 430, 767, 768, 1280)

CHROME_CANDIDATES = (
    "/mnt/c/Program Files/Google/Chrome/Application/chrome.exe",
    "/mnt/c/Program Files (x86)/Google/Chrome/Application/chrome.exe",
    "/mnt/c/Program Files (x86)/Microsoft/Edge/Application/msedge.exe",
    "/mnt/c/Program Files/Microsoft/Edge/Application/msedge.exe",
)
CHROME_COMMANDS = ("google-chrome", "google-chrome-stable", "chromium", "chromium-browser")

REF_ATTRS = {"href", "src"}


class PageParser(HTMLParser):
    """HTML を実タグとして走査し、参照・id・表の数を集める。

    ``<code>`` 内のコード例のようにエスケープされた記述はタグにならないため、
    正規表現と違って誤検出しない。
    """

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.refs: list[str] = []
        self.ids: list[str] = []
        self.tables = 0

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag == "table":
            self.tables += 1
        for name, value in attrs:
            if value is None:
                continue
            if name == "id":
                self.ids.append(value)
            elif name in REF_ATTRS:
                self.refs.append(value)

    def handle_startendtag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        self.handle_starttag(tag, attrs)


def parse_page(text: str) -> PageParser:
    """HTML を解析して参照・id・表の数を返す。"""
    parser = PageParser()
    parser.feed(text)
    parser.close()
    return parser


@dataclass(frozen=True)
class Finding:
    """静的チェックの指摘 1 件。

    Attributes:
        page: リポジトリルートからの相対パス。
        kind: 指摘の種別（``missing-file`` / ``missing-anchor`` / ``duplicate-id``）。
        detail: 指摘の内容（参照文字列など）。
    """

    page: str
    kind: str
    detail: str

    def line(self) -> str:
        """1 行表示に整形する。"""
        return f"{self.page}: [{self.kind}] {self.detail}"


class Tree:
    """検査対象のファイル集合（作業ツリー / git ref）を同じ形で扱うための基底クラス。"""

    def html_pages(self) -> list[str]:
        """アーカイブを除く現役 HTML のリポジトリ相対パスを返す。"""
        raise NotImplementedError

    def read(self, rel: str) -> str:
        """リポジトリ相対パスのテキストを読む。"""
        raise NotImplementedError

    def exists(self, rel: str) -> bool:
        """リポジトリ相対パスのファイル / ディレクトリが存在するか。"""
        raise NotImplementedError


class WorkTree(Tree):
    """作業ツリー（現在のファイル）を対象にする。"""

    def __init__(self, root: Path) -> None:
        self.root = root

    def html_pages(self) -> list[str]:
        docs = self.root / "docs"
        pages = [
            p.relative_to(self.root).as_posix()
            for p in docs.rglob("*.html")
            if not (set(p.relative_to(docs).parts) & EXCLUDED_DIRS)
        ]
        return sorted(pages)

    def read(self, rel: str) -> str:
        return (self.root / rel).read_text(encoding="utf-8")

    def exists(self, rel: str) -> bool:
        return (self.root / rel).exists()


class GitTree(Tree):
    """git ref の内容（追跡ファイル）を対象にする。既存不備の把握に使う。"""

    def __init__(self, root: Path, ref: str) -> None:
        self.root = root
        self.ref = ref
        listing = subprocess.run(
            ["git", "ls-tree", "-r", "--name-only", ref],
            cwd=root,
            capture_output=True,
            text=True,
        )
        if listing.returncode != 0:
            raise RuntimeError(listing.stderr.strip() or f"git ref '{ref}' を読めない")
        self.files = set(listing.stdout.splitlines())
        self.dirs = set()
        for f in self.files:
            parts = f.split("/")
            for i in range(1, len(parts)):
                self.dirs.add("/".join(parts[:i]))

    def html_pages(self) -> list[str]:
        return sorted(
            f
            for f in self.files
            if f.startswith("docs/")
            and f.endswith(".html")
            and not (set(f.split("/")[1:-1]) & EXCLUDED_DIRS)
        )

    def read(self, rel: str) -> str:
        out = subprocess.run(
            ["git", "show", f"{self.ref}:{rel}"], cwd=self.root, capture_output=True
        )
        return out.stdout.decode("utf-8")

    def exists(self, rel: str) -> bool:
        rel = rel.rstrip("/")
        if rel in self.files or rel in self.dirs:
            return True
        # 祖先がシンボリックリンク（git 上は blob）なら、その先は追跡一覧では辿れないため存在扱いにする
        parts = rel.split("/")
        return any("/".join(parts[:i]) in self.files for i in range(1, len(parts)))


def count_tables(text: str) -> int:
    """HTML 内の ``<table>`` の数を数える（コード例は除く）。"""
    return parse_page(text).tables


def check_links(tree: Tree) -> list[Finding]:
    """相対リンクの参照先ファイルとアンカーの実在を確認する。

    Args:
        tree: 検査対象（作業ツリー or git ref）。

    Returns:
        指摘の一覧。外部リンク（http/https/mailto 等）は対象外。
    """
    pages = tree.html_pages()
    parsed = {p: parse_page(tree.read(p)) for p in pages}
    ids_by_page = {p: parsed[p].ids for p in pages}
    findings: list[Finding] = []

    for page in pages:
        seen: set[str] = set()
        for value in ids_by_page[page]:
            if value in seen:
                findings.append(Finding(page, "duplicate-id", f'id="{value}"'))
            seen.add(value)

        base_dir = posixpath.dirname(page)
        for raw in parsed[page].refs:
            ref = raw.strip()
            if not ref or ref.startswith(
                ("http://", "https://", "mailto:", "data:", "//", "javascript:")
            ):
                continue
            parts = urlsplit(ref)
            path_part = unquote(parts.path)
            fragment = unquote(parts.fragment)

            if path_part:
                target = posixpath.normpath(posixpath.join(base_dir, path_part))
                if target.startswith(".."):
                    findings.append(Finding(page, "missing-file", ref))
                    continue
                if not tree.exists(target):
                    findings.append(Finding(page, "missing-file", ref))
                    continue
            else:
                target = page
            if not fragment or not target.endswith(".html"):
                continue  # .md 等の見出しアンカーは対象外
            if target in ids_by_page:
                target_ids = ids_by_page[target]
            else:
                try:
                    target_ids = parse_page(tree.read(target)).ids
                except (OSError, UnicodeDecodeError):
                    findings.append(Finding(page, "missing-file", ref))
                    continue
            if fragment not in target_ids:
                findings.append(Finding(page, "missing-anchor", ref))

    return findings


def find_browser() -> str | None:
    """利用できるヘッドレス Chrome / Edge の実行パスを探す。

    Returns:
        実行パス。見つからなければ ``None``。環境変数 ``DOCS_CHECK_CHROME`` が最優先。
    """
    env = os.environ.get("DOCS_CHECK_CHROME")
    if env and (Path(env).exists() or shutil.which(env)):
        return env
    for command in CHROME_COMMANDS:
        found = shutil.which(command)
        if found:
            return found
    for candidate in CHROME_CANDIDATES:
        if Path(candidate).exists():
            return candidate
    return None


DRIVER_TEMPLATE = """<!DOCTYPE html><html><head><meta charset="utf-8"><title>docs_check</title></head>
<body><pre id="out">PENDING</pre><div id="host"></div><script>
const PAGES = %s, WIDTHS = %s;
function load(src, w) {
  return new Promise(res => {
    const f = document.createElement('iframe');
    f.style.cssText = 'width:' + w + 'px;height:2400px;border:0;';
    f.src = src;
    f.onload = () => setTimeout(() => res(f), 30);
    document.getElementById('host').appendChild(f);
  });
}
async function main() {
  const out = [];
  for (const w of WIDTHS) {
    for (const p of PAGES) {
      const f = await load(p, w);
      const d = f.contentDocument;
      const vw = d.documentElement.clientWidth;
      const sw = Math.max(d.documentElement.scrollWidth, d.body.scrollWidth);
      const rec = {page: p, width: w, vw: vw, over: sw - vw, offenders: []};
      if (rec.over > 1) {
        const scrollable = el => {
          for (let n = el.parentElement; n && n !== d.body; n = n.parentElement) {
            const ox = getComputedStyle(n).overflowX;
            if (ox === 'auto' || ox === 'scroll' || ox === 'hidden') return true;
          }
          return false;
        };
        for (const el of d.querySelectorAll('body *')) {
          const r = el.getBoundingClientRect();
          if (r.width <= 0 || r.right <= vw + 1) continue;
          if (scrollable(el)) continue;
          if ([...el.children].some(c => c.getBoundingClientRect().right > vw + 1)) continue;
          rec.offenders.push({
            tag: el.tagName, cls: (el.className || '').toString().slice(0, 40),
            right: Math.round(r.right), text: (el.textContent || '').trim().slice(0, 60)
          });
        }
        rec.offenders = rec.offenders.slice(0, 5);
      }
      out.push(rec);
      f.remove();
    }
  }
  document.getElementById('out').textContent = JSON.stringify(out);
}
main();
</script></body></html>"""


def _make_handler(root: Path, driver_html: bytes):
    """ドライバーページを合成して返す HTTP ハンドラを作る。"""

    class Handler(http.server.SimpleHTTPRequestHandler):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, directory=str(root), **kwargs)

        def do_GET(self):  # noqa: N802 (http.server の命名に合わせる)
            if self.path.startswith("/__docs_check__"):
                self.send_response(200)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.send_header("Content-Length", str(len(driver_html)))
                self.end_headers()
                self.wfile.write(driver_html)
                return
            super().do_GET()

        def log_message(self, *args):  # noqa: D102
            pass

    return Handler


def measure_overflow(
    pages: Sequence[str], root: Path, widths: Sequence[int], browser: str
) -> list[dict]:
    """指定幅でページ全体の横はみ出しを実測する。

    ローカル HTTP サーバーを立て、同一オリジンの iframe に各ページを読み込んで
    ``scrollWidth`` と ``clientWidth`` を比較する（iframe 幅 = CSS px のビューポート幅）。

    Args:
        pages: 対象の現役 HTML（リポジトリ相対パス）。
        root: HTTP サーバーの公開ルート（リポジトリルート）。
        widths: 測定する CSS px 幅。
        browser: ヘッドレス Chrome / Edge の実行パス。

    Returns:
        ``{page, width, vw, over, offenders}`` の一覧。

    Raises:
        RuntimeError: ブラウザーから測定結果を取得できなかった場合。
    """
    urls = ["/" + rel for rel in pages]
    driver = (DRIVER_TEMPLATE % (json.dumps(urls), json.dumps(list(widths)))).encode("utf-8")

    server = socketserver.ThreadingTCPServer(("0.0.0.0", 0), _make_handler(root, driver))
    port = server.server_address[1]
    threading.Thread(target=server.serve_forever, daemon=True).start()
    time.sleep(1.5)  # WSL からの localhost 転送が張られるのを待つ
    try:
        budget = 20000 + 500 * len(urls) * len(widths)
        proc = subprocess.run(
            [
                browser,
                "--headless=new",
                "--disable-gpu",
                "--no-sandbox",
                "--hide-scrollbars",
                "--window-size=1800,1200",
                f"--virtual-time-budget={budget}",
                "--dump-dom",
                f"http://localhost:{port}/__docs_check__.html",
            ],
            capture_output=True,
            text=True,
            timeout=max(600, budget // 1000 + 300),
        )
    finally:
        server.shutdown()
        server.server_close()

    match = re.search(r'<pre id="out">(.*?)</pre>', proc.stdout, re.S)
    if not match or match.group(1).strip() == "PENDING":
        raise RuntimeError("ヘッドレスブラウザーから測定結果を取得できなかった")
    return json.loads(html.unescape(match.group(1)))


def format_findings(findings: Iterable[Finding]) -> list[str]:
    """指摘を表示用の行に整形する。"""
    return [f.line() for f in sorted(findings, key=lambda f: (f.page, f.kind, f.detail))]


def main(argv: Sequence[str] | None = None) -> int:
    """エントリポイント。

    Returns:
        終了コード（0: 合格 / 1: 不備あり・未確認あり）。
    """
    parser = argparse.ArgumentParser(description="設計書 HTML の機械検証")
    parser.add_argument(
        "--widths",
        default=",".join(str(w) for w in DEFAULT_WIDTHS),
        help="横はみ出しを測定する CSS px 幅（カンマ区切り）",
    )
    parser.add_argument("--no-browser", action="store_true", help="横はみ出し測定を行わない")
    parser.add_argument("--list", action="store_true", help="対象ページを全件列挙する")
    parser.add_argument(
        "--baseline",
        metavar="REF",
        help="指定 git ref の静的チェック結果と比較し、既存不備と今回の差分を区別する",
    )
    args = parser.parse_args(argv)

    widths = [int(w) for w in args.widths.split(",") if w.strip()]
    tree = WorkTree(REPO_ROOT)
    pages = tree.html_pages()
    texts = {p: tree.read(p) for p in pages}
    tables = sum(count_tables(t) for t in texts.values())

    print("=== 1. 対象 ===")
    print(f"現役ページ数: {len(pages)}（docs/ 配下の HTML から {'/'.join(sorted(EXCLUDED_DIRS))} を除外）")
    print(f"表の件数: {tables}")
    by_dir: dict[str, int] = {}
    for page in pages:
        key = posixpath.dirname(page)
        by_dir[key] = by_dir.get(key, 0) + 1
    print("内訳: " + ", ".join(f"{k}={v}" for k, v in sorted(by_dir.items())))
    if args.list:
        for page in pages:
            print(f"  - {page}（表 {count_tables(texts[page])}）")

    print()
    print("=== 2. リンク / アンカー整合 ===")
    findings = check_links(tree)
    exit_code = 0
    if args.baseline:
        try:
            base = check_links(GitTree(REPO_ROOT, args.baseline))
        except RuntimeError as exc:
            base = None
            print(f"baseline を読めなかった: {exc}")
        if base is None:
            print(f"baseline '{args.baseline}' を取り出せなかった（比較なしで全件を列挙）")
            for line in format_findings(findings):
                print(f"  NG {line}")
            exit_code = 1 if findings else exit_code
        else:
            base_set = set(base)
            new = [f for f in findings if f not in base_set]
            fixed = [f for f in base if f not in set(findings)]
            existing = [f for f in findings if f in base_set]
            print(f"今回の差分による不備: {len(new)} 件")
            for line in format_findings(new):
                print(f"  NG {line}")
            print(f"既存不備（baseline {args.baseline} にも存在）: {len(existing)} 件")
            for line in format_findings(existing):
                print(f"  既存 {line}")
            if fixed:
                print(f"baseline から解消: {len(fixed)} 件")
                for line in format_findings(fixed):
                    print(f"  解消 {line}")
            if new:
                exit_code = 1
    else:
        print(f"不備: {len(findings)} 件（既存 / 今回の区別は --baseline REF を付けて実行）")
        for line in format_findings(findings):
            print(f"  NG {line}")
        if findings:
            exit_code = 1

    print()
    print("=== 3. ページ全体の横はみ出し ===")
    if args.no_browser:
        print("スキップ（--no-browser）。未確認のため合格扱いにしない")
        return 1
    browser = find_browser()
    if not browser:
        print("ヘッドレスブラウザーが見つからないため測定できない（未確認）。")
        print("  対処: DOCS_CHECK_CHROME に Chrome / Edge の実行パスを設定するか、")
        print("        静的チェックのみで進め、24-3 の実機確認に委ねる。")
        return 1
    print(f"ブラウザー: {browser}")
    try:
        results = measure_overflow(pages, REPO_ROOT, widths, browser)
    except (RuntimeError, subprocess.TimeoutExpired) as exc:
        print(f"測定に失敗した（未確認）: {exc}")
        return 1

    measured = {(r["page"], r["width"]) for r in results}
    expected = {("/" + rel, w) for rel in pages for w in widths}
    missing = expected - measured
    over = [r for r in results if r["over"] > 1]
    for width in widths:
        count = sum(1 for r in results if r["width"] == width and r["over"] > 1)
        total = sum(1 for r in results if r["width"] == width)
        print(f"  {width:>5} CSS px: はみ出し {count} 件 / {total} ページ")
    for rec in over:
        print(f"  NG {rec['width']}px {rec['page']}: +{rec['over']}px")
        for off in rec["offenders"]:
            print(f"       {off['tag']}.{off['cls']} right={off['right']} :: {off['text']}")
    if missing:
        print(f"  未測定: {len(missing)} 件（未確認のため合格扱いにしない）")
        for page, width in sorted(missing)[:10]:
            print(f"       {width}px {page}")
        exit_code = 1
    if over:
        exit_code = 1

    print()
    print("=== 判定 ===")
    print("OK" if exit_code == 0 else "NG（上記の不備・未確認を参照）")
    return exit_code


if __name__ == "__main__":
    sys.exit(main())
