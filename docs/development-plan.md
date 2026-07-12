# 開発計画・進捗管理

## 進め方の方針

- **設計（インフラ → アプリ）を先に固め、構築はインフラ → アプリ実装の順に進める**
  - Phase D: インフラ設計の一時 Fix → Phase A: アプリ設計の大枠（上流設計）→ Phase 9: アプリ設計（詳細・前倒し）→ Phase 0〜8: インフラ構築（空回し確認・監視・CI/CD まで）→ Phase 10 以降: アプリ実装（冒頭でアプリ設計の最終 Fix）
- **アプリ設計は 2 段階で行う**: 大枠（Phase A）と詳細（Phase 9）に分ける
  - Phase A では仕様の壁打ち・設計書構成の決定・主要方針の骨子までを固め、Phase 9 で詳細化する
  - 経緯 1: 2026-07-06、上流工程に適した生成 AI モデル（Claude Fable 5）の利用期限を機に、Phase 9 の上流部分を Phase A として前倒しした
  - 経緯 2: 2026-07-06、Phase A が想定より早く完了したため、同じ理由で Phase 9（詳細設計）自体も Phase 0 より前に前倒しした。フェーズ名は「Phase 9」のまま維持する（設計書各所の「Phase 9-x で詳細化」参照を有効に保つため）。インフラ構築で得る知見の反映は Phase 10 冒頭の最終 Fix（10-1）で行う
- 各ステップで実際に AWS 上で稼働確認を行い、動作を確認してから次に進む
- 1 ステップ = 1 プロンプトを基本とし、「作る → 確認 → 次へ」のリズムで進める
- 各ステップの完了後、ユーザーが確認方法に従って動作確認を行い、チェックを入れる
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

## Phase D: インフラ設計の一時 Fix

**ゴール**: インフラ設計書（docs/infra/）を一時 Fix し、Phase 0〜8 に着手できる状態にする

- [x] **D-1** 設計書体系の再編とインフラ設計書の HTML 化
  - 確認: [docs/index.html](index.html) から各設計書が辿れる。インフラ設計書 6 本（architecture / stacks / workflow / security / cicd / operation）が HTML で存在する
  - 備考: 2026-07-06 実施・ユーザー確認済み。アプリ設計（旧 batch.md / database.md 等）は docs/_archive/ に退避し、Phase 9 の参考資料とする

- [x] **D-2** 生成 AI レビュー（観点限定・最大 2 巡）
  - 確認: blocker 指摘がゼロ、または修正済みである。改善提案は設計課題リストに記録されている
  - 備考: 2026-07-06 に 2 巡実施（上限到達）。1 巡目: blocker 2 件（Aurora Secret 名の明示指定漏れ / dbReadinessCheckImageTag 未指定時の運用未定義）を修正。2 巡目: 1 巡目修正が生んだ blocker 2 件（synth エラー方式が他スタックデプロイを巻き込む矛盾 / Secret 名変更時の影響の誤記）を修正。改善提案 1 件は設計課題リストに記録。レビュー依頼時は以下のテンプレートを使用する

    > docs/infra/ のインフラ設計書をレビューしてください。
    > 指摘してよいのは「開発計画 Phase 0〜8 の作業を妨げる誤り・矛盾・欠落」（blocker）のみです。
    > 改善提案・ベストプラクティス・将来拡張・アプリ仕様（処理ロジック・テーブル設計）への言及は不要です。
    > 各指摘には、blocker である理由（どのフェーズのどの作業が妨げられるか）を必ず添えてください。

- [x] **D-3** ユーザー通読と一時 Fix 宣言
  - 確認: ユーザーが全インフラ設計書を通読し、疑問点が解消されている
  - 備考: 残った指摘・懸念は設計課題リストに記録して終了する。以降の設計変更は「実装を正とする」ルールで随時反映する。2026-07-12 実施。通読中に cicd.html セクション 2「パイプライン分割」を起点に、複数セット運用時のアプリ資材の持ち方を議論。「セットごとにアプリ資材（コンテナ・パイプライン）を分けるべきか」の疑問に対し、アプリ資材はサービス単位で共有し、セット差分は DB 設定 + image-batch 内の生成方式 strategy モジュールで表現する現行方針を確認。将来の多段生成 AI チェーンによる複雑化・肥大化への対応（生成方式の 3 層分冊、デプロイ分離・資材分離の段階的エスカレーション）を整理し、Phase 10-1 で拾えるよう検討メモ・設計課題リストに記録済み。疑問点は解消し、インフラ設計を一時 Fix とする

---

## Phase A: アプリ設計の大枠（上流設計）

**ゴール**: アプリ仕様の壁打ちを行い、アプリ設計の大枠（設計書構成・主要方針の骨子）を決めて docs/app/ に記載する

> Phase A は D-3 の完了を前提としない（D-3 はユーザー作業のため並行してよい）。成果物は **Phase 9 で見直す前提の一時 Fix** とし、生成 AI レビュー（観点限定・最大 2 巡）は Phase 9-5 でまとめて実施する。詳細設計（テーブル定義・処理フローの詳細・DDL 等）には踏み込まない。

- [x] **A-1** アプリ仕様の壁打ち
  - 確認: ユースケース・投稿運用のイメージ・セットの考え方・失敗時にどうしたいか等が言語化され、docs/app/ 配下に記録されている
  - 備考: 生成 AI と対話しながら要件を言語化する。**設計書はまだ書かない**。[docs/_archive/](_archive/) の旧設計を参考資料としてよい。2026-07-06 実施。壁打ち結果は [docs/app/requirements-notes.html](app/requirements-notes.html) に記録（目的・セットの考え方・投稿運用・失敗時方針・初期/将来スコープ・旧設計との差分・持ち越し論点）

- [x] **A-2** アプリ設計の大枠決め
  - 確認: docs/app/ の設計書構成（ドキュメント一覧と各スコープ）と、主要設計方針の骨子（処理フロー概要・データモデル概要・運用方針）が決まっている
  - 備考: A-1 の壁打ち結果をもとに決める。どこまでを大枠とし、何を Phase 9 に持ち越すかもここで線引きする。2026-07-06 実施。決定内容は [docs/app/design-outline.html](app/design-outline.html) に記録（設計書構成は batch-flow / data-model / operation の 3 分冊で Phase 9-2〜9-4 と 1:1 対応。ユーザーレビューを受け「1 生成実行（1 起動）= 1 投稿（アカウントごと）」を不変条件とし、generation_runs を投稿単位の中心に据えるデータモデル概要（generation_runs / posts / post_images / caption_templates 新設）と「投稿試行のない最古の生成実行を対象とする」投稿フローを定義）

- [x] **A-3** 大枠を踏まえた既存設計の見直し
  - 確認: インフラ設計書 6 本と開発計画を大枠と突き合わせ、矛盾・欠落（blocker）が修正されている。改善提案は設計課題リストに記録されている
  - 備考: 見直し観点の例: `set_code` / `scheduled_at` の意味付け、SNS Secret 規約（`set_code` / `account_code` の定義）、環境変数の受け渡し契約。修正は blocker のみ（設計 Fix の運用ルールに従う）。2026-07-06 実施。blocker 修正 3 分類: (1) workflow.html セクション 5 / security.html セクション 1.2 の「Phase 9 で確定」を design-outline.html セクション 5 の確定済み参照へ更新 (2)「手動での再投稿」表現 3 箇所（workflow / architecture / operation）をインフラの能力（単独実行可能）とアプリ仕様（投稿対象の決定）に分離 (3) 開発計画の文言更新（4-6 備考・9-2〜9-4 確認欄）。Scheduler Input・SNS 投稿 SFN 入力（`set_code` のみ）・Secret 規約の多プラットフォーム整合・1 日複数回実行・IAM 権限は矛盾なしを確認。改善提案 1 件（S3 30 日ライフサイクルと「生成画像は残す」の整理）を設計課題リストに記録

