# 運用設計

## 1. バッチ運用

### 1.1 スケジュール管理

- EventBridge Scheduler で cron 式により画像生成 Step Functions を定期実行する
- SNS 投稿バッチは画像生成 Step Functions の成功後に自動起動されるため、SNS 投稿用の EventBridge Scheduler は不要
- スケジュールはバッチセットごとに個別設定可能とする
- スケジュール定義のマスタは IaC（CDK）とする

#### スケジュール変更手順

1. CDK コードの EventBridge Scheduler の cron 式を変更する
2. `cdk deploy -c env=prod ImageBatchStack` で EventBridge Scheduler を更新する

### 1.2 バッチ実行時の動作

1. EventBridge Scheduler が画像生成 Step Functions（image-generation-sfn）を起動
2. Step Functions が DB 準備確認 ECS タスクを実行（WaitForDbReady ステート）
3. DB 準備完了後、Step Functions が画像生成 ECS Fargate RunTask を実行
4. 画像生成タスク成功後、Step Functions が SNS 投稿 Step Functions（sns-posting-sfn）を `StartExecution` で起動
5. SNS 投稿 Step Functions が DB 準備確認 ECS タスクを実行
6. DB 準備完了後、SNS 投稿 Step Functions が SNS 投稿 ECS Fargate RunTask を実行
7. 各タスク完了後、Fargate タスクは自動的に停止（課金終了）

> **手動での SNS 投稿実行**: SNS 投稿の再実行や単独実行が必要な場合は、AWS Console や CLI から sns-posting-sfn を直接起動する（`set_code` を入力パラメータとして渡す）。
>
> ```bash
> # CLI での手動実行例
> aws stepfunctions start-execution \
>   --state-machine-arn arn:aws:states:ap-northeast-1:123456789012:stateMachine:acps-prod-sns-posting-sfn \
>   --input '{"set_code": "fashion-set-1"}'
> ```

### 1.3 プロンプト管理

- 画像生成に使用するプロンプトは DB（`prompt_configs` テーブル）で管理する
- プロンプトの追加・変更は DB 操作で行う（将来的には管理画面から操作）
- `is_active` フラグにより、使用するプロンプトを制御する
- 同一セットで `is_active=1` の `prompt_configs` は、1 回の画像生成バッチ実行で全件を順次処理する

### 1.4 実行ログ管理

- 各バッチは開始時に `batch_execution_logs` へ `running` レコードを登録し、終了時に `succeeded` または `failed` に更新する
- `execution_arn` には Step Functions 実行 ARN を保存し、CloudWatch Logs と突合できるようにする
- `running` のまま残ったレコードは stale とみなし、Step Functions 実行履歴と CloudWatch Logs を確認して `failed` へ補正する

### 1.5 CDK デプロイ後チェックリスト

CDK デプロイ実行後は、以下のチェックリストを確認する。

- [ ] **ImageBatchStack に変更があった場合**: latest ACTIVE revision に期待するロール、環境変数、ログ設定が反映されていることを確認する
- [ ] **SnsPostBatchStack に変更があった場合**: latest ACTIVE revision に期待するロール、環境変数、ログ設定が反映されていることを確認する
- [ ] **db-readiness-check を更新した場合**: `cdk deploy -c env=prod -c dbReadinessCheckImageTag=<tag> FoundationStack` を使用し、latest ACTIVE revision が該当タグを参照していることを確認する
- [ ] **新規セット追加の場合**: DB に `batch_sets` レコードを追加する
- [ ] **デプロイ結果の確認**: AWS Console で各リソースの状態が正常であることを確認する

### 1.6 SNS アカウント追加手順

SNS アカウントを追加する際は、Secrets Manager のシークレット作成を DB レコード追加より先に行うこと。

#### 手順

1. **Secrets Manager にシークレットを作成する**
   - Secret 名規約は [design/security.md](security.md) を参照
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
- 最小 ACU は 0 とし、0 ACU の自動一時停止をサポートする Aurora MySQL バージョンを採用する
- 一時停止中にアクセスがあると自動的に再開する（再開には数十秒〜数分）

### 2.2 DB 準備確認

- 各 Step Functions ワークフローの最初のステートとして DB 準備確認 ECS タスクを実行する
- 仕様の詳細は [design/batch.md](batch.md) セクション 1.2 を参照

### 2.3 DDL マイグレーション方針

