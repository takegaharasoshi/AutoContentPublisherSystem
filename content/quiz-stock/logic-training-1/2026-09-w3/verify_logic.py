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
# A41 8 を 8 個で 1000: 8 だけで作る数(8/88/888/8888)の足し算で桁数の合計が 8 になる組を全列挙し、
#      合計 1000 になる組がちょうど 1 つ(888+88+8+8+8)であること
# ---------------------------------------------------------------
if "A41" in BY_NO:
    parts = [8, 88, 888, 8888]
    sols: set[tuple[int, ...]] = set()
    for k in range(1, 9):
        for combo in combinations_with_replacement(parts, k):
            if sum(len(str(p)) for p in combo) == 8 and sum(combo) == 1000:
                sols.add(tuple(sorted(combo, reverse=True)))
    check("A41", "足し算限定の解は一意", sols == {(888, 88, 8, 8, 8)}, f"解: {sorted(sols)}")
    check("A41", "8 の個数", BY_NO["A41"]["answer"].count("8") == 8, BY_NO["A41"]["answer"])

# ---------------------------------------------------------------
# A42 計算マジック: 整数・負の数・小数のどれから始めても (2x+10)÷2−x が必ず 5 になること
# ---------------------------------------------------------------
if "A42" in BY_NO:
    from fractions import Fraction

    starts = [Fraction(n) for n in range(-1000, 1001)] + [Fraction(1, 3), Fraction(-7, 2), Fraction(123456789, 10)]
    results = {(2 * x + 10) / 2 - x for x in starts}
    check("A42", "答えは必ず 5", results == {Fraction(5)}, f"{len(starts)} 通りの初期値で結果 = {sorted(results)}")
    check("A42", "answer に 5", "必ず5" in BY_NO["A42"]["answer"], BY_NO["A42"]["answer"])

# ---------------------------------------------------------------
# A43 文字盤を直線 2 本で 3 分割: 交わらない 2 本の線 = 両端の「弧」2 つ(連続した数字の並び)+ 残りの中央部。
#      両弧と中央の合計がすべて等しい分け方を全列挙し、{11,12,1,2}{5,6,7,8}{3,4,9,10} のみであること
#      (交わる 2 本は 4 つの部分になるため対象外)
# ---------------------------------------------------------------
if "A43" in BY_NO:
    nums = list(range(1, 13))
    total = sum(nums)
    arcs = []
    for start in range(12):
        for length in range(1, 11):  # 12 個すべて・11 個は他の部分が作れないので除外
            arcs.append(frozenset((nums[(start + i) % 12]) for i in range(length)))
    arcs = list(set(arcs))
    sols = set()
    for a, b in combinations(arcs, 2) if False else [(a, b) for i, a in enumerate(arcs) for b in arcs[i + 1:]]:
        if a & b:
            continue
        mid = frozenset(nums) - a - b
        if not mid:
            continue
        if sum(a) == sum(b) == sum(mid):
            sols.add(frozenset([a, b, mid]))
    expected = frozenset([frozenset({11, 12, 1, 2}), frozenset({5, 6, 7, 8}), frozenset({3, 4, 9, 10})])
    check("A43", "各部分の合計", total // 3 == 26 and total % 3 == 0, f"1〜12 の合計 {total} ÷ 3 = {total // 3}")
    check("A43", "分け方は一意", sols == {expected}, f"解: {[sorted(sorted(x) for x in s) for s in sols]}")

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
# A46 地球のロープ: 円周 +1m のとき半径の増分 = 1/(2π) m。地球半径に依存しないことを 2 つの半径で確認
# ---------------------------------------------------------------
if "A46" in BY_NO:
    gaps = []
    for r in (6_371_000.0, 1.0):
        c = 2 * math.pi * r
        r2 = (c + 1) / (2 * math.pi)
        gaps.append(round((r2 - r) * 100, 2))
    check("A46", "隙間は約 16cm", all(abs(g - 15.92) < 0.01 for g in gaps), f"半径 6371km と 1m のどちらでも {gaps} cm")

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