- [x] **A-4** アプリ設計大枠の設計書記載
  - 確認: A-2 で決めた構成に従い、docs/app/ に大枠設計書（HTML、共通スタイル使用）が作成されている
  - 備考: 詳細未定の節は「Phase 9 で詳細化」と明記する。[docs/app/index.html](app/index.html) はアプリ設計の目次ページとして更新する。2026-07-06 実施。骨子版 3 分冊（batch-flow / data-model / operation）を作成し、design-outline.html を親ページ（全体方針・分冊間の整合）へ再編、index.html を目次化。計画レビューでのユーザー要望により**複数セット前提の 2 層構造**（セット追加で増えるのは docs/app/sets/ のセット別設計書 1 本のみ。共通設計書・インフラ設計書・CDK スタックは変更しない）を design-outline セクション 1.1 にルール化し、AI プロンプト生成・AI キャプション等のセット別方式は分冊内の「セット別拡張ポイント」として明示（requirements-notes に追記）。あわせてインフラ設計書 3 箇所（architecture / workflow / operation）の投稿対象決定リンクを batch-flow.html#flow-sns へ更新

---

## Phase 9: アプリ設計（詳細）※Phase 0 より前に前倒しで実施

**ゴール**: Phase A の大枠設計を詳細化してアプリ設計書（docs/app/）を完成させ、一時 Fix する

> 当初はインフラ構築（Phase 0〜8）の完了後に実施する計画だったが、2026-07-06、Phase A が想定より早く完了したため、上流工程に適した生成 AI モデル（Claude Fable 5）の利用期限内に前倒しで実施する。詳細設計に必要なインプット（Phase A の骨子版 3 分冊・一時 Fix 済みインフラ設計・A-3 で整合確認済みの入出力契約）は揃っており、AWS 環境は不要。[docs/_archive/](_archive/) の旧設計（batch.md / database.md / operation.md）を参考資料として活用する。
>
> **前倒しに伴う制約**: (1) スコープは初期構築版（[requirements-notes.html](app/requirements-notes.html) の初期スコープ）に限定し、セット別拡張ポイントは骨子のままとする (2) AWS 作業（本スキーマ DDL の Aurora への適用等）は行わない（Phase 10 で実施） (3) 成果物は一時 Fix とし、インフラ構築で得た知見の反映は Phase 10 冒頭の最終 Fix（10-1）で行う。なお 9-2 と 9-3 は相互依存のため、データモデル（9-3）を軸に往復しながら進めてよい

- [x] **9-1** Phase A 大枠の棚卸し
  - 確認: Phase A の大枠設計書と [docs/app/index.html](app/index.html) の検討メモを棚卸しし、詳細化の作業リスト（各分冊末尾の「詳細化する項目」）に漏れがないことが確認されている
  - 備考: 旧 9-1 の主目的だった「インフラ構築中に得た知見の反映」は前倒しに伴い Phase 10-1 へ移動した。2026-07-06 実施。想定どおり検討メモは空（インフラ構築前のため）で大枠に変更なし。[requirements-notes.html](app/requirements-notes.html) セクション 7・8（旧設計との差分・持ち越し論点）を各分冊末尾の詳細化項目と突き合わせ、漏れがないことを確認した。プロンプト選択方式・失敗時ポリシーのセット別設定は [design-outline.html](app/design-outline.html) セクション 6「分冊横断の将来拡張」に実装時期未定として整理済みで、9-2〜9-4 側での追加対応は不要と判断。blocker なし。9-2 へ進む

- [x] **9-2** バッチ処理フロー設計
  - 確認: Phase A の骨子版（docs/app/batch-flow.html）が詳細化されている
  - 備考: 2026-07-06 実施。主な決定事項: (1) `posts` の状態を `pending/container_created/success/failed/published_unconfirmed` の 5 状態とし、`attempt_number` 相当は持たず `(generation_run_id, sns_account_id)` の 1 行の状態遷移で表現（自動再試行なし方針と整合） (2) SNS 投稿バッチの処理件数は常に最古の未試行生成実行 1 件のみとし、`BATCH_SIZE_LIMIT` は不要と判断 (3) 失敗定義は「対象アカウントのうち 1 つでも success 以外」、終了コードは 0/1 の二値、通知は既存の CloudWatch Alarm（ExecutionsFailed）1 本に一本化 (4) 画像生成はシステムとして「1 prompt_config から複数画像保存」「1 セット複数 prompt_config」の両方に対応させ、初期運用は 1 セット 1 prompt_config（プロンプト文言で 1 枚に制御）という設定値・運用ルールで実現する（ユーザー指摘により、当初案の「複数件はエラー・2 枚目以降は破棄」から修正）。`is_active=1` の prompt_config が 0 件の場合のみ設定ミスとしてエラー終了、1 件以上はすべてループ処理する (5) SNS 投稿バッチは初期構築の仕様として生成実行内の先頭画像 1 枚のみを `post_images` に登録する（投稿は常に 1 枚。カルーセルは将来対応）。データモデルへの申し送り事項（`generated_images.output_index` の追加等）は batch-flow.html セクション 5 に整理し Phase 9-3 の入力とする。docs/_archive/batch.md を参考資料とした（post_records の attempt 方式・BATCH_SIZE_LIMIT は不採用）。design-outline.html・index.html のステータス表記も更新済み

- [x] **9-3** DB スキーマ設計 + 本スキーマ DDL 作成
  - 確認: Phase A の骨子版（docs/app/data-model.html）が詳細化され、`database/` に本スキーマの DDL がある
  - 備考: 2026-07-07 実施。主な決定事項: (1) `generation_runs` を新設し「投稿済みフラグ・生成完了フラグは持たず実体（`posts` / `generated_images`）の存在で導出する」を徹底 (2) SNS 投稿バッチの投稿対象決定クエリを厳密化: 「有効アカウントのうち 1 つでも終端状態（`success`/`failed`/`published_unconfirmed`）に未到達」な生成実行を対象とする定義とし、Step Functions Retry での同一生成実行の再選択（復旧ロジック）と、異常終了時の stale データ挙動（Phase 9-4 持ち越し）を両立させた（`data-model.html` セクション 4.4、`batch-flow.html` セクション 3.1 に反映） (3) `caption_templates` の紐づけ単位をセットに確定し、選定ルール（`is_active=1` を `id` 昇順で 1 件、0 件ならキャプションなしで続行）を定義 (4) `generated_images` に `output_index` を追加し `(generation_run_id, prompt_config_id, output_index)` で一意性・完了判定・S3 キーの整合を取る (5) `posts` は旧 `post_records` を生成実行×アカウント単位に再編し `attempt_number` を廃止、`caption_template_id`/`caption_text_snapshot` 等の中間状態カラムを追加 (6) S3 キー命名規約 `images/{set_code}/{YYYYMMDD}/{generation_run_id}/{prompt_config_id}_{output_index}.jpg` を確定し、セット廃止時に「残す」対象は DB レコードのみで S3 実体は 30 日ライフサイクルで自動削除される旨を明確化（下記設計課題リストの該当項目を解消） (7) セット境界の整合性は複合 FK（`set_id` 非正規化 + `(set_id, id)` UNIQUE）で `generated_images`/`posts` に適用し、`post_images.generated_image_id` の生成実行境界チェックはアプリ層に委ねる既知の割り切りとして明記。DDL は `database/V001__initial_schema.sql` に作成（Aurora への適用は Phase 10）。`data-model.html`・`batch-flow.html`（軽微な厳密化追記）・`design-outline.html`・`index.html`・`operation.html`（S3 実体の記述更新）のステータス表記も更新済み

