# 開発計画・進捗管理

## 進め方の方針

- **設計（インフラ → アプリ）を先に固め、構築はインフラ → アプリ実装の順に進める**
  - Phase D: インフラ設計の一時 Fix → Phase A: アプリ設計の大枠（上流設計）→ Phase 9: アプリ設計（詳細・前倒し）→ Phase 0〜8: インフラ構築（空回し確認・監視・CI/CD まで）→ Phase 10〜13: アプリ実装（10: 実装準備〔冒頭でアプリ設計の最終 Fix〕→ 11: 画像生成バッチ → 12: SNS 投稿バッチ → 13: 定常運用開始。10-2 で展開）
- **アプリ設計は 2 段階で行う**: 大枠（Phase A）と詳細（Phase 9）に分ける
  - Phase A では仕様の壁打ち・設計書構成の決定・主要方針の骨子までを固め、Phase 9 で詳細化する
  - 経緯 1: 2026-07-06、上流工程に適した生成 AI モデル（Claude Fable 5）の利用期限を機に、Phase 9 の上流部分を Phase A として前倒しした
  - 経緯 2: 2026-07-06、Phase A が想定より早く完了したため、同じ理由で Phase 9（詳細設計）自体も Phase 0 より前に前倒しした。フェーズ名は「Phase 9」のまま維持する（設計書各所の「Phase 9-x で詳細化」参照を有効に保つため）。インフラ構築で得る知見の反映は Phase 10 冒頭の最終 Fix（10-1）で行う
- 各ステップで実際に AWS 上で稼働確認を行い、動作を確認してから次に進む
- 1 ステップ = 1 プロンプトを基本とし、「作る → 確認 → 次へ」のリズムで進める
- 各ステップの完了後、ユーザーが確認方法に従って動作確認を行い、チェックを入れる
- **記録の運用**: ステップ完了時、本ファイルにはチェック + 完了日 + 要点（1〜2 行）のみを記録し、詳細な実施記録（検証内容・決定事項の全文）は [development-log.md](development-log.md) に追記する（計画書の肥大化防止。2026-07-18 に完了フェーズの記録を移管して導入）
- CDK コマンド例では app 内の論理スタック ID（`FoundationStack` など）を指定する。`-c env=prod` により、CloudFormation 上の実スタック名は `Prod-FoundationStack` のように環境名付きで作成される

### 設計 Fix の運用ルール

設計書が Fix しない問題の再発防止ルール（詳細は [docs/index.html](index.html) セクション 4 を参照）:

- 設計書は「**次フェーズの作業に着手できる**」水準で一時 Fix とする。「生成 AI の指摘ゼロ」は Fix 条件にしない
- 生成 AI レビューは**観点を限定**して依頼し、**最大 2 巡**まで
- 指摘は **blocker**（誤り・矛盾・欠落）と**改善提案**に分類し、blocker のみ修正する。改善提案・3 巡目以降の指摘は「設計課題リスト」（本ファイル末尾）に記録する
- インフラ設計書にアプリ仕様を書かない。アプリの論点は [docs/app/index.html](app/index.html) の検討メモへ

## 凡例

- `[ ]` 未着手
- `[x]` 完了
- `[!]` 問題あり・要対応

---

## 完了フェーズのサマリ（Phase D 〜 Phase 8）

設計（Phase D・A・9）とインフラ構築（Phase 0〜8）は 2026-07-06〜07-15 に完了済み。各ステップの実施記録（確認・備考の全文）は [development-log.md](development-log.md) を参照。

