# SNS 投稿バッチ

SNS 投稿を行う ECS Fargate RunTask 用バッチです。Phase 6 では Aurora（MySQL）への接続確認として、`connection_test` テーブルへの INSERT / SELECT を実行します。

## 環境変数

`ENV_NAME` は必須です。通常は `DB_SECRET_ARN` に Secrets Manager の ARN を渡します。ローカル開発では `DB_SECRET_JSON` に Secret JSON を直接渡せますが、この方法はローカル開発専用です。

## ローカルテスト

```bash
cd services/sns-post-batch && uv run pytest
```

## Docker ビルドとローカル動作確認

リポジトリルートから実行します。接続先のローカル MySQL は `docker compose up -d` で起動しておきます（接続情報はルート README の「ローカル開発環境」を参照）。

```bash
docker build -f services/sns-post-batch/Dockerfile -t sns-post-batch .

export ENV_NAME=local
export DB_SECRET_JSON='{"username":"app","password":"password","host":"host.docker.internal","port":3306,"dbname":"acps"}'
docker run --rm -e ENV_NAME -e DB_SECRET_JSON sns-post-batch
```

## Docker ビルドと ECR push

不変タグには Git コミットハッシュを使用します。push 前に作業ツリーがクリーン（コミット済み）であることを確認してください。`--provenance=false` は必須です（省略すると buildx が attestation 用のタグなしイメージを ECR に登録し、ECR ライフサイクルルールの「1 push = 1 イメージ」の前提が崩れるため）。

```bash
IMAGE=516964473143.dkr.ecr.ap-northeast-1.amazonaws.com/auto-content-publisher/sns-post-batch
TAG=$(git rev-parse --short=12 HEAD)

docker build --platform linux/amd64 --provenance=false -f services/sns-post-batch/Dockerfile -t "${IMAGE}:${TAG}" .
aws ecr get-login-password --region ap-northeast-1 | docker login --username AWS --password-stdin 516964473143.dkr.ecr.ap-northeast-1.amazonaws.com
docker push "${IMAGE}:${TAG}"
```
