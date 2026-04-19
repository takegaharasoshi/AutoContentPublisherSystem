# バッチ処理設計

## 1. 共通設計

### 1.1 実行方式

画像生成バッチと SNS 投稿バッチは順次実行される:

```
EventBridge Scheduler
    │  cron 式でトリガー
    ▼
Step Functions（image-generation-sfn）
    │  ワークフロー制御、Retry/Catch
    ▼
ECS Fargate RunTask（DB 準備確認）
    │  Aurora 接続確認、リトライ付き
    ▼
ECS Fargate RunTask（画像生成バッチ）
    │  Docker コンテナとして実行
    ▼
処理完了 → 終了コード 0 で正常終了
    │
    ▼  成功時
Step Functions（sns-posting-sfn）を StartExecution で起動
    │  ワークフロー制御、Retry/Catch
    ▼
ECS Fargate RunTask（DB 準備確認）
    │  Aurora 接続確認、リトライ付き
    ▼
ECS Fargate RunTask（SNS 投稿バッチ）
    │  Docker コンテナとして実行
    ▼
処理完了 → 終了コード 0 で正常終了
```

> **順次実行の設計方針**: 画像生成完了後に SNS 投稿を自動実行することで、通常運用時（未投稿のバックログがない状態）は生成直後の画像が即座に投稿される。バックログが存在する場合は `generated_at` の昇順（古い画像優先）で処理されるため、当回生成分の投稿は既存のバックログ解消後となる（バックログ解消優先。処理順序の詳細はセクション 3.1 参照）。SNS 投稿 Step Functions（sns-posting-sfn）は独立したステートマシンとして存在するため、手動での再投稿や投稿のみの単独実行も引き続き可能。EventBridge Scheduler は画像生成 Step Functions のみに設定し、SNS 投稿用のスケジューラは不要。

> **SNS 投稿起動の冪等性**: image-generation-sfn から sns-posting-sfn を起動する際は、親の `$$.Execution.Name` を子実行の `Name` として使用する。これにより `StartExecution` の Retry 時も同一要求として扱われ、二重起動のリスクを抑制できる。

### 1.2 DB 準備確認（ECS Fargate タスク）

Aurora Serverless v2 の自動一時停止からの再開に対応するため、各 Step Functions ワークフローの最初のステートとして DB 準備確認 ECS タスクを実行する。

- **ECS Task Definition**: FoundationStack で定義（db-readiness-check）。両ワークフローで共有する
- **リソース**: 最小構成（0.25 vCPU / 0.5 GB）
- **配置**: Public Subnet（`assignPublicIp=ENABLED`）。Aurora（Isolated Subnet）へ VPC 内部ルーティングで接続する
- **リトライ設計**:
  ```
  最大リトライ回数: 8
  リトライ間隔: 指数バックオフ（2, 4, 8, 16, 32, 64, 128, 256 秒）
  対象例外: OperationalError, InterfaceError
  ```
  > Aurora Serverless v2 のコールドスタート（自動一時停止からの再開）は通常 15〜30 秒程度だが、リージョン状況や負荷によっては数分かかる場合があるため、安全側に倒して最大約 510 秒の待機時間を確保する。
- **Step Functions との責務分担**: `WaitForDbReady` ステートには Step Functions の Retry を設定しない。待機・再試行は db-readiness-check コンテナ内部で完結させ、総待機時間を上記の約 510 秒に固定する
- **認証情報**: Secrets Manager（DB 認証情報）から取得
- **成功時**: 終了コード 0 で終了し、Step Functions が次のステートへ遷移する
- **失敗時**: 終了コード 1 で終了し、Step Functions の Catch でハンドリングする

> **設計変更理由**: DB 接続リトライをバッチアプリケーションコードから分離し、Step Functions ワークフローの責務とした。これにより、バッチアプリケーションは DB が利用可能な状態を前提として実装できる。

