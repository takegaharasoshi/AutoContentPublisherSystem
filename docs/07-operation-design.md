# 運用設計書

## 1. バッチ運用

### 1.1 スケジュール管理

- EventBridge Scheduler で cron 式により定期実行する
- スケジュールはバッチセットごとに個別設定可能とする
- スケジュール定義のマスタは IaC（CDK）とする。EventBridge Scheduler の cron 式は CDK コードで定義し、`cdk deploy` で反映する
- DB の `batch_schedules` テーブルには運用参照用にスケジュール情報のコピーを保持する
  - バッチ自己診断（「自分は何時に実行されるはずか」の確認）に利用
  - `schedule_expression`: cron 式または rate 式
  - `timezone`: タイムゾーン（デフォルト: Asia/Tokyo）
  - `is_enabled`: 有効/無効フラグ
  - DB のみ変更してもスケジュールは変更されない。必ず CDK デプロイが必要

#### スケジュール変更手順

1. CDK コードの EventBridge Scheduler の cron 式を変更する
2. `cdk deploy` で EventBridge Scheduler を更新する
3. DB の `batch_schedules` テーブルの `schedule_expression` を手動で更新する（運用参照の整合性維持）

> **注意**: DB の `batch_schedules` を変更しても実際のスケジュールは変わらない。CDK デプロイが必須。

### 1.2 バッチ実行時の動作

1. EventBridge Scheduler が Step Functions を起動
2. Step Functions が ECS Fargate RunTask を実行
3. タスク完了後、Fargate タスクは自動的に停止（課金終了）
4. ECS Service は使用しないため、常駐プロセスは存在しない

### 1.3 プロンプト管理

- 画像生成に使用するプロンプトは DB（`prompt_configs` テーブル）で管理する
- プロンプトの追加・変更は DB 操作で行う（将来的には管理画面から操作）
- `is_active` フラグにより、使用するプロンプトを制御する

## 2. データベース運用

### 2.1 Aurora Serverless v2 の自動一時停止

- コスト最適化のため、自動一時停止を有効にする
- 一時停止中にアクセスがあると自動的に再開する
- 再開には数十秒〜数分かかる場合がある

### 2.2 DB 接続リトライ

- バッチ開始時に DB 接続を試行する
- 接続失敗時は指数バックオフでリトライする（最大 5 回、2〜32 秒間隔）
- リトライ超過時はタスク失敗とし、Step Functions の Catch で処理する

### 2.3 バックアップ

- Aurora のスナップショットによるバックアップ（自動バックアップ有効）
- 保持期間は要件に応じて設定

## 3. エラーハンドリング

### 3.1 Step Functions レベル

| エラー種別 | 対応 |
|---|---|
| ECS タスク起動失敗 | Retry（最大 2 回、30 秒間隔） |
| ECS タスク異常終了 | Retry → Catch → Fail ステートへ遷移 |
| タイムアウト | Catch → Fail ステートへ遷移 |

### 3.2 アプリケーションレベル

| エラー種別 | 対応 |
|---|---|
| DB 接続失敗 | 指数バックオフリトライ |
| 外部 API 失敗（画像生成） | ログ出力後、終了コード 1 で終了 → Step Functions Retry。再実行時は DB レコード有無で冪等性を確保 |
| 外部 API 失敗（SNS 投稿） | pending レコードの status を failed に更新、処理続行（画像単位で個別ハンドリング）。全件失敗時は終了コード 1。次回バッチ実行で再試行される（`batch_sets.max_post_retries` の上限まで）。上限超過した組はスキップされログに警告を出力する。手動で再試行する場合は新しい `pending` レコード（`attempt_number` インクリメント）を挿入する |
| S3 操作失敗 | ログ出力後、終了コード 1 で終了 → Step Functions Retry |
| 想定外エラー | ログ出力後、終了コード 1 で終了 → Step Functions Catch |

## 4. 監視・通知

### 4.1 監視方式

| 監視対象 | 実装方式 | 条件 |
|---|---|---|
| Step Functions 失敗 | CloudWatch Alarm（標準メトリクス `ExecutionsFailed`） | >= 1 |
| ECS タスク異常終了 | EventBridge Rule（ECS Task State Change イベント）→ SNS Topic | `exitCode != 0` または異常停止 |
| Aurora 異常 | CloudWatch Alarm（標準メトリクス `CPUUtilization` / `FreeableMemory`） | 閾値超過 |

> **ECS タスク異常終了の監視について**: ECS タスクの終了コードは CloudWatch の標準メトリクスとして提供されないため、CloudWatch Alarm では直接監視できない。代わりに EventBridge Rule で ECS Task State Change イベント（`detail.stoppedReason` / `detail.containers[].exitCode` でフィルタ）を捕捉し、SNS Topic に通知する。Step Functions の `ExecutionsFailed` は標準メトリクスであり CloudWatch Alarm で直接設定可能。

### 4.2 通知先

- SNS Topic 経由でメール通知
- 将来的には Slack 連携等も検討

### 4.3 ダッシュボード

- CloudWatch Dashboard でバッチ実行状況を可視化（必要に応じて段階的に構築）

## 5. コスト最適化

| リソース | 最適化方針 |
|---|---|
| ECS Fargate | バッチ実行時のみ起動、タスク完了後に自動停止 |
| Aurora Serverless v2 | 自動一時停止を有効化、最小 ACU を低く設定 |
| NAT Gateway | 利用量に応じてコストを監視 |
| S3 | ライフサイクルルールで古いデータを整理（必要に応じて） |

## 6. セキュリティ運用

- API キー・DB 認証情報は Secrets Manager で管理し、定期的なローテーションを検討する
- ECS タスクには最小権限の IAM ロールを付与する
- VPC 内のプライベートサブネットで DB・タスクを実行する
- セキュリティグループで不要な通信を遮断する
