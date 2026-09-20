# 2026-09-w3 補充: 機械検証できる問題の答え合わせ
#
# なぞなぞ・とんち・水平思考の「想定解」は機械検証できない(人間レビューが唯一の砦)。
# ここではブルートフォース・全列挙・単純計算で確かめられるものだけを検証する。
# 今回のバッチに L3(フェルミ推定)は含まれないため、算数の検算セクションはない。
from __future__ import annotations

import math
import random
import sys
from itertools import combinations_with_replacement

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
# A40 5+5+5=550: 元の式が不成立で、「+」→「4」の置換後の式が成立すること(左右どちらの + でも)
# ---------------------------------------------------------------
if "A40" in BY_NO:
    check("A40", "元の式は不成立", (5 + 5 + 5) != 550, "5+5+5=15≠550")
    check("A40", "左の+を4に", 545 + 5 == 550, "545+5=550")
    check("A40", "右の+を4に(別解)", 5 + 545 == 550, "5+545=550")
    check("A40", "式は問題文に書かない(黒板で提示)", "5+5+5" not in BY_NO["A40"]["question"] and "5+5+5=550" in BY_NO["A40"]["illustration_scene"], "問題文に式なし・情景文に式あり")
    check("A40", "answer に 545+5=550", "545+5=550" in BY_NO["A40"]["answer"], BY_NO["A40"]["answer"])

# ---------------------------------------------------------------
# A41 位置抽出の暗号: 2 文字目を拾うと「けんか」になり、他の位置では語にならないこと
# ---------------------------------------------------------------
if "A41" in BY_NO:
    words = ["たけやぶ", "ほんだな", "さかみち"]
    picks = {i + 1: "".join(w[i] for w in words) for i in range(4)}
    check("A41", "2 文字目で けんか", picks[2] == "けんか", f"位置ごとの縦読み: {picks}")
    others = {k: v for k, v in picks.items() if k != 2}
    check("A41", "他の位置は語にならない", set(others.values()) == {"たほさ", "やだみ", "ぶなち"},
          f"1/3/4 文字目 = {sorted(others.values())}(いずれも意味のある語ではない)")
    check("A41", "answer は けんか", BY_NO["A41"]["answer"].startswith("けんか"), BY_NO["A41"]["answer"])
    check("A41", "3 語は問題文に書かない(黒板で提示)",
          "たけやぶ" not in BY_NO["A41"]["question"] and "たけやぶ" in BY_NO["A41"]["illustration_scene"],
          "問題文に語なし・情景文に 3 語あり")

# ---------------------------------------------------------------
# A43 合体漢字: 4 部品が 2 つずつで「時」「計」を構成し、熟語「時計」になること
# ---------------------------------------------------------------
if "A43" in BY_NO:
    parts = ["日", "寺", "言", "十"]
    compose = {("日", "寺"): "時", ("言", "十"): "計"}
    made = [compose[k] for k in compose]
    used = sorted(p for k in compose for p in k)
    check("A43", "部品をすべて使う", used == sorted(parts), f"{used} = 提示の 4 部品")
    check("A43", "2 つずつで時・計", made == ["時", "計"], f"{list(compose.items())}")
    check("A43", "熟語は時計", "".join(made) == "時計" and BY_NO["A43"]["answer"].startswith("時計"), BY_NO["A43"]["answer"])
    check("A43", "4 部品は問題文に書かない(黒板で提示)",
          "寺" not in BY_NO["A43"]["question"] and "「寺」" in BY_NO["A43"]["illustration_scene"],
          "問題文に部品なし・情景文に 4 字あり")

# ---------------------------------------------------------------
# A46 隠れ数字の数列: 各語の語頭に 3・4・5 が隠れ、1 ずつ増えていること(次は 6)
# ---------------------------------------------------------------
if "A46" in BY_NO:
    hidden = [("さんま", "さん", 3), ("しいたけ", "しい", 4), ("ごぼう", "ご", 5)]
    for word, head, num in hidden:
        check("A46", f"{word} の語頭に {num}", word.startswith(head), f"{word} → {head}({num})")
    nums = [n for _, _, n in hidden]
    check("A46", "1 ずつ増える", nums == list(range(nums[0], nums[0] + len(nums))), f"{nums} → 次は {nums[-1] + 1}")
    check("A46", "answer は 6", "6" in BY_NO["A46"]["answer"], BY_NO["A46"]["answer"])