- [x] **9-4** アプリ運用・セキュリティ（アプリ部分）の設計
  - 確認: Phase A の骨子版（docs/app/operation.html）が詳細化されている
  - 備考: 2026-07-07 実施。主な決定事項: (1) セット追加手順を「設計書雛形 → Secret 作成 → DB 登録（`batch_sets`→`prompt_configs`→`caption_templates`→`sns_accounts`の順）→ Scheduler 追加 deploy → 動作確認」の 5 ステップに具体化しチェックリスト化 (2) プロンプト・キャプション変更を「直接 UPDATE（履歴を残さない）」と「新規 INSERT + 旧行 `is_active=0`（履歴を残す）」の 2 方式で定義し、`prompt_configs` は 0 件化を避けるためトランザクション実行を必須化 (3) 投稿失敗時の手動補正は `attempt_number` 方式を採用せず、`posts` 行を `pending` に戻し `platform_container_id` 等をクリアして「最初から実行」扱いにする方式に確定。あわせて、投稿対象決定が「最古の actionable」優先のため補正しても即座には処理されない場合がある点を明記 (4) stale データ（`pending`/`container_created` のまま残り後続投稿をブロックする生成実行）は専用の自動検知を追加せず、既存の失敗アラームを起点に定期確認クエリで検出し手動補正する運用と確定（自動化は改善提案として設計課題リストへ） (5) SNS Secret 規約 `acps/{env}/{set_code}/sns/{platform}/{account_code}` は変更なしで最終確認とし、既存セットへのアカウント追加手順（Secret 作成 → DB 登録の順）を新規セット追加と分けて明文化 (6) Instagram トークン更新のリマインドは管理画面のない初期スコープでは運用者の手動カレンダー管理とし、自動化は将来課題として記録。docs/_archive/operation.md の `attempt_number`/`max_post_retries` に基づく再試行上限確認は不採用（自動再試行なし方針のため）、SNS アカウント追加手順・手動補正の記録ルール・トークン更新の考え方は引き継いだ。data-model.html・batch-flow.html の relevant クロスリンクも更新済み

- [x] **9-5** 生成 AI レビュー → 一時 Fix
  - 確認: blocker 指摘がゼロ、または修正済み。改善提案は設計課題リストに記録されている
  - 備考: 2026-07-07 実施。Phase D と同じレビュー運用ルール（観点限定・blocker のみ修正）で、docs/app/ 配下 6 本（design-outline / batch-flow / data-model / operation / index / requirements-notes）と database/V001__initial_schema.sql、および参照先のインフラ設計書（workflow.html / security.html / stacks.html / operation.html）との突き合わせを 1 巡実施。全内部リンク（アンカー）の到達性も確認し、欠落なし。**blocker 1 件を発見・修正**: `batch_execution_logs` の `UNIQUE (execution_arn, batch_type)` 制約に対し、実行ログ記録の手順が単純な INSERT のみを想定しており、Step Functions Retry による同一実行内の ECS タスク再起動時（`attempt_count` を +1 する想定のケース）に一意制約違反が起きる矛盾があった。`generation_runs`（batch-flow.html セクション 2）と同じ INSERT-or-fetch パターンを適用する手順を batch-flow.html セクション 1（`#exec-log`）に追記し、data-model.html セクション 4.7 から参照リンクを追加して解消した。2 巡目相当の再確認も実施し、追加の blocker なしを確認。改善提案 3 件（SNS 投稿バッチタスクロールの未使用 `cloudwatch:PutMetricData` 権限、posts 作成手順の INSERT-or-skip の明文化不足、stale データ検知の将来拡張）を設計課題リストに記録（前 2 件は本レビューで新規発見）。これで Phase 9（アプリ設計詳細）は一時 Fix 完了。Phase 10-1 でインフラ構築の知見を踏まえた最終 Fix を行う

> 旧 **9-6**（Phase 10 以降の実装計画の詳細化）は、インフラ構築の知見を踏まえて行うため **10-2** へ移動した（Phase 9 時点でのドラフト作成は可）

---

## Phase 0: ローカル開発基盤の整備

**ゴール**: CDK と Docker がローカルで動く状態にする

- [x] **0-1** AWS CLI のインストール・認証設定
  - 確認: `aws sts get-caller-identity` で自分のアカウントが表示される
  - 備考: 2026-07-12 実施。AWS CLI v2.32.14 が既にインストール済み（`~/.aws/` の認証設定も設定済み）だったため新規作業なし。`aws sts get-caller-identity` でアカウント `516964473143`（IAM ユーザー `takegaharawork`）の表示を確認。デフォルトリージョンは `ap-northeast-1`

- [x] **0-2** AWS CDK CLI のインストール
  - 確認: `cdk --version` でバージョンが表示される
  - 備考: 2026-07-12 実施。AWS CDK CLI v2.1034.0 が既にグローバルインストール済み（`/usr/bin/cdk`、Node.js v22.22.1 / npm 10.9.4）だったため新規作業なし。`cdk --version` でバージョン表示を確認

- [x] **0-3** CDK Bootstrap（初回のみ）
  - 確認: `cdk bootstrap aws://ACCOUNT/REGION` が成功する
  - 備考: 2026-07-12 実施。CDKToolkit スタックが 2025-12-13 に作成済み（テンプレートバージョン 30、状態 `CREATE_COMPLETE`）だったため、`cdk bootstrap aws://516964473143/ap-northeast-1` の再実行は「no changes」で正常終了（冪等）。新規リソース作成なし

- [x] **0-4** Python / Docker の動作確認
  - 確認: `python --version`, `docker run hello-world` が通る
  - 備考: 本プロジェクトは WSL2 + Docker Desktop の WSL integration を有効化する前提。Docker Desktop を使わず WSL 内に直接 Docker Engine を導入する場合は、systemd 有効化やユーザーグループ設定などの手動セットアップが別途必要。2026-07-12 実施。Docker: Docker Desktop（Windows 側インストール済み・未起動）を起動したところ WSL integration 有効で `docker run hello-world` 成功（Docker version 29.1.2）。Python: `python` コマンドは存在せず `python3` で Python 3.8.10（Ubuntu 20.04 標準）を確認。**3.8 は 2024-10 に EOL 済み**のため、ローカルで Python 開発を始める Phase 3-2（db-readiness-check 実装）までに新しいバージョン（3.12 等）の導入を検討する（バッチ本体はコンテナ内の Python を使うため本番影響はなし）

- [x] **0-5** リポジトリのディレクトリ構成を作成
  - 確認: `services/`, `shared/`, `infra/` ディレクトリが存在する
  - 備考: 2026-07-12 実施。`infra/`, `services/db-readiness-check/`, `services/image-batch/`, `services/sns-post-batch/`, `shared/` を作成（Git は空ディレクトリを追跡しないため各ディレクトリに `.gitkeep` を配置）。`database/` は Phase 9 で作成済み。**注意**: 1-1 の `cdk init` は空ディレクトリでないと失敗するため、実施時に `infra/.gitkeep` を削除してから `cdk init` すること。CLAUDE.md / README.md のリポジトリ構成の「未作成」注記も更新済み

