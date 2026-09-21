"""計画書 HTML の構造を検査するモジュール。"""

from __future__ import annotations

import re
import sys
from dataclasses import dataclass, field
from html.parser import HTMLParser
from pathlib import Path
from typing import Iterable, Sequence


REPO_ROOT = Path(__file__).resolve().parent.parent

# 本番の検査対象ページ（リポジトリルートからの相対パス）。
# 25-1 時点では空。Phase 25-2 で "docs/plans/development-plan.html" を登録する。
REGISTERED_PAGES: tuple[str, ...] = ()

_VOID_TAGS = {
    "area", "base", "br", "col", "embed", "hr", "img", "input", "link",
    "meta", "param", "source", "track", "wbr",
}
_STATUSES = {"todo", "doing", "done", "blocked"}
_NORMAL_FIELDS = (
    "overview", "prerequisites", "constraints", "acceptance", "gate", "stop",
    "result",
)
_LEGACY_FIELDS = ("overview", "prerequisites", "result")
_COMPLETED_DATE = re.compile(r"\d{4}-\d{2}-\d{2}\Z")
_LEGACY_MARKERS = ("⬜", "✅", "⚠️")


@dataclass(frozen=True)
class PlanFinding:
    """計画書の構造上の不備を表す値。

    Attributes:
        page: ページのパス。
        step_id: 該当ステップの ID。ページ全体の指摘は ``-``。
        rule: 規則 ID。
        message: 利用者向けの日本語説明。
    """

    page: str
    step_id: str
    rule: str
    message: str


@dataclass
class _Node:
    """HTML 要素の最小限の木構造を保持する内部ノード。"""

    tag: str
    attrs: dict[str, str | None]
    position: int
    parent: _Node | None = None
    children: list[_Node] = field(default_factory=list)
    texts: list[str] = field(default_factory=list)


class _TreeParser(HTMLParser):
    """HTMLParser のイベントから入れ子を保持した木を作る。"""

    def __init__(self) -> None:
        """パーサーを初期化する。"""
        super().__init__(convert_charrefs=True)
        self.root = _Node("#document", {}, 0)
        self._stack = [self.root]
        self._position = 0

    def handle_starttag(
        self, tag: str, attrs: list[tuple[str, str | None]]
    ) -> None:
        """開始タグを木へ追加する。"""
        self._add_node(tag, attrs, push=tag not in _VOID_TAGS)

    def handle_startendtag(
        self, tag: str, attrs: list[tuple[str, str | None]]
    ) -> None:
        """自己終了タグを木へ追加する。"""
        self._add_node(tag, attrs, push=False)

    def handle_endtag(self, tag: str) -> None:
        """終了タグに対応するスタック要素を閉じる。"""
        for index in range(len(self._stack) - 1, 0, -1):
            if self._stack[index].tag == tag:
                del self._stack[index:]
                return

    def handle_data(self, data: str) -> None:
        """現在の要素の直接テキストを記録する。"""
        self._stack[-1].texts.append(data)

    def _add_node(
        self, tag: str, attrs: list[tuple[str, str | None]], push: bool
    ) -> None:
        """ノードを追加し、必要ならスタックへ積む。"""
        self._position += 1
        node = _Node(tag, dict(attrs), self._position, self._stack[-1])
        self._stack[-1].children.append(node)
        if push:
            self._stack.append(node)


def _walk(node: _Node) -> Iterable[_Node]:
    """ノード自身を含む深さ優先順で走査する。"""
    yield node
    for child in node.children:
        yield from _walk(child)


def _has_class(node: _Node, class_name: str) -> bool:
    """class 属性が指定したトークンを含むか返す。"""
    return class_name in (node.attrs.get("class") or "").split()


def _is_step(node: _Node) -> bool:
    """ノードが検査対象のステップか返す。"""
    return node.tag == "article" and _has_class(node, "plan-step")


def _ancestors(node: _Node) -> Iterable[_Node]:
    """親から文書ルートまでの祖先を返す。"""
    current = node.parent
    while current is not None:
        yield current
        current = current.parent


