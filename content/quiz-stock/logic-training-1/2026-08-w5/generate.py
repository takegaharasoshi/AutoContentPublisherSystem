# 2026-08-w5 補充: stock_items.py から review.md(人間レビュー用)と insert_quiz_stock.sql(投入用)を生成
import json
import sys

sys.path.insert(0, __file__.rsplit("/", 1)[0])
from stock_items import ITEMS

BASE = __file__.rsplit("/", 1)[0]

# 昼(L3 / standard)は 16-4d(2026-08-24)で停止中のため本バッチの対象外
GROUPS = [
    ("L1", "light", "朝 7:30(morning)L1 なぞなぞ・言葉あそび / light"),
    ("L1", "deep", "夜 21:00(night)L1 とんち・水平思考・ひっかけ / deep"),
]

# content_key の採番用: quiz_type × difficulty → slot_code(V007 で導入。data-model.html セクション 4.10)
SLOT_CODES = {("L1", "light"): "morning", ("L3", "standard"): "noon", ("L1", "deep"): "night"}

# ---------- review.md ----------
lines = [
    "# 2026-08-w5 問題ストック補充: 14 問レビューシート",
    "",
    "投入前の人間レビュー用(operation.html セクション 3 手順 3)。**承認後に Claude がローカル MySQL + Aurora へ INSERT** する(手順 4)。",
    "",
    "補充対象は **朝 = なぞなぞ・言葉あそび / 夜 = とんち・水平思考・ひっかけの古典** の 2 組 × 7 問(1 週間分)。昼(L3 / standard)は 16-4d で停止中のため補充しない。",
    "",
    "## 着手時の在庫(2026-08-31)",
    "",
    "- 朝(L1/light)= 未使用 0 問 / 夜(L1/deep)= 未使用 0 問。**両組とも在庫ゼロで再利用出題に突入済み**(のべ使用 23 回 > 在庫 21 問)",
    "- 昼(L3/standard)= 未使用 7 問。停止中のため補充対象外(既存在庫は凍結・残置)",
    "",
    "## レビュー観点(operation.html 手順 3)",
    "",
    "1. **誤答チェック**(唯一の砦): 夜の論理パズルはブルートフォースで一意解を機械検証済み(verify_logic.py)。朝のなぞなぞ・夜のとんちは「想定解」であり機械検証できないため、**想定解として自然か・別解で炎上しないか**をご確認ください",
    "2. **表現の独自性・出典**: 全問 folklore 級・古典のみ採用(特定サイトの創作なぞなぞは除外)。各問の source_note に流布例 URL を記録済み。文面はすべて書き下ろし",
    "3. **既存ストック・出題履歴との重複**: 既存ストック 63 問(2026-08-initial 42 + 2026-08-w3 21)と突合済み。投入直前に Aurora の quiz_items 全件と再突合する",
    "4. **フォーマット適合**: 文字数上限・tags 数・出典 URL は validate.py で機械検証済み(全問適合)",
    "",
    "修正指示は「A15 の問題文を〜に」のように番号 + 項目名でお願いします。",
    "",
]

for qt, diff, title in GROUPS:
    lines.append(f"## {title}")
    lines.append("")
    for it in ITEMS:
        if it["quiz_type"] != qt or it["difficulty"] != diff:
            continue
        lines += [
            f"### {it['no']}",
            "",
            f"- **つかみ**(動画1カット目の吹き出し・キャプション1行目): {it['hook']}",
            f"- **ヒント**(動画3カット目の吹き出し・カウントダウンと同時表示): {it['hint']}",
            f"- **問題文**(動画に常時表示): {it['question']}",
            f"- **答え**(動画には出さずキャプションで開示): {it['answer']}",
            f"- **解説**(キャプションで開示): {it['explanation']}",
            f"- **コーチの一言**(キャプション末尾): {it['coach_comment']}",
            f"- **タグ**(記録用): {' / '.join(it['tags'])}",
            f"- **出題要旨**(記録用・重複管理の単位): {it['summary']}",
            f"- **イラストの情景**(問題文の下に配置するイラストの生成指示文): {it['illustration_scene']}",
            f"- **出典メモ**(著作権の証跡): {it['source_note']}",
            "",
        ]

