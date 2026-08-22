# 2026-08-w3 補充: 機械検証できる問題の数値・構造チェック
# なぞなぞ・とんち(朝・夜の大半)は「定番の想定解」であり機械検証の対象外 → 人間レビューが砦。
# ここでは昼のフェルミ推定の算数、朝の文字あそび、夜のブルートフォース可能な論理問題を検証する。
from datetime import date, timedelta
from fractions import Fraction
from itertools import combinations, permutations

checks = []


def check(name, cond, note=""):
    checks.append((name, cond, note))


# ---- 昼(L3)フェルミ推定の算数 ----
# B15 電柱: 居住地の道路 120万km、100m あたり 3 本
poles = 1_200_000 * 1000 / 100 * 3
check("B15 電柱3600万本", 3.4e7 < poles < 3.8e7, f"{poles:,.0f}本(12億m÷100m×3本)")

# B16 郵便ポスト: 可住地 12万km² ÷ 2.4万局 = 1 局 5km²、一辺 800m(0.64km²)に 1 本
area_per_office = 12e4 / 2.4e4
per_office = area_per_office / 0.8 ** 2
posts = 2.4e4 * 8
check("B16 1局5km²", abs(area_per_office - 5) < 0.1, f"12万km²÷2.4万局={area_per_office:.1f}km²")
check("B16 1局あたり約8本", 7.5 < per_office < 8.5, f"5km²÷0.64km²={per_office:.1f}本")
check("B16 ポスト19万本", 18e4 < posts < 20e4, f"{posts:,.0f}本(実勢 17.5万本)")

# B17 歯科診療所: 国試合格 2400 人/年 × 40 年 = 歯科医師 10 万人、1 軒あたり 1.5 人
dentists = 2400 * 40  # 96,000 → 解説では「約10万人」に丸める
clinic_dentists = 1e5 * 0.9  # 病院勤務を 1 割と見て除外 → 診療所で働く歯科医師
dental = clinic_dentists / 1.5  # 1 軒あたり院長 + 勤務医で平均 1.5 人
check("B17 歯科医師10万人", 9e4 < dentists < 1.1e5, f"2400人×40年={dentists:,.0f}人≒10万人(実勢 約10万7千人)")
check("B17 診療所勤務9万人", clinic_dentists == 9e4, "10万人×0.9=9万人(実勢 診療所従事 約9万人)")
check("B17 歯科6万軒", 5.5e4 < dental < 6.5e4, f"{dental:,.0f}軒(実勢 66,818軒)")

# B18 道路橋: 川の総延長 14万km × 川 1km あたりの道路との交差回数(道路格子 200m → 5 回)
crossings_per_km = 1 / 0.2
bridges = 14e4 * crossings_per_km
check("B18 川1kmで5回交差", abs(crossings_per_km - 5) < 0.01, "道路の間隔200m → 1km÷0.2km=5回")
check("B18 橋70万橋", 6.5e5 < bridges < 7.5e5, f"{bridges:,.0f}橋(実勢 約73万橋)")

# B19 肉用鶏: 1 人 14kg ÷ 1 羽 1.7kg → 消費羽数、自給率 2/3 で国産出荷、鶏舎 70 日回転で在庫換算
consumed = 1.2e8 * 14 / 1.7
shipped = consumed * 2 / 3
broiler = shipped * 70 / 365
check("B19 消費10億羽相当", 9e8 < consumed < 1.1e9, f"{consumed:,.0f}羽/年")
check("B19 国産出荷6.6億羽", 6.3e8 < shipped < 6.9e8, f"{shipped:,.0f}羽/年(実勢 出荷 約7億羽)")
check("B19 肉用鶏1億3千万羽", 1.2e8 < broiler < 1.4e8, f"{broiler:,.0f}羽(実勢 1億3923万羽)")

