# 2026-08-w5 補充: 機械検証できる問題の答え合わせ
#
# なぞなぞ・とんちの「想定解」は機械検証できない(人間レビューが唯一の砦)。
# ここではブルートフォース・全列挙・単純計算で確かめられるものだけを検証する。
# 今回のバッチに L3(フェルミ推定)は含まれないため、算数の検算セクションはない。
from __future__ import annotations

import sys
from collections import deque

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
# A31 同音異字(しょう)
#   5 語の読みがすべて「〜しょう」で、頭文字が「かきくけこ」を縦断することを確認する。
#   (読みデータ自体は手入力のため、解説の「か行縦断」主張との整合チェック)
# ---------------------------------------------------------------
if "A31" in BY_NO:
    readings = {"花椒": "かしょう", "起床": "きしょう", "苦笑": "くしょう", "化粧": "けしょう", "呼称": "こしょう"}
    ok_suffix = all(r.endswith("しょう") for r in readings.values())
    heads = [r[0] for r in readings.values()]
    ok_heads = heads == list("かきくけこ")
    check("A31", "読みの構造", ok_suffix and ok_heads, f"全語が「〜しょう」/ 頭文字 {''.join(heads)} = か行縦断")

# ---------------------------------------------------------------
# A27 文字の置換(あいうおお vs あいうえお)
#   差分が「え→お」の 1 箇所だけであることを機械確認する。
# ---------------------------------------------------------------
if "A27" in BY_NO:
    shown, correct = "あいうおお", "あいうえお"
    diffs = [(i, c, s) for i, (c, s) in enumerate(zip(correct, shown)) if c != s]
    ok = diffs == [(3, "え", "お")]
    check("A27", "置換位置", ok, f"差分 = {diffs}(「え」が「お」の 1 箇所のみ)")

# ---------------------------------------------------------------
# A32 法則発見(ひらがなを一画消す)
#   4 組すべてが「読みの 1 文字だけが変わる」構造であることを機械確認する。
#   (一画消せるかどうかは字形の話なので機械検証できない。人間レビューが砦)
# ---------------------------------------------------------------
if "A32" in BY_NO:
    pairs = [("かき", "かさ"), ("ほし", "はし"), ("あし", "めし"), ("にし", "こし")]
    diffs = [[i for i, (a, b) in enumerate(zip(x, y)) if a != b] for x, y in pairs]
    ok = all(len(d) == 1 for d in diffs) and all(len(x) == len(y) == 2 for x, y in pairs)
    check("A32", "1 文字だけ変化", ok, f"変化位置 {diffs}(全 4 組とも 2 文字中 1 文字のみ)")

# ※ A22(合体漢字)・A25(字形)・A32(一画消し)・A26(同音読み替え)・A29(穴埋めの一意性)は
#   字形・音・語彙の問題のため機械検証不能。
#   人間レビューが唯一の砦(なぞなぞの「想定解」全般も同様)。

# ---------------------------------------------------------------
# C22 3つのスイッチと白熱電球(一度だけ入室)
#   手順が 3 つのスイッチを一意に識別できることを、観測値の集合で確認する。
#   観測は (点灯しているか, 熱いか) の組。SW1=点けて消した / SW2=点けたまま / SW3=触らない。
# ---------------------------------------------------------------
if "C22" in BY_NO:
    observations = {
        "SW1": (False, True),   # 消えているが熱い
        "SW2": (True, True),    # 点いている
        "SW3": (False, False),  # 消えていて冷たい
    }
    unique = len(set(observations.values())) == 3
    check("C22", "3スイッチの観測値が一意", unique, f"{observations}")

