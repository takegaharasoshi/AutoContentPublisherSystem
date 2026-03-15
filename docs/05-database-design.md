# データベース設計書

## 1. 設計方針

- Aurora Serverless v2（MySQL 互換）を使用する
- 将来の複数セット運用を前提に、`set_id` でデータを識別可能にする
- 設定値・プロンプト・投稿先・実行履歴をすべて DB で管理する

## 2. テーブル一覧

| テーブル名 | 説明 |
|---|---|
| batch_sets | バッチセットの定義（画像生成＋SNS 投稿の 1 組） |
| prompt_configs | 画像生成に使用するプロンプト設定 |
| generated_images | 生成された画像のメタ情報 |
| sns_accounts | SNS 投稿先アカウント情報 |
| post_records | SNS 投稿の実行履歴 |
| batch_execution_logs | バッチ実行ログ |
| batch_schedules | バッチスケジュール設定 |

## 3. テーブル定義

### 3.1 batch_sets（バッチセット）

バッチセットの定義を管理する。1 セット = 画像生成バッチ + SNS 投稿バッチの組み合わせ。

| カラム名 | 型 | NULL | デフォルト | 説明 |
|---|---|---|---|---|
| id | BIGINT UNSIGNED | NO | AUTO_INCREMENT | 主キー |
| set_code | VARCHAR(50) | NO | | セット識別コード（一意） |
| name | VARCHAR(200) | NO | | セット名称 |
| description | TEXT | YES | NULL | 説明 |
| is_active | TINYINT(1) | NO | 1 | 有効フラグ |
| max_post_retries | INT UNSIGNED | NO | 3 | SNS 投稿の最大再試行回数 |
| created_at | DATETIME | NO | CURRENT_TIMESTAMP | 作成日時（UTC） |
| updated_at | DATETIME | NO | CURRENT_TIMESTAMP ON UPDATE | 更新日時（UTC） |

- **PK**: `id`
- **UNIQUE**: `set_code`

### 3.2 prompt_configs（プロンプト設定）

画像生成に使用するプロンプトの設定を管理する。

| カラム名 | 型 | NULL | デフォルト | 説明 |
|---|---|---|---|---|
| id | BIGINT UNSIGNED | NO | AUTO_INCREMENT | 主キー |
| set_id | BIGINT UNSIGNED | NO | | バッチセット ID（FK） |
| prompt_text | TEXT | NO | | プロンプト本文 |
| negative_prompt | TEXT | YES | NULL | ネガティブプロンプト |
| parameters | JSON | YES | NULL | 生成パラメータ（サイズ、品質等） |
| is_active | TINYINT(1) | NO | 1 | 有効フラグ |
| created_at | DATETIME | NO | CURRENT_TIMESTAMP | 作成日時（UTC） |
| updated_at | DATETIME | NO | CURRENT_TIMESTAMP ON UPDATE | 更新日時（UTC） |

- **PK**: `id`
- **FK**: `set_id` → `batch_sets.id`
- **INDEX**: `idx_prompt_configs_set_id` (`set_id`)

### 3.3 generated_images（生成画像）

生成された画像のメタ情報を管理する。

| カラム名 | 型 | NULL | デフォルト | 説明 |
|---|---|---|---|---|
| id | BIGINT UNSIGNED | NO | AUTO_INCREMENT | 主キー |
| set_id | BIGINT UNSIGNED | NO | | バッチセット ID（FK） |
| prompt_config_id | BIGINT UNSIGNED | NO | | 使用プロンプト設定 ID（FK） |
| scheduled_at | DATETIME | NO | | スケジュール実行日時（UTC、冪等性キー） |
| s3_key | VARCHAR(500) | NO | | S3 オブジェクトキー |
| s3_bucket | VARCHAR(200) | NO | | S3 バケット名 |
| file_format | VARCHAR(20) | NO | 'jpg' | ファイル形式（Instagram 要件により jpg を標準とする） |
| file_size_bytes | BIGINT UNSIGNED | YES | NULL | ファイルサイズ（バイト） |
| width | INT UNSIGNED | YES | NULL | 画像幅（ピクセル） |
| height | INT UNSIGNED | YES | NULL | 画像高さ（ピクセル） |
| generation_api_response | JSON | YES | NULL | API レスポンス（参考用） |
| generated_at | DATETIME | NO | CURRENT_TIMESTAMP | 生成日時（UTC） |
| created_at | DATETIME | NO | CURRENT_TIMESTAMP | 作成日時（UTC） |
| updated_at | DATETIME | NO | CURRENT_TIMESTAMP ON UPDATE | 更新日時（UTC） |

