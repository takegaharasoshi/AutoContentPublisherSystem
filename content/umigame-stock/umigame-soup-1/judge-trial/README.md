# 21-6b 判定モジュール試走

コメント判定案の比較用スクリプトです。本番コードではなく、実投稿や本番データの更新は行いません。評価ケースと真相ポイントのフィクスチャを使い、パターン 1 (gpt-6-luna) とパターン 2 (Jev) の結果・品質指標を記録します。

## ファイル構成

- `judge_contract.py`: 問題と判定結果の共通契約、batch-01 と真相ポイントの読み込み
- `templates.py`: パターン 2 と安全な後処理に使う定型文
- `pattern1_luna.py`: OpenAI chat completions による一括判定
- `pattern2_jev.py`: Jev の段階判定と定型返信
- `run_trial.py`: ケース実行、キャッシュ、集計とレポート生成
- `data/eval_problems.json`: 問題ごとの評価ケース
- `data/common_cases.json`: 問題に依存しない共通ケース
- `data/truth_points.json`: 各問題の真相ポイントと正解開示文
- `work/trial_results.json`: ケース ID × 方式の結果キャッシュ
- `work/trial_report.md`: 集計と誤りケースのレポート

評価入力の形式:

```json
{
  "U01": [
    {"id": "U01-Q01", "text": "影は写真に写っていますか？", "kind": "q_yesno", "answer": "yes"}
  ]
}
```

共通ケースは配列にし、問題番号順に round-robin で割り当てます。`answer` は `q_yesno` のケースだけに `yes` / `no` / `irrelevant` を指定します。

```json
[
  {"id": "COMMON-01", "text": "面白い問題！", "kind": "impression"}
]
```

真相フィクスチャは次の形式です。`truth_points` は 2〜4 項目、`reveal_text` は 70 字以内の開示文にします。

```json
{
  "U01": {
    "truth_points": ["真相の要点 1", "真相の要点 2"],
    "reveal_text": "正解時に開示する文。"
  }
}
```

## 実行方法

このディレクトリで実行します。

```bash
/home/takegaharawork/projects/AutoContentPublisherSystem/services/image-batch/.venv/bin/python run_trial.py
```

方式や問題、並列数、Jev の閾値を指定できます。結果は `work/trial_results.json` に保存され、`--from-cache` は API を呼ばずキャッシュだけを集計します。

```bash
python run_trial.py --methods p1 p2 --only U01 U12 --workers 6
python run_trial.py --methods p2 --t-point 0.6 --t-quality 0.25 --t-answer 0.6
python run_trial.py --from-cache
```

パターン 1 は `OPENAI_API_KEY` を優先し、未設定なら Secrets Manager の `umigame-poc/credentials` から `openai_api_key` を読みます。パターン 2 は `TYPESAFE_API_KEY` を使います。`~/.bashrc` に登録したキーを使う場合は、ログインシェルから起動します。

```bash
bash -ic 'cd /home/takegaharawork/projects/AutoContentPublisherSystem/content/umigame-stock/umigame-soup-1/judge-trial && /home/takegaharawork/projects/AutoContentPublisherSystem/services/image-batch/.venv/bin/python run_trial.py --methods p2'
```

## テスト

ネットワークを呼ばないモックテストです。

```bash
/home/takegaharawork/projects/AutoContentPublisherSystem/services/image-batch/.venv/bin/python -m pytest -q tests
```
