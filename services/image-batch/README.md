# 画像生成バッチ

画像生成を行う ECS Fargate RunTask 用バッチです。現状は Phase 5 空回し用の Hello World であり、業務ロジックは実装していません。

## 環境変数

現段階では環境変数を使用しません。将来の受け渡し契約は `docs/infra/workflow.html` のセクション 5.2 を参照してください。

## ローカルテスト

```bash
cd services/image-batch
uv venv --python 3.12
uv pip install -r requirements-dev.txt
uv run pytest
```

## Docker ビルドとローカル動作確認

```bash
cd services/image-batch
docker build -t image-batch .
docker run --rm image-batch
```

## Docker ビルドと ECR push

不変タグには Git コミットハッシュを使用します。push 前に作業ツリーがクリーン（コミット済み）であることを確認してください。`--provenance=false` は必須です（省略すると buildx が attestation 用のタグなしイメージを ECR に登録し、ECR ライフサイクルルールの「1 push = 1 イメージ」の前提が崩れるため）。

```bash
cd services/image-batch
IMAGE=516964473143.dkr.ecr.ap-northeast-1.amazonaws.com/auto-content-publisher/image-batch
TAG=$(git rev-parse --short=12 HEAD)

docker build --platform linux/amd64 --provenance=false -t "${IMAGE}:${TAG}" .
aws ecr get-login-password --region ap-northeast-1 | docker login --username AWS --password-stdin 516964473143.dkr.ecr.ap-northeast-1.amazonaws.com
docker push "${IMAGE}:${TAG}"
```
