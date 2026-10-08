"""batch-01: stock_items.py から投入用 SQL を生成し、ローカル MySQL でドライランする。

- set_id は ``set_code='umigame-soup-1'`` のサブクエリで解決するため、ローカル / Aurora 共通の SQL。
- content_key は stock_items.py で採番済みの値をそのまま入れる（{3 桁連番}-{slug}。両環境で同一）。
- 先頭で batch_sets 行（``is_active = 0``）を既存でなければ作る（21-4b）。稼働化（``is_active = 1``）・
  ``problem_snapshot_enabled`` / ``stories_enabled`` の有効化は 21-7 の人間ゲートで行い、本 SQL では触らない。
- INSERT は ``stock_items.POST_ORDER`` の順に並べる（id の順 = 投稿順。2026-09-26 の素材の全数レビューで決定）。
- 既存行向けに core_points / reveal_text / title / truth / caption の UPDATE SQL と、
  judge_criteria（全 14 問）・U12 / U27 の fact_sheet・U27 の core_points の UPDATE SQL を生成する。
- ``--dry-run`` はローカル MySQL（docker の acps-mysql）でトランザクション内に流し、件数と content_key の
  重複を確認して ROLLBACK する。セットに既存ストック行があれば UPDATE、なければ INSERT を試す。

使い方:
    python3 generate.py            # INSERT SQL と 2 本の UPDATE SQL を生成
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

from stock_items import ITEMS, POST_ORDER  # noqa: E402
from umigame_common import SET_CODE  # noqa: E402

SQL_PATH = HERE / "insert_umigame_stock.sql"
UPDATE_SQL_PATH = HERE / "update_judge_points.sql"
CRITERIA_SQL_PATH = HERE / "update_judge_criteria.sql"
SET_NAME = "探偵カメロックのウミガメのスープ"
GENERATOR_NAME = "umigame-prebuilt"
MYSQL_CMD = [
    "docker", "exec", "-i", "acps-mysql", "mysql", "--default-character-set=utf8mb4",
    "--batch", "--skip-column-names",
    "-uroot", "-proot", "acps",
]


def esc(s: str) -> str:
    """MySQL の単一引用符リテラル用にエスケープする。"""
    return s.replace("\\", "\\\\").replace("'", "''")


def jsonlit(obj) -> str:
    """JSON カラム用のリテラル文字列を返す。"""
    return esc(json.dumps(obj, ensure_ascii=False, separators=(",", ":")))


def build_sql() -> str:
    """batch_sets 行と全問の INSERT 文を組み立てる。"""
    lines = [
        f"-- batch-01 ウミガメストック投入（{len(ITEMS)} 問。人間レビュー + プローブテスト承認後に実行）",
        "-- 生成元: content/umigame-stock/umigame-soup-1/batch-01/stock_items.py（単一ソース）。適用先: ローカル MySQL / Aurora（acps）",
        "-- set_id は set_code から解決するため両環境共通で実行できる。content_key は stock_items.py で採番済み。",
        "",
        "-- batch_sets 行（is_active = 0 で登録。稼働化は 21-7 の人間ゲート。既存なら作らない）",
        "INSERT INTO batch_sets (set_code, name, generator_name, is_active)",
        f"SELECT '{SET_CODE}', '{esc(SET_NAME)}', '{GENERATOR_NAME}', 0",
        f"WHERE NOT EXISTS (SELECT 1 FROM batch_sets WHERE set_code = '{SET_CODE}');",
        "",
    ]
    by_no = {it["no"]: it for it in ITEMS}
    lines += [
        "-- INSERT は stock_items.POST_ORDER の順（= id の順 = 投稿順。投稿バッチは未使用のストックを id の小さい順に選ぶ）",
        "",
    ]
    for order, no in enumerate(POST_ORDER, start=1):
        it = by_no[no]
        lines += [
            f"-- 投稿順 {order}: {it['no']} {it['title']}（{it['puzzle_type']}）",
            "INSERT INTO umigame_stock_items (set_id, content_key, title, difficulty, problem_text, truth, fact_sheet,",
            "    core_points, judge_criteria, reveal_text,",
            "    expected_questions, hook, rule_text, narration, play_example, character_lines, illustration_prompt,",
            "    caption, source_note, is_active)",
            f"VALUES ((SELECT id FROM batch_sets WHERE set_code = '{SET_CODE}'),",
            f"        '{esc(it['content_key'])}', '{esc(it['title'])}', {int(it['difficulty'])},",
            f"        '{esc(it['problem_text'])}',",
            f"        '{esc(it['truth'])}',",
            f"        '{jsonlit(it['fact_sheet'])}',",
            f"        '{jsonlit(it['core_points'])}', '{jsonlit(it['judge_criteria'])}', '{esc(it['reveal_text'])}',",
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


def build_update_sql() -> str:
    """既存 14 問へ判定要点と公開前提の文（core_points / reveal_text / title / truth / caption）を設定する UPDATE 文を組み立てる。

    title / truth / caption は 21-6d3e（truth を翌日リールのキャプションで公開する方針）で足した。
    """
    lines = [
        "-- batch-01 既存ストックの判定要点・公開前提の文の更新（V013 適用後に実行。title / truth / caption は 21-6d3e で追加）",
        "-- 生成元: content/umigame-stock/umigame-soup-1/batch-01/stock_items.py（単一ソース）",
        "-- 適用先: ローカル MySQL / Aurora（acps）。content_key で対象を特定する。",
        "",
    ]
    for it in ITEMS:
        lines += [
            f"-- {it['content_key']}: {it['title']}",
            "UPDATE umigame_stock_items s",
            "JOIN batch_sets b ON b.id = s.set_id",
            f"SET s.core_points = '{jsonlit(it['core_points'])}',",
            f"    s.reveal_text = '{esc(it['reveal_text'])}',",
            f"    s.title = '{esc(it['title'])}',",
            f"    s.truth = '{esc(it['truth'])}',",
            f"    s.caption = '{esc(it['caption'])}'",
            f"WHERE b.set_code = '{SET_CODE}' AND s.content_key = '{esc(it['content_key'])}';",
            "",
        ]
    return "\n".join(lines)


def build_criteria_update_sql() -> str:
    """既存の両表へ正解基準を設定し、U12・U27 の変更済み事実と U27 の要点も反映する。"""
    lines = [
        "-- batch-01 既存 14 問の正解基準と U12・U27 の事実・U27 の要点の更新（V014 適用後に実行）",
        "-- 生成元: content/umigame-stock/umigame-soup-1/batch-01/stock_items.py（単一ソース）",
        "-- 適用先: ローカル MySQL / Aurora（acps）。set_code と content_key で対象を特定する。",
        "-- 出題済み行がある場合は umigame_items のスナップショット値も更新する。",
        "",
    ]
    for it in ITEMS:
        updates = [f"judge_criteria = '{jsonlit(it['judge_criteria'])}'"]
        if it["no"] in ("U12", "U27"):  # U12 は 21-6d16 で楽器の事実を追加
            updates.append(f"fact_sheet = '{jsonlit(it['fact_sheet'])}'")
        if it["no"] == "U27":
            updates.append(f"core_points = '{jsonlit(it['core_points'])}'")
        lines.append(f"-- {it['content_key']}: {it['title']}")
        for table, alias in (("umigame_stock_items", "s"), ("umigame_items", "i")):
            lines += [
                f"UPDATE {table} {alias}",
                f"JOIN batch_sets b ON b.id = {alias}.set_id",
                "SET " + ",\n    ".join(f"{alias}.{update}" for update in updates),
                f"WHERE b.set_code = '{SET_CODE}' AND {alias}.content_key = '{esc(it['content_key'])}';",
                "",
            ]
    return "\n".join(lines)


def _run_mysql(script: str) -> tuple[int, str, str]:
    """ローカル MySQL に SQL を渡し、終了コード・標準出力・標準エラーを返す。"""
    proc = subprocess.run(MYSQL_CMD, input=script.encode("utf-8"), capture_output=True)
    out = proc.stdout.decode("utf-8", "replace")
    err = "\n".join(
        line for line in proc.stderr.decode("utf-8", "replace").splitlines()
        if "Using a password" not in line
    )
    return proc.returncode, out, err


def _print_mysql_result(out: str, err: str) -> None:
    """MySQL の結果を表示する。"""
    if out.strip():
        print(out.rstrip())
    if err.strip():
        print(err.rstrip(), file=sys.stderr)


def dry_run(sql: str, update_sql: str, criteria_sql: str) -> int:
    """既存行の有無に応じて UPDATE または INSERT を試し、確認後 ROLLBACK する。

    Args:
        sql: 生成した INSERT 文。
        update_sql: 既存行向け UPDATE 文。
        criteria_sql: 正解基準と U27 の変更を反映する UPDATE 文。

    Returns:
        終了コード（0 = 成功）。
    """
    probe = (
        "SELECT COUNT(*) FROM umigame_stock_items s "
        "JOIN batch_sets b ON b.id = s.set_id "
        f"WHERE b.set_code = '{SET_CODE}';"
    )
    probe_code, probe_out, probe_err = _run_mysql(probe)
    _print_mysql_result("", probe_err)
    if probe_code != 0:
        print(f"dry-run: NG（既存行確認の mysql 終了コード {probe_code}）")
        return 1
    try:
        existing_rows = int(probe_out.strip().splitlines()[-1])
    except (IndexError, ValueError):
        print("dry-run: NG（既存行確認の件数を読めない）")
        return 1

    if existing_rows:
        print(f"dry-run: 既存ストック {existing_rows} 件を検出。UPDATE SQL を実行します")
        action_sql = update_sql + "\n" + criteria_sql
        action_name = "UPDATE"
    else:
        print("dry-run: セットのストック行なし。INSERT SQL を実行します")
        action_sql = sql
        action_name = "INSERT"
    script = "\n".join(
        [
            "START TRANSACTION;",
            action_sql,
            "SELECT COUNT(*) AS stock_rows, COUNT(DISTINCT s.content_key) AS distinct_keys,",
            "       MIN(CHAR_LENGTH(s.problem_text)) AS min_problem_len,",
            "       MAX(CHAR_LENGTH(s.problem_text)) AS max_problem_len,",
            "       SUM(JSON_LENGTH(s.fact_sheet) BETWEEN 8 AND 20) AS fact_sheet_ok,",
            "       SUM(JSON_LENGTH(s.expected_questions) BETWEEN 15 AND 20) AS expected_q_ok,",
            "       SUM(JSON_LENGTH(s.play_example) = 6) AS play_example_ok,",
            "       SUM(core_points IS NOT NULL) AS core_points_set,",
            "       SUM(judge_criteria IS NOT NULL) AS judge_criteria_set,",
            "       SUM(reveal_text IS NOT NULL) AS reveal_text_set,",
            "       SUM(core_points IS NOT NULL AND reveal_text IS NOT NULL) AS judge_points_set,",
            "       SUM(JSON_LENGTH(core_points) BETWEEN 1 AND 3) AS core_points_ok,",
            "       MAX(CHAR_LENGTH(s.reveal_text)) AS max_reveal_text_len,",
            "       MAX(b.is_active) AS set_is_active",
            "FROM umigame_stock_items s JOIN batch_sets b ON b.id = s.set_id",
            f"WHERE b.set_code = '{SET_CODE}';",
            "ROLLBACK;",
        ]
    )
    code, out, err = _run_mysql(script)
    _print_mysql_result(out, err)
    if code != 0:
        print(f"dry-run: NG（mysql 終了コード {code}）")
        return 1
    print(f"dry-run: OK（{action_name} を試行して確認後 ROLLBACK 済み。DB は変更していない）")
    return 0


def main() -> int:
    """SQL を生成し、指定があればドライランする。"""
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    sql = build_sql()
    update_sql = build_update_sql()
    criteria_sql = build_criteria_update_sql()
    SQL_PATH.write_text(sql, encoding="utf-8")
    UPDATE_SQL_PATH.write_text(update_sql, encoding="utf-8")
    CRITERIA_SQL_PATH.write_text(criteria_sql, encoding="utf-8")
    print(f"generate: {SQL_PATH.name} に {len(ITEMS)} INSERT 文を生成")
    print(f"generate: {UPDATE_SQL_PATH.name} に {len(ITEMS)} UPDATE 文を生成")
    print(f"generate: {CRITERIA_SQL_PATH.name} に {len(ITEMS) * 2} UPDATE 文を生成")
    if args.dry_run:
        return dry_run(sql, update_sql, criteria_sql)
    return 0


if __name__ == "__main__":
    sys.exit(main())