- **PK**: `id`
- **FK**: `set_id` → `batch_sets.id`
- **FK**: `prompt_config_id` → `prompt_configs.id`
- **INDEX**: `idx_generated_images_set_id` (`set_id`)
- **UNIQUE**: `uq_generated_images_idempotency` (`set_id`, `prompt_config_id`, `scheduled_at`)

> **注記**: 投稿ステータスは `post_records` テーブルから導出する。`generated_images` テーブルには投稿状態を持たない。

> **設計変更理由**: `scheduled_at` カラム（DATETIME 型）を追加し、(`set_id`, `prompt_config_id`, `scheduled_at`) の UNIQUE 制約で冪等性を保証する。同一スケジュール実行枠の同一プロンプトに対する二重生成を DB レベルで防止でき、Step Functions のリトライ時にも安全に再実行可能。DATETIME 型を採用することで、日次だけでなくサブ日次スケジュール（1 日複数回実行）にも対応する。

### 3.4 sns_accounts（SNS アカウント）

SNS 投稿先のアカウント情報を管理する。

| カラム名 | 型 | NULL | デフォルト | 説明 |
|---|---|---|---|---|
| id | BIGINT UNSIGNED | NO | AUTO_INCREMENT | 主キー |
| set_id | BIGINT UNSIGNED | NO | | バッチセット ID（FK） |
| platform | VARCHAR(50) | NO | | プラットフォーム（instagram 等） |
| account_code | VARCHAR(50) | NO | | アカウント識別コード（不変、Secret 名導出に使用） |
| account_name | VARCHAR(200) | NO | | アカウント表示名 |
| is_active | TINYINT(1) | NO | 1 | 有効フラグ |
| created_at | DATETIME | NO | CURRENT_TIMESTAMP | 作成日時（UTC） |
| updated_at | DATETIME | NO | CURRENT_TIMESTAMP ON UPDATE | 更新日時（UTC） |

- **PK**: `id`
- **FK**: `set_id` → `batch_sets.id`
- **INDEX**: `idx_sns_accounts_set_id` (`set_id`)
- **UNIQUE**: `uq_sns_accounts_set_platform_code` (`set_id`, `platform`, `account_code`)

> **認証情報の管理方針**: SNS 認証情報の Secret 名はテーブルに保持せず、アプリケーション側で `acps/{set_id}/sns/{platform}/{account_code}` の規約に基づき導出する。これにより IAM ポリシーでプレフィックス `acps/*` ベースの最小権限を維持しつつ、DB へのアカウント追加だけで新しい Secret へのアクセスが可能になる。

> **設計変更理由（Secret 名規約）**: 従来の `credentials_secret_arn` カラム（任意の ARN を格納）では、DB にアカウントを追加しても ECS タスクロールの IAM ポリシーが追随せず、wildcard 権限か個別 ARN の手動追加が必要だった。Secret 名規約に統一することで、プレフィックスベースの IAM ポリシー（`arn:aws:secretsmanager:*:*:secret:acps/*`）で最小権限と運用の簡便さを両立する。

> **設計変更理由（account_code）**: Secret 名の導出に `account_name`（表示名）を使用すると、表示名の変更時に Secrets Manager の Secret 名と不整合が生じる。不変の `account_code` を導入し Secret 名導出に使用することで、`account_name` を安全に変更可能にする。`account_code` は作成時に設定し変更不可とする。