---

## Phase 0.5: AWS アカウントのクリーンアップ

**ゴール**: 過去の実験・旧プロジェクトの残存資材を棚卸しし、ユーザー確認のうえ AWS アカウントから完全に削除して、Phase 1 以降の構築をきれいな状態から始める

> 2026-07-12、Phase 1 着手前に AWS アカウント上のごみ資材（過去の実験・旧プロジェクトの残存物）を整理する方針とし、本フェーズを追加した。事前スキャン（ap-northeast-1 のみの簡易確認）で、古い Cloud9 スタック・オーファン S3 バケット 2 つ・Lambda 関数 5 つ・旧 graphicanews プロジェクトの Secret などの削除候補を確認済み。
>
> **保持必須資材（誤削除禁止）**: `CDKToolkit` スタック、`cdk-hnb659fds-*` の S3 バケット / ECR リポジトリ（CDK Bootstrap 一式。0-3 で確認済み）、IAM ユーザー `takegaharawork` と認証情報、デフォルト VPC、アカウント既定のリソース

- [x] **0.5-1** 残存資材の棚卸し（全リージョン + グローバル）
  - 確認: 全リージョンのスキャン結果が「保持 / 削除候補 / 要判断」に分類された棚卸しリストとして提示されている
  - 備考: Resource Groups Tagging API による全リージョン横断スキャン + 主要サービスの個別列挙（CloudFormation / S3 / Lambda / ECR / ECS / RDS / DynamoDB / EC2(インスタンス・EIP・EBS・非デフォルト VPC・SG) / API Gateway / CloudWatch Logs / EventBridge / Step Functions / SNS / SQS / Secrets Manager / Cloud9 / CodePipeline / CodeBuild）、グローバルサービス（IAM ロール・ポリシー・ユーザー / CloudFront / Route 53 / ACM）も確認する。Lambda に紐づく IAM ロール・CloudWatch Logs ロググループ・API Gateway などの付随資材も洗い出す。棚卸しリスト・スキャンスクリプトは作業ファイルとして扱いリポジトリにはコミットしない（記録は本ファイルの備考に残す）
  - 実施記録: 2026-07-12 実施。全 17 リージョン + グローバル（IAM / S3 / CloudFront / Route 53）をスキャンし、**資材が存在するのは ap-northeast-1 のみ**（他 16 リージョンは空。us-east-1 の payment-instrument は支払い手段でリソースではない）。分類結果 — **保持**: CDK Bootstrap 一式（CDKToolkit スタック・S3・ECR・IAM ロール ×5・SSM パラメータ）、IAM ユーザー、デフォルト VPC、サービスリンクロール ×7。**削除候補**: (A) Cloud9 実験一式（スタック `aws-cloud9-test-8401aa...` ※配下 EC2 は終了済みで SG のみ残存・環境・IAM ロール/インスタンスプロファイル）、(B) 2024-07 の Lambda 実験一式（関数 ×4: HelloWorldFunction / gptTest / CustomRuntimes / bash-runtime、ロググループ ×4、IAM ロール ×10、ポリシー ×8）、(C) CI/CD 実験 MyLambdaPipeline 一式（CodePipeline / CodeBuild / EventBridge ルール / ロググループ / IAM ロール ×3・ポリシー ×3）、(D) 旧バッチシステム残骸（空の S3 `pipelinestack-batchsystempipeline...`、ComputeStack 系ロググループ ×5、SFN 自動作成ルール `StepFunctionsGetEventsForECSTaskRule`）、(E) SG `launch-wizard-1`。**要判断**: 旧 graphicanews / Meta アプリ関連一式（S3 `graphica-news-privacy-policy`（privacy.htm 1 件）、Secret `/graphicanews/facebook/credentials`、Lambda + API Gateway `instagram-oauth-callback`（エンドポイント `https://0bd2at3gal.execute-api.ap-northeast-1.amazonaws.com`）、付随ロググループ・IAM ロール・ポリシー `SecretsManagerGetSecretValue`）

- [x] **0.5-2** ユーザー確認・削除対象の確定
  - 確認: 棚卸しリストの全項目について「残す / 消す」をユーザーが判定し、削除対象が確定している
  - 備考: 特に旧 graphicanews 関連（S3 `graphica-news-privacy-policy` / Secret `/graphicanews/facebook/credentials` / Lambda `instagram-oauth-callback`）は、Meta アプリ登録（プライバシーポリシー URL 等）から参照されている可能性があるため要判断。本プロジェクトで同じ Meta アプリを再利用する場合は影響を確認してから判断する
  - 実施記録: 2026-07-12 実施。要判断だった graphicanews 関連の利用状況を追加確認したうえで、ユーザーが全項目を判定した。**追加確認の結果**: S3 `graphica-news-privacy-policy` は静的ウェブサイトとして一般公開中（PublicReadGetObject ポリシー + website hosting 有効。`privacy.htm` 1 件のみ。Meta アプリのプライバシーポリシー URL として登録されている可能性が高い）、Secret `/graphicanews/facebook/credentials` は 2025-12-29 作成で最終アクセスも同日（以降アクセスなし）、Lambda `instagram-oauth-callback` + API Gateway はロググループにイベント 0 件で一度も実行された形跡なし。**ユーザー判定**: 削除候補 (A) Cloud9 実験一式 (B) 2024-07 の Lambda 実験一式 (C) CI/CD 実験 MyLambdaPipeline 一式 (D) 旧バッチシステム残骸 (E) SG `launch-wizard-1` は**すべて削除で確定**（付随する IAM ロール・ポリシー・ロググループ含む）。graphicanews 関連（S3・Secret・Lambda + API Gateway・付随の IAM ロール `instagram-oauth-callback-Role`・ロググループ・ポリシー `SecretsManagerGetSecretValue`）は**全保持**（当初 Secret のみ削除の判定だったが、Lambda が当該 Secret を参照しているため一体で保持に変更）。**0.5-3 の削除対象は 0.5-1 実施記録の (A)〜(E) のみ**

