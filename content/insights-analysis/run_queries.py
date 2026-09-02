"""インサイト集計ランナー（読み取り専用・RDS Data API 経由）。

16-5 効果検証（2026-09-02）で作成。``post_insights`` / ``account_insights_daily`` の
JSON メトリクスを集計し、セット横断で「現行フォーマットの水準と推移」を出す。

使い方::

    python run_queries.py                       # 全クエリ
    python run_queries.py population weekly     # 指定クエリのみ
    python run_queries.py --since 2026-08-08 --split 2026-08-23
    python run_queries.py kpi_post_monthly kpi_account_monthly   # 月次 KPI 転記用（V011 のビュー）

出力: 標準出力にテキスト表、``results/<name>.json`` に生データ。
接続先は ``AURORA_CLUSTER_ARN`` / ``AURORA_SECRET_ARN``（未設定なら aws cli で自動解決）。
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import time
from pathlib import Path

HERE = Path(__file__).parent
OUT = HERE / "results"
DB = "acps"
JST = "INTERVAL 9 HOUR"


def metric(key: str, typ: str = "DECIMAL(12,4)") -> str:
    """post_insights.metrics の JSON キーを SQL の数値式にする。"""
    return f"CAST(JSON_UNQUOTE(JSON_EXTRACT(pi.metrics, '$.{key}')) AS {typ})"


def build_queries(since: str, split: str) -> dict[str, str]:
    """集計クエリを組み立てる。

    Args:
        since: 母集団の起点日（JST）。この日以降に success 投稿されたリールが対象。
        split: フォーマット切替日（JST）。期間比較の境界。

    Returns:
        クエリ名 → SQL。
    """
    population = f"""
      posts p
      JOIN batch_sets bs ON bs.id = p.set_id
      JOIN sns_accounts sa ON sa.id = p.sns_account_id
      WHERE p.status = 'success' AND p.platform_post_id IS NOT NULL
        AND p.media_type = 'reel'
        AND p.posted_at + {JST} >= '{since} 00:00:00'
    """
    # 投稿ごとの最新スナップショット
    latest = """
      JOIN (SELECT post_id, MAX(collected_at) AS collected_at FROM post_insights GROUP BY post_id) lt
        ON lt.post_id = p.id
      JOIN post_insights pi ON pi.post_id = lt.post_id AND pi.collected_at = lt.collected_at
    """
    # 72 時間水準: posted_at + 3 日以降で最初のスナップショット（投稿年齢をそろえた比較用）
    age_fixed = """
      JOIN (SELECT s.post_id, MIN(s.collected_at) AS collected_at
              FROM post_insights s JOIN posts q ON q.id = s.post_id
             WHERE s.collected_at >= q.posted_at + INTERVAL 3 DAY
             GROUP BY s.post_id) af ON af.post_id = p.id
      JOIN post_insights pi ON pi.post_id = af.post_id AND pi.collected_at = af.collected_at
    """
    slot = f"""CASE WHEN HOUR(p.posted_at + {JST}) < 11 THEN 'morning'
                    WHEN HOUR(p.posted_at + {JST}) < 16 THEN 'noon' ELSE 'evening' END"""
    period = f"CASE WHEN p.posted_at + {JST} < '{split}' THEN 'a:before {split}' ELSE 'b:from {split}' END"

    def pop_with(join: str) -> str:
        return population.replace("posts p\n", f"posts p\n{join}\n", 1)

    return {
        "population": f"""
SELECT bs.set_code, sa.account_code, COUNT(*) AS reels,
       MIN(DATE(p.posted_at + {JST})) AS first_post_jst,
       MAX(DATE(p.posted_at + {JST})) AS last_post_jst,
       SUM(EXISTS (SELECT 1 FROM post_insights x WHERE x.post_id = p.id)) AS with_insights
FROM {population}
GROUP BY bs.set_code, sa.account_code ORDER BY bs.set_code""",

        "per_post_latest": f"""
