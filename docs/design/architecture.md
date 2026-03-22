# アーキテクチャ設計

本システムは AWS マネージドサービスを中心に構成し、バッチ実行時のみリソースを起動するコスト効率の高い設計とする。

## 1. 全体アーキテクチャ

```
GitHub ──▶ CodePipeline ──▶ CodeBuild ──▶ ECR (Docker push)
                                              │
                                              ▼
                                    ECS Task Definition (新リビジョン登録)
                                              │
                                              ▼
EventBridge Scheduler ──▶ Step Functions (image-generation-sfn)
                              │
                              ▼
                         ECS Fargate RunTask (DB 準備確認)
                              │  Aurora 接続確認、リトライ付き
                              ├──▶ Aurora Serverless v2
                              ├──▶ Secrets Manager (DB 認証情報)
                              │
                              ▼
                         ECS Fargate RunTask (画像生成バッチ)
                              │
                              ├──▶ External API (画像生成)
                              ├──▶ S3 Bucket (画像保存)
                              └──▶ Aurora Serverless v2
                              │
                              ▼  成功時
                         Step Functions (sns-posting-sfn)
                              │
                              ▼
                         ECS Fargate RunTask (DB 準備確認)
                              │  Aurora 接続確認、リトライ付き
                              │
                              ▼
                         ECS Fargate RunTask (SNS 投稿バッチ)
                              │
                              ├──▶ S3 Bucket (Presigned URL)
                              ├──▶ External API (Instagram)
                              └──▶ Aurora Serverless v2
                              │
                              ▼
                        CloudWatch Logs ──▶ CloudWatch Alarm ──▶ SNS Topic
```

## 2. ネットワーク構成

### VPC 設計

- **VPC**: 1 つの VPC を全サービスで共有（CDK デフォルトの 2 AZ 構成）
- **Public Subnet（各 AZ に 1 つ、計 2 つ）**: ECS Fargate タスクを配置（`assignPublicIp=ENABLED` でパブリック IP を自動付与し、Internet Gateway 経由で外部 API にアクセス）
- **Isolated Subnet（各 AZ に 1 つ、計 2 つ）**: Aurora Serverless v2 を配置（インターネットアクセス不要）
- **NAT Gateway**: 使用しない（コスト削減のため。ECS Fargate はパブリック IP で直接インターネットにアクセスする）

> **NAT Gateway への移行パス**: 将来的にセキュリティ要件の強化やトラフィック増加に伴い、ECS Fargate を Private Subnet に移動し NAT Gateway 経由の構成に変更可能。現時点ではコスト優先でパブリック IP 方式を採用する。

> **Security Group 運用上の注意**: ECS Fargate タスクが Public Subnet でパブリック IP を持つため、Security Group のインバウンドルールを全ポート拒否に維持することが不可欠である。Security Group の変更時は、意図しないインバウンド許可が追加されていないことを必ず確認すること。CDK でのリソース追加時にも、バッチ共通 Security Group のインバウンドルールが変更されないよう注意する。

### 通信フロー

- ECS Fargate → 外部 API: パブリック IP + Internet Gateway 経由でインターネットアクセス
- ECS Fargate → Aurora: VPC 内部ルーティングによる通信（Security Group で制御）
- ECS Fargate → S3: VPC Endpoint（Gateway 型）を利用（無料のため維持）
  - Presigned URL は S3 の標準エンドポイント URL で生成されるため、Instagram 側からインターネット経由でアクセス可能
- ECS Fargate → Secrets Manager: パブリック IP 経由（TLS 暗号化。詳細は [design/security.md](security.md) を参照）
- ECS Fargate → CloudWatch Logs: パブリック IP 経由でインターネットアクセス

## 3. コンピューティング

### ECS Fargate

