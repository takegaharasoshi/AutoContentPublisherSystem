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

## 2. 画像生成バッチ

### 2.1 処理フロー

```
開始
  │
  ├── 1. DB 接続確認（リトライ付き）
  │
  ├── 2. DB からプロンプト情報を取得
  │       - 対象のプロンプト設定を取得
  │       - 生成対象がない場合はスキップして正常終了
  │
  ├── 3. 画像生成 API 呼び出し
  │       - Nano Banana Pro（Gemini 3 Pro 画像 API）
  │       - API 失敗時は Step Functions Retry で再試行
  │
  ├── 4. 生成画像を S3 に保存
  │       - キー: images/{set_id}/{YYYYMMDD}/{uuid}.{ext}
  │       - メタデータ: Content-Type 設定
  │
  ├── 5. メタ情報を DB に登録
  │       - 画像テーブルにレコード挿入
  │       - S3 キー、プロンプト ID、生成日時等
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
| SET_ID | バッチセット識別子 | CDK で設定 |

## 3. SNS 投稿バッチ

### 3.1 処理フロー

```
開始
  │
  ├── 1. DB 接続確認（リトライ付き）
  │
  ├── 2. DB から投稿対象を取得
  │       - 未投稿の画像レコードを取得
  │       - 投稿対象がない場合はスキップして正常終了
  │
  ├── 3. S3 から画像を取得
  │       - DB のメタ情報に基づき S3 から画像をダウンロード
  │
  ├── 4. SNS API で投稿
  │       - Instagram Graph API / Content Posting API
  │       - API 失敗時は Step Functions Retry で再試行
  │       - 重複投稿防止チェック
  │
  ├── 5. 投稿結果を DB に記録
  │       - 投稿ステータスの更新
  │       - 投稿日時、投稿先 ID の記録
  │
  └── 正常終了（終了コード 0）
```

### 3.2 Step Functions 定義（概要）

画像生成バッチと同様の構成（Retry/Catch 付き ECS RunTask）。

### 3.3 環境変数

| 変数名 | 説明 | 取得元 |
|---|---|---|
| DB_SECRET_ARN | DB 接続情報の Secret ARN | CDK で設定 |
| SNS_API_SECRET_ARN | SNS API 認証情報の Secret ARN | CDK で設定 |
| S3_BUCKET_NAME | 画像保存元 S3 バケット名 | CDK で設定 |
| SET_ID | バッチセット識別子 | CDK で設定 |

### 3.4 重複投稿防止

- DB の投稿ステータスを確認し、投稿済みの画像はスキップする
- 投稿 API 呼び出し後、DB 更新前に障害が発生した場合に備え、投稿先 API のレスポンスを用いた冪等性チェックを考慮する
