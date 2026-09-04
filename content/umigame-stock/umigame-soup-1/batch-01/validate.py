"""batch-01: stock_items.py の素材 14 項目を機械検証する。

仕様の正は docs/app/sets/umigame-soup-1.html セクション 4（字数・件数）・5.2（画風固定行）・
6（#AIart 必須・「第 N 問」を書かない）と docs/app/generators/umigame-prebuilt.html 8.3
（ナレーション予算。ここでは推定長で事前検査し、実測長の最終判定はビルド時）。

使い方: python3 validate.py  （終了コード 0 = 全件 OK）
"""

from __future__ import annotations

import re
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parent / "common"))

from stock_items import ITEMS  # noqa: E402
from umigame_common import (  # noqa: E402
    ANSWER_HEADS,
    PROHIBITION_LINE,
    PUZZLE_TYPES,
    REQUIRED_KEYS,
    STYLE_LINE,
)

PROBLEM_MIN, PROBLEM_MAX = 78, 85
FACT_MIN, FACT_MAX = 8, 12
QUESTION_MIN, QUESTION_MAX = 15, 20
HOOK_MAX = 14  # 12 字前後（74px・1 行）
RULE_MAX = 50  # 45 字前後（34px・2 行）
QUESTIONER_MAX, MASTER_MAX = 16, 17  # 吹き出し 1 行
CHARACTER_LINE_MAX = 17
TITLE_MAX = 100
CAPTION_MAX = 2200
# ナレーション予算（8.3）: problem 実測長 + 1.2 秒 + rule 実測長 <= 21.0 秒。
# Polly Takumi 125% の実測（21-2: 78 字 + 37 字 = 17.8 秒）から 1 字 0.155 秒として推定する。
NARRATION_SEC_PER_CHAR = 0.155
NARRATION_GAP_SEC = 1.2
NARRATION_BUDGET_SEC = 21.0
CONTENT_KEY_RE = re.compile(r"^\d{3}-[a-z0-9]+(-[a-z0-9]+)*$")
NUMBERED_RE = re.compile(r"第\s*\d+\s*問")

errors: list[str] = []
warnings: list[str] = []


