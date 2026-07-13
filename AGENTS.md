# AGENTS.md

Codex（実装ワーカー）向けのプロジェクト規約。全体像は `CLAUDE.md` と `docs/` の設計書を参照。

## プロジェクト概要

AutoContentPublisherSystem — AWS 上で動作する画像生成・SNS 自動投稿バッチシステム。
モノリポジトリ構成。サービスごとにコンテナイメージ・CDK スタック・CI/CD を分離する。

## リポジトリ構成

- `infra/` — AWS CDK プロジェクト（TypeScript）
- `services/db-readiness-check/` — DB 準備確認バッチ（Python）
- `services/image-batch/` — 画像生成バッチ（Python）
- `services/sns-post-batch/` — SNS 投稿バッチ（Python）
- `shared/` — サービス間共通ライブラリ（Python）
- `database/` — DDL ファイル（スキーマ管理）
- `docs/` — 設計書（HTML）。**編集禁止**（Claude / ユーザーが管理する。旧 Markdown 設計書は `docs/_archive/` にあり現役ではない）

## 技術スタック

- 言語: Python（バッチ処理）、AWS CDK は TypeScript
- DB: Aurora Serverless v2（MySQL 互換）
- 実行基盤: ECS Fargate RunTask（ECS Service は使用しない）
- ワークフロー: Step Functions Standard、スケジューラ: EventBridge Scheduler
- 既定の環境名は `prod`（CDK コマンドは `-c env=prod` を付ける）

## コーディング規約

- Python コードは PEP 8 に準拠し、型ヒントを使用する。docstring は Google スタイル
- CDK の命名は設計書（`docs/infra/stacks.html`）に合わせる（例: `FoundationStack`, `ImageBatchStack`, `SnsPostBatchStack`）
- テストは `services/<service>/tests/` に置き、`pytest` で実行する

## 作業ルール

- 指示されたタスクの範囲だけを実装する。関係ないファイルは変更しない
- `docs/` 配下・`CLAUDE.md`・`.claude/` は変更しない
- git commit は指示された場合のみ行い、コミットメッセージは簡潔な日本語で書く（例: `設計書の参照先を整理`）
- シークレットや環境固有値はコミットしない。認証・秘密情報の規約は `docs/infra/security.html` に従う（Secrets Manager で管理）

## 応答フォーマット

- 最終応答は簡潔にする。含めるのは「変更ファイル一覧」「実施内容の要約（5 行以内）」「実行したテスト・確認の結果」のみ
- 最終応答にコード全文や長い引用を貼らない（コードはファイルに書けば十分）
