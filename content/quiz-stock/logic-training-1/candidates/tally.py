#!/usr/bin/env python3
"""候補ディレクトリの集計ツール(logic-training-1・改修 R-3-1)。

「1 候補 1 ファイル」(フロントマター付き Markdown)を読み、朝夜別に
候補数・未レビュー・OK・NG・保留・完成稿 NG・余剰 OK・不足・追加数(不足 × 2)を出し、
仕上げ(G1b)へ進めるかを判定する。依存は標準ライブラリのみ。

使い方(リポジトリルートから):
    python3 content/quiz-stock/logic-training-1/candidates/tally.py plan --target 7 7
    python3 content/quiz-stock/logic-training-1/candidates/tally.py <batch_dir> [--target 7 7]
        [--carry-from <old_dir> ...] [--write-index]

集計の規則(正は同ディレクトリの README.md):
- 1 ファイル = 1 候補。版(修正版)は同じファイルに追記するので、版の数だけ重複加算されない
- 別ファイルへ切り出した修正版は ``supersedes: <元 id>`` を持ち、元の候補は集計から外す
- OK として数えるのは state が ok / drafting / approved(候補 OK・完成稿へ進行中・完成稿承認)
- 不足 = max(0, 目標 - OK)。追加 = 不足 × 2。余剰 OK = max(0, OK - 目標)
- 朝夜の両方で不足 0 のときだけ G1b(完成稿)へ進める。未レビューが残る間は追加数を確定しない
- 完成稿 NG(final_ng)は OK に数えない(再選別待ち。修正版を版として追記し unreviewed に戻す)
"""
from __future__ import annotations

import argparse
import sys
from dataclasses import dataclass, field
from pathlib import Path

SLOTS = ("morning", "night")
SLOT_LABEL = {"morning": "朝", "night": "夜"}
STATES = ("unreviewed", "ok", "ng", "hold", "drafting", "approved", "final_ng", "withdrawn")
STATE_LABEL = {
    "unreviewed": "未レビュー",
    "ok": "OK(候補)",
    "ng": "NG",
    "hold": "保留",
    "drafting": "完成稿へ進行中",
    "approved": "完成稿承認",
    "final_ng": "完成稿NG(再選別待ち)",
    "withdrawn": "取り下げ",
}
OK_LIKE = ("ok", "drafting", "approved")
REQUIRED = ("id", "batch", "slot", "state", "version")


@dataclass
class Candidate:
    path: Path
    meta: dict[str, str]
    errors: list[str] = field(default_factory=list)

    @property
    def id(self) -> str:
        return self.meta.get("id", self.path.stem)


def parse_front_matter(path: Path) -> dict[str, str]:
    """先頭の ``---`` 〜 ``---`` を key: value として読む(YAML ライブラリ不要)。"""
    lines = path.read_text(encoding="utf-8").splitlines()
    if not lines or lines[0].strip() != "---":
        raise ValueError("フロントマター(先頭の ---)がない")
    meta: dict[str, str] = {}
    for line in lines[1:]:
        if line.strip() == "---":
            return meta
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        key, sep, value = line.partition(":")
        if not sep:
            raise ValueError(f"key: value でない行: {line!r}")
        meta[key.strip()] = value.split("#", 1)[0].strip() if not value.strip().startswith("http") else value.strip()
    raise ValueError("フロントマターの終わり(---)がない")


def last_judgement(path: Path) -> str | None:
    """本文の最後の「- 判定:」行の値(空欄なら "")。無ければ None。"""
    value = None
    for line in path.read_text(encoding="utf-8").splitlines():
        s = line.strip()
        if s.startswith("- 判定:"):
            value = s[len("- 判定:"):].strip()
    return value


JUDGEMENT_TO_STATE = {"": "unreviewed", "OK": "ok", "NG": "ng", "保留": "hold"}


def load_dir(directory: Path) -> list[Candidate]:
    items: list[Candidate] = []
    for path in sorted(directory.glob("*.md")):
        if path.name.upper() in ("README.MD", "INDEX.MD") or path.name.startswith("_"):
            continue
        try:
            meta = parse_front_matter(path)
        except ValueError as exc:
            items.append(Candidate(path, {}, [f"{path.name}: {exc}"]))
            continue
        cand = Candidate(path, meta)
        for key in REQUIRED:
            if not meta.get(key):
                cand.errors.append(f"{path.name}: 必須項目 {key} が空")
        if meta.get("slot") not in SLOTS:
            cand.errors.append(f"{path.name}: slot は morning / night のどちらか(現在 {meta.get('slot')!r})")
        if meta.get("state") not in STATES:
            cand.errors.append(f"{path.name}: state が不正 {meta.get('state')!r}")
        if meta.get("state") not in ("withdrawn",) and not meta.get("source"):
            cand.errors.append(f"{path.name}: source(流布例 URL)が空")
        judged = last_judgement(path)
        state = meta.get("state")
        if judged is not None and state in ("unreviewed", "ok", "ng", "hold"):
            expected = JUDGEMENT_TO_STATE.get(judged)
            if expected and expected != state:
                cand.errors.append(
                    f"{path.name}: 本文の最後の判定 {judged or '(空欄)'} と state {state} が食い違う"
                )
        items.append(cand)
    return items


