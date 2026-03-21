# データベース設計書

## 1. 設計方針

- Aurora Serverless v2（MySQL 互換）を使用する
- 将来の複数セット運用を前提に、DB 内部の FK 参照には `set_id` でデータを識別可能にする。外部識別子（S3 キー、Secret 名、EventBridge Scheduler 入力、ECS 環境変数）には `set_code`（人が定義する安定した識別コード）を使用する
- 複数環境対応のため、外部の Secret 名には `env` を含める。環境識別子は ECS タスクの `ENV_NAME` 環境変数で扱う
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
- **UNIQUE**: `uq_prompt_configs_set_id` (`set_id`, `id`) — 複合 FK の参照先として使用
- **INDEX**: `idx_prompt_configs_set_id` (`set_id`)

### 3.3 generated_images（生成画像）

生成された画像のメタ情報を管理する。

| カラム名 | 型 | NULL | デフォルト | 説明 |
|---|---|---|---|---|
| id | BIGINT UNSIGNED | NO | AUTO_INCREMENT | 主キー |
| set_id | BIGINT UNSIGNED | NO | | バッチセット ID（FK） |
| prompt_config_id | BIGINT UNSIGNED | NO | | 使用プロンプト設定 ID（FK） |
| prompt_text_snapshot | TEXT | NO | | 画像生成時に使用したプロンプト本文のスナップショット |
| parameters_snapshot | JSON | YES | NULL | 画像生成時に使用したパラメータのスナップショット |
| scheduled_at | DATETIME | NO | | スケジュール実行日時（UTC、冪等性キー） |
| s3_key | VARCHAR(500) | NO | | S3 オブジェクトキー |
| s3_bucket | VARCHAR(200) | NO | | S3 バケット名 |
| file_format | VARCHAR(20) | NO | 'jpg' | ファイル形式（Instagram 要件により jpg を標準とする） |
| file_size_bytes | BIGINT UNSIGNED | YES | NULL | ファイルサイズ（バイト） |
| width | INT UNSIGNED | YES | NULL | 画像幅（ピクセル） |
| height | INT UNSIGNED | YES | NULL | 画像高さ（ピクセル） |
| generation_api_response | JSON | YES | NULL | API レスポンス（参考用） |
| generated_at | DATETIME | NO | CURRENT_TIMESTAMP | 画像生成 API から画像を取得した日時（UTC） |
| created_at | DATETIME | NO | CURRENT_TIMESTAMP | DB レコード作成日時（UTC） |
| updated_at | DATETIME | NO | CURRENT_TIMESTAMP ON UPDATE | 更新日時（UTC） |

- **PK**: `id`
- **FK**: `set_id` → `batch_sets.id`
- **FK**: `(set_id, prompt_config_id)` → `prompt_configs(set_id, id)` — セット境界の整合性を保証する複合 FK
- **UNIQUE**: `uq_generated_images_set_id` (`set_id`, `id`) — 複合 FK の参照先として使用
- **INDEX**: `idx_generated_images_set_id` (`set_id`)
- **UNIQUE**: `uq_generated_images_idempotency` (`set_id`, `prompt_config_id`, `scheduled_at`)

> **注記**: 投稿ステータスは `post_records` テーブルから導出する。`generated_images` テーブルには投稿状態を持たない。

> **S3 キーの命名規約**: `s3_key` に格納するオブジェクトキーは `images/{set_code}/{YYYYMMDD}/{uuid}.jpg` の形式とする。`set_code` はバッチ起動時の環境変数 `SET_CODE` から取得する。

> **設計変更理由（プロンプトスナップショット）**: `prompt_configs` は運用中に内容が更新される可能性がある。`generated_images` に生成時点のプロンプト本文とパラメータのスナップショットを保持することで、過去の生成結果がどのプロンプトで作られたかを正確に追跡できる。`prompt_config_id` は FK として保持し、設定の系譜を辿れるようにする。