SELECT bs.set_code, p.id AS post_id,
       DATE_FORMAT(p.posted_at + {JST}, '%m-%d %H:%i') AS posted_jst,
       ROUND(TIMESTAMPDIFF(HOUR, p.posted_at, pi.collected_at)/24, 1) AS age_days,
       {metric('views','SIGNED')} AS views, {metric('reach','SIGNED')} AS reach,
       ROUND({metric('reels_skip_rate')}, 1) AS skip_rate_pct,
       ROUND({metric('ig_reels_avg_watch_time')}/1000, 1) AS avg_watch_s,
       {metric('likes','SIGNED')} AS likes, {metric('comments','SIGNED')} AS comments,
       {metric('saved','SIGNED')} AS saved, {metric('shares','SIGNED')} AS shares
FROM {pop_with(latest)}
ORDER BY bs.set_code, p.posted_at""",

        "by_set_period_slot": f"""
SELECT bs.set_code, {period} AS period, {slot} AS slot, COUNT(*) AS n,
       ROUND(AVG({metric('views','SIGNED')})) AS avg_views,
       MIN({metric('views','SIGNED')}) AS min_views, MAX({metric('views','SIGNED')}) AS max_views,
       ROUND(AVG({metric('reels_skip_rate')}), 1) AS avg_skip_pct,
       ROUND(AVG({metric('ig_reels_avg_watch_time')})/1000, 1) AS avg_watch_s,
       ROUND(AVG({metric('comments','SIGNED')}), 2) AS avg_comments,
       ROUND(AVG({metric('saved','SIGNED')}), 2) AS avg_saved,
       ROUND(AVG({metric('likes','SIGNED')}), 2) AS avg_likes
FROM {pop_with(latest)}
GROUP BY bs.set_code, period, slot ORDER BY bs.set_code, period, slot""",

        "weekly_age_fixed": f"""
SELECT bs.set_code,
       DATE_FORMAT(DATE_SUB(DATE(p.posted_at + {JST}), INTERVAL WEEKDAY(p.posted_at + {JST}) DAY), '%m-%d') AS week_from,
       COUNT(*) AS n,
       ROUND(AVG({metric('views','SIGNED')})) AS avg_views_72h,
       ROUND(AVG({metric('reach','SIGNED')})) AS avg_reach_72h,
       ROUND(AVG({metric('reels_skip_rate')}), 1) AS avg_skip_pct_72h,
       ROUND(AVG({metric('ig_reels_avg_watch_time')})/1000, 1) AS avg_watch_s_72h,
       ROUND(AVG({metric('comments','SIGNED')}), 2) AS avg_comments_72h,
       ROUND(AVG({metric('saved','SIGNED')}), 2) AS avg_saved_72h
FROM {pop_with(age_fixed)}
GROUP BY bs.set_code, week_from ORDER BY bs.set_code, week_from""",

        "growth_curve": f"""
SELECT bs.set_code, LEAST(TIMESTAMPDIFF(DAY, p.posted_at, pi.collected_at), 14) AS age_d,
       COUNT(DISTINCT p.id) AS posts,
       ROUND(AVG({metric('views','SIGNED')})) AS avg_views,
       ROUND(AVG({metric('reels_skip_rate')}), 1) AS avg_skip_pct
FROM {pop_with('JOIN post_insights pi ON pi.post_id = p.id')}
GROUP BY bs.set_code, age_d ORDER BY bs.set_code, age_d""",

        "account_daily": f"""
SELECT bs.set_code, ai.metric_date, ai.followers_count,
       CAST(JSON_UNQUOTE(JSON_EXTRACT(ai.metrics, '$.views')) AS SIGNED) AS views,
       CAST(JSON_UNQUOTE(JSON_EXTRACT(ai.metrics, '$.reach')) AS SIGNED) AS reach,
       CAST(JSON_UNQUOTE(JSON_EXTRACT(ai.metrics, '$.accounts_engaged')) AS SIGNED) AS engaged,
       CAST(JSON_UNQUOTE(JSON_EXTRACT(ai.metrics, '$.comments')) AS SIGNED) AS comments,
       CAST(JSON_UNQUOTE(JSON_EXTRACT(ai.metrics, '$.saves')) AS SIGNED) AS saves
