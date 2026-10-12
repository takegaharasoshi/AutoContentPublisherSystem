# SNS 投稿バッチ

指定セットの予定時刻に完全一致する生成実行の素材を有効アカウントへ投稿し、投稿状態と実行ログを Aurora（MySQL）に記録する ECS Fargate RunTask 用バッチです。

## 環境変数

`ENV_NAME` は必須です。通常は `DB_SECRET_ARN` に Secrets Manager の ARN を渡します。ローカル開発では `DB_SECRET_JSON` に Secret JSON を直接渡せますが、この方法はローカル開発専用です。

| 環境変数 | 内容 |
| --- | --- |
| `SET_CODE` | 必須。投稿対象のセットコード。 |
| `SCHEDULED_AT` | 必須。UTC の `YYYY-MM-DDTHH:MM:SSZ` 形式。その回の `generation_runs.scheduled_at` と一致させ、現在時刻を入れない。欠落・不正値は DB 接続前に失敗する。 |
| `EXECUTION_ARN` | 必須。SNS 投稿 Step Functions の実行 ARN（ローカルでは実行を識別する一意な値）。 |
| `S3_BUCKET_NAME` | 必須。投稿素材を置いた S3 バケット名。 |

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
export SET_CODE=sample-set
export SCHEDULED_AT=2026-10-12T22:30:00Z
export EXECUTION_ARN=local-sns-20261012T223000Z
export S3_BUCKET_NAME=local-test-bucket
docker run --rm -e ENV_NAME -e DB_SECRET_JSON \
  -e SET_CODE -e SCHEDULED_AT -e EXECUTION_ARN -e S3_BUCKET_NAME sns-post-batch
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
