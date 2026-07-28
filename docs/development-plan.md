# 開発計画・進捗管理

## 進め方の方針

- **設計（インフラ → アプリ）を先に固め、構築はインフラ → アプリ実装の順に進める**
  - Phase D: インフラ設計の一時 Fix → Phase A: アプリ設計の大枠（上流設計）→ Phase 9: アプリ設計（詳細・前倒し）→ Phase 0〜8: インフラ構築（空回し確認・監視・CI/CD まで）→ Phase 10〜13: アプリ実装（10: 実装準備〔冒頭でアプリ設計の最終 Fix〕→ 11: 画像生成バッチ → 12: SNS 投稿バッチ → 13: 定常運用開始。10-2 で展開）→ Phase 14〜17: 収益化に向けた機能拡充（14-1 で展開。上位方針は [docs/strategy/business-strategy.html](strategy/business-strategy.html)）
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

- [x] **12-4** AWS E2E（全チェーン実行）
  - 確認: 画像生成 SFN からの全チェーン実行で実投稿がフィードに載り、`posts` が success・`posted_at` 記録
  - 備考: 2026-07-20 完了。push（`9172596`）で両パイプライン（image-batch・sns-post-batch）が起動し、両タスク定義とも最新化（image-batch rev 10 / sns-post-batch rev 6、イメージタグ `9172596f1f2d`）。画像生成 SFN 手動実行 → 連鎖起動された sns-posting-sfn とも SUCCEEDED。投稿対象決定ロジック（最古の未試行生成実行を優先）どおり、今日新規生成した画像（`generation_runs.id=2`）ではなく 11-5 で生成済みだった 2026-07-19 の画像（`generation_runs.id=1`）が実際に投稿された（今日の新規画像は次回実行で投稿対象になる）。`posts`（`id=1, status='success', platform_post_id=18115758976922783, posted_at='2026-07-20 14:09:30'`）・`post_images`・`batch_execution_logs`（`image_generation`/`sns_posting` とも succeeded）を確認。ユーザーが Instagram フィードへの実投稿を目視確認済み。詳細は [development-log.md](development-log.md) の 12-4 を参照

- [x] **12-5** 重複投稿防止・復旧分岐の確認
  - 確認: 同一実行の SFN 再実行等で二重投稿が発生しない。終端状態のスキップ・`published_unconfirmed` の扱いが設計どおり
  - 備考: 2026-07-20 完了。旧計画の 8-3 に相当。本番 Instagram アカウントへの実投稿リスクを避けるため、ユーザー判断でローカル pytest（実 DB + フェイク Graph API）による検証を採用（AWS 上の実 SFN Retry 検証は実施しない）。コードレビューで `instagram_api.py` の分類バグ（`create_container`/`poll_container_status` の通信失敗を `published_unconfirmed` 扱いにしていた。設計は「パブリッシュ要求送信後」のみ対象）を検出・修正。Codex 委譲で `test_e2e_local_mysql.py` に `main()` を同一 `execution_arn` で 2 回連続実行し SFN Retry を模擬するテストを 2 件追加（`container_created` からの再開でコンテナ重複作成・`posts` 重複行なし／終端状態 `published_unconfirmed` はリトライで API 呼び出し自体が発生しない）。詳細は [development-log.md](development-log.md) の 12-5 を参照

---

## Phase 13: 定常運用の開始

**ゴール**: EventBridge Scheduler による全自動運用が回っている

- [x] **13-1** Scheduler 本番化
  - 確認: 本番 cron 式で ENABLED 化され、スケジュール時刻に全チェーンが自動実行・投稿まで成功する
  - 備考: 2026-07-22 完了。既存プレースホルダ Scheduler を 1 日 3 回（7:00 / 12:00 / 21:00 JST、ユーザー決定）・`set_code=fantasy-animals-1` で ENABLED 化し、3 タグ指定 + `--exclusively` で ImageBatchStack のみ deploy。初回の自動実行（12:00 JST）で全チェーン SUCCEEDED・実投稿成功（`posts.id=2`）をユーザーが目視確認。詳細は [development-log.md](development-log.md) の 13-1 を参照

- [x] **13-2** 本採用に伴う設計書整備と締め
  - 確認: 3 層構造の設計書一式（`docs/app/generators/` の方式設計書新設 + 方式カタログ更新 + `docs/app/sets/<set_code>.html` 最終化）が実態と一致し、設計課題リストの残項目が棚卸しされている
  - 備考: 2026-07-23 完了。方式設計書 [docs/app/generators/gpt-image-single.html](app/generators/gpt-image-single.html) を新設（「本採用時に作成」ルールの初適用。実装を正として記述）し、方式カタログ・[sets/fantasy-animals-1.html](app/sets/fantasy-animals-1.html)（Fix 化・パラメータ確定値反映）・stacks.html セクション 5 ツリー図を実態に合わせて更新。あわせて Aurora アラームを 3/3 データポイントへ延長し MonitoringStack をデプロイ（設計課題リストの 2026-07-06・2026-07-18 を解消、残項目を棚卸し）。詳細は [development-log.md](development-log.md) の 13-2 を参照

> 課題「db-readiness-check の Secret パース二重管理」（設計課題リスト 2026-07-14）は本計画のステップに含めない（db-readiness-check に機能変更で手を入れるタイミングで再検討する）。

---

## 次期計画（Phase 14〜17）: 収益化に向けた機能拡充

2026-07-23 の壁打ちで策定。**上位方針（収益化経路・予算・KPI・プラットフォーム展開方針）は [docs/strategy/business-strategy.html](strategy/business-strategy.html) を正とする**（Phase 14-1 で新設した事業戦略層）。優先順位の考え方: 配信面の拡大より先に「リーチ獲得能力（動画・リール）」→「勝負セット投入」→「効果測定」→「当たりが出てからプラットフォーム展開」の順。

### ステップ別の利用モデル・エフォートレベル

2026-07-24 のトークン最適化検討で策定。方針: **壁打ち・設計 Fix・大型委譲成果物のレビューは Fable 5、それ以外の定型ステップは `/model` で最新の Opus に切り替える**。Codex 委譲は terra / high を既定とし、機械的な横展開は luna、大型・新規性の高い実装は sol へ per-call で変更する（CLAUDE.md の Codex 連携ルールを参照）。エフォートは「確実にこなせる最低レベル」を選ぶ。

> 2026-07-28 更新（15-9 の壁打ち）: 生活溶け込み 4 要件のステップ挿入（15-9〜15-12）と旧 15-9〜15-12 → 15-13〜15-16 の再番号付けに伴い表を更新。

> 2026-07-26 更新（15-4 の再検討）: **Opus 5 のリリースに伴い、定型ステップの既定を Opus 4.8 → Opus 5 へ更新**（策定時は Opus 4.8 が最新 Opus だった。Phase 14 の行は当時の実績記録としてそのまま）。Fable 5 の使いどころ（壁打ち・設計 Fix・大型レビュー）は Opus 5 前提で再確認のうえ**維持**をユーザー決定（15-5 の設計 Fix・15-6 の大型レビューとも Fable 5 のまま。理由: 完全自動運用の安全性を担保する判断密度の高い箇所で、1 回きりのコスト影響は限定的）。Sonnet 5 への引き下げは不採用（機械的作業は Codex 委譲済みで、残る Claude 側ステップは AWS 実操作・実 API 中心のため）。

