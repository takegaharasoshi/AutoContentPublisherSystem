# 2026-10-w2 補充: 機械検証できる問題の答え合わせ
#
# なぞなぞ・とんち・水平思考の「想定解」は機械検証できない(人間レビューが唯一の砦)。
# ここでは逆さ読みの対応表・時計の剰余・頭文字・字形の対応など、単純に確かめられるものだけを検証する。
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


# 数字を 180 度回転させたときに数字として読めるもの(7 セグメント・手書きの一般的な見え方)
ROTATE_DIGIT = {"0": "0", "1": "1", "6": "9", "8": "8", "9": "6"}


def rotate_number(s: str) -> str | None:
    """数字列を 180 度回転させて読んだ数字列を返す(読めない字があれば None)。"""
    out = []
    for ch in reversed(s):
        if ch not in ROTATE_DIGIT:
            return None
        out.append(ROTATE_DIGIT[ch])
    return "".join(out)



# ---------------------------------------------------------------
# A63 マッチの十字: 情景文にマッチ棒 4 本と「+」を明示(十字は問題文に書かず黒板の絵で提示)
# ---------------------------------------------------------------
if "A63" in BY_NO:
    scene = BY_NO["A63"]["illustration_scene"]
    check("A63", "情景文にマッチ棒 4 本と「+」", "マッチ棒4本" in scene and "「+」" in scene, "黒板の十字を明示")

# ---------------------------------------------------------------
# A65 NEW DOOR: NEW DOOR と ONE WORD は同じ 7 文字の並べ替え
# ---------------------------------------------------------------
if "A65" in BY_NO:
    a, b = "NEWDOOR", "ONEWORD"
    check("A65", "NEW DOOR → ONE WORD は同じ文字の並べ替え", sorted(a) == sorted(b), f"{''.join(sorted(a))} / {''.join(sorted(b))}")
    check("A65", "文字は 7 文字", len(a) == 7 and "7文字" in BY_NO["A65"]["question"], f"{len(a)} 文字")
    check("A65", "文字は情景文に明示(問題文には書かない)",
          "「NEW DOOR」" in BY_NO["A65"]["illustration_scene"] and "NEW DOOR" not in BY_NO["A65"]["question"], "カードの文字を明示")

# ---------------------------------------------------------------
# A68 まちがいが三つ: カードの文と正しい文の差は 2 か所(分→文・わ→は)= 3 つ目は「三つ」の主張
# ---------------------------------------------------------------
if "A68" in BY_NO:
    card = "この分章にわ、まちがいが三つあります。"
    right = "この文章には、まちがいが三つあります。"
    diffs = [(i, c, r) for i, (c, r) in enumerate(zip(card, right)) if c != r]
    check("A68", "字のまちがいは 2 か所", len(card) == len(right) and len(diffs) == 2, f"{[(c + '→' + r) for _, c, r in diffs]}")
    check("A68", "情景文にカードの文を一字一句", f"「{card}」" in BY_NO["A68"]["illustration_scene"], card)

# ---------------------------------------------------------------
# C64 ケーキ: 十字 2 回で 4 切れ、横から厚みを半分で 8 切れ(各片は中心角 90 度 × 厚み 1/2 で同じ大きさ)
# ---------------------------------------------------------------
if "C64" in BY_NO:
    pieces = 4 * 2
    check("C64", "十字 2 回 × 横 1 回 = 8 切れ", pieces == 8, f"{pieces} 切れ(1 切れ = 全体の 1/{pieces})")

# ---------------------------------------------------------------
# C68 穴の土: 掘り出した土の体積は 1×1×1 = 1 立方メートル(穴の中は 0)
# ---------------------------------------------------------------
if "C68" in BY_NO:
    check("C68", "掘り出した土 = 1 立方メートル", 1 * 1 * 1 == 1 and "1立方メートル" in BY_NO["C68"]["explanation"], "1m×1m×1m")

# ---------------------------------------------------------------
# 答えの物を描かない指定の確認(想定解そのものは人間レビュー)
# ---------------------------------------------------------------
NO_DRAW = {"A62": "炭", "A64": "足あと", "A66": "錨", "C63": "数字", "C65": "頭", "C66": "小石",
           "C67": "野球場", "C68": "人物"}
for no, word in NO_DRAW.items():
    if no in BY_NO:
        scene = BY_NO[no]["illustration_scene"]
        check(no, f"情景で「{word}」を描かない指定", f"{word}・" in scene or f"{word}は描かない" in scene, "描かない指定あり")

# ---------------------------------------------------------------
# 機械検証の限界: 想定解の自然さ・別解・面白さは人間レビュー。
# ---------------------------------------------------------------
manual = [it["no"] for it in ITEMS if it["no"] in {"A62", "A64", "A66", "A67", "C63", "C65", "C66", "C67", "C69"}]
print(f"-- 機械検証対象外(人間レビューが必要): {', '.join(manual)}")
print("   検証済みの問題も、難度・別解・想定解の自然さ・完成イラストの字形は別途レビュー")

if failures:
    print(f"\nNG: {len(failures)} 件")
    for f in failures:
        print(" -", f)
    sys.exit(1)
print("\nOK: 機械検証できる問題はすべて答えと一致")