# ---------------------------------------------------------------
# A44 指の頭文字: 親指〜小指の読みの頭文字が「お ひ な く こ」になり、□(3 番目)が「な」であること
# ---------------------------------------------------------------
if "A44" in BY_NO:
    fingers = ["おやゆび", "ひとさしゆび", "なかゆび", "くすりゆび", "こゆび"]
    initials = "".join(f[0] for f in fingers)
    check("A44", "頭文字の並び", initials == "おひなくこ", f"{fingers} → {initials}")
    check("A44", "□ は 3 番目 = な", initials[2] == "な" and BY_NO["A44"]["answer"].startswith("な"), BY_NO["A44"]["answer"])
    check("A44", "情景文のカード 5 枚", all(f"「{c}」" in BY_NO["A44"]["illustration_scene"] for c in "おひ?くこ"), "お・ひ・?・く・こ を明示")
    check("A44", "5 文字は問題文に書かない(カードで提示)", "お、ひ" not in BY_NO["A44"]["question"] and "□" not in BY_NO["A44"]["question"], "問題文に文字列なし・情景文にカードあり")

# ---------------------------------------------------------------
# A45 母音送り: 提示 3 組 + 答えのすべてが「読みの各文字の母音を 1 段送った語」であること、
#      および単純な変換(逆順・循環並べ替え・濁点)では説明できないことを確認
# ---------------------------------------------------------------
if "A45" in BY_NO:
    ROWS = ["あいうえお", "かきくけこ", "さしすせそ", "たちつてと", "なにぬねの",
            "はひふへほ", "まみむめも", "らりるれろ"]
    POS = {ch: (r, i) for r, row in enumerate(ROWS) for i, ch in enumerate(row)}

    def shift_vowel(reading: str) -> str:
        """各文字の母音を 1 段送る(あ→い→う→え→お→あ)。"""
        out = []
        for ch in reading:
            r, i = POS[ch]
            out.append(ROWS[r][(i + 1) % 5])
        return "".join(out)

    pairs = [("かき", "きく", "柿→菊"), ("あめ", "いも", "雨→芋"), ("かに", "きぬ", "蟹→絹"), ("うま", "えみ", "馬→笑み")]
    for src, dst, label in pairs:
        check("A45", f"母音送りで対応 {label}", shift_vowel(src) == dst, f"{src} → {shift_vowel(src)}")
    # 他の単純変換では説明できないこと(逆順・循環並べ替え)
    other = [(src, dst) for src, dst, _ in pairs if src[::-1] == dst or src[1:] + src[0] == dst]
    check("A45", "逆順・循環では説明できない", not other, f"逆順/循環で一致する組: {other}")
    check("A45", "answer は えみ", BY_NO["A45"]["answer"].startswith("えみ"), BY_NO["A45"]["answer"])
    check("A45", "3 組は問題文に書かない(黒板で提示)",
          "柿" not in BY_NO["A45"]["question"] and "柿 → 菊" in BY_NO["A45"]["illustration_scene"],
          "問題文に組なし・情景文に 4 行あり")

# ---------------------------------------------------------------
# C48 ケーキを 3 回で 8 等分: 中心を通る直交 2 平面 + 高さ半分の水平面で 8 片の体積が等しいこと(モンテカルロ)
# ---------------------------------------------------------------
if "C48" in BY_NO:
    rng = random.Random(0)
    counts = [0] * 8
    n = 200_000
    for _ in range(n):
        x, y = rng.uniform(-1, 1), rng.uniform(-1, 1)
        if x * x + y * y > 1:
            continue
        z = rng.uniform(0, 1)
        idx = (x > 0) + 2 * (y > 0) + 4 * (z > 0.5)
        counts[idx] += 1
    mean = sum(counts) / 8
    spread = max(abs(c - mean) / mean for c in counts)
    check("C48", "8 片の体積が等しい", spread < 0.03, f"各片の比率のばらつき {spread:.3%}(サンプル {sum(counts)})")

# ---------------------------------------------------------------
# 機械検証できない問題(想定解の妥当性は人間レビューが砦)
# ---------------------------------------------------------------
manual = [no for no in ("C42", "C43", "C44", "C45", "C46", "C47") if no in BY_NO]
print(f"-- 機械検証対象外(人間レビューが砦): {', '.join(manual)}")
print("   C45 は「同じ喫水線 = 同じ排水量 = 同じ重さ」(アルキメデスの原理)で成立。C42/C43/C44/C46/C47 は手順・一言の妥当性を人間が判断")

if failures:
    print(f"\nNG: {len(failures)} 件")
    for f in failures:
        print(" -", f)
    sys.exit(1)
print("\nOK: 機械検証できる問題はすべて答えと一致")