| ステップ | Claude 側（モデル / エフォート） | Codex 委譲（モデル / エフォート） |
|---|---|---|
| 14-5 | Opus 4.8 / high（指示書・diff レビュー・Aurora 裏取り） | terra / high（DDL 生成 + sqlfluff・ローカル適用ループ） |
| 14-6 | Opus 4.8 / high（CDK 小修正は Claude が直接実施） | なし |
| 14-7 | **Fable 5** / デフォルト（大型成果物のレビュー。指示書作成は Opus 4.8 でも可） | **sol** / high（詰まった場合のみ xhigh） |
| 14-8 | Opus 4.8 / high | なし（実 API・対話的のため委譲不向き） |
| 14-9 | Opus 4.8 / high（指示書・diff レビュー） | terra / high（既存パターンの拡張。不安があれば sol） |
| 14-10 | Opus 4.8 / high（トラブル発生時のみ Fable 5 へ切替） | なし |
| 14-11 | Opus 5 / high（原因分析・幾何設計・プロンプト改訂の判断） | terra / high（`_compose_canvas` 実装 + テスト） |
| 14-12 | Opus 4.8 / high（設計課題リストの棚卸しのみ Fable 5 でも可） | なし（docs は Codex 編集禁止） |
| 15-1〜15-4（壁打ち）・15-5（設計 Fix） | **Fable 5** / デフォルト | — |
| 15-6 新方式実装 | **Fable 5** / デフォルト（大型成果物レビュー。指示書作成は Opus 5 でも可） | **sol** / high（14-7 級: 新モジュール 6 段チェーン。詰まった場合のみ xhigh） |
| 15-9（壁打ち）・15-10（設計 Fix） | **Fable 5** / デフォルト | — |
| 15-11 image-batch 拡張実装 | **Fable 5** / デフォルト（大型成果物レビュー。指示書作成は Opus 5 でも可） | **sol** / high（イラスト生成連携 + 全カット合成の新規性。詰まった場合のみ xhigh） |
| 15-12 sns-post-batch ストーリーズ対応 | **Opus 5** / high（指示書・diff レビュー） | terra / high（既存 Graph API パターンの拡張） |
| 15-7〜15-16 のその他（投入・定型ステップ） | **Opus 5** / high（定型の既定。CDK 小修正は Claude が直接実施・詰まった場合のみ Fable 5 へ切替。15-16 の設計課題リスト棚卸しは Fable 5 でも可） | なし（外部作業・実 API の対話的作業・docs のため委譲不向き） |
| Phase 16 設計（壁打ち・設計 Fix） | **Fable 5** / デフォルト | 実装ステップは展開時に割当 |
| Phase 17 調査・着手判断 | **Fable 5** / デフォルト | — |

## Phase 14: コンテンツ生成への一般化（動画・リール対応）

**ゴール**: 画像生成バッチが動画（リール）も生成・投稿できる「コンテンツ生成バッチ」に拡張され、検証用セット（fantasy-animals-1）でリール自動投稿が回っている（KPI マイルストーン M1）

> 初期スコープは「静止画 + 音楽」の簡易動画方式（ffmpeg 等のローカル合成。生成 API 費ほぼゼロ）から開始し、生成 AI 動画方式は generator strategy の差し替えで後から導入する（2026-07-23 壁打ちで合意。初期パラメータ感は 1 日 1 本・10 秒前後・標準画質）。

- [x] **14-1** 事業戦略の明文化とドキュメント体系拡張
  - 確認: [docs/strategy/business-strategy.html](strategy/business-strategy.html) が新設され、体系ガイド・システム概要・CLAUDE.md が整合している。Phase 14〜17 の骨子が本ファイルに展開されている
  - 備考: 2026-07-23 完了。事業戦略層（docs/strategy/）を新設し、2026-07-23 の壁打ち結果（収益化経路 = Meta ボーナス本命・予算月 2 万円上限・KPI M1〜M4・fantasy-animals-1 の検証用位置づけ）を初版として記載。詳細は [development-log.md](development-log.md) の 14-1 を参照

- [x] **14-2** コンテンツ生成（動画）対応の要件壁打ち（A-1 相当）
  - 確認: 壁打ち記録（docs/app/ に新規ノート 1 本。壁打ち記録は 1 回 1 本のパターン）に、要件・初期スコープ（簡易動画方式）・音源ライセンスの調査結果（API 経由のリール投稿では Meta 音楽ライブラリ不可のため自前音源の調達方針が必要）・データモデルへの影響整理が記録されている
  - 備考: 2026-07-23 完了。壁打ち記録は [docs/app/requirements-notes-video.html](app/requirements-notes-video.html)。主な決定: 音源は段階方式（検証用セットは CC0/フリー音源 → 勝負セットで AI 音楽生成を検討。Meta Sound Collection は Meta 限定ライセンスのため不採用）、縦長 1024x1536 生成 + ズーム/パン 10 秒前後の簡易動画、fantasy-animals-1 は全て動画に置換・1 日 1 回へ削減（gpt-image-single 方式は残置）、音源は複数曲ストック + ローテーション（ライセンス証跡必須）、AI 開示はハッシュタグ、share_to_feed=true。データモデル影響（動画メタ情報の置き場・音源テーブル新設・S3 キー規約拡張・posts のメディア種別）を整理。詳細は [development-log.md](development-log.md) の 14-2 を参照

- [x] **14-3** 実装計画のステップ展開
  - 確認: 本ファイルの Phase 14 が具体的なステップ（14-4〜14-11）に展開されている
  - 備考: 2026-07-23 完了。壁打ち記録（[requirements-notes-video.html](app/requirements-notes-video.html)）の決定事項・持ち越し論点を、Phase 11〜13 で実績のある進行パターン（設計 Fix → DDL → データ準備 → 疎通 → Codex 委譲実装 → AWS E2E → 定常運用切替・締め）に沿って 8 ステップへ展開。詳細は [development-log.md](development-log.md) の 14-3 を参照

> 実装の大きいステップ（14-7・14-9）は Codex に委譲し、完了条件に pytest 全パスを含める（CLAUDE.md の Codex 連携ルール）。14-6 の選曲はユーザーの外部作業を含むため、14-4 完了後であれば後続ステップと並行して進めてよい。14-10 のセット切替後は締めのステップ完了まで定時実行が旧頻度（1 日 3 回）のまま動画で走るため、両者は近接して実施する（間隔が空く場合の扱いは 14-10 で判断）。実際には 14-10 で見切れが判明したため、締めの前に 14-11（見切れ対策とプロンプト改訂）を割り込ませ、締めを 14-12 へ繰り下げた。

- [x] **14-4** 動画対応の設計 Fix（データモデル・方式契約・投稿フロー・運用ルール）
  - 確認: 壁打ちの持ち越し論点（[requirements-notes-video.html](app/requirements-notes-video.html) セクション 7）が決定され、data-model.html・batch-flow.html・operation.html が動画対応を含む形で一時 Fix されている（blocker のみ修正、改善提案は設計課題リストへ）
  - 備考: 2026-07-24 完了。主な決定: `generated_images`/`post_images` を `generated_media`/`post_media` にリネームし「生成メディア」に一般化（候補 (a) の発展形。中間静止画は DB 記録なし・S3 のみ）、`posts.media_type ENUM('feed_image','reel')` 追加、`audio_assets` 新設（証跡カラム一元管理・順繰り選曲・0 件はフェイルラウド）、S3 キーに `videos/`・`audio/` を追加、方式契約を「最終メディアを返す」に一般化・方式名 `gpt-image-kenburns`、音源前処理は事前手動（AAC 化まで）、「標準画質」= 1080x1920・30fps・CRF 20 目安・AAC 128kbps・10 秒・ズームイン 1.0→1.08、AI 開示は `#AIart` のみ、カバー画像はデフォルト（先頭フレーム。14-8 実機確認）、ミュート誤検知は週次手動確認。**S3 の 30 日ライフサイクルがバケット全体に掛かっており音源ストックが消える問題を発見** → プレフィックス限定への変更を 14-6 前の必須作業として計画に反映。詳細は [development-log.md](development-log.md) の 14-4 を参照

- [x] **14-5** V002 マイグレーションの作成と適用
  - 確認: V002 DDL がローカル MySQL・Aurora 双方に適用され、`SHOW CREATE TABLE` で定義一致（data-model.html との一致）を裏取りできている
  - 備考: 2026-07-25 完了。14-4 で確定したデータモデル（音源テーブル新設 + 既存テーブルの変更）を `database/V002__video_support.sql` として DDL 化。V001 は Aurora 適用済みのため直接修正せず V002 を新設。ローカル MySQL 8.0 へ V001→V002 を適用し `SHOW CREATE TABLE` 一致 + 音源複合 FK の動作（画像=NULL 許容 / 動画=同一セット音源で成立 / 別セット・不存在は REJECT）を検証。稼働継続のため既存アプリ（image-batch / sns-post-batch）の SQL を新テーブル名へ機械的にリネーム（pytest 全パス）。**Aurora 適用**: 今回は 10-4 の役割分担ではなく、ユーザーの依頼で Claude が Data API 経由で直接適用（9 文全成功）→ Claude が CLI で `SHOW CREATE TABLE` 裏取り（定義一致）。**無停止移行**: push（`fb1d15e`）で両 CodePipeline が走り新タスク定義（image-batch rev 12 / sns-post-batch rev 8、いずれもイメージ `fb1d15e9f436`）を登録、次回 RunTask から新アプリ×新スキーマで稼働。Scheduler 一時停止は classifier にブロックされ未実施だが、次回実行（07:00 JST）前に再デプロイ完了のためミスマッチ窓は解消。初回の実スケジュール実行成功の確認は 07:00 JST 実行時に事後確認。詳細は [development-log.md](development-log.md) の 14-5 を参照