| Phase | ゴール（達成済み） |
|---|---|
| Phase D: インフラ設計の一時 Fix | インフラ設計書（docs/infra/）を一時 Fix し、Phase 0〜8 に着手できる状態にする |
| Phase A: アプリ設計の大枠（上流設計） | アプリ仕様の壁打ちを行い、設計書構成・主要方針の骨子を docs/app/ に記載する |
| Phase 9: アプリ設計（詳細）※前倒し | Phase A の大枠を詳細化してアプリ設計書を完成させ、一時 Fix する（本スキーマ DDL 作成含む） |
| Phase 0: ローカル開発基盤の整備 | CDK と Docker がローカルで動く状態にする |
| Phase 0.5: AWS アカウントのクリーンアップ | 過去の残存資材を棚卸し・削除し、きれいな状態から構築を始める |
| Phase 1: CDK プロジェクト初期化 + VPC デプロイ | CDK で最小のリソース（VPC）を AWS に作れることを確認する |
| Phase 2: FoundationStack の段階的構築（低リスクリソース） | Aurora・DB 準備確認以外の共通基盤リソースを構築する |
| Phase 3: FoundationStack の段階的構築（Aurora + DB 準備確認） | Aurora と DB 準備確認タスクを構築する |
| Phase 4: SNS 投稿バッチの空回し | SnsPostBatchStack でパイプラインが動くことを確認する（業務ロジックなし） |
| Phase 5: 画像生成バッチの空回し | EventBridge → Step Functions → ECS Fargate のパイプラインが動くことを確認する |
| Phase 6: DB 接続の疎通（最小） | ECS タスクから Aurora に接続できることを確認する |
| Phase 7: MonitoringStack | バッチ失敗時にアラーム通知が届く |
| Phase 8: CI/CD パイプライン構築 | GitHub push で自動的にビルド・デプロイされる（イメージは空回し版のまま） |

---

## Phase 10: 実装準備

**ゴール**: DB スキーマ・ローカル環境が業務ロジック実装に耐える状態になっている

- [x] **10-1** アプリ設計の最終 Fix（インフラ構築の知見反映）
  - 確認: [docs/app/index.html](app/index.html) の検討メモとインフラ構築（Phase 0〜8）で得た知見を棚卸しし、アプリ設計書に反映されている。blocker のみ修正し、改善提案は設計課題リストに記録されている
  - 備考: 2026-07-15 完了。検討メモ 2 件の反映（設計書の 3 層構造化・生成方式 strategy 構造）、外部 API 名の非固定化（画像生成 API は ChatGPT Images 2.0 へ変更予定。上位ドキュメントから特定 API 名を排除）、運用手順の実態合わせ、未使用 IAM 権限の削除を実施。詳細は [development-log.md](development-log.md) の 10-1 を参照

- [x] **10-2** 実装計画の詳細化 + 開発計画の整理
  - 確認: 本ファイルの「Phase 10 以降」が具体的なステップに展開されている
  - 備考: 2026-07-18 完了。アプリ実装を Phase 10〜13 の 14 ステップへ展開し、あわせて完了フェーズの実施記録を [development-log.md](development-log.md) へ移管（計画書 414 行 → 約 100 行）。詳細は development-log.md の 10-2 を参照

- [x] **10-3** 生成方式カラムの反映（V001 直接修正）
  - 確認: `database/V001__initial_schema.sql` の `batch_sets` に生成方式名カラムがあり、[docs/app/data-model.html](app/data-model.html) セクション 4.1・ER 図と一致している
  - 備考: 2026-07-18 完了。`batch_sets` に `generator_name VARCHAR(50) NOT NULL` を追加（V002 なしの V001 直接修正）し、data-model.html 4.1 の decision にカラム仕様・理由を記録（関連 3 設計書の記述も整合）。あわせて構文検証で検出した複合 FK 5 本の COMMENT 句（MySQL 構文違反。10-4 適用を阻む blocker）を行コメント化で修正。詳細は [development-log.md](development-log.md) の 10-3 を参照

- [x] **10-4** 本スキーマ DDL（V001）の Aurora 適用
  - 確認: Query Editor で V001 を適用し、`SHOW TABLES` で 9 テーブル + CLI（`SHOW CREATE TABLE`）で定義一致を裏取りできている
  - 備考: 2026-07-18 完了。Query Editor で V001 の 9 テーブルを prod Aurora（DB `acps`）へ適用し、Data API CLI で `SHOW TABLES`（9 テーブル + 残置の `connection_test`）と全 9 テーブルの `SHOW CREATE TABLE` の定義一致（複合 FK 5 本含む）を裏取りした。初回実行は接続設定の DB 名の末尾空白（`acps `）で全文エラーになった（トラブルシューティングログ参照）。詳細は [development-log.md](development-log.md) の 10-4 を参照

