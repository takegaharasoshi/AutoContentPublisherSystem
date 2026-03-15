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
| created_at | DATETIME | NO | CURRENT_TIMESTAMP | 作成日時 |
| updated_at | DATETIME | NO | CURRENT_TIMESTAMP ON UPDATE | 更新日時 |

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
| created_at | DATETIME | NO | CURRENT_TIMESTAMP | 作成日時 |
| updated_at | DATETIME | NO | CURRENT_TIMESTAMP ON UPDATE | 更新日時 |

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
| s3_key | VARCHAR(500) | NO | | S3 オブジェクトキー |
| s3_bucket | VARCHAR(200) | NO | | S3 バケット名 |
| file_format | VARCHAR(20) | NO | | ファイル形式（png, jpg 等） |
| file_size_bytes | BIGINT UNSIGNED | YES | NULL | ファイルサイズ（バイト） |
| width | INT UNSIGNED | YES | NULL | 画像幅（ピクセル） |
| height | INT UNSIGNED | YES | NULL | 画像高さ（ピクセル） |
| generation_api_response | JSON | YES | NULL | API レスポンス（参考用） |
| post_status | ENUM('unposted', 'posted', 'failed', 'skipped') | NO | 'unposted' | 投稿ステータス |
| generated_at | DATETIME | NO | CURRENT_TIMESTAMP | 生成日時 |
| created_at | DATETIME | NO | CURRENT_TIMESTAMP | 作成日時 |
| updated_at | DATETIME | NO | CURRENT_TIMESTAMP ON UPDATE | 更新日時 |

- **PK**: `id`
- **FK**: `set_id` → `batch_sets.id`
- **FK**: `prompt_config_id` → `prompt_configs.id`
- **INDEX**: `idx_generated_images_set_id` (`set_id`)
- **INDEX**: `idx_generated_images_post_status` (`post_status`)
- **INDEX**: `idx_generated_images_set_status` (`set_id`, `post_status`)

### 3.4 sns_accounts（SNS アカウント）

SNS 投稿先のアカウント情報を管理する。

| カラム名 | 型 | NULL | デフォルト | 説明 |
|---|---|---|---|---|
| id | BIGINT UNSIGNED | NO | AUTO_INCREMENT | 主キー |
| set_id | BIGINT UNSIGNED | NO | | バッチセット ID（FK） |
| platform | VARCHAR(50) | NO | | プラットフォーム（instagram 等） |
| account_name | VARCHAR(200) | NO | | アカウント名 |
| credentials_secret_arn | VARCHAR(500) | NO | | 認証情報の Secrets Manager ARN |
| is_active | TINYINT(1) | NO | 1 | 有効フラグ |
| created_at | DATETIME | NO | CURRENT_TIMESTAMP | 作成日時 |
| updated_at | DATETIME | NO | CURRENT_TIMESTAMP ON UPDATE | 更新日時 |

- **PK**: `id`
- **FK**: `set_id` → `batch_sets.id`
- **INDEX**: `idx_sns_accounts_set_id` (`set_id`)

### 3.5 post_records（投稿履歴）

SNS 投稿の実行結果を管理する。

| カラム名 | 型 | NULL | デフォルト | 説明 |
|---|---|---|---|---|
| id | BIGINT UNSIGNED | NO | AUTO_INCREMENT | 主キー |
| generated_image_id | BIGINT UNSIGNED | NO | | 投稿画像 ID（FK） |
| sns_account_id | BIGINT UNSIGNED | NO | | 投稿先アカウント ID（FK） |
| status | ENUM('success', 'failed', 'retry_pending') | NO | | 投稿結果 |
| platform_post_id | VARCHAR(200) | YES | NULL | プラットフォーム側の投稿 ID |
| error_message | TEXT | YES | NULL | エラーメッセージ |
| api_response | JSON | YES | NULL | API レスポンス（参考用） |
| posted_at | DATETIME | YES | NULL | 投稿日時 |
| created_at | DATETIME | NO | CURRENT_TIMESTAMP | 作成日時 |

- **PK**: `id`
- **FK**: `generated_image_id` → `generated_images.id`
- **FK**: `sns_account_id` → `sns_accounts.id`
- **UNIQUE**: `uq_post_records_image_account` (`generated_image_id`, `sns_account_id`) — 重複投稿防止
- **INDEX**: `idx_post_records_status` (`status`)

### 3.6 batch_execution_logs（バッチ実行ログ）

バッチの実行履歴を管理する。

| カラム名 | 型 | NULL | デフォルト | 説明 |
|---|---|---|---|---|
| id | BIGINT UNSIGNED | NO | AUTO_INCREMENT | 主キー |
| set_id | BIGINT UNSIGNED | NO | | バッチセット ID（FK） |
| batch_type | ENUM('image_generation', 'sns_posting') | NO | | バッチ種別 |
| execution_arn | VARCHAR(500) | YES | NULL | Step Functions 実行 ARN |
| status | ENUM('running', 'succeeded', 'failed') | NO | | 実行結果 |
| started_at | DATETIME | NO | | 開始日時 |
| finished_at | DATETIME | YES | NULL | 終了日時 |
| error_message | TEXT | YES | NULL | エラーメッセージ |
| records_processed | INT UNSIGNED | YES | NULL | 処理件数 |
| created_at | DATETIME | NO | CURRENT_TIMESTAMP | 作成日時 |

- **PK**: `id`
- **FK**: `set_id` → `batch_sets.id`
- **INDEX**: `idx_batch_execution_logs_set_type` (`set_id`, `batch_type`)
- **INDEX**: `idx_batch_execution_logs_status` (`status`)

## 4. ER 図（概要）

```
batch_sets (1) ─── (N) prompt_configs
     │
     ├── (1) ─── (N) generated_images ─── (N) post_records
     │                                          │
     ├── (1) ─── (N) sns_accounts ──────────────┘
     │
     └── (1) ─── (N) batch_execution_logs
```

## 5. 文字コード・照合順序

- 文字コード: `utf8mb4`
- 照合順序: `utf8mb4_unicode_ci`