def check_item(it: dict) -> None:
    """1 問の全項目を検査し、errors / warnings に追記する。

    Args:
        it: stock_items.py の 1 問。
    """
    no = it.get("no", "?")
    missing = [k for k in REQUIRED_KEYS if k not in it]
    extra = [k for k in it if k not in REQUIRED_KEYS]
    if missing:
        errors.append(f"{no}: 必須キー不足 {missing}")
        return
    if extra:
        errors.append(f"{no}: 未知のキー {extra}")

    if not CONTENT_KEY_RE.match(it["content_key"]):
        errors.append(f"{no}: content_key の形式が不正: {it['content_key']}")
    if not it["title"] or len(it["title"]) > TITLE_MAX:
        errors.append(f"{no}: title が空または {TITLE_MAX} 字超")
    if it["puzzle_type"] not in PUZZLE_TYPES:
        errors.append(f"{no}: puzzle_type は {PUZZLE_TYPES} のいずれか")
    if not isinstance(it["difficulty"], int) or not 1 <= it["difficulty"] <= 5:
        errors.append(f"{no}: difficulty は 1〜5 の整数")

    p = it["problem_text"]
    if not PROBLEM_MIN <= len(p) <= PROBLEM_MAX:
        errors.append(f"{no}: problem_text が {len(p)} 字（{PROBLEM_MIN}〜{PROBLEM_MAX}）")
    if "\n" in p:
        errors.append(f"{no}: problem_text に改行がある")

    if not it["truth"].strip():
        errors.append(f"{no}: truth が空")

    fs = it["fact_sheet"]
    if not (isinstance(fs, list) and all(isinstance(f, str) and f.strip() for f in fs)):
        errors.append(f"{no}: fact_sheet は非空文字列の配列")
    elif not FACT_MIN <= len(fs) <= FACT_MAX:
        errors.append(f"{no}: fact_sheet が {len(fs)} 件（{FACT_MIN}〜{FACT_MAX}）")

    qs = it["expected_questions"]
    if not (isinstance(qs, list) and all(isinstance(q, dict) and q.get("q") and q.get("a") for q in qs)):
        errors.append(f"{no}: expected_questions は {{q, a}} の配列")
    else:
        if not QUESTION_MIN <= len(qs) <= QUESTION_MAX:
            errors.append(f"{no}: expected_questions が {len(qs)} 件（{QUESTION_MIN}〜{QUESTION_MAX}）")
        heads = Counter()
        for q in qs:
            head = next((h for h in ANSWER_HEADS if q["a"].startswith(h)), None)
            if head is None:
                errors.append(f"{no}: 期待回答の冒頭が {ANSWER_HEADS} でない: {q['a'][:20]}")
            else:
                heads[head] += 1
        for h in ("はい", "いいえ", "関係ない", "正解"):
            if heads[h] == 0:
                errors.append(f"{no}: 期待回答「{h}」の質問が 1 件もない（正解に向かう質問・引っかけ・無関係・正解宣言を混ぜる）")
        if len({q["q"] for q in qs}) != len(qs):
            errors.append(f"{no}: expected_questions に重複した質問がある")

    if not it["hook"] or len(it["hook"]) > HOOK_MAX:
        errors.append(f"{no}: hook が空または {HOOK_MAX} 字超（{len(it['hook'])} 字）")
    elif len(it["hook"]) < 8:
        warnings.append(f"{no}: hook が {len(it['hook'])} 字（12 字前後が目安）")
    if not it["rule_text"] or len(it["rule_text"]) > RULE_MAX:
        errors.append(f"{no}: rule_text が空または {RULE_MAX} 字超")

    nar = it["narration"]
    if not (isinstance(nar, dict) and nar.get("problem") and nar.get("rule")):
        errors.append(f"{no}: narration は {{problem, rule}} の両方が必要")
    else:
        if re.search(r"[「」（）()【】]", nar["problem"]):
            errors.append(f"{no}: narration.problem に括弧・記号が残っている（読み上げ用の文にする）")
        est = (len(nar["problem"]) + len(nar["rule"])) * NARRATION_SEC_PER_CHAR + NARRATION_GAP_SEC
        if est > NARRATION_BUDGET_SEC:
            errors.append(f"{no}: ナレーション推定 {est:.1f} 秒（予算 {NARRATION_BUDGET_SEC} 秒。実測は ビルド時）")
        elif est > NARRATION_BUDGET_SEC - 1.0:
            warnings.append(f"{no}: ナレーション推定 {est:.1f} 秒（予算まで 1 秒未満）")

    pe = it["play_example"]
    if not (isinstance(pe, list) and len(pe) == 6):
        errors.append(f"{no}: play_example は 6 要素（3 往復）")
    else:
        yes = 0
        for i, turn in enumerate(pe):
            want = "questioner" if i % 2 == 0 else "master"
            if turn.get("role") != want:
                errors.append(f"{no}: play_example[{i}] の role は {want}")
            text = turn.get("text", "")
            limit = QUESTIONER_MAX if want == "questioner" else MASTER_MAX
            if not text or len(text) > limit:
                errors.append(f"{no}: play_example[{i}] が空または {limit} 字超: {text}")
            if want == "master":
                if not text.startswith(("はい", "いいえ", "関係ありません")):
                    errors.append(f"{no}: play_example[{i}] の返答は はい / いいえ / 関係ありません で始める: {text}")
                if text.startswith("はい"):
                    yes += 1
        if yes < 1:
            errors.append(f"{no}: play_example の返答に「はい」が 1 つもない（喜びポーズの約束事）")

    cl = it["character_lines"]
    try:
        for path, text in (
            ("master.intro", cl["master"]["intro"]),
            ("master.outro", cl["master"]["outro"]),
        ):
            if not text or len(text) > CHARACTER_LINE_MAX:
                errors.append(f"{no}: character_lines.{path} が空または {CHARACTER_LINE_MAX} 字超")
        if not cl["jr"]["outro"]:
            errors.append(f"{no}: character_lines.jr.outro が空")
    except (KeyError, TypeError):
        errors.append(f"{no}: character_lines の構造が不正（master.intro / master.outro / jr.outro）")

    ip = it["illustration_prompt"]
    if STYLE_LINE not in ip:
        errors.append(f"{no}: illustration_prompt に画風固定行がない")
    if PROHIBITION_LINE not in ip:
        errors.append(f"{no}: illustration_prompt に固定の禁止事項がない")

    cap = it["caption"]
    if "#AIart" not in cap:
        errors.append(f"{no}: caption に #AIart がない")
    if len(cap) > CAPTION_MAX:
        errors.append(f"{no}: caption が {len(cap)} 字（上限 {CAPTION_MAX}）")
    if NUMBERED_RE.search(cap):
        errors.append(f"{no}: caption に「第 N 問」がある（LRU 消費のため投稿順は確定しない）")
    if p not in cap:
        errors.append(f"{no}: caption に問題文の再掲がない")

    if "完全オリジナル" not in it["source_note"]:
        errors.append(f"{no}: source_note に完全オリジナル宣言がない")


def main() -> int:
    """全問を検査し、結果を標準出力へ出す。

    Returns:
        終了コード（0 = 全件 OK）。
    """
    for it in ITEMS:
        check_item(it)
    for field in ("no", "content_key", "problem_text", "title"):
        dup = [k for k, c in Counter(it.get(field) for it in ITEMS).items() if c > 1]
        if dup:
            errors.append(f"{field} が重複: {dup}")
    serials = sorted(int(it["content_key"][:3]) for it in ITEMS if CONTENT_KEY_RE.match(it.get("content_key", "")))
    if serials and serials != list(range(serials[0], serials[0] + len(serials))):
        errors.append(f"content_key の連番が連続していない: {serials}")

    types = Counter(it.get("puzzle_type") for it in ITEMS)
    diffs = Counter(it.get("difficulty") for it in ITEMS)
    print(f"validate: {len(ITEMS)} 問 / 型 {dict(types)} / 難易度 {dict(sorted(diffs.items()))}")
    for w in warnings:
        print(f"  WARN {w}")
    if errors:
        for e in errors:
            print(f"  NG   {e}")
        print(f"validate: NG {len(errors)} 件")
        return 1
    print(f"validate: 全 {len(ITEMS)} 問 OK（警告 {len(warnings)} 件）")
    return 0


if __name__ == "__main__":
    sys.exit(main())
