# 2026-09-w1 補充: 機械検証できる問題の答え合わせ
#
# なぞなぞ・とんちの「想定解」は機械検証できない(人間レビューが唯一の砦)。
# ここではブルートフォース・全列挙・単純計算で確かめられるものだけを検証する。
# 今回のバッチに L3(フェルミ推定)は含まれないため、算数の検算セクションはない。
from __future__ import annotations

import sys
from collections import deque
from itertools import combinations

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
# A34 見て言う数列: 問題文の 5 項から法則で生成した 6 項目が answer と一致すること
# ---------------------------------------------------------------
if "A34" in BY_NO:
    def look_and_say(t: str) -> str:
        out, i = [], 0
        while i < len(t):
            j = i
            while j < len(t) and t[j] == t[i]:
                j += 1
            out.append(f"{j - i}{t[i]}")
            i = j
        return "".join(out)

    seq = ["1"]
    for _ in range(5):
        seq.append(look_and_say(seq[-1]))
    given = ["1", "11", "21", "1211", "111221"]
    check("A34", "問題文の 5 項が法則どおり", seq[:5] == given and all(g in BY_NO["A34"]["question"] for g in given), " → ".join(seq[:5]))
    check("A34", "次項 = answer", BY_NO["A34"]["answer"].startswith(seq[5]), f"{seq[4]} → {seq[5]}")

# ---------------------------------------------------------------
# A35 「日」に一画: answer の 8 字が重複なく 8 個であること
# ---------------------------------------------------------------
if "A35" in BY_NO:
    ans = BY_NO["A35"]["answer"]
    chars = ans.split("(")[0].split("・")
    check("A35", "定番 8 字が重複なし", len(chars) == 8 and len(set(chars)) == 8, "・".join(chars))
    check("A35", "解説に 8 字すべてが登場", all(c in BY_NO["A35"]["explanation"] for c in chars), "explanation に全字あり")

# ---------------------------------------------------------------
# A37 あるなし: 「ある」側 + 「ら」が answer/explanation の語と一致し、「ない」側 + 「ら」が
#   一般的な語にならないことを簡易辞書で確認(辞書は手入力。人間レビューの補助)
# ---------------------------------------------------------------
if "A37" in BY_NO:
    aru = ["くじ", "さく", "まく", "はし"]
    nai = ["かべ", "ふた", "みち", "いす"]
    words = {"くじら", "さくら", "まくら", "はしら", "かけら", "とびら", "そら", "あぶら", "かめら"}
    # 8 語は問題文ではなくイラスト(あるなしの表)で見せるため、情景文に字形指定があることを確認する
    scene = BY_NO["A37"]["illustration_scene"]
    check("A37", "情景に ある/ない の 8 語", all(f"「{w}」" in scene for w in aru + nai), " ".join(aru + nai))
    check("A37", "情景に ある/ない の見出し", "「ある」" in scene and "「ない」" in scene, "見出し 2 語")
    check("A37", "ある側 + ら が語になる", all(w + "ら" in words for w in aru), ", ".join(w + "ら" for w in aru))
    check("A37", "ない側 + ら が語にならない", all(w + "ら" not in words for w in nai), ", ".join(w + "ら" for w in nai))
    check("A37", "解説に 4 語の変換を明記", all(f"{w}→{w}ら" in BY_NO["A37"]["explanation"] for w in aru), "explanation に 4 組")

