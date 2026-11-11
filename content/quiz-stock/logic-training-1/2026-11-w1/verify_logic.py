# 2026-11-w1 補充: 機械検証できる問題の答え合わせ
#
# なぞなぞ・とんち・水平思考の「想定解」は機械検証できない(人間レビューが唯一の砦)。
# ここでは漢字の画数・元号の頭文字・情景文の描かない指定など、単純に確かめられるものだけを検証する。
# 今回のバッチに L3(フェルミ推定)は含まれないため、算数の検算セクションはない。
from __future__ import annotations

import sys

sys.path.insert(0, __file__.rsplit("/", 1)[0])
from stock_items import ITEMS

BY_NO = {it["no"]: it for it in ITEMS}
failures: list[str] = []


def check(no: str, label: str, ok: bool, detail: str) -> None:
    """1 件の検証結果を記録して表示する。

    Args:
        no: 問題番号。
        label: 検証項目名。
        ok: 検証が通ったか。
        detail: 表示する計算・列挙の要約。
    """
    mark = "OK " if ok else "NG "
    print(f"{mark}{no} {label}: {detail}")
    if not ok:
        failures.append(f"{no} {label}: {detail}")



# ---------------------------------------------------------------
# A84 木に二画: 挙げた字の画数 = 木 4 画 + 2 画 = 6 画
# ---------------------------------------------------------------
STROKES = {"木": 4, "休": 6, "米": 6, "朱": 6, "机": 6, "朽": 6, "朴": 6}
if "A84" in BY_NO:
    listed = [c for c in STROKES if c != "木"]
    it = BY_NO["A84"]
    check("A84", "挙げた字はすべて 6 画(木 4 + 2)", all(STROKES[c] == STROKES["木"] + 2 for c in listed), "".join(listed))
    check("A84", "答えの字が解説にもある", all(c in it["answer"] and c in it["explanation"] for c in listed), f"{len(listed)} 字")
    check("A84", "名人の数(5つ)<= 挙げた字の数", "5つ" in it["question"] and len(listed) >= 5, f"{len(listed)} 字")

# ---------------------------------------------------------------
# A86 元号の頭文字: 明治・大正・昭和・平成・令和の読みの 1 文字目 = め・た・し・へ・れ
# ---------------------------------------------------------------
ERAS = [("明治", "めいじ"), ("大正", "たいしょう"), ("昭和", "しょうわ"), ("平成", "へいせい"), ("令和", "れいわ")]
if "A86" in BY_NO:
    it = BY_NO["A86"]
    heads = [yomi[0] for _, yomi in ERAS]
    check("A86", "頭文字 = め・た・し・へ・れ", heads == list("めたしへれ"), "・".join(heads))
    check("A86", "答えが「れ」で元号 5 つを挙げる", it["answer"].startswith("れ") and all(k in it["answer"] for k, _ in ERAS), it["answer"])
    check("A86", "情景文に提示の 4 字と ? がある", all(f"「{c}」" in it["illustration_scene"] for c in "めたしへ?"), "め・た・し・へ・?")
    check("A86", "情景文・問題文に答えの字と元号がない", "「れ」" not in it["illustration_scene"] and not any(k in it["question"] + it["illustration_scene"] for k, _ in ERAS), "なし")

# ---------------------------------------------------------------
# A88 親: 立 + 木 + 見
# ---------------------------------------------------------------
if "A88" in BY_NO:
    it = BY_NO["A88"]
    check("A88", "答え・解説に 立・木・見 がある", all(c in it["answer"] and c in it["explanation"] for c in "立木見"), it["answer"])

# ---------------------------------------------------------------
# 情景文に答えの物の名前を書かない(スキルのイラスト方針 10。否定形でも書かない)
# ---------------------------------------------------------------
FORBIDDEN = {
    "A83": ["鉛筆", "芯", "ノート", "文房具"], "A85": ["つらら", "氷", "雪", "軒", "屋根"], "A87": ["卵", "たまご", "黄身", "フライパン"],
    "A88": ["親", "母", "父"], "A89": ["塩", "しお", "氷", "料理"],
    "C84": ["エレベーター", "体重計", "ボタン"], "C85": ["長い線", "2本"], "C86": ["眠", "寝", "夢", "椅子", "いす"],
    "C87": ["スマホ", "画面", "携帯", "電話"], "C88": ["メリーゴーラウンド", "遊園地", "木馬", "回"],
    "C89": ["赤い明かり", "赤い光", "暗室", "照明", "ランプ", "ライト", "電気"], "C90": ["取っ手", "回", "皿"],
}
for no, words in FORBIDDEN.items():
    if no in BY_NO:
        scene = BY_NO[no]["illustration_scene"]
        hit = [w for w in words if w in scene]
        check(no, "情景文に答えの物の名前がない", not hit, "なし" if not hit else f"含む: {hit}")

if failures:
    print(f"\nNG: {len(failures)} 件")
    for f in failures:
        print(" -", f)
    sys.exit(1)
print("\nOK: 機械検証できる問題はすべて答えと一致")
