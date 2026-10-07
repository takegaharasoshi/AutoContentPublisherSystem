"""batch-01: stock_items.py の素材 17 項目 + 管理項目（コア宣言 core 等）を機械検証する。

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

from stock_items import ITEMS, POST_ORDER  # noqa: E402
from umigame_common import (  # noqa: E402
    ANSWER_HEADS,
    CAPTION_PLAY,
    PROHIBITION_LINE,
    PUZZLE_TYPES,
    REQUIRED_KEYS,
    STYLE_LINE,
)

PROBLEM_MIN, PROBLEM_MAX = 78, 85
FACT_MIN, FACT_MAX = 8, 20  # 上限は 2026-09-26 に 12 → 20（PoC の目安がそのまま上限になっていたため。セット別設計書 4）
QUESTION_MIN, QUESTION_MAX = 15, 20
HOOK_MAX = 14  # 12 字前後（74px・1 行）
RULE_MAX = 50  # 45 字前後（34px・2 行）
QUESTIONER_MAX, MASTER_MAX = 16, 17  # 吹き出し 1 行
CHARACTER_LINE_MAX = 17
TITLE_MAX = 100
CAPTION_MAX = 2200
# truth の上限（21-6d3e。翌日リールのキャプション末尾で全文公開するため）。改行も 1 字に数える。行数は検査しない
# （改行は読みやすい位置に書き手が入れ、機械的に決めないため）。値の根拠はセット別設計書 4。
TRUTH_MAX = 400
# 投稿時に差し込まれる前回の真相ブロック（21-6h）の最大の見積もり: 区切り行と「・」の行・【真相】の定型 60 字 + 前回の title + truth。
PREV_BLOCK_RESERVE = 60 + TITLE_MAX + TRUTH_MAX
# ナレーション予算（8.3）: problem 実測長 + 1.2 秒 + rule 実測長 <= 21.0 秒。
# Polly Takumi 125% の実測（21-2: 78 字 + 37 字 = 17.8 秒）から 1 字 0.155 秒として推定する。
NARRATION_SEC_PER_CHAR = 0.155
NARRATION_GAP_SEC = 1.2
NARRATION_BUDGET_SEC = 21.0
CONTENT_KEY_RE = re.compile(r"^\d{3}-[a-z0-9]+(-[a-z0-9]+)*$")
NUMBERED_RE = re.compile(r"第\s*\d+\s*問")
# コア宣言の様式（作問スキル工程 3。2026-09-20 の型別分冊で型ごとに固定。story は 2026-09-22 の物語先行方式で置き換え）:
#   misdirection: 「コア: 「<語・状況>」を <誤認> と読ませる → 実際は <反転>」
#   story:        「コア: 物語「<一文要約>」の <B = 隠す出来事・事情> を隠して「<A→C の見え方>」を出す → 復元: <B を戻した一文>」
CORE_RE_BY_TYPE = {
    "misdirection": re.compile(r"^コア: 「.+」を.+と読ませる → 実際は.+$"),
    "story": re.compile(r"^コア: 物語「.+」の.+を隠して「.+」を出す → 復元: .+$"),
}
CORE_FORMAT_BY_TYPE = {
    "misdirection": "「コア: 「…」を … と読ませる → 実際は …」",
    "story": "「コア: 物語「…」の … を隠して「…」を出す → 復元: …」",
}
CORE_MAX = 120
CORE_POINTS_MIN, CORE_POINTS_MAX = 1, 3  # 判定用のコアの要点（21-6c1。セット別設計書 5.1.1・5.1.2）
REVEAL_MAX = 70  # 正解時の開示文
CORE_POINT_MAX = 20  # コアの要点 1 個の字数（目安 15 字前後。個数は説明に必要なだけ。2026-09-30 ユーザー整理）
# 正解基準 judge_criteria（21-6d7b。セット別設計書 10.2「正解基準」）
CRITERIA_TEXT_MAX = 80  # points[].hit / touch の字数
CRITERIA_ERRORS_MAX = 3  # errors の個数（0 個も可）
CRITERIA_ERROR_MAX = 40  # errors 1 個の字数
# 確定事実シートに書いてはいけない境目の言い方（境目は正解基準にだけ書く）。漏洩防止の目印「正解宣言のとき以外は」の行は対象外
BOUNDARY_RE = re.compile(r"正解にする|正解にしない|正解とする|言えたら正解|惜しい")
BOUNDARY_EXEMPT = "正解宣言のとき以外は"
# 欠番の content_key 連番（差し替えで ITEMS から外し、再利用しない番号。DB の行の扱いは全数レビュー後に決める）。
# 002 = U11（2026-09-26 に U27 = 015 へ差し替え。素材の全数レビュー指摘 17）
# 011 = U23（2026-09-26 に U28 = 016 へ差し替え。本家ウミガメのスープ）
RETIRED_SERIALS = {2, 11}

errors: list[str] = []
warnings: list[str] = []


def check_judge_criteria(no: str, jc: object, cps: object) -> None:
    """正解基準 judge_criteria を検査し、errors に追記する。

    Args:
        no: 問題番号（メッセージ用）。
        jc: judge_criteria の値。
        cps: 同じ問の core_points（points の個数の照合に使う）。
    """
    if not isinstance(jc, dict) or set(jc) != {"points", "errors"}:
        errors.append(f"{no}: judge_criteria は {{points, errors}} の dict")
        return
    pts = jc["points"]
    if not isinstance(pts, list) or not isinstance(cps, list) or len(pts) != len(cps):
        n = len(pts) if isinstance(pts, list) else "-"
        errors.append(f"{no}: judge_criteria.points の個数（{n}）が core_points と一致しない")
    for i, pt in enumerate(pts if isinstance(pts, list) else [], start=1):
        if not isinstance(pt, dict) or set(pt) != {"hit", "touch"}:
            errors.append(f"{no}: judge_criteria.points[{i}] は {{hit, touch}} の dict")
            continue
        for key in ("hit", "touch"):
            v = pt[key]
            if not isinstance(v, str) or not v.strip() or "\n" in v or len(v) > CRITERIA_TEXT_MAX:
                ln = len(v) if isinstance(v, str) else "-"
                errors.append(f"{no}: judge_criteria.points[{i}].{key} は改行なし {CRITERIA_TEXT_MAX} 字以内の空でない文字列（{ln} 字）")
        if pt["hit"] == pt["touch"]:
            errors.append(f"{no}: judge_criteria.points[{i}] の hit と touch が同文")
    errs = jc["errors"]
    if not isinstance(errs, list) or len(errs) > CRITERIA_ERRORS_MAX:
        errors.append(f"{no}: judge_criteria.errors は 0〜{CRITERIA_ERRORS_MAX} 個のリスト")
    elif any(not isinstance(e, str) or not e.strip() or "\n" in e or len(e) > CRITERIA_ERROR_MAX for e in errs):
        errors.append(f"{no}: judge_criteria.errors の要素は改行なし {CRITERIA_ERROR_MAX} 字以内の空でない文字列")


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
    core = it["core"]
    if not isinstance(core, str) or not core.strip():
        errors.append(f"{no}: core（コア宣言）が空。作問スキル umigame-problem-writer 工程 3 の 1 文を入れる")
    elif it["puzzle_type"] in CORE_RE_BY_TYPE and not CORE_RE_BY_TYPE[it["puzzle_type"]].match(core):
        fmt = CORE_FORMAT_BY_TYPE[it["puzzle_type"]]
        errors.append(f"{no}: core は {it['puzzle_type']} 型の様式 {fmt}（→ を含む 1 文）: {core[:30]}")
    elif "\n" in core or len(core) > CORE_MAX:
        errors.append(f"{no}: core は改行なし {CORE_MAX} 字以内（{len(core)} 字）")

    cps = it["core_points"]
    if not isinstance(cps, list) or not CORE_POINTS_MIN <= len(cps) <= CORE_POINTS_MAX:
        errors.append(f"{no}: core_points は {CORE_POINTS_MIN}〜{CORE_POINTS_MAX} 個のリスト")
    if isinstance(cps, list) and any(not isinstance(x, str) or not x.strip() or "\n" in x for x in cps):
        errors.append(f"{no}: core_points の要素は改行なしの空でない文字列")
    if isinstance(cps, list) and any(isinstance(x, str) and len(x) > CORE_POINT_MAX for x in cps):
        errors.append(f"{no}: core_points の要素は {CORE_POINT_MAX} 字以内（{[len(x) for x in cps]} 字）")
    rv = it["reveal_text"]
    if not isinstance(rv, str) or not rv.strip() or "\n" in rv or len(rv) > REVEAL_MAX:
        errors.append(f"{no}: reveal_text は改行なし {REVEAL_MAX} 字以内の空でない文字列（{len(rv) if isinstance(rv, str) else '-'} 字）")

    check_judge_criteria(no, it["judge_criteria"], cps)

    p = it["problem_text"]
    if not PROBLEM_MIN <= len(p) <= PROBLEM_MAX:
        errors.append(f"{no}: problem_text が {len(p)} 字（{PROBLEM_MIN}〜{PROBLEM_MAX}）")
    if "\n" in p:
        errors.append(f"{no}: problem_text に改行がある")

    if not it["truth"].strip():
        errors.append(f"{no}: truth が空")
    elif len(it["truth"]) > TRUTH_MAX:
        errors.append(f"{no}: truth が {len(it['truth'])} 字（上限 {TRUTH_MAX}。改行込み）")

    fs = it["fact_sheet"]
    if not (isinstance(fs, list) and all(isinstance(f, str) and f.strip() for f in fs)):
        errors.append(f"{no}: fact_sheet は非空文字列の配列")
    elif not FACT_MIN <= len(fs) <= FACT_MAX:
        errors.append(f"{no}: fact_sheet が {len(fs)} 件（{FACT_MIN}〜{FACT_MAX}）")
    if isinstance(fs, list):
        for f in fs:
            if isinstance(f, str) and BOUNDARY_EXEMPT not in f and BOUNDARY_RE.search(f):
                errors.append(f"{no}: fact_sheet に境目の言い方がある（正解基準 judge_criteria へ移す）: {f[:30]}")

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
    elif not it["hook"].endswith("？"):
        errors.append(f"{no}: hook は「？」で終える（2026-09-26 素材レビュー）: {it['hook']}")
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
    if len(cap) + PREV_BLOCK_RESERVE > CAPTION_MAX:
        errors.append(
            f"{no}: caption が {len(cap)} 字（前回の真相ブロックの枠 {PREV_BLOCK_RESERVE} 字と合わせて上限 {CAPTION_MAX}）"
        )
    if not cap.startswith(f"【{it['title']}】\n"):
        errors.append(f"{no}: caption の見出しが【title】になっていない")
    if CAPTION_PLAY not in cap:
        errors.append(f"{no}: caption に遊び方と真相公開の予告がない")
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
    reused = sorted(RETIRED_SERIALS & set(serials))
    if reused:
        errors.append(f"欠番の content_key 連番を再利用している: {reused}")
    serials = sorted(set(serials) | RETIRED_SERIALS)
    if serials and serials != list(range(serials[0], serials[0] + len(serials))):
        errors.append(f"content_key の連番が連続していない: {serials}")

    nos = [it.get("no") for it in ITEMS]
    if sorted(POST_ORDER) != sorted(nos) or len(set(POST_ORDER)) != len(POST_ORDER):
        errors.append(f"POST_ORDER が ITEMS の問題番号と一致しない（過不足・重複）: {POST_ORDER}")
    else:
        type_of = {it["no"]: it["puzzle_type"] for it in ITEMS}
        seq = [type_of[n] for n in POST_ORDER]
        same = [f"{POST_ORDER[i]}-{POST_ORDER[i + 1]}" for i in range(len(seq) - 1) if seq[i] == seq[i + 1]]
        if same:
            warnings.append(f"POST_ORDER で同じ型が続く（story / misdirection の交互が既定）: {same}")

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