- [x] **0.5-3** 削除の実行（Claude Code が AWS CLI で実行）
  - 確認: 承認済みの削除対象がすべて削除されている（各削除コマンドの成功を確認）
  - 備考: 削除順序: (1) CloudFormation スタック（スタック管理下の資材はスタック削除に任せる） (2) オーファン資材の個別削除。S3 はバージョン・削除マーカー含め空にしてからバケット削除、Secret は `--force-delete-without-recovery` で即時完全削除、Lambda は付随する IAM ロール・ロググループも削除。実行した削除の記録（対象と結果）を本備考に残す
  - 実施記録: 2026-07-12 実施。0.5-2 で確定した (A)〜(E) を AWS CLI で削除、全コマンド成功。**手順1（CFN スタック）**: Cloud9 スタック `aws-cloud9-test-8401aa...` を delete-stack → 削除完了（配下の EC2 `i-0c71d78a983202fea`・InstanceSecurityGroup `sg-004bac3f...` も消滅を確認）。スタック外の Cloud9 環境 `8401aa...` は別リソースのため `cloud9 delete-environment` で個別削除（非同期反映、最終検証で消滅確認）。**手順2**: Lambda ×4（HelloWorldFunction / gptTest / CustomRuntimes / bash-runtime）、CodePipeline `MyLambdaPipeline`、CodeBuild `MyLambdaBuild`、EventBridge ルール `codepipeline-MyLamb-main-707241-rule`（remove-targets 後 delete）、`StepFunctionsGetEventsForECSTaskRule`（マネージドルールのため `--force` で remove-targets/delete）、S3 `pipelinestack-batchsystempipeline...`（空だったため直接 delete-bucket）を削除。**手順3**: ロググループ ×10（Lambda 実験 ×4・codebuild/MyLambdaBuild・ComputeStack 系 ×5）削除。**手順4**: SG `launch-wizard-1`（sg-0aa2697ad7ae73e00）削除。**手順5（IAM）**: インスタンスプロファイル `AWSCloud9SSMInstanceProfile`（role 除去後削除）、ロール ×14（A:AWSCloud9SSMAccessRole / B:bash-runtime・CustomRuntimes・gptTest ×4・HelloWorldFunction ×2・LambdaExecutionRole・CodeDeployServiceRole / C:AWSCodePipelineServiceRole-…・codebuild-MyLambdaBuild-service-role・cwe-role-…）、customer-managed ポリシー ×11（AWSLambdaBasicExecutionRole-* ×8・start-pipeline-execution-…・AWSCodePipelineServiceRole-…・CodeBuildBasePolicy-…）を削除。各ロールにアタッチされていた AWS マネージドポリシー（AWSCloud9SSMInstanceProfile / AWSLambdaBasicExecutionRole / AWSCodeDeployRoleForLambda / AmazonS3FullAccess）は detach のみ（AWS 管理のため非削除）、削除対象ロールにインラインポリシーは無し。**最終検証（当該リージョン）**: CFN=`CDKToolkit` のみ / Cloud9 環境=0 / Lambda=`instagram-oauth-callback` のみ / ロググループ=`/aws/lambda/instagram-oauth-callback` のみ / CodePipeline・CodeBuild・EventBridge=空 / S3=`cdk-hnb659fds-assets…`+`graphica-news-privacy-policy` / 非default SG=0 / IAM ロール=`cdk-hnb659fds-*`5本+`instagram-oauth-callback-Role` / local ポリシー=`SecretsManagerGetSecretValue` のみ / インスタンスプロファイル=0。保持対象（CDK Bootstrap 一式・graphicanews 関連一式）はすべて残存を確認。DELETE_FAILED なし。全リージョン横断の再スキャンとコンソール/請求画面確認は 0.5-4 で実施

- [x] **0.5-4** 削除後の確認（再スキャン）
  - 確認: 0.5-1 と同じスキャンを再実行し、保持対象以外が残っていないこと。ユーザーがコンソール・請求画面でも最終確認
  - 備考: DELETE_FAILED やライフサイクル待ちなど削除しきれないものがあれば原因と対応を記録する
  - 実施記録: 2026-07-12 実施。0.5-1 と同じ範囲（全リージョン横断の Resource Groups Tagging API + ap-northeast-1 の主要サービス個別列挙 + グローバルサービス）を再スキャンし、**保持対象以外は残存ゼロ**を確認。**全リージョン横断（Tagging API・全17リージョン）**: 資材があるのは ap-northeast-1 のみ（CDKToolkit スタック・CDK S3・CDK SSM パラメータ・graphicanews Secret＝すべて保持対象）、us-east-1 の payment-instrument ×2 は支払い手段でリソースではない、他は空。**ap-northeast-1 個別列挙**: CFN=`CDKToolkit` のみ / Lambda=`instagram-oauth-callback` のみ / ECR=`cdk-hnb659fds-container-assets…` のみ / ECS・RDS・DynamoDB・EIP・EBS・非default VPC・非default SG・REST API Gateway・EventBridge ルール・Step Functions・SNS・SQS・Cloud9 環境・CodePipeline・CodeBuild=すべて空 / EC2 インスタンス=0 / HTTP API Gateway=`instagram-oauth-callback`(0bd2at3gal) のみ / ロググループ=`/aws/lambda/instagram-oauth-callback` のみ / Secret=`/graphicanews/facebook/credentials` のみ / S3=`cdk-hnb659fds-assets…`＋`graphica-news-privacy-policy` のみ。**グローバル**: IAM ロール=`cdk-hnb659fds-*` ×5＋`instagram-oauth-callback-Role`（0.5-3 で削除した Cloud9/Lambda 実験/CI-CD 実験系ロールは全消滅、`aws-service-role` パスのサービスリンクロールは除外表示）/ ローカル管理ポリシー=`SecretsManagerGetSecretValue` のみ / インスタンスプロファイル=0（`AWSCloud9SSMInstanceProfile` 消滅）/ IAM ユーザー=`takegaharawork` のみ / CloudFront・Route 53・ACM(ap-northeast-1/us-east-1)=なし。**削除対象 (A)〜(E) の残存はすべてゼロ**、**DELETE_FAILED・ライフサイクル待ちなし**。AWS アカウントは CDK Bootstrap 一式＋graphicanews 関連一式（保持確定）＋アカウント既定リソースのみのクリーンな状態。**ユーザーへのお願い**: 念のため AWS マネジメントコンソールと Billing/Cost Explorer（請求画面）でも最終確認をお願いします

---

## Phase 1: CDK プロジェクト初期化 + VPC デプロイ

**ゴール**: CDK で最小のリソース（VPC）を AWS に作れることを確認する

- [x] **1-1** `infra/` に CDK プロジェクトを初期化（TypeScript）
  - 確認: `cdk synth -c env=prod` でテンプレートが出力される
  - 備考: 2026-07-12 実施。`infra/.gitkeep` を削除後、`cdk init app --language typescript` で初期化（aws-cdk-lib 2.232.1 / aws-cdk CLI 2.1034.0 / TypeScript ~5.9.3 / Jest。`package-lock.json` はコミット対象）。生成物のデフォルトスタック（InfraStack）は使い捨てになるため、本ステップでリソースなしの空の **FoundationStack**（`lib/foundation-stack.ts`）に置換した（1-2 は VPC を足すだけになる）。エントリポイント `bin/infra.ts` は Context `env` を必須化し（未指定・`prod` 以外は明確なエラーで失敗。対応環境は現時点で prod のみ）、実スタック名は README の規約どおり環境名プレフィックス付き（`Prod-FoundationStack`）、リージョンは `ap-northeast-1` 固定、アカウントは CLI 認証情報（`CDK_DEFAULT_ACCOUNT`）から解決する。検証: `npm run build` / `npm test`（空スタック synth テスト 1 件）成功、`cdk ls -c env=prod` → `FoundationStack (Prod-FoundationStack)`、`cdk synth -c env=prod` でテンプレート出力、env 未指定・`env=dev` がエラーになることを確認。CLAUDE.md / README.md の「ディレクトリのみ作成済み」注記から `infra/` を除外済み

- [x] **1-2** FoundationStack に VPC だけ定義
  - 確認: `cdk diff -c env=prod FoundationStack` で差分が見える
  - 備考: VPC の CDK 引数は [docs/infra/stacks.html](infra/stacks.html) セクション 3.1 を参照。2026-07-13 実施。`lib/foundation-stack.ts` に設計書どおりの引数（`maxAzs: 2` / `natGateways: 0` / `subnetConfiguration` は PUBLIC + PRIVATE_ISOLATED の 2 種のみ）で VPC を定義し、後続スタックからの参照用に `public readonly vpc` として公開。CIDR は設計書に指定がないため CDK デフォルト（10.0.0.0/16、サブネットは自動分割）。**留意点**: cdk.json のフィーチャーフラグ `@aws-cdk/aws-ec2:restrictDefaultSecurityGroup: true`（1-1 の cdk init 既定）により、デフォルト SG のルールを全除去するカスタムリソース（Lambda 関数 + IAM ロール各 1）がスタックに含まれる。インバウンド全拒否の維持方針（architecture.html セクション 2.1）と整合するため採用。1-4 のコンソール確認時に VPC 関連以外に Lambda が 1 つ見えるのはこのため。検証: `npm run build` / `npm test`（VPC x1・Public/Isolated Subnet 各 x2・NAT Gateway ゼロ・IGW x1 のアサーション 4 件）成功、`cdk synth -c env=prod` で NAT Gateway を含まないテンプレート出力を確認、`cdk diff -c env=prod FoundationStack` で全リソースが追加差分として表示（スタック未デプロイのため）

