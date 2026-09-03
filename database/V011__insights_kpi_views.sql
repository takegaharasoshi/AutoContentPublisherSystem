-- V011__insights_kpi_views.sql
-- AutoContentPublisherSystem 「継続的に見る指標セット」（16-12a で確定）のビュー昇格
--
-- 設計の詳細（指標の定義・72 時間水準の基準スナップショット・中央値の求め方・転記先）は
-- docs/app/data-model.html のセクション 4.11、月次の転記運用は docs/app/operation.html の
-- セクション 6.3 を参照。DDL のバージョン管理は Flyway 風の命名規則（V<連番>__<説明>.sql）に従う。
--
-- 方式: 生成カラムは追加せずビューのみで昇格する（決定は data-model.html 4.11 の decision）。
--   ・投稿単位の基準スナップショット（posted_at + 72 時間以降の最初の行）は JOIN でしか選べず、
--     生成カラムでは表現できない
--   ・現行規模（post_insights 1 日約 200 行）では JSON 抽出のインデックス化は不要
--   ・Meta のメトリクス改名時は CREATE OR REPLACE VIEW だけで追随できる（テーブルの ALTER 不要）
--
-- 稼働中 DB への適用順序: 追加のみ（ビュー 6 本の新設。既存テーブルは変更しない）でアプリと無関係のため、
-- デプロイとの順序調整は不要。CREATE OR REPLACE VIEW のため再適用は冪等。
-- 前提: MySQL 8.0.14 以降（ウィンドウ関数・ビュー内の派生テーブル）。ローカル MySQL 8.0.46 と Aurora MySQL 3.10.3 へ 2026-09-03 適用済み。
-- 全 DATETIME は UTC。投稿の年月・スロットは JST（+9 時間）で切る。アカウント日次の年月は UTC 日のまま。
-- DDL は暗黙コミットされるため、単一トランザクション化は行わない。

-- ============================================================
-- 投稿単位: 72 時間水準（1 投稿 1 行）
-- ============================================================
-- 母集団: success かつ platform_post_id を持つリール（集計ランナー content/insights-analysis と同じ）
-- 基準スナップショット: collected_at >= posted_at + 72 時間 を満たす post_insights のうち最初の 1 行
-- （collected_at, id の昇順）。まだ 72 時間に達していない投稿は行を持たない。
CREATE OR REPLACE VIEW v_post_kpi_72h AS
SELECT
    bs.set_code,
    p.set_id,
    p.id AS post_id,
    p.sns_account_id,
    p.posted_at,
    DATE_FORMAT(p.posted_at + INTERVAL 9 HOUR, '%Y-%m') AS post_month,
    CASE
        WHEN HOUR(p.posted_at + INTERVAL 9 HOUR) < 11 THEN 'morning'
        WHEN HOUR(p.posted_at + INTERVAL 9 HOUR) < 16 THEN 'noon'
        ELSE 'evening'
    END AS slot,
    pi.collected_at,
    TIMESTAMPDIFF(HOUR, p.posted_at, pi.collected_at) AS age_hours,
    CAST(JSON_UNQUOTE(JSON_EXTRACT(pi.metrics, '$.views')) AS SIGNED) AS views,
    CAST(JSON_UNQUOTE(JSON_EXTRACT(pi.metrics, '$.reels_skip_rate')) AS DECIMAL(6, 2)) AS skip_rate_pct,
    ROUND(CAST(JSON_UNQUOTE(JSON_EXTRACT(pi.metrics, '$.ig_reels_avg_watch_time')) AS DECIMAL(12, 3)) / 1000, 1) AS avg_watch_s,
    CAST(JSON_UNQUOTE(JSON_EXTRACT(pi.metrics, '$.comments')) AS SIGNED) AS comments,
    CAST(JSON_UNQUOTE(JSON_EXTRACT(pi.metrics, '$.saved')) AS SIGNED) AS saved
FROM posts p
JOIN batch_sets bs ON bs.id = p.set_id
JOIN (
    SELECT s.id,
           ROW_NUMBER() OVER (PARTITION BY s.post_id ORDER BY s.collected_at, s.id) AS rn
    FROM post_insights s
    JOIN posts q ON q.id = s.post_id
    WHERE s.collected_at >= q.posted_at + INTERVAL 72 HOUR
) af ON af.rn = 1
JOIN post_insights pi ON pi.id = af.id AND pi.post_id = p.id
WHERE p.status = 'success'
  AND p.platform_post_id IS NOT NULL
  AND p.media_type = 'reel';