FROM account_insights_daily ai JOIN batch_sets bs ON bs.id = ai.set_id
WHERE ai.metric_date >= DATE_SUB(CURDATE(), INTERVAL 30 DAY)
ORDER BY bs.set_code, ai.metric_date""",

        # 16-12b: 月次転記用。V011 のビューをそのまま引く（--since / --split は使わない）
        "kpi_post_monthly": """
SELECT set_code, post_month, slot, posts, median_views, median_skip_rate_pct, median_avg_watch_s,
       median_comments, median_saved
FROM v_post_kpi_monthly
ORDER BY set_code, post_month, FIELD(slot, 'all', 'morning', 'noon', 'evening')""",

        "kpi_account_monthly": """
SELECT set_code, metric_month, days_collected, first_date, last_date,
       month_end_followers, month_end_followers_date, reach_total
FROM v_account_kpi_monthly
ORDER BY set_code, metric_month""",
    }


def resolve_endpoints() -> tuple[str, str]:
    """Aurora クラスタ ARN と認証情報 Secret ARN を解決する。"""
    def discover(cmd: list[str]) -> str:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=60, check=True)
        return r.stdout.split()[0]
    cluster = os.environ.get("AURORA_CLUSTER_ARN") or discover(
        ["aws", "rds", "describe-db-clusters", "--query", "DBClusters[0].DBClusterArn", "--output", "text"])
    secret = os.environ.get("AURORA_SECRET_ARN") or discover(
        ["aws", "secretsmanager", "list-secrets", "--query",
         "SecretList[?contains(Name,'db/credentials')].ARN", "--output", "text"])
    return cluster, secret


def execute(cluster: str, secret: str, sql: str) -> list[dict]:
    """1 文を Data API で実行し、行の辞書リストを返す（自動一時停止からの復帰を待つ）。"""
    cmd = ["aws", "rds-data", "execute-statement", "--resource-arn", cluster, "--secret-arn", secret,
           "--database", DB, "--sql", sql, "--format-records-as", "JSON", "--output", "json"]
    for attempt in range(8):
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=180)
        if r.returncode == 0:
            return json.loads(json.loads(r.stdout).get("formattedRecords", "[]"))
        if "DatabaseResumingException" in r.stderr or "Communications link failure" in r.stderr:
            print(f"  (DB resuming, retry {attempt + 1})", file=sys.stderr)
            time.sleep(20)
            continue
        raise SystemExit(r.stderr.strip())
    raise SystemExit("DB did not resume")


def render(rows: list[dict]) -> str:
    """行の辞書リストを等幅テキスト表にする。"""
    if not rows:
        return "(0 rows)"
    cols = list(rows[0].keys())
    cells = [["" if r.get(c) is None else str(r.get(c)) for c in cols] for r in rows]
    width = [max(len(c), *(len(row[i]) for row in cells)) for i, c in enumerate(cols)]

    def line(vals: list[str]) -> str:
        return "  ".join(v.ljust(width[i]) for i, v in enumerate(vals))

    return "\n".join([line(cols), line(["-" * w for w in width]), *(line(r) for r in cells), f"({len(rows)} rows)"])


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("names", nargs="*", help="実行するクエリ名（省略時は全部）")
    parser.add_argument("--since", default="2026-08-08", help="母集団の起点日 JST（既定: 2026-08-08）")
    parser.add_argument("--split", default="2026-08-23", help="期間比較の境界日 JST（既定: 2026-08-23 = 3 カット化）")
    args = parser.parse_args()
    queries = build_queries(args.since, args.split)
    names = args.names or list(queries)
    unknown = [n for n in names if n not in queries]
    if unknown:
        raise SystemExit(f"unknown query: {unknown}. available: {list(queries)}")
    OUT.mkdir(exist_ok=True)
    cluster, secret = resolve_endpoints()
    for name in names:
        rows = execute(cluster, secret, queries[name])
        (OUT / f"{name}.json").write_text(json.dumps(rows, ensure_ascii=False, indent=1))
        print(f"\n## {name}\n{render(rows)}")


if __name__ == "__main__":
    main()
