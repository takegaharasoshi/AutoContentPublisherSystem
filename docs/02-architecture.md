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
- ECS Fargate → Secrets Manager: VPC Endpoint（Interface 型）を利用

## 3. コンピューティング

### ECS Fargate

- **ECS Cluster**: FoundationStack で 1 つ作成し、全バッチで共有
- **ECS Service**: 使用しない（バッチ用途のため RunTask のみ）
- **Task Definition**: サービスごとに作成
  - `image-batch-task`: 画像生成バッチ用
  - `sns-post-batch-task`: SNS 投稿バッチ用

### Step Functions

- **ステートマシン**: サービスごとに作成
- **実行モード**: Standard（長時間実行に対応）
- **エラーハンドリング**: Retry / Catch を設定

### EventBridge Scheduler

- **スケジュール**: サービスごとに cron 式で定義
- **ターゲット**: 対応する Step Functions ステートマシン

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
- Instagram Graph API / Content Posting API の認証情報

### IAM

- ECS タスクロール: S3、Secrets Manager、CloudWatch Logs へのアクセス権限
- Step Functions 実行ロール: ECS RunTask の実行権限
- EventBridge Scheduler ロール: Step Functions の起動権限

## 6. ログ・監視

### CloudWatch Logs

- ECS タスクのログを CloudWatch Logs に出力
- ロググループはサービスごとに分離

### CloudWatch Alarm

- Step Functions の実行失敗を検知
- ECS タスクの異常終了を検知
- Aurora の異常を検知

### SNS Topic

- アラーム発生時に通知（メール等）

## 7. デプロイ方式

1. GitHub へのプッシュにより CodePipeline が起動
2. CodeBuild で Docker イメージをビルド、ECR へ push
3. 新しい ECS タスク定義リビジョンを登録
4. Step Functions は最新のタスク定義で Fargate タスクを起動

- Blue/Green デプロイは採用しない
- ECS Service は使用しない
- バッチ用途に適したシンプルな構成とする
