# 2026-09-w3 補充: stock_items.py のフィールド仕様検証
# 昼(L3/standard)は 16-4d で停止中のため、本バッチの対象は朝(L1/light)7 問 + 夜(L1/deep)7 問
# 仕様: docs/app/generators/gpt-quiz-multicut.html セクション 5
#
# 実行方法(2 段構え。課題体系 I-033 の同梱で 2026-09-20 から):
#   1) 執筆ツール側の上限検証(このファイルの LIMITS)       … python3 validate.py でも動く
#   2) 実行時同等検証(image-batch の validate_content_fields) … 依存(PIL 等)があるため uv 環境で実行する:
#        cd services/image-batch && uv run python ../../content/quiz-stock/logic-training-1/2026-09-w3/validate.py
#      2) は投入前に必ず通す(2) が import できない環境では NG 終了する)。2026-09-04 の障害
#      (実行時 FIELD_LIMITS 違反が LRU 先頭に来て本番停止)の再発防止。
import json
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from content_fields import content_fields_of  # noqa: E402
from stock_items import ITEMS  # noqa: E402

# 実行時(services/image-batch)の検証関数を同じ環境から読む。pytest と同じ pythonpath(app と shared)を足す
REPO = HERE.parents[3]
sys.path.insert(0, str(REPO / "services" / "image-batch"))
sys.path.insert(0, str(REPO / "shared"))

LIMITS = {
    "hook": 20,
    "hint": 20,
    "question": 80,  # 改修 R-2(2026-09-19)で 90 → 80 字。版面の使える高さ 294px・下限 44px で収まる上限(I-035)
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
# 「答えが手順の問題は answer に全手順を書く」= 2026-08-31 ユーザー決定(w5 C24/C25/C31/C34 と同じ扱い)。
OVERRIDES = {}  # 本バッチは緩和なし(型: {(問題番号, フィールド): 上限})
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

# ---- 実行時同等検証(I-033): 投入する content_fields JSON を、image-batch が実行時に使う関数そのもので検証する ----
# quiz-prebuilt 方式ではキャプション専用フィールド(answer / explanation / coach_comment)は実行時に長さを縛らない
# (quiz_prebuilt.CAPTION_ONLY_FIELDS)。ここでもまったく同じ引数で呼び、実行時が拒否する行を投入前に必ず落とす。
try:
    from app.generators.gpt_quiz_multicut import validate_content_fields
    from app.generators.quiz_prebuilt import CAPTION_ONLY_FIELDS
except Exception as exc:  # 依存(PIL 等)や Python の版が古い素の python3 で走らせたとき(ImportError・TypeError 等)
    errors.append(
        "実行時同等検証を実行できない(image-batch の依存が読めない): "
        f"{exc}。`cd services/image-batch && uv run python <このファイル>` で再実行すること"
    )
else:
    runtime_ok = 0
    for it in ITEMS:
        cf_json = json.dumps(content_fields_of(it), ensure_ascii=False, separators=(",", ":"))
        try:
            validate_content_fields(cf_json, it["quiz_type"], CAPTION_ONLY_FIELDS)
        except RuntimeError as exc:
            errors.append(f"{it['no']}: 実行時検証 NG: {exc}")
        else:
            runtime_ok += 1
    print(f"実行時同等検証(validate_content_fields + CAPTION_ONLY_FIELDS={sorted(CAPTION_ONLY_FIELDS)}): {runtime_ok}/{len(ITEMS)} 問 OK")

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