### 3.5 post_records（投稿履歴）

SNS 投稿の実行結果を管理する。再試行のたびにレコードを追加し、`status='success'` のレコードの有無で投稿完了を判断する（success が 1 件でもあれば投稿済みと見なす）。

| カラム名 | 型 | NULL | デフォルト | 説明 |
|---|---|---|---|---|
| id | BIGINT UNSIGNED | NO | AUTO_INCREMENT | 主キー |
| generated_image_id | BIGINT UNSIGNED | NO | | 投稿画像 ID（FK） |
| sns_account_id | BIGINT UNSIGNED | NO | | 投稿先アカウント ID（FK） |
| attempt_number | INT UNSIGNED | NO | 1 | 試行回数（同一 image + account の何回目か） |
| status | ENUM('pending', 'success', 'failed') | NO | | 投稿結果 |
| platform_container_id | VARCHAR(200) | YES | NULL | プラットフォーム側のコンテナ/事前登録 ID（Instagram の creation_id 等） |
| platform_post_id | VARCHAR(200) | YES | NULL | プラットフォーム側の投稿 ID |
| error_message | TEXT | YES | NULL | エラーメッセージ |
| api_response | JSON | YES | NULL | API レスポンス（参考用） |
| posted_at | DATETIME | YES | NULL | 投稿日時（UTC） |
| created_at | DATETIME | NO | CURRENT_TIMESTAMP | 作成日時 |

- **PK**: `id`
- **FK**: `generated_image_id` → `generated_images.id`
- **FK**: `sns_account_id` → `sns_accounts.id`
- **INDEX**: `idx_post_records_image_account` (`generated_image_id`, `sns_account_id`)
- **INDEX**: `idx_post_records_status` (`status`)
- **INDEX**: `idx_post_records_image_account_status` (`generated_image_id`, `sns_account_id`, `status`) — 投稿完了判定用

> **設計変更理由**: UNIQUE 制約 `(generated_image_id, sns_account_id)` を廃止した。複数アカウントへの投稿で「A に成功、B に失敗」を表現でき、再試行履歴を自然に蓄積できるようにするため。`pending` ステータスは投稿予約（API 呼び出し前の冪等性確保）に使用する。

> **再試行の仕組み**: 再試行は新規レコード（`attempt_number` インクリメント）で管理する。`failed` レコードは履歴として保持され、次回バッチ実行時に `status='success'` が存在しなければ新しい `pending` レコードが作成される。`attempt_number` が `batch_sets.max_post_retries`（デフォルト: 3）以上の場合はスキップされ、ログに警告が出力される。

> **排他制御**: 並行実行による二重投稿を防止するため、投稿対象の判定と `pending` レコード挿入はトランザクション内で `SELECT ... FOR UPDATE` を使用する。`(generated_image_id, sns_account_id)` の既存レコードをロックした上で `status='success'` の有無を確認し、存在しなければ `pending` を挿入する。

> **二重投稿防止の強化**: Instagram Graph API の 2 段階フロー（コンテナ作成 → パブリッシュ）に対応し、`platform_container_id` で中間状態を永続化する。再実行時は `platform_container_id` と `platform_post_id` の組み合わせで復旧ポイントを判定する。将来の他プラットフォーム対応では、`platform_container_id` をプラットフォーム固有の「事前登録 ID」として汎用的に使用する。

### 3.6 batch_execution_logs（バッチ実行ログ）

バッチの実行履歴を管理する。

| カラム名 | 型 | NULL | デフォルト | 説明 |
|---|---|---|---|---|
| id | BIGINT UNSIGNED | NO | AUTO_INCREMENT | 主キー |
| set_id | BIGINT UNSIGNED | NO | | バッチセット ID（FK） |
| batch_type | ENUM('image_generation', 'sns_posting') | NO | | バッチ種別 |
| execution_arn | VARCHAR(500) | YES | NULL | Step Functions 実行 ARN |
| status | ENUM('running', 'succeeded', 'failed') | NO | | 実行結果 |
| started_at | DATETIME | NO | | 開始日時（UTC） |
| finished_at | DATETIME | YES | NULL | 終了日時（UTC） |
| error_message | TEXT | YES | NULL | エラーメッセージ |
| records_processed | INT UNSIGNED | YES | NULL | 処理件数 |
| created_at | DATETIME | NO | CURRENT_TIMESTAMP | 作成日時 |