> **設計変更理由（複合 FK）**: `prompt_config_id → prompt_configs.id` の単純 FK では、異なるセットの `prompt_configs` を参照可能だった。`(set_id, prompt_config_id) → prompt_configs(set_id, id)` の複合 FK に変更し、同一セット内のプロンプト設定のみ参照できるよう DB レベルで保証する。

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
- **UNIQUE**: `uq_sns_accounts_set_id` (`set_id`, `id`) — 複合 FK の参照先として使用
- **INDEX**: `idx_sns_accounts_set_id` (`set_id`)
- **UNIQUE**: `uq_sns_accounts_set_platform_code` (`set_id`, `platform`, `account_code`)

> **認証情報の管理方針**: SNS 認証情報の Secret 名はテーブルに保持せず、アプリケーション側で Secret 名規約に基づき導出する（規約の詳細は [design/security.md](../design/security.md) を参照）。`set_code` は `batch_sets` テーブルから取得し、`env` は ECS タスクの `ENV_NAME`（現時点では `prod`）を使用する。これにより IAM ポリシーでプレフィックスベースの最小権限を維持しつつ、DB へのアカウント追加だけで新しい Secret へのアクセスが可能になる。

> **設計変更理由（account_code）**: Secret 名の導出に `account_name`（表示名）を使用すると、表示名の変更時に Secrets Manager の Secret 名と不整合が生じる。不変の `account_code` を導入し Secret 名導出に使用することで、`account_name` を安全に変更可能にする。`account_code` は作成時に設定し変更不可とする。

### 3.5 post_records（投稿履歴）

SNS 投稿の実行結果を管理する。再試行のたびにレコードを追加し、`status='success'` のレコードの有無で投稿完了を判断する（success が 1 件でもあれば投稿済みと見なす）。

| カラム名 | 型 | NULL | デフォルト | 説明 |
|---|---|---|---|---|
| id | BIGINT UNSIGNED | NO | AUTO_INCREMENT | 主キー |
| set_id | BIGINT UNSIGNED | NO | | バッチセット ID（FK、セット境界の整合性保証用） |
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
| updated_at | DATETIME | NO | CURRENT_TIMESTAMP ON UPDATE | 更新日時（UTC） |

- **PK**: `id`
- **FK**: `(set_id, generated_image_id)` → `generated_images(set_id, id)` — セット境界の整合性を保証する複合 FK
- **FK**: `(set_id, sns_account_id)` → `sns_accounts(set_id, id)` — セット境界の整合性を保証する複合 FK
- **UNIQUE**: `uq_post_records_image_account_attempt` (`generated_image_id`, `sns_account_id`, `attempt_number`) — 同一 attempt の二重 INSERT を DB レベルで防止
- **INDEX**: `idx_post_records_image_account` (`generated_image_id`, `sns_account_id`)
- **INDEX**: `idx_post_records_status` (`status`)
- **INDEX**: `idx_post_records_image_account_status` (`generated_image_id`, `sns_account_id`, `status`) — 投稿完了判定用

> **設計変更理由（セット境界の整合性）**: `post_records` に `set_id` カラムを追加し、複合外部キー `(set_id, generated_image_id)` → `generated_images(set_id, id)` および `(set_id, sns_account_id)` → `sns_accounts(set_id, id)` を設定する。これにより、異なるセットの画像とアカウントを組み合わせた投稿レコードの作成を DB レベルで防止する。`set_id` は `generated_images` または `sns_accounts` から導出可能だが、複合 FK の制約上 `post_records` テーブルにも保持する必要がある。

> **設計変更理由（UNIQUE 制約）**: UNIQUE 制約 `(generated_image_id, sns_account_id)` を廃止し、`(generated_image_id, sns_account_id, attempt_number)` に変更した。複数アカウントへの投稿で「A に成功、B に失敗」を表現でき、再試行履歴を自然に蓄積できるようにするため。同時に、同一 attempt の二重 INSERT を DB レベルで防止する。`pending` ステータスは投稿予約（API 呼び出し前の冪等性確保）に使用する。

