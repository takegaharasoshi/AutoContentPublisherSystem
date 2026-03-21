# Repository Guidelines

## Project Structure & Module Organization
現時点の SSOT は `docs/` です。`docs/overview/` は概要、`docs/design/` は論理設計、`docs/specs/` は実装仕様を扱います。作業前に `docs/document-guide.md` で参照先を確認し、進行状況は `docs/development-plan.md` を見ます。`plans/` は作業メモ用です。`infra/`、`services/image-batch/`、`services/sns-post-batch/`、`shared/` は今後追加される前提です。

## Build, Test, and Development Commands
このリポジトリは現在ドキュメント中心です。コード追加後は以下を基本コマンドとします。

- `git diff -- docs/`: 設計書の差分確認
- `cd infra && cdk diff <StackName>`: インフラ差分の確認
- `cd infra && cdk deploy <StackName>`: 手動デプロイ
- `cd services/<service> && pytest`: Python テスト実行
- `docker build -t <service-name> services/<service>`: バッチのローカル確認

## Coding Style & Naming Conventions
ドキュメント、コミットメッセージ、PR 説明は日本語で統一します。見出しは短くし、重複説明より参照リンクを優先してください。Python は PEP 8、型ヒント、Google スタイル docstring を採用します。CDK の命名は設計書に合わせ、`FoundationStack`、`ImageBatchStack`、`SnsPostBatchStack` のように役割が分かる名前にします。

## Testing Guidelines
現時点でカバレッジ基準は未設定です。ドキュメント変更では、関連する L0/L1/L2 の整合性と SSOT の更新漏れを確認してください。コード追加時は `services/<service>/tests/` に `pytest` ベースのテストを置き、共通処理から先に検証します。インフラ変更では `cdk diff`、Docker 動作確認、必要に応じて AWS Console での確認を実施します。

## Commit & Pull Request Guidelines
コミットメッセージは履歴に合わせて簡潔な日本語で記述します。例: `設計書の参照先を整理`。通常の作業ブランチは `feature/*` を使用してください。PR には対象範囲、影響するドキュメントやスタック、実施した確認内容を記載し、Step Functions や Scheduler に影響する変更ではログや画面確認結果も添えてください。

## Security & Configuration Tips
シークレットや環境固有値はコミットしません。認証情報は `docs/design/security.md` の規約に従い、Secrets Manager に `acps/{env}/{set_code}/...` 形式で管理します。現在の既定環境名は `prod` です。
