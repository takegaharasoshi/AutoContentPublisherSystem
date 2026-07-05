# 旧 Markdown 設計書アーカイブ

このディレクトリのファイルは **現役の設計書ではない**。

2026-07-06 の設計書体系見直し（インフラ設計とアプリ設計の分離、設計書の HTML 化）に伴い、旧 Markdown 設計書を退避したもの。現行の設計書体系は [docs/index.html](../index.html) を参照。

## 位置付け

- インフラ関連の内容（architecture / infrastructure / workflow / security / cicd / operation のインフラ部分）は `docs/infra/*.html` に移行済み。このアーカイブを参照しないこと
- アプリ設計の内容（batch.md の処理フロー・冪等性設計、database.md のテーブル定義、operation.md のアプリ運用手順）は **Phase 9（アプリ設計）の参考資料** として保管している

| ファイル | 旧配置 | 主な内容 |
|---|---|---|
| document-guide.md | docs/ | 旧設計書体系ガイド（L0/L1/L2 の 3 層構造） |
| system-overview.md | docs/overview/ | システム概要 |
| architecture.md | docs/design/ | アーキテクチャ設計 |
| batch.md | docs/design/ | バッチ処理設計（冪等性・再試行・投稿ステータス等のアプリ設計を含む） |
| cicd.md | docs/design/ | CI/CD 設計 |
| operation.md | docs/design/ | 運用設計（アプリ運用手順・手動補正 SQL を含む） |
| security.md | docs/design/ | セキュリティ設計 |
| infrastructure.md | docs/specs/ | CDK スタック実装仕様 |
| workflow.md | docs/specs/ | Step Functions 実装仕様 |
| database.md | docs/specs/ | データベース設計（6 テーブルの定義・ER 図） |
