# インフラ実装設計

## 1. スタック分割方針

責務ごとに AWS CDK のスタックを分割する。

- **共通基盤**は FoundationStack で一元管理し、各バッチスタックから参照する
- **業務機能**はサービスごとにスタックを分離し、独立したデプロイ・保守を可能にする
- **監視・通知**は MonitoringStack として業務スタックから分離する

## 2. スタック一覧

| スタック | フェーズ | 責務 |
|---|---|---|
| FoundationStack | 初期 | 共通基盤リソース |
| ImageBatchStack | 初期 | 画像生成バッチ実行基盤 |
| SnsPostBatchStack | 初期 | SNS 投稿バッチ実行基盤 |
| MonitoringStack | 初期 | 監視・通知 |
| AdminApiStack | 将来 | 管理画面バックエンド API |
| AdminWebStack | 将来 | 管理画面フロントエンド |

## 3. スタック詳細

### 3.1 FoundationStack

**目的**: システム全体で共通利用する基盤リソースをまとめて管理する

**リソース一覧**:

| リソース | 説明 |
|---|---|
| VPC | 2 AZ 構成。Public Subnet x2（ECS Fargate 用）、Isolated Subnet x2（Aurora 用）。NAT Gateway なし |
| Security Group | サービスごとのアクセス制御（詳細は下表） |
| S3 Bucket | 画像保存用（Lifecycle Policy: 30 日で自動削除） |
| Aurora Serverless v2 | MySQL 互換 DB（自動一時停止有効、最小 ACU は 0。Aurora MySQL 3.08.0 以降など対応バージョンを採用） |
| Secrets Manager | DB 認証情報（CDK の Aurora コンストラクトで自動生成）、画像生成 API キー（CDK でシークレットの「箱」を作成し、値は AWS Console から手動設定）。SNS 認証情報は CDK 管理外で手動作成（手順は [design/operation.md](../design/operation.md) セクション 1.6 参照） |
| ECS Cluster | 全バッチ共通の実行基盤 |
| ECR Repository | サービスごとのコンテナイメージリポジトリ（image-batch、sns-post-batch、db-readiness-check の 3 つ） |
| VPC Endpoint | S3（Gateway）のみ |
| ECS Task Definition (DB 準備確認) | DB 準備確認用（db-readiness-check）。コンテナ名: `db-readiness-check`。最小構成（0.25 vCPU / 0.5 GB）。Public Subnet に配置し、両バッチスタックの Step Functions から共有される。コンテナイメージは CDK Context `dbReadinessCheckImageTag` で指定された不変タグを参照する |
| IAM Role (DB 準備確認タスク) | 権限詳細は [design/security.md](../design/security.md) を参照 |
| Security Group (DB 準備確認) | DB 準備確認 ECS タスク用 |
| CloudWatch Log Group (DB 準備確認) | DB 準備確認タスクのログ出力先（リテンション: 90 日） |

**Security Group ルール詳細**:

| Security Group | 方向 | プロトコル | ポート | ソース/宛先 | 用途 |
|---|---|---|---|---|---|
| ECS Fargate 用（バッチ共通） | Inbound | - | - | 全拒否 | バッチ処理のため着信不要 |
| 同上 | Outbound | TCP | 443 | 0.0.0.0/0 | 外部 API、Secrets Manager、CloudWatch Logs |
| 同上 | Outbound | TCP | 3306 | Aurora SG | Aurora への DB 接続 |
| DB 準備確認用 | Inbound | - | - | 全拒否 | バッチ処理のため着信不要 |
| 同上 | Outbound | TCP | 443 | 0.0.0.0/0 | Secrets Manager、CloudWatch Logs |
| 同上 | Outbound | TCP | 3306 | Aurora SG | Aurora への DB 接続確認 |
| Aurora 用 | Inbound | TCP | 3306 | ECS Fargate SG, DB 準備確認 SG | ECS タスクからの DB 接続を許可 |
| 同上 | Outbound | - | - | なし | アウトバウンド通信なし |

> **CDK 実装時の注意**: CDK はデフォルトで全アウトバウンドを許可する Security Group を作成する。Aurora 用 SG では `allowAllOutbound: false` を明示的に指定してアウトバウンドルールを削除すること。

> **設計方針**: ネットワークセキュリティの方針は [design/architecture.md](../design/architecture.md) セクション 2 および [design/security.md](../design/security.md) セクション 3 を参照。

**出力値（他スタックへの共有）**:

- VPC ID、Public Subnet ID x2、Isolated Subnet ID x2
- バッチ共通 Security Group ID
- S3 Bucket 名 / ARN
- Aurora Cluster Endpoint / ARN
- Secrets Manager Secret ARN（DB 認証情報用 `acps/{env}/db/*`、画像 API キー用 `acps/{env}/image/*`。SNS 認証情報は Secret 名規約によりアプリ側で導出するため出力不要。規約は [design/security.md](../design/security.md) を参照）
- ECS Cluster 名 / ARN
- ECR Repository URI（サービスごと + DB 準備確認用）
- DB 準備確認 ECS Task Definition family 名（リビジョンなし。Step Functions が常に最新リビジョンを使用するため）
- DB 準備確認用 Security Group ID

**注意事項**:

- DB 準備確認の仕様詳細は [design/batch.md](../design/batch.md) セクション 1.2 を参照
- db-readiness-check の更新時は `cdk deploy -c env=prod -c dbReadinessCheckImageTag=<tag> FoundationStack` で新しいイメージタグを明示的に渡す
- 将来の AdminApiStack、AdminWebStack からも参照される