> **ECS Fargate 採用理由**: VPC 内の Lambda はパブリック IP が付与されないため、NAT Gateway または VPC Endpoint（Interface 型）なしでは Secrets Manager にアクセスできない。ECS Fargate は `assignPublicIp=ENABLED` でパブリック IP を取得可能なため、追加のネットワークリソースなしで Secrets Manager にアクセスできる。起動レイテンシ（30〜60 秒）の増加はバッチ用途では許容範囲内であり、月額コストも $0.01 未満と無視できる水準。

### 1.3 Secrets Manager からの認証情報取得

- DB 接続情報、API キーは Secrets Manager から取得する
- SNS API の認証情報は Secret 名規約に基づき取得する（規約の詳細は [design/security.md](security.md) を参照）
- `env` は CDK が設定する静的環境変数 `ENV_NAME` を使用する（現時点では `prod`）

### 1.4 ログ出力

- Python の `logging` モジュールを使用
- ログレベル: INFO（デフォルト）、ERROR（異常時）
- 出力先: CloudWatch Logs（ロググループはサービスごと）
- 構造化ログ（JSON 形式）を推奨

### 1.5 エラーハンドリング方針

| レイヤー | ハンドリング方式 |
|---|---|
| ECS タスク（DB 準備確認） | DB 接続リトライ（指数バックオフ、最大 8 回）。失敗時は終了コード 1 で終了 |
| Python コード（バッチ） | try/except で例外捕捉、ログ出力、適切な終了コードを返す（DB 接続リトライは不要。DB は利用可能前提） |
| Step Functions | 画像生成 / SNS 投稿 ECS タスクに対して Retry/Catch を設定する。DB 準備確認は ECS タスク内の retry のみを使用し、Step Functions 側では Catch のみ設定する。ASL 定義は [specs/workflow.md](../specs/workflow.md) を参照 |
| EventBridge | Step Functions の起動失敗は CloudWatch で検知 |

> **タイムアウト方針**: Step Functions の各 Task ステートには明示タイムアウトを設定し、ハング時にワークフローが長時間ぶら下がらないようにする。具体値は [specs/workflow.md](../specs/workflow.md) を参照。

### 1.6 同時実行に関する制約事項

Step Functions Standard にはステートマシン自体の同時実行数を制限するネイティブ機能がない（`MaxConcurrency` は Map State 内の並列イテレーション制御であり、ステートマシンの実行数制限ではない）。

- **通常運用での回避策**: EventBridge Scheduler の実行間隔をバッチの想定実行時間より十分長く設定することで、同時実行を回避する
- **同時実行が発生した場合の動作**: 複数の実行が並行して進行する。ただし、DB レベルの排他制御により、データの整合性は保証される
  - **画像生成バッチ**: `(set_id, prompt_config_id, scheduled_at)` の UNIQUE 制約により、同一スケジュール枠の二重生成を DB レベルで防止する
  - **SNS 投稿バッチ**: 親行ロック（`generated_images` の `SELECT ... FOR UPDATE`）+ UNIQUE 制約 `(generated_image_id, sns_account_id, attempt_number)` により、二重投稿を防止する
- **手動実行時の注意**: 手動実行とスケジュール実行が重なっても、上記の DB レベル排他制御によりデータ不整合は発生しない。ただし、不要な API コール（画像生成 API の二重呼び出し等）が発生する可能性がある

> **スケーラビリティに関する注記**: 現在のステートマシン構成（バッチ種別ごとに 1 つ、全セット共有）では、セット数の増加によりスケジュール時刻からの遅延が蓄積する可能性がある。遅延が問題になった場合は、ステートマシンをセットごとに分離する対応を検討する。

### 1.7 複数セット運用方針

- Step Functions ステートマシンはバッチ種別ごとに 1 つとする（image-generation-sfn, sns-posting-sfn）
- EventBridge Scheduler はセットごとに作成し、画像生成 Step Functions をターゲットとして `set_code` を渡す
- `SET_CODE`、`EXECUTION_ARN` は両バッチ共通で Step Functions から ECS RunTask のコンテナオーバーライド環境変数として渡す。`SCHEDULED_AT` は画像生成バッチのみ（環境変数一覧は [specs/workflow.md](../specs/workflow.md) を参照）
- `ENV_NAME` は CDK が Task Definition に静的設定する環境変数とする（現時点では `prod`）
- スケジュール定義のマスタは IaC（CDK の EventBridge Scheduler リソース定義）とする
- セット追加手順: (1) DB に `batch_sets` レコード追加 → (2) CDK コードに EventBridge Scheduler を追加して `cdk deploy`
- スケジュール変更手順: CDK コードの cron 式を変更して `cdk deploy`

