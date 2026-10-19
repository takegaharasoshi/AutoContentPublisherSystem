# 2026-10-w3 補充: 機械検証できる問題の答え合わせ
#
# なぞなぞ・とんち・水平思考の「想定解」は機械検証できない(人間レビューが唯一の砦)。
# ここではマッチ棒の本数・文字数え・デジタル数字の棒の本数・五十音の順・情景文の描かない指定など、単純に確かめられるものだけを検証する。
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
# A70 マッチ棒で 9: NINE は N(縦 2 + 斜め 1)・I(縦 1)・N(縦 2 + 斜め 1)・E(縦 1 + 横 3)= 11 本、うち縦 6 本
# ---------------------------------------------------------------
if "A70" in BY_NO:
    sticks = {"N": (2, 1), "I": (1, 0), "E": (1, 3)}  # (縦, 縦以外)
    word = "NINE"
    vertical = sum(sticks[c][0] for c in word)
    other = sum(sticks[c][1] for c in word)
    check("A70", "NINE の縦の棒 = 最初の 6 本", vertical == 6, f"縦 {vertical} 本")
    check("A70", "足す棒 = 5 本", other == 5, f"縦以外 {other} 本(合計 {vertical + other} 本)")
    q = BY_NO["A70"]["question"]
    check("A70", "問題文の数値(6本・5本)", "6本" in q and "5本" in q, "6本・5本")

# ---------------------------------------------------------------
# A71 あした / きのう: 五十音順で「あした」が「きのう」より前
# ---------------------------------------------------------------
if "A71" in BY_NO:
    check("A71", "五十音順で あした < きのう", "あした" < "きのう", f"{sorted(['きのう', 'あした'])}")

# ---------------------------------------------------------------
# A72 F の数: 黒板の英文に F は 6 個(うち OF の F が 3 個)。英文は情景文だけに書く
# ---------------------------------------------------------------
if "A72" in BY_NO:
    lines = ["FINISHED FILES ARE THE", "RESULT OF YEARS OF SCIENTIFIC", "STUDY COMBINED WITH THE EXPERIENCE OF YEARS"]
    text = " ".join(lines)
    total = text.count("F")
    in_of = text.split().count("OF")
    check("A72", "F は 6 個", total == 6, f"F {total} 個(うち OF {in_of} 回)")
    check("A72", "OF の F は 3 個", in_of == 3, f"OF {in_of} 回")
    scene = BY_NO["A72"]["illustration_scene"]
    check("A72", "情景文に英文 3 行を一字一句", all(f"「{ln}」" in scene for ln in lines), " / ".join(lines))
    check("A72", "英文は問題文に書かない", "FINISHED" not in BY_NO["A72"]["question"], "問題文に英文なし")

# ---------------------------------------------------------------
# A74 デジタル数字: 7 セグメントで使う棒の本数(7 は 3 本の字形)
# ---------------------------------------------------------------
if "A74" in BY_NO:
    seg = {"0": 6, "1": 2, "2": 5, "3": 5, "4": 4, "5": 5, "6": 6, "7": 3, "8": 7, "9": 6}
    q = BY_NO["A74"]["question"]
    pairs = [("1", 2), ("7", 3), ("4", 4), ("8", 7)]
    check("A74", "例の 4 式が棒の本数と一致", all(seg[d] == n and f"「{d}={n}」" in q for d, n in pairs), str(pairs))
    check("A74", "0 は 6 本", seg["0"] == 6 and BY_NO["A74"]["answer"].startswith("6"), f"0 → {seg['0']} 本")
    scene = BY_NO["A74"]["illustration_scene"]
    check("A74", "情景文にカードの 5 行", all(f"「{s}」" in scene for s in ["1=2", "7=3", "4=4", "8=7", "0=?"]), "5 行を明示")

# ---------------------------------------------------------------
# C70 春の芝生: 問題文の数(炭 5 個・ニンジン 1 本・マフラー 1 本)
# ---------------------------------------------------------------
if "C70" in BY_NO:
    q = BY_NO["C70"]["question"]
    check("C70", "問題文の数", "炭が5個" in q and "ニンジンが1本" in q and "マフラーが1本" in q, "炭 5・ニンジン 1・マフラー 1")

# ---------------------------------------------------------------
# 情景文に答えの物・答えを連想させる物の名前を書かない(スキル「イラストの情景の方針」10。否定形でも書かない)
# ---------------------------------------------------------------
ANSWER_WORDS = {
    "A69": ["昼ごはん", "晩ごはん"], "A70": ["NINE"], "A71": ["辞書"], "A72": ["6個"],
    "A73": ["寝", "ベッド"], "A74": ["デジタル", "電卓"], "A75": ["鏡", "お札"],
    "C70": ["雪"], "C71": ["点字", "本"], "C72": ["筆", "絵の具"], "C73": ["内側", "室内"],
    "C74": [], "C75": ["サングラス", "めがね"], "C76": ["テント"],
}
for no, words in ANSWER_WORDS.items():
    if no in BY_NO:
        scene = BY_NO[no]["illustration_scene"]
        hit = [w for w in words if w in scene]
        check(no, "情景文に答えの物の名前なし", not hit, f"含まれる語: {hit}" if hit else "なし")

# ---------------------------------------------------------------
# 機械検証の限界: 想定解の自然さ・別解・面白さは人間レビュー。
# ---------------------------------------------------------------
manual = [it["no"] for it in ITEMS if it["no"] in {"A69", "A73", "A75", "C71", "C72", "C73", "C74", "C75", "C76"}]
print(f"-- 機械検証対象外(人間レビューが必要): {', '.join(manual)}")
print("   検証済みの問題も、難度・別解・想定解の自然さ・完成イラストの字形は別途レビュー")

if failures:
    print(f"\nNG: {len(failures)} 件")
    for f in failures:
        print(" -", f)
    sys.exit(1)
print("\nOK: 機械検証できる問題はすべて答えと一致")
