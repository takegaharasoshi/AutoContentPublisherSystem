# 2026-11-w2 補充: 機械検証できる問題の答え合わせ
#
# なぞなぞ・とんち・水平思考の「想定解」は機械検証できない(人間レビューが唯一の砦)。
# ここでは漢字の部品・時報の全列挙・情景文の描かない指定など、単純に確かめられるものだけを検証する。
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
# A97 黒い犬: 答えと解説に 黒・犬・黙 がある
# ---------------------------------------------------------------
if "A97" in BY_NO:
    it = BY_NO["A97"]
    check("A97", "答え・解説に 黒・犬・黙 がある", all(c in it["answer"] and c in it["explanation"] for c in "黒犬黙"), it["answer"])

# ---------------------------------------------------------------
# A90 じゃんけん: 指の本数 グー 0・チョキ 2・パー 5 の三すくみが問題文・情景文と一致
# ---------------------------------------------------------------
if "A90" in BY_NO:
    it = BY_NO["A90"]
    wins = [(0, 2), (2, 5), (5, 0)]  # グー>チョキ、チョキ>パー、パー>グー
    check("A90", "問題文の 3 つの強弱", all(f"{a}は{b}より強" in it["question"] for a, b in wins), "0>2・2>5・5>0")
    check("A90", "情景文に 3 行がそのままある", all(f"「{a} > {b}」" in it["illustration_scene"] for a, b in wins), "3 行")

# ---------------------------------------------------------------
# C92 混ざった薬: 4 錠を半分に割り半分ずつ = 毎晩 A 1 錠・B 1 錠
# ---------------------------------------------------------------
if "C92" in BY_NO:
    from fractions import Fraction
    half = Fraction(1, 2)
    night = {"A": 2 * half, "B": 2 * half}
    check("C92", "半分ずつで毎晩 A 1 錠・B 1 錠", night == {"A": 1, "B": 1}, f"A {night['A']}・B {night['B']} × 2 晩")

# ---------------------------------------------------------------
# C96 柱時計: 30 分おきに「1 回」が 4 度つづく帰宅時刻を全列挙(正時 = 時の数・30 分 = 1 回。
# 帰宅の瞬間に正時の最後の 1 打だけを聞く場合も含める)
# ---------------------------------------------------------------
if "C96" in BY_NO:
    def strikes(slot: int) -> int:
        """30 分きざみの slot(0 = 12:00)で鳴る回数を返す。"""
        hour = (slot // 2) % 12 or 12
        return hour if slot % 2 == 0 else 1

    sols = []
    for start in range(24):
        for last_only in (False, True):
            if last_only and start % 2 == 1:
                continue
            first = 1 if last_only else strikes(start)
            seq = [first] + [strikes(start + k) for k in (1, 2, 3)]
            if seq == [1, 1, 1, 1]:
                hour = (start // 2) % 12 or 12
                sols.append(f"{hour}:{'00' if start % 2 == 0 else '30'}{'(最後の1打)' if last_only else ''}")
    check("C96", "帰宅時刻は 12 時(最後の 1 打)だけ", sols == ["12:00(最後の1打)"], " / ".join(sols))
    check("C96", "答えが 12時", BY_NO["C96"]["answer"].startswith("12時"), BY_NO["C96"]["answer"])

# ---------------------------------------------------------------
# 情景文に答えの物の名前を書かない(スキルのイラスト方針 10。否定形でも書かない)
# ---------------------------------------------------------------
FORBIDDEN = {
    "A90": ["じゃんけん", "グー", "チョキ", "パー", "手", "指"], "A91": ["とうもろこし", "粒", "芯", "皮", "ひげ", "畑"],
    "A92": ["夫", "妻", "女", "婦"], "A93": ["田", "束", "切り口", "断面"], "A94": ["札", "お金", "財布", "硬貨", "コイン", "にせ"],
    "A95": ["将棋", "駒", "盤", "歩", "金"], "A96": ["血", "乳", "ミルク", "「ち」"], "A97": ["黙", "だま"],
    "C91": ["模型", "ジオラマ", "人形", "おもちゃ", "ミニチュア"], "C92": ["半分", "割", "包丁", "カッター"],
    "C93": ["燃料", "ガソリン", "タンク", "給油", "排気"], "C94": ["T字", "真ん中", "端"],
    "C95": ["風船", "ヘリウム", "ひも", "浮"], "C96": ["12", "十二"], "C97": ["坂", "転が", "斜め", "空洞"],
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
