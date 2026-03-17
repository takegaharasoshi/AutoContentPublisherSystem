# CDK スタック設計書

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
| VPC | Public Subnet（ECS Fargate 用）、Isolated Subnet（Aurora 用）。NAT Gateway なし |
| Security Group | サービスごとのアクセス制御 |
| S3 Bucket | 画像保存用（Lifecycle Policy: 30 日で自動削除） |
| Aurora Serverless v2 | MySQL 互換 DB（自動一時停止有効） |
| Secrets Manager | DB 認証情報、API キー |
| ECS Cluster | 全バッチ共通の実行基盤 |
| ECR Repository | サービスごとのコンテナイメージリポジトリ（image-batch、sns-post-batch） |
| VPC Endpoint | S3（Gateway）のみ。Secrets Manager へは ECS Fargate / Lambda のパブリック IP 経由でアクセス |
| Lambda Function | DB 準備確認用（db-readiness-check）。VPC 内（Public Subnet）に配置し、Aurora への接続確認を行う。Python ランタイム。両バッチスタックの Step Functions から共有される |
| IAM Role (Lambda) | Lambda 実行ロール: VPC アクセス（AWSLambdaVPCAccessExecutionRole 相当）、Secrets Manager 読み取り（DB 認証情報）、CloudWatch Logs |
| Security Group (Lambda) | DB 準備確認 Lambda 用。Aurora SG へのインバウンドを許可するための送信元として使用 |

**出力値（他スタックへの共有）**:

- VPC ID、Subnet ID
- Security Group ID
- S3 Bucket 名 / ARN
- Aurora Cluster Endpoint / ARN
- Secrets Manager Secret ARN（DB 認証情報・API キー用。SNS 認証情報は Secret 名規約によりアプリ側で導出するため出力不要）
- ECS Cluster 名 / ARN
- ECR Repository URI（サービスごと）
- DB 準備確認 Lambda 関数 ARN（両バッチスタックの Step Functions から参照）

**注意事項**:

- Aurora Serverless v2 の自動再開待ちに対応するため、FoundationStack に DB 準備確認 Lambda を配置する。各 Step Functions ワークフローはこの Lambda をワークフローの最初のステートで実行し、DB 準備完了を確認してから ECS タスクを起動する。Lambda 内部で最大 5 回のリトライ（指数バックオフ: 2, 4, 8, 16, 32 秒）を行う
- 将来の AdminApiStack、AdminWebStack からも参照される

### 3.2 ImageBatchStack

**目的**: 画像生成バッチの実行基盤を構築する

**リソース一覧**:

| リソース | 説明 |
|---|---|
| ECS Task Definition | 画像生成バッチ用コンテナ定義（初期版の作成のみ。以降の revision 更新は CI/CD パイプラインの CodeBuild が行う） |
| Container Definition | ECR イメージ、環境変数（`ENV_NAME=prod` など）、ログ設定 |
| Step Functions | ワークフロー定義（**最初のステートとして DB 準備確認 Lambda（WaitForDbReady）を実行し**、その後 ECS RunTask を実行。Retry/Catch 付き、タスク定義はリビジョンなし ARN で参照。CodeBuild が新 revision を登録すれば自動的に最新が使われる。**同時実行数制限: 1**。画像生成 ECS タスク成功後に SNS 投稿 Step Functions を `StartExecution` で起動する） |
| EventBridge Scheduler | セットごとの定期実行スケジュール（`set_code` と `scheduled_at`（`<aws.scheduler.scheduled-time>` から取得）を入力パラメータとして渡す）。SNS 投稿は画像生成完了後に自動起動されるため、本スケジューラのみで両バッチを順次実行する |
| IAM Role | タスクロール、実行ロール。Step Functions 実行ロールには SNS 投稿 Step Functions の `StartExecution` 権限および DB 準備確認 Lambda の Invoke 権限を追加する |
| CloudWatch Log Group | タスクログ出力先 |

**依存スタック**: FoundationStack、SnsPostBatchStack（SNS 投稿 Step Functions の ARN を参照するため）

**処理フロー**:

> ※ DB 準備確認は Step Functions の WaitForDbReady ステート（Lambda）で完了済み。バッチ開始時点で DB は利用可能。

1. DB からプロンプト情報を取得
2. 画像生成 API を呼び出し
3. 生成画像を S3 に JPEG 形式で保存
4. メタ情報を DB に登録
5. 成功時: SNS 投稿 Step Functions を起動（`set_code` を引き継ぐ）

