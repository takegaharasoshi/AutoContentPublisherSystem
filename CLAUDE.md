# CLAUDE.md

## プロジェクト概要

AutoContentPublisherSystem — AWS 上で動作する画像生成・SNS 自動投稿バッチシステム。
モノリポジトリ構成で、サービスごとにコンテナイメージ・CDK スタック・CI/CD パイプラインを分離する。

## リポジトリ構成

> **注意**: `infra/`, `services/`, `shared/` は未作成。開発計画に沿って段階的に作成する。

```
AutoContentPublisherSystem/
├── docs/                            # 設計書（下記「設計書体系」参照）
│   ├── document-guide.md            #   設計書体系ガイド（エントリポイント）
│   ├── overview/                    #   L0 概要層
│   ├── design/                      #   L1 論理設計層
│   ├── specs/                       #   L2 実装仕様層
│   └── development-plan.md          #   開発計画・進捗管理
├── infra/                           # AWS CDK プロジェクト（TypeScript）※未作成
├── services/
│   ├── db-readiness-check/          # DB 準備確認（Python）※未作成
│   ├── image-batch/                 # 画像生成バッチ（Python）※未作成
│   └── sns-post-batch/              # SNS 投稿バッチ（Python）※未作成
├── database/                        # DDL ファイル（スキーマ管理）※未作成
├── shared/                          # サービス間共通ライブラリ（Python）※未作成
├── CLAUDE.md
└── README.md
```

## 技術スタック

- **言語**: Python（バッチ処理）
- **インフラ定義**: AWS CDK（TypeScript）
- **DB**: Aurora Serverless v2（MySQL 互換）
- **実行基盤**: ECS Fargate RunTask（ECS Service は使用しない）
- **ワークフロー**: Step Functions Standard
- **スケジューラ**: EventBridge Scheduler
- **CI/CD**: CodePipeline → CodeBuild → ECR push → ECS Task Definition 更新（インフラは手動 `cdk deploy`）

## 設計書体系

設計書は 3 層構造（L0 → L1 → L2）で段階的に詳細化する。体系の全体像は `docs/document-guide.md` を参照。

| 層 | ディレクトリ | 目的 | ドキュメント |
|---|---|---|---|
| L0 概要 | `docs/overview/` | システムの目的・スコープ・技術選定 | `system-overview.md` |
| L1 論理設計 | `docs/design/` | 設計判断・論理フロー・方針 | `architecture.md`, `batch.md`, `cicd.md`, `operation.md`, `security.md` |
| L2 実装仕様 | `docs/specs/` | CDK 定義・ASL・テーブル定義等の実装詳細 | `infrastructure.md`, `workflow.md`, `database.md` |

### ドキュメント参照ガイド（タスク別）

タスクに必要なドキュメントだけを読み、コンテキストを節約すること。

| タスク | 読むべきドキュメント |
|---|---|
| プロジェクトの全体像を把握 | L0 `docs/overview/system-overview.md` |
| CDK コードを書く・修正する | L2 `docs/specs/infrastructure.md`（前提知識が必要なら L1 `docs/design/architecture.md`） |
| Step Functions 定義を書く・修正する | L2 `docs/specs/workflow.md`（前提知識が必要なら L1 `docs/design/batch.md`） |
| DB スキーマを変更する | L2 `docs/specs/database.md` |
| バッチ処理ロジックを実装する | L1 `docs/design/batch.md` + L2 `docs/specs/database.md` |
| CI/CD パイプラインを構築する | L1 `docs/design/cicd.md` |
| 監視・運用手順を設定する | L1 `docs/design/operation.md` + L2 `docs/specs/workflow.md`（監視リソース定義） |
| 認証・秘密情報の設定を変更する | L1 `docs/design/security.md` |
| SNS アカウントを追加する | L1 `docs/design/operation.md` セクション 1.6 + L1 `docs/design/security.md`（Secret 名規約） |
| 開発の次ステップを確認する | `docs/development-plan.md` |

### SSOT 原則

各情報の「正」は 1 箇所のみに配置する。詳細な SSOT 配置ルールは `docs/document-guide.md` を参照。

## 開発計画

- 開発計画と進捗は `docs/development-plan.md` で管理する
- Phase 0〜10 の段階的アプローチで、インフラ構築 → 空回し確認 → 業務ロジック実装の順に進める
- 各ステップは「Claude Code でコード作成 → ユーザーが AWS 上で稼働確認 → 次へ」の流れで進める
- 作業開始時は `docs/development-plan.md` を読み、現在の Phase・ステップを確認してから着手する

## ドキュメント更新ルール

コードやインフラに変更を加えた際は、関連ドキュメントも同時に更新する。
更新対象の特定には `docs/document-guide.md` の SSOT 配置ルールに従う。

- 設計と異なる実装をした場合は、実装に合わせてドキュメントを修正する（実態の記録を優先）
- 将来の拡張予定として記載している項目は、実装開始時にドキュメントを具体化する
- 設計変更が発生した場合は、変更理由をドキュメントの備考に残す

## コーディング規約

- Python コードは PEP 8 に準拠する
- 型ヒントを使用する
- docstring は Google スタイルを使用する

## 開発上の注意事項

- Aurora Serverless v2 の自動一時停止を利用するため、Step Functions ワークフローの最初のステートとして DB 準備確認 ECS タスクを実行する（FoundationStack で定義）。バッチアプリケーション（ECS タスク）は DB が利用可能な状態を前提とする
- 外部 API 呼び出し失敗時は Step Functions の Retry / Catch でハンドリングする
- デプロイは Blue/Green なし、ECS Service なし。Docker イメージを ECR に push し、新しいタスク定義リビジョンを登録する方式
- 将来の複数セット運用を前提とした DB 設計（設定値・プロンプト・投稿先・実行履歴を識別可能にする）

## CDK スタック

デプロイ順序: FoundationStack → SnsPostBatchStack → ImageBatchStack → MonitoringStack

- **FoundationStack**: 共通基盤（VPC、S3、Aurora、Secrets Manager、ECS Cluster、ECR、DB 準備確認 ECS タスク）
- **ImageBatchStack**: 画像生成バッチ実行基盤
- **SnsPostBatchStack**: SNS 投稿バッチ実行基盤
- **MonitoringStack**: 監視・通知
- **AdminApiStack**（将来拡張）: 管理画面バックエンド API
- **AdminWebStack**（将来拡張）: 管理画面フロントエンド

## Git 運用ルール

- コミットメッセージは必ず**日本語**で記述する

## よく使うコマンド

```bash
# Python テスト実行（各サービスディレクトリ内で）
pytest

# CDK 差分確認
cd infra && cdk diff <StackName>

# CDK デプロイ
cd infra && cdk deploy <StackName>

# Docker ビルド（各サービスディレクトリ内で）
docker build -t <service-name> .
```
