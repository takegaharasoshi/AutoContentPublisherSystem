# バッチ処理設計書

## 1. 共通設計

### 1.1 実行方式

すべてのバッチは以下の流れで実行される:

```
EventBridge Scheduler
    │  cron 式でトリガー
    ▼
Step Functions（Standard）
    │  ワークフロー制御、Retry/Catch
    ▼
ECS Fargate RunTask
    │  Docker コンテナとして実行
    ▼
処理完了 → 終了コード 0 で正常終了
```

### 1.2 DB 接続リトライ

Aurora Serverless v2 の自動一時停止からの再開に対応するため、バッチ開始時に以下のリトライを行う:

```python
# リトライ設計
最大リトライ回数: 5
リトライ間隔: 指数バックオフ（2, 4, 8, 16, 32 秒）
対象例外: OperationalError, InterfaceError
```

### 1.3 Secrets Manager からの認証情報取得

- DB 接続情報、API キーは Secrets Manager から取得する
- SNS API の認証情報は Secret 名規約 `acps/{env}/{set_code}/sns/{platform}/{account_code}` に基づき取得する
- ECS タスクロールに Secrets Manager の読み取り権限を付与する
- `env` は CDK が設定する静的環境変数 `ENV_NAME` を使用する（現時点では `prod`）

### 1.4 ログ出力

- Python の `logging` モジュールを使用
- ログレベル: INFO（デフォルト）、ERROR（異常時）
- 出力先: CloudWatch Logs（ロググループはサービスごと）
- 構造化ログ（JSON 形式）を推奨

### 1.5 エラーハンドリング方針

| レイヤー | ハンドリング方式 |
|---|---|
| Python コード | try/except で例外捕捉、ログ出力、適切な終了コードを返す |
| Step Functions | Retry（リトライ可能エラー）、Catch（リトライ不可エラー） |
| EventBridge | Step Functions の起動失敗は CloudWatch で検知 |

### 1.6 複数セット運用方針

- Step Functions ステートマシンはバッチ種別ごとに 1 つとする（image-generation-sfn, sns-posting-sfn）
- EventBridge Scheduler はセットごと・バッチ種別ごとに作成し、入力パラメータとして `set_code` を渡す
- `SET_CODE`、`SCHEDULED_AT`、`EXECUTION_ARN` は Step Functions から ECS RunTask のコンテナオーバーライド環境変数として渡す
- `ENV_NAME` は CDK が Task Definition に静的設定する環境変数とする（現時点では `prod`）
- スケジュール定義のマスタは IaC（CDK の EventBridge Scheduler リソース定義）とする
- DB の `batch_schedules` テーブルは運用参照・バッチ自己診断用のコピーとして使用する（DB 変更だけではスケジュールは変わらない）
- セット追加手順: (1) DB に `batch_sets` + `batch_schedules` レコード追加 → (2) CDK コードに EventBridge Scheduler を追加して `cdk deploy`
- スケジュール変更手順: (1) CDK コードの cron 式を変更して `cdk deploy` → (2) DB の `batch_schedules` も合わせて更新

> **設計変更理由（set_code の採用）**: 外部識別子（S3 キー、Secret 名、EventBridge Scheduler 入力、ECS 環境変数）には `set_code`（人が定義する安定した文字列）を使用する。`set_id`（AUTO_INCREMENT）は環境間で値が異なるため、S3 パスや Secret 名に使用すると環境移行やデータ復旧時に不整合が生じる。DB 内部の FK 参照には従来通り `set_id` を使用する。バッチ起動後、`SET_CODE` 環境変数から `batch_sets` テーブルを検索して内部 `set_id` を取得し、以降の DB 操作に使用する。Secret 名の環境分離には別途 `ENV_NAME` を併用する。

### 1.7 冪等性・再試行設計

バッチ処理が途中で失敗し Step Functions の Retry でタスク全体が再実行された場合に、副作用の重複（画像の二重生成、投稿の二重実行）を防ぐための設計方針。

