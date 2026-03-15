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
| VPC | Private/Public Subnet、NAT Gateway |
| Security Group | サービスごとのアクセス制御 |
| S3 Bucket | 画像保存用 |
| Aurora Serverless v2 | MySQL 互換 DB（自動一時停止有効） |
| Secrets Manager | DB 認証情報、API キー |
| ECS Cluster | 全バッチ共通の実行基盤 |
| VPC Endpoint | S3（Gateway）、Secrets Manager（Interface） |

**出力値（他スタックへの共有）**:

- VPC ID、Subnet ID
- Security Group ID
- S3 Bucket 名 / ARN
- Aurora Cluster Endpoint / ARN
- Secrets Manager Secret ARN
- ECS Cluster 名 / ARN

**注意事項**:

- Aurora Serverless v2 の自動再開待ちが発生しうるため、利用側で接続確認とリトライを考慮する
- 将来の AdminApiStack、AdminWebStack からも参照される

### 3.2 ImageBatchStack

**目的**: 画像生成バッチの実行基盤を構築する

**リソース一覧**:

| リソース | 説明 |
|---|---|
| ECS Task Definition | 画像生成バッチ用コンテナ定義 |
| Container Definition | ECR イメージ、環境変数、ログ設定 |
| Step Functions | ワークフロー定義（Retry/Catch 付き） |
| EventBridge Scheduler | 定期実行スケジュール |
| IAM Role | タスクロール、実行ロール |
| CloudWatch Log Group | タスクログ出力先 |

**依存スタック**: FoundationStack

**処理フロー**:

1. DB 接続確認（リトライ付き）
2. DB からプロンプト情報を取得
3. 画像生成 API を呼び出し
4. 生成画像を S3 に保存
5. メタ情報を DB に登録

### 3.3 SnsPostBatchStack

**目的**: SNS 投稿バッチの実行基盤を構築する

**リソース一覧**:

| リソース | 説明 |
|---|---|
| ECS Task Definition | SNS 投稿バッチ用コンテナ定義 |
| Container Definition | ECR イメージ、環境変数、ログ設定 |
| Step Functions | ワークフロー定義（Retry/Catch 付き） |
| EventBridge Scheduler | 定期実行スケジュール |
| IAM Role | タスクロール、実行ロール |
| CloudWatch Log Group | タスクログ出力先 |

**依存スタック**: FoundationStack

**処理フロー**:

1. DB 接続確認（リトライ付き）
2. DB から投稿対象を取得
3. S3 から画像を取得
4. SNS API（Instagram Graph API / Content Posting API）で投稿
5. 投稿結果を DB に記録

**注意事項**:

- 重複投稿防止の仕組みを考慮する
- 投稿結果の履歴管理を行う

### 3.4 MonitoringStack

**目的**: バッチ全体の監視と通知をまとめて管理する

**リソース一覧**:

| リソース | 説明 |
|---|---|
| CloudWatch Alarm | Step Functions 失敗、ECS 異常終了、Aurora 異常 |
| SNS Topic | アラーム通知先 |
| CloudWatch Dashboard | 運用可視化（必要に応じて） |

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
    ├── 2. ImageBatchStack    ← 共通基盤を利用
    │
    ├── 3. SnsPostBatchStack  ← 共通基盤を利用
    │
    └── 4. MonitoringStack    ← 各スタックのメトリクスを監視
              │
              ├── 5. AdminApiStack    （将来）
              │
              └── 6. AdminWebStack    （将来）
```

## 5. スタック間のデータ受け渡し

CDK の `CfnOutput` / `Fn.importValue` または コンストラクタ引数を用いて、スタック間でリソース情報を受け渡す。

```
FoundationStack
  ├── vpc              → ImageBatchStack, SnsPostBatchStack
  ├── securityGroup    → ImageBatchStack, SnsPostBatchStack
  ├── s3Bucket         → ImageBatchStack, SnsPostBatchStack
  ├── auroraCluster    → ImageBatchStack, SnsPostBatchStack
  ├── secretsArn       → ImageBatchStack, SnsPostBatchStack
  └── ecsCluster       → ImageBatchStack, SnsPostBatchStack
```
