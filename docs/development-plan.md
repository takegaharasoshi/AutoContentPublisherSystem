# 開発計画・進捗管理

## 進め方の方針

- **インフラから先に構築し、アプリ（業務ロジック）の設計・実装は後から行う**
  - Phase D: インフラ設計の一時 Fix → Phase A: アプリ設計の大枠（上流設計）→ Phase 0〜8: インフラ構築（空回し確認・監視・CI/CD まで）→ Phase 9: アプリ設計（詳細）→ Phase 10 以降: アプリ実装
- **アプリ設計は 2 段階で行う**: 大枠（Phase A）と詳細（Phase 9）に分ける
  - Phase A では仕様の壁打ち・設計書構成の決定・主要方針の骨子までを固め、詳細設計はインフラ完成後の Phase 9 で行う
  - 経緯: 2026-07-06、上流工程に適した生成 AI モデル（Claude Fable 5）の利用期限を機に、Phase 9 の上流部分を Phase A として前倒しした
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

- [ ] **D-3** ユーザー通読と一時 Fix 宣言
  - 確認: ユーザーが全インフラ設計書を通読し、疑問点が解消されている
  - 備考: 残った指摘・懸念は設計課題リストに記録して終了する。以降の設計変更は「実装を正とする」ルールで随時反映する

---

## Phase A: アプリ設計の大枠（上流設計）

**ゴール**: アプリ仕様の壁打ちを行い、アプリ設計の大枠（設計書構成・主要方針の骨子）を決めて docs/app/ に記載する

> Phase A は D-3 の完了を前提としない（D-3 はユーザー作業のため並行してよい）。成果物は **Phase 9 で見直す前提の一時 Fix** とし、生成 AI レビュー（観点限定・最大 2 巡）は Phase 9-5 でまとめて実施する。詳細設計（テーブル定義・処理フローの詳細・DDL 等）には踏み込まない。

- [ ] **A-1** アプリ仕様の壁打ち
  - 確認: ユースケース・投稿運用のイメージ・セットの考え方・失敗時にどうしたいか等が言語化され、docs/app/ 配下に記録されている
  - 備考: 生成 AI と対話しながら要件を言語化する。**設計書はまだ書かない**。[docs/_archive/](_archive/) の旧設計を参考資料としてよい

- [ ] **A-2** アプリ設計の大枠決め
  - 確認: docs/app/ の設計書構成（ドキュメント一覧と各スコープ）と、主要設計方針の骨子（処理フロー概要・データモデル概要・運用方針）が決まっている
  - 備考: A-1 の壁打ち結果をもとに決める。どこまでを大枠とし、何を Phase 9 に持ち越すかもここで線引きする

- [ ] **A-3** 大枠を踏まえた既存設計の見直し
  - 確認: インフラ設計書 6 本と開発計画を大枠と突き合わせ、矛盾・欠落（blocker）が修正されている。改善提案は設計課題リストに記録されている
  - 備考: 見直し観点の例: `set_code` / `scheduled_at` の意味付け、SNS Secret 規約（`set_code` / `account_code` の定義）、環境変数の受け渡し契約。修正は blocker のみ（設計 Fix の運用ルールに従う）

- [ ] **A-4** アプリ設計大枠の設計書記載
  - 確認: A-2 で決めた構成に従い、docs/app/ に大枠設計書（HTML、共通スタイル使用）が作成されている
  - 備考: 詳細未定の節は「Phase 9 で詳細化」と明記する。[docs/app/index.html](app/index.html) はアプリ設計の目次ページとして更新する

---

## Phase 0: ローカル開発基盤の整備

**ゴール**: CDK と Docker がローカルで動く状態にする

- [ ] **0-1** AWS CLI のインストール・認証設定
  - 確認: `aws sts get-caller-identity` で自分のアカウントが表示される
  - 備考:

- [ ] **0-2** AWS CDK CLI のインストール
  - 確認: `cdk --version` でバージョンが表示される
  - 備考:

- [ ] **0-3** CDK Bootstrap（初回のみ）
  - 確認: `cdk bootstrap aws://ACCOUNT/REGION` が成功する
  - 備考:

- [ ] **0-4** Python / Docker の動作確認
  - 確認: `python --version`, `docker run hello-world` が通る
  - 備考: 本プロジェクトは WSL2 + Docker Desktop の WSL integration を有効化する前提。Docker Desktop を使わず WSL 内に直接 Docker Engine を導入する場合は、systemd 有効化やユーザーグループ設定などの手動セットアップが別途必要

- [ ] **0-5** リポジトリのディレクトリ構成を作成
  - 確認: `services/`, `shared/`, `infra/` ディレクトリが存在する
  - 備考:

---

## Phase 1: CDK プロジェクト初期化 + VPC デプロイ

**ゴール**: CDK で最小のリソース（VPC）を AWS に作れることを確認する

