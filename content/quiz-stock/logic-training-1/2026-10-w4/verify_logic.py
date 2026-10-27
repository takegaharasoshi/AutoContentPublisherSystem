# 2026-10-w4 補充: 機械検証できる問題の答え合わせ
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
# A77 I+XI=X: 180 度回すと X=IX+I。回す前は誤り・回した後は正しい
# ---------------------------------------------------------------
ROMAN = {"I": 1, "V": 5, "X": 10}


def roman(s: str) -> int:
    """ローマ数字(I・V・X のみ)を整数にする。

    Args:
        s: ローマ数字の文字列。

    Returns:
        整数値。
    """
    total = 0
    for i, c in enumerate(s):
        v = ROMAN[c]
        total += -v if i + 1 < len(s) and ROMAN[s[i + 1]] > v else v
    return total


def holds(expr: str) -> bool:
    """「a+b=c」「a=b+c」形式の式が成り立つかを返す。"""
    left, right = expr.split("=")
    val = lambda side: sum(roman(t) for t in side.split("+"))  # noqa: E731
    return val(left) == val(right)


if "A77" in BY_NO:
    before = "I+XI=X"
    after = before[::-1]  # I・X・+・= は 180 度回しても同じ形なので、回転 = 並びの反転
    check("A77", "回す前は誤り(1+11≠10)", not holds(before), before)
    check("A77", "回すと X=IX+I で正しい(10=9+1)", after == "X=IX+I" and holds(after), after)
    # 式はイラストで見せる(問題文には書かない。2026-10-27 のレビューで変更)
    check("A77", "情景文に式・問題文に式なし", f"「{before}」" in BY_NO["A77"]["illustration_scene"] and before not in BY_NO["A77"]["question"], before)

# ---------------------------------------------------------------
# A78 口に二画・A82 大に一画: 挙げた字の画数 = 元の字 + 足す画数(口 3 画・大 3 画)
# ---------------------------------------------------------------
STROKES = {"田": 5, "目": 5, "由": 5, "甲": 5, "申": 5, "旧": 5, "古": 5, "右": 5, "石": 5, "兄": 5,
           "只": 5, "史": 5, "台": 5, "叶": 5, "四": 5, "加": 5, "可": 5, "句": 5, "犬": 4, "太": 4, "天": 4, "夫": 4}
if "A78" in BY_NO:
    listed = "田目由甲申四旧古右石兄只史台叶加可句"
    check("A78", "挙げた字はすべて 5 画(口 3 + 2)", all(STROKES[c] == 5 for c in listed), f"{len(listed)} 字")
    check("A78", "答え・解説の字が一覧に含まれる", all(c in listed for c in "田目由甲申旧古右石兄"), "答えの 10 字")
    shown = [c for c in listed if c in BY_NO["A78"]["explanation"]]
    check("A78", "解説に名人の 15 字以上を挙げる", len(shown) >= 15 and "15個" in BY_NO["A78"]["question"], f"{len(shown)} 字")
if "A82" in BY_NO:
    listed = "犬太天夫"
    check("A82", "挙げた字はすべて 4 画(大 3 + 1)", all(STROKES[c] == 4 for c in listed), listed)

# ---------------------------------------------------------------
# A79 teapot: T で始まり T で終わる
# ---------------------------------------------------------------
if "A79" in BY_NO:
    w = "teapot"
    check("A79", "teapot は t で始まり t で終わる", w[0] == "t" and w[-1] == "t" and w[:3] == "tea", w)

# ---------------------------------------------------------------
# A80 片手で 31: 1+2+4+8+16 = 31・両手 10 本で 1023
# ---------------------------------------------------------------
if "A80" in BY_NO:
    one = sum(2 ** i for i in range(5))
    both = 2 ** 10 - 1
    ex = BY_NO["A80"]["explanation"]
    check("A80", "片手 5 本の最大 = 31", one == 31 and "31" in ex, f"{one}")
    check("A80", "両手 10 本の最大 = 1023", both == 1023 and "1023" in ex, f"{both}")
    check("A80", "解説の割り当て 1・2・4・8・16", all(f"{n}" in ex for n in (1, 2, 4, 8, 16)), "1・2・4・8・16")

# ---------------------------------------------------------------
# A81 マッチ棒 7 本で十本: 十 = 2 画・本 = 5 画で 7 本
# ---------------------------------------------------------------
if "A81" in BY_NO:
    check("A81", "十(2)+本(5)= 7 本", 2 + 5 == 7 and "7本" in BY_NO["A81"]["question"], "2 + 5 = 7")

# ---------------------------------------------------------------
# 情景文に答えの物の名前を書かない(スキルのイラスト方針 10。否定形でも書かない)
# ---------------------------------------------------------------
FORBIDDEN = {
    "A76": ["台風"], "A79": ["ポット", "紅茶", "お茶", "カップ", "砂糖"], "A81": ["十本"],
    "C77": ["橋"], "C78": ["砂糖", "スプーン"], "C79": ["フェリー", "船", "港", "海"], "C80": ["ゆで", "鍋", "皿"],
    "C81": ["洗車"], "C82": ["歩く", "通路"], "C83": ["トライアスロン", "泳", "プール", "自転車"],
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