- [x] **10-5** ローカル開発環境の整備（MySQL compose）
  - 確認: docker-compose 起動（mysql:8.0 + V000/V001 を docker-entrypoint-initdb.d で初期化）→ 両サービス（現行の疎通版）のローカル Docker 実行が V001 スキーマの DB に対して成功する
  - 備考: 2026-07-18 完了。ルートに `docker-compose.yml` を新設（mysql:8.0、`database/` を initdb マウントしファイル名順に自動適用、DB 名は Aurora と同じ `acps`、認証プラグイン・文字コードも Aurora MySQL 3 デフォルトに合わせた）。README を手順化（ルート「ローカル開発環境」新設 + 両サービス README の接続例を実値へ更新）。検証: 初回起動で全 10 テーブル作成 → 両サービスの docker run が exit 0・「DB 接続成功」ログ。詳細は [development-log.md](development-log.md) の 10-5 を参照

---

## Phase 11: 画像生成バッチの業務ロジック実装

**ゴール**: Step Functions 経由で実画像が生成され、S3 + DB に記録される

> 実装の大きいステップ（11-3・11-4）は Codex に委譲し、完了条件に pytest 全パスを含める。設計判断・レビュー・ドキュメント更新は Claude が行う（CLAUDE.md の Codex 連携ルール）。

- [x] **11-1** 初セットの登録と Secret 実値投入
  - 確認: Aurora に `is_active=1` の初セット（`batch_sets` + `prompt_configs`）が登録され、`acps/prod/image/api-key` が実 API キーになっている
  - 備考: 2026-07-19 完了。初セット `fantasy-animals-1`（架空のかわいい動物図鑑）を決定し、セット別設計書 [docs/app/sets/fantasy-animals-1.html](app/sets/fantasy-animals-1.html) を作成（sets/ の初作成。docs/app/index.html にセット一覧を追加）。`batch_sets`（`generator_name='gpt-image-single'`）・`prompt_configs`（プロンプト文言はユーザー決定、1 枚だけ生成されるよう文言で制御）をローカル（`id=1`）& Aurora（`prompt_configs` は失敗試行分の採番消費により `id=2`。詳細は development-log.md 参照）に登録。Aurora への書き込みは Phase 10-4 の役割分担（Query Editor 操作はユーザー、CLI 裏取りは Claude）を踏襲し `aws rds-data execute-statement` で裏取り。画像生成 API キー（`acps/prod/image/api-key`）はユーザーがマネジメントコンソールで実値に差し替え、`LastChangedDate` の更新を CLI で確認（値自体は非取得）。詳細は [development-log.md](development-log.md) の 11-1 を参照

- [x] **11-2** 画像生成 API の疎通確認
  - 確認: 初期方式が使う API（`gpt-image-2`）をローカル小スクリプトで呼び出し、画像が返る
  - 備考: 2026-07-19 完了。実プロンプトで `size=1024x1024, quality=high, n=1` の画像を確認し、`prompt_configs.parameters`（ローカル `id=1`・Aurora `id=2`）に反映。詳細は [development-log.md](development-log.md) の 11-2 を参照

- [x] **11-3** image-batch 共通骨格の実装（Codex 委譲）
  - 確認: pytest 全パス + ローカル MySQL E2E（テスト用フェイク方式）で `generation_runs`・`generated_images`・`batch_execution_logs` に行が入る
  - 備考: 2026-07-19 完了。`services/image-batch` を空回し版から共通骨格（実行ログ INSERT-or-fetch・`generation_runs` 冪等解決・`prompt_configs` ループ + 完了判定・S3 保存・`generated_images` 登録・方式レジストリ〔`fake` のみ〕）に全面書き換え。`shared/acps_shared` に `get_secret_string`・`s3.put_object`・DB セッション UTC 固定を追加。レビューで E2E テストの接続バグ（`pymysql.connect()` 引数名の不一致で常に自己スキップしていた）を検出し Codex に再委譲して修正、ローカル MySQL 起動状態で E2E が実際に実行され green になることを確認済み。詳細は [development-log.md](development-log.md) の 11-3 を参照