> **設計変更理由（set_code の採用）**: 外部識別子（S3 キー、Secret 名、EventBridge Scheduler 入力、ECS 環境変数）には `set_code`（人が定義する安定した文字列）を使用する。`set_id`（AUTO_INCREMENT）は環境間で値が異なるため、S3 パスや Secret 名に使用すると環境移行やデータ復旧時に不整合が生じる。DB 内部の FK 参照には従来通り `set_id` を使用する。バッチ起動後、`SET_CODE` 環境変数から `batch_sets` テーブルを検索して内部 `set_id` を取得し、以降の DB 操作に使用する。

### 1.8 冪等性・再試行設計

バッチ処理が途中で失敗し Step Functions の Retry でタスク全体が再実行された場合に、副作用の重複（画像の二重生成、投稿の二重実行）を防ぐための設計方針。

#### 画像生成バッチの冪等性

| 処理ステップ | 失敗時の影響 | 再実行時の対応 |
|---|---|---|
| 画像生成 API 呼び出し | 画像未生成 | 問題なし。再度 API を呼び出す |
| S3 保存 | API コスト消費済み、画像未保存 | 再度 API 呼び出しから実行（API コストは許容する） |
| DB 登録 | S3 に orphan ファイルが残る | S3 orphan は許容し、Lifecycle Policy で対応。DB にレコードがなければ未生成と見なす |

- **冪等性キー**: `(set_id, prompt_config_id, scheduled_at)` の UNIQUE 制約
- **方針**: 同一レコードが存在する = 当該スケジュール枠の生成は完了。UNIQUE 制約により DB レベルで二重 INSERT を防止

#### SNS 投稿バッチの冪等性

SNS 投稿バッチには 2 種類のリカバリが存在する:

1. **同一 attempt 内の中断復旧**: pending レコードの `platform_container_id` / `platform_post_id` の状態に基づき、中断した処理ステップから再開する
2. **attempt 間の再試行**: failed で完了した attempt に対し、次回バッチ実行時に新規 pending レコード（`attempt_number` インクリメント）を作成して再試行する

| 処理ステップ | 失敗時の影響 | 再実行時の対応 |
|---|---|---|
| pending レコード挿入 | 投稿未着手 | 問題なし。再度 pending を挿入する |
| コンテナ作成 API | pending のまま（container_id = NULL） | container_id が NULL → 再度コンテナ作成（冪等、ユーザーに不可視） |
| container_id の DB 保存 | API 成功だが未記録 | コンテナ再作成は冪等のため問題なし |
| パブリッシュ API | container_id 保存済み、投稿未完了 | container_id ≠ NULL、platform_post_id = NULL → 同じ container_id でパブリッシュ再試行（Instagram は同一コンテナの二重パブリッシュを拒否） |
| platform_post_id の DB 保存 | 投稿済みだが status が pending | platform_post_id ≠ NULL → status を success に更新してスキップ |
| 投稿失敗（status=failed） | 前回バッチで失敗した | 次回バッチ実行時に success が存在しない組として再検出 → 新規 pending レコード（attempt_number インクリメント）で再試行。retry 上限（max_post_retries）超過時はスキップ |

> **注記**: `status='failed'` のレコードは復旧対象ではなく、履歴として保持される。再試行は常に新しい `pending` レコードの作成により行われる。

- **冪等性キー**: `platform_container_id` と `platform_post_id` の組み合わせ
- **投稿前予約**: API 呼び出し前に `status='pending'` のレコードを挿入する
- **2 段階フロー（Instagram）**:
  1. コンテナ作成 API（`POST /{ig-user-id}/media`）→ `platform_container_id` を取得・即座に DB 保存
  2. パブリッシュ API（`POST /{ig-user-id}/media_publish`）→ `platform_post_id` を取得・DB 保存