- 初期構築時および運用中のスキーマ変更は、手動で DDL を実行する（AWS Console の Query Editor または MySQL CLI を使用）
- DDL ファイルはリポジトリ内で管理する（`services/db-readiness-check/sql/` 等に配置し、バージョン番号付きで命名。例: `V001__create_tables.sql`）
- 変更時は新しい DDL ファイルを追加し、適用済みバージョンを把握できるようにする
- 将来的に管理画面の導入やスキーマ変更頻度の増加に伴い、Alembic 等のマイグレーションツールの採用を検討する

### 2.4 テーブル肥大化の監視

- `post_records` テーブルは再試行のたびにレコードが追加される設計のため、長期運用でレコード数が増加する
- 現時点では対策不要。パフォーマンスへの影響が観測された場合に、アーカイブテーブルへの移行やパーティショニングを検討する

### 2.5 バックアップ

- Aurora のスナップショットによるバックアップ（自動バックアップ有効）
- 保持期間: 7 日間（Aurora のデフォルト値。運用状況に応じて調整する）

## 3. エラーハンドリング（運用対応）

### 3.1 Step Functions レベル

Step Functions の Retry/Catch 設定の詳細は [specs/workflow.md](../specs/workflow.md) を参照。

| エラー種別 | 運用対応 |
|---|---|
| ECS タスク起動失敗（Retry 超過） | CloudWatch Logs を確認し原因を調査。必要に応じて手動再実行 |
| ECS タスク異常終了（Retry 超過） | CloudWatch Logs でエラー内容を確認。アプリケーションのバグの場合は修正してデプロイ |
| タイムアウト | バッチ処理の処理時間を確認し、タイムアウト値の調整を検討 |

### 3.2 アプリケーションレベル

エラーハンドリングのアプリ実装詳細は [design/batch.md](batch.md) を参照。

| エラー種別 | 運用対応 |
|---|---|
| DB 接続失敗（WaitForDbReady 後） | Aurora の状態を確認。長時間の DB 停止の場合は AWS Console で手動再開 |
| 外部 API 失敗（画像生成） | API サービスの障害状況を確認。復旧後に手動再実行 |
| 外部 API 失敗（SNS 投稿） | `post_records` の `status='failed'` を確認。次回バッチ実行で自動再試行される（上限まで）。上限超過の場合は原因調査の上、手動で再試行 |
| S3 操作失敗 | S3 バケットの状態と IAM 権限を確認 |

## 4. 監視・通知

### 4.1 監視方式

監視リソースの具体的なメトリクス名・しきい値は [specs/workflow.md](../specs/workflow.md) セクション 6〜7 を参照。

| 監視対象 | 通知が来たらやること |
|---|---|
| Step Functions 失敗 | CloudWatch Logs で失敗原因を確認。一時的なエラーであれば手動再実行 |
| SNS 投稿起動失敗 | カスタムメトリクスで検知。手動で sns-posting-sfn を起動する |
| ECS タスク異常終了 | CloudWatch Logs でエラー内容を確認。アプリケーションのバグの場合は修正してデプロイ |
| Aurora 異常 | Aurora の状態を AWS Console で確認。ACU 設定の見直しを検討 |

### 4.2 通知先

- SNS Topic 経由でメール通知
- 将来的には Slack 連携等も検討

#### SNS Topic サブスクリプション設定手順

1. MonitoringStack のデプロイ後、AWS Console で SNS Topic を開く
2. 「サブスクリプションの作成」からプロトコル「Email」を選択し、通知先メールアドレスを入力する
3. 入力したメールアドレスに確認メールが届くので、メール内のリンクをクリックして承認する
4. サブスクリプションのステータスが「確認済み」になったことを確認する

> **注意**: サブスクリプションの承認を行わないと通知が届かない。MonitoringStack デプロイ後は必ず承認を完了すること。

### 4.3 ダッシュボード

- CloudWatch Dashboard でバッチ実行状況を可視化（必要に応じて段階的に構築）

## 5. コスト最適化

| リソース | 最適化方針 |
|---|---|
| ECS Fargate | バッチ実行時のみ起動、タスク完了後に自動停止 |
| Aurora Serverless v2 | 自動一時停止を有効化、最小 ACU を低く設定 |
| ネットワーク | NAT Gateway は使用しない。ECS Fargate にパブリック IP を付与して直接インターネットアクセス |
| S3 | Lifecycle Policy で全オブジェクトを 30 日で自動削除 |
| CloudWatch Logs | リテンション期間を設定し、不要なログの蓄積を防止する（初期開発では未設定。運用開始後にコスト状況を見て設定を検討する） |

## 6. セキュリティ運用

セキュリティ設計の詳細は [design/security.md](security.md) を参照。
