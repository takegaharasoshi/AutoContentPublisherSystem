# セキュリティ設計

## 1. Secrets Manager 管理方針

### 1.1 管理対象

以下の秘密情報を Secrets Manager で管理する:

- Aurora DB の認証情報（ホスト、ポート、ユーザー名、パスワード、DB 名）
- 画像生成 API のキー
- SNS 認証情報（プラットフォームごとの API 認証情報）

### 1.2 Secret 名規約

すべての Secret は `acps/{env}/` プレフィックスで始まる。種別ごとの命名規約:

| 種別 | Secret 名パターン | 例 |
|---|---|---|
| DB 認証情報 | `acps/{env}/db/credentials` | `acps/prod/db/credentials` |
| 画像生成 API キー | `acps/{env}/image/api-key` | `acps/prod/image/api-key` |
| SNS 認証情報 | `acps/{env}/{set_code}/sns/{platform}/{account_code}` | `acps/prod/fashion-set-1/sns/instagram/main-account` |

SNS 認証情報の Secret 名の詳細規約:

```
acps/{env}/{set_code}/sns/{platform}/{account_code}
```

| 要素 | 説明 | 例 |
|---|---|---|
| `env` | 環境識別子（ECS タスクの `ENV_NAME` 環境変数） | `prod` |
| `set_code` | バッチセット識別コード（`batch_sets.set_code`） | `fashion-set-1` |
| `platform` | SNS プラットフォーム名（`sns_accounts.platform`） | `instagram` |
| `account_code` | アカウント識別コード（`sns_accounts.account_code`、不変） | `main-account` |

例: `acps/prod/fashion-set-1/sns/instagram/main-account`

- Secret 名はアプリケーション側で上記規約に基づき導出する（DB に Secret 名・ARN は保持しない）
- `account_code` は Secret 名の導出に使用するため、作成後に変更してはならない
- 環境分離は `env` 部分で行い、IAM ポリシーのプレフィックスベース制御と整合する

> **設計理由**: 従来の `credentials_secret_arn` カラム方式では、DB にアカウントを追加するたびに IAM ポリシーの個別 ARN 追加が必要だった。Secret 名規約に統一することで、プレフィックスベースの IAM ポリシーで最小権限と運用の簡便さを両立する。

### 1.3 将来の複数環境対応

| リソース | 命名規約 | 例（本番） | 例（開発） |
|---|---|---|---|
| Secrets Manager | `acps/{env}/...` | `acps/prod/db/credentials` | `acps/dev/db/credentials` |

- 現時点の単一環境でも `env=prod` を付与して運用する
- ECS Task Definition には `ENV_NAME` を環境変数として注入し、アプリケーションが Secret 名を導出できるようにする

## 2. IAM ロール設計

### 2.1 ECS タスクロール

| ロール | 権限 |
|---|---|
| DB 準備確認タスクロール | Secrets Manager 読み取り（`acps/{env}/db/*`） |
| 画像生成バッチタスクロール | S3 読み書き、Secrets Manager 読み取り（`acps/{env}/db/*` + `acps/{env}/image/*`） |
| SNS 投稿バッチタスクロール | S3 読み取り、Secrets Manager 読み取り（`acps/{env}/db/*` + `acps/{env}/*/sns/*`） |

- Secrets Manager 権限はサービスごとに必要最小限のプレフィックスで制限する。DB 認証情報（`acps/{env}/db/*`）は全サービス共通、それ以外は各サービスが必要とする種別のみ付与する
- DB にアカウントを追加するだけで、IAM ポリシーの変更なしに新しい Secret へのアクセスが可能になる

### 2.2 ECS タスク実行ロール

- ECR イメージの pull 権限
- CloudWatch Logs への書き込み権限

> **注記**: CloudWatch Logs への書き込みは ECS Fargate の awslogs ドライバがタスク実行ロールの権限で行う。タスクロール（セクション 2.1）には CloudWatch Logs 権限を含めない。

### 2.3 Step Functions 実行ロール