# B20 信号機: 市街地 1.9万km²、300m 四方に 1 基(= 1km² あたり 11.1 基)
per_km2 = (1000 / 300) ** 2
signals = 1.9e4 * 11
check("B20 交差点密度11基/km²", 10.5 < per_km2 < 11.5, f"300m四方で {per_km2:.1f}基/km²")
check("B20 信号機21万基", 2.0e5 < signals < 2.2e5, f"{signals:,.0f}基(実勢 約21万基)")

# B21 道路トンネル: 山地 26万km²(国土 37.8万 × 0.7)、谷 4km 間隔 → 山道 6.5万km、5km に 1 本
mountain_area = 378_000 * 0.7
mountain_road = mountain_area / 4
tunnels = mountain_road / 5
check("B21 山地26万km²", 2.5e5 < mountain_area < 2.7e5, f"37.8万km²×0.7={mountain_area:,.0f}km²")
check("B21 山道6.5万km", 6.0e4 < mountain_road < 7.0e4, f"26万km²÷4km={mountain_road:,.0f}km")
check("B21 トンネル1万3千か所", 1.2e4 < tunnels < 1.4e4, f"{tunnels:,.0f}か所(実勢 約1.2万か所)")

# 市街地面積の仮定が国土に対して妥当か(国土 37.8万km² の約 5%)
check("B20 市街地1.9万km²", abs(378_000 * 0.05 - 18_900) < 100, "37.8万km²×5%=1.89万km²")

# ---- 朝(L1)文字あそびの機械確認 ----
check("A16 イルカ逆読み", "いるか"[::-1] == "かるい", "いるか ⇄ かるい")
check(
    "A19 たいやき⇄やきたい",
    sorted("たいやき") == sorted("やきたい") and "たいやき" != "やきたい",
    "同じ4文字の並べかえで別の語になる",
)

# ---- 夜(L1)ブルートフォース可能な論理問題 ----
# C15 17頭のラクダ: 1 頭借りて 18 頭にすると各人の取り分が整数になり、合計が元の 17 頭に戻る。
SHARES = (Fraction(1, 2), Fraction(1, 3), Fraction(1, 9))
check(
    "C15 遺言の合計は1に満たない",
    sum(SHARES) == Fraction(17, 18),
    f"1/2+1/3+1/9={sum(SHARES)}(1 に 1/18 足りない → 1 頭借りても返せる)",
)
check("C15 17頭では割り切れない", any((17 * s).denominator != 1 for s in SHARES), "17×1/2=8.5 頭")
lent = [18 * s for s in SHARES]
check("C15 18頭なら全員整数", all(x.denominator == 1 for x in lent), f"長男{lent[0]}・次男{lent[1]}・三男{lent[2]}頭")
check("C15 合計17頭で1頭返せる", sum(lent) == 17, f"9+6+2={sum(lent)}頭(借りた1頭が残る)")
check(
    "C15 借用なしでは整数解なし",
    not all((17 * s).denominator == 1 for s in SHARES),
    "17 頭のままでは遺言どおりに分けられない",
)

# C21 誤ラベルの3箱: ラベル(りんご/みかん/両方)がすべて誤り。
# 「両方」ラベルの箱から 1 個取り出せば中身が一意に決まるかを全列挙で確認する。
LABELS = ("りんご", "みかん", "両方")
valid = [
    p for p in permutations(LABELS)
    if all(label != content for label, content in zip(LABELS, p))
]
check("C21 全ラベル誤りの配置は2通り", len(valid) == 2, f"配置 {valid}")

# 「両方」ラベルの箱(index 2)は、どの配置でも単一果物である
check(
    "C21 「両方」箱は必ず単一果物",
    all(p[2] in ("りんご", "みかん") for p in valid),
    "→ 1 個取り出せば中身が判明する",
)

# 取り出した果物で配置が一意に決まる(同じ果物に 2 配置が対応しない)
outcomes = [p[2] for p in valid]
check("C21 取り出し結果で一意に確定", len(set(outcomes)) == len(valid), f"取り出し {outcomes}")

