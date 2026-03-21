# AutoContentPublisherSystem

AWS 上で動作する画像生成・SNS 自動投稿バッチシステム。

## 概要

- **画像生成バッチ**: Nano Banana Pro（Gemini 3 Pro 画像 API）で画像を生成し、S3 に保存、DB にメタ情報を登録
- **SNS 投稿バッチ**: S3 上の画像を Instagram Graph API を用いて SNS に投稿

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

| スタック | 責務 |
|---|---|
| FoundationStack | VPC、S3、Aurora、Secrets Manager、ECS Cluster、ECR、DB 準備確認 ECS タスク等の共通基盤 |
| ImageBatchStack | 画像生成バッチの実行基盤（Task Definition、Step Functions、Scheduler） |
| SnsPostBatchStack | SNS 投稿バッチの実行基盤 |
| MonitoringStack | CloudWatch Alarm、SNS Topic による監視・通知 |
| AdminApiStack | 管理画面バックエンド API（将来拡張） |
| AdminWebStack | 管理画面フロントエンド（将来拡張） |

## リポジトリ構成

> **注意**: 以下は予定構成です。各ディレクトリは段階的に作成します。

```
AutoContentPublisherSystem/
├── docs/                    # 設計書
├── infra/                   # AWS CDK（インフラ定義）
├── services/
│   ├── db-readiness-check/  # DB 準備確認（Python）
│   ├── image-batch/         # 画像生成バッチ（Python）
│   └── sns-post-batch/      # SNS 投稿バッチ（Python）
├── shared/                  # サービス間共通ライブラリ
├── CLAUDE.md
└── README.md
```

## ドキュメント

設計書は `docs/` 配下に L0（概要）→ L1（論理設計）→ L2（実装仕様）の 3 層構造で管理している。
体系の全体像は [docs/document-guide.md](docs/document-guide.md) を参照。

## 開発環境

- OS: Windows + WSL2（Ubuntu）
- エディタ: VS Code ベースのエディタ
- コンテナ: Docker Desktop

## セットアップ

> **注意**: 以下は予定構成です。実装完了後に手順を確定します。

```bash
# リポジトリをクローン
git clone <repository-url>
cd AutoContentPublisherSystem

# Python 仮想環境のセットアップ（各サービスごと）
cd services/image-batch
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## デプロイ

> **注意**: 以下は予定構成です。実装完了後に手順を確定します。

```bash
# CDK デプロイ（スタック順序に従う）
cd infra
cdk deploy FoundationStack
cdk deploy SnsPostBatchStack
cdk deploy ImageBatchStack
cdk deploy MonitoringStack
```
