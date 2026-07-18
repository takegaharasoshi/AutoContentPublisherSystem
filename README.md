# AutoContentPublisherSystem

AWS 上で動作する画像生成・SNS 自動投稿バッチシステム。

## 概要

- **画像生成バッチ**: 画像生成 API で画像を生成し、S3 に保存、DB にメタ情報を登録（生成方式はセット単位で選択・差し替え可能。特定の API に固定しない）
- **SNS 投稿バッチ**: S3 上の画像を投稿先プラットフォームの API を用いて SNS に投稿（複数 SNS プラットフォーム対応を前提とする）

## アーキテクチャ

| レイヤー | 技術 |
|---|---|
| 開発言語 | Python |
| DB | Aurora Serverless v2（MySQL 互換） |
| バッチ実行 | EventBridge Scheduler → Step Functions → ECS Fargate RunTask |
| コンテナ管理 | ECR / ECS Fargate |
| インフラ定義 | AWS CDK（TypeScript） |
| CI/CD | GitHub → CodePipeline → CodeBuild → ECR push → ECS Task Definition 更新（インフラは手動 cdk deploy） |
| 秘密情報管理 | Secrets Manager |
| ログ・監視 | CloudWatch Logs / CloudWatch Alarm |

## CDK スタック構成

| スタック | フェーズ | 責務 |
|---|---|---|
| FoundationStack | 初期 | VPC、S3、Aurora、Secrets Manager、ECS Cluster、ECR、DB 準備確認 ECS タスク等の共通基盤 |
| ImageBatchStack | 初期 | 画像生成バッチの実行基盤（Task Definition、Step Functions、Scheduler、Scheduler DLQ） |
| SnsPostBatchStack | 初期 | SNS 投稿バッチの実行基盤 |
| MonitoringStack | 初期 | Step Functions / Scheduler / ECS / Aurora の CloudWatch Alarm、SNS Topic による監視・通知 |
| AdminApiStack | 将来拡張 | 管理画面バックエンド API |
| AdminWebStack | 将来拡張 | 管理画面フロントエンド |

## リポジトリ構成

> **注意**: ディレクトリは作成済みですが、`services/`・`shared/` の中身は開発計画に沿って段階的に実装します。

```
AutoContentPublisherSystem/
├── docs/                    # 設計書
├── infra/                   # AWS CDK（インフラ定義）
├── services/
│   ├── db-readiness-check/  # DB 準備確認（Python）
│   ├── image-batch/         # 画像生成バッチ（Python）
│   └── sns-post-batch/      # SNS 投稿バッチ（Python）
├── database/                # DDL ファイル（スキーマ管理）
├── shared/                  # サービス間共通ライブラリ
├── CLAUDE.md
└── README.md
```

## ドキュメント

設計書は `docs/` 配下で管理し、**インフラ設計（`docs/infra/`）とアプリ設計（`docs/app/`）を分離**している。
体系の全体像は [docs/index.html](docs/index.html) を参照。開発計画・進捗は [docs/development-plan.md](docs/development-plan.md) で管理し、完了ステップの実施記録は [docs/development-log.md](docs/development-log.md) に保管する。

- 設計書は HTML で記述している（開発計画・開発記録のみ Markdown）。GitHub 上ではソース表示になるため、ローカルのブラウザまたは VS Code の Live Preview で閲覧すること
- `docs/_archive/` は旧 Markdown 設計書のアーカイブ（現役の設計書ではない）

## 開発環境

- OS: Windows + WSL2（Ubuntu）
- エディタ: VS Code ベースのエディタ
- コンテナ: Docker Desktop

## ローカル開発環境

### ローカル MySQL（docker compose）

Aurora（MySQL 8.0 互換）の代替としてローカル MySQL を docker compose で起動する。初回起動時に `database/` 配下の DDL（V000 → V001 → …）がファイル名順に自動適用される。

```bash
# 起動（リポジトリルートから）
docker compose up -d

# 初期化完了（healthy）を待って確認
docker compose ps

# スキーマを再初期化したいとき（データボリュームごと破棄）
docker compose down -v
```

接続情報（[docker-compose.yml](docker-compose.yml) で定義）:

| 項目 | 値 |
|---|---|
| ホスト | `127.0.0.1`（ホストから） / `host.docker.internal`（コンテナから） |
| ポート | `3306` |
| データベース | `acps`（Aurora と同名） |
| ユーザー / パスワード | `app` / `password`（root は `root` / `root`） |

### テスト実行

Python は uv で管理する（`uv run` が `uv.lock` どおりの環境を自動構築する）。

```bash
cd services/image-batch && uv run pytest   # 各サービス・shared で同様
```

### バッチのローカル Docker 実行

ローカル MySQL に対して各バッチを実行する手順は各サービスの README（例: [services/image-batch/README.md](services/image-batch/README.md)）を参照。

## デプロイ

> **注意**: 以下は予定構成です。実装完了後に手順を確定します。

```bash
# CDK デプロイ（スタック順序に従う）
cd infra
cdk deploy -c env=prod FoundationStack
cdk deploy -c env=prod SnsPostBatchStack
cdk deploy -c env=prod ImageBatchStack
cdk deploy -c env=prod MonitoringStack
```

CDK コマンド例では app 内の論理スタック ID（`FoundationStack` など）を指定する。`-c env=prod` により、CloudFormation 上の実スタック名は `Prod-FoundationStack` のように環境名付きで作成される。
