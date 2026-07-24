# CLAUDE.md

## プロジェクト概要

AutoContentPublisherSystem — AWS 上で動作する画像生成・SNS 自動投稿バッチシステム。
モノリポジトリ構成で、サービスごとにコンテナイメージ・CDK スタック・CI/CD パイプラインを分離する。

## リポジトリ構成

> **注意**: `services/`, `shared/` はディレクトリのみ作成済み（中身は開発計画に沿って段階的に実装する）。

```
AutoContentPublisherSystem/
├── docs/                            # 設計書（下記「設計書体系」参照）
│   ├── index.html                   #   設計書体系ガイド（エントリポイント）
│   ├── assets/style.css             #   設計書共通スタイル
│   ├── strategy/                    #   事業戦略書（収益化戦略・予算・KPI・展開方針）
│   ├── overview/                    #   システム概要
│   ├── infra/                       #   インフラ設計書（HTML）
│   ├── app/                         #   アプリ設計書（大枠は骨子版作成済み・Phase 9 で詳細化。セット別設計書は app/sets/ に初セット追加時に作成）
│   ├── _archive/                    #   旧 Markdown 設計書（参考資料。現役ではない）
│   ├── development-plan.md          #   開発計画・進捗管理（現役の計画・設計課題リスト）
│   └── development-log.md           #   開発記録（完了ステップの実施記録）
├── infra/                           # AWS CDK プロジェクト（TypeScript）
├── services/
│   ├── db-readiness-check/          # DB 準備確認（Python）
│   ├── image-batch/                 # 画像生成バッチ（Python）
│   └── sns-post-batch/              # SNS 投稿バッチ（Python）
├── database/                        # DDL ファイル（スキーマ管理）
├── shared/                          # サービス間共通ライブラリ（Python）
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

設計書は **HTML** で記述する（開発計画 `docs/development-plan.md` と開発記録 `docs/development-log.md` のみ Markdown）。体系の全体像・スコープ境界・設計 Fix 基準は `docs/index.html` を参照。

- **インフラ設計とアプリ設計を明確に分離する**。インフラ設計は `docs/infra/`、アプリ設計は `docs/app/`（大枠は Phase A、詳細は Phase 9 で作成する 2 段階方針）
- **事業とシステムを分離する**。事業の意思決定（収益化戦略・予算・KPI・プラットフォーム展開方針）は `docs/strategy/business-strategy.html` に書き、システム設計書には書かない
- **インフラ設計書にアプリ仕様を書かない**。作業中にアプリの論点（処理ロジック・テーブル設計等）が出たら `docs/app/index.html` の検討メモに記録する
- HTML 設計書は外部 CDN に依存せず、`docs/assets/style.css` を共通スタイルとして使用する。閲覧はローカルブラウザまたは VS Code の Live Preview で行う（GitHub 上ではソース表示になる）

| ディレクトリ | 目的 | ドキュメント |
|---|---|---|
| `docs/strategy/` | 事業戦略（収益化戦略・予算・KPI・展開方針・セットポートフォリオ） | `business-strategy.html` |
| `docs/overview/` | システムの目的・スコープ・技術選定 | `system-overview.html` |
| `docs/infra/` | インフラ設計（現役の設計書） | `architecture.html`, `stacks.html`, `workflow.html`, `security.html`, `cicd.html`, `operation.html` |
| `docs/app/` | アプリ設計（大枠は骨子版作成済み / 詳細は Phase 9。セット追加で増えるのは `sets/` のセット別設計書 1 本のみ） | `index.html`（目次・検討メモ）, `design-outline.html`（全体方針・親ページ）, `batch-flow.html`, `data-model.html`, `operation.html`, `requirements-notes.html` |
| `docs/_archive/` | 旧 Markdown 設計書（アプリ設計の参考資料。現役ではない） | 参照は Phase A・Phase 9 のアプリ設計時のみ |

### ドキュメント参照ガイド（タスク別）

タスクに必要なドキュメントだけを読み、コンテキストを節約すること。

| タスク | 読むべきドキュメント |
|---|---|
| プロジェクトの全体像を把握 | `docs/overview/system-overview.html` |
| 収益化戦略・予算・KPI・プラットフォーム展開方針を確認する | `docs/strategy/business-strategy.html` |
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
| 過去の実施記録・経緯を確認する | `docs/development-log.md`（完了ステップの確認・備考の全文） |

### 設計 Fix・レビューの運用ルール

設計が Fix しない問題の再発防止ルール（詳細は `docs/index.html` セクション 4）:

- 設計書は「次フェーズの作業に着手できる」水準で一時 Fix とする。「生成 AI の指摘ゼロ」を目指さない
- 設計レビューは観点を限定して行い、最大 2 巡まで。指摘は blocker（誤り・矛盾・欠落）と改善提案に分類し、**blocker のみ修正**する
- 改善提案・持ち越し論点は `docs/development-plan.md` 末尾の「設計課題リスト」に記録する

## 開発計画

- 開発計画と進捗は `docs/development-plan.md` で管理する。ステップ完了時、計画書にはチェック + 完了日 + 要点のみを記録し、詳細な実施記録は `docs/development-log.md` に追記する（計画書の肥大化防止）
- **Phase D（インフラ設計の一時 Fix）→ Phase A（アプリ設計の大枠）→ Phase 9（アプリ設計の詳細・前倒し）→ Phase 0〜8（インフラ構築: 空回し確認・監視・CI/CD まで）→ Phase 10〜13（アプリ実装: 実装準備 → 画像生成バッチ → SNS 投稿バッチ → 定常運用開始）** の順に進める
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

## Codex 連携（実装ワーカー）

Claude のトークン消費を抑えるため、以下のタスクは Codex CLI に委譲する（MCP サーバー `codex` として `.mcp.json` に登録済み。`mcp__codex__codex` ツールで実行し、Claude 自身は作業しない）。

- **まとまったコード生成**: 仕様が確定していて自己完結した実装タスク（新規モジュール・関数の実装、テスト雛形、定型的なボイラープレート。Python / CDK TypeScript とも）
- **テスト修正ループ**: 実装とテストを書かせ、pytest がパスするまで Codex 側で反復させる（委譲指示の完了条件に「pytest 全パス」を含める）
- **ログの一次解析**: 長いエラーログ・コマンド出力はファイルに保存し、`sandbox: read-only` で委譲して原因の要約のみ受け取る（Claude はログ全文を読まない）
- **レビューの一次スクリーニング**: Codex 以外が書いた変更の一次レビュー。指摘の妥当性判断は Claude が行う。Codex 自身の成果物のレビューは Claude が担当する（自己レビュー禁止）
- **機械的な横展開修正**: 同一パターンの一括適用・書式統一など判断を伴わない修正

**Claude が行う**: タスク分解と指示書作成、設計判断、設計書（`docs/`）の作成・更新、Codex 成果物のレビュー、数行で済む小修正（委譲のオーバーヘッドの方が大きいもの）、git コミット

### 委譲時のパラメータ・運用

- `sandbox: workspace-write`（読み取り専用タスクは `read-only`）、`cwd` はリポジトリルート。同じタスクへの追加指示は `codex-reply`（threadId 指定）で同一セッションに出す
- モデルは委譲時（MCP 経由）・直接実行とも既定は `gpt-5.6-terra` / reasoning effort `high`（MCP は `.mcp.json` の起動引数、直接実行は `~/.codex/config.toml` で設定）。per-call の使い分け（GPT-5.6 の序列は sol > terra > luna）:
  - **機械的な横展開・書式統一**（判断を伴わない修正）: `model: "gpt-5.6-luna"` に下げてよい
  - **14-7 級の大型・新規性の高い実装**（新モジュール新設・依存追加・複数コンポーネント横断）: `model: "gpt-5.6-sol"` に上げる
  - エフォートは「確実にこなせる最低レベル」を選ぶ（通常 `high`。sol 委譲で詰まった場合のみ `xhigh`）
- プロジェクト規約は `AGENTS.md` に記載済みで Codex が自動で読む。指示文には規約を重複記載せず、タスク固有の要件（対象ファイル・仕様・完了条件）のみ書く

### トークン節約の作業ルール

- 成果物レビューは `git diff` の差分のみを読む。変更されていないファイルを再読しない
- コードベース・設計書の広い調査は Explore サブエージェントに委ね、本会話に生ファイルを持ち込まない
- 長いコマンド出力（cdk diff・deploy ログ等）は全文を読まず、tail / grep で必要部分のみ取得する

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

# Docker ビルド（リポジトリルートから。shared/ を COPY するためルートをビルドコンテキストにする）
docker build -f services/<service-name>/Dockerfile -t <service-name> .
# ※ db-readiness-check のみ従来方式（サービスディレクトリ内で docker build -t db-readiness-check .）
```