def tally(cands: list[Candidate], targets: dict[str, int]) -> tuple[dict, list[str]]:
    superseded = {c.meta.get("supersedes") for c in cands if c.meta.get("supersedes")}
    seen: dict[str, Path] = {}
    errors = [e for c in cands for e in c.errors]
    rows = {s: {k: 0 for k in ("cands", "unreviewed", "ok", "ng", "hold", "final_ng", "withdrawn")} for s in SLOTS}
    for c in cands:
        if c.errors:
            continue
        if c.id in seen:
            errors.append(f"id 重複: {c.id}({seen[c.id].name} と {c.path.name})")
            continue
        seen[c.id] = c.path
        if c.id in superseded:
            continue  # 別ファイルの修正版が引き継いだ(重複加算しない)
        row = rows[c.meta["slot"]]
        st = c.meta["state"]
        if st == "withdrawn":
            row["withdrawn"] += 1
            continue
        row["cands"] += 1
        if st in OK_LIKE:
            row["ok"] += 1
        else:
            row[st] += 1
    for s in SLOTS:
        row = rows[s]
        t = targets[s]
        row["target"] = t
        row["shortfall"] = max(0, t - row["ok"])
        row["add"] = row["shortfall"] * 2
        row["surplus"] = max(0, row["ok"] - t)
    return rows, errors


def render(rows: dict, title: str) -> str:
    head = f"候補集計: {title}(目標 朝 {rows['morning']['target']} / 夜 {rows['night']['target']})"
    cols = ["スロット", "候補", "未レビュー", "OK", "NG", "保留", "完成稿NG", "余剰OK", "不足", "追加(不足×2)"]
    lines = [head, "  ".join(cols)]
    for s in SLOTS:
        r = rows[s]
        lines.append(
            "  ".join(
                str(v).ljust(len(c) + (len(c.encode("utf-8")) - len(c)) // 2)
                for v, c in zip(
                    [SLOT_LABEL[s], r["cands"], r["unreviewed"], r["ok"], r["ng"], r["hold"], r["final_ng"], r["surplus"], r["shortfall"], r["add"]],
                    cols,
                )
            )
        )
    pending = [SLOT_LABEL[s] for s in SLOTS if rows[s]["unreviewed"]]
    short = [f"{SLOT_LABEL[s]} 不足 {rows[s]['shortfall']}" for s in SLOTS if rows[s]["shortfall"]]
    surplus = [f"{SLOT_LABEL[s]} 余剰 OK {rows[s]['surplus']}" for s in SLOTS if rows[s]["surplus"]]
    if pending:
        lines.append(f"判定: 未レビューあり({'・'.join(pending)})。選別を終えてから追加数を確定する(仕上げには進めない)。")
    elif short:
        adds = " / ".join(f"{SLOT_LABEL[s]} {rows[s]['add']}" for s in SLOTS)
        lines.append(f"判定: 仕上げ(G1b)へ進めない({'・'.join(short)})。G1a へ戻り {adds} を追加する。")
    else:
        lines.append("判定: 朝夜とも OK が目標に達した。仕上げ(G1b)へ進める(目標数だけ完成稿にする)。")
    if surplus:
        lines.append(f"余剰: {'・'.join(surplus)}(候補 OK のまま次回バッチへ持ち越す。完成稿にはしない)。")
    return "\n".join(lines)


def write_index(directory: Path, cands: list[Candidate]) -> Path:
    """一覧 INDEX.md(ID・状態・版・リンクだけ。原記録は各ファイル)。"""
    out = directory / "INDEX.md"
    lines = [
        f"# {directory.name} 候補一覧(tally.py が生成。ID・状態・版・リンクだけ。内容と判定の正は各ファイル)",
        "",
        "| ID | 朝夜 | 状態 | 版 | 完成稿 no | ファイル |",
        "|---|---|---|---|---|---|",
    ]
    for c in sorted(cands, key=lambda c: (c.meta.get("slot", ""), c.id)):
        m = c.meta
        lines.append(
            f"| {c.id} | {SLOT_LABEL.get(m.get('slot'), '?')} | {STATE_LABEL.get(m.get('state'), m.get('state'))} | "
            f"{m.get('version', '')} | {m.get('stock_no', '') or '—'} | [{c.path.name}]({c.path.name}) |"
        )
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return out


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("target_dir", help="候補バッチのディレクトリ。'plan' なら候補数の計画だけ出す")
    ap.add_argument("--target", nargs=2, type=int, default=[7, 7], metavar=("MORNING", "NIGHT"), help="目標数(既定 7 7)")
    ap.add_argument("--carry-from", nargs="*", default=[], metavar="DIR", help="前バッチの余剰 OK(state=ok)だけを持ち越して数える")
    ap.add_argument("--write-index", action="store_true", help="INDEX.md を生成する")
    args = ap.parse_args(argv)
    targets = {"morning": args.target[0], "night": args.target[1]}

    if args.target_dir == "plan":
        print(f"候補計画: 目標 朝 {targets['morning']} / 夜 {targets['night']} → 用意する候補 朝 {targets['morning'] * 2} / 夜 {targets['night'] * 2}(目標の 2 倍)")
        return 0

    directory = Path(args.target_dir)
    if not directory.is_dir():
        print(f"ディレクトリがない: {directory}", file=sys.stderr)
        return 2
    cands = load_dir(directory)
    carried: list[Candidate] = []
    for old in args.carry_from:
        carried += [c for c in load_dir(Path(old)) if c.meta.get("state") == "ok" and not c.errors]
    rows, errors = tally(cands + carried, targets)
    title = directory.as_posix() + (f" + 持ち越し {len(carried)} 件" if carried else "")
    print(render(rows, title))
    if args.write_index:
        print(f"一覧を生成: {write_index(directory, cands)}")
    if errors:
        print("NG:")
        for e in errors:
            print(f"  - {e}")
        return 1
    print("形式チェック: OK(必須項目・slot・state・判定と state の整合・id 重複)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