### 3.2 ImageBatchStack

**目的**: 画像生成バッチの実行基盤を構築する

**リソース一覧**:

| リソース | 説明 |
|---|---|
| ECS Task Definition | 画像生成バッチ用コンテナ定義（0.25 vCPU / 0.5 GB。実運用で調整）。Task Definition 全体の SSOT は CDK とし、CI/CD は latest ACTIVE revision をベースに image URI だけを差し替えて新 revision を登録する（詳細は [design/cicd.md](../design/cicd.md) を参照） |
| Container Definition | コンテナ名: `image-batch`。ECR イメージ、環境変数、ログ設定 |
| Step Functions | ワークフロー定義（ASL は [specs/workflow.md](workflow.md) を参照） |
| EventBridge Scheduler | セットごとの定期実行スケジュール |
| CodePipeline | image-batch 用 CI/CD パイプライン（詳細は [design/cicd.md](../design/cicd.md) を参照） |
| CodeBuild | Docker ビルド・ECR push・タスク定義更新 |
| IAM Role | 権限詳細は [design/security.md](../design/security.md) を参照 |
| CloudWatch Log Group | タスクログ出力先（リテンション: 90 日） |

**依存スタック**: FoundationStack、SnsPostBatchStack（SNS 投稿 Step Functions の ARN を参照するため）

### 3.3 SnsPostBatchStack

**目的**: SNS 投稿バッチの実行基盤を構築する

**リソース一覧**:

| リソース | 説明 |
|---|---|
| ECS Task Definition | SNS 投稿バッチ用コンテナ定義（0.25 vCPU / 0.5 GB。実運用で調整）。Task Definition 全体の SSOT は CDK とし、CI/CD は latest ACTIVE revision をベースに image URI だけを差し替えて新 revision を登録する |
| Container Definition | コンテナ名: `sns-post-batch`。ECR イメージ、環境変数、ログ設定 |
| Step Functions | ワークフロー定義（ASL は [specs/workflow.md](workflow.md) を参照） |
| CodePipeline | sns-post-batch 用 CI/CD パイプライン（詳細は [design/cicd.md](../design/cicd.md) を参照） |
| CodeBuild | Docker ビルド・ECR push・タスク定義更新 |
| IAM Role | 権限詳細は [design/security.md](../design/security.md) を参照 |
| CloudWatch Log Group | タスクログ出力先（リテンション: 90 日） |

> **注記**: SnsPostBatchStack には EventBridge Scheduler を含めない。SNS 投稿バッチは画像生成 Step Functions の成功後に自動起動される。

**依存スタック**: FoundationStack

### 3.4 MonitoringStack

**目的**: バッチ全体の監視と通知をまとめて管理する

**リソース一覧**:

| リソース | 説明 |
|---|---|
| CloudWatch Alarm | 監視リソースの詳細は [specs/workflow.md](workflow.md) セクション 6 を参照 |
| EventBridge Rule | ECS Task State Change 検知。詳細は [specs/workflow.md](workflow.md) セクション 7 を参照 |
| SNS Topic | アラーム・イベント通知先 |
| CloudWatch Dashboard | 運用可視化（必要に応じて） |

**依存スタック**: FoundationStack、ImageBatchStack、SnsPostBatchStack

**注意事項**:

- 過剰通知を避けるため、必要なアラームから段階的に設定する

### 3.5 AdminApiStack（将来拡張）

**目的**: 管理画面から利用するバックエンド API を提供する

**想定リソース**: ECS Service または Lambda、ALB または API Gateway、IAM Role

**依存スタック**: FoundationStack

### 3.6 AdminWebStack（将来拡張）

**目的**: 管理画面のフロントエンドを提供する

**想定リソース**: S3（静的ファイル配信）、CloudFront、Route 53、ACM

**連携先**: AdminApiStack

## 4. デプロイ順序

```
1. FoundationStack        ← 共通基盤を先に作成
    │
    ├── 2. SnsPostBatchStack  ← 共通基盤を利用（ImageBatchStack より先にデプロイ）
    │
    ├── 3. ImageBatchStack    ← 共通基盤 + SnsPostBatchStack の Step Functions ARN を参照
    │
    ├── 4. MonitoringStack    ← 各スタックのメトリクスを監視
    │
    ├── 5. AdminApiStack      （将来）← 共通基盤を利用
    │
    └── 6. AdminWebStack      （将来）← AdminApiStack と連携
```

> **デプロイ方法**: 上記 1〜4 のスタックは開発者が `cdk diff` で差分確認後、`cdk deploy` で手動デプロイする。インフラパイプラインは構築しない（詳細は [design/cicd.md](../design/cicd.md) を参照）。

## 5. スタック間のデータ受け渡し

CDK の `CfnOutput` / `Fn.importValue` または コンストラクタ引数を用いて、スタック間でリソース情報を受け渡す。

```
FoundationStack
  ├── vpc              → ImageBatchStack, SnsPostBatchStack
  ├── securityGroup    → ImageBatchStack, SnsPostBatchStack
  ├── s3Bucket         → ImageBatchStack, SnsPostBatchStack
  ├── auroraCluster    → ImageBatchStack, SnsPostBatchStack
  ├── secretsArn       → ImageBatchStack, SnsPostBatchStack
  ├── ecsCluster       → ImageBatchStack, SnsPostBatchStack
  └── dbReadinessCheckTaskDefFamily → ImageBatchStack, SnsPostBatchStack

SnsPostBatchStack
  └── snsPostingSfnArn → ImageBatchStack（画像生成完了後の SNS 投稿 Step Functions 起動用）
```