- [x] **14-6** 音源の調達と登録（外部作業含む）
  - 確認: CC0・フリーライセンス音源 3〜5 曲が前処理済みで S3 に配置され、音源テーブルにローカル & Aurora とも登録されている。全曲のライセンス証跡（出典 URL・ライセンス種別・取得日）が記録済み
  - 備考: 2026-07-25 完了。前提作業の **S3 ライフサイクルのプレフィックス限定化**（バケット全体 → `images/`・`videos/` 各 30 日、`audio/` 対象外）を FoundationStack へ実装・デプロイし裏取り済み。音源は Pixabay の 4 曲（Pixabay Content License = 商用可・クレジット不要）をユーザーが選曲・ダウンロード（Pixabay は Cloudflare の bot challenge により自動取得不可のため、ダウンロードはユーザー作業に確定）、Claude が前処理（切り出し 10 秒・ラウドネス正規化・フェード・AAC 化）〜 S3 配置 〜 ローカル & Aurora への `audio_assets` 登録（id=1〜4・`last_used_at` NULL の未使用状態）を実施。**設計書のレシピを実測に基づき改訂**: 単一パス `loudnorm` は実測 2.8 dB のばらつきが出たため **2 パス方式**（解析 → `measured_*` + `linear=true` で適用）に変更し 1.1 dB に収斂 → operation.html に decision として記録。詳細は [development-log.md](development-log.md) の 14-6 を参照

- [x] **14-7** 動画方式 strategy の実装（Codex 委譲）
  - 確認: pytest 全パス + ローカル E2E（実 API）で縦長静止画（1024x1536）→ ffmpeg 合成の MP4（9:16・10 秒前後・ズーム/パン・音源入り・H.264 + AAC）が生成され、S3 保存 + DB 登録まで通る
  - 備考: 2026-07-25 完了。Codex（sol/high）へ委譲し 2 巡で Fix。方式契約を「最終メディアを返す」へ一般化（`generators/contracts.py` に `MediaOutput` / `IntermediateOutput` / `GeneratorResult` / `GeneratorContext` を新設）、`gpt_image_kenburns` を追加・レジストリ登録（gpt-image-single / fake は新契約へ追随、OpenAI 呼び出しは `openai_image.py` に共通化）。共通骨格は S3 キーのプレフィックス・拡張子・Content-Type を `file_format` 駆動に変更し、中間静止画は S3 のみ保存・メタ情報（寸法・尺・`audio_asset_id`）を DB 登録、失敗時 `rollback` でローテーション副作用を残さない。Dockerfile に ffmpeg 追加、ImageBatchStack を 1 vCPU / 2 GB へ引き上げ。**ローカル E2E（実 API + 実 ffmpeg + 実 S3 音源）で 1080x1920・10.0 秒・h264 + aac・4.2 MB の MP4 生成 → DB 登録 → `last_used_at` 更新まで確認**。14-6 の S3 ライフサイクル変更に未追随だった FoundationStack のテストも修正。詳細は [development-log.md](development-log.md) の 14-7 を参照

- [x] **14-8** リール投稿の疎通確認（実 API）
  - 確認: 14-7 で生成した実 MP4 を使い、ローカルからリール投稿（`media_type=REELS` のコンテナ作成 → FINISHED までポーリング → パブリッシュ）のテスト投稿が成功する
  - 備考: 2026-07-25 完了。12-2 と同じ使い捨てスクリプト方式（scratchpad・非コミット、`boto3` + 標準ライブラリ `urllib`）で実 API へ疎通。14-7 のローカル E2E 成果物 MP4（1080x1920 / 30fps / 10.0 秒 / H.264 + AAC 128kbps / 4.2 MB）を S3 へ配置 → presigned URL（1 時間）→ `media_type=REELS` + `share_to_feed=true`・カバー未指定でコンテナ作成 → FINISHED までポーリング → パブリッシュまで成功（`platform_post_id=18363360217208949`、permalink `/reel/DbNiRIcggGq/`）。**実測（14-9 の入力）**: コンテナ作成応答 1.2 秒 / **FINISHED まで 33.5 秒**（間隔 5 秒で 7 回目）/ パブリッシュ応答 10.2 秒 → 動画のポーリングは**間隔 10 秒・上限 10 分**を推奨値として batch-flow.html に反映（SFN タイムアウト・HTTP タイムアウト 30 秒とも見直し不要）。**実機確認 2 件は設計どおり**: カバー画像 = デフォルトで先頭フレーム（公開後の `thumbnail_url` を取得して照合）、`share_to_feed=true` = リールタブとプロフィールのフィード両方に表示（目視）。テスト投稿はユーザーが手動削除。詳細は [development-log.md](development-log.md) の 14-8 を参照

- [x] **14-9** sns-post-batch のリール対応（Codex 委譲）
  - 確認: pytest 全パス + ローカル E2E（API モック）でリール投稿の `posts` が success まで遷移する。既存の画像投稿経路も回帰テストで green
  - 備考: 2026-07-25 完了。Codex（terra/high）へ委譲し 1 巡で Fix。`app/media_types.py` を新設し `file_format='mp4'` → `posts.media_type='reel'` の導出を一元化、`create_container` をメディア種別で分岐（リールは `media_type=REELS` + `video_url` + `share_to_feed=true`、カバーは未指定でデフォルト）、ポーリングを `resolve_poll_settings` でメディア種別ごとに解決（画像 3 秒 × 10 回を維持、**動画 10 秒 × 60 回 = 上限約 10 分**を確定）。14-5 で SQL のみ追随していたモジュール・モデル名を DB 名に合わせてリネーム（`generated_media.py` / `post_media.py` / `GeneratedMediaRef` / `update_post_snapshot`）。**pytest 88 件全パス（ローカル MySQL 起動状態で E2E 4 件も実行、リールシナリオを 1 本追加）**。**CDK 変更は不要と判断**（動画の最大待ち 10 分は `RunSnsPostBatchTask` タイムアウト 3600 秒に収まり、監視アラームは失敗回数ベースで所要時間に依存しないため）。詳細は [development-log.md](development-log.md) の 14-9 を参照

- [x] **14-10** AWS E2E（セット切替 + 全チェーンでリール実投稿）
  - 確認: fantasy-animals-1 の動画方式への切替後、画像生成 SFN からの全チェーン実行でリールが Instagram に実投稿され、`posts` が success・動画メタ情報・実行ログに行が入る
  - 備考: 2026-07-25 完了。**デプロイ**: 未 push の 3 コミット（`aea9224`）を push → 両パイプライン Succeeded（image-batch rev 13 / sns-post-batch rev 9）→ 14-7 の CDK 変更を反映するため `cdk deploy --exclusively ImageBatchStack`（rev 14 = 1 vCPU / 2 GB）。**順序の要点**: CDK はイメージタグを Context 必須のためパイプライン完了後にデプロイし、Scheduler の DISABLE は CDK が `enabled: true` を持つため cdk deploy の後に行う。**切替**: Aurora の 3 レコード（`generator_name` → `gpt-image-kenburns`、`prompt_configs.size` → `1024x1536`、キャプションの `#AIアート` → `#AIart`）を Data API で更新（ローカル MySQL も同期）。**全チェーン実行**: image-batch 3 分 41 秒（うち生成 143 秒）で `generated_media` id=14（mp4 / 1080x1920 / 10 秒 / `audio_asset_id=1`・S3 に MP4 3.8 MiB + 中間静止画）を登録。**判明した挙動**: 投稿対象は「終端状態の posts を持たない最古の generation_run」のため、以前から滞留していた未投稿 run 1 件により**生成と投稿が 1 実行分ずれており**、チェーンからの投稿は 1 本前の静止画になった（自然解消しない）。**リール実投稿**: ユーザー判断で SNS 投稿 SFN を単体実行し `posts` id=14（`media_type='reel'` / success / `platform_post_id=18613826326051098` / permalink `/reel/DbOEiPujvkK/` / 所要 48 秒）を確認。バックログは 0 件になり、初回定時実行は自分の生成分を投稿する状態に揃った。**Scheduler は DISABLED のまま後続ステップへ引き継ぐ**（14-11 を挟んだため ENABLED 化は 14-12）。詳細は [development-log.md](development-log.md) の 14-10 を参照