- **二重投稿防止**: Instagram は同一 container_id の二重パブリッシュを拒否するため、API レベルでの安全性が保証される

### 1.9 実行ログ記録

- 各バッチは開始直後に `batch_execution_logs` へ `status='running'` のレコードを INSERT する
- `set_id` は `SET_CODE` から解決した内部 ID、`batch_type` はバッチ種別固定値、`execution_arn` は `EXECUTION_ARN` を使用する
- 正常終了時は `status='succeeded'` に更新し、`finished_at` と `records_processed` を記録する
- 異常終了時は例外ハンドラで `status='failed'`、`finished_at`、`error_message` を更新する
- `batch_execution_logs` の INSERT/UPDATE が失敗した場合は、バッチ全体を失敗（終了コード 1）とする。ログ記録はバッチ実行の追跡に不可欠であり、記録なしでの続行は運用上のリスクが高いため
- プロセス強制終了などで `running` のまま残ったレコードは、Step Functions 実行履歴と CloudWatch Logs を正とし、運用で stale レコードとして補正する
- `batch_execution_logs` にはテーブルレベルの一意性制約を設けない（`execution_arn` が NULL 許容のため単純な UNIQUE 制約は不適合）。同一実行での二重 INSERT はアプリケーション側で防御する（開始時に 1 回だけ INSERT し、以降は UPDATE のみ）

## 2. 画像生成バッチ

### 2.1 処理フロー

画像生成バッチは、対象セットの `is_active=1` な `prompt_configs` を全件取得し、1 回の実行で各プロンプトを順次処理する。

```
開始（※ DB 準備確認は Step Functions の WaitForDbReady ステートで完了済み。DB は利用可能前提）
  │
  ├── 1. set_code から内部 set_id を取得
  │       - 環境変数 SET_CODE を使って batch_sets テーブルから set_id（内部 PK）を取得する
  │       - 該当する set_code が存在しない場合はエラーログを出力し、終了コード 1 で終了する
  │       - 以降の DB 操作には取得した set_id を使用する
  │
  ├── 2. DB から生成対象のプロンプト一覧を取得
  │       - 対象: set_id に紐づく `is_active=1` の prompt_configs 全件
  │       - 環境変数 SCHEDULED_AT で指定されたスケジュール実行日時を冪等性キーとして使用
  │       - 生成対象がない場合はスキップして正常終了
  │
  ├── 3. 各 prompt_config ごとに順次処理
  │       - （再実行時）同一 (set_id, prompt_config_id, scheduled_at) のレコードがある画像は生成済みと見なしスキップする
  │       - 画像生成 API 呼び出し
  │         - Nano Banana Pro（Gemini 3 Pro 画像 API）
  │         - API 失敗時は Step Functions Retry で再試行
  │       - 生成画像を S3 に保存
  │         - キー: images/{set_code}/{YYYYMMDD}/{uuid}.jpg
  │         - メタデータ: Content-Type: image/jpeg
  │         - Instagram 投稿要件に合わせ JPEG 形式で保存する
  │         - 生成 API が PNG を返す場合は JPEG に変換してから保存する
  │       - メタ情報を DB に登録
  │         - 画像テーブルにレコード挿入
  │         - S3 キー、プロンプト ID、生成日時等
  │         - プロンプト本文・パラメータのスナップショットも保存する
  │         - DB 登録が成功した時点で生成完了とする
  │         - S3 保存成功・DB 登録失敗の場合、S3 に orphan が残るが許容する
  │
  └── 正常終了（終了コード 0）
```

> **画像生成 API のレートリミット考慮**: Gemini API には RPM（requests per minute）・日次クォータが存在する。本設計では `prompt_configs` の `is_active=1` レコードを 1 回のバッチで全件順次処理する方式のため、有効プロンプト件数が増えた場合は API クォータに到達するリスクがある。現時点では運用側でプロンプト件数を抑制することで対処し、将来クォータ起因の失敗が顕在化した場合は SNS 投稿バッチと同様の `IMAGE_BATCH_SIZE_LIMIT` 環境変数による総量制御や、プロンプト間の sleep による間隔制御の導入を検討する。既知の制約は本書セクション 4 を参照。

