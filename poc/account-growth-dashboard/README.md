# account-growth-dashboard — アカウント成長ノートの PoC

アイデア `docs/ideas/account-growth-visualization.md` の試作。3 アカウントのフォロワー・再生・リーチを
週単位で見せるスマホ向けのページを、集計ランナーの結果から組み立てる。設計書ではなく試作の資材。

- 公開先（非公開のアーティファクト）: https://claude.ai/artifact/NMPNxbEYTwtC8AVQDSFwBk
- `template.html`: ページ本体。`/*DATA*/` に集計結果が入る。節目の人数・表示名・色は冒頭の `SETS` にある
- `build.py`: 集計結果を埋め込んで `out/growth.html` を書き出す（`out/` は git 管理外）

## 更新の手順（週 1 回）

```bash
cd content/insights-analysis && python3 run_queries.py growth_account_weekly growth_post_weekly
```

```bash
python3 poc/account-growth-dashboard/build.py
```

そのあと Claude Code で `out/growth.html` を上の公開先へ公開し直す
（Artifact の publish に `url` として公開先を渡す。渡さないと別のページができる）。