- [x] **11-4** 初期方式 gpt-image-single の実装（Codex 委譲）
  - 確認: ローカル E2E で実画像が生成され、S3 保存 + DB 登録まで通る
  - 備考: 2026-07-19 完了。`generators/gpt_image_single.py` を追加（OpenAI Images API・モデル `gpt-image-2`・Pillow で PNG→JPEG 変換）しレジストリに登録。API シークレットは方式モジュールが自分で取得する設計とし、共通骨格（`main.py`/`processing.py`/レジストリ型）は無変更。requirements に `openai`・`Pillow` を追加。実 API を使うローカル E2E（`RUN_REAL_IMAGE_API_E2E=1` でのみ実行、デフォルトは自己スキップ）で実際に実画像を生成し S3（フェイク）保存・DB 登録まで確認済み。`docs/app/batch-flow.html` の方式カタログを更新（仮称表記の解消・ステータス更新）。詳細は [development-log.md](development-log.md) の 11-4 を参照

- [x] **11-5** AWS E2E（パイプライン経由デプロイ + SFN 実行）
  - 確認: 画像生成 SFN の手動実行が SUCCEEDED し、S3 に実画像・`generated_images` / `batch_execution_logs` に行が入る。連鎖起動された sns-posting-sfn（現行疎通版のまま）も成功終了する
  - 備考: 2026-07-19 完了。push（`3e83d62`）で image-batch-pipeline のみ起動（sns-post-batch-pipeline は 11-3 の push で既に更新済みだったため今回は不起動。両タスク定義とも最新化済み）。画像生成 SFN 手動実行（`set_code=fantasy-animals-1`）が SUCCEEDED（所要4分51秒、実画像生成約3分46秒）、連鎖起動された sns-posting-sfn も SUCCEEDED（所要1分46秒、疎通版のまま）。S3 に実画像1枚・`generation_runs`/`generated_images`/`batch_execution_logs`（image_generation, succeeded）にDBレコードを確認。詳細は [development-log.md](development-log.md) の 11-5 を参照

---

## Phase 12: SNS 投稿バッチの業務ロジック実装

**ゴール**: 生成済みの実行が投稿先プラットフォーム（初期スコープ: Instagram）に自動投稿され、重複しない

> 12-3 は Codex に委譲し、完了条件に pytest 全パスを含める。12-1 の Instagram 側準備は外部作業でリードタイムがあるため、Phase 11 と並行して早めに着手してよい。

- [x] **12-1** 投稿先プラットフォームの準備と登録
  - 確認: SNS 認証 Secret（`acps/prod/<set_code>/sns/instagram/<account_code>`）が実値で存在し、`caption_templates`・`sns_accounts` が登録されている
  - 備考: 2026-07-19 完了。ユーザーが Instagram プロアカウント化・Facebook ページ連携・Meta アプリ作成・長期アクセストークン取得（外部作業）を実施し、`acps/prod/fantasy-animals-1/sns/instagram/main-account` を作成（`account_code=main-account`、Instagram ユーザーネーム `dokonimo_inai_zukan`）。`caption_templates`（キャプション文言はユーザー選定・Claude 草案作成）・`sns_accounts` をローカル・Aurora 双方に `id=1` で登録。外部準備の具体手順は今回初めて実施したため、恒久ドキュメントとして [docs/app/operation.html](app/operation.html) セクション 5.1（新設）に一般化して記録し、既存セクション 5.1〜5.4 を 5.2〜5.5 へ繰り下げた。[docs/app/sets/fantasy-animals-1.html](app/sets/fantasy-animals-1.html) セクション 2 も確定内容で更新。詳細は [development-log.md](development-log.md) の 12-1 を参照

- [x] **12-2** Instagram Graph API の疎通確認
  - 確認: ローカルからコンテナ作成（`POST /{ig-user-id}/media`）→ パブリッシュ（`POST /{ig-user-id}/media_publish`）のテスト投稿が成功する
  - 備考: 2026-07-19 完了。11-5 で生成済みの実画像（S3 Presigned URL）でテスト投稿し成功（`platform_post_id=18118130536780845`）。詳細は [development-log.md](development-log.md) の 12-2 を参照。トークン失効日のリマインダー登録（operation.html セクション 5.4）は未実施（別途対応）

