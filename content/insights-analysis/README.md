# insights-analysis — インサイト集計ランナー

`post_insights` / `account_insights_daily` の JSON メトリクスを本番 Aurora から読み取り専用で集計し、
セット横断で「現行フォーマットの水準と推移」を出すツール。16-5 効果検証（2026-09-02）で作成した。
書き込みは一切しない（`SELECT` のみ・RDS Data API 経由）。

## 使い方

```bash
cd content/insights-analysis
python3 run_queries.py                    # 全クエリ（Aurora が一時停止中なら復帰を最大 8 回待つ）
python3 run_queries.py population weekly_age_fixed
python3 run_queries.py --since 2026-08-08 --split 2026-08-23
python3 run_queries.py kpi_post_monthly kpi_account_monthly   # 月次 KPI 転記用（16-12b）
```

- 接続先は `AURORA_CLUSTER_ARN` / `AURORA_SECRET_ARN`。未設定なら aws cli で自動解決する（`apply_aurora.py` と同じ方式）
- 結果は標準出力（等幅の表）と `results/<name>.json`。`results/` は git 管理外（`.gitignore`）。残す集計は `results/YYYY-MM-DD.txt` として明示的にコミットする

## クエリ

| 名前 | 内容 |
|---|---|
| `population` | 母集団（`--since` 以降に success 投稿されたリール）の件数・期間・インサイト有無 |
| `per_post_latest` | 投稿ごとの最新スナップショット（views / reach / スキップ率 / 平均視聴秒 / いいね / コメント / 保存 / シェア） |
| `by_set_period_slot` | セット × 期間（`--split` 前後）× スロット（朝・昼・夜）の平均・最小・最大 |
| `weekly_age_fixed` | 投稿週別の **72 時間水準**（投稿 + 3 日以降の最初のスナップショット。投稿年齢をそろえた推移用） |
| `growth_curve` | 投稿年齢（日）別の平均 views・スキップ率（何日で伸び切るかの確認） |
| `account_daily` | アカウント日次（直近 30 日）: フォロワー数・views・reach・engaged・comments・saves |
| `kpi_post_monthly` | **月次 KPI 転記用**（16-12b）。ビュー `v_post_kpi_monthly`（セット × 年月 × スロットの 72 時間水準の中央値。`slot='all'` は全スロット合算）をそのまま出す |
| `kpi_account_monthly` | **月次 KPI 転記用**（16-12b）。ビュー `v_account_kpi_monthly`（月末フォロワー・月間 reach 合計・収集日数）をそのまま出す |

`kpi_*` の転記先・手順は `docs/app/operation.html` セクション 6.3、ビューの定義は `docs/app/data-model.html` セクション 4.11（`database/V011__insights_kpi_views.sql`）。

## 読み方の注意

- `reels_skip_rate` は API の値そのままで **パーセント**（50.6 = 50.6%）
- `ig_reels_avg_watch_time` はミリ秒。表では秒に換算している
- 投稿翌日までのスナップショットは値が動く。比較には `weekly_age_fixed` の 72 時間水準を使う
- 平均は 1 本のバズで大きく歪む。判断には `per_post_latest` から中央値を取る（16-5 の記録を参照）
- `account_insights_daily.metrics` に `follows_and_unfollows` の内訳は入っていない（Meta の仕様で 100 フォロワー未満のアカウントには返らない。16-12b で確認）。フォロー増減は `followers_count` の差分（ビュー `v_account_kpi_daily.followers_delta`）で見る