### 2.2 Step Functions 定義・環境変数

Step Functions ASL 定義と環境変数一覧は [specs/workflow.md](../specs/workflow.md) を参照。

## 3. SNS 投稿バッチ

### 3.1 処理フロー

```
開始（※ DB 準備確認は Step Functions の WaitForDbReady ステートで完了済み。DB は利用可能前提）
  │
  ├── 1. set_code から内部 set_id を取得
  │       - 環境変数 SET_CODE を使って batch_sets テーブルから set_id（内部 PK）を取得する
  │       - 該当する set_code が存在しない場合はエラーログを出力し、終了コード 1 で終了する
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
  │       - 各 sns_account の platform、account_code、ENV_NAME、set_code から Secret 名を組み立て、
  │         Secrets Manager から認証情報を取得する（Secret 名規約は [design/security.md](security.md) を参照）
  │
  ├── 3. 再試行判断（画像・アカウントの組ごと）
  │       - retry 上限チェック: 該当 (image, account) の既存レコード数（= 最大 attempt_number）が
  │         max_post_retries（デフォルト 3）以上の場合はスキップし、ログに警告を出力する
  │         （初回は attempt_number=1、再試行ごとに +1。max_post_retries=3 なら最大 3 回試行）
  │       - pending レコードが存在する場合（同一バッチ実行内での再試行）:
  │         - platform_post_id が NOT NULL → 投稿済み、status を success に更新してスキップ
  │         - platform_container_id が NOT NULL、platform_post_id が NULL → ステップ 5 へ（パブリッシュから再開）
  │         - platform_container_id が NULL → ステップ 4 へ（コンテナ作成から開始）
  │       - pending レコードが存在しない場合（初回、または前回 failed で完了している場合）:
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
  │
  └── 正常終了（終了コード 0）
```

### 3.2 Step Functions 定義・環境変数

Step Functions ASL 定義と環境変数一覧は [specs/workflow.md](../specs/workflow.md) を参照。

### 3.3 重複投稿防止

- 投稿対象の判定は `post_records` テーブルの `status='success'` レコードの有無で行う
- 各 (`generated_image_id`, `sns_account_id`) の組について、`status='success'` のレコードが存在する場合はスキップする
- **排他制御（親行ロック方式）**: 投稿対象の `generated_images` レコードを `SELECT ... FOR UPDATE` でロックし（親行は必ず存在するため、ロック対象が 0 件になる問題を回避）、ロック取得後に `post_records` から `status='success'` の有無を確認してから `pending` を挿入する。UNIQUE 制約 `(generated_image_id, sns_account_id, attempt_number)` により、万一並行 INSERT が発生しても DB レベルで重複を防止する（DuplicateKeyError はアプリ側で捕捉してスキップ）
- 投稿前に `status='pending'` のレコードを挿入（予約）し、API 呼び出し後に status を更新する
- **2 段階フロー**: コンテナ作成 → パブリッシュの各段階で DB に中間状態を記録し、再実行時の復旧判定に使用する
- 再試行はレコードを新規追加する形で履歴を保持する（`attempt_number` をインクリメント）

### 3.4 バッチサイズ制限とレート制御

- **バッチサイズ制限**: 1 回のバッチ実行で処理する投稿数の上限を `BATCH_SIZE_LIMIT` 環境変数で設定する（CDK が Task Definition に設定する。デフォルト値: 50。アプリ側にフォールバック値は持たない）
- **処理順序**: `generated_images.generated_at` の昇順で処理し、古い画像を優先する
- **上限超過時の動作**: 上限に達した時点で処理を終了する。未処理分は次回のスケジュール実行で処理される
- **レート制御**: Instagram Graph API のレート制限に対応するため、プラットフォーム・アカウントごとの投稿間隔を設ける（将来拡張。初期版では BATCH_SIZE_LIMIT による総量制御のみ）
- **バックログ監視**: 未投稿件数が一定閾値を超えた場合はログに WARNING を出力する（閾値は BATCH_SIZE_LIMIT の 3 倍を目安）