def _ancestor(node: _Node, predicate: object) -> _Node | None:
    """条件に合う最も近い祖先を返す。"""
    for parent in _ancestors(node):
        if predicate(parent):  # type: ignore[operator]
            return parent
    return None


def _text(node: _Node, exclude_folds: bool = False) -> str:
    """子孫を含むテキストを返す。

    Args:
        node: テキストを集める起点要素。
        exclude_folds: 実装詳細・記録の折りたたみを除外するか。
    """
    pieces: list[str] = []

    def collect(current: _Node, is_root: bool = False) -> None:
        if not is_root and exclude_folds and current.attrs.get("data-field") in {
            "implementation", "record",
        }:
            return
        pieces.extend(current.texts)
        for child in current.children:
            collect(child)

    collect(node, is_root=True)
    return "".join(pieces)


def _is_descendant(node: _Node, ancestor: _Node) -> bool:
    """node が ancestor の子孫か返す。"""
    return any(parent is ancestor for parent in _ancestors(node))


def check_text(page: str, text: str) -> list[PlanFinding]:
    """HTML 文字列に含まれる計画書構造の不備を返す。

    Args:
        page: 結果に表示するページのパス。
        text: 検査対象の HTML。

    Returns:
        文書内の出現順に並べた不備一覧。
    """
    parser = _TreeParser()
    parser.feed(text)
    parser.close()
    nodes = list(_walk(parser.root))
    findings: list[tuple[int, int, PlanFinding]] = []
    serial = 0

    def add(position: int, step_id: str, rule: str, message: str) -> None:
        nonlocal serial
        findings.append((position, serial, PlanFinding(page, step_id, rule, message)))
        serial += 1

    body = next((node for node in nodes if node.tag == "body"), None)
    if body is None or body.attrs.get("data-plan-format") != "1":
        add(0, "-", "page-format", "body に data-plan-format=\"1\" がありません")

    steps = [node for node in nodes if _is_step(node)]
    if not steps:
        add(0, "-", "page-empty", "article.plan-step がありません")

    for node in nodes:
        if node.tag != "li":
            continue
        direct_text = "".join(node.texts).lstrip()
        in_step = _ancestor(node, _is_step) is not None
        if not in_step and direct_text.startswith(_LEGACY_MARKERS):
            add(node.position, "-", "page-legacy-mixed", "旧形式の状態付き li が残っています")

    phases = [
        node for node in nodes
        if node.tag == "section" and _has_class(node, "plan-phase")
        and "data-plan-phase" in node.attrs
    ]
    for phase in phases:
        groups = [
            node for node in _walk(phase)
            if node is not phase
            and node.attrs.get("data-plan-group") in {"done", "active"}
        ]
        done_positions = [
            group.position for group in groups
            if group.attrs.get("data-plan-group") == "done"
        ]
        active_positions = [
            group.position for group in groups
            if group.attrs.get("data-plan-group") == "active"
        ]
        if (
            done_positions
            and active_positions
            and max(done_positions) > min(active_positions)
        ):
            add(
                phase.position,
                "-",
                "group-order",
                "完了済みグループが進行中グループより後ろにあります",
            )
        for group in groups:
            if group.attrs.get("data-plan-group") != "done":
                continue
            if group.tag != "details":
                add(
                    group.position,
                    "-",
                    "group-tag",
                    "完了済みグループは details 要素にしてください",
                )
            elif "open" in group.attrs:
                add(
                    group.position,
                    "-",
                    "group-open",
                    "完了済みグループに open を付けないでください",
                )

    seen_step_ids: set[str] = set()
    seen_ids: set[str] = set()
    for step in steps:
        step_id = step.attrs.get("data-step-id") or "-"
        html_id = step.attrs.get("id")
        phase = _ancestor(
            step,
            lambda node: node.tag == "section" and _has_class(node, "plan-phase")
            and "data-plan-phase" in node.attrs,
        )
        if phase is None:
            add(step.position, step_id, "phase-missing", "ステップが plan-phase の外にあります")

        group = _ancestor(
            step, lambda node: node.attrs.get("data-plan-group") in {"done", "active"}
        )
        if group is None:
            add(
                step.position,
                step_id,
                "group-missing",
                "ステップが完了済み・進行中グループのどちらにもありません",
            )

        if (
            not step.attrs.get("data-step-id")
            or html_id != f"step-{step.attrs.get('data-step-id')}"
        ):
            add(
                step.position,
                step_id,
                "step-attrs",
                "data-step-id と id=step-<data-step-id> が一致していません",
            )
        if step.attrs.get("data-step-id"):
            value = step.attrs["data-step-id"]
            if value in seen_step_ids:
                add(
                    step.position,
                    step_id,
                    "step-duplicate",
                    "data-step-id が同一ページ内で重複しています",
                )
            seen_step_ids.add(value)
        if html_id:
            if html_id in seen_ids:
                add(step.position, step_id, "step-duplicate", "id が同一ページ内で重複しています")
            seen_ids.add(html_id)

        status = step.attrs.get("data-status")
        if status not in _STATUSES:
            add(step.position, step_id, "step-status", "data-status が許可された状態ではありません")
        if status == "done" and not _COMPLETED_DATE.fullmatch(
            step.attrs.get("data-completed") or ""
        ):
            add(
                step.position,
                step_id,
                "step-completed",
                "done のステップには YYYY-MM-DD の完了日が必要です",
            )
        group_name = group.attrs.get("data-plan-group") if group else None
        if (status == "done" and group_name != "done") or (
            status in {"todo", "doing", "blocked"} and group_name == "done"
        ):
            add(
                step.position,
                step_id,
                "step-group",
                "ステータスと所属グループが一致していません",
            )

        kind = step.attrs.get("data-kind")
        if kind not in {None, "decision", "legacy-completed"}:
            add(step.position, step_id, "kind-unknown", "data-kind の値が未定義です")
        if kind == "decision":
            if "ゴール対象外" not in _text(step, exclude_folds=True):
                add(
                    step.position,
                    step_id,
                    "kind-decision-label",
                    "折りたたみの外に「ゴール対象外」の表示がありません",
                )
        if kind == "legacy-completed" and status != "done":
            add(
                step.position,
                step_id,
                "kind-legacy-status",
                "legacy-completed は done のステップだけに使えます",
            )

        fields: dict[str, list[_Node]] = {}
        for node in _walk(step):
            if node is not step and "data-field" in node.attrs:
                fields.setdefault(node.attrs["data-field"] or "", []).append(node)
        for field_name, field_nodes in fields.items():
            for repeated in field_nodes[1:]:
                add(
                    repeated.position,
                    step_id,
                    "field-duplicate",
                    f"data-field=\"{field_name}\" が重複しています",
                )

        required = _LEGACY_FIELDS if kind == "legacy-completed" else _NORMAL_FIELDS
        for field_name in required:
            field_nodes = fields.get(field_name, [])
            if not field_nodes:
                add(step.position, step_id, "field-missing", f"必須欄 {field_name} がありません")
                continue
            for field_node in field_nodes:
                if not _text(field_node).strip():
                    add(
                        field_node.position,
                        step_id,
                        "field-empty",
                        f"欄 {field_name} が空です",
                    )
                fold = _ancestor(
                    field_node,
                    lambda node: node is not step and node.attrs.get("data-field")
                    in {"implementation", "record"},
                )
                if fold is not None:
                    add(
                        field_node.position,
                        step_id,
                        "field-in-fold",
                        f"必須欄 {field_name} が折りたたみ内にあります",
                    )
            if field_name == "acceptance":
                for field_node in field_nodes:
                    if field_node.tag not in {"ul", "ol"}:
                        add(
                            field_node.position,
                            step_id,
                            "acceptance-tag",
                            "acceptance は ul または ol にしてください",
                        )

        if kind == "decision":
            stop_fields = fields.get("stop", [])
            if not any("ゴールにしない" in _text(node) for node in stop_fields):
                add(
                    step.position,
                    step_id,
                    "kind-decision-stop",
                    "stop 欄に「ゴールにしない」がありません",
                )

        implementations = fields.get("implementation", [])
        records = fields.get("record", [])
        for implementation in implementations:
            if implementation.tag != "details":
                add(
                    implementation.position,
                    step_id,
                    "fold-tag",
                    "implementation は details 要素にしてください",
                )
            elif "open" in implementation.attrs:
                add(
                    implementation.position,
                    step_id,
                    "fold-open",
                    "折りたたみに open を付けないでください",
                )
        if not records:
            add(step.position, step_id, "record-missing", "作業記録欄がありません")
        for record in records:
            if record.tag not in {"details", "section"}:
                add(
                    record.position,
                    step_id,
                    "fold-tag",
                    "record は details または section 要素にしてください",
                )
            if record.tag == "details" and "open" in record.attrs:
                add(
                    record.position,
                    step_id,
                    "fold-open",
                    "折りたたみに open を付けないでください",
                )
            if not _text(record).strip():
                add(record.position, step_id, "record-empty", "作業記録欄が空です")
            links = [
                node for node in _walk(record)
                if node.tag == "a" and "href" in node.attrs
            ]
            if record.tag == "section" and not links:
                add(
                    record.position,
                    step_id,
                    "record-link",
                    "section 形式の作業記録にはリンクが必要です",
                )
            if kind == "legacy-completed" and not links:
                add(
                    record.position,
                    step_id,
                    "kind-legacy-record",
                    "legacy-completed の記録にはリンクが必要です",
                )
        is_nested = any(
            _is_descendant(implementation, record)
            or _is_descendant(record, implementation)
            for implementation in implementations
            for record in records
        )
        if is_nested:
            add(step.position, step_id, "fold-separate", "実装詳細と作業記録を入れ子にしないでください")

    return [finding for _, _, finding in sorted(findings, key=lambda item: item[:2])]


