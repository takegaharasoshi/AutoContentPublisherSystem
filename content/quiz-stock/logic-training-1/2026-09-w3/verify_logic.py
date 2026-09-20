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
    check("A40", "=を≠に(別解)", (5 + 5 + 5) != 550, "5+5+5≠550 は真")
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
# A42 止まった時計 vs 1 日 1 分遅れる時計: 正しい時刻を示す回数の比較
#      止まった時計 = 1 日 2 回。遅れる時計 = 遅れの累計が 12 時間(720 分)の倍数になった瞬間だけ → 720 日に 1 回
# ---------------------------------------------------------------
if "A42" in BY_NO:
    lag = 0
    days = 0
    while True:
        days += 1
        lag += 1  # 1 日 1 分
        if lag % 720 == 0:
            break
    stopped_per_720d = 2 * days
    check("A42", "遅れる時計が再び合う周期", days == 720, f"{days} 日に 1 回")
    check("A42", "同じ期間の止まった時計", stopped_per_720d > 1, f"720 日で {stopped_per_720d} 回 vs 遅れる時計 1 回")
    check("A42", "explanation に 720 日", "720日" in BY_NO["A42"]["explanation"], "解説の数値と一致")

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
# A44 漢数字一〜十の画数: 常用漢字表の画数で最多が「四」のみであること
# ---------------------------------------------------------------
if "A44" in BY_NO:
    strokes = {"一": 1, "二": 2, "三": 3, "四": 5, "五": 4, "六": 4, "七": 2, "八": 2, "九": 2, "十": 2}
    mx = max(strokes.values())
    top = [k for k, v in strokes.items() if v == mx]
    check("A44", "最多画数は四のみ", top == ["四"] and mx == 5, f"{strokes} → 最多 {top}({mx} 画)")
    expl = BY_NO["A44"]["explanation"]
    check("A44", "解説の画数一覧が一致", all(f"{k}{v}画" in expl for k, v in strokes.items()), "一1画〜十2画をすべて記載")

# ---------------------------------------------------------------
# A45 本棚の虫: 洋書(左開き)を背表紙を手前に順に並べると、各巻の 1 ページ目は右端・最後のページは左端。
#      巻 i の区間を [3(i-1), 3i] cm とし、1 巻の 1 ページ目(x=3)から 10 巻の最後(x=27)までの距離
# ---------------------------------------------------------------
if "A45" in BY_NO:
    t = 3
    first_page_vol1 = 1 * t  # 右端
    last_page_vol10 = 9 * t  # 10 巻の左端
    dist = last_page_vol10 - first_page_vol1
    check("A45", "食べた長さ", dist == 24, f"{last_page_vol10} - {first_page_vol1} = {dist} cm(早合点の 10 冊分は {10 * t} cm)")
    check("A45", "answer に 24cm", "24cm" in BY_NO["A45"]["answer"], BY_NO["A45"]["answer"])

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