# ---------------------------------------------------------------
# A38 時計の針: 0 時ちょうどから 24 時間で長針と短針が重なる回数を、
#   角速度から解析的に数え、1 分刻みの走査でも同じ回数になることを確認する
# ---------------------------------------------------------------
if "A38" in BY_NO:
    # 長針 6 度/分、短針 0.5 度/分 → 相対 5.5 度/分。360 度差をつけるのに 720/11 分
    interval = 720 / 11
    n = int(1440 // interval) + 1  # t=0(0 時)を含み、t=1440(翌 0 時)は含めない
    overlaps = [k * interval for k in range(n) if k * interval < 1440]
    # 走査による裏取り: 角度差の符号が変わる(= 追い越す)瞬間を数える
    def diff(t: float) -> float:
        d = (6 * t - 0.5 * t) % 360
        return d - 360 if d > 180 else d

    crossings = sum(1 for m in range(1440) if diff(m) <= 0 < diff(m + 1) or diff(m) == 0)
    check("A38", "24 時間で重なる回数", len(overlaps) == 22, f"{len(overlaps)} 回(間隔 {interval:.4f} 分 = 約 65 分 27 秒)")
    check("A38", "走査でも同じ回数", crossings == 22, f"1 分刻みの走査で {crossings} 回")
    # 解説の柱: 「11 時台には一度も重ならず、次は 12 時ちょうど」(2026-09-07 ユーザー指示で説明方針を変更)
    in_11 = [t for t in overlaps if 660 <= t < 720]
    check("A38", "11 時台に重なりがない", not in_11, "660〜719 分に重なりなし")
    check("A38", "次の重なりは 12 時ちょうど", any(abs(t - 720) < 1e-9 for t in overlaps), "t=720 分 = 12 時 00 分")
    check("A38", "12 時間で 11 回", sum(1 for t in overlaps if t < 720) == 11, "0〜11 時台で 11 回")
    check("A38", "解説が 11 時台と 12 時ちょうどに触れる", "11時台" in BY_NO["A38"]["explanation"] and "12時ちょうど" in BY_NO["A38"]["explanation"], "explanation に両方")

# ---------------------------------------------------------------
# A39 たちつみと: 「たちつてと」との差分が 1 箇所(4 文字目)で て→み であること
# ---------------------------------------------------------------
if "A39" in BY_NO:
    given, base = "たちつみと", "たちつてと"
    diffs = [(i, base[i], given[i]) for i in range(5) if base[i] != given[i]]
    check("A39", "差分が 1 箇所で て→み", diffs == [(3, "て", "み")], f"{diffs}")
    check("A39", "問題文に「たちつみと」", given in BY_NO["A39"]["question"], given)

# ---------------------------------------------------------------
# C35 3L / 5L で 4L: BFS で到達可能性と最短手数を確認し、answer の手順をシミュレートする
# ---------------------------------------------------------------
if "C35" in BY_NO:
    A, B = 3, 5  # (3L, 5L)

    def neighbors(s: tuple[int, int]) -> list[tuple[int, int]]:
        a, b = s
        res = [(A, b), (a, B), (0, b), (a, 0)]
        t = min(a, B - b); res.append((a - t, b + t))  # 3L → 5L
        t = min(b, A - a); res.append((a + t, b - t))  # 5L → 3L
        return res

    start = (0, 0)
    dist = {start: 0}
    dq = deque([start])
    while dq:
        s = dq.popleft()
        for n in neighbors(s):
            if n not in dist:
                dist[n] = dist[s] + 1
                dq.append(n)
    reach = [s for s in dist if 4 in s]
    best = min(dist[s] for s in reach) if reach else None
    check("C35", "4L が到達可能", bool(reach), f"到達状態 {reach}(最短 {best} 手)")
    # answer の手順: 5L 満杯 → 5L→3L → 3L 空ける → 5L→3L → 5L 満杯 → 5L→3L
    s = (0, 0)
    steps = ["fillB", "BtoA", "emptyA", "BtoA", "fillB", "BtoA"]
    for st in steps:
        a, b = s
        if st == "fillB": s = (a, B)
        elif st == "emptyA": s = (0, b)
        elif st == "BtoA":
            t = min(b, A - a); s = (a + t, b - t)
    check("C35", "answer の手順で 5L 側に 4L", s[1] == 4, f"{steps} → {s}(手数 {len(steps)} = 最短 {best})")

# ---------------------------------------------------------------
# C36 硬貨 20 枚(表 10): 取り分けた 10 枚に含まれる表の枚数 n = 0..10 の全ケースで、
#   裏返し後の表の枚数が残りの表の枚数と一致すること
# ---------------------------------------------------------------
if "C36" in BY_NO:
    TOTAL, HEADS, TAKE = 20, 10, 10
    ok_all = True
    detail = []
    for n in range(0, min(HEADS, TAKE) + 1):  # 取り分けた 10 枚の中の表の枚数
        rest_heads = HEADS - n
        flipped_heads = TAKE - n
        ok_all &= flipped_heads == rest_heads
        detail.append(f"n={n}:{flipped_heads}/{rest_heads}")
    check("C36", "n=0..10 の全ケースで一致", ok_all, " ".join(detail))

# ---------------------------------------------------------------
# C37 南京錠: 手順の各時点で箱に錠が 1 個以上かかっていること(状態機械)
# ---------------------------------------------------------------
if "C37" in BY_NO:
    locks: set[str] = set()
    transit_ok = True
    log = []
    locks.add("mine"); log.append(f"送る:{sorted(locks)}"); transit_ok &= bool(locks)
    locks.add("theirs"); log.append(f"返送:{sorted(locks)}"); transit_ok &= bool(locks)
    locks.discard("mine"); log.append(f"再送:{sorted(locks)}"); transit_ok &= bool(locks)
    locks.discard("theirs"); opened = not locks
    check("C37", "輸送中は常に錠あり・最後に相手が開錠", transit_ok and opened, " → ".join(log) + " → 開く")

# ---------------------------------------------------------------
# C38 井戸のカタツムリ: 日ごとのシミュレーション
# ---------------------------------------------------------------
if "C38" in BY_NO:
    depth, up, down = 10, 3, 2
    pos, day = 0, 0
    while True:
        day += 1
        pos += up
        if pos >= depth:
            break
        pos -= down
    check("C38", "脱出は 8 日目", day == 8, f"7 日目終了時 {7 * (up - down)}m → 8 日目の昼 {7 * (up - down) + up}m ≥ {depth}m")

# ---------------------------------------------------------------
# C39 棒 6 本で正三角形 4 つ: 正四面体の辺 6・面 4 を確認(組合せ論的に)。
#   平面で棒 6 本の正三角形が最大 2 つであることは既知の事実として人間レビューに委ねる
# ---------------------------------------------------------------
if "C39" in BY_NO:
    vertices = 4
    edges = len(list(combinations(range(vertices), 2)))
    faces = len(list(combinations(range(vertices), 3)))
    check("C39", "正四面体は辺 6・面 4", edges == 6 and faces == 4, f"頂点 {vertices} → 辺 {edges}・面 {faces}")

# ---------------------------------------------------------------
# C41 アルキメデスの王冠: 同じ質量なら、銀を混ぜた王冠のほうが体積(あふれる水)が大きいこと
#   (密度 金 19.3 g/cm3・銀 10.5 g/cm3。手順の妥当性そのものは人間レビューが砦)
# ---------------------------------------------------------------
if "C41" in BY_NO:
    rho_au, rho_ag, mass = 19.3, 10.5, 1000.0  # g/cm3, g
    v_pure = mass / rho_au
    for ag_ratio in (0.1, 0.3, 0.5):
        v_alloy = mass * (1 - ag_ratio) / rho_au + mass * ag_ratio / rho_ag
        check("C41", f"銀 {int(ag_ratio*100)}% 混入で体積が増える", v_alloy > v_pure, f"{v_alloy:.1f} cm3 > 純金 {v_pure:.1f} cm3")
    check("C41", "解説が『銀は金より軽い』を前提にする", "銀は金より軽い" in BY_NO["C41"]["explanation"] and rho_ag < rho_au, f"密度 銀 {rho_ag} < 金 {rho_au}")

# ---------------------------------------------------------------
# 機械検証不能(人間レビューが砦): A33 情景なぞなぞ / C39 の「平面では 2 つが限界」 / C40 ケーキの分け方(手順の妥当性)
# ---------------------------------------------------------------

print()
if failures:
    print(f"NG: {len(failures)} 件")
    for f in failures:
        print(" -", f)
    sys.exit(1)
print("すべての機械検証を通過")