#### 画像生成バッチの冪等性

| 処理ステップ | 失敗時の影響 | 再実行時の対応 |
|---|---|---|
| 画像生成 API 呼び出し | 画像未生成 | 問題なし。再度 API を呼び出す |
| S3 保存 | API コスト消費済み、画像未保存 | 再度 API 呼び出しから実行（API コストは許容する） |
| DB 登録 | S3 に orphan ファイルが残る | S3 orphan は許容し、定期クリーンアップで対応。DB にレコードがなければ未生成と見なす |

- **冪等性キー**: `(set_id, prompt_config_id, scheduled_at)` の UNIQUE 制約
- **方針**: 同一 `(set_id, prompt_config_id, scheduled_at)` のレコードが存在する = 当該スケジュール枠の生成は完了。UNIQUE 制約により DB レベルで二重 INSERT を防止
- **S3 orphan 対応**: S3 に存在するが DB に記録がないファイルは月次等で定期削除する

#### SNS 投稿バッチの冪等性

SNS 投稿バッチには 2 種類のリカバリが存在する:

1. **同一 attempt 内の中断復旧**: pending レコードの `platform_container_id` / `platform_post_id` の状態に基づき、中断した処理ステップから再開する。Step Functions の Retry による再実行時、または次回バッチ実行時に pending レコードが残っている場合に適用される。
2. **attempt 間の再試行**: failed で完了した attempt に対し、次回バッチ実行時に新規 pending レコード（`attempt_number` インクリメント）を作成して再試行する。failed レコード自体は履歴として保持され、直接更新されない。

| 処理ステップ | 失敗時の影響 | 再実行時の対応 |
|---|---|---|
| pending レコード挿入 | 投稿未着手 | 問題なし。再度 pending を挿入する |
| コンテナ作成 API | pending のまま（container_id = NULL） | container_id が NULL → 再度コンテナ作成（冪等、ユーザーに不可視） |
| container_id の DB 保存 | API 成功だが未記録 | コンテナ再作成は冪等のため問題なし |
| パブリッシュ API | container_id 保存済み、投稿未完了 | container_id ≠ NULL、platform_post_id = NULL → 同じ container_id でパブリッシュ再試行（Instagram は同一コンテナの二重パブリッシュを拒否） |
| platform_post_id の DB 保存 | 投稿済みだが status が pending | platform_post_id ≠ NULL → status を success に更新してスキップ |
| 投稿失敗（status=failed） | 前回バッチで失敗した | 次回バッチ実行時に success が存在しない組として再検出 → 新規 pending レコード（attempt_number インクリメント）で再試行。retry 上限（max_post_retries）超過時はスキップ |

> **注記**: `status='failed'` のレコードは復旧対象ではなく、履歴として保持される。再試行は常に新しい `pending` レコード（新しい `attempt_number`）の作成により行われる（上記「attempt 間の再試行」に該当）。

- **冪等性キー**: `platform_container_id` と `platform_post_id` の組み合わせ
- **投稿前予約**: API 呼び出し前に `status='pending'` のレコードを挿入する
- **2 段階フロー（Instagram）**:
  1. コンテナ作成 API（`POST /{ig-user-id}/media`）→ `platform_container_id` を取得・即座に DB 保存
  2. パブリッシュ API（`POST /{ig-user-id}/media_publish`）→ `platform_post_id` を取得・DB 保存
- **再実行時の復旧判定**（pending レコードに対して適用。failed レコードには適用されない = 「同一 attempt 内の中断復旧」に該当）:
  - `platform_container_id` = NULL → コンテナ作成から開始
  - `platform_container_id` ≠ NULL、`platform_post_id` = NULL → パブリッシュから再開
  - `platform_post_id` ≠ NULL → 投稿済み、status を success に更新
- **二重投稿防止**: Instagram は同一 container_id の二重パブリッシュを拒否するため、API レベルでの安全性が保証される