#### BATCH_SIZE_LIMIT のチューニング基準

デフォルト値 50 は以下の前提に基づく。実運用の状況に応じて調整する。

| 観点 | 制約 | 備考 |
|---|---|---|
| Instagram Graph API レートリミット | アカウントあたり 200 リクエスト/時間 | 1 投稿あたり 2 API コール。50 件 × 2 = 100 リクエストでリミットの 50% |
| ECS タスクタイムアウト | `sns-post-batch` は 3600 秒 | 50 件の投稿処理が 3600 秒以内に完了するように `BATCH_SIZE_LIMIT` を調整する |
| Presigned URL 有効期限 | 1 時間 | URL は各投稿直前に発行する。長時間ハング時は Step Functions のタイムアウトで打ち切る |

> **調整指針**: API レートリミットエラーが頻発する場合は値を下げる。未投稿のバックログが蓄積する場合は値を上げるか、スケジュール間隔を短縮する。

## 4. 制約事項

本システムにおける既知の制約事項を以下に記載する。現時点では対策を実装せず、実運用で問題が発生した場合に個別に対策を検討する。

| # | 制約事項 | 影響 | 備考 |
|---|---|---|---|
| 1 | SNS 投稿時の S3 Presigned URL の有効期限は 1 時間である | Instagram API 側の処理遅延やネットワーク障害が長時間継続した場合、URL が期限切れとなり投稿が失敗する | 失敗時は `post_records` に `status='failed'` として記録され、次回バッチ実行で再試行される（`max_post_retries` の上限まで）。再試行時に新しい Presigned URL が発行されるため、一時的な遅延であれば自動復旧する |
| 2 | Step Functions Standard にはステートマシンの同時実行数を制限するネイティブ機能がない | 手動実行とスケジュール実行が重なった場合、同一ステートマシンが並行実行される。不要な外部 API コールが発生する可能性がある | DB の UNIQUE 制約と親行ロックにより、データの整合性は保証される。EventBridge Scheduler の実行間隔をバッチ想定実行時間より十分長く設定することで通常運用では回避可能 |
| 3 | S3 Lifecycle Policy により全オブジェクトは作成から 30 日で自動削除される | 30 日以内に投稿されなかった画像は S3 から削除され、以後投稿不可能になる | 通常運用では問題にならない想定。長期間の投稿失敗が続いた場合は、S3 オブジェクトの手動復旧または画像の再生成で対応する |
| 4 | Instagram Graph API の長期アクセストークンは 60 日で失効する | トークン失効後は SNS 投稿バッチが全件失敗する。特定セット・アカウントの Secret がすべて無効になるため、当該アカウントへの投稿は不能になる | 運用側で期限前に手動リフレッシュを行う。Graph API の `GET /oauth/access_token?grant_type=fb_exchange_token` で新トークンを取得し Secrets Manager の値を更新する。自動リフレッシュバッチ化は将来拡張として検討 |
| 5 | `batch_sets.max_post_retries` 超過時の通知がない | ログ WARNING のみの検知のため、長期間気づかれないまま S3 Lifecycle で画像が削除され、当該画像の投稿が恒久的に不能になるリスクがある | 運用初期は `batch_execution_logs` や CloudWatch Logs の目視確認で代替する。将来は専用カスタムメトリクス（例: `PostRetryExceededCount`）を発行し MonitoringStack のアラームで検知する案を検討 |
| 6 | 画像生成 API（Gemini）にレートリミット・日次クォータが存在する | `prompt_configs` の `is_active=1` 件数が増えるとバッチ実行中にクォータ超過が発生し、一部プロンプトの生成が失敗する可能性がある | 現時点は運用側でプロンプト件数を抑制することで対処する。顕在化した場合は `IMAGE_BATCH_SIZE_LIMIT` 環境変数や間隔制御の導入を検討（セクション 2.1 の補足参照） |
