# アーキテクチャ設計書

## 1. 全体アーキテクチャ

本システムは AWS マネージドサービスを中心に構成し、バッチ実行時のみリソースを起動するコスト効率の高い設計とする。

```
GitHub ──▶ CodePipeline ──▶ CodeBuild ──▶ ECR (Docker push)
                                              │
                                              ▼
                                    ECS Task Definition (新リビジョン登録)
                                              │
                                              ▼
EventBridge Scheduler ──▶ Step Functions ──▶ ECS Fargate RunTask
                                              │
                              ┌───────────────┼───────────────┐
                              ▼               ▼               ▼
                         External API       S3 Bucket    Aurora Serverless v2
                                                         (Secrets Manager)
                              │
                              ▼
                        CloudWatch Logs ──▶ CloudWatch Alarm ──▶ SNS Topic
```

## 2. ネットワーク構成

### VPC 設計

- **VPC**: 1 つの VPC を全サービスで共有
- **Public Subnet**: ECS Fargate タスクを配置（`assignPublicIp=ENABLED` でパブリック IP を自動付与し、Internet Gateway 経由で外部 API にアクセス）
- **Isolated Subnet**: Aurora Serverless v2 を配置（インターネットアクセス不要）
- **NAT Gateway**: 使用しない（コスト削減のため。ECS Fargate はパブリック IP で直接インターネットにアクセスする）
- **Security Group**: サービスごとにアクセスを制御

### 通信フロー

- ECS Fargate → 外部 API: パブリック IP + Internet Gateway 経由でインターネットアクセス
- ECS Fargate → Aurora: VPC 内部ルーティングによる通信（Public Subnet と Isolated Subnet 間は VPC 内で直接通信可能。Security Group で制御）
- ECS Fargate → S3: VPC Endpoint（Gateway 型）を利用（無料のため維持）
  - SNS 投稿バッチでは S3 Presigned URL を発行し、Instagram API に渡す
  - Presigned URL は S3 の標準エンドポイント URL で生成されるため、Instagram 側からインターネット経由でアクセス可能（VPC Endpoint の有無に影響されない）
- ECS Fargate → Secrets Manager: パブリック IP 経由でインターネットアクセス（コスト削減のため Interface 型 VPC Endpoint は使用しない）
- ECS Fargate → CloudWatch Logs: パブリック IP 経由でインターネットアクセス

## 3. コンピューティング

### ECS Fargate

- **ECS Cluster**: FoundationStack で 1 つ作成し、全バッチで共有
- **ECS Service**: 使用しない（バッチ用途のため RunTask のみ）
- **Task Definition**: サービスごとに作成
  - `image-batch-task`: 画像生成バッチ用
  - `sns-post-batch-task`: SNS 投稿バッチ用
  - 静的環境変数として `ENV_NAME`（例: `prod`）を設定し、Secrets Manager の Secret 名導出やログ出力に利用する

### Step Functions

- **ステートマシン**: バッチ種別ごとに 1 つ（image-generation-sfn, sns-posting-sfn）
- **入力パラメータ**: `set_code`, `scheduled_at` をスケジューラから受け取り、ECS タスクの環境変数として渡す
- **実行コンテキスト**: `$$.Execution.Id` を `EXECUTION_ARN` として ECS タスクへ渡し、`batch_execution_logs` の関連付けに利用する
- **実行モード**: Standard（長時間実行に対応）
- **同時実行数制限**: ステートマシンごとに同時実行数を 1 に制限する（`maxConcurrency: 1` 相当）。同一セットの手動実行とスケジュール実行が重なった場合の二重投稿リスクを防止する。同時実行数の上限に達した場合、後続の実行はキューイングされる
- **エラーハンドリング**: Retry / Catch を設定

### EventBridge Scheduler

- **スケジュール**: セットごと・バッチ種別ごとに cron 式で定義
- **ターゲット**: 対応する Step Functions ステートマシン（`set_code` と `scheduled_at` を入力に含める）
- **スケジュール管理**: スケジュール定義のマスタは IaC（CDK）とする。DB の `batch_schedules` テーブルには運用参照・バッチ自己診断用にスケジュール情報のコピーを保持する

## 4. データストア

### Aurora Serverless v2（MySQL 互換）

- **自動一時停止**: コスト最適化のため有効化
- **最小 ACU**: 0.5（一時停止時は 0）
- **最大 ACU**: 要件に応じて設定
- **接続**: Isolated Subnet に配置。VPC 内部ルーティングにより、同一 VPC 内の Public Subnet（ECS Fargate）からアクセス可能。インターネットからの直接アクセスは不可
- **認証情報**: Secrets Manager で管理

### S3

- **バケット**: 画像保存用に 1 つ作成
- **ライフサイクル**: 全オブジェクトを作成から 30 日で自動削除する Lifecycle Policy を設定する。SNS 投稿は通常数日以内に完了するため、30 日あれば十分なバッファとなる。これにより、DB 登録に失敗した S3 孤立ファイルも自動的にクリーンアップされる
- **アクセス**: VPC Endpoint（Gateway 型）経由（無料のため維持）

## 5. セキュリティ

### Secrets Manager

以下の秘密情報を管理する:

- Aurora DB の認証情報（ホスト、ポート、ユーザー名、パスワード、DB 名）
- 画像生成 API のキー
- SNS 認証情報: Secret 名は `acps/{env}/{set_code}/sns/{platform}/{account_code}` の規約に従う（`env` は `ENV_NAME`、現時点では `prod` 固定）

### IAM

- ECS タスクロール: S3、Secrets Manager（プレフィックス `acps/{env}/*` で制限）、CloudWatch Logs へのアクセス権限
- Step Functions 実行ロール: ECS RunTask の実行権限
- EventBridge Scheduler ロール: Step Functions の起動権限

## 6. ログ・監視

### CloudWatch Logs

- ECS タスクのログを CloudWatch Logs に出力
- ロググループはサービスごとに分離

### CloudWatch Alarm

- Step Functions ExecutionsFailed メトリクスで実行失敗を検知
- Aurora CPUUtilization / FreeableMemory メトリクスで異常を検知

### EventBridge Rule

- ECS Task State Change イベントでタスクの異常終了（exitCode != 0）を検知し、SNS Topic に通知する
- ECS タスク終了コードは CloudWatch 標準メトリクスに含まれないため、EventBridge で捕捉する

### SNS Topic

- アラーム発生時に通知（メール等）

## 7. デプロイ方式

1. GitHub へのプッシュにより CodePipeline が起動
2. CodeBuild で Docker イメージをビルド、ECR へ push
3. CodeBuild の post_build で新しい ECS タスク定義リビジョンを登録（`aws ecs register-task-definition`）
4. Step Functions はタスク定義をリビジョンなし ARN で参照しているため、自動的に最新リビジョンで Fargate タスクを起動する

- Blue/Green デプロイは採用しない
- ECS Service は使用しない
- バッチ用途に適したシンプルな構成とする

> **Task Definition の管理責任**: 初期版は CDK（ImageBatchStack / SnsPostBatchStack）で作成する。以降のイメージ更新時は CodeBuild が新 revision を登録する。CDK deploy でサービススタックを更新する場合はロール・環境変数等のインフラ変更に限定し、Task Definition の revision 管理は CI に一本化する。