- [x] **14-11** リール画角の見切れ対策とプロンプト改訂
  - 確認: 動画化で生成画像の全ピクセルが常に可視になり（ズーム終端でも切れない）、新プロンプトで図鑑フォーマットの構成・文字量・トーンが安定して再現される
  - 備考: 2026-07-26 完了。14-10 の実投稿で**画像内の文字が左右で見切れている**ことが判明したため、14-12（定常運用切替）の前に割り込みで実施。**原因**: `scale=-2:1920,crop=1080:1920`（中央クロップで幅の 15.6% 喪失）+ zoompan 1.0→1.08（終盤にさらに各 3.7%）の 2 段階クロップで、最終フレームには元画像の横幅の 78% しか映っていなかった。**対策 (1) 合成方式の変更**: ffmpeg の中央クロップを廃止し、Pillow で「セーフボックスに contain した前景 + 同じ画像をぼかし減光した背景」の 1080x1920 キャンバスを組んでから zoompan に渡す方式へ変更（`_compose_canvas`）。セーフボックスは `出力寸法 / ZOOM_END - SAFE_BOX_MARGIN` として定数から導出するため、**ズーム終端でも元画像の 100% が可視**であることが構造的に保証される。**対策 (2) プロンプト全面改訂**: 1:1 時代の 4 文から、構成（リード文 2 行 / 名前 / ローマ字 / 基本情報 4 項目 / 特徴 3 項目）・文字量・写真トーン・Instagram UI セーフエリア（右端 12%・下端 15%）を明示した文言へ差し替え、Aurora + ローカル MySQL の `prompt_configs.prompt_text` を更新。**検証**: pytest 72 件全パス、実 ffmpeg でズーム終端フレームの切れゼロを確認、実 Images API の試し打ち 3 巡 6 枚で構成の安定を確認。**AWS E2E**: push → パイプライン（タスク定義 rev 15）→ 投稿前レビューのため image-batch を直接 RunTask して `generated_media` id=15 を生成・目視確認 → SNS 投稿 SFN を単体実行し `posts` id=15（reel / success / permalink `/reel/DbORFkeF-eX/`）。バックログは 0 件を維持し、**Scheduler は DISABLED のまま 14-12 へ引き継ぐ**。詳細は [development-log.md](development-log.md) の 14-11 を参照

- [x] **14-12** 定常運用切替と締め（Scheduler 1 日 1 回化・設計書整備）
  - 確認: Scheduler が 1 日 1 回（時刻はユーザー決定）で ENABLED になり、スケジュール時刻の自動実行でリール投稿まで成功している（KPI マイルストーン M1 達成）。設計書一式が実態と一致している
  - 備考: 2026-07-26 完了。**Scheduler**: cron を `cron(0 7,12,21 * * ? *)` → **`cron(0 21 * * ? *)`（1 日 1 回・21:00 JST、時刻はユーザー決定）**へ CDK で変更し `cdk deploy --exclusively ImageBatchStack`。14-10 で手動 DISABLED にしていた State も同デプロイで **ENABLED** に戻ることを実機で確認（CDK テンプレートが `enabled: true` を保持しており、Scheduler の更新 API が全プロパティを送るため）→ 「Scheduler は CDK を単一の正とする」を workflow.html の decision に明記。デプロイ前に未投稿 run のバックログが **0 件**であることを再確認（初回定時実行は自分の生成分を投稿する）。CDK テスト 71 件全パス。**設計書**: 方式設計書 [generators/gpt-image-kenburns.html](app/generators/gpt-image-kenburns.html) を新設（「本採用時に作成」ルール。実装を正として記述し、14-11 の合成仕様〔セーフボックス = 出力寸法/ZOOM_END − マージン、ぼかし背景、スーパーサンプリング〕・選曲・実測値を収録）、方式カタログを更新（kenburns = 採用中 / single = 実装済み・稼働セットなし）、[sets/fantasy-animals-1.html](app/sets/fantasy-animals-1.html) を動画運用へ更新（頻度・音源 4 曲の一覧・キャプションの `#AIart`・使用方式）、gpt-image-single.html の「14-7 で更新予定」記述を実装追随後の内容へ修正、workflow.html 1.5 / app/operation.html の頻度記述を更新、事業戦略書に KPI 状況列を追加し **M1 を達成として記録**。設計課題リストを棚卸し（V001 COMMENT 行の表崩れ修正、投稿ずれ・0 件生成の項目を現状追記、新規 2 件〔1 日 1 回化に伴う当日リカバリ手順の未定義 / Scheduler 手動 DISABLE が deploy で解除される性質〕を追加）。**初回定時実行（07-26 21:00 JST）で成功を確認**: 画像生成 SFN 5 分 22 秒 → SNS 投稿 SFN 2 分 22 秒（チェーン全体 7 分 44 秒）とも SUCCEEDED、`generated_media` id=16（mp4 / 1080x1920 / 10 秒 / `audio_asset_id=3` = 順繰りどおり）→ `posts` id=16（**同一 `generation_run_id=16`** / reel / success / `platform_post_id=18138660886575511`）で、**1 回のチェーンで生成したリールがそのまま投稿された**（14-10 の 1 実行分ずれは再発なし・バックログ 0 件維持・アラーム発報なし・ユーザー目視確認済み）。詳細は [development-log.md](development-log.md) の 14-12 を参照

---

## Phase 15: 勝負セットの投入（セット 2）

**ゴール**: リーチ獲得を狙う勝負セットが投入され、動画中心の自動運用が回っている（KPI M2 への挑戦開始）

> 2026-07-26 にステップ展開（14-12 の事後確認〔初回定時実行〕のみ残した状態で先行実施）し、**同日のユーザーフィードバックで改訂**（経緯・差分の詳細は [development-log.md](development-log.md) の Phase 15 冒頭を参照）。改訂の要点: **(1) 勝負セットは既存セット（gpt-image-kenburns）と生成方式を変える** — 静止画合成の高度化を軸に壁打ちで新方式を確定し、本フェーズで開発する（新方式の追加は「`generators/<方式名>.py` 新規ファイル + レジストリ 1 行」に閉じる strategy 構造〔[batch-flow.html](app/batch-flow.html) セクション 2.1〕。出力がリール用 MP4 である限り sns-post-batch の改修は不要）。**(2) 意思決定は段階的な壁打ちで行う** — 15-1〜15-4 に分割し、各ステップ内でも壁打ちを複数回繰り返してから確定する（前段の見直しが必要になったら戻ってよい）。壁打ち記録は 1 本のノートを 15-1 で新設し 15-4 まで段階更新する。投入ブロック（15-7〜15-12）はセット追加運用手順（[docs/app/operation.html](app/operation.html) セクション 2.1 手順 0〜4）の初回実地検証を兼ねる。外部作業を含む 15-7 は 15-2 完了後、15-8 は 15-4 完了後であれば後続と並行して進めてよい（14-6 と同じ扱い）。

**意思決定ブロック（壁打ち）**

- [x] **15-1** テーマ候補の発散と絞り込み（壁打ち）
  - 確認: 評価軸（リーチを狙える × 独自の世界観〔[事業戦略書](strategy/business-strategy.html) セクション 2 のオリジナリティ対策要件〕× 生成 AI での再現安定性 × 既存セットとの差別化）が定まり、候補の発散から有望 2〜3 案への絞り込みまでが壁打ち記録ノート（新設）に記録されている
  - 備考: 2026-07-26 完了。壁打ち 2 巡で確定 — 評価軸は指定 4 軸 + 運用系 3 軸（ネタ枯渇耐性・新生成方式との相性・権利/炎上リスク）の **7 軸**、言語戦略は**日本語コンテンツ**（ユーザー決定）。視覚系 10 案の発散を経て、ユーザー提示の**「社会人向けロジカルトレーニング」**（クイズ形式リール）に方向転換し一本化（保険案なし）。有望案 = **L1 論理パズル・謎解き + L3 フェルミ推定のミックス編成**、世界観は**出題者キャラクターの固定アセット化**を主軸。急所は誤答リスクの担保（LLM 自己検証 or 人間レビュー付きストック。15-3/15-4 へ持ち越し）。壁打ち記録ノート [docs/app/requirements-notes-set2.html](app/requirements-notes-set2.html) を新設。詳細は [development-log.md](development-log.md) の 15-1 を参照

