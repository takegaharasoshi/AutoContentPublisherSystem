# 2026-09-w4 補充: 機械検証できる問題の答え合わせ
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
# A47 駐車場: 逆さから読むと右から 86・87・88・89・90・91 の連番になり、? = 87
# ---------------------------------------------------------------
if "A47" in BY_NO:
    labels = ["16", "06", "68", "88", None, "98"]
    rotated = [rotate_number(x) if x else None for x in labels]
    seq = list(reversed(rotated))  # 逆さから見ると右端が左端になる
    expected = ["86", "87", "88", "89", "90", "91"]
    ok = all(a == b for a, b in zip(seq, expected) if a is not None) and seq[1] is None
    check("A47", "逆さ読みで連番", ok, f"逆さの並び {seq} / 期待 {expected}")
    check("A47", "87 は逆さでは数字にならない(L8 の形)", rotate_number("87") is None, "7 は回転後に数字として読めない")
    scene = BY_NO["A47"]["illustration_scene"]
    check("A47", "番号は情景文に明示(問題文には書かない)",
          all(f"「{x}」" in scene for x in ["16", "06", "68", "88", "?", "98"])
          and "16" not in BY_NO["A47"]["question"], "情景文に 6 マスの番号あり")
    check("A47", "answer に 87", BY_NO["A47"]["answer"].startswith("87"), BY_NO["A47"]["answer"])

# ---------------------------------------------------------------
# A48 IX → SIX: 前に S を足すと英語の 6
# ---------------------------------------------------------------
if "A48" in BY_NO:
    check("A48", "S + IX = SIX", "S" + "IX" == "SIX", "SIX = six = 6")
    check("A48", "情景文に「IX」", "「IX」" in BY_NO["A48"]["illustration_scene"], "黒板の文字を明示")

# ---------------------------------------------------------------
# A50 電卓: 0.7734 を逆さにすると hELLO(4→h, 3→E, 7→L, 0→O)
# ---------------------------------------------------------------
if "A50" in BY_NO:
    calc = {"0": "O", "3": "E", "4": "h", "7": "L"}
    digits = "07734"
    read = "".join(calc[d] for d in reversed(digits))
    check("A50", "逆さ読み", read == "hELLO", f"{digits} → {read}")
    check("A50", "情景文に「0.7734」", "「0.7734」" in BY_NO["A50"]["illustration_scene"], "液晶表示を明示")

# ---------------------------------------------------------------
# A51 時計: 10 時の 4 時間後は 2 時(12 時間制)
# ---------------------------------------------------------------
if "A51" in BY_NO:
    h = (10 + 4 - 1) % 12 + 1
    check("A51", "12 時間制で 10+4", h == 2, f"(10+4) を 12 時間制で = {h}")
    check("A51", "式は情景文に明示・時計は描かない",
          "「10+4=2」" in BY_NO["A51"]["illustration_scene"]
          and "時計・腕時計・人物は描かない" in BY_NO["A51"]["illustration_scene"], "答えの物を描かない指定あり")

# ---------------------------------------------------------------
# A52 OTTFFSS: One〜Eight の頭文字
# ---------------------------------------------------------------
if "A52" in BY_NO:
    words = ["One", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight"]
    initials = [w[0].upper() for w in words]
    check("A52", "頭文字列", initials[:7] == list("OTTFFSS") and initials[7] == "E",
          f"{''.join(initials)} / ? = {initials[7]}")
    scene = BY_NO["A52"]["illustration_scene"]
    check("A52", "カード 8 枚を情景文に明示",
          all(f"「{c}」" in scene for c in ["O", "T", "F", "S", "?"]), "O・T・T・F・F・S・S・?")

# ---------------------------------------------------------------
# A53 XII の上半分: 各字の上半分が見える形(X → V、I → I)
# ---------------------------------------------------------------
if "A53" in BY_NO:
    top_half = {"X": "V", "I": "I"}
    roman = {"XII": 12, "VII": 7}
    top = "".join(top_half[c] for c in "XII")
    check("A53", "XII の上半分", top == "VII" and roman[top] == 7 and roman["XII"] == 12,
          f"XII(12) の上半分 = {top}({roman[top]})")
    check("A53", "ローマ数字は情景に描かない",
          "ローマ数字・時計・人物は描かない" in BY_NO["A53"]["illustration_scene"], "答えの字形を描かない指定あり")

# ---------------------------------------------------------------
# C50 縄ばしご: 船が潮と同じだけ浮くので、浸かる段数は時間によらず一定
# ---------------------------------------------------------------
if "C50" in BY_NO:
    submerged = []
    for hour in range(4):
        sea = hour  # 海面の上昇(段)
        ship = hour  # 船(= はしご)の上昇(段)
        submerged.append(3 + sea - ship)
    check("C50", "3 時間後も 3 段", submerged == [3, 3, 3, 3], f"0〜3 時間後: {submerged}")

# ---------------------------------------------------------------
# C52 バス: 日本(左側通行)はドアが車体の左側。見えるのが右側面なら、進行方向は見る人の右
#   見る人は南に立って北を向く → バスの右側面が南向き → バスは東(= 見る人の右)へ進む
# ---------------------------------------------------------------
if "C52" in BY_NO:
    # 方位を角度で表す(北 0・東 90・南 180・西 270)。車体の右側面は進行方向 + 90 度を向く
    viewer_faces = 0  # 見る人は北を向く
    for heading, name in [(90, "東"), (270, "西")]:
        right_side_faces = (heading + 90) % 360
        visible = right_side_faces == (viewer_faces + 180) % 360  # 右側面が見る人の方(南)を向くか
        if heading == 90:
            check("C52", "東(見る人の右)へ進むとき右側面が見える", visible, f"進行 {name}: 右側面は {right_side_faces} 度")
        else:
            check("C52", "西(見る人の左)へ進むときは左側面(ドア側)が見える", not visible,
                  f"進行 {name}: 右側面は {right_side_faces} 度")
    check("C52", "answer は右", BY_NO["C52"]["answer"].startswith("右"), BY_NO["C52"]["answer"])
    check("C52", "情景にドアを描かない",
          "ドアは1つもない" in BY_NO["C52"]["illustration_scene"], "ドアなし・前後同形の指定あり")

# ---------------------------------------------------------------
# 機械検証の限界: 想定解の自然さ・別解・面白さは人間レビュー。
# ---------------------------------------------------------------
manual = [it["no"] for it in ITEMS if it["no"] in {"A49", "C49", "C51", "C53", "C54", "C55"}]
print(f"-- 機械検証対象外(人間レビューが必要): {', '.join(manual)}")
print("   検証済みの問題も、難度・別解・想定解の自然さ・完成イラストの字形は別途レビュー")

if failures:
    print(f"\nNG: {len(failures)} 件")
    for f in failures:
        print(" -", f)
    sys.exit(1)
print("\nOK: 機械検証できる問題はすべて答えと一致")