- [x] **12-3** sns-post-batch 業務ロジックの実装（Codex 委譲）
  - 確認: pytest 全パス + ローカル E2E（API モック）で `posts` が success まで遷移する
  - 備考: 2026-07-19 完了。`services/sns-post-batch` を空回し版から業務ロジック（投稿対象決定、posts 状態機械 + INSERT-or-skip + Retry 復旧分岐、post_images、キャプション適用、S3 Presigned URL、Secret 規約からの認証情報導出、実行ログ）に全面書き換え。実装前に batch-flow.html へ「コンテナステータスのポーリング」手順を追記（12-2 で確認済みの実際の Graph API 挙動が未反映だったため）。`shared/acps_shared` に `generate_presigned_url` を追加。詳細は [development-log.md](development-log.md) の 12-3 を参照

- [ ] **12-4** AWS E2E（全チェーン実行）
  - 確認: 画像生成 SFN からの全チェーン実行で実投稿がフィードに載り、`posts` が success・`posted_at` 記録
  - 備考: パイプライン push → 画像生成 SFN 手動実行で確認する

- [ ] **12-5** 重複投稿防止・復旧分岐の確認
  - 確認: 同一実行の SFN 再実行等で二重投稿が発生しない。終端状態のスキップ・`published_unconfirmed` の扱いが設計どおり
  - 備考: 旧計画の 8-3 に相当。batch-flow.html セクション 3.2 の復旧分岐を実機で検証する

---

## Phase 13: 定常運用の開始

**ゴール**: EventBridge Scheduler による全自動運用が回っている

- [ ] **13-1** Scheduler 本番化
  - 確認: 本番 cron 式で ENABLED 化され、スケジュール時刻に全チェーンが自動実行・投稿まで成功する
  - 備考: cron 式（投稿時刻・回数）はユーザーが決定。既存プレースホルダ Scheduler を書き換える（[docs/app/operation.html](app/operation.html) セクション 2.1 の注記）。[docs/infra/workflow.html](infra/workflow.html) セクション 1.5 の decision を更新し、3 タグ指定で deploy（[docs/infra/cicd.html](infra/cicd.html) セクション 3.2）

- [ ] **13-2** 本採用に伴う設計書整備と締め
  - 確認: 3 層構造の設計書一式（`docs/app/generators/` の方式設計書新設 + 方式カタログ更新 + `docs/app/sets/<set_code>.html` 最終化）が実態と一致し、設計課題リストの残項目が棚卸しされている
  - 備考: 「方式設計書はセットが本採用した時点で作成」ルールの初適用。実装中に生じた設計乖離も「実装を正とする」ルールで反映する。残課題の例: stacks.html セクション 5 ツリー図の追記（設計課題リスト 2026-07-06）

> 課題「db-readiness-check の Secret パース二重管理」（設計課題リスト 2026-07-14）は本計画のステップに含めない（db-readiness-check に機能変更で手を入れるタイミングで再検討する）。

---

## トラブルシューティングログ

各ステップで発生した問題と解決策を記録する。

| 日付 | Phase-Step | 問題 | 解決策 |
|---|---|---|---|
| 2026-07-18 | 10-3 | V001 の複合 FK 5 本（`generated_images` 2 本・`posts` 3 本）に付けていた `COMMENT` 句が MySQL 構文違反（FOREIGN KEY 制約は COMMENT をサポートしない）。V001 は実 MySQL で未実行のため潜伏しており、10-4 の適用時に ERROR 1064 で失敗するところだった | 10-3 の構文検証（sqlfluff・MySQL 方言）で検出。COMMENT の記載内容を FK 直前の行コメントへ移動して解消（`UNIQUE KEY`・`KEY` の COMMENT は正当な構文のため残置）。全 9 テーブルのパース成功を再検証済み |
| 2026-07-18 | 10-4 | Query Editor での V001 初回実行が全 9 文 `Incorrect database name 'acps '; Error code: 1102` で失敗。接続ダイアログのデータベース名に末尾空白が入っていた（コピペ起因）。テーブルは 1 つも作られない | データベース名を空白なしの `acps` で入力し直して再実行 → 全文成功。Query Editor の接続ダイアログは入力値の前後空白をトリムしないため、DB 名はコピペ後に空白を確認する |

## 設計課題リスト

設計レビューで出た改善提案や、一時 Fix 時に持ち越した論点を記録する（運用ルールは [docs/index.html](index.html) セクション 4 を参照）。