- [x] **1-3** VPC をデプロイ
  - 確認: `cdk deploy -c env=prod FoundationStack` 成功
  - 備考: 2026-07-13 実施。デプロイ前確認（`npm run build` / `npm test` / `cdk diff` が全リソース追加のみ・NAT Gateway なし）のうえ `cdk deploy -c env=prod FoundationStack --require-approval never` を実行し、約 65 秒で `CREATE_COMPLETE`。AWS CLI 検証: VPC `vpc-008cb8f0be9c708dc`（10.0.0.0/16・available）、サブネット 4 つ（Public ×2: 10.0.0.0/18@1a・10.0.64.0/18@1c＝パブリック IP 自動割当あり / Isolated ×2: 10.0.128.0/18@1a・10.0.192.0/18@1c）、IGW `igw-060cc53f7b862cb66` アタッチ済み、**NAT Gateway ゼロ**、デフォルト SG はカスタムリソースによりインバウンド・アウトバウンドとも空を確認。コンソールでの目視確認は 1-4 で実施

- [x] **1-4** AWS コンソールで VPC を確認
  - 確認: VPC、Public Subnet x2（各 AZ）、Isolated Subnet x2（各 AZ）が作成されている（NAT Gateway がないことを確認）
  - 備考: スタックに VPC 関連以外の Lambda 関数が 1 つ含まれるのは想定どおり（デフォルト SG のルール除去用カスタムリソース。1-2 の備考を参照）。2026-07-13 ユーザーがコンソールで確認完了

- [x] **1-5** 削除して再作成できることを確認
  - 確認: `cdk destroy -c env=prod FoundationStack` → `cdk deploy -c env=prod FoundationStack` が通る
  - 備考: 2026-07-13 実施。事前確認（`npm run build` / `npm test` 成功、`cdk diff` 差分なし）のうえ `cdk destroy --force` を実行し削除完了（スタック不存在・非 default VPC ゼロを AWS CLI で確認）。**残骸**: デフォルト SG ルール除去用カスタムリソース Lambda のロググループ `/aws/lambda/Prod-FoundationStack-CustomVpcRestrictDefaultSGCus-*` は CFN 管理外のため destroy 後も残存 → 手動削除した。destroy するたびに残る点は今後も留意（Lambda 関数名にランダムサフィックスが付くため、再デプロイ後の destroy でも別名で残る）。その後 `cdk deploy --require-approval never` で再作成し約 62 秒で `CREATE_COMPLETE`。再作成後の検証（1-3 と同じ観点）: 新 VPC `vpc-00b1327fb58e687a0`（10.0.0.0/16・available）、Public Subnet ×2（10.0.0.0/18@1a・10.0.64.0/18@1c＝パブリック IP 自動割当あり）、Isolated Subnet ×2（10.0.128.0/18@1a・10.0.192.0/18@1c）、IGW `igw-09a0e50d3ec962d56` アタッチ済み、**NAT Gateway ゼロ**、デフォルト SG はインバウンド・アウトバウンドとも空。構成は 1-3 と同一（リソース ID のみ新規）で「壊して作り直せる」ことを確認

---

## Phase 2: FoundationStack の段階的構築（低リスクリソース）

**ゴール**: Aurora・DB 準備確認以外の共通基盤リソースを構築する

- [ ] **2-1** S3 バケットを追加
  - 確認: コンソールでバケットが見える、`aws s3 cp` でファイルアップロードできる
  - 備考:

- [ ] **2-2** Security Group を追加
  - 確認: コンソールで SG が見える
  - 備考: ルール詳細は [docs/infra/stacks.html](infra/stacks.html) セクション 3.1 を参照

- [ ] **2-3** Secrets Manager（画像生成 API キーの箱）を追加
  - 確認: コンソールで `acps/prod/image/api-key` のシークレットが見える
  - 備考: 画像 API キー用 Secret は CDK で「箱」のみ作成する。実際の API キー値の設定はアプリ実装フェーズ（Phase 10 以降）で行う。DB 接続情報の Secret は Aurora 作成時（Phase 3-1）に `acps/prod/db/credentials` として作成される

- [ ] **2-4** ECS Cluster を追加
  - 確認: コンソールでクラスターが見える
  - 備考:

- [ ] **2-5** ECR リポジトリを追加（image-batch、sns-post-batch、db-readiness-check の 3 つ）
  - 確認: コンソールで 3 つの ECR リポジトリが見える
  - 備考: ECR リポジトリは FoundationStack で一元管理する（[docs/infra/stacks.html](infra/stacks.html) 参照）

- [ ] **2-6** VPC Endpoint（S3 Gateway のみ）を追加
  - 確認: コンソールで S3 Gateway VPC Endpoint が作成されている（Secrets Manager Interface Endpoint は不要）
  - 備考: Secrets Manager へのアクセスは ECS Fargate のパブリック IP 経由で行う

---

## Phase 3: FoundationStack の段階的構築（Aurora + DB 準備確認）

**ゴール**: Aurora と DB 準備確認タスクを構築する

- [ ] **3-1** Aurora Serverless v2 を追加
  - 確認: コンソールで DB クラスターが見える、自動一時停止が設定されている、最小 ACU が 0 になっている。Secrets Manager に `acps/prod/db/credentials` が作成されている
  - 備考: Aurora MySQL 3.08.0 以降など、自動一時停止対応バージョンを採用する。Phase 4 以降の Step Functions 空回しは DB 準備確認タスクに依存するため、Aurora は Phase 4 より前に作成する。CDK 引数は [docs/infra/stacks.html](infra/stacks.html) セクション 3.1 を参照

- [ ] **3-2** `services/db-readiness-check/` に DB 準備確認用の Python + Dockerfile を作成し、ECR に push
  - 確認: ECR コンソールでイメージが見える
  - 備考: DB 接続リトライ（指数バックオフ、最大 8 回）を実装する。詳細は [docs/infra/workflow.html](infra/workflow.html) セクション 2 を参照。ECR push 時は不変タグ（例: Git コミットハッシュ）を使用する。以降の db-readiness-check 更新時は [docs/infra/cicd.html](infra/cicd.html) セクション 2 の手順を参照

- [ ] **3-3** DB 準備確認 ECS タスク定義を FoundationStack に追加し、手動 RunTask で疎通確認
  - 確認: Aurora が起動状態のとき: CloudWatch Logs に接続成功ログが出力され、終了コード 0 で終了する
  - 備考: `cdk deploy -c env=prod -c dbReadinessCheckImageTag=<tag> FoundationStack` でタスク定義を作成する（`<tag>` は Phase 3-2 で ECR push した不変タグ）。Aurora が一時停止状態からのリトライ確認は Phase 6-5 で実施する

---

## Phase 4: SNS 投稿バッチの空回し

**ゴール**: SnsPostBatchStack でパイプラインが動くことを確認する（業務ロジックなし）

