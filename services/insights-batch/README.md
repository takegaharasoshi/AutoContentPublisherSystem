# インサイト収集バッチ

Instagram Graph API から投稿別・アカウント日次のインサイトを収集し、Aurora MySQL に保存する ECS Fargate RunTask 用バッチです。

## 環境変数

`ENV_NAME`、`SET_CODE`、`EXECUTION_ARN`、`SCHEDULED_AT` が必須です。DB 接続には `DB_SECRET_ARN`、ローカル開発では `DB_SECRET_JSON` を使用します。`MEDIA_LOOKBACK_DAYS` は任意で、既定値は 14 日です。

## ローカルテスト

```bash
cd services/insights-batch && uv run pytest
```

## Docker ビルド

```bash
docker build -f services/insights-batch/Dockerfile -t insights-batch .
```
