# SNS 投稿バッチ

SNS 投稿を行う ECS Fargate RunTask 用バッチです。現状は Phase 4 空回し用の Hello World であり、業務ロジックは実装していません。

## 環境変数

現段階では環境変数を使用しません。将来の受け渡し契約は `docs/infra/workflow.html` のセクション 5.2 を参照してください。

## ローカルテスト

```bash
cd services/sns-post-batch
uv venv --python 3.12
uv pip install -r requirements-dev.txt
uv run pytest
```

## Docker ビルドとローカル動作確認

```bash
cd services/sns-post-batch
docker build -t sns-post-batch .
docker run --rm sns-post-batch
```

ECR push の手順は Phase 4-2 で追記予定です。