- [x] **15-2** テーマ・世界観の確定（壁打ち + 試し生成）
  - 確認: 有望案について実 Images API の少数試し打ちで世界観の再現性を確認したうえでテーマ 1 案が確定し、`set_code`・アカウント構成の方向性が決まり、事業戦略書セクション 6（セットポートフォリオ）が更新されている
  - 備考: 2026-07-26 完了。壁打ち 2 巡 + 実 Images API 試し打ち計 11 回で確定 — **テーマ =「社会人向けロジカルトレーニング」**（L1 論理パズル + L3 フェルミ推定のクイズ形式リール・日本語）、出題者キャラは体育会系コーチ路線へのユーザーフィードバックを経て**「脳みそコーチ」**（フラットベクター調・ネイビー×アンバー統一・固定アセット方式）に決定。images/edits の参照画像方式で同一キャラの別ポーズ生成が成立することを確認（C 軸クリア）。**`set_code` = `logic-training-1`**・アカウントは新規専用 1 アカウント（開設は 15-7。以降並行着手可）。技術知見 3 点（gpt-image-2 透過非対応 → アセット制作は gpt-image-1 / 透過指定の確率的無視 → アルファ検査 + リトライ / ポーズ展開時の細部揺れ → 15-13〔旧 15-9〕でリファレンスシート化）を壁打ち記録 [requirements-notes-set2.html](app/requirements-notes-set2.html) セクション 7 に記録し、事業戦略書セクション 6 を更新。詳細は [development-log.md](development-log.md) の 15-2 を参照

- [x] **15-3** コンテンツフォーマットと新生成方式の選定（壁打ち）
  - 確認: 静止画合成の高度化を軸に方式候補（複数カット構成・多段生成チェーン・合成演出の高度化等）を比較し、見せ方・尺・コスト試算（予算適合。事業戦略書セクション 3）・方式契約（[batch-flow.html](app/batch-flow.html) 2.1「最終メディアを返す」）への適合・影響範囲（データモデル / S3 キー規約 / Secret / CDK リソース）の確認を経て方式名が決定している。新しい外部 API を使う場合は疎通確認ステップの挿入を 15-4 で判断する
  - 備考: 2026-07-26 完了。壁打ち 2 巡で確定 — フォーマット = **20 秒・4 カット**（フック → 問題 → カウントダウン 5 秒 → 答え。末尾カードをフックと同型にしてループを閉じる）、方式名 = **`gpt-quiz-multicut`**（LLM 問題生成〔構造化フィールド方式〕→ 自己検証 → 重複検査 → **Pillow 完全プログラム組版（画像 API 不使用）** → ffmpeg 多カット連結の 6 段チェーン。L1/L3 ローテーションは方式内・稼働 prompt_config は 1 件維持）。誤答対策は**完全自動（LLM 自己検証のみ・フェイルラウド。慣らし目視期間なし）**をユーザー決定し、構造ヘッジ 2 点（L1 は機械検証可能な型に寄せる / L3 実数は幅表現で断定しない）を 15-5 へ引き継ぎ。コスト = LLM 月数十円以下・画像 API 定常ゼロで **1 日 3 回でも予算論点なし**。影響範囲 = V003（`quiz_items` 仮）+ S3 `assets/` プレフィックス + Dockerfile 日本語フォント追加のみ（Secret・CDK・sns-post-batch は変更なし見込み。OpenAI テキスト API の疎通確認要否は 15-4 で判断）。詳細は [development-log.md](development-log.md) の 15-3 を参照

- [x] **15-4** 音源方針・運用パラメータの決定と実装ステップの確定（壁打ち）
  - 確認: 音源方針（AI 音楽生成〔Suno 等・単発費用〕への格上げ要否。事業戦略書セクション 3.1 の段階方式）・投稿頻度・アカウント構成が確定し、15-5 以降のステップとモデル・エフォート割当が確定している（疎通確認等のステップ追加が必要な場合は本ファイルへ反映する）
  - 備考: 2026-07-26 完了。壁打ち 1 巡（4 論点同時提示）で確定 — **音源 = CC0/フリー音源を継続**（Suno 格上げは見送り・事業戦略書 3.1 更新。将来 M2 の手応えで再検討余地は残す）+ **SE〔カウントダウンティック・正解チャイム〕を新規採用**（BGM ローテーション外の固定アセット。合成設計・置き場は 15-5）、**投稿頻度 = 1 日 3 回**（朝 7:30・昼 12:30・夜 21:00 JST 目安。時刻の最終確定は 15-15〔旧 15-11〕。重複検査・`quiz_items` は 1 日 3 回前提で 15-5 設計）、**疎通確認ステップは挿入せず** 15-6 ローカル E2E の完了条件に統合、15-5 以降のモデル・エフォート割当を上表に確定（ステップ構成は 8 ステップ据え置き。同日のユーザー指摘〔Opus 5 リリースにより Phase 14 時点の前提が変化〕を受けて再検討し、定型ステップの既定を Opus 4.8 → **Opus 5** へ更新・Fable 5 の使いどころ〔15-5 設計 Fix・15-6 大型レビュー〕は維持をユーザー決定）。アカウント構成は 15-2 決定を維持（名前・ハンドルは 15-7）。15-8 は並行着手可になった。詳細は [development-log.md](development-log.md) の 15-4 を参照

**開発ブロック（新生成方式）**

- [x] **15-5** 新方式の設計 Fix
  - 確認: [batch-flow.html](app/batch-flow.html) 2.1 の方式カタログに新方式の行が追加され、データモデル・S3 キー規約への影響が Fix されている（DDL 変更があれば V003 として作成・適用、なければ不要と明記。V001 の `file_format` COMMENT 課題〔設計課題リスト 2026-07-25〕は V003 を起こす場合に合わせて解消する）。14-4 パターン（blocker のみ修正、持ち越しは設計課題リストへ）
  - 備考: 2026-07-27 完了（Fable 5）。引き継ぎ論点 10 項目（壁打ち記録 8.6 + 9.6）を全決定 — `quiz_items` 新設 + `audio_assets.asset_type`（SE を証跡一元管理へ統合）+ `file_format` COMMENT 解消を **V003** として作成し、ローカル MySQL・Aurora 双方へ適用・検証済み（複合 FK / UNIQUE の動作確認・`SHOW CREATE TABLE` の定義一致込み。Aurora は当日中のユーザー依頼で Data API 適用）。S3 規約に `assets/{set_code}/`（固定アセット・DB 管理なし・固定ファイル名規約）と `audio/{set_code}/se/` を追加。型選択は LRU に代えて**時間帯スロット**（`parameters.slots`・`GeneratorContext` に `scheduled_at` 追加）。LLM 既定 = `gpt-5.6-terra`。検証チェーン 4 段（プログラム検査 → L1 全列挙機械検証 → LLM 独立解答 → 類似度検査〔bigram Jaccard〕）・再生成上限 3 でフェイルラウド。詳細は [development-log.md](development-log.md) の 15-5 を参照

- [x] **15-6** 新方式 strategy の実装（Codex 委譲）
  - 確認: `generators/<方式名>.py` 新規 + レジストリ 1 行 + テストで pytest 全パス、ローカル E2E（実 API）で最終メディア（リール用 MP4）の生成 → S3 保存 → DB 登録まで通る。ローカル E2E の最初に OpenAI テキスト API の最小疎通を確認する（15-4 決定: 既存キー共用のため独立疎通ステップは置かない）。CDK リソース（vCPU / メモリ）の見直し要否を判断済み（14-7 で 1 vCPU / 2 GB へ引き上げた経緯あり）。15-5 決定の共通部変更 2 点を含む: `GeneratorContext` へ `scheduled_at` 追加（[batch-flow.html](app/batch-flow.html) 2.1）・既存 kenburns の選曲クエリへ `asset_type='bgm'` 条件の追随（[data-model.html](app/data-model.html) 4.8）
  - 備考: 2026-07-27 完了（Codex sol / high 委譲・レビューは Fable 5）。`gpt_quiz_multicut.py`（約 1,350 行）+ ユニット/E2E テストを実装し pytest 98 件全パス、実 API ローカル E2E（疎通 → 生成 → 検証 → MP4 → DB 登録）成功。レビューで blocker 3 件を検出・解消 — ①E2E 疎通の `max_output_tokens=4`（Responses API 下限 16 未満）②**ffmpeg 8 入力同時 zoompan のピーク 2.56 GB 実測 → OOM リスクのためセグメント逐次エンコード + concat 連結の 2 パス構成へ再構成（実測 1.13 GB）**③「⏸」が Noto Sans JP 未収録で豆腐 → 矩形描画へ置換。**CDK リソースは 1 vCPU / 2 GB 据え置きと判断**（②の再構成により kenburns と同水準に収まる）。`GeneratorContext` へは `scheduled_at` に加え `quiz_items` INSERT に必要な `generation_run_id` も追加（batch-flow.html 2.1 に追記）。詳細は [development-log.md](development-log.md) の 15-6 を参照