- [ ] **4-1** `services/sns-post-batch/` に Hello World の Python + Dockerfile を作成
  - 確認: `docker build` & `docker run` でローカル動作確認
  - 備考:

- [ ] **4-2** ECR リポジトリ（Phase 2-5 で作成済み）に手動で Docker イメージを push
  - 確認: ECR コンソールでイメージが見える
  - 備考:

- [ ] **4-3** SnsPostBatchStack に ECS Task Definition を定義してデプロイ
  - 確認: `cdk deploy -c env=prod SnsPostBatchStack` 成功
  - 備考:

- [ ] **4-4** 手動で ECS RunTask を実行
  - 確認: CloudWatch Logs に「Hello World」が出る
  - 備考: ここが最重要確認ポイント

- [ ] **4-5** Step Functions ステートマシンを追加してデプロイ
  - 確認: `cdk deploy -c env=prod SnsPostBatchStack` 成功、コンソールでステートマシンが見える
  - 備考: ASL 定義は [docs/infra/workflow.html](infra/workflow.html) セクション 4 を参照

- [ ] **4-6** Step Functions 手動実行による E2E 確認（WaitForDbReady → ECS タスク実行の一連フロー）
  - 確認: コンソールから手動実行 → DB 準備確認 → SNS 投稿 ECS タスク起動 → 成功（全ステートが正常遷移）
  - 備考: Phase 4-5 は Step Functions の追加デプロイのみ。4-6 は WaitForDbReady を含む一連フローの動作確認。手動実行 input は `{"set_code":"test-set-1"}` のように `set_code` を必ず渡す（空回し段階ではダミー値でよい。意味付けは [docs/app/design-outline.html](app/design-outline.html) セクション 5 で確定済み）。Phase 5 で ImageBatchStack に EventBridge Scheduler を追加し、SNS 投稿は画像生成成功後に自動起動される

---

## Phase 5: 画像生成バッチの空回し

**ゴール**: EventBridge → Step Functions → ECS Fargate のパイプラインが動くことを確認する（業務ロジックなし）

- [ ] **5-1** `services/image-batch/` に Hello World の Python + Dockerfile を作成
  - 確認: `docker build` & `docker run` でローカル動作確認
  - 備考:

- [ ] **5-2** ECR リポジトリ（Phase 2-5 で作成済み）に手動で Docker イメージを push
  - 確認: ECR コンソールでイメージが見える
  - 備考:

- [ ] **5-3** ImageBatchStack に ECS Task Definition を定義してデプロイ
  - 確認: `cdk deploy -c env=prod ImageBatchStack` 成功
  - 備考:

- [ ] **5-4** 手動で ECS RunTask を実行
  - 確認: CloudWatch Logs に「Hello World」が出る
  - 備考: ここが最重要確認ポイント

- [ ] **5-5** Step Functions ステートマシンを追加
  - 確認: コンソールから手動実行 → WaitForDbReady（DB 準備確認）→ ECS タスク起動 → 成功（全ステートが正常遷移）
  - 備考: ImageBatchStack の Step Functions は SnsPostBatchStack の Step Functions ARN を参照するため、Phase 4 完了が前提。手動実行 input は `{"set_code":"test-set-1","scheduled_at":"2026-04-19T00:00:00Z"}` のように `set_code` と `scheduled_at` を必ず渡す（ダミー値でよい）。ASL 定義は [docs/infra/workflow.html](infra/workflow.html) セクション 3 を参照

- [ ] **5-6** EventBridge Scheduler を追加
  - 確認: スケジュール時刻に自動で Step Functions が起動される。Scheduler に RetryPolicy と DLQ が設定されている
  - 備考: Scheduler 起動失敗は Step Functions の失敗メトリクスには出ないため、DLQ と `AWS/Scheduler` メトリクスで検知する。アラーム設定は Phase 7 で行う

---

## Phase 6: DB 接続の疎通（最小）

**ゴール**: ECS タスクから Aurora に接続できることを確認する（本スキーマの DDL はアプリ設計後に作成する）

- [ ] **6-1** `shared/` に DB 接続共通モジュールを作成（DB が利用可能な前提。リトライなし）
  - 確認: ユニットテストが通る
  - 備考: DB 接続リトライは DB 準備確認 ECS タスク（FoundationStack）の責務。バッチアプリケーションの DB 接続モジュールにはリトライを持たせない（[docs/infra/workflow.html](infra/workflow.html) セクション 2）

- [ ] **6-2** Hello World コンテナを DB 接続テスト版に差し替え
  - 確認: ローカル Docker + ローカル MySQL で接続テスト
  - 備考:

- [ ] **6-3** 接続確認用の最小 DDL を作成し、Aurora に適用
  - 確認: `database/V000__connection_test.sql`（接続確認用の `connection_test` テーブル 1 つ）を AWS Console の Query Editor で適用でき、テーブルが確認できる
  - 備考: Query Editor の利用には Aurora Serverless v2 の Data API 有効化（`enableDataApi: true`）が必要。CDK 設定は [docs/infra/stacks.html](infra/stacks.html) セクション 3.1 を参照。**本スキーマのテーブル設計・DDL・マイグレーション方針は Phase 9（前倒しで定義済み）を参照する。本スキーマの Aurora への適用は Phase 10 で行う**

- [ ] **6-4** ECR に push して ECS RunTask
  - 確認: CloudWatch Logs に「DB 接続成功」が出る（`connection_test` テーブルへの SELECT / INSERT の成功を含む）
  - 備考:

- [ ] **6-5** Aurora 一時停止状態からの再開リトライを確認（db-readiness-check タスクを使用）
  - 確認: Aurora を一時停止させた後、db-readiness-check タスクを手動 RunTask で実行 → リトライ後に接続成功のログが出力される
  - 備考: Phase 3-3 で動作確認済みの db-readiness-check タスクを使用する。バッチアプリケーション自体には DB 接続リトライを持たせない

---

## Phase 7: MonitoringStack

**ゴール**: バッチ失敗時にアラーム通知が届く（空回しバッチのまま確認できる）

- [ ] **7-1** MonitoringStack に SNS Topic + CloudWatch Alarm を定義
  - 確認: `cdk deploy -c env=prod MonitoringStack` 成功
  - 備考: アラーム・EventBridge Rule の定義は [docs/infra/workflow.html](infra/workflow.html) セクション 8〜10 を参照

- [ ] **7-2** SNS Topic サブスクリプションの設定・確認
  - 確認: (1) SNS Topic にメールサブスクリプションが作成されている (2) 確認メールのリンクをクリックし、ステータスが「確認済み」になっている
  - 備考: 手順の詳細は [docs/infra/operation.html](infra/operation.html) セクション 4.2 を参照。サブスクリプションの承認を行わないと通知が届かない

- [ ] **7-3** 意図的にバッチを失敗させてアラーム通知を確認
  - 確認: メール通知が届く
  - 備考: 空回しバッチ（Hello World / DB 接続テスト版）を意図的に失敗させて確認する（例: 終了コード 1 で終了させたイメージを一時的に push）

---

## Phase 8: CI/CD パイプライン構築

**ゴール**: GitHub push で自動的にビルド・デプロイされる（イメージは空回し版のままでよい）

- [ ] **8-0** CodeStar Connections の事前作成（AWS コンソール）
  - 確認: AWS コンソールの CodePipeline > 設定 > 接続で、GitHub との接続が「利用可能」ステータスになっている
  - 備考: CodeStar Connections は CDK 管理外。AWS コンソールで作成し、GitHub リポジトリとの接続を承認する。詳細は [docs/infra/cicd.html](infra/cicd.html) セクション 1.1 を参照

