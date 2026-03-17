# 運用設計書

## 1. バッチ運用

### 1.1 スケジュール管理

- EventBridge Scheduler で cron 式により画像生成 Step Functions を定期実行する
- SNS 投稿バッチは画像生成 Step Functions の成功後に自動起動されるため、SNS 投稿用の EventBridge Scheduler は不要
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

1. EventBridge Scheduler が画像生成 Step Functions（image-generation-sfn）を起動
2. Step Functions が DB 準備確認 Lambda を実行（WaitForDbReady ステート）
3. DB 準備完了後、Step Functions が画像生成 ECS Fargate RunTask を実行
4. 画像生成タスク成功後、Step Functions が SNS 投稿 Step Functions（sns-posting-sfn）を `StartExecution` で起動
5. SNS 投稿 Step Functions が DB 準備確認 Lambda を実行（WaitForDbReady ステート）
6. DB 準備完了後、SNS 投稿 Step Functions が SNS 投稿 ECS Fargate RunTask を実行
7. 各タスク完了後、Fargate タスクは自動的に停止（課金終了）
8. ECS Service は使用しないため、常駐プロセスは存在しない

> **手動での SNS 投稿実行**: SNS 投稿の再実行や単独実行が必要な場合は、AWS Console や CLI から sns-posting-sfn を直接起動する（`set_code` を入力パラメータとして渡す）。

### 1.3 プロンプト管理

- 画像生成に使用するプロンプトは DB（`prompt_configs` テーブル）で管理する
- プロンプトの追加・変更は DB 操作で行う（将来的には管理画面から操作）
- `is_active` フラグにより、使用するプロンプトを制御する

### 1.4 実行ログ管理

- 各バッチは開始時に `batch_execution_logs` へ `running` レコードを登録し、終了時に `succeeded` または `failed` に更新する
- `execution_arn` には Step Functions 実行 ARN を保存し、CloudWatch Logs と突合できるようにする
- 手動 RunTask で起動した場合は `execution_arn` を `NULL` として扱ってよい
- `running` のまま残ったレコードは stale とみなし、Step Functions 実行履歴と CloudWatch Logs を確認して `failed` へ補正する

### 1.5 CDK デプロイ後チェックリスト

CDK デプロイ実行後は、以下のチェックリストを確認する。

- [ ] **スケジュール変更があった場合**: DB の `batch_schedules` テーブルの `schedule_expression` を手動更新する
- [ ] **ImageBatchStack に変更があった場合**: `image-batch-pipeline` を手動実行する（タスク定義の revision 整合性維持のため。詳細は `docs/06-cicd-design.md` セクション 6 を参照）
- [ ] **SnsPostBatchStack に変更があった場合**: `sns-post-batch-pipeline` を手動実行する（同上）
- [ ] **新規セット追加の場合**: DB に `batch_sets`、`batch_schedules` レコードを追加する
- [ ] **デプロイ結果の確認**: AWS Console で各リソースの状態が正常であることを確認する

### 1.6 SNS アカウント追加手順

SNS アカウントを追加する際は、Secrets Manager のシークレット作成を DB レコード追加より先に行うこと。シークレットが存在しない状態で DB にレコードを追加すると、バッチ実行時にランタイムエラーとなる。

#### 手順

1. **Secrets Manager にシークレットを作成する**
   - Secret 名: `acps/{env}/{set_code}/sns/{platform}/{account_code}`
   - 例: `acps/prod/fashion-set-1/sns/instagram/main-account`
   - シークレット値には各プラットフォームの API 認証情報を格納する
2. **DB の `sns_accounts` テーブルにレコードを追加する**
   - `set_id`: 対象バッチセットの ID
   - `platform`: プラットフォーム名（例: `instagram`）
   - `account_code`: シークレット名と一致するコード（**作成後の変更不可**）
   - `is_active`: 1（有効）
3. **動作確認**: バッチを手動実行し、シークレット取得が成功することを確認する

> **注意**: `account_code` はシークレット名の導出に使用するため、作成後に変更してはならない。変更が必要な場合は、新しいシークレットとレコードを作成し、旧レコードを `is_active=0` に設定する。

## 2. データベース運用

### 2.1 Aurora Serverless v2 の自動一時停止

- コスト最適化のため、自動一時停止を有効にする
- 一時停止中にアクセスがあると自動的に再開する
- 再開には数十秒〜数分かかる場合がある

### 2.2 DB 準備確認

- 各 Step Functions ワークフローの最初のステートとして DB 準備確認 Lambda を実行する
- Lambda 内で DB 接続を試行し、接続失敗時は指数バックオフでリトライする（最大 5 回、2〜32 秒間隔）
- Lambda のリトライ超過時は例外を送出し、Step Functions の Retry/Catch でハンドリングする
- バッチアプリケーション（ECS タスク）は DB が利用可能な状態を前提とする（アプリケーション内の DB 接続リトライは不要）

> **設計変更理由**: DB 準備確認の責務をバッチアプリケーションから Step Functions ワークフロー（Lambda）に移動した。これによりバッチアプリケーションがシンプルになり、DB 準備確認ロジックの共通化が実現される。

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
| DB 接続失敗 | Step Functions の WaitForDbReady ステート（Lambda）で事前確認済み。ECS タスク実行中に DB 接続が切れた場合はログ出力後、終了コード 1 で終了 → Step Functions Retry |
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
| ネットワーク | NAT Gateway は使用しない。ECS Fargate にパブリック IP を付与して直接インターネットアクセスする構成とし、固定費を削減 |
| S3 | Lifecycle Policy で全オブジェクトを作成から 30 日で自動削除。孤立ファイルのクリーンアップも兼ねる |

## 6. セキュリティ運用

- API キー・DB 認証情報は Secrets Manager で管理し、定期的なローテーションを検討する
- SNS 認証情報の Secret 名は `acps/{env}/{set_code}/sns/{platform}/{account_code}` の規約で管理する（現時点の `env` は `prod`）
- ECS タスクロールの Secrets Manager 権限は `acps/{env}/*` プレフィックスに制限し、環境を跨いだ参照を避ける
- ECS タスクには最小権限の IAM ロールを付与する
- Aurora は Isolated Subnet に配置しインターネットからの直接アクセスを遮断する。ECS Fargate は Public Subnet に配置し、Security Group でアウトバウンドを制御する
- セキュリティグループで不要な通信を遮断する
