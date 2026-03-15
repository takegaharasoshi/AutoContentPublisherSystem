# 開発計画・進捗管理

## 進め方の方針

- インフラから先に構築し、業務ロジックは後から実装する
- 各ステップで実際に AWS 上で稼働確認を行い、動作を確認してから次に進む
- 1 ステップ = 1 プロンプトを基本とし、「作る → 確認 → 次へ」のリズムで進める
- 各ステップの完了後、ユーザーが確認方法に従って動作確認を行い、チェックを入れる

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
  - 確認: `cdk synth` でテンプレートが出力される
  - 備考:

- [ ] **1-2** FoundationStack に VPC だけ定義
  - 確認: `cdk diff FoundationStack` で差分が見える
  - 備考:

- [ ] **1-3** VPC をデプロイ
  - 確認: `cdk deploy FoundationStack` 成功
  - 備考:

- [ ] **1-4** AWS コンソールで VPC を確認
  - 確認: VPC、Subnet、NAT Gateway が作成されている
  - 備考:

- [ ] **1-5** 削除して再作成できることを確認
  - 確認: `cdk destroy` → `cdk deploy` が通る
  - 備考:

---

## Phase 2: FoundationStack の段階的構築

**ゴール**: 共通基盤リソースをすべて構築する

- [ ] **2-1** S3 バケットを追加
  - 確認: コンソールでバケットが見える、`aws s3 cp` でファイルアップロードできる
  - 備考:

- [ ] **2-2** Security Group を追加
  - 確認: コンソールで SG が見える
  - 備考:

- [ ] **2-3** Secrets Manager（DB 接続情報のダミー値）を追加
  - 確認: コンソールでシークレットが見える
  - 備考:

- [ ] **2-4** ECS Cluster を追加
  - 確認: コンソールでクラスターが見える
  - 備考:

- [ ] **2-5** Aurora Serverless v2 を追加
  - 確認: コンソールで DB クラスターが見える、自動一時停止が設定されている
  - 備考: コストに注意。不安なら Phase 3 の後に回してもよい

- [ ] **2-6** VPC Endpoint（S3 Gateway, Secrets Manager Interface）を追加
  - 確認: コンソールで VPC Endpoint が作成されている
  - 備考:

---

## Phase 3: 画像生成バッチの空回し

**ゴール**: EventBridge → Step Functions → ECS Fargate のパイプラインが動くことを確認する（業務ロジックなし）

- [ ] **3-1** `services/image-batch/` に Hello World の Python + Dockerfile を作成
  - 確認: `docker build` & `docker run` でローカル動作確認
  - 備考:

- [ ] **3-2** ECR リポジトリを作成し、手動で Docker イメージを push
  - 確認: ECR コンソールでイメージが見える
  - 備考:

- [ ] **3-3** ImageBatchStack に ECS Task Definition を定義してデプロイ
  - 確認: `cdk deploy ImageBatchStack` 成功
  - 備考:

- [ ] **3-4** 手動で ECS RunTask を実行
  - 確認: CloudWatch Logs に「Hello World」が出る
  - 備考: ここが最重要確認ポイント

- [ ] **3-5** Step Functions ステートマシンを追加
  - 確認: コンソールから手動実行 → ECS タスク起動 → 成功
  - 備考:

- [ ] **3-6** EventBridge Scheduler を追加
  - 確認: スケジュール時刻に自動で Step Functions が起動される
  - 備考:

---

## Phase 4: SNS 投稿バッチの空回し

**ゴール**: SnsPostBatchStack でも同じパイプラインが動くことを確認する

- [ ] **4-1** `services/sns-post-batch/` に Hello World を作成
  - 確認: ローカル Docker で動作確認
  - 備考:

- [ ] **4-2** ECR push + SnsPostBatchStack デプロイ + 手動 RunTask
  - 確認: CloudWatch Logs に「Hello World」が出る
  - 備考:

- [ ] **4-3** Step Functions + EventBridge Scheduler を追加
  - 確認: スケジュール実行を確認
  - 備考:

---

## Phase 5: DB 接続の疎通

**ゴール**: ECS タスクから Aurora に接続できることを確認する

- [ ] **5-1** `shared/` に DB 接続共通モジュールを作成（リトライ付き）
  - 確認: ユニットテストが通る
  - 備考:

- [ ] **5-2** Hello World コンテナを DB 接続テスト版に差し替え
  - 確認: ローカル Docker + ローカル MySQL で接続テスト
  - 備考:

- [ ] **5-3** DDL（テーブル作成 SQL）を作成
  - 確認: ローカル MySQL でテーブルが作れる
  - 備考:

- [ ] **5-4** Aurora に DDL を実行
  - 確認: コンソールの Query Editor 等でテーブル確認
  - 備考:

- [ ] **5-5** ECR に push して ECS RunTask
  - 確認: CloudWatch Logs に「DB 接続成功」が出る
  - 備考:

- [ ] **5-6** Aurora 一時停止状態からの再開リトライを確認
  - 確認: 一時停止後にタスク実行 → リトライ後に接続成功のログ
  - 備考:

---

## Phase 6: 画像生成バッチの業務ロジック実装

**ゴール**: 実際に画像を生成して S3 に保存、DB にメタ情報を登録する

- [ ] **6-1** 画像生成 API との疎通（ローカル Python スクリプト）
  - 確認: API を叩いて画像が返る
  - 備考:

- [ ] **6-2** S3 保存処理の実装
  - 確認: ローカルから S3 にアップロードできる
  - 備考:

- [ ] **6-3** DB メタ情報登録処理の実装
  - 確認: ローカルから DB にレコードが入る
  - 備考:

- [ ] **6-4** 上記を結合してコンテナ化・ECS RunTask
  - 確認: S3 に画像 + DB にメタ情報が登録される
  - 備考:

- [ ] **6-5** Step Functions 経由でエンドツーエンド実行
  - 確認: 一連の流れが自動で動く
  - 備考:

---

## Phase 7: SNS 投稿バッチの業務ロジック実装

**ゴール**: DB の未投稿画像を取得し、SNS に投稿して結果を記録する

- [ ] **7-1** Instagram API との疎通（ローカル）
  - 確認: API でテスト投稿できる
  - 備考:

- [ ] **7-2** DB 取得 → Presigned URL 生成 → 投稿の結合・ECS RunTask
  - 確認: 一連の流れが動く
  - 備考:

- [ ] **7-3** 投稿結果の DB 記録・重複投稿防止の確認
  - 確認: 同じ画像が二重投稿されない
  - 備考:

---

## Phase 8: MonitoringStack

**ゴール**: バッチ失敗時にアラーム通知が届く

- [ ] **8-1** MonitoringStack に SNS Topic + CloudWatch Alarm を定義
  - 確認: `cdk deploy MonitoringStack` 成功
  - 備考:

- [ ] **8-2** 意図的にバッチを失敗させてアラーム通知を確認
  - 確認: メール通知が届く
  - 備考:

---

## Phase 9: CI/CD パイプライン構築

**ゴール**: GitHub push で自動的にビルド・デプロイされる

- [ ] **9-1** CodePipeline + CodeBuild の定義（image-batch 用）
  - 確認: push → ECR イメージ更新 → タスク定義更新
  - 備考:

- [ ] **9-2** sns-post-batch 用パイプラインの追加
  - 確認: 同上
  - 備考:

- [ ] **9-3** インフラは手動デプロイであることをチーム内で確認
  - 確認: `cdk diff` → `cdk deploy` の手動運用が問題なく行えることを確認
  - 備考: インフラパイプラインは構築しない（破壊的変更リスク回避のため）

---

## トラブルシューティングログ

各ステップで発生した問題と解決策を記録する。

| 日付 | Phase-Step | 問題 | 解決策 |
|---|---|---|---|
| | | | |