-- ============================================================
-- 投稿単位: 月次中央値の内部ビュー（順位付け）
-- ============================================================
-- 指標ごとに「セット × 年月 × スロット」と「セット × 年月（全スロット）」の 2 通りで順位を付ける。
-- NULL（キー欠落）の行は末尾に送り、件数 n_* は非 NULL のみを数える（中央値の対象から外す）。
CREATE OR REPLACE VIEW v_post_kpi_72h_ranked AS
SELECT
    k.*,
    COUNT(k.views)         OVER (PARTITION BY k.set_code, k.post_month, k.slot) AS n_views_slot,
    ROW_NUMBER()           OVER (PARTITION BY k.set_code, k.post_month, k.slot ORDER BY (k.views IS NULL), k.views) AS rn_views_slot,
    COUNT(k.skip_rate_pct) OVER (PARTITION BY k.set_code, k.post_month, k.slot) AS n_skip_slot,
    ROW_NUMBER()           OVER (PARTITION BY k.set_code, k.post_month, k.slot ORDER BY (k.skip_rate_pct IS NULL), k.skip_rate_pct) AS rn_skip_slot,
    COUNT(k.avg_watch_s)   OVER (PARTITION BY k.set_code, k.post_month, k.slot) AS n_watch_slot,
    ROW_NUMBER()           OVER (PARTITION BY k.set_code, k.post_month, k.slot ORDER BY (k.avg_watch_s IS NULL), k.avg_watch_s) AS rn_watch_slot,
    COUNT(k.comments)      OVER (PARTITION BY k.set_code, k.post_month, k.slot) AS n_comments_slot,
    ROW_NUMBER()           OVER (PARTITION BY k.set_code, k.post_month, k.slot ORDER BY (k.comments IS NULL), k.comments) AS rn_comments_slot,
    COUNT(k.saved)         OVER (PARTITION BY k.set_code, k.post_month, k.slot) AS n_saved_slot,
    ROW_NUMBER()           OVER (PARTITION BY k.set_code, k.post_month, k.slot ORDER BY (k.saved IS NULL), k.saved) AS rn_saved_slot,
    COUNT(k.views)         OVER (PARTITION BY k.set_code, k.post_month) AS n_views_all,
    ROW_NUMBER()           OVER (PARTITION BY k.set_code, k.post_month ORDER BY (k.views IS NULL), k.views) AS rn_views_all,
    COUNT(k.skip_rate_pct) OVER (PARTITION BY k.set_code, k.post_month) AS n_skip_all,
    ROW_NUMBER()           OVER (PARTITION BY k.set_code, k.post_month ORDER BY (k.skip_rate_pct IS NULL), k.skip_rate_pct) AS rn_skip_all,
    COUNT(k.avg_watch_s)   OVER (PARTITION BY k.set_code, k.post_month) AS n_watch_all,
    ROW_NUMBER()           OVER (PARTITION BY k.set_code, k.post_month ORDER BY (k.avg_watch_s IS NULL), k.avg_watch_s) AS rn_watch_all,
    COUNT(k.comments)      OVER (PARTITION BY k.set_code, k.post_month) AS n_comments_all,
    ROW_NUMBER()           OVER (PARTITION BY k.set_code, k.post_month ORDER BY (k.comments IS NULL), k.comments) AS rn_comments_all,
    COUNT(k.saved)         OVER (PARTITION BY k.set_code, k.post_month) AS n_saved_all,
    ROW_NUMBER()           OVER (PARTITION BY k.set_code, k.post_month ORDER BY (k.saved IS NULL), k.saved) AS rn_saved_all
FROM v_post_kpi_72h k;

-- ============================================================
-- 投稿単位: 月次中央値（セット × 年月 × スロット + 全スロット行 'all'）
-- ============================================================
-- 中央値 = 非 NULL の値を昇順に並べたときの中央（偶数件は中央 2 件の平均）。
-- セット計画書の KPI 欄へはこのビューの行をそのまま転記する（operation.html 6.3）。
CREATE OR REPLACE VIEW v_post_kpi_monthly AS
SELECT
    r.set_code,
    r.post_month,
    r.slot,
    COUNT(*) AS posts,
    ROUND(AVG(CASE WHEN r.rn_views_slot    IN (FLOOR((r.n_views_slot    + 1) / 2), CEIL((r.n_views_slot    + 1) / 2)) THEN r.views         END), 1) AS median_views,
    ROUND(AVG(CASE WHEN r.rn_skip_slot     IN (FLOOR((r.n_skip_slot     + 1) / 2), CEIL((r.n_skip_slot     + 1) / 2)) THEN r.skip_rate_pct END), 1) AS median_skip_rate_pct,
    ROUND(AVG(CASE WHEN r.rn_watch_slot    IN (FLOOR((r.n_watch_slot    + 1) / 2), CEIL((r.n_watch_slot    + 1) / 2)) THEN r.avg_watch_s   END), 1) AS median_avg_watch_s,
    ROUND(AVG(CASE WHEN r.rn_comments_slot IN (FLOOR((r.n_comments_slot + 1) / 2), CEIL((r.n_comments_slot + 1) / 2)) THEN r.comments      END), 1) AS median_comments,
    ROUND(AVG(CASE WHEN r.rn_saved_slot    IN (FLOOR((r.n_saved_slot    + 1) / 2), CEIL((r.n_saved_slot    + 1) / 2)) THEN r.saved         END), 1) AS median_saved