def check_file(path: str | Path, page: str | None = None) -> list[PlanFinding]:
    """ファイルを読み込み、存在しない場合も含めて検査する。

    Args:
        path: 読み込む HTML ファイル。
        page: 結果に表示するページ名。省略時は path の文字列表現。

    Returns:
        構造上の不備一覧。ファイルが無い場合は page-missing を 1 件返す。
    """
    file_path = Path(path)
    page_name = page if page is not None else str(file_path)
    if not file_path.is_file():
        return [PlanFinding(page_name, "-", "page-missing", "検査対象のファイルが存在しません")]
    return check_text(page_name, file_path.read_text(encoding="utf-8"))


def check_registered(root: Path = REPO_ROOT) -> list[PlanFinding]:
    """登録済みページを root から検査する。

    Args:
        root: 登録パスを解決するリポジトリルート。

    Returns:
        登録済み全ページの不備一覧。
    """
    findings: list[PlanFinding] = []
    for page in REGISTERED_PAGES:
        findings.extend(check_file(root / page, page))
    return findings


def format_findings(findings: Iterable[PlanFinding]) -> list[str]:
    """不備一覧を CLI 用の一行表記へ変換する。

    Args:
        findings: 整形する不備一覧。

    Returns:
        ``<page> / <step_id> / <rule>: <message>`` 形式の行一覧。
    """
    return [
        f"{item.page} / {item.step_id} / {item.rule}: {item.message}"
        for item in findings
    ]


def main(argv: Sequence[str] | None = None) -> int:
    """コマンドラインから検査を実行して終了コードを返す。

    Args:
        argv: ファイルパスの列。省略時は実行時のコマンドライン引数。

    Returns:
        不備がなければ 0、不備があれば 1。
    """
    arguments = list(sys.argv[1:] if argv is None else argv)
    if arguments:
        targets = list(arguments)
        findings = [
            finding for path in arguments for finding in check_file(path, path)
        ]
    else:
        targets = list(REGISTERED_PAGES)
        findings = check_registered()
    if findings:
        print("\n".join(format_findings(findings)))
        return 1
    if not targets:
        # 登録が空のときに「実ページを検査した」と誤読されないようにする
        # （Phase 25-2 で development-plan.html を登録するまでの状態）。
        print("検査対象のページが登録されていません（REGISTERED_PAGES が空）")
        return 0
    print(f"OK（不備 0 件 / 対象 {len(targets)} ページ）")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