> **再試行の仕組み**: 再試行は新規レコード（`attempt_number` インクリメント）で管理する。`failed` レコードは履歴として保持され、次回バッチ実行時に `status='success'` が存在しなければ新しい `pending` レコードが作成される。`attempt_number` が `batch_sets.max_post_retries`（デフォルト: 3）以上の場合はスキップされ、ログに警告が出力される。

> **排他制御**: 並行実行による二重投稿を防止するため、以下の親行ロック方式を採用する:
>
> 1. 投稿対象の `generated_images` レコードを `SELECT ... FOR UPDATE` でロックする（親行は必ず存在するため、ロック対象が 0 件になる問題を回避できる）
> 2. ロック取得後、`post_records` から当該 `(generated_image_id, sns_account_id)` の既存レコードを確認する
> 3. `status='success'` が存在すればスキップ、存在しなければ `pending` レコードを INSERT する
> 4. **フォールバック**: UNIQUE 制約 `uq_post_records_image_account_attempt` により、万一並行 INSERT が発生しても DB レベルで重複を防止する（DuplicateKeyError はアプリ側で捕捉してスキップする）
>
> **設計変更理由（親行ロック方式）**: 従来の `post_records` に対する `SELECT ... FOR UPDATE` は、初回投稿時にロック対象行が 0 件となり、並行実行で二重 `pending` が発生する可能性があった。親行（`generated_images`）をロックすることで、行が必ず存在する状態でのロックを保証する。

> **二重投稿防止の強化**: Instagram Graph API の 2 段階フロー（コンテナ作成 → パブリッシュ）に対応し、`platform_container_id` で中間状態を永続化する。再実行時は `platform_container_id` と `platform_post_id` の組み合わせで復旧ポイントを判定する。将来の他プラットフォーム対応では、`platform_container_id` をプラットフォーム固有の「事前登録 ID」として汎用的に使用する。

> **運用上の注意（テーブル肥大化）**: `post_records` テーブルは再試行のたびにレコードが追加される設計のため、運用期間の長期化に伴いレコード数が増加する。現時点では対策不要だが、パフォーマンスへの影響が観測された場合は、アーカイブテーブルへの移行やパーティショニングを検討する。

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

> **更新責務**: 各バッチアプリケーションが開始時に `status='running'` を INSERT し、終了時に `succeeded` または `failed` へ UPDATE する。`execution_arn` には Step Functions から渡される `EXECUTION_ARN` を格納し、手動 RunTask 時は `NULL` を許容する。

> **records_processed の定義**: 画像生成バッチでは生成完了した画像件数、SNS 投稿バッチでは当該実行で処理した投稿対象件数を格納する。

> **stale running レコードの扱い**: プロセス異常終了などで `running` のまま残る場合がある。Step Functions 実行履歴と CloudWatch Logs を正とし、運用で stale レコードを `failed` へ補正する。

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

> **注記**: `generated_images` の投稿ステータスは `post_records` から導出する（`generated_images` テーブルに `post_status` カラムは持たない）。

> **注記（セット境界の整合性）**: `generated_images` → `prompt_configs` および `post_records` → `generated_images` / `sns_accounts` の FK は複合キー（`set_id` を含む）で定義し、セット境界を超えた参照を DB レベルで防止する。

## 5. 時刻の取り扱い方針

- DB の全 DATETIME カラムは **UTC で保存する**
- MySQL の DATETIME 型はタイムゾーン情報を持たないため、アプリケーション側で UTC に変換してから格納する責務を負う
- EventBridge Scheduler の `<aws.scheduler.scheduled-time>` は UTC（ISO 8601 の `Z` 接尾辞）で渡されるため、`Z` を除いた値をそのまま DATETIME カラムに格納する
- 表示時のタイムゾーン変換（UTC → Asia/Tokyo 等）はアプリケーション層の責務とする
- 冪等性キーの比較・UNIQUE 制約の判定もすべて UTC ベースで行う

## 6. 文字コード・照合順序

- 文字コード: `utf8mb4`
- 照合順序: `utf8mb4_unicode_ci`
