#!/usr/bin/env python3
"""設計書 HTML（docs/）の機械検証ツール。

Phase 24-1 で新設。アーカイブ（``docs/_archive/``）を除く現役 HTML について、
次の 4 つを確認する。

1. 対象ページと表の件数（実行時に再集計する。固定の期待件数は持たない）
2. リンク / アンカーの整合（相対 href・src の参照先ファイルと ``#id`` の実在）
3. 指定幅でのページ全体の横はみ出し（ヘッドレス Chrome で実測）
4. ``table[data-cards]`` の表構造と、767 / 768 CSS px でのカード表示

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
        self.script_srcs: list[str] = []
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
                if tag == "script" and name == "src":
                    self.script_srcs.append(value)

    def handle_startendtag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        self.handle_starttag(tag, attrs)


def parse_page(text: str) -> PageParser:
    """HTML を解析して参照・id・表の数を返す。"""
    parser = PageParser()
    parser.feed(text)
    parser.close()
    return parser


def normalize_text(value: str) -> str:
    """ブラウザーの ``textContent`` と比較できるよう空白を正規化する。"""
    return re.sub(r"\s+", " ", value).strip()


@dataclass(frozen=True)
class CardRow:
    """カード表示対象の tbody 行。

    Attributes:
        row_id: 行の ``id`` 属性。なければ ``None``。
        cells: 元の td のテキスト（空白正規化済み）。
        colspans: 各 td の ``colspan``。指定がなければ 1。
    """

    row_id: str | None
    cells: tuple[str, ...]
    colspans: tuple[int, ...]


@dataclass(frozen=True)
class CardTable:
    """``table[data-cards]`` 1 表の静的解析結果。"""

    page: str
    index: int
    headers: tuple[str, ...]
    extra_indexes: tuple[int, ...]
    invalid_extra_indexes: tuple[str, ...]
    rows: tuple[CardRow, ...]


class CardTableParser(HTMLParser):
    """``table[data-cards]`` の見出し・行・補足列指定を抽出する。"""

    def __init__(self, page: str) -> None:
        super().__init__(convert_charrefs=True)
        self.page = page
        self.tables: list[CardTable] = []
        self._table_depth = 0
        self._current: dict | None = None
        self._section: str | None = None
        self._row: dict | None = None
        self._cell: list[str] | None = None
        self._cell_colspan = 1

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        """開始タグに応じて対象表の構造を記録する。"""
        attr_map = dict(attrs)
        if tag == "table":
            self._table_depth += 1
            if self._table_depth == 1 and "data-cards" in attr_map:
                raw = attr_map.get("data-card-extra") or ""
                indexes: list[int] = []
                invalid: list[str] = []
                for part in raw.split(","):
                    value = part.strip()
                    if not value:
                        continue
                    if value.isdigit():
                        indexes.append(int(value))
                    else:
                        invalid.append(value)
                self._current = {
                    "index": len(self.tables),
                    "headers": [],
                    "extra_indexes": indexes,
                    "invalid_extra_indexes": invalid,
                    "rows": [],
                }
            return
        if self._current is None:
            return
        if tag in {"thead", "tbody"}:
            self._section = tag
        elif tag == "tr" and self._section in {"thead", "tbody"}:
            self._row = {"id": attr_map.get("id"), "cells": []}
        elif tag in {"th", "td"} and self._row is not None:
            if (self._section == "thead" and tag == "th") or (
                self._section == "tbody" and tag == "td"
            ):
                self._cell = []
                raw_colspan = attr_map.get("colspan") or "1"
                self._cell_colspan = int(raw_colspan) if raw_colspan.isdigit() else 1

    def handle_data(self, data: str) -> None:
        """セル内のテキストを蓄積する。"""
        if self._cell is not None:
            self._cell.append(data)

    def handle_endtag(self, tag: str) -> None:
        """終了タグに応じてセル・行・表を確定する。"""
        if self._current is not None and tag in {"th", "td"} and self._cell is not None:
            self._row["cells"].append(normalize_text("".join(self._cell)))
            self._row.setdefault("colspans", []).append(self._cell_colspan)
            self._cell = None
        if self._current is not None and tag == "tr" and self._row is not None:
            cells = self._row["cells"]
            if self._section == "thead" and not self._current["headers"]:
                self._current["headers"] = cells
            elif self._section == "tbody":
                self._current["rows"].append(
                    CardRow(
                        self._row["id"],
                        tuple(cells),
                        tuple(self._row["colspans"]),
                    )
                )
            self._row = None
        if self._current is not None and tag in {"thead", "tbody"}:
            self._section = None
        if tag == "table":
            if self._table_depth == 1 and self._current is not None:
                self.tables.append(
                    CardTable(
                        page=self.page,
                        index=self._current["index"],
                        headers=tuple(self._current["headers"]),
                        extra_indexes=tuple(self._current["extra_indexes"]),
                        invalid_extra_indexes=tuple(self._current["invalid_extra_indexes"]),
                        rows=tuple(self._current["rows"]),
                    )
                )
                self._current = None
            self._table_depth -= 1


def parse_card_tables(page: str, text: str) -> list[CardTable]:
    """ページ内の ``table[data-cards]`` を静的に解析して返す。"""
    parser = CardTableParser(page)
    parser.feed(text)
    parser.close()
    return parser.tables


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


DRIVER_HEAD = """<!DOCTYPE html><html><head><meta charset="utf-8"><title>docs_check</title></head>
<body><pre id="out">PENDING</pre><div id="host"></div><script>
function load(src, w) {
  return new Promise(res => {
    const f = document.createElement('iframe');
    f.style.cssText = 'width:' + w + 'px;height:2400px;border:0;';
    f.src = src;
    f.onload = () => setTimeout(() => res(f), 30);
    document.getElementById('host').appendChild(f);
  });
}
"""

OVERFLOW_DRIVER_TEMPLATE = DRIVER_HEAD + """
const PAGES = %s, WIDTHS = %s;
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

