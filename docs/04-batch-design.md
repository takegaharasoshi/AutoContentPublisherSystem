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
- ECS タスクロールに Secrets Manager の読み取り権限を付与する

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
- EventBridge Scheduler はセットごと・バッチ種別ごとに作成し、入力パラメータとして `set_id` を渡す
- `SET_ID` と `SCHEDULED_AT` は Step Functions の入力 → ECS RunTask のコンテナオーバーライド環境変数として渡す
- スケジュール定義のマスタは IaC（CDK の EventBridge Scheduler リソース定義）とする
- DB の `batch_schedules` テーブルは運用参照・バッチ自己診断用のコピーとして使用する（DB 変更だけではスケジュールは変わらない）
- セット追加手順: (1) DB に `batch_sets` + `batch_schedules` レコード追加 → (2) CDK コードに EventBridge Scheduler を追加して `cdk deploy`
- スケジュール変更手順: (1) CDK コードの cron 式を変更して `cdk deploy` → (2) DB の `batch_schedules` も合わせて更新

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

## 2. 画像生成バッチ

### 2.1 処理フロー

```
開始
  │
  ├── 1. DB 接続確認（リトライ付き）
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
  │       - キー: images/{set_id}/{YYYYMMDD}/{uuid}.jpg
  │       - メタデータ: Content-Type: image/jpeg
  │       - Instagram 投稿要件に合わせ JPEG 形式で保存する
  │       - 生成 API が PNG を返す場合は JPEG に変換してから保存する
  │
  ├── 5. メタ情報を DB に登録
  │       - 画像テーブルにレコード挿入
  │       - S3 キー、プロンプト ID、生成日時等
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
| SET_ID | バッチセット識別子 | Step Functions 入力パラメータ |
| SCHEDULED_AT | スケジュール実行日時（ISO 8601、例: 2024-01-15T00:00:00Z）。DB には UTC の DATETIME として保存する（`Z` 接尾辞を除いた値） | Step Functions 入力パラメータ（EventBridge Scheduler の `<aws.scheduler.scheduled-time>` から取得） |

## 3. SNS 投稿バッチ

### 3.1 処理フロー

```
開始
  │
  ├── 1. DB 接続確認（リトライ付き）
  │
  ├── 2. DB から投稿対象を取得
  │       - 対象: 該当 set_id の active な sns_accounts すべてについて、
  │         post_records に status='success' のレコードが存在しない (image, account) の組
  │       - failed のみ存在する組も対象に含まれる（success がないため）
  │       - pending レコードが存在する場合も対象に含める（再試行判断はステップ 3 で行う）
  │       - 投稿対象がない場合はスキップして正常終了
  │
  ├── 2.5. SNS 認証情報の取得
  │       - 各 sns_account の platform、account_code、set_id から Secret 名
  │         `acps/{set_id}/sns/{platform}/{account_code}` を組み立て、
  │         Secrets Manager から認証情報を取得する
  │       - ECS タスクロールにプレフィックス `acps/*` の Secret への読み取り権限が必要
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
| SET_ID | バッチセット識別子 | Step Functions 入力パラメータ |

> **SNS 認証情報の取得方式**: SNS API の認証情報は環境変数ではなく、Secrets Manager からアカウントごとに取得する。Secret 名は `acps/{set_id}/sns/{platform}/{account_code}` の規約でアプリ側が導出する（DB には Secret 名・ARN を保持しない）。

### 3.4 重複投稿防止

- 投稿対象の判定は `post_records` テーブルの `status='success'` レコードの有無で行う（`generated_images` に `post_status` は持たない）
- 各 (`generated_image_id`, `sns_account_id`) の組について、`status='success'` のレコードが存在する場合はスキップする
- **排他制御**: 投稿対象の判定と pending レコード挿入はトランザクション内で `SELECT ... FOR UPDATE` を使用する。対象の `(generated_image_id, sns_account_id)` の既存レコードをロックし、`status='success'` が存在しないことを確認してから `pending` を挿入する。これにより並行実行による二重投稿を防止する
- 投稿前に `status='pending'` のレコードを挿入（予約）し、API 呼び出し後に status を更新する
- **2 段階フロー**: コンテナ作成 → パブリッシュの各段階で DB に中間状態（`platform_container_id`）を記録し、「API 成功 → DB 書き込み失敗」のギャップを解消する
- 再実行時は `platform_container_id` と `platform_post_id` の組み合わせで、どの段階から再開するかを判定する
- 再試行はレコードを新規追加する形で履歴を保持する（`attempt_number` をインクリメント）
