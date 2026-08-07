# 16-2: stock_items.py のフィールド仕様検証
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
errors = []

for it in ITEMS:
    no = it["no"]
    for field, limit in LIMITS.items():
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
    if "http" not in sn or "書き直し済み" not in sn:
        errors.append(f"{no}: source_note に URL または書き直しの旨がない")

combo = Counter((it["quiz_type"], it["difficulty"]) for it in ITEMS)
expected = {("L1", "light"): 14, ("L3", "standard"): 14, ("L1", "deep"): 14}
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
    print(f"  {field}: 最長 {mx} / 上限 {LIMITS[field]}")