- [ ] **8-1** CodePipeline + CodeBuild の定義（image-batch 用、ImageBatchStack に追加）
  - 確認: push → ECR イメージ更新 → タスク定義更新
  - 備考: buildspec の構成は [docs/infra/cicd.html](infra/cicd.html) セクション 3.1 を参照

- [ ] **8-2** sns-post-batch 用パイプラインの追加（SnsPostBatchStack に追加）
  - 確認: 同上
  - 備考:

- [ ] **8-3** インフラの手動デプロイ運用手順を確認
  - 確認: `cdk diff -c env=prod <StackName>` → `cdk deploy -c env=prod <StackName>` の手動運用が問題なく行えることを確認
  - 備考: インフラパイプラインは構築しない（破壊的変更リスク回避のため。[docs/infra/cicd.html](infra/cicd.html) 参照）

---

## Phase 10 以降: アプリ実装

**ゴール**: アプリ設計に基づき業務ロジックを実装し、E2E で動作させる

- [ ] **10-1** アプリ設計の最終 Fix（インフラ構築の知見反映）
  - 確認: [docs/app/index.html](app/index.html) の検討メモとインフラ構築（Phase 0〜8）で得た知見を棚卸しし、アプリ設計書に反映されている。blocker のみ修正し、改善提案は設計課題リストに記録されている
  - 備考: 前倒しで作成した Phase 9 の成果物（一時 Fix）をここで最終 Fix する（旧 9-1 の「インフラ構築の知見反映」に相当）

- [ ] **10-2** 実装計画の詳細化
  - 確認: 本ファイルの「Phase 10 以降」が具体的なステップに展開されている
  - 備考: 旧 9-6。旧計画の Phase 7〜8（業務ロジック実装）相当。旧計画の内容は git 履歴（2026-07-06 以前の development-plan.md）を参照できる

以降は 10-2 で具体的なステップへ展開する。想定する内容:

- 本スキーマ DDL（Phase 9-3 で作成済み）の Aurora への適用
- テストデータと Secret 値（画像生成 API キー・SNS 認証情報）の準備
- 画像生成バッチの業務ロジック実装（API 疎通 → S3 保存 → DB 登録 → E2E）
- SNS 投稿バッチの業務ロジック実装（Instagram API 疎通 → 投稿フロー → 重複投稿防止の確認）

---

## トラブルシューティングログ

各ステップで発生した問題と解決策を記録する。

| 日付 | Phase-Step | 問題 | 解決策 |
|---|---|---|---|
| | | | |

## 設計課題リスト

設計レビューで出た改善提案や、一時 Fix 時に持ち越した論点を記録する（運用ルールは [docs/index.html](index.html) セクション 4 を参照）。

| 日付 | 対象ドキュメント | 課題 | 対応方針 | 対応時期 |
|---|---|---|---|---|
| 2026-07-06 | docs/infra/stacks.html | セクション 5「スタック間のデータ受け渡し」のツリー図に MonitoringStack への入力（SnsPostingSfnArn・AuroraClusterIdentifier・EcsClusterArn・ImageGenerationSfnName）と DbReadinessCheckSgId の記載がない。3.1 出力一覧・3.4 依存スタックには記載済みのため実装は可能 | Phase 7 実装時に実態へ合わせて追記 | Phase 7 |
| 2026-07-06 | docs/app/design-outline.html | セット廃止時「データ（生成画像・投稿履歴）は残す」とあるが、S3 実体はインフラ設計の 30 日ライフサイクルで自動削除される。「残す」対象が DB レコード（メタ情報・投稿履歴）であることの明確化と S3 実体の保持要否の確認が必要 | **解消済み（2026-07-07）**: 「残す」対象は DB レコードのみと確定。S3 実体は 30 日ライフサイクルで自動削除される前提を明記した（[docs/app/data-model.html](app/data-model.html#s3-key) セクション 5、[docs/app/operation.html](app/operation.html#set-retire) セクション 2.2） | Phase 9-3 |
| 2026-07-07 | docs/app/operation.html | Instagram トークン失効日（`token_expires_at`）のリマインドは運用者の手動カレンダー管理としたが、セット数が増えると手運用が破綻する | Secrets Manager を横断的に読み取り失効間近のものを通知する仕組み（Lambda + EventBridge 等）の導入を、管理画面（将来拡張）と合わせて検討する | 未定（将来拡張） |
| 2026-07-07 | docs/app/operation.html | stale データ（`pending`/`container_created` のまま残った生成実行）の検知は専用アラームを持たず、既存の失敗通知を起点にした手動クエリ確認に依存する | セット数・投稿頻度が増えて見落としリスクが高まった場合、stale 行数を CloudWatch カスタムメトリクスとして発行する仕組みの導入を検討する | 未定（将来拡張） |
| 2026-07-07 | docs/infra/security.html, docs/infra/workflow.html | SNS 投稿バッチタスクロールに付与済みの `cloudwatch:PutMetricData`（Namespace=`ACPS`）は、Phase 9-2 でアプリ側は個別カスタムメトリクスを持たず既存の Step Functions 失敗アラーム 1 本に一本化する方針が確定したため、実装しても使用しない権限として残る | 実害はない（過剰権限だが最小権限の原則からはやや外れる）。将来アプリ側で個別メトリクス追加が必要になった際に活用するか、使わないなら Phase 10-1 で IAM ポリシーからの削除を検討する | Phase 10-1 |
| 2026-07-07 | docs/app/batch-flow.html | posts の作成（3.3 手順 1）が Step Functions Retry での再実行時にも毎回 INSERT を試みる記述に読めるが、3.2 の復旧ロジックは既存 pending 行への分岐を前提としており、両者を combine して初めて「行が存在する場合は INSERT をスキップする」という意図が読み取れる。明文化されていないため誤読の余地がある | Phase 10 実装時に 3.3 手順 1 を「存在しなければ INSERT」と明記する形で軽微修正を検討する（blocker ではないため 9-5 では見送り） | Phase 10-1 |
| 2026-07-12 | docs/app/batch-flow.html, docs/app/design-outline.html | D-3 通読時の議論で、セット別生成ロジックの隔離方針（image-batch 内の strategy モジュール構造。方式の割当は DB のセット設定で行う）と、生成方式の設計書分冊ルール（batch-flow.html には契約 + 方式カタログのみ、方式本体は `docs/app/generators/` に 1 方式 1 本の 3 層構造）を合意した。現行のアプリ設計書には未反映 | Phase 10-1 の最終 Fix で design-outline.html セクション 1.1 と batch-flow.html のセット別拡張ポイントに反映する。詳細は [docs/app/index.html](app/index.html#memo) の検討メモ（2026-07-12 の 2 件）を参照 | Phase 10-1 |
| 2026-07-12 | docs/infra/workflow.html | 将来セット間のデプロイ分離（セットごとに使うタスク定義リビジョンを Scheduler payload で固定し、新セットの開発中も既存セットは検証済みイメージで動かし続ける方式）が必要になった場合、Step Functions の RunTask がタスク定義を入力から受け取れる形になっていれば、Scheduler の設定値追加だけで移行できる | Phase 10 のワークフロー実装時に「入力未指定なら family 最新リビジョン、指定があればそれを使う」形の継ぎ目を設けるか検討する（デプロイ分離自体は現時点で導入しないと決定済み） | Phase 10-1（検討） |