| ステートマシン | 権限 |
|---|---|
| image-generation-sfn | ECS RunTask（DB 準備確認タスク + 画像生成バッチタスク）、`iam:PassRole`（ECS RunTask 時にタスクロール・タスク実行ロールを渡すため）、SNS 投稿 Step Functions の `StartExecution`、CloudWatch `PutMetricData`（カスタムメトリクス発行用。詳細は下記注記を参照） |
| sns-posting-sfn | ECS RunTask（DB 準備確認タスク + SNS 投稿バッチタスク）、`iam:PassRole`（ECS RunTask 時にタスクロール・タスク実行ロールを渡すため） |

> **`cloudwatch:PutMetricData` の IAM 条件**: `PutMetricData` API はリソース ARN をサポートしていないため、ステートメントの `Resource` は `"*"` にせざるを得ない。過剰権限化を避けるため、条件キー `cloudwatch:namespace` で発行可能な Namespace を `ACPS`（本システムのカスタムメトリクス Namespace）に制限する。例:
>
> ```json
> {
>   "Effect": "Allow",
>   "Action": "cloudwatch:PutMetricData",
>   "Resource": "*",
>   "Condition": {
>     "StringEquals": { "cloudwatch:namespace": "ACPS" }
>   }
> }
> ```

### 2.4 EventBridge Scheduler ロール

- 画像生成 Step Functions の起動権限（`states:StartExecution`）

### 2.5 CI/CD サービスロール

#### CodeBuild サービスロール

| パイプライン | 権限 |
|---|---|
| image-batch-pipeline / sns-post-batch-pipeline | ECR 認証トークン取得（`ecr:GetAuthorizationToken`）、対象 ECR リポジトリへのイメージ push（`ecr:PutImage` 等）、ECS タスク定義の読み取り・登録（`ecs:DescribeTaskDefinition`、`ecs:RegisterTaskDefinition`）、ECS タスク実行ロールおよびタスクロールの `iam:PassRole`、CloudWatch Logs 書き込み（ビルドログ出力用） |

- 各パイプラインの CodeBuild プロジェクトに対し、操作対象のリソース（ECR リポジトリ、ECS タスク定義 family、IAM ロール）を最小限にスコープする
- `iam:PassRole` は、CodeBuild が `ecs:RegisterTaskDefinition` で新リビジョンを登録する際にタスクロールとタスク実行ロールを指定するために必要

#### CodePipeline サービスロール

| パイプライン | 権限 |
|---|---|
| image-batch-pipeline / sns-post-batch-pipeline | CodeStar Connections の使用（`codestar-connections:UseConnection`）、CodeBuild プロジェクトの起動（`codebuild:StartBuild`、`codebuild:BatchGetBuilds` 等）、S3 アーティファクトバケットの読み書き（`s3:GetObject`、`s3:PutObject` 等） |

- CodePipeline が Source Stage で GitHub からソースを取得し、Build Stage で CodeBuild を起動するために必要な最小権限
- S3 アーティファクトバケットは CodePipeline が使用する中間ストレージ（CDK がデフォルトで作成）

## 3. ネットワークセキュリティ

- **Aurora**: Isolated Subnet に配置し、インターネットからの直接アクセスを遮断する。Security Group はアウトバウンド通信を完全に遮断する（CDK で `allowAllOutbound: false` を明示指定）
- **ECS Fargate**: Public Subnet に配置し、Security Group でアクセスを制御する
  - インバウンド: 全ポート拒否（バッチ処理であり外部からの着信接続は不要）
  - アウトバウンド: インターネットアクセス（外部 API、Secrets Manager、CloudWatch Logs）と VPC 内通信（Aurora）を許可
- **Secrets Manager**: ECS Fargate のパブリック IP 経由でアクセス（通信は TLS で暗号化）
  - Interface VPC Endpoint は使用しない（コスト削減のため。より厳格なネットワーク分離が必要な場合は導入を検討）

> **NAT Gateway への移行パス**: セキュリティ要件の強化やトラフィック増加時には、ECS Fargate を Private Subnet に移動し NAT Gateway 経由の構成に変更可能。

## 4. セキュリティ運用

- API キー・DB 認証情報は定期的なローテーションを検討する
- ECS タスクには最小権限の IAM ロールを付与する
- Secrets Manager 権限はサービスごとに最小プレフィックスで制限し、環境およびサービスを跨いだ参照を避ける
- Security Group で不要な通信を遮断する