**投入ブロック（セット追加運用手順〔operation.html 2.1〕の初回実地検証）**

- [x] **15-7** Instagram アカウントの開設と Secret 登録（外部作業含む。15-2 完了後に並行可）
  - 確認: 勝負セット用の Instagram プロアカウントが開設され、アクセストークンが Secret 規約（`acps/prod/<set_code>/sns/instagram/<account_code>`）で Secrets Manager に登録済み。トークン失効日の手動リマインダーが登録されている（12-2 で未実施のままの fantasy-animals-1 分もここで合わせて登録する）
  - 備考: 2026-07-27 完了。アカウント確定（**表示名「脳みそコーチのロジトレ」/ ユーザーネーム `nomiso_coach`** = 15-2 の「ロジトレ」系方針どおり・`account_code` = `main-account`）、Meta アプリは**既存流用**（ユーザー決定）。Secret `acps/prod/logic-training-1/sns/instagram/main-account` を作成し、Claude が読み取り専用の Graph API 呼び出しで**トークン実働（`username=nomiso_coach`・権限 5 種すべて付与）を裏取り**（実投稿は 15-14〔旧 15-10〕）。**設計書と実態のズレを 1 件発見**: `debug_token` の実測で両セットのトークンとも `expires_at=0`（無期限）であり operation.html 5.4 の「60 日失効」前提が成立していなかった。実効期限は `data_access_expires_at`（90 日・2026-10-25）で、**同一アプリ×同一ユーザーのため 1 回の再認可で全セットが同時延長される**（15-7 の再認可で `fantasy-animals-1` 分も延長されたことを実測確認）→ リマインダーを**アカウントごと → 全セット 1 件（2026-10-18）に集約**する方針へ改訂（ユーザー決定）し、両 Secret の `token_expires_at` メモを実測値へ更新。operation.html 5.1 / 5.4 を実態へ改訂（既存 FB ページ流用不可・アカウントセンターのクロスポスト確認・既存アプリ再認可時のページ選択注意・`/me/accounts` は Page ID であって `ig_user_id` ではない点・CloudShell での Secret 作成方式）。詳細は [development-log.md](development-log.md) の 15-7 を参照

- [x] **15-8** 音源の調達と登録（外部作業含む。15-4 完了後に並行可）
  - 確認: 15-4 の音源方針（CC0/フリー音源の継続）に沿った BGM 3〜5 曲が前処理（14-6 で確立した 2 パス loudnorm レシピを 20 秒尺に調整）済みで S3 `audio/<set_code>/` に配置され、ライセンス証跡込みで `audio_assets` にローカル & Aurora とも登録されている。SE 2 種（カウントダウンティック・正解チャイム）も CC0 で調達し、15-5 で確定した置き場・証跡方式で登録されている（15-4 決定）
  - 備考: 2026-07-27 完了。**追加要件（朝昼夜のだし分け）を受けて BGM は「各時間帯 1 曲・計 3 曲」構成**（Pixabay Content License）。前処理は 14-6 の 2 パス loudnorm を 20 秒尺へ調整（実測 -14.5 / -13.8 / -14.1 LUFS = ばらつき 0.7 dB）、SE 2 種は loudnorm を掛けずピーク -1.5 dBTP 調整のみ（ティックは 1 秒周期の立ち上がりに合わせ 0.445 秒から 5.0 秒切り出し = 5 打）。S3 は `audio/logic-training-1/{morning,noon,night}/track01.m4a` + `se/{countdown_tick,answer_chime}.m4a`。**`batch_sets` 行の作成を 15-14〔旧 15-10〕から前倒し**（`audio_assets` の FK 前提のため。ローカル id=44 / Aurora id=2）し、`audio_assets` 5 行をローカル & Aurora へ登録・選曲クエリと SE 存在検査の結果まで裏取り済み。詳細は [development-log.md](development-log.md) の 15-8 を参照

> 2026-07-27 要件追加（ユーザー）: **勝負セットの投稿を「フォロワーの生活への溶け込み」方向へ拡張する 4 要件** — (1) 朝・昼・夜での BGM のだし分け（15-8 は S3 キーを `audio/<set_code>/{morning,noon,night}/` のスロット別プレフィックスで先行配置。選曲ロジックのスロット対応は本要件ブロックで実装）(2) 問題（生成プロンプト）の朝昼夜だし分け（15-5 の `parameters.slots` の拡張方向）(3) 動画デザインの朝昼夜だし分け（4) リールに加えて**ストーリーズ投稿**（sns-post-batch 改修が必要 = フェーズ冒頭注記「sns-post-batch の改修は不要」の前提が変わる）+ 問題を**図示した画像**を含む投稿（L1 は `machine_spec` DSL のプログラム描画で図示できる可能性あり。方式選定から壁打ち）。**15-8 完了後に壁打ちステップを挿入し、壁打ちの結論をもってステップを展開・15-9 以降を再番号付けする**（壁打ちはモデル選択方針どおり Fable 5）。**→ 2026-07-28 壁打ち完了（15-9）**: 結論をもって 15-10〜15-12 を挿入し、旧 15-9〜15-12 を 15-13〜15-16 へ再番号付けした（決定内容は 15-9 の備考と壁打ち記録セクション 11 を参照）。

- [x] **15-9** 生活溶け込み 4 要件の壁打ち（方式検証込み）
  - 確認: 4 要件の実現方式が確定し、壁打ち記録に決定事項・検証結果が記録され、結論に基づくステップ展開（15-10〜15-12 の挿入と旧 15-9〜15-12 の再番号付け）が本ファイルへ反映されている
  - 備考: 2026-07-28 完了（Fable 5）。壁打ち 4 巡 + 実 API 検証で確定 — **(1) BGM** = `audio_assets.time_slot` カラム追加（V004）+ `parameters.slots` へ `slot_code` 追加で選曲をスロット対応（LRU はスロット内で維持） **(2) 問題** = slots へ `tone_hint` 追加（朝 = 出勤前のウォームアップ / 昼 = 昼休みの気分転換 / 夜 = 締めのじっくり）し hook・coach_comment の口調へ反映 **(3) デザイン** = スロット別パレット + 時間帯ラベル帯（組版ロジックは共通） **(4) ストーリーズ** = リールと同一 MP4 を同一 SFN 実行内で連続投稿（`media_type=STORIES`・キャプション不可）。`posts` は media_type 別 2 行で独立記録（UNIQUE 拡張 = V004）・ストーリーズ失敗はリール success を巻き戻さずアラームのみ。**図示** = 3 方式を実 API で比較検証（A: LLM figure_spec → Pillow 描画 / B: インフォグラフィック全体を gpt-image-1 生成 / C: 文字なし情景イラスト + プログラム文字描画）し、**B は 4/4 枚で誤字・見切れ・答え示唆・構造崩壊のいずれかが発生し不採用、C を採用**（A は成立したが最終構成で不要化し不採用）。最終形 = **1 run 1 枚の情景イラスト（LLM が `illustration_scene` を出力 → gpt-image-1 medium・文字/答え示唆の描画禁止指示）を全 4 カットに常駐**させ、脳みそコーチ（固定アセット 4 表情 = 現行実装のポーズ構造を流用）とテキストだけがカットごとに変わる（答えカットはイラスト減光）。イラストのズレは「品質の傷」であって誤答ではないと整理（ユーザー決定）し、**15-3 の「画像 API 定常ゼロ」を改訂**（月 ¥600 前後を許容・ユーザー決定）。詳細は [development-log.md](development-log.md) の 15-9 を参照