| 日付 | 対象ドキュメント | 課題 | 対応方針 | 対応時期 |
|---|---|---|---|---|
| 2026-07-06 | docs/infra/stacks.html | セクション 5「スタック間のデータ受け渡し」のツリー図に MonitoringStack への入力（SnsPostingSfnArn・AuroraClusterIdentifier・EcsClusterArn・ImageGenerationSfnName）と DbReadinessCheckSgId の記載がない。3.1 出力一覧・3.4 依存スタックには記載済みのため実装は可能 | Phase 7 実装時に実態へ合わせて追記 | Phase 7 |
| 2026-07-06 | docs/app/design-outline.html | セット廃止時「データ（生成画像・投稿履歴）は残す」とあるが、S3 実体はインフラ設計の 30 日ライフサイクルで自動削除される。「残す」対象が DB レコード（メタ情報・投稿履歴）であることの明確化と S3 実体の保持要否の確認が必要 | **解消済み（2026-07-07）**: 「残す」対象は DB レコードのみと確定。S3 実体は 30 日ライフサイクルで自動削除される前提を明記した（[docs/app/data-model.html](app/data-model.html#s3-key) セクション 5、[docs/app/operation.html](app/operation.html#set-retire) セクション 2.2） | Phase 9-3 |
| 2026-07-07 | docs/app/operation.html | Instagram トークン失効日（`token_expires_at`）のリマインドは運用者の手動カレンダー管理としたが、セット数が増えると手運用が破綻する | Secrets Manager を横断的に読み取り失効間近のものを通知する仕組み（Lambda + EventBridge 等）の導入を、管理画面（将来拡張）と合わせて検討する | 未定（将来拡張） |
| 2026-07-07 | docs/app/operation.html | stale データ（`pending`/`container_created` のまま残った生成実行）の検知は専用アラームを持たず、既存の失敗通知を起点にした手動クエリ確認に依存する | セット数・投稿頻度が増えて見落としリスクが高まった場合、stale 行数を CloudWatch カスタムメトリクスとして発行する仕組みの導入を検討する | 未定（将来拡張） |
| 2026-07-07 | docs/infra/security.html, docs/infra/workflow.html | SNS 投稿バッチタスクロールに付与済みの `cloudwatch:PutMetricData`（Namespace=`ACPS`）は、Phase 9-2 でアプリ側は個別カスタムメトリクスを持たず既存の Step Functions 失敗アラーム 1 本に一本化する方針が確定したため、実装しても使用しない権限として残る | **解消済み（2026-07-15、Phase 10-1）**: 使用しないことが確定しているため SnsPostBatchStack のタスクロールから削除した（Step Functions 実行ロール側の `PutMetricData` は `SnsPostStartFailureCount` 発行に使用中のため残置）。経緯は security.html セクション 2.1 の decision に記録 | Phase 10-1 |
| 2026-07-07 | docs/app/batch-flow.html | posts の作成（3.3 手順 1）が Step Functions Retry での再実行時にも毎回 INSERT を試みる記述に読めるが、3.2 の復旧ロジックは既存 pending 行への分岐を前提としており、両者を combine して初めて「行が存在する場合は INSERT をスキップする」という意図が読み取れる。明文化されていないため誤読の余地がある | **解消済み（2026-07-15、Phase 10-1）**: batch-flow.html 3.3 手順 1 を「存在しなければ INSERT（INSERT-or-skip。既存行がある場合は 3.2 の復旧分岐で再開）」と明文化した | Phase 10-1 |
| 2026-07-12 | docs/app/batch-flow.html, docs/app/design-outline.html | D-3 通読時の議論で、セット別生成ロジックの隔離方針（image-batch 内の strategy モジュール構造。方式の割当は DB のセット設定で行う）と、生成方式の設計書分冊ルール（batch-flow.html には契約 + 方式カタログのみ、方式本体は `docs/app/generators/` に 1 方式 1 本の 3 層構造）を合意した。現行のアプリ設計書には未反映 | **解消済み（2026-07-15、Phase 10-1）**: design-outline.html セクション 1.1 を 3 層構造（契約 / 方式 / セット）へ拡張し、batch-flow.html セクション 2.1 に strategy 構造・方式の契約・方式カタログを新設した。検討メモ側にも反映済みを記録 | Phase 10-1 |
| 2026-07-12 | docs/infra/workflow.html | 将来セット間のデプロイ分離（セットごとに使うタスク定義リビジョンを Scheduler payload で固定し、新セットの開発中も既存セットは検証済みイメージで動かし続ける方式）が必要になった場合、Step Functions の RunTask がタスク定義を入力から受け取れる形になっていれば、Scheduler の設定値追加だけで移行できる | **結論（2026-07-15、Phase 10-1 で検討済み）**: 継ぎ目は設けない。デプロイ分離自体を導入しないと決定済みであり、現行のシンプルな family 名参照を維持する。導入を判断する時点で、SFN 改修（タスク定義を入力から受け取る形）とセットで行う | デプロイ分離導入時 |
| 2026-07-14 | services/db-readiness-check | 6-1 で `shared/acps_shared` に DB 接続共通モジュールを作成したが、db-readiness-check は移植元の `app/secrets.py` / `app/db.py` を持ったままで、Secret パース処理が二重管理になっている。統合には db-readiness-check の Dockerfile をルートコンテキスト方式（`COPY shared/`）に変更してイメージを再ビルド・再 push する必要があるため 6-1 では見送った | **6-2 で判断（2026-07-14）**: 統合は見送り。db-readiness-check は Phase 3 で検証済み・全ワークフローの先頭ステートで稼働中の安定コンポーネントであり、二重管理の Secret パース処理は Phase 10 まで双方とも変更予定がない一方、統合にはイメージ再ビルド・再 push・AWS 上の再検証が必要でリスクに見合う実益がないため。db-readiness-check に次に機能変更で手を入れるタイミングで、ルートコンテキスト方式への変更と合わせて統合を再検討する | Phase 10 以降（再検討） |
| 2026-07-15 | docs/infra/workflow.html, docs/app/operation.html | Scheduler は現在、機能名の 1 件（`acps-prod-image-generation-schedule`）のみで、セット別の命名規約が未定義。セット 2 追加時に「セットごとに Scheduler 1 件追加」する際の名前の付け方が決まっていない | セット 2 追加時に命名規約を確定する（既存 1 件のリネーム要否も含めて判断） | セット 2 追加時 |
| 2026-07-15 | docs/infra/security.html | 画像生成 API の複数プロバイダを併用する場合、単一 Secret `acps/{env}/image/api-key` では足りない（生成方式は差し替え可能な strategy 構造のため、将来プロバイダが並存しうる） | provider 軸の Secret 命名拡張（例 `acps/{env}/image/<provider>/api-key`）を security.html の規約改定・IAM プレフィックス確認とセットで、2 プロバイダ併用が現実になった時点で検討する | 2 プロバイダ併用時 |
| 2026-07-15 | docs/app/batch-flow.html | 2 つ目の SNS プラットフォーム追加時、batch-flow.html セクション 3 の Instagram 固有部分（コンテナ作成 → パブリッシュの 2 段階フロー、`published_unconfirmed` の判定条件等）をどう分冊・共通化するかの設計書構造が未定義 | 生成方式の 3 層分冊と同様の考え方（共通フロー + プラットフォーム別分冊）を軸に、追加が現実になった時点で確定する | 2 つ目のプラットフォーム追加時 |
| 2026-07-18 | docs/infra/workflow.html（MonitoringStack の Aurora アラーム） | Aurora の `acps-prod-aurora-cpu-high`（CPU ≥ 80%）と `acps-prod-aurora-memory-low`（FreeableMemory ≤ 256 MB）は、min ACU 0 からの再開直後の低容量状態（0.5〜1 ACU ≒ メモリ 1〜2 GiB）で構造的に鳴りやすい。10-4 の DDL 適用時、再開 + 軽微なアクセスのみで両方が ALARM → 数分で OK 復帰した実績あり（実負荷なし）。定常運用でバッチ起動のたびに同じ通知が届くノイズになる可能性がある | Phase 13 の定常運用開始時に実際の発報状況を見て、しきい値・評価期間（データポイント数）の調整、または再開直後の一時的な高負荷を許容する設計（評価期間の延長等）を見直す | Phase 13 |
