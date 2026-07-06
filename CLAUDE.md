# CLAUDE.md

## プロジェクト概要

AutoContentPublisherSystem — AWS 上で動作する画像生成・SNS 自動投稿バッチシステム。
モノリポジトリ構成で、サービスごとにコンテナイメージ・CDK スタック・CI/CD パイプラインを分離する。

## リポジトリ構成

> **注意**: `infra/`, `services/`, `shared/`, `database/` は未作成。開発計画に沿って段階的に作成する。

```
AutoContentPublisherSystem/
├── docs/                            # 設計書（下記「設計書体系」参照）
│   ├── index.html                   #   設計書体系ガイド（エントリポイント）
│   ├── assets/style.css             #   設計書共通スタイル
│   ├── overview/                    #   システム概要
│   ├── infra/                       #   インフラ設計書（HTML）
│   ├── app/                         #   アプリ設計書（大枠は骨子版作成済み・Phase 9 で詳細化。セット別設計書は app/sets/ に初セット追加時に作成）
│   ├── _archive/                    #   旧 Markdown 設計書（参考資料。現役ではない）
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

設計書は **HTML** で記述する（開発計画 `docs/development-plan.md` のみ Markdown）。体系の全体像・スコープ境界・設計 Fix 基準は `docs/index.html` を参照。

- **インフラ設計とアプリ設計を明確に分離する**。インフラ設計は `docs/infra/`、アプリ設計は `docs/app/`（大枠は Phase A、詳細は Phase 9 で作成する 2 段階方針）
- **インフラ設計書にアプリ仕様を書かない**。作業中にアプリの論点（処理ロジック・テーブル設計等）が出たら `docs/app/index.html` の検討メモに記録する
- HTML 設計書は外部 CDN に依存せず、`docs/assets/style.css` を共通スタイルとして使用する。閲覧はローカルブラウザまたは VS Code の Live Preview で行う（GitHub 上ではソース表示になる）

| ディレクトリ | 目的 | ドキュメント |
|---|---|---|
| `docs/overview/` | システムの目的・スコープ・技術選定 | `system-overview.html` |
| `docs/infra/` | インフラ設計（現役の設計書） | `architecture.html`, `stacks.html`, `workflow.html`, `security.html`, `cicd.html`, `operation.html` |
| `docs/app/` | アプリ設計（大枠は骨子版作成済み / 詳細は Phase 9。セット追加で増えるのは `sets/` のセット別設計書 1 本のみ） | `index.html`（目次・検討メモ）, `design-outline.html`（全体方針・親ページ）, `batch-flow.html`, `data-model.html`, `operation.html`, `requirements-notes.html` |
| `docs/_archive/` | 旧 Markdown 設計書（アプリ設計の参考資料。現役ではない） | 参照は Phase A・Phase 9 のアプリ設計時のみ |

### ドキュメント参照ガイド（タスク別）

タスクに必要なドキュメントだけを読み、コンテキストを節約すること。

| タスク | 読むべきドキュメント |
|---|---|
| プロジェクトの全体像を把握 | `docs/overview/system-overview.html` |
| CDK コードを書く・修正する | `docs/infra/stacks.html`（前提知識が必要なら `docs/infra/architecture.html`） |
| Step Functions 定義を書く・修正する | `docs/infra/workflow.html` |
| DB 準備確認タスクを実装・修正する | `docs/infra/workflow.html` セクション 2 |
| CI/CD パイプラインを構築する | `docs/infra/cicd.html` |
| 監視・通知を設定する | `docs/infra/workflow.html` セクション 7〜10 + `docs/infra/operation.html` |
| 認証・秘密情報の設定を変更する | `docs/infra/security.html` |
| アプリ設計の大枠（全体方針・骨子）を確認する | `docs/app/design-outline.html`（親ページ）+ 分冊 `batch-flow.html` / `data-model.html` / `operation.html` |
| セットを追加・廃止する | `docs/app/operation.html` セクション 2 + `docs/app/design-outline.html` セクション 1.1（セット別設計書ルール） |
| アプリ（業務ロジック）の詳細設計・実装 | Phase 9 以降。Phase A の大枠設計書（骨子版）を詳細化してから着手する |
| 開発の次ステップを確認する | `docs/development-plan.md` |

### 設計 Fix・レビューの運用ルール

設計が Fix しない問題の再発防止ルール（詳細は `docs/index.html` セクション 4）:

- 設計書は「次フェーズの作業に着手できる」水準で一時 Fix とする。「生成 AI の指摘ゼロ」を目指さない
- 設計レビューは観点を限定して行い、最大 2 巡まで。指摘は blocker（誤り・矛盾・欠落）と改善提案に分類し、**blocker のみ修正**する
- 改善提案・持ち越し論点は `docs/development-plan.md` 末尾の「設計課題リスト」に記録する

## 開発計画

- 開発計画と進捗は `docs/development-plan.md` で管理する
- **Phase D（インフラ設計の一時 Fix）→ Phase A（アプリ設計の大枠）→ Phase 9（アプリ設計の詳細・前倒し）→ Phase 0〜8（インフラ構築: 空回し確認・監視・CI/CD まで）→ Phase 10 以降（アプリ実装。冒頭 10-1 でアプリ設計の最終 Fix）** の順に進める
- 各ステップは「Claude Code でコード作成 → ユーザーが AWS 上で稼働確認 → 次へ」の流れで進める
- 作業開始時は `docs/development-plan.md` を読み、現在の Phase・ステップを確認してから着手する

## ドキュメント更新ルール

コードやインフラに変更を加えた際は、関連ドキュメントも同時に更新する。

- 設計と異なる実装をした場合は、実装に合わせてドキュメントを修正する（実態の記録を優先）。変更理由はドキュメントの備考（`decision` コールアウト）に残す
- 同じ情報を複数ドキュメントに書かない。詳細は 1 箇所に書き、他からは参照リンクを張る
- 将来の拡張予定として記載している項目は、実装開始時にドキュメントを具体化する

## コーディング規約

- Python コードは PEP 8 に準拠する
- 型ヒントを使用する
- docstring は Google スタイルを使用する

## 開発上の注意事項

- Aurora Serverless v2 の自動一時停止を利用するため、Step Functions ワークフローの最初のステートとして DB 準備確認 ECS タスクを実行する（FoundationStack で定義）。バッチアプリケーション（ECS タスク）は DB が利用可能な状態を前提とする
- 外部 API 呼び出し失敗時は Step Functions の Retry / Catch でハンドリングする
- デプロイは Blue/Green なし、ECS Service なし。Docker イメージを ECR に push し、新しいタスク定義リビジョンを登録する方式
- 将来の複数セット運用を前提とする（詳細なデータ設計は Phase 9 のアプリ設計で定義する）

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
cd infra && cdk diff -c env=prod <StackName>

# CDK デプロイ
cd infra && cdk deploy -c env=prod <StackName>

# Docker ビルド（各サービスディレクトリ内で）
docker build -t <service-name> .
```
