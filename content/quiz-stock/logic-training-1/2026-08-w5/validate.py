# 2026-08-w5 補充: stock_items.py のフィールド仕様検証
# 昼(L3/standard)は 16-4d で停止中のため、本バッチの対象は朝(L1/light)7 問 + 夜(L1/deep)7 問
# 仕様: docs/app/generators/gpt-quiz-multicut.html セクション 5
import sys
from collections import Counter

sys.path.insert(0, __file__.rsplit("/", 1)[0])
from stock_items import ITEMS

LIMITS = {
    "hook": 20,
    "hint": 20,
    "question": 90,
    "answer": 30,
    "explanation": 80,
    "coach_comment": 30,
    "summary": 100,
    "illustration_scene": 200,
}
# L3 の解説のみ 240 字(16-2b で方式設計書へ反映済みの 5 ステップ解説に対応)
L3_EXPLANATION_LIMIT = 240

# 個別の上限緩和(問題番号, フィールド) -> 上限。
# answer はキャプション専用フィールドで版面に出ないため、可読性のために超過を許すことがある。
# C24: 手順が 2 段階(同時点火 → 1 本目が尽きたら残り端)で 30 字に収まらない。
#      「答えに着火のタイミングを明記する」= 2026-08-31 ユーザー決定。
# C25: 川渡りの全 7 航行を答えに書くため 30 字に収まらない(同日ユーザー決定)。
# C31: 砂時計の全手順(同時開始 → 7 分計を裏返す → 11 分計落下時に再度)も同様。
# C34: 金貨の取り出し方(袋 n から n 枚)も手順が答えのため同様。
OVERRIDES = {("C24", "answer"): 40, ("C25", "answer"): 40, ("C31", "answer"): 45, ("C34", "answer"): 40}
errors = []


def limit_for(item: dict, field: str) -> int:
    """当該問題・当該フィールドの文字数上限を返す。

    Args:
        item: 問題 1 件。
        field: フィールド名。

    Returns:
        上限文字数。
    """
    if (item["no"], field) in OVERRIDES:
        return OVERRIDES[(item["no"], field)]
    if field == "explanation" and item["quiz_type"] == "L3":
        return L3_EXPLANATION_LIMIT
    return LIMITS[field]


for it in ITEMS:
    no = it["no"]
    for field in LIMITS:
        limit = limit_for(it, field)
        v = it[field]
        if not v:
            errors.append(f"{no}: {field} が空")
        elif len(v) > limit:
            errors.append(f"{no}: {field} が {len(v)} 字(上限 {limit}): {v[:30]}…")
    tags = it["tags"]
    if len(tags) != 3:
        errors.append(f"{no}: tags が {len(tags)} 個(ちょうど 3 個)")
    for t in tags:
        if len(t) > 10:
            errors.append(f"{no}: tag が {len(t)} 字(上限 10): {t}")
    if it["quiz_type"] == "L3":
        if not it["answer"].startswith("約") or "目安" not in it["answer"]:
            errors.append(f"{no}: L3 answer が「約〜(目安)」形式でない: {it['answer']}")
        if "×" not in it["explanation"]:
            errors.append(f"{no}: L3 explanation に式(×)がない")
    sn = it["source_note"]
    if "オリジナル書き下ろし" in sn:
        # 自作問題は流布例の裏取りが存在しないため URL を要求しない(2026-08-19 ユーザー決定)
        if "自作問題" not in sn:
            errors.append(f"{no}: オリジナル問題の source_note に「自作問題」の明記がない")
    elif "http" not in sn or "書き直し済み" not in sn:
        errors.append(f"{no}: source_note に URL または書き直しの旨がない")

combo = Counter((it["quiz_type"], it["difficulty"]) for it in ITEMS)
expected = {("L1", "light"): 7, ("L1", "deep"): 7}
if dict(combo) != expected:
    errors.append(f"内訳が不一致: {dict(combo)} (期待: {expected})")

nos = [it["no"] for it in ITEMS]
if len(nos) != len(set(nos)):
    errors.append("no の重複あり")
hooks = [it["hook"] for it in ITEMS]
for h, c in Counter(hooks).items():
    if c > 1:
        errors.append(f"hook の重複: {h} ({c} 件)")

if errors:
    print(f"NG: {len(errors)} 件")
    for e in errors:
        print(" -", e)
    sys.exit(1)
print(f"OK: {len(ITEMS)} 問すべて仕様適合(内訳 {dict(combo)})")
for field in LIMITS:
    mx = max(len(it[field]) for it in ITEMS)
    limits = {limit_for(it, field) for it in ITEMS}
    print(f"  {field}: 最長 {mx} / 上限 {'/'.join(str(x) for x in sorted(limits))}")
