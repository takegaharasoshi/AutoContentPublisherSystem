# 2026-10-w1 補充: 機械検証できる問題の答え合わせ
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
# A54 数字の輪: 各カードの左辺の輪の数の合計が右辺と一致し、2581 は 2
# ---------------------------------------------------------------
LOOPS = {"0": 1, "1": 0, "2": 0, "3": 0, "4": 0, "5": 0, "6": 1, "7": 0, "8": 2, "9": 1}
if "A54" in BY_NO:
    cards = [("8809", 6), ("1111", 0), ("6666", 4)]
    for left, right in cards:
        n = sum(LOOPS[c] for c in left)
        check("A54", f"{left}={right}", n == right, f"輪の数 {n}")
    ans = sum(LOOPS[c] for c in "2581")
    check("A54", "2581 の輪の数", ans == 2, f"{ans}")
    check("A54", "answer は 2", BY_NO["A54"]["answer"].startswith("2"), BY_NO["A54"]["answer"])
    check("A54", "カードに 4 を使わない(書体で輪が閉じる)", "4" not in "8809111166662581", "4 なし")
    scene = BY_NO["A54"]["illustration_scene"]
    check("A54", "式は情景文に明示(問題文には書かない)",
          all(f"「{s}」" in scene for s in ["8809=6", "1111=0", "6666=4", "2581=?"])
          and "8809" not in BY_NO["A54"]["question"], "4 枚の式を情景文に明示")

# ---------------------------------------------------------------
# A56 62−63=1: 数字 1 つの移動で成立するのは 6 を 2 の指数へ動かす形だけ(横並びの移動は全列挙で不成立)
# ---------------------------------------------------------------
if "A56" in BY_NO:
    check("A56", "2^6 - 63 = 1", 2 ** 6 - 63 == 1, f"{2 ** 6} - 63 = {2 ** 6 - 63}")
    digits = list("6263")  # 左辺 62, 63 の 4 桁(右辺 1 は除いて横並び移動を全列挙)
    flat_ok = []
    for i in range(4):
        rest = digits[:i] + digits[i + 1:]
        for j in range(4):
            cand = rest[:j] + [digits[i]] + rest[j:]
            for k in range(1, 4):
                a, b = "".join(cand[:k]), "".join(cand[k:])
                if (a, b) != ("62", "63") and int(a) - int(b) == 1:
                    flat_ok.append(f"{a}-{b}")
    check("A56", "横並びの移動では成立しない(左辺 4 桁の並べ替え全列挙)", not flat_ok, f"成立 {flat_ok or 'なし'}")
    check("A56", "情景文に「62−63=1」", "「62−63=1」" in BY_NO["A56"]["illustration_scene"], "黒板の式を明示")

# ---------------------------------------------------------------
# A58 逆さ年: 1961 より後で 180 度回転しても同じに読む最初の年は 6009
# ---------------------------------------------------------------
if "A58" in BY_NO:
    check("A58", "1961 は逆さでも 1961", rotate_number("1961") == "1961", f"1961 → {rotate_number('1961')}")
    nxt = next(y for y in range(1962, 10000) if rotate_number(str(y)) == str(y))
    check("A58", "次の年", nxt == 6009, f"全列挙で {nxt}")
    check("A58", "answer は 6009 年", BY_NO["A58"]["answer"].startswith("6009"), BY_NO["A58"]["answer"])

