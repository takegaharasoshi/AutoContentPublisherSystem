# CLAUDE.md

## プロジェクト概要

AutoContentPublisherSystem — AWS 上で動作する画像生成・SNS 自動投稿バッチシステム。
モノリポジトリ構成で、サービスごとにコンテナイメージ・CDK スタック・CI/CD パイプラインを分離する。

## リポジトリ構成

```
AutoContentPublisherSystem/
├── docs/
│   ├── document-guide.md
│   ├── overview/
│   │   └── system-overview.md
│   ├── design/
│   │   ├── architecture.md
│   │   ├── batch.md
│   │   ├── cicd.md
│   │   ├── operation.md
│   │   └── security.md
│   ├── specs/
│   │   ├── infrastructure.md
│   │   ├── workflow.md
│   │   └── database.md
│   └── development-plan.md
├── infra/                   # AWS CDK プロジェクト
├── services/
│   ├── image-batch/         # 画像生成バッチ（Python）
│   └── sns-post-batch/      # SNS 投稿バッチ（Python）
├── shared/                  # サービス間共通ライブラリ（Python）
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
- **CI/CD**: CodePipeline → CodeBuild → ECR push → CDK Deploy

## 開発計画

- 開発計画と進捗は `docs/development-plan.md` で管理する
- Phase 0〜9 の段階的アプローチで、インフラ構築 → 空回し確認 → 業務ロジック実装の順に進める
- 各ステップは「Claude Code でコード作成 → ユーザーが AWS 上で稼働確認 → 次へ」の流れで進める
- 作業開始時は `docs/development-plan.md` を読み、現在の Phase・ステップを確認してから着手する

## ドキュメント更新ルール

コードやインフラに変更を加えた際は、実装との乖離が生じないよう関連ドキュメントも同時に更新する。

### 更新対象と更新タイミング

| 変更内容 | 更新するファイル |
|---|---|
| アーキテクチャ・技術選定の変更 | `docs/design/architecture.md` |
| バッチ処理フロー・業務ルールの変更 | `docs/design/batch.md` |
| CI/CD パイプラインの変更 | `docs/design/cicd.md` |
| 運用手順・監視運用の変更 | `docs/design/operation.md` |
| 認証・認可・秘密情報の変更 | `docs/design/security.md` |
| CDK スタック構成の変更 | `docs/specs/infrastructure.md` |
| Step Functions 定義・環境変数・監視リソースの変更 | `docs/specs/workflow.md` |
| DB テーブル・カラムの変更 | `docs/specs/database.md` |
| ステップ完了・問題発生 | `docs/development-plan.md` |

### ルール

- 設計と異なる実装をした場合は、実装に合わせてドキュメントを修正する（ドキュメントを正として実装を戻すのではなく、実態を記録することを優先する）
- 将来の拡張予定として記載している項目（AdminApiStack 等）は、実装開始時にドキュメントを具体化する
- 設計変更が発生した場合は、変更理由をドキュメントのコメントや備考に残す

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