CARD_DRIVER_TEMPLATE = DRIVER_HEAD + """
const PAGES = %s, WIDTHS = %s;
function textOf(el) {
  return (el.textContent || '').replace(/\\s+/g, ' ').trim();
}
function cellsOf(tr) {
  return Array.from(tr.children)
    .filter(el => (el.tagName === 'TD' || el.tagName === 'TH') &&
                  !el.classList.contains('card-toggle-cell'))
    .map((el, i) => ({
      column: i + 1,
      text: textOf(el),
      extra: el.classList.contains('card-extra'),
      hidden: el.hasAttribute('hidden') ? el.getAttribute('hidden') : null,
      visible: el.getClientRects().length > 0
    }));
}
async function main() {
  const out = [];
  for (const w of WIDTHS) {
    for (const p of PAGES) {
      const f = await load(p, w);
      const d = f.contentDocument;
      const tables = Array.from(d.querySelectorAll('table[data-cards]'));
      out.push({
        page: p,
        width: w,
        tables: tables.map((table, index) => ({
          index: index,
          display: getComputedStyle(table).display,
          rows: Array.from(table.querySelectorAll('tbody > tr')).map((tr, row) => {
            const toggle = Array.from(tr.children).find(
              el => el.classList && el.classList.contains('card-toggle-cell'));
            return {
              row: row + 1,
              rowId: tr.id || null,
              cells: cellsOf(tr),
              toggle: toggle ? {exists: true, display: getComputedStyle(toggle).display} :
                {exists: false, display: null}
            };
          })
        }))
      });
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


def run_browser_driver(root: Path, browser: str, driver_html: bytes, budget: int) -> list[dict]:
    """ローカル HTTP サーバー上でドライバーをヘッドレス Chrome に実行させる。

    Args:
        root: HTTP サーバーの公開ルート（リポジトリルート）。
        browser: ヘッドレス Chrome / Edge の実行パス。
        driver_html: ``/__docs_check__.html`` として配信するドライバー HTML。
        budget: ブラウザーに与える仮想時間の上限（ミリ秒）。

    Returns:
        ドライバーが JSON として返した測定結果の一覧。

    Raises:
        RuntimeError: ブラウザーから測定結果を取得できなかった場合。
    """
    server = socketserver.ThreadingTCPServer(("0.0.0.0", 0), _make_handler(root, driver_html))
    port = server.server_address[1]
    threading.Thread(target=server.serve_forever, daemon=True).start()
    time.sleep(1.5)  # WSL からの localhost 転送が張られるのを待つ
    try:
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


def measure_overflow(
    pages: Sequence[str], root: Path, widths: Sequence[int], browser: str
) -> list[dict]:
    """指定幅でページ全体の横はみ出しを実測する。

    同一オリジンの iframe に各ページを読み込んで ``scrollWidth`` と
    ``clientWidth`` を比較する（iframe 幅 = CSS px のビューポート幅）。
    """
    urls = ["/" + rel for rel in pages]
    driver = (
        OVERFLOW_DRIVER_TEMPLATE % (json.dumps(urls), json.dumps(list(widths)))
    ).encode("utf-8")
    budget = 20000 + 500 * len(urls) * len(widths)
    return run_browser_driver(root, browser, driver, budget)


def measure_cards(
    pages: Sequence[str], root: Path, widths: Sequence[int], browser: str
) -> list[dict]:
    """指定幅で ``table[data-cards]`` のセル・トグルの実測値を取得する。"""
    urls = ["/" + rel for rel in pages]
    driver = (CARD_DRIVER_TEMPLATE % (json.dumps(urls), json.dumps(list(widths)))).encode(
        "utf-8"
    )
    budget = 20000 + 500 * len(urls) * len(widths)
    return run_browser_driver(root, browser, driver, budget)


CARD_WIDTHS = (767, 768)


def measure_cards_with_retry(
    pages: Sequence[str], root: Path, browser: str, attempts: int = 2
) -> list[dict]:
    """カード表示の実測を、取得できなかった場合に限り retry しながら行う。

    Args:
        pages: 対象の現役 HTML（リポジトリ相対パス）。
        root: HTTP サーバーの公開ルート（リポジトリルート）。
        browser: ヘッドレス Chrome / Edge の実行パス。
        attempts: 最大試行回数。

    Returns:
        ドライバーが返した測定結果の一覧。

    Raises:
        RuntimeError: すべての試行で測定結果を取得できなかった場合。
    """
    last: Exception | None = None
    for attempt in range(attempts):
        try:
            return measure_cards(pages, root, CARD_WIDTHS, browser)
        except (RuntimeError, subprocess.TimeoutExpired) as exc:
            last = exc
            if attempt + 1 < attempts:
                time.sleep(2.0)
    raise RuntimeError(str(last))


def format_findings(findings: Iterable[Finding]) -> list[str]:
    """指摘を表示用の行に整形する。"""
    return [f.line() for f in sorted(findings, key=lambda f: (f.page, f.kind, f.detail))]


def check_card_static(
    card_tables: Sequence[CardTable], texts: dict[str, str]
) -> list[Finding]:
    """カード表示対象表の HTML 構造とスクリプト読込を確認する。"""
    findings: list[Finding] = []
    pages = {table.page for table in card_tables}
    for page in sorted(pages):
        scripts = parse_page(texts[page]).script_srcs
        if not any(urlsplit(src).path.endswith("docs-cards.js") for src in scripts):
            findings.append(Finding(page, "cards-script", "docs-cards.js の script src がない"))

    for table in card_tables:
        label = f"table {table.index + 1}"
        columns = len(table.headers)
        for row_number, row in enumerate(table.rows, start=1):
            row_columns = sum(row.colspans)
            if row_columns != columns:
                findings.append(
                    Finding(
                        table.page,
                        "cards-column-count",
                        f"{label} 行 {row_number}: thead {columns} 列 / tbody {row_columns} 列",
                    )
                )
        for value in table.invalid_extra_indexes:
            findings.append(
                Finding(
                    table.page,
                    "cards-extra-index",
                    f"{label}: data-card-extra の列番号でない値 '{value}'",
                )
            )
        for value in table.extra_indexes:
            if not 1 <= value <= columns:
                findings.append(
                    Finding(
                        table.page,
                        "cards-extra-index",
                        f"{label}: data-card-extra={value}（列数 {columns} の範囲外）",
                    )
                )

        has_issue_ids = any(
            row.row_id is not None and re.fullmatch(r"I-\d+", row.row_id)
            for row in table.rows
        )
        if has_issue_ids:
            for row_number, row in enumerate(table.rows, start=1):
                if row.row_id is None:
                    findings.append(
                        Finding(
                            table.page,
                            "cards-row-id",
                            f"{label} 行 {row_number}: issues 形式の表に id がない",
                        )
                    )
    return findings


def card_table_summary(table: CardTable) -> str:
    """表ごとの静的チェック結果を 1 行に整形する。"""
    extras = set(table.extra_indexes)
    main_labels = [name for i, name in enumerate(table.headers, start=1) if i not in extras]
    extra_labels = [name for i, name in enumerate(table.headers, start=1) if i in extras]
    issue_ids = sum(
        row.row_id is not None and re.fullmatch(r"I-\d+", row.row_id) is not None
        for row in table.rows
    )
    with_id = sum(row.row_id is not None for row in table.rows)
    without_id = len(table.rows) - with_id
    anchor = (
        f"ID アンカーあり {issue_ids} 行 / id あり {with_id} 行 / id なし {without_id} 行"
        if issue_ids
        else f"id なし（元の表にも無し） {without_id} 行 / id あり {with_id} 行"
    )
    return (
        f"  {table.page} table {table.index + 1}: {len(table.rows)} 行 / "
        f"常時表示: {'・'.join(main_labels) or 'なし'} / "
        f"補足: {'・'.join(extra_labels) or 'なし'} / {anchor}"
    )


def preview_text(value: str) -> str:
    """NG 出力用にテキストの先頭 40 字を返す。"""
    return value[:40] + ("…" if len(value) > 40 else "")


def card_row_name(table: CardTable, row_number: int) -> str:
    """NG 出力で使う行 ID または 1 始まり行番号を返す。"""
    row = table.rows[row_number - 1]
    return row.row_id or f"行 {row_number}"


def check_card_measurements(
    card_tables: Sequence[CardTable], results: Sequence[dict]
) -> tuple[dict[str, tuple[int, int]], list[str]]:
    """カード表示のブラウザー実測を静的な元表と突き合わせる。

    Returns:
        判定項目ごとの ``(確認数, NG 数)`` と、NG の詳細表示行。
    """
    counts: dict[str, list[int]] = {
        "767px 表示:block": [0, 0],
        "767px 常時表示セル": [0, 0],
        "767px 補足セル": [0, 0],
        "767px トグル": [0, 0],
        "768px 表示・全セル・トグル": [0, 0],
    }
    findings: list[str] = []
    by_result = {(rec["page"].lstrip("/"), rec["width"]): rec for rec in results}

    def add(key: str, detail: str) -> None:
        counts[key][1] += 1
        findings.append(detail)

    for table in card_tables:
        extras = set(table.extra_indexes)
        for width in (767, 768):
            record = by_result.get((table.page, width))
            prefix = f"{width}px {table.page} table {table.index + 1}"
            if record is None or table.index >= len(record["tables"]):
                keys = (
                    ["767px 表示:block", "767px 常時表示セル", "767px 補足セル", "767px トグル"]
                    if width == 767
                    else ["768px 表示・全セル・トグル"]
                )
                for key in keys:
                    counts[key][0] += 1
                    add(key, f"{prefix}: 測定結果がない")
                continue
            measured = record["tables"][table.index]
            if width == 767:
                counts["767px 表示:block"][0] += 1
                if measured["display"] != "block":
                    add(
                        "767px 表示:block",
                        f"{prefix}: table display={measured['display']}（block ではない）",
                    )
            else:
                counts["768px 表示・全セル・トグル"][0] += 1
                if measured["display"] != "table":
                    add(
                        "768px 表示・全セル・トグル",
                        f"{prefix}: table display={measured['display']}（table ではない）",
                    )

            if len(measured["rows"]) != len(table.rows):
                key = "767px 常時表示セル" if width == 767 else "768px 表示・全セル・トグル"
                counts[key][0] += 1
                add(
                    key,
                    f"{prefix}: 元の表 {len(table.rows)} 行 / 実測 {len(measured['rows'])} 行",
                )

            for row_number, original in enumerate(table.rows, start=1):
                if row_number > len(measured["rows"]):
                    continue
                actual = measured["rows"][row_number - 1]
                row_name = card_row_name(table, row_number)
                if len(actual["cells"]) != len(original.cells):
                    key = "767px 常時表示セル" if width == 767 else "768px 表示・全セル・トグル"
                    counts[key][0] += 1
                    add(
                        key,
                        f"{prefix} {row_name}: 元の表 {len(original.cells)} セル / "
                        f"実測 {len(actual['cells'])} セル",
                    )
                for column, original_text in enumerate(original.cells, start=1):
                    if column > len(actual["cells"]):
                        continue
                    cell = actual["cells"][column - 1]
                    expected_extra = column in extras
                    if width == 767 and not expected_extra:
                        counts["767px 常時表示セル"][0] += 1
                        if cell["extra"] or not cell["visible"] or cell["text"] != original_text:
                            add(
                                "767px 常時表示セル",
                                f"{prefix} {row_name} 列 {column}: 元='{preview_text(original_text)}' / "
                                f"実='{preview_text(cell['text'])}' "
                                f"（card-extra={cell['extra']}, 表示={cell['visible']}）",
                            )
                    elif width == 767:
                        counts["767px 補足セル"][0] += 1
                        hidden = cell["hidden"]
                        if (
                            not cell["extra"]
                            or hidden not in {"", "until-found"}
                            or cell["text"] != original_text
                        ):
                            add(
                                "767px 補足セル",
                                f"{prefix} {row_name} 列 {column}: 元='{preview_text(original_text)}' / "
                                f"実='{preview_text(cell['text'])}' "
                                f"（card-extra={cell['extra']}, hidden={hidden!r}）",
                            )
                    elif width == 768:
                        counts["768px 表示・全セル・トグル"][0] += 1
                        if not cell["visible"]:
                            add(
                                "768px 表示・全セル・トグル",
                                f"{prefix} {row_name} 列 {column}: セルが表示されていない",
                            )

                row_has_extra = any(
                    column in extras for column in range(1, len(original.cells) + 1)
                )
                if width == 767 and row_has_extra:
                    counts["767px トグル"][0] += 1
                    if not actual["toggle"]["exists"] or actual["toggle"]["display"] == "none":
                        add(
                            "767px トグル",
                            f"{prefix} {row_name}: トグルセルがないか display=none",
                        )
                elif width == 768:
                    counts["768px 表示・全セル・トグル"][0] += 1
                    if actual["toggle"]["exists"] and actual["toggle"]["display"] != "none":
                        add(
                            "768px 表示・全セル・トグル",
                            f"{prefix} {row_name}: トグルセル display={actual['toggle']['display']}",
                        )

    return {key: (value[0], value[1]) for key, value in counts.items()}, findings


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
    card_tables = [table for page in pages for table in parse_card_tables(page, texts[page])]

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
    browser_ready = False
    browser: str | None = None
    if args.no_browser:
        print("スキップ（--no-browser）。未確認のため合格扱いにしない")
        exit_code = 1
    else:
        browser = find_browser()
    if not args.no_browser and not browser:
        print("ヘッドレスブラウザーが見つからないため測定できない（未確認）。")
        print("  対処: DOCS_CHECK_CHROME に Chrome / Edge の実行パスを設定するか、")
        print("        静的チェックのみで進め、24-3 の実機確認に委ねる。")
        exit_code = 1
    elif not args.no_browser:
        print(f"ブラウザー: {browser}")
        try:
            results = measure_overflow(pages, REPO_ROOT, widths, browser)
        except (OSError, RuntimeError, subprocess.TimeoutExpired) as exc:
            print(f"測定に失敗した（未確認）: {exc}")
            exit_code = 1
        else:
            browser_ready = True
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
    print("=== 4. カード表示（24-2） ===")
    card_static = check_card_static(card_tables, texts)
    card_pages = {table.page for table in card_tables}
    print(f"対象: {len(card_pages)} ページ / {len(card_tables)} 表")
    for table in card_tables:
        print(card_table_summary(table))
    print(f"静的チェック: {'OK' if not card_static else 'NG'}（不備 {len(card_static)} 件）")
    for line in format_findings(card_static):
        print(f"  NG {line}")
    if card_static:
        exit_code = 1

    if not browser_ready:
        print("ブラウザー実測: 未確認（セクション 3 と同じ理由。合格扱いにしない）")
        exit_code = 1
    else:
        try:
            # セクション 3 の直後はブラウザーの起動が間に合わず空振りすることがあるため 1 度だけ retry する
            card_results = measure_cards_with_retry(sorted(card_pages), REPO_ROOT, browser)
        except (OSError, RuntimeError, subprocess.TimeoutExpired) as exc:
            print(f"ブラウザー実測: 未確認（測定に失敗: {exc}）")
            exit_code = 1
        else:
            card_counts, card_findings = check_card_measurements(card_tables, card_results)
            for name, (checked, failed) in card_counts.items():
                print(f"  {name}: NG {failed} 件 / {checked} 件")
            for finding in card_findings:
                print(f"  NG {finding}")
            if card_findings:
                exit_code = 1
            print("カード表示の判定: " + ("OK" if not card_findings and not card_static else "NG"))

    print()
    print("=== 判定 ===")
    print("OK" if exit_code == 0 else "NG（上記の不備・未確認を参照）")
    return exit_code


if __name__ == "__main__":
    sys.exit(main())