# ---------------------------------------------------------------
# A59 マッチのグラス: 座標で 2 本移動後の形が逆さのグラスになり、さくらんぼが外に出る
# 元: 左縦 (0,0)-(0,2)・右縦 (2,0)-(2,2)・底 (0,0)-(2,0)・脚 (1,0)-(1,-2)。さくらんぼ (1,1)
# 移動: 底を (1,0)-(3,0) へずらし、左縦を (3,0)-(3,-2) へ
# ---------------------------------------------------------------
if "A59" in BY_NO:
    after = {((2, 0), (2, 2)), ((1, 0), (3, 0)), ((1, 0), (1, -2)), ((3, 0), (3, -2))}
    # 逆さのグラス = 下に開いたコの字(底 y=0 の x1..3 と、両端から下へ伸びる縦 2 本)+ 中央から上への脚
    cup = {((1, 0), (3, 0)), ((1, 0), (1, -2)), ((3, 0), (3, -2))}
    leg = ((2, 0), (2, 2))
    check("A59", "移動後は下に開いたコの字 + 中央の脚", cup | {leg} == after, "逆さのグラス")
    cherry = (1, 1)
    inside = 1 < cherry[0] < 3 and -2 < cherry[1] < 0
    check("A59", "さくらんぼはコの字の外", not inside, f"さくらんぼ {cherry} / 器の内側 x1..3, y-2..0")

# ---------------------------------------------------------------
# A60 HIJKLMNO: H から O までの連続した文字列
# ---------------------------------------------------------------
if "A60" in BY_NO:
    seq = "".join(chr(c) for c in range(ord("H"), ord("O") + 1))
    check("A60", "H から O まで", seq == "HIJKLMNO", seq)
    check("A60", "情景文に「HIJKLMNO」", "「HIJKLMNO」" in BY_NO["A60"]["illustration_scene"], "カードの文字を明示")

# ---------------------------------------------------------------
# A61 直線と曲線の文字: 上の組は直線だけ・下の組は曲線を含み、R は曲線を含む
# ---------------------------------------------------------------
STRAIGHT = set("AEFHIKLMNTVWXYZ")
CURVED = set("BCDGJOPQRSU")
if "A61" in BY_NO:
    check("A61", "26 文字を漏れなく 2 分", STRAIGHT | CURVED == set("ABCDEFGHIJKLMNOPQRSTUVWXYZ") and not STRAIGHT & CURVED, "直線 15 / 曲線 11")
    check("A61", "上の組は直線だけ", set("AEFHIKL") <= STRAIGHT, "A E F H I K L")
    check("A61", "下の組は曲線を含む", set("BCDJOPQ") <= CURVED, "B C D J O P Q")
    check("A61", "R は曲線を含む = 下の組", "R" in CURVED, "R")
    scene = BY_NO["A61"]["illustration_scene"]
    check("A61", "文字は情景文に明示(問題文には書かない)",
          "「A E F H I K L」" in scene and "「B C D J O P Q」" in scene and "「R」" in scene
          and "B C D" not in BY_NO["A61"]["question"], "2 列 + R を情景文に明示")

# ---------------------------------------------------------------
# 答えの物を描かない指定の確認(想定解そのものは人間レビュー)
# ---------------------------------------------------------------
NO_DRAW = {"A55": "ピアノ", "A57": "切手", "A60": "水", "C56": "写真", "C58": "3つ目のベッド",
           "C59": "ボール", "C61": "人物", "C62": "金魚"}
for no, word in NO_DRAW.items():
    if no in BY_NO:
        check(no, f"情景で「{word}」を描かない指定", word in BY_NO[no]["illustration_scene"].split("。")[-2]
              or f"{word}・" in BY_NO[no]["illustration_scene"], "描かない指定あり")

# ---------------------------------------------------------------
# 機械検証の限界: 想定解の自然さ・別解・面白さは人間レビュー。
# ---------------------------------------------------------------
manual = [it["no"] for it in ITEMS if it["no"] in {"A55", "A57", "C56", "C57", "C58", "C59", "C60", "C61", "C62"}]
print(f"-- 機械検証対象外(人間レビューが必要): {', '.join(manual)}")
print("   検証済みの問題も、難度・別解・想定解の自然さ・完成イラストの字形は別途レビュー")

if failures:
    print(f"\nNG: {len(failures)} 件")
    for f in failures:
        print(" -", f)
    sys.exit(1)
print("\nOK: 機械検証できる問題はすべて答えと一致")