lines += [
    "## 投入時の注意(承認後に Claude が実施)",
    "",
    "- INSERT は `insert_quiz_stock.sql` を使用(set_id は `set_code='logic-training-1'` のサブクエリで解決するためローカル/Aurora 共通)",
    "- ローカルは `docker exec` + `--default-character-set=utf8mb4`(15-10 の知見)",
    "- Aurora は Data API 経由(本セッションでは classifier にブロックされたため、投入時に許可が必要)",
    "- 投入前に Aurora の `quiz_items` の summary 全件を取得し、既出題との重複がないか最終確認する",
    "- 投入後は在庫確認クエリで朝・夜が各 + 7 問(未使用ビルド済み 7 問以上)になることを確認する(operation.html セクション 3)",
    "- 投入しただけでは出題候補にならない。手順 5(イラスト生成 → ビルド → 全数レビュー → S3 配置)まで完了させ `unbuilt` = 0 にする",
]

with open(f"{BASE}/review.md", "w", encoding="utf-8") as f:
    f.write("\n".join(lines) + "\n")

# ---------- insert_quiz_stock.sql ----------


def esc(s: str) -> str:
    return s.replace("\\", "\\\\").replace("'", "''")


def next_content_key_expr(slot_code: str) -> str:
    """スロット内の既存最大連番 + 1 を適用時に解決する SQL 式を返す。

    両環境が同一の content_key 集合を持つ(投入運用の不変条件)前提で、
    ローカル / Aurora のどちらで実行しても同じ値に解決される。
    派生テーブルを挟むのは INSERT 対象と同じテーブルの参照(ERROR 1093)を避けるため。
    """
    return (
        f"(SELECT CONCAT('{slot_code}-', LPAD(COALESCE(MAX(CAST(SUBSTRING_INDEX(t.content_key, '-', -1) AS UNSIGNED)), 0) + 1, 3, '0'))"
        f" FROM (SELECT q.content_key FROM quiz_stock_items q JOIN batch_sets b ON b.id = q.set_id"
        f" WHERE b.set_code = 'logic-training-1' AND q.content_key LIKE '{slot_code}-%') t)"
    )


sql = [
    "-- 2026-08-w5 問題ストック補充投入(14 問。レビュー承認後に実行)",
    "-- 生成元: content/quiz-stock/logic-training-1/2026-08-w5/stock_items.py(単一ソース)。適用先: ローカル MySQL / Aurora(acps)",
    "-- set_id は set_code から解決するため両環境共通で実行できる。",
    "-- content_key はスロット内の既存最大連番 + 1 を適用時に解決する(V007。両環境で同一値になる)。",
    "",
]
for it in ITEMS:
    cf = {
        "hook": it["hook"],
        "hint": it["hint"],
        "question": it["question"],
        "answer": it["answer"],
        "explanation": it["explanation"],
        "coach_comment": it["coach_comment"],
        "tags": it["tags"],
        "summary": it["summary"],
        "illustration_scene": it["illustration_scene"],
    }
    cf_json = json.dumps(cf, ensure_ascii=False, separators=(",", ":"))
    slot_code = SLOT_CODES[(it["quiz_type"], it["difficulty"])]
    sql += [
        f"-- {it['no']}",
        "INSERT INTO quiz_stock_items (set_id, content_key, quiz_type, difficulty, question_text, answer_text, content_fields, source_note, is_active)",
        f"VALUES ((SELECT id FROM batch_sets WHERE set_code = 'logic-training-1'),",
        f"        {next_content_key_expr(slot_code)},",
        f"        '{it['quiz_type']}', '{it['difficulty']}',",
        f"        '{esc(it['question'])}',",
        f"        '{esc(it['answer'])}',",
        f"        '{esc(cf_json)}',",
        f"        '{esc(it['source_note'])}', 1);",
        "",
    ]

with open(f"{BASE}/insert_quiz_stock.sql", "w", encoding="utf-8") as f:
    f.write("\n".join(sql))

print(f"review.md: {len(ITEMS)} 問 / insert_quiz_stock.sql: {len(ITEMS)} INSERT 文を生成")