### 3.3 SnsPostBatchStack

**目的**: SNS 投稿バッチの実行基盤を構築する

**リソース一覧**:

| リソース | 説明 |
|---|---|
| ECS Task Definition | SNS 投稿バッチ用コンテナ定義（初期版の作成のみ。以降の revision 更新は CI/CD パイプラインの CodeBuild が行う） |
| Container Definition | ECR イメージ、環境変数（`ENV_NAME=prod` など）、ログ設定 |
| Step Functions | ワークフロー定義（**最初のステートとして DB 準備確認 Lambda（WaitForDbReady）を実行し**、その後 ECS RunTask を実行。Retry/Catch 付き、タスク定義はリビジョンなし ARN で参照。CodeBuild が新 revision を登録すれば自動的に最新が使われる。**同時実行数制限: 1**）。画像生成 Step Functions から呼び出されるほか、手動での単独実行も可能 |
| IAM Role | タスクロール、実行ロール。Step Functions 実行ロールには DB 準備確認 Lambda の Invoke 権限を追加する |
| CloudWatch Log Group | タスクログ出力先 |

> **注記**: SnsPostBatchStack には EventBridge Scheduler を含めない。SNS 投稿バッチは画像生成 Step Functions の成功後に自動起動される。手動での再投稿が必要な場合は、AWS Console や CLI から sns-posting-sfn を直接起動する。

**依存スタック**: FoundationStack

**処理フロー**:

> ※ DB 準備確認は Step Functions の WaitForDbReady ステート（Lambda）で完了済み。バッチ開始時点で DB は利用可能。

1. DB から投稿対象を取得
2. S3 Presigned URL を発行
3. Instagram Graph API に Presigned URL を渡して投稿
4. 投稿結果を DB に記録

**注意事項**:

- 重複投稿防止の仕組みを考慮する
- 投稿結果の履歴管理を行う
- SNS API の認証情報は Secret 名規約 `acps/{env}/{set_code}/sns/{platform}/{account_code}` に基づきアプリ側で導出し、Secrets Manager から取得する。`env` は CDK Context から設定される `ENV_NAME`（現時点では `prod`）とする。ECS タスクロールには `arn:aws:secretsmanager:*:*:secret:acps/{env}/*` のプレフィックスベースで Secrets Manager の読み取り権限を付与する

### 3.4 MonitoringStack

**目的**: バッチ全体の監視と通知をまとめて管理する

**リソース一覧**:

| リソース | 説明 |
|---|---|
| CloudWatch Alarm | Step Functions ExecutionsFailed、Aurora CPUUtilization / FreeableMemory |
| EventBridge Rule | ECS Task State Change（異常終了検知）→ SNS Topic に通知 |
| SNS Topic | アラーム・イベント通知先 |
| CloudWatch Dashboard | 運用可視化（必要に応じて） |

> **注記**: ECS 異常終了の検知は CloudWatch Alarm ではなく EventBridge Rule で実装する。ECS タスク終了コードは CloudWatch 標準メトリクスに含まれないため。

**依存スタック**: FoundationStack、ImageBatchStack、SnsPostBatchStack

**注意事項**:

- 過剰通知を避けるため、必要なアラームから段階的に設定する

### 3.5 AdminApiStack（将来拡張）

**目的**: 管理画面から利用するバックエンド API を提供する

**想定リソース**:

- ECS Service または Lambda
- ALB または API Gateway
- IAM Role

**依存スタック**: FoundationStack

### 3.6 AdminWebStack（将来拡張）

**目的**: 管理画面のフロントエンドを提供する

**想定リソース**:

- S3（静的ファイル配信）
- CloudFront
- Route 53
- ACM

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

> **デプロイ方法**: 上記 1〜4 のスタックは開発者が `cdk diff` で差分確認後、`cdk deploy` で手動デプロイする。インフラパイプラインは構築しない（Aurora・VPC 等の破壊的変更リスクを考慮）。詳細は CI/CD 設計書（`docs/06-cicd-design.md`）を参照。

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
  └── dbReadinessCheckLambdaArn → ImageBatchStack, SnsPostBatchStack

SnsPostBatchStack
  └── snsPostingSfnArn → ImageBatchStack（画像生成完了後の SNS 投稿 Step Functions 起動用）
```
