# 開発計画・進捗管理

## 進め方の方針

- インフラから先に構築し、業務ロジックは後から実装する
- 各ステップで実際に AWS 上で稼働確認を行い、動作を確認してから次に進む
- 1 ステップ = 1 プロンプトを基本とし、「作る → 確認 → 次へ」のリズムで進める
- 各ステップの完了後、ユーザーが確認方法に従って動作確認を行い、チェックを入れる
- CDK コマンド例では app 内の論理スタック ID（`FoundationStack` など）を指定する。`-c env=prod` により、CloudFormation 上の実スタック名は `Prod-FoundationStack` のように環境名付きで作成される

## 凡例

- `[ ]` 未着手
- `[x]` 完了
- `[!]` 問題あり・要対応

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
  - 備考:

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
  - 備考:

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
  - 備考:

- [ ] **2-3** Secrets Manager（DB 接続情報のダミー値 + 画像生成 API キーの箱）を追加
  - 確認: コンソールでシークレットが 2 つ見える（DB 接続情報用、画像生成 API キー用）
  - 備考: 画像 API キー用 Secret は CDK で「箱」のみ作成する。実際の API キー値は Phase 7-0 で手動設定する

- [ ] **2-4** ECS Cluster を追加
  - 確認: コンソールでクラスターが見える
  - 備考:

- [ ] **2-5** ECR リポジトリを追加（image-batch、sns-post-batch、db-readiness-check の 3 つ）
  - 確認: コンソールで 3 つの ECR リポジトリが見える
  - 備考: ECR リポジトリは FoundationStack で一元管理する（specs/infrastructure.md 参照）

- [ ] **2-6** VPC Endpoint（S3 Gateway のみ）を追加
  - 確認: コンソールで S3 Gateway VPC Endpoint が作成されている（Secrets Manager Interface Endpoint は不要）
  - 備考: Secrets Manager へのアクセスは ECS Fargate のパブリック IP 経由で行う

---

## Phase 3: FoundationStack の段階的構築（Aurora + DB 準備確認）

**ゴール**: Aurora と DB 準備確認タスクを構築する

- [ ] **3-1** Aurora Serverless v2 を追加
  - 確認: コンソールで DB クラスターが見える、自動一時停止が設定されている、最小 ACU が 0 になっている
  - 備考: Aurora MySQL 3.08.0 以降など、自動一時停止対応バージョンを採用する。コストに注意。不安なら Phase 4 の後に回してもよい

- [ ] **3-2** `services/db-readiness-check/` に DB 準備確認用の Python + Dockerfile を作成し、ECR に push
  - 確認: ECR コンソールでイメージが見える
  - 備考: DB 接続リトライ（指数バックオフ、最大 8 回）を実装する。詳細は design/batch.md セクション 1.2 参照。ECR push 時は不変タグ（例: Git コミットハッシュ）を使用する

- [ ] **3-3** DB 準備確認 ECS タスク定義を FoundationStack に追加し、手動 RunTask で疎通確認
  - 確認: Aurora が起動状態のとき: CloudWatch Logs に接続成功ログが出力され、終了コード 0 で終了する
  - 備考: `cdk deploy -c env=prod -c dbReadinessCheckImageTag=<tag> FoundationStack` でタスク定義を作成する（`<tag>` は Phase 3-2 で ECR push した不変タグ）。Aurora が一時停止状態からのリトライ確認は Phase 6-6 で実施する

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
  - 備考:

- [ ] **4-6** Step Functions 手動実行による E2E 確認（WaitForDbReady → ECS タスク実行の一連フロー）
  - 確認: コンソールから手動実行 → DB 準備確認 → SNS 投稿 ECS タスク起動 → 成功（全ステートが正常遷移）
  - 備考: Phase 4-5 は Step Functions の追加デプロイのみ。4-6 は WaitForDbReady を含む一連フローの動作確認。Phase 5 で ImageBatchStack に EventBridge Scheduler を追加し、SNS 投稿は画像生成成功後に自動起動される

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
  - 備考: ImageBatchStack の Step Functions は SnsPostBatchStack の Step Functions ARN を参照するため、Phase 4 完了が前提

- [ ] **5-6** EventBridge Scheduler を追加
  - 確認: スケジュール時刻に自動で Step Functions が起動される
  - 備考:

---

## Phase 6: DB 接続の疎通

**ゴール**: ECS タスクから Aurora に接続できることを確認する

- [ ] **6-1** `shared/` に DB 接続共通モジュールを作成（DB が利用可能な前提。リトライなし）
  - 確認: ユニットテストが通る
  - 備考: DB 接続リトライは DB 準備確認 ECS タスク（FoundationStack）の責務。バッチアプリケーションの DB 接続モジュールにはリトライを持たせない

- [ ] **6-2** Hello World コンテナを DB 接続テスト版に差し替え
  - 確認: ローカル Docker + ローカル MySQL で接続テスト
  - 備考:

- [ ] **6-3** DDL（テーブル作成 SQL）を作成
  - 確認: ローカル MySQL でテーブルが作れる
  - 備考:

- [ ] **6-4** Aurora に DDL を実行
  - 確認: コンソールの Query Editor 等でテーブル確認
  - 備考:

- [ ] **6-5** ECR に push して ECS RunTask
  - 確認: CloudWatch Logs に「DB 接続成功」が出る
  - 備考:

- [ ] **6-6** Aurora 一時停止状態からの再開リトライを確認（db-readiness-check タスクを使用）
  - 確認: Aurora を一時停止させた後、db-readiness-check タスクを手動 RunTask で実行 → リトライ後に接続成功のログが出力される
  - 備考: Phase 3-3 で動作確認済みの db-readiness-check タスクを使用する。バッチアプリケーション自体には DB 接続リトライを持たせない

---

## Phase 7: 画像生成バッチの業務ロジック実装

**ゴール**: 実際に画像を生成して S3 に保存、DB にメタ情報を登録する

- [ ] **7-0** テストデータと Secret の準備
  - 確認: (1) `batch_sets` にテスト用セットのレコードが存在する (2) `prompt_configs` にテスト用プロンプトのレコードが存在する (3) Secrets Manager の `acps/prod/image/api-key` に実際の API キー値が格納されている
  - 備考: DB テーブルへの INSERT は Query Editor 等で手動実行する。Secret 値は AWS Console から手動設定する

- [ ] **7-1** 画像生成 API との疎通（ローカル Python スクリプト）
  - 確認: API を叩いて画像が返る
  - 備考:

- [ ] **7-2** S3 保存処理の実装
  - 確認: ローカルから S3 にアップロードできる
  - 備考:

- [ ] **7-3** DB メタ情報登録処理の実装
  - 確認: ローカルから DB にレコードが入る
  - 備考:

- [ ] **7-4** 上記を結合してコンテナ化・ECS RunTask
  - 確認: S3 に画像 + DB にメタ情報が登録される
  - 備考:

- [ ] **7-5** Step Functions 経由でエンドツーエンド実行
  - 確認: 一連の流れが自動で動く
  - 備考:

---

## Phase 8: SNS 投稿バッチの業務ロジック実装

**ゴール**: DB の未投稿画像を取得し、SNS に投稿して結果を記録する

- [ ] **8-0** テストデータと Secret の準備
  - 確認: (1) `sns_accounts` にテスト用アカウントのレコードが存在する (2) Secrets Manager に SNS 認証情報 Secret（`acps/prod/{set_code}/sns/instagram/{account_code}`）が作成・値が格納されている (3) Phase 7 で生成済みの画像データが `generated_images` に存在する
  - 備考: SNS アカウント追加手順は design/operation.md セクション 1.6 を参照

- [ ] **8-1** Instagram API との疎通（ローカル）
  - 確認: API でテスト投稿できる
  - 備考:

- [ ] **8-2** DB 取得 → Presigned URL 生成 → 投稿の結合・ECS RunTask
  - 確認: 一連の流れが動く
  - 備考:

- [ ] **8-3** 投稿結果の DB 記録・重複投稿防止の確認
  - 確認: 同じ画像が二重投稿されない
  - 備考:

---

## Phase 9: MonitoringStack

**ゴール**: バッチ失敗時にアラーム通知が届く

- [ ] **9-1** MonitoringStack に SNS Topic + CloudWatch Alarm を定義
  - 確認: `cdk deploy -c env=prod MonitoringStack` 成功
  - 備考:

- [ ] **9-2** SNS Topic サブスクリプションの設定・確認
  - 確認: (1) SNS Topic にメールサブスクリプションが作成されている (2) 確認メールのリンクをクリックし、ステータスが「確認済み」になっている
  - 備考: 手順の詳細は design/operation.md セクション 4.2 を参照。サブスクリプションの承認を行わないと通知が届かない

- [ ] **9-3** 意図的にバッチを失敗させてアラーム通知を確認
  - 確認: メール通知が届く
  - 備考:

---

## Phase 10: CI/CD パイプライン構築

**ゴール**: GitHub push で自動的にビルド・デプロイされる

- [ ] **10-0** CodeStar Connections の事前作成（AWS コンソール）
  - 確認: AWS コンソールの CodePipeline > 設定 > 接続で、GitHub との接続が「利用可能」ステータスになっている
  - 備考: CodeStar Connections は CDK 管理外。AWS コンソールで作成し、GitHub リポジトリとの接続を承認する。詳細は design/cicd.md セクション 1.1 を参照

- [ ] **10-1** CodePipeline + CodeBuild の定義（image-batch 用、ImageBatchStack に追加）
  - 確認: push → ECR イメージ更新 → タスク定義更新
  - 備考:

- [ ] **10-2** sns-post-batch 用パイプラインの追加（SnsPostBatchStack に追加）
  - 確認: 同上
  - 備考:

- [ ] **10-3** インフラの手動デプロイ運用手順を確認
  - 確認: `cdk diff -c env=prod <StackName>` → `cdk deploy -c env=prod <StackName>` の手動運用が問題なく行えることを確認
  - 備考: インフラパイプラインは構築しない（破壊的変更リスク回避のため）

---

## トラブルシューティングログ

各ステップで発生した問題と解決策を記録する。

| 日付 | Phase-Step | 問題 | 解決策 |
|---|---|---|---|
| | | | |