# ---------------------------------------------------------------
# C29 8 個の球から重い 1 個を天秤で特定する最少回数
#   「どの球を左右に何個ずつ載せるか」の戦略を全探索し、最悪ケースで
#   必要な回数の下限が 2 回であること・4 対 4 では 3 回かかることを確認する。
# ---------------------------------------------------------------
if "C29" in BY_NO:
    from functools import lru_cache
    from itertools import combinations

    @lru_cache(maxsize=None)
    def min_weighings(candidates: int) -> int:
        """重い球の候補が candidates 個のとき、最悪ケースで必要な最少計量回数。

        Args:
            candidates: 重い球でありうる球の数。

        Returns:
            必要な計量回数。
        """
        if candidates <= 1:
            return 0
        best = 99
        # 左右に k 個ずつ載せる(残り candidates - 2k 個は乗せない)
        for k in range(1, candidates // 2 + 1):
            rest = candidates - 2 * k
            worst = max(min_weighings(k), min_weighings(rest) if rest else 0)
            best = min(best, 1 + worst)
        return best

    check("C29", "8 個は最少 2 回", min_weighings(8) == 2, f"{min_weighings(8)} 回")
    # 初手 3 対 3 だと残り 2 個 / 重い側 3 個ともあと 1 回で確定する
    first_3v3 = 1 + max(min_weighings(3), min_weighings(2))
    first_4v4 = 1 + max(min_weighings(4), 0)
    check("C29", "初手 3 対 3 なら 2 回", first_3v3 == 2, f"3 対 3 → {first_3v3} 回")
    check("C29", "初手 4 対 4 だと 3 回", first_4v4 == 3, f"4 対 4 → {first_4v4} 回")

# ---------------------------------------------------------------
# C24 燃える速さが不均一なロープ 2 本で 45 分
#   両端点火は全長を半分の時間で燃やす、という条件だけで計算する。
# ---------------------------------------------------------------
if "C24" in BY_NO:
    rope_minutes = 60
    first_both_ends = rope_minutes / 2                 # 1 本目を両端 → 30 分
    second_remaining = rope_minutes - first_both_ends  # 2 本目は片端で 30 分ぶん残る
    second_both_ends = second_remaining / 2            # そこから両端 → 15 分
    total = first_both_ends + second_both_ends
    check("C24", "合計 45 分", total == 45, f"{first_both_ends} + {second_both_ends} = {total} 分")

    # 反例チェック(2026-08-31 レビューで出た別解案): 「両端 + 真ん中」に点火しても 15 分にはならない。
    # 位置の中点で分けた左半分が a 分・右半分が 60 - a 分かかるとすると、
    # 4 つの火で燃え尽きるのは max(a/2, (60-a)/2) 分。15 分になるのは a = 30 のときだけ。
    middle_times = {a: max(a / 2, (60 - a) / 2) for a in range(1, 60)}
    always_15 = all(abs(t - 15) < 1e-9 for t in middle_times.values())
    check(
        "C24",
        "両端+真ん中は 15 分にならない(別解の反証)",
        not always_15,
        f"a=10 なら {middle_times[10]} 分 / a=30 なら {middle_times[30]} 分 / a=50 なら {middle_times[50]} 分",
    )

# ---------------------------------------------------------------
# C28 6 つのグラス(満杯 3・空 3)を 1 つ動かして交互にする
#   「i 番目の中身を j 番目へ注ぐ」全 30 通りを列挙し、交互配列になる手が一意か確認する。
# ---------------------------------------------------------------
if "C28" in BY_NO:
    start = [1, 1, 1, 0, 0, 0]          # 1 = 満杯 / 0 = 空
    target = [1, 0, 1, 0, 1, 0]
    solutions = []
    for src in range(6):
        for dst in range(6):
            if src == dst or start[src] != 1 or start[dst] != 0:
                continue
            state = list(start)
            state[src], state[dst] = 0, 1
            if state == target:
                solutions.append((src + 1, dst + 1))
    check(
        "C28",
        "1 回の注ぎで交互になる手は一意",
        solutions == [(2, 5)],
        f"解 {solutions}(左から2番目 → 5番目)",
    )

# ---------------------------------------------------------------
# C25 オオカミ・ヤギ・キャベツの川渡り
#   状態空間を BFS で全探索し、最短の航行回数と初手を確認する。
#   状態 = (船, オオカミ, ヤギ, キャベツ) の岸。0 = 出発岸 / 1 = 対岸。
# ---------------------------------------------------------------
if "C25" in BY_NO:
    NAMES = ("オオカミ", "ヤギ", "キャベツ")

    def safe(state: tuple[int, int, int, int]) -> bool:
        """人がいない岸で食べられる組み合わせが起きないかを判定する。

        Args:
            state: (船, オオカミ, ヤギ, キャベツ) の位置。

        Returns:
            安全なら True。
        """
        boat, wolf, goat, cabbage = state
        if goat == wolf and goat != boat:
            return False
        if goat == cabbage and goat != boat:
            return False
        return True

    start_state = (0, 0, 0, 0)
    goal_state = (1, 1, 1, 1)
    queue: deque[tuple[tuple[int, int, int, int], list[str]]] = deque([(start_state, [])])
    seen = {start_state}
    shortest: list[str] | None = None
    while queue:
        state, path = queue.popleft()
        if state == goal_state:
            shortest = path
            break
        boat = state[0]
        # 単独で渡る + 同じ岸のものを 1 つ載せて渡る
        for cargo in (None, 0, 1, 2):
            nxt = list(state)
            nxt[0] = 1 - boat
            label = "単独"
            if cargo is not None:
                if state[cargo + 1] != boat:
                    continue
                nxt[cargo + 1] = 1 - boat
                label = NAMES[cargo]
            nxt_t = (nxt[0], nxt[1], nxt[2], nxt[3])
            if not safe(nxt_t) or nxt_t in seen:
                continue
            seen.add(nxt_t)
            queue.append((nxt_t, path + [label]))
    check("C25", "全員を渡せる", shortest is not None, f"最短手順 {shortest}")
    if shortest is not None:
        check("C25", "最短は 7 航行", len(shortest) == 7, f"{len(shortest)} 回")
        check("C25", "初手はヤギ", shortest[0] == "ヤギ", f"初手 {shortest[0]}")
        check(
            "C25",
            "途中でヤギを連れ戻す",
            shortest.count("ヤギ") >= 2,
            f"ヤギを運ぶ回数 {shortest.count('ヤギ')}",
        )

# ---------------------------------------------------------------
# C31 7 分計と 11 分計で 15 分をはかる
#   手順(同時開始 / t=7 で 7 分計を裏返す / t=11 で 7 分計を再度裏返す)を
#   イベントごとにシミュレートし、最後の落下完了がちょうど t=15 になることを確認する。
#   あわせて「素朴な組み合わせでは 15 が作れない」(7+11=18・11-7=4)ことも確認する。
# ---------------------------------------------------------------
if "C31" in BY_NO:
    t = 0
    # 7 分計: t=0 開始 → t=7 で落ち切り、即裏返す
    t7_flip1 = 7
    # 11 分計: t=0 開始 → t=11 で落ち切る
    t11_done = 11
    # t=11 時点、7 分計は 2 回目の計測を 4 分消化(残り 3 分)。裏返すと落ちた 4 分ぶんが戻る
    elapsed_in_7 = t11_done - t7_flip1
    final = t11_done + elapsed_in_7
    check("C31", "手順の完了時刻が 15 分", final == 15, f"11 + {elapsed_in_7} = {final} 分")
    check(
        "C31",
        "単純な和・差では 15 分にならない(ワナの確認)",
        7 + 11 != 15 and 11 - 7 != 15,
        f"7+11={7 + 11} / 11-7={11 - 7}",
    )

# ---------------------------------------------------------------
# C34 10 袋の金貨(1 袋だけ全部 1g 重い偽物)をはかり 1 回で特定
#   偽物の袋が 1〜10 番のどれであっても、袋 n から n 枚取る手順の合計重量が
#   すべて相異なり、超過グラム数 = 袋番号になることを全ケース確認する。
# ---------------------------------------------------------------
if "C34" in BY_NO:
    GENUINE = 10  # g
    FAKE = 11     # g
    BASE = GENUINE * sum(range(1, 11))  # 全部本物なら 550g
    weights = {}
    for fake_bag in range(1, 11):
        total = sum(n * (FAKE if n == fake_bag else GENUINE) for n in range(1, 11))
        weights[fake_bag] = total
    all_unique = len(set(weights.values())) == 10
    excess_matches = all(weights[b] - BASE == b for b in weights)
    check("C34", "10 ケースの合計重量が相異なる", all_unique,
          f"{sorted(weights.values())}")
    check("C34", "超過グラム数 = 袋番号", excess_matches,
          f"例: 3 番が偽物 → {weights[3]}g(550 + 3)")

# ---------------------------------------------------------------
# 朝(A22〜A28)の文字あそび検証はリサーチ確定後にここへ追加する
# ---------------------------------------------------------------

print()
if failures:
    print(f"NG: {len(failures)} 件")
    for f in failures:
        print(" -", f)
    sys.exit(1)
print("すべての機械検証を通過")