# 他のラベル(りんご / みかん)から取ると一意に決まらない場合があることも確認(想定解の必然性)
for idx, label in ((0, "りんご"), (1, "みかん")):
    picks = [p[idx] for p in valid]
    ambiguous = any(p == "両方" for p in picks)
    check(
        f"C21 「{label}」箱から取るのは不適",
        ambiguous,
        f"中身候補 {picks}(両方が混じり1個では確定しない)",
    )

# C16 2人の番人: 「もう一人はどちらの道と言うか」への返答は、聞いた相手が正直/うそのどちらでも
# 必ず「まちがった道」になる。正しい道 × 聞いた相手の 4 通りを全列挙して確認する。
gate_ok = []
for correct in (0, 1):
    for asked_is_honest in (True, False):
        other_is_honest = not asked_is_honest
        other_answer = correct if other_is_honest else 1 - correct
        reply = other_answer if asked_is_honest else 1 - other_answer
        gate_ok.append((reply != correct, 1 - reply == correct))
check("C16 返答は常にまちがった道", all(a for a, _ in gate_ok), f"4 通りすべてで返答≠正解")
check("C16 返答の逆が常に正解", all(b for _, b in gate_ok), "正しい道×聞いた相手の 4 通りを全列挙")

# C18 吊り橋と1つの灯り: 灯りは必ず携行・同時2人まで。全状態(各人の岸 × 灯りの位置)を
# ダイクストラ法で最短探索し、17 分が最小であること・素朴解(最速が毎回付き添う)が 19 分を確認する。
BRIDGE = {"A": 1, "B": 2, "C": 5, "D": 10}


def shortest_crossing(times):
    start = (frozenset(times), 0)
    dist = {start: 0}
    queue = [(0, start)]
    while queue:
        queue.sort()
        cost, state = queue.pop(0)
        if dist.get(state, cost + 1) < cost:
            continue
        here, torch = state
        if not here and torch == 1:
            return cost
        movers = here if torch == 0 else frozenset(times) - here
        groups = [frozenset(g) for g in combinations(movers, 2)] + [frozenset([m]) for m in movers]
        for group in groups:
            spent = max(times[m] for m in group)
            nxt = ((here - group, 1) if torch == 0 else (here | group, 0))
            if cost + spent < dist.get(nxt, float("inf")):
                dist[nxt] = cost + spent
                queue.append((cost + spent, nxt))
    return None


check("C18 最短は17分", shortest_crossing(BRIDGE) == 17, "全状態の最短探索で 17 分")
check("C18 素朴解は19分", 2 + 1 + 5 + 1 + 10 == 19, "最速の1分が毎回付き添うと 19 分(2分損する)")

# C19 おととい12歳・来年15歳: 誕生日を 12/31 と置き、1 年分の日付を総当たりして
# 「おととい 12 歳」かつ「翌年の誕生日に 15 歳」を満たす日が 1/1 のみであることを確認する。
BIRTHDAY = date(2013, 12, 31)


def age_on(birth, when):
    return when.year - birth.year - ((when.month, when.day) < (birth.month, birth.day))


matching = []
for offset in range(365):
    today = date(2027, 1, 1) + timedelta(days=offset)
    two_days_ago = today - timedelta(days=2)
    next_year_birthday = date(today.year + 1, BIRTHDAY.month, BIRTHDAY.day)
    if age_on(BIRTHDAY, two_days_ago) == 12 and age_on(BIRTHDAY, next_year_birthday) == 15:
        matching.append(today.isoformat())

check("C19 成立する日は1日だけ", len(matching) == 1, f"該当 {matching}")
check("C19 その日は1月1日", matching == ["2027-01-01"], "誕生日 12/31・今日 1/1 で発言がすべて成立")
check("C19 きのう13歳になっている", age_on(BIRTHDAY, date(2026, 12, 31)) == 13, "12/31 の誕生日で 12→13 歳")

ng = [c for c in checks if not c[1]]
for name, ok, note in checks:
    print(f"{'OK' if ok else 'NG'} {name}: {note}")
print(f"\n{'全チェック OK' if not ng else f'NG {len(ng)} 件'}(なぞなぞ・とんちの想定解は人間レビューで確認)")
raise SystemExit(1 if ng else 0)