- **PK**: `id`
- **FK**: `set_id` → `batch_sets.id`
- **INDEX**: `idx_batch_execution_logs_set_type` (`set_id`, `batch_type`)
- **INDEX**: `idx_batch_execution_logs_status` (`status`)

### 3.7 batch_schedules（バッチスケジュール設定）

各バッチセットの実行スケジュール情報を保持する（運用参照・バッチ自己診断用）。スケジュール定義のマスタは IaC（CDK の EventBridge Scheduler）であり、本テーブルはそのコピーを格納する。

| カラム名 | 型 | NULL | デフォルト | 説明 |
|---|---|---|---|---|
| id | BIGINT UNSIGNED | NO | AUTO_INCREMENT | 主キー |
| set_id | BIGINT UNSIGNED | NO | | バッチセット ID（FK） |
| batch_type | ENUM('image_generation', 'sns_posting') | NO | | バッチ種別 |
| schedule_expression | VARCHAR(200) | NO | | cron/rate 式（例: cron(0 9 * * ? *)） |
| timezone | VARCHAR(100) | NO | 'Asia/Tokyo' | タイムゾーン |
| is_enabled | TINYINT(1) | NO | 1 | スケジュール有効フラグ |
| description | VARCHAR(500) | YES | NULL | 説明 |
| created_at | DATETIME | NO | CURRENT_TIMESTAMP | 作成日時（UTC） |
| updated_at | DATETIME | NO | CURRENT_TIMESTAMP ON UPDATE | 更新日時（UTC） |

- **PK**: `id`
- **FK**: `set_id` → `batch_sets.id`
- **UNIQUE**: `uq_batch_schedules_set_type` (`set_id`, `batch_type`)
- **INDEX**: `idx_batch_schedules_enabled` (`is_enabled`)

> **設計変更理由**: スケジュール定義のマスタを IaC（CDK）に一元化した。DB → EventBridge Scheduler への自動同期機構は構築せず、CDK デプロイ後に手動で DB を更新する運用とする。将来の管理画面導入時に同期機構を検討する。

## 4. ER 図（概要）

```
batch_sets (1) ─── (N) prompt_configs
     │
     ├── (1) ─── (N) generated_images ─── (N) post_records
     │                                          │
     ├── (1) ─── (N) sns_accounts ──────────────┘
     │
     ├── (1) ─── (N) batch_execution_logs
     │
     └── (1) ─── (N) batch_schedules
```

> **注記**: `generated_images` の投稿ステータスは `post_records` から導出する（`generated_images` テーブルに `post_status` カラムは持たない）。

## 5. 時刻の取り扱い方針

- DB の全 DATETIME カラムは **UTC で保存する**
- MySQL の DATETIME 型はタイムゾーン情報を持たないため、アプリケーション側で UTC に変換してから格納する責務を負う
- EventBridge Scheduler の `<aws.scheduler.scheduled-time>` は UTC（ISO 8601 の `Z` 接尾辞）で渡されるため、`Z` を除いた値をそのまま DATETIME カラムに格納する
- `batch_schedules.timezone` はユーザー向け表示・運用参照用であり、DB 保存値の変換には使用しない
- 表示時のタイムゾーン変換（UTC → Asia/Tokyo 等）はアプリケーション層の責務とする
- 冪等性キーの比較・UNIQUE 制約の判定もすべて UTC ベースで行う

## 6. 文字コード・照合順序

- 文字コード: `utf8mb4`
- 照合順序: `utf8mb4_unicode_ci`