- [x] **15-10** 生活溶け込み拡張の設計 Fix + V004
  - 確認: V004（`audio_assets.time_slot`・`posts` の UNIQUE への media_type 追加）が作成されローカル & Aurora へ適用済み。方式仕様（`illustration_scene` の検証仕様・イラスト生成失敗時の扱い・全カット合成・コーチ 4 表情・スロット別パレット）・選曲のスロット対応・ストーリーズ投稿フロー（セット単位の有効化方法を含む）が batch-flow.html / data-model.html / operation.html へ反映され、事業戦略書セクション 3 のコスト表（画像 API 定常費の復活）が更新されている。14-4 パターン（blocker のみ修正、持ち越しは設計課題リストへ）
  - 備考: 2026-07-29 完了（Fable 5）。**Aurora への V004 適用は設計 Fix 時点では権限クラシファイアのブロックで未実施だったが、当日中のユーザー依頼を受けて Data API で適用完了**（15-5 と同じ経緯。4 文全成功 + `time_slot` 埋め戻し 3 行 + `SHOW CREATE TABLE` の定義一致を裏取り済み）。引き継ぎ論点 6 項目を全決定し `database/V004__life_fit_extension.sql`（`audio_assets.time_slot` / `posts.media_type` へ `'story'` 追加 + UNIQUE の media_type 拡張 / `batch_sets.stories_enabled`）を作成、ローカル MySQL へ適用・検証済み（SHOW CREATE 確認 + 機能検証: リール行 + ストーリーズ行の 2 行併存 OK・同種別 2 行目は ERROR 1062 で拒否・埋め戻し 3 行済み）。方式仕様 = `illustration_scene` はプログラム検査のみ（必須・最大 200 字。禁止事項・時間帯ムードはコード側固定プロンプトで担保）・イラスト生成失敗はフェイルラウド（縮退なし）・パレットはコード側定数 + `parameters.slots` へ `slot_label` 追加・コーチのイラスト内登場は不採用。**検知経路の正確化 1 件**: 終端状態で確定した投稿失敗は SFN Retry の再実行が成功終了するため `ExecutionsFailed` に現れず、検知は ECS タスク異常終了通知が担う（ストーリーズ失敗も同経路。batch-flow.html 3.4 に明記）。batch-flow.html（方式カタログ・3.1〜3.4）/ data-model.html（4.1 / 4.4 / 4.6 / 4.8 / 5 / 8）/ operation.html（2.1 / 3 / 4）/ 事業戦略書セクション 3（画像 API 定常費の復活 + LLM テキスト API 費目の追加）を更新。詳細は [development-log.md](development-log.md) の 15-10 を参照

- [x] **15-11** image-batch 拡張実装（Codex 委譲）
  - 確認: gpt-quiz-multicut にスロット選曲（`time_slot`）・`tone_hint` 差し込み・スロット別パレット/ラベル・情景イラスト生成（images API・リトライ）と全カット合成が実装され、pytest 全パス、ローカル E2E（実 API）で 3 スロットぶんの MP4 生成まで通る。kenburns の選曲クエリの `time_slot` 追随（NULL 許容）を含む
  - 備考: 2026-07-29 完了（実装 = Codex `gpt-5.6-sol` / high・レビュー + blocker 修正 = Fable 5）。仕様（15-10 の方式仕様・スロットだし分け）どおり実装され pytest 124 件全パス。実 API E2E で **L1 の潜在問題 1 件が顕在化**（15-6 以来 L1 は実 API 未検証で、LLM が `machine_spec` を kind 入れ子・`machine_answer` を非正準形で返し全滅）→ 生成プロンプトに正準形を明示する修正（Claude 直接）で 3 スロット全て MP4 生成まで成功。詳細は [development-log.md](development-log.md) の 15-11 を参照

- [ ] **15-12** sns-post-batch ストーリーズ対応（Codex 委譲）
  - 確認: リール投稿成功後に同一 MP4 を `media_type=STORIES` で連続投稿し、`posts` に media_type 別 2 行が独立記録される（ストーリーズ失敗時もリールの success は保持し、失敗はアラームで検知）。pytest 全パスし、ストーリーズを有効化しない既存セット（fantasy-animals-1）の動作が変わらないことをテストで確認済み

- [ ] **15-13**（旧 15-9）セット別設計書の作成とプロンプト・キャプション設計
  - 確認: `docs/app/sets/<set_code>.html` が作成され（operation.html 2.1 手順 0 の雛形）、**コーチの表情別固定アセット 4 種（hook / question / think / answer。15-2 決定のリファレンスシート方式）が作成され S3 `assets/logic-training-1/` へ配置済み**。15-6 のローカル E2E 基盤を流用した試し打ちで、新方式での最終形（MP4。イラスト常駐 + 表情切替込み）までテーマの構成・世界観が安定して再現される（14-11 のプロンプト設計の知見〔構成の明示・Instagram UI セーフエリア〕を流用）。キャプションテンプレート案に `#AIart` が含まれている

- [ ] **15-14**（旧 15-10）セット登録と投稿前レビュー（試し生成・実投稿）
  - 確認: DB 登録（`batch_sets`〔15-8 で作成済み〕→ `prompt_configs` → `caption_templates` → `sns_accounts` → `audio_assets`〔15-8 で登録済み〕の順。ローカル & Aurora）後、image-batch の直接 RunTask で生成物を目視レビューし（朝昼夜スロットの BGM・パレット・tone_hint の切替確認を含む）、SNS 投稿 SFN の単体実行で新アカウントへの**リール + ストーリーズ**実投稿が success になる（14-11 で実績のある投稿前レビュー方式）

- [ ] **15-15**（旧 15-11）Scheduler 追加と命名規約の確定
  - 確認: セット別 Scheduler の命名規約が確定し（設計課題リスト 2026-07-15。既存 `acps-prod-image-generation-schedule` のリネーム要否の判断を含む）、勝負セットの Scheduler（1 日 3 回: 朝 7:30・昼 12:30・夜 21:00 JST 目安 = 15-4 決定。時刻の最終確定は本ステップ）が CDK で追加・deploy・ENABLED 化されている。workflow.html・operation.html の記述が実態と一致している

- [ ] **15-16**（旧 15-12）定常運用切替と締め（2 セット並行運用・設計書整備）
  - 確認: 2 セット並行の定時実行が双方とも成功して自動運用に入り（KPI M2 への挑戦開始）、方式設計書 `docs/app/generators/<方式名>.html` の新設（「本採用時に作成」ルール）・セット別設計書の Fix・事業戦略書の更新・トークン失効監視の自動化の要否判断（設計課題リスト 2026-07-07）・設計課題リストの棚卸しが済んでいる

---

## Phase 16: インサイト収集と KPI 運用

**ゴール**: 投稿パフォーマンス（再生数・フォロワー等）が自動収集され、KPI 実績（事業戦略書セクション 4.1）が数字で追える

- 骨子: 第 3 のバッチ（インサイト収集）の設計・実装（A-1 壁打ちから将来拡張として織り込み済み。データモデルの拡張余地を使う）。ステップ展開は Phase 15 完了時に行う

---

## Phase 17: プラットフォーム展開

**ゴール**: 当たりの兆しが出たセットを他プラットフォームへ展開する

- 骨子: TikTok を第一候補とする（動画資産の転用。Content Posting API のアプリ審査等の要件は着手時に調査）。X は当面見送り（判断根拠は事業戦略書セクション 5）。着手判断の基準は「勝負セットで M2 到達が目安」。ステップ展開は着手判断時に行う

---

## トラブルシューティングログ

各ステップで発生した問題と解決策を記録する。

| 日付 | Phase-Step | 問題 | 解決策 |
|---|---|---|---|
| 2026-07-18 | 10-3 | V001 の複合 FK 5 本（`generated_images` 2 本・`posts` 3 本）に付けていた `COMMENT` 句が MySQL 構文違反（FOREIGN KEY 制約は COMMENT をサポートしない）。V001 は実 MySQL で未実行のため潜伏しており、10-4 の適用時に ERROR 1064 で失敗するところだった | 10-3 の構文検証（sqlfluff・MySQL 方言）で検出。COMMENT の記載内容を FK 直前の行コメントへ移動して解消（`UNIQUE KEY`・`KEY` の COMMENT は正当な構文のため残置）。全 9 テーブルのパース成功を再検証済み |
| 2026-07-18 | 10-4 | Query Editor での V001 初回実行が全 9 文 `Incorrect database name 'acps '; Error code: 1102` で失敗。接続ダイアログのデータベース名に末尾空白が入っていた（コピペ起因）。テーブルは 1 つも作られない | データベース名を空白なしの `acps` で入力し直して再実行 → 全文成功。Query Editor の接続ダイアログは入力値の前後空白をトリムしないため、DB 名はコピペ後に空白を確認する |
| 2026-07-29 | 15-10 | `docker exec -i acps-mysql mysql ... < V004.sql` で DDL を適用すると、mysql クライアントの既定文字コードが latin1 のため日本語 COMMENT が二重エンコードで保存される（utf8mb4 クライアントで読むと文字化け。latin1 クライアントで読むと一見正常に見えるため気づきにくい） | カラム・インデックスを一度戻してから `--default-character-set=utf8mb4` を付けて再適用し解消。ローカル MySQL への SQL ファイル適用・日本語を含む SQL 実行では同オプションを必須とする（初回起動時の自動適用〔docker-entrypoint-initdb.d〕はサーバー設定で utf8mb4 になるため影響なし） |