FROM v_post_kpi_72h_ranked r
GROUP BY r.set_code, r.post_month, r.slot
UNION ALL
SELECT
    r.set_code,
    r.post_month,
    'all' AS slot,
    COUNT(*) AS posts,
    ROUND(AVG(CASE WHEN r.rn_views_all    IN (FLOOR((r.n_views_all    + 1) / 2), CEIL((r.n_views_all    + 1) / 2)) THEN r.views         END), 1) AS median_views,
    ROUND(AVG(CASE WHEN r.rn_skip_all     IN (FLOOR((r.n_skip_all     + 1) / 2), CEIL((r.n_skip_all     + 1) / 2)) THEN r.skip_rate_pct END), 1) AS median_skip_rate_pct,
    ROUND(AVG(CASE WHEN r.rn_watch_all    IN (FLOOR((r.n_watch_all    + 1) / 2), CEIL((r.n_watch_all    + 1) / 2)) THEN r.avg_watch_s   END), 1) AS median_avg_watch_s,
    ROUND(AVG(CASE WHEN r.rn_comments_all IN (FLOOR((r.n_comments_all + 1) / 2), CEIL((r.n_comments_all + 1) / 2)) THEN r.comments      END), 1) AS median_comments,
    ROUND(AVG(CASE WHEN r.rn_saved_all    IN (FLOOR((r.n_saved_all    + 1) / 2), CEIL((r.n_saved_all    + 1) / 2)) THEN r.saved         END), 1) AS median_saved
FROM v_post_kpi_72h_ranked r
GROUP BY r.set_code, r.post_month;

-- ============================================================
-- アカウント単位: 日次（1 アカウント・UTC 日につき 1 行）
-- ============================================================
-- followers_delta は前行（直前の収集日）との差。バックフィル行（followers_count NULL）や欠測日を挟むと
-- NULL または複数日分の差になる。follows_and_unfollows は 100 フォロワー未満のアカウントには API が返さないため
-- （Meta 公式リファレンスの記載。2026-09-03 確認）、フォロー増減は当面この差分で見る。
CREATE OR REPLACE VIEW v_account_kpi_daily AS
SELECT
    bs.set_code,
    ai.set_id,
    ai.sns_account_id,
    ai.metric_date,
    DATE_FORMAT(ai.metric_date, '%Y-%m') AS metric_month,
    ai.followers_count,
    CAST(ai.followers_count AS SIGNED)
        - CAST(LAG(ai.followers_count) OVER (PARTITION BY ai.sns_account_id ORDER BY ai.metric_date) AS SIGNED) AS followers_delta,
    CAST(JSON_UNQUOTE(JSON_EXTRACT(ai.metrics, '$.reach')) AS SIGNED) AS reach,
    ai.collected_at
FROM account_insights_daily ai
JOIN batch_sets bs ON bs.id = ai.set_id;

-- ============================================================
-- アカウント単位: 月次の内部ビュー（月末フォロワーの特定）
-- ============================================================
-- 月末フォロワー = その月の行のうち followers_count が非 NULL で最も遅い日の値（バックフィル行は NULL のため除外）。
CREATE OR REPLACE VIEW v_account_kpi_daily_ranked AS
SELECT
    d.*,
    FIRST_VALUE(d.followers_count) OVER w AS month_end_followers,
    FIRST_VALUE(CASE WHEN d.followers_count IS NOT NULL THEN d.metric_date END) OVER w AS month_end_followers_date
FROM v_account_kpi_daily d
WINDOW w AS (
    PARTITION BY d.sns_account_id, d.metric_month
    ORDER BY (d.followers_count IS NULL), d.metric_date DESC
    ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
);

-- ============================================================
-- アカウント単位: 月次（セット × アカウント × 年月）
-- ============================================================
-- 事業戦略書 KPI 実績表（月末フォロワー・月間 reach 合計）へはこのビューの行を転記する（operation.html 6.3）。
-- days_collected が月の日数に満たない月は reach_total が部分合計である点に注意（欠測日は補完しない）。
CREATE OR REPLACE VIEW v_account_kpi_monthly AS
SELECT
    r.set_code,
    r.set_id,
    r.sns_account_id,
    r.metric_month,
    COUNT(*) AS days_collected,
    MIN(r.metric_date) AS first_date,
    MAX(r.metric_date) AS last_date,
    MAX(r.month_end_followers) AS month_end_followers,
    MAX(r.month_end_followers_date) AS month_end_followers_date,
    SUM(r.reach) AS reach_total
FROM v_account_kpi_daily_ranked r
GROUP BY r.set_code, r.set_id, r.sns_account_id, r.metric_month;