- **ECS Cluster**: 1 つ作成し全バッチで共有
- **ECS Service**: 使用しない（バッチ用途のため RunTask のみ）
- **Task Definition**: サービスごとに作成（`db-readiness-check-task`, `image-batch-task`, `sns-post-batch-task`）
- **DB 準備確認**: Aurora Serverless v2 の自動一時停止からの再開に対応するため、ECS タスクで実装する（Lambda は VPC 内からパブリック IP が付与されず、NAT Gateway または VPC Endpoint（Interface 型）なしでは Secrets Manager にアクセスできないため）。詳細な仕様は [design/batch.md](batch.md) を参照

### Step Functions

- **ステートマシン**: バッチ種別ごとに 1 つ（image-generation-sfn, sns-posting-sfn）
- **DB 準備確認**: 各ワークフローの最初のステートとして実行
- **順次実行**: 画像生成 Step Functions の成功後に SNS 投稿 Step Functions を `StartExecution` で起動
- **子実行名**: image-generation-sfn から sns-posting-sfn を起動する際は、親の `$$.Execution.Name` を `StartExecution.Name` に渡し、同一要求の retry を冪等化する
- **入力パラメータ**: `set_code`, `scheduled_at` をスケジューラから受け取り、ECS タスクの環境変数として渡す
- **実行コンテキスト**: `$$.Execution.Id` を `EXECUTION_ARN` として ECS タスクへ渡す
- **実行モード**: Standard（長時間実行に対応）
- **タイムアウト**: 各 Task ステートに明示タイムアウトを設定し、ハング時にワークフローが長時間ぶら下がらないようにする（具体値は [specs/workflow.md](../specs/workflow.md) を参照）
- **同時実行に関する制約**: EventBridge Scheduler の実行間隔で回避し、万一の同時実行は DB の排他制御で整合性を保証する（詳細は [design/batch.md](batch.md) セクション 1.6 を参照）
- **エラーハンドリング**: Retry / Catch を設定（ASL 定義は [specs/workflow.md](../specs/workflow.md) を参照）
- **SNS 投稿の単独実行**: sns-posting-sfn は独立したステートマシンのため、手動での再投稿や投稿のみの実行も可能

### EventBridge Scheduler

- **スケジュール**: セットごとに cron 式で定義（画像生成 Step Functions のみをターゲット）
- **ターゲット**: 画像生成 Step Functions ステートマシン（`set_code` と `scheduled_at` を入力に含める）
- **スケジュール管理**: マスタは IaC（CDK）とする

## 4. データストア

### Aurora Serverless v2（MySQL 互換）

- **自動一時停止**: コスト最適化のため有効化
- **最小 ACU**: 0（自動一時停止対応バージョンを前提とする）
- **エンジン要件**: Aurora MySQL 3.08.0 以降など、0 ACU の自動一時停止をサポートするバージョンを採用する
- **接続**: Isolated Subnet に配置。VPC 内部ルーティングにより同一 VPC 内の ECS Fargate からアクセス可能
- **認証情報**: Secrets Manager で管理（詳細は [design/security.md](security.md) を参照）

### S3

- **バケット**: 画像保存用に 1 つ作成
- **ライフサイクル**: 全オブジェクトを作成から 30 日で自動削除（詳細は [specs/infrastructure.md](../specs/infrastructure.md) を参照）
- **アクセス**: VPC Endpoint（Gateway 型）経由

## 5. セキュリティ

認証・認可・秘密情報管理の方針は [design/security.md](security.md) を参照。

## 6. ログ・監視

- ECS タスクのログを CloudWatch Logs に出力（ロググループはサービスごとに分離）
- Step Functions 失敗、ECS タスク異常終了、Aurora 異常を監視し SNS Topic で通知
- 監視リソースの具体的なメトリクス名・しきい値は [specs/workflow.md](../specs/workflow.md) を参照

## 7. デプロイ方式

デプロイ方式の詳細は [design/cicd.md](cicd.md) を参照。

- Blue/Green デプロイは採用しない
- ECS Service は使用しない
- Docker イメージを ECR に push し、新しい ECS タスク定義リビジョンを登録する方式
