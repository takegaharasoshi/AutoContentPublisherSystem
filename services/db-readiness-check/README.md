# DB 準備確認バッチ

Aurora Serverless v2（MySQL 互換）が自動一時停止から再開し、接続可能になるまで待機する ECS Fargate RunTask 用バッチです。Step Functions ワークフローの最初に実行します。

## 環境変数

| 変数 | 説明 |
| --- | --- |
| `DB_SECRET_ARN` | DB 接続情報を持つ Secrets Manager の ARN。必須です。 |
| `ENV_NAME` | 実行環境名（例: `prod`）。必須です。 |

Secrets Manager の `SecretString` は次の JSON スキーマです。`port` は数値または文字列の数値を指定できます。

```json
{
  "username": "db_user",
  "password": "db_password",
  "host": "database-cluster.example.ap-northeast-1.rds.amazonaws.com",
  "port": 3306,
  "dbname": "application"
}
```

## リトライ仕様

接続確認では `SELECT 1` を実行します。初回試行に加え最大 8 回リトライし、合計 9 回試行します。`OperationalError` と `InterfaceError` のみをリトライし、待機時間は 2、4、8、16、32、64、128、256 秒です。最後の失敗後は待機しません。Secrets Manager からの Secret 取得は 1 回のみで、リトライしません。

このタスク自身が DB の起動待ちを完結するため、Step Functions 側では Retry を設定しません。

## ローカルテスト

```bash
cd services/db-readiness-check
uv venv --python 3.12
uv pip install -r requirements-dev.txt
uv run pytest
```

## Docker ビルドと ECR push

不変タグには Git コミットハッシュを使用します。push 前に作業ツリーがクリーン（コミット済み）であることを確認してください。`--provenance=false` は必須です（省略すると buildx が attestation 用のタグなしイメージを ECR に登録し、ECR ライフサイクルルールの「1 push = 1 イメージ」の前提が崩れるため）。

```bash
cd services/db-readiness-check
IMAGE=516964473143.dkr.ecr.ap-northeast-1.amazonaws.com/auto-content-publisher/db-readiness-check
TAG=$(git rev-parse --short=12 HEAD)

docker build --platform linux/amd64 --provenance=false -t "${IMAGE}:${TAG}" .
aws ecr get-login-password --region ap-northeast-1 | docker login --username AWS --password-stdin 516964473143.dkr.ecr.ap-northeast-1.amazonaws.com
docker push "${IMAGE}:${TAG}"
```

## 注記

1. 接続ドライバの例外にはホスト名などの接続情報が含まれ得るため、ログには例外クラス名と整数の errno のみを出力します。このため詳細な接続失敗理由の調査性とはトレードオフがあります。
2. Aurora の認証プラグインが `caching_sha2_password` の場合、PyMySQL は `cryptography` パッケージを要求する既知のリスクがあります。Aurora MySQL 3 のデフォルトは `mysql_native_password` のため、現時点では追加していません。