## 設計課題リスト

設計レビューで出た改善提案や、一時 Fix 時に持ち越した論点を記録する（運用ルールは [docs/index.html](index.html) セクション 4 を参照）。

| 日付 | 対象ドキュメント | 課題 | 対応方針 | 対応時期 |
|---|---|---|---|---|
| 2026-07-06 | docs/infra/stacks.html | セクション 5「スタック間のデータ受け渡し」のツリー図に MonitoringStack への入力（SnsPostingSfnArn・AuroraClusterIdentifier・EcsClusterArn・ImageGenerationSfnName）と DbReadinessCheckSgId の記載がない。3.1 出力一覧・3.4 依存スタックには記載済みのため実装は可能 | **解消済み（2026-07-23、Phase 13-2）**: ツリー図に MonitoringStack へのエッジ 3 本（auroraCluster・ecsCluster・snsPostingSfnArn）と dbReadinessCheckSg → 両バッチスタックのエッジを実装（各スタックの props）どおり追記した（stacks.html セクション 5 の decision に記録） | Phase 13-2 |
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
| 2026-07-18 | docs/infra/workflow.html（MonitoringStack の Aurora アラーム） | Aurora の `acps-prod-aurora-cpu-high`（CPU ≥ 80%）と `acps-prod-aurora-memory-low`（FreeableMemory ≤ 256 MB）は、min ACU 0 からの再開直後の低容量状態（0.5〜1 ACU ≒ メモリ 1〜2 GiB）で構造的に鳴りやすい。10-4 の DDL 適用時、再開 + 軽微なアクセスのみで両方が ALARM → 数分で OK 復帰した実績あり（実負荷なし）。定常運用でバッチ起動のたびに同じ通知が届くノイズになる可能性がある | **解消済み（2026-07-23、Phase 13-2）**: 定常運用初日の定時実行（2026-07-22 12:00 JST）でも memory-low が発報（1〜6 分で OK 復帰。21:00 の回は非発報 = 毎回ではないが繰り返し発生）しノイズを確認したため、両アラームの DatapointsToAlarm を 2 → 3（5 分 × 3/3 = 15 分継続）へ延長し MonitoringStack をデプロイした（workflow.html セクション 8 の decision に記録）。以後の定時実行で非発報を観察する | Phase 13-2 |
| 2026-07-22 | docs/app/batch-flow.html セクション 3.1, services/sns-post-batch/app/target_selection.py | 投稿対象の選定条件は「有効アカウントに終端状態の posts がない最古の generation_run」のみで、生成画像の存在を条件にしていない。画像生成が全滅して `generated_media`（14-5 のリネーム前は `generated_images`）0 件のまま終わった generation_run が残ると、以後の投稿バッチはその実行を選び続けて RuntimeError（No generated image was found）で失敗し、手動クリーンアップまで新しい生成実行の投稿がブロックされる。フェイルラウド方針（失敗アラーム → stale データ運用による手動復旧）とは整合しており blocker ではない（12-4/12-5 後の Sonnet 作業チェックのコードレビューで検出） | 発生した場合は stale データ運用（[docs/app/operation.html](app/operation.html) セクション 4）で該当 generation_run を手動クリーンアップする。発生が繰り返して運用負荷になる場合は、選定条件に「`generated_media` が 1 件以上存在する」を加える改修（batch-flow.html 3.1 の更新とセット）を検討する。**14-12 の棚卸し時点で発生実績なし**（動画方式では ffmpeg 失敗という新しい全滅経路が増えたため、引き続き観察する） | Phase 15 以降（発生実績を見て判断） |
| 2026-07-24 | docs/app/operation.html | AI 開示ハッシュタグ `#AIart` の付与はキャプションテンプレートに含める運用ルール（テンプレート登録時のチェックリスト）のみで担保しており、システム的な検証（テンプレートに含まれているかのチェックや投稿時の自動付与）はない。テンプレート差し替え時の付け忘れは目視でしか気づけない | セット数・テンプレート更新頻度が増えた場合、投稿バッチ側でのタグ存在チェック（警告ログ）または自動付与の導入を検討する（管理画面の将来拡張と合わせて判断） | 未定（将来拡張） |
| 2026-07-25 | database/V001__initial_schema.sql（`generated_media.file_format`） | カラム COMMENT が「ファイル形式（Instagram 要件により jpg に変換して保存する）」のままで、動画（`mp4`）を含む 14-4 以降の実態とずれている。型は `VARCHAR(20)` のため動作影響はない | **解消済み（2026-07-27、Phase 15-5）**: クイズ方式対応の `V003__quiz_support.sql` で COMMENT を実態（`jpg` / `mp4` 等・S3 キーと `posts.media_type` 導出の入力）へ更新した | Phase 15-5 |
| 2026-07-25 | services/sns-post-batch/app/target_selection.py, docs/app/batch-flow.html セクション 3.1 | 投稿対象は「終端状態の posts を持たない**最も古い** generation_run」のため、未投稿の run が 1 件でも滞留すると以後の投稿が恒常的に 1 実行分遅れ、**自然解消しない**（毎回 1 件ずつ古い方を消化するだけ）。14-10 の全チェーン実行で、生成したリールではなく 1 本前の静止画が投稿されて判明した。投稿自体は成功し続けるため、失敗アラームでは気づけない | 14-10 では SNS 投稿 SFN を単体実行してバックログを消化し解消した（生成なしで投稿 1 本のみ実行できる）。再発時も同じ手順で解消できる。定期的に「未投稿 run の件数」を確認する運用、または滞留件数の可視化（2026-07-07 の stale データ検知の課題と同じ枠組み）を、頻発するようなら検討する。**14-12 で 1 日 1 回に減らしたため、1 件の滞留がそのまま「毎日 1 日遅れの投稿」になり気づきにくさが増した**点に注意（14-12 時点のバックログは 0 件） | Phase 15 以降（発生頻度を見て判断） |
| 2026-07-26 | docs/app/operation.html, docs/infra/workflow.html | 14-12 で投稿頻度を 1 日 1 回に減らしたため、**1 回の失敗がその日の投稿ゼロに直結する**（1 日 3 回のときは残り 2 回で自然にカバーされていた）。失敗アラーム受信後に当日中へ復旧させる手順（画像生成 SFN の手動再実行の可否・締切時刻の目安）が運用ルールとして明文化されていない | 失敗アラームが実際に鳴った際の対応で運用感を掴んでから、operation.html の失敗時ポリシー（セクション 4）に「当日リカバリの手順と判断基準」を追記する。頻度をさらに上げる場合は不要になる可能性がある | Phase 15 以降（失敗実績を見て判断） |
| 2026-07-26 | infra/lib/image-batch-stack.ts | Scheduler の State は CDK テンプレートで `enabled: true` 固定のため、検証のためコンソール・CLI で `DISABLED` にしても次の `cdk deploy`（当該リソースに変更がある場合）で ENABLED に戻る。14-10〜14-12 は意図どおりだったが、**「手動 DISABLE が deploy で無言のうちに解除される」性質は事故につながりうる** | 14-12 で workflow.html セクション 1.5 に「Scheduler の設定は CDK を単一の正とし、手動変更は一時的な検証時のみ」と decision として明記した。長期の停止が必要になった場合は CDK 側で `enabled: false` にして deploy する運用とする（対応不要・注意喚起として記録） | 対応不要（記録のみ） |
| 2026-07-27 | docs/app/data-model.html セクション 4.9（`quiz_items`） | クイズ方式の検証・再生成の過程メタ（再生成回数・自己検証の結果・類似度スコア）は DB に記録しない割り切りとした（観測は CloudWatch Logs のみ）。検証チェーンの実際の NG 率・再生成頻度が運用開始まで見えない | Phase 16 のインサイト収集で問題別パフォーマンス分析を設計する際、必要になれば `quiz_items` へのカラム追加（または検証ログテーブル新設）を検討する。それまでは CloudWatch Logs の構造化ログで観測する | Phase 16 で判断 |
