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
- **Public Subnet**: NAT Gateway 配置用（外部 API 通信のため）
- **Private Subnet**: ECS Fargate タスク、Aurora Serverless v2 を配置
- **Security Group**: サービスごとにアクセスを制御

### 通信フロー

- ECS Fargate → 外部 API: NAT Gateway 経由でインターネットアクセス
- ECS Fargate → Aurora: Private Subnet 内の VPC 内通信
- ECS Fargate → S3: VPC Endpoint（Gateway 型）を利用
  - SNS 投稿バッチでは S3 Presigned URL を発行し、Instagram API に渡す
  - Presigned URL は S3 の標準エンドポイント URL で生成されるため、Instagram 側からインターネット経由でアクセス可能（VPC Endpoint の有無に影響されない）
- ECS Fargate → Secrets Manager: VPC Endpoint（Interface 型）を利用

## 3. コンピューティング

### ECS Fargate

- **ECS Cluster**: FoundationStack で 1 つ作成し、全バッチで共有
- **ECS Service**: 使用しない（バッチ用途のため RunTask のみ）
- **Task Definition**: サービスごとに作成
  - `image-batch-task`: 画像生成バッチ用
  - `sns-post-batch-task`: SNS 投稿バッチ用

### Step Functions

- **ステートマシン**: バッチ種別ごとに 1 つ（image-generation-sfn, sns-posting-sfn）
- **入力パラメータ**: `set_id`, `scheduled_at` をスケジューラから受け取り、ECS タスクの環境変数として渡す
- **実行モード**: Standard（長時間実行に対応）
- **エラーハンドリング**: Retry / Catch を設定

### EventBridge Scheduler

- **スケジュール**: セットごと・バッチ種別ごとに cron 式で定義
- **ターゲット**: 対応する Step Functions ステートマシン（`set_id` と `scheduled_at` を入力に含める）
- **スケジュール管理**: スケジュール定義のマスタは IaC（CDK）とする。DB の `batch_schedules` テーブルには運用参照・バッチ自己診断用にスケジュール情報のコピーを保持する

## 4. データストア

### Aurora Serverless v2（MySQL 互換）

- **自動一時停止**: コスト最適化のため有効化
- **最小 ACU**: 0.5（一時停止時は 0）
- **最大 ACU**: 要件に応じて設定
- **接続**: Private Subnet 内からのみアクセス可能
- **認証情報**: Secrets Manager で管理

### S3

- **バケット**: 画像保存用に 1 つ作成
- **ライフサイクル**: 必要に応じて設定
- **アクセス**: VPC Endpoint 経由

## 5. セキュリティ

### Secrets Manager

以下の秘密情報を管理する:

- Aurora DB の認証情報（ホスト、ポート、ユーザー名、パスワード、DB 名）
- 画像生成 API のキー
- SNS 認証情報: Secret 名は `acps/{set_id}/sns/{platform}/{account_code}` の規約に従う

### IAM

- ECS タスクロール: S3、Secrets Manager（プレフィックス `acps/*` で制限）、CloudWatch Logs へのアクセス権限
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