### 1.8 実行ログ記録

- 各バッチは開始直後に `batch_execution_logs` へ `status='running'` のレコードを INSERT する
- `set_id` は `SET_CODE` から解決した内部 ID、`batch_type` はバッチ種別固定値、`execution_arn` は `EXECUTION_ARN` を使用する
- 正常終了時は同一レコードを `status='succeeded'` に更新し、`finished_at` と `records_processed` を記録する
- 異常終了時は例外ハンドラで `status='failed'`、`finished_at`、`error_message` を更新する
- プロセス強制終了などで更新できず `running` のまま残ったレコードは、Step Functions 実行履歴と CloudWatch Logs を正とし、運用で stale レコードとして補正する

## 2. 画像生成バッチ

### 2.1 処理フロー

```
開始
  │
  ├── 1. DB 接続確認（リトライ付き）
  │
  ├── 1.5. set_code から内部 set_id を取得
  │       - 環境変数 SET_CODE を使って batch_sets テーブルから set_id（内部 PK）を取得する
  │       - 以降の DB 操作には取得した set_id を使用する
  │
  ├── 2. DB からプロンプト情報を取得
  │       - 対象のプロンプト設定を取得
  │       - 環境変数 SCHEDULED_AT で指定されたスケジュール実行日時を冪等性キーとして使用
  │       - 生成対象がない場合はスキップして正常終了
  │
  ├── 3. 画像生成 API 呼び出し
  │       - Nano Banana Pro（Gemini 3 Pro 画像 API）
  │       - API 失敗時は Step Functions Retry で再試行
  │
  ├── 4. 生成画像を S3 に保存
  │       - キー: images/{set_code}/{YYYYMMDD}/{uuid}.jpg
  │       - メタデータ: Content-Type: image/jpeg
  │       - Instagram 投稿要件に合わせ JPEG 形式で保存する
  │       - 生成 API が PNG を返す場合は JPEG に変換してから保存する
  │
  ├── 5. メタ情報を DB に登録
  │       - 画像テーブルにレコード挿入
  │       - S3 キー、プロンプト ID、生成日時等
  │       - プロンプト本文・パラメータのスナップショットも保存する（prompt_configs の将来変更に備え、生成時点の状態を記録）
  │       - DB 登録が成功した時点で生成完了とする
  │       - S3 保存成功・DB 登録失敗の場合、S3 に orphan が残るが許容する
  │
  ├── （再実行時）同一 (set_id, prompt_config_id, scheduled_at) のレコードがある画像は生成済みと見なしスキップする
  │
  └── 正常終了（終了コード 0）
```

### 2.2 Step Functions 定義（概要）

```json
{
  "StartAt": "RunImageBatchTask",
  "States": {
    "RunImageBatchTask": {
      "Type": "Task",
      "Resource": "arn:aws:states:::ecs:runTask.sync",
      "Retry": [
        {
          "ErrorEquals": ["States.TaskFailed"],
          "IntervalSeconds": 30,
          "MaxAttempts": 2,
          "BackoffRate": 2.0
        }
      ],
      "Catch": [
        {
          "ErrorEquals": ["States.ALL"],
          "Next": "HandleError"
        }
      ],
      "End": true
    },
    "HandleError": {
      "Type": "Fail",
      "Error": "ImageBatchFailed",
      "Cause": "Image batch task failed after retries"
    }
  }
}
```

### 2.3 環境変数

