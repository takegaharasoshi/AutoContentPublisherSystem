# 16-2: stock_items.py から review.md(人間レビュー用)と insert_quiz_stock.sql(投入用)を生成
import json
import sys

sys.path.insert(0, __file__.rsplit("/", 1)[0])
from stock_items import ITEMS

BASE = __file__.rsplit("/", 1)[0]

GROUPS = [
    ("L1", "light", "朝 7:30(morning)L1 なぞなぞ・言葉あそび / light"),
    ("L3", "standard", "昼 12:30(noon)L3 フェルミ推定(身近な規模感) / standard"),
    ("L1", "deep", "夜 21:00(night)L1 とんち・水平思考・ひっかけ / deep"),
]

# ---------- review.md ----------
lines = [
    "# 16-2 問題ストック初期整備: 42 問レビューシート(v2: 面白なぞなぞ路線)",
    "",
    "投入前の人間レビュー用(operation.html セクション 3 手順 3)。**承認後に Claude がローカル MySQL + Aurora へ INSERT** する(手順 4)。",
    "",
    "方向性はユーザーフィードバック(2026-08-01)を反映: **朝 = 定番なぞなぞ・言葉あそび / 昼 = フェルミ推定(身近で意外な題材へ刷新)/ 夜 = とんち・水平思考・ひっかけの古典**。旧版(古典論理パズル路線)は review_v1.md / stock_items_v1_logic.py に退避。",
    "",
    "## レビュー観点(operation.html 手順 3)",
    "",
    "1. **誤答チェック**(唯一の砦): 昼のフェルミ 14 問は算数を機械検証済み(verify_logic.py)。朝・夜のなぞなぞ・とんちは「広く流布した定番の想定解」であり機械検証できないため、**想定解として自然か・別解で炎上しないか**をご確認ください",
    "2. **表現の独自性・出典**: 全問 folklore 級・古典のみ採用(特定サイトの創作なぞなぞは除外)。各問の source_note に流布例 URL を記録済み。文面はすべて書き下ろし",
    "3. **既存ストック・出題履歴との重複**: 既出判明分は「資料 A〜E の確認順(L1)」「昼のコンビニ利用回数(L3)」の 2 問で、42 問と重複なし。**Aurora の quiz_items 全件との突合は投入時に実施**",
    "4. **フォーマット適合**: 文字数上限・L3 の「約〇〇(目安)」は validate.py で機械検証済み(全問適合)",
    "",
    "修正指示は「A03 の問題文を〜に」のように番号 + 項目名でお願いします。",
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
    "- 投入後は在庫確認クエリで 3 組 × 14 問を確認する(operation.html セクション 3)",
]

with open(f"{BASE}/review.md", "w", encoding="utf-8") as f:
    f.write("\n".join(lines) + "\n")

# ---------- insert_quiz_stock.sql ----------


def esc(s: str) -> str:
    return s.replace("\\", "\\\\").replace("'", "''")


sql = [
    "-- 16-2 問題ストック初期投入(42 問。レビュー承認後に実行)",
    "-- 生成元: plans/16-2-stock/stock_items.py(単一ソース)。適用先: ローカル MySQL / Aurora(acps)",
    "-- set_id は set_code から解決するため両環境共通で実行できる。",
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
    sql += [
        f"-- {it['no']}",
        "INSERT INTO quiz_stock_items (set_id, quiz_type, difficulty, question_text, answer_text, content_fields, source_note, is_active)",
        f"VALUES ((SELECT id FROM batch_sets WHERE set_code = 'logic-training-1'), '{it['quiz_type']}', '{it['difficulty']}',",
        f"        '{esc(it['question'])}',",
        f"        '{esc(it['answer'])}',",
        f"        '{esc(cf_json)}',",
        f"        '{esc(it['source_note'])}', 1);",
        "",
    ]

with open(f"{BASE}/insert_quiz_stock.sql", "w", encoding="utf-8") as f:
    f.write("\n".join(sql))

print(f"review.md: {len(ITEMS)} 問 / insert_quiz_stock.sql: {len(ITEMS)} INSERT 文を生成")