- [ ] **1-1** `infra/` に CDK プロジェクトを初期化（TypeScript）
  - 確認: `cdk synth -c env=prod` でテンプレートが出力される
  - 備考:

- [ ] **1-2** FoundationStack に VPC だけ定義
  - 確認: `cdk diff -c env=prod FoundationStack` で差分が見える
  - 備考: VPC の CDK 引数は [docs/infra/stacks.html](infra/stacks.html) セクション 3.1 を参照

- [ ] **1-3** VPC をデプロイ
  - 確認: `cdk deploy -c env=prod FoundationStack` 成功
  - 備考:

- [ ] **1-4** AWS コンソールで VPC を確認
  - 確認: VPC、Public Subnet x2（各 AZ）、Isolated Subnet x2（各 AZ）が作成されている（NAT Gateway がないことを確認）
  - 備考:

- [ ] **1-5** 削除して再作成できることを確認
  - 確認: `cdk destroy -c env=prod FoundationStack` → `cdk deploy -c env=prod FoundationStack` が通る
  - 備考:

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
  - 備考: Phase 4-5 は Step Functions の追加デプロイのみ。4-6 は WaitForDbReady を含む一連フローの動作確認。手動実行 input は `{"set_code":"test-set-1"}` のように `set_code` を必ず渡す（空回し段階ではダミー値でよい。意味付けはアプリ設計で確定する）。Phase 5 で ImageBatchStack に EventBridge Scheduler を追加し、SNS 投稿は画像生成成功後に自動起動される

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
  - 備考: Query Editor の利用には Aurora Serverless v2 の Data API 有効化（`enableDataApi: true`）が必要。CDK 設定は [docs/infra/stacks.html](infra/stacks.html) セクション 3.1 を参照。**本スキーマのテーブル設計・DDL・マイグレーション方針は Phase 9（アプリ設計）で定義する**

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

## Phase 9: アプリ設計（詳細）

**ゴール**: Phase A の大枠設計を詳細化してアプリ設計書（docs/app/）を完成させ、一時 Fix する

> ここまでのフェーズでインフラは完成し、空回しでの動作イメージが得られている。Phase A で作成した大枠設計書をベースに、インフラ構築で得た知見と検討メモを反映して詳細化する。[docs/_archive/](_archive/) の旧設計（batch.md / database.md / operation.md）を参考資料として活用する。

- [ ] **9-1** Phase A 大枠の棚卸しと更新
  - 確認: Phase A の大枠設計書と [docs/app/index.html](app/index.html) の検討メモを棚卸しし、インフラ構築中に得た知見・論点が大枠に反映されている
  - 備考: 大枠に変更が必要なら先に更新してから詳細設計（9-2 以降）に入る

- [ ] **9-2** バッチ処理フロー設計
  - 確認: docs/app/ に処理フロー設計書（HTML）が作成されている
  - 備考: Phase A の大枠設計書（処理フロー概要）を詳細化する。冪等性・再試行・投稿ステータス管理・二重投稿防止・バッチサイズ制限を扱う。docs/_archive/batch.md を参考資料とする

- [ ] **9-3** DB スキーマ設計 + 本スキーマ DDL 作成
  - 確認: docs/app/ に DB 設計書（HTML）が、`database/` に本スキーマの DDL がある
  - 備考: Phase A の大枠設計書（データモデル概要）を詳細化する。docs/_archive/database.md を参考資料とする。DDL のバージョン管理・マイグレーション方針もここで定義する

- [ ] **9-4** アプリ運用・セキュリティ（アプリ部分）の設計
  - 確認: docs/app/ にアプリ運用設計書（HTML）が作成されている
  - 備考: Phase A の大枠設計書（運用方針）を詳細化する。プロンプト管理、SNS アカウント追加手順、投稿失敗時の手動補正、SNS Secret 規約の最終確認（[docs/infra/security.html](infra/security.html) セクション 1.2 の注記）。docs/_archive/operation.md を参考資料とする

- [ ] **9-5** 生成 AI レビュー → 一時 Fix
  - 確認: blocker 指摘がゼロ、または修正済み。改善提案は設計課題リストに記録されている
  - 備考: Phase D と同じレビュー運用ルール（観点限定・最大 2 巡・blocker のみ修正）。レビュー観点は「Phase 10 以降のアプリ実装を妨げる誤り・矛盾・欠落のみ」とする

- [ ] **9-6** Phase 10 以降の実装計画を詳細化
  - 確認: 本ファイルの「Phase 10 以降」が具体的なステップに展開されている
  - 備考: 旧計画の Phase 7〜8（業務ロジック実装）相当。旧計画の内容は git 履歴（2026-07-06 以前の development-plan.md）を参照できる

---

## Phase 10 以降: アプリ実装（Phase 9-6 で詳細化する）

アプリ設計の完了後に具体的なステップへ展開する。想定する内容:

- 本スキーマ DDL の Aurora への適用
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