| 変数名 | 説明 | 取得元 |
|---|---|---|
| DB_SECRET_ARN | DB 接続情報の Secret ARN | CDK で設定 |
| API_SECRET_ARN | 画像生成 API キーの Secret ARN | CDK で設定 |
| S3_BUCKET_NAME | 画像保存先 S3 バケット名 | CDK で設定 |
| ENV_NAME | 環境識別子（現時点では `prod`） | CDK で設定 |
| SET_CODE | バッチセット識別コード（batch_sets.set_code に対応） | Step Functions 入力パラメータ |
| EXECUTION_ARN | Step Functions 実行 ARN（手動 RunTask 時は空） | Step Functions コンテナオーバーライド（`$$.Execution.Id`） |
| SCHEDULED_AT | スケジュール実行日時（ISO 8601、例: 2024-01-15T00:00:00Z）。DB には UTC の DATETIME として保存する（`Z` 接尾辞を除いた値） | Step Functions 入力パラメータ（EventBridge Scheduler の `<aws.scheduler.scheduled-time>` から取得） |

## 3. SNS 投稿バッチ

### 3.1 処理フロー

```
開始
  │
  ├── 1. DB 接続確認（リトライ付き）
  │
  ├── 1.5. set_code から内部 set_id を取得
  │       - 環境変数 SET_CODE を使って batch_sets テーブルから set_id（内部 PK）を取得する
  │       - 以降の DB 操作には取得した set_id を使用する
  │
  ├── 2. DB から投稿対象を取得
  │       - 対象: 該当セット（set_code で特定）の active な sns_accounts すべてについて、
  │         post_records に status='success' のレコードが存在しない (image, account) の組
  │       - failed のみ存在する組も対象に含まれる（success がないため）
  │       - pending レコードが存在する場合も対象に含める（再試行判断はステップ 3 で行う）
  │       - 処理上限: 1 回のバッチ実行で処理する最大件数は BATCH_SIZE_LIMIT（デフォルト: 50）件とする
  │       - 処理順序: generated_images.generated_at の昇順（古い画像を優先）
  │       - 上限超過時: 残りは次回スケジュール実行で処理する（ログに残件数を出力）
  │       - 投稿対象がない場合はスキップして正常終了
  │
  ├── 2.5. SNS 認証情報の取得
  │       - 各 sns_account の platform、account_code、ENV_NAME、set_code から Secret 名
  │         `acps/{env}/{set_code}/sns/{platform}/{account_code}` を組み立て、
  │         Secrets Manager から認証情報を取得する
  │       - ECS タスクロールにプレフィックス `acps/{env}/*` の Secret への読み取り権限が必要
  │
  ├── 3. 再試行判断（画像・アカウントの組ごと）
  │       - retry 上限チェック: 該当 (image, account) の既存レコード数（= 最大 attempt_number）が
  │         max_post_retries（デフォルト 3）以上の場合はスキップし、ログに警告を出力する
  │         （初回は attempt_number=1、再試行ごとに +1。max_post_retries=3 なら最大 3 回試行）
  │       - pending レコードが存在する場合（同一バッチ実行内での再試行）:
  │         - platform_post_id が NOT NULL → 投稿済み、status を success に更新してスキップ
  │         - platform_container_id が NOT NULL、platform_post_id が NULL → ステップ 5 へ（パブリッシュから再開）
  │         - platform_container_id が NULL → ステップ 4 へ（コンテナ作成から開始）
  │       - pending レコードが存在しない場合（初回、または前回 failed で完了している場合 = 「attempt 間の再試行」に該当）:
  │         - 新規に status='pending' のレコードを挿入（attempt_number インクリメント）してステップ 4 へ
  │
  ├── 4. Presigned URL 発行 + コンテナ作成
  │       - DB のメタ情報に基づき S3 オブジェクトの Presigned URL を生成（有効期限: 1 時間）
  │       - Instagram Graph API のコンテナ作成 API（`POST /{ig-user-id}/media`）に
  │         Presigned URL を image_url パラメータとして渡す
  │       - 取得した container_id（creation_id）を pending レコードの platform_container_id に即座に保存
  │
  ├── 5. パブリッシュ API 呼び出し
  │       - Instagram Graph API の media_publish API（`POST /{ig-user-id}/media_publish`）に
  │         container_id を渡して投稿
  │       - Instagram は同一 container_id の二重パブリッシュを拒否するため安全
  │       - API 失敗時は pending レコードの status を failed に更新（次回バッチ実行時に再試行される、上限まで）
  │
  ├── 6. 投稿結果を DB に記録
  │       - pending レコードの platform_post_id（media_id）、status、posted_at、api_response を更新
  │       - （generated_images テーブルへの更新は不要）
  │
  └── 正常終了（終了コード 0）
```

### 3.2 Step Functions 定義（概要）

画像生成バッチと同様の構成（Retry/Catch 付き ECS RunTask）。

### 3.3 環境変数

| 変数名 | 説明 | 取得元 |
|---|---|---|
| DB_SECRET_ARN | DB 接続情報の Secret ARN | CDK で設定 |
| S3_BUCKET_NAME | 画像保存元 S3 バケット名 | CDK で設定 |
| ENV_NAME | 環境識別子（現時点では `prod`） | CDK で設定 |
| SET_CODE | バッチセット識別コード（batch_sets.set_code に対応） | Step Functions 入力パラメータ |
| EXECUTION_ARN | Step Functions 実行 ARN（手動 RunTask 時は空） | Step Functions コンテナオーバーライド（`$$.Execution.Id`） |
| BATCH_SIZE_LIMIT | 1 回のバッチ実行で処理する最大投稿件数（デフォルト: 50） | CDK で設定 |

> **SNS 認証情報の取得方式**: SNS API の認証情報は環境変数ではなく、Secrets Manager からアカウントごとに取得する。Secret 名は `acps/{env}/{set_code}/sns/{platform}/{account_code}` の規約でアプリ側が導出する（`env` は `ENV_NAME`、DB には Secret 名・ARN を保持しない）。

### 3.4 重複投稿防止

- 投稿対象の判定は `post_records` テーブルの `status='success'` レコードの有無で行う（`generated_images` に `post_status` は持たない）
- 各 (`generated_image_id`, `sns_account_id`) の組について、`status='success'` のレコードが存在する場合はスキップする
- **排他制御（親行ロック方式）**: 投稿対象の `generated_images` レコードを `SELECT ... FOR UPDATE` でロックし（親行は必ず存在するため、ロック対象が 0 件になる問題を回避）、ロック取得後に `post_records` から `status='success'` の有無を確認してから `pending` を挿入する。UNIQUE 制約 `(generated_image_id, sns_account_id, attempt_number)` により、万一並行 INSERT が発生しても DB レベルで重複を防止する（DuplicateKeyError はアプリ側で捕捉してスキップ）
- 投稿前に `status='pending'` のレコードを挿入（予約）し、API 呼び出し後に status を更新する
- **2 段階フロー**: コンテナ作成 → パブリッシュの各段階で DB に中間状態（`platform_container_id`）を記録し、「API 成功 → DB 書き込み失敗」のギャップを解消する
- 再実行時は `platform_container_id` と `platform_post_id` の組み合わせで、どの段階から再開するかを判定する
- 再試行はレコードを新規追加する形で履歴を保持する（`attempt_number` をインクリメント）

### 3.5 バッチサイズ制限とレート制御

- **バッチサイズ制限**: 1 回のバッチ実行で処理する投稿数の上限を `BATCH_SIZE_LIMIT` 環境変数で設定する（デフォルト: 50）
- **処理順序**: `generated_images.generated_at` の昇順で処理し、古い画像を優先する
- **上限超過時の動作**: 上限に達した時点で処理を終了する。未処理分は次回のスケジュール実行で処理される
- **レート制御**: Instagram Graph API のレート制限（アカウントごとの制限等）に対応するため、プラットフォーム・アカウントごとの投稿間隔を設ける（将来拡張。初期版では BATCH_SIZE_LIMIT による総量制御のみ）
- **バックログ監視**: 未投稿件数が一定閾値を超えた場合はログに WARNING を出力する（閾値は BATCH_SIZE_LIMIT の 3 倍を目安）
