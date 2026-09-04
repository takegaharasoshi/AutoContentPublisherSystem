"""batch-01: stock_items.py から投入用 insert_umigame_stock.sql を生成し、ローカル MySQL でドライランする。

- set_id は ``set_code='umigame-soup-1'`` のサブクエリで解決するため、ローカル / Aurora 共通の SQL。
- content_key は stock_items.py で採番済みの値をそのまま入れる（{3 桁連番}-{slug}。両環境で同一）。
- ``--dry-run`` はローカル MySQL（docker の acps-mysql）でトランザクション内に流し、件数と content_key の
  重複を確認して ROLLBACK する。batch_sets 行がまだ無い環境（21-7 で登録）では、同じトランザクション内に
  仮の行を作ってから流す（ROLLBACK で消える）。Aurora への投入は 21-4b（人間ゲート後）。

使い方:
    python3 generate.py            # insert_umigame_stock.sql を生成
    python3 generate.py --dry-run  # 生成 + ローカル MySQL でドライラン
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parent / "common"))

from stock_items import ITEMS  # noqa: E402
from umigame_common import SET_CODE  # noqa: E402

SQL_PATH = HERE / "insert_umigame_stock.sql"
MYSQL_CMD = [
    "docker", "exec", "-i", "acps-mysql", "mysql", "--default-character-set=utf8mb4",
    "-uroot", "-proot", "acps",
]


def esc(s: str) -> str:
    """MySQL の単一引用符リテラル用にエスケープする。"""
    return s.replace("\\", "\\\\").replace("'", "''")


def jsonlit(obj) -> str:
    """JSON カラム用のリテラル文字列を返す。"""
    return esc(json.dumps(obj, ensure_ascii=False, separators=(",", ":")))


def build_sql() -> str:
    """全問の INSERT 文を組み立てる。"""
    lines = [
        f"-- batch-01 ウミガメストック投入（{len(ITEMS)} 問。人間レビュー + プローブテスト承認後に実行）",
        "-- 生成元: content/umigame-stock/umigame-soup-1/batch-01/stock_items.py（単一ソース）。適用先: ローカル MySQL / Aurora（acps）",
        "-- set_id は set_code から解決するため両環境共通で実行できる。content_key は stock_items.py で採番済み。",
        "",
    ]
    for it in ITEMS:
        lines += [
            f"-- {it['no']} {it['title']}",
            "INSERT INTO umigame_stock_items (set_id, content_key, title, difficulty, problem_text, truth, fact_sheet,",
            "    expected_questions, hook, rule_text, narration, play_example, character_lines, illustration_prompt,",
            "    caption, source_note, is_active)",
            f"VALUES ((SELECT id FROM batch_sets WHERE set_code = '{SET_CODE}'),",
            f"        '{esc(it['content_key'])}', '{esc(it['title'])}', {int(it['difficulty'])},",
            f"        '{esc(it['problem_text'])}',",
            f"        '{esc(it['truth'])}',",
            f"        '{jsonlit(it['fact_sheet'])}',",
            f"        '{jsonlit(it['expected_questions'])}',",
            f"        '{esc(it['hook'])}', '{esc(it['rule_text'])}',",
            f"        '{jsonlit(it['narration'])}',",
            f"        '{jsonlit(it['play_example'])}',",
            f"        '{jsonlit(it['character_lines'])}',",
            f"        '{esc(it['illustration_prompt'])}',",
            f"        '{esc(it['caption'])}',",
            f"        '{esc(it['source_note'])}', 1);",
            "",
        ]
    return "\n".join(lines)


def dry_run(sql: str) -> int:
    """ローカル MySQL でトランザクション内に流し、件数確認後 ROLLBACK する。

    Args:
        sql: 生成した INSERT 文。

    Returns:
        終了コード（0 = 成功）。
    """
    script = "\n".join(
        [
            "START TRANSACTION;",
            f"INSERT INTO batch_sets (set_code, name, generator_name, is_active)",
            f"SELECT '{SET_CODE}', 'umigame-soup-1（dry-run 仮行）', 'umigame-prebuilt', 0",
            f"WHERE NOT EXISTS (SELECT 1 FROM batch_sets WHERE set_code = '{SET_CODE}');",
            sql,
            "SELECT COUNT(*) AS inserted, COUNT(DISTINCT content_key) AS distinct_keys,",
            "       MIN(CHAR_LENGTH(problem_text)) AS min_problem_len, MAX(CHAR_LENGTH(problem_text)) AS max_problem_len,",
            "       SUM(JSON_LENGTH(fact_sheet) BETWEEN 8 AND 12) AS fact_sheet_ok,",
            "       SUM(JSON_LENGTH(expected_questions) BETWEEN 15 AND 20) AS expected_q_ok,",
            "       SUM(JSON_LENGTH(play_example) = 6) AS play_example_ok",
            "FROM umigame_stock_items s JOIN batch_sets b ON b.id = s.set_id",
            f"WHERE b.set_code = '{SET_CODE}';",
            "ROLLBACK;",
        ]
    )
    proc = subprocess.run(MYSQL_CMD, input=script.encode("utf-8"), capture_output=True)
    out = proc.stdout.decode("utf-8", "replace")
    err = "\n".join(l for l in proc.stderr.decode("utf-8", "replace").splitlines() if "Using a password" not in l)
    print(out.rstrip())
    if err.strip():
        print(err.rstrip(), file=sys.stderr)
    if proc.returncode != 0:
        print(f"dry-run: NG（mysql 終了コード {proc.returncode}）")
        return 1
    print(f"dry-run: OK（{len(ITEMS)} 件を INSERT → ROLLBACK 済み。DB は変更していない）")
    return 0


def main() -> int:
    """SQL を生成し、指定があればドライランする。"""
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    sql = build_sql()
    SQL_PATH.write_text(sql, encoding="utf-8")
    print(f"generate: {SQL_PATH.name} に {len(ITEMS)} INSERT 文を生成")
    if args.dry_run:
        return dry_run(sql)
    return 0


if __name__ == "__main__":
    sys.exit(main())
