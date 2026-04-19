# 設計書体系ガイド

本ドキュメントは AutoContentPublisherSystem の設計書体系を定義する。

## 設計原則

1. **SSOT (Single Source of Truth)**: 各情報の「正」は 1 箇所のみ。他のドキュメントでは参照リンクで代替する
2. **段階的詳細化**: L0（Why/What）→ L1（How: 論理設計）→ L2（How: 実装仕様）の 3 層構造
3. **関心の分離**: 「何を作るか」「どう作るか」「どう動かすか」を分離する

## ドキュメント階層構造

```
docs/
├── document-guide.md              # 本ファイル（設計書体系ガイド）
│
├── overview/                       # L0 概要層（Why / What）
│   └── system-overview.md          #   システムの目的・スコープ・構成概要
│
├── design/                         # L1 論理設計層（How: 設計判断）
│   ├── architecture.md             #   AWS サービス構成・ネットワーク・データフロー
│   ├── batch.md                    #   バッチ処理フロー・業務ルール・冪等性方針
│   ├── cicd.md                     #   CI/CD フロー・ブランチ戦略
│   ├── operation.md                #   運用手順・監視方針・コスト方針
│   └── security.md                 #   認証・認可・秘密情報管理の方針
│
├── specs/                          # L2 実装仕様層（How: 実装詳細）
│   ├── infrastructure.md           #   CDK スタック構成・リソース定義
│   ├── workflow.md                 #   Step Functions ASL・環境変数・監視リソース詳細
│   └── database.md                 #   テーブル定義・ER 図・制約
│
└── development-plan.md             # 開発計画・進捗管理（横断的管理文書）
```

## 各ドキュメントの責務

| ドキュメント | 層 | 責務 |
|---|---|---|
| [overview/system-overview.md](overview/system-overview.md) | L0 | システムの目的・構成概要・技術選定一覧 |
| [design/architecture.md](design/architecture.md) | L1 | AWS サービスの論理構成と設計判断 |
| [design/batch.md](design/batch.md) | L1 | バッチ処理の論理フローと業務ルール |
| [design/cicd.md](design/cicd.md) | L1 | CI/CD パイプライン構成・デプロイ方式 |
| [design/operation.md](design/operation.md) | L1 | 運用手順・監視方針・コスト最適化 |
| [design/security.md](design/security.md) | L1 | 認証・認可・秘密情報管理の方針と具体設定 |
| [specs/infrastructure.md](specs/infrastructure.md) | L2 | CDK スタック構成・リソース定義・デプロイ順序 |
| [specs/workflow.md](specs/workflow.md) | L2 | Step Functions ASL・環境変数・監視リソース詳細 |
| [specs/database.md](specs/database.md) | L2 | テーブル定義・ER 図・制約 |

## 依存関係

```
overview/
  └── system-overview.md             (全ドキュメントの前提知識)
            │
    ┌───────┼──────────────────────────────────┐
    ▼       ▼                                  ▼
design/
  ├── architecture.md ◄── security.md    cicd.md   operation.md
  │       │                  │              │           │
  │  ┌────┼──────────────────┤              │           │
  │  ▼    ▼                  ▼              ▼           │
  └── batch.md          (参照元)        (参照元)         │
         │                                              │
         ▼                                              │
specs/                                                  │
  ├── infrastructure.md                                 │
  ├── workflow.md ──────────────────────────────────────┘
  └── database.md            (operation.md は specs/* を参照)
```

- 上位層（overview/）は下位層（design/, specs/）の詳細を複写しない。読者の導線として必要な参照リンクのみ許容する
- design/ から specs/ への参照は、SSOT 配置ルールに基づく参照リンク（「詳細は specs/xxx.md を参照」形式）に限定する。design/ 側に specs/ の内容を複写しない

## SSOT 配置ルール（主要な情報の配置先）

| 情報 | SSOT（正） | 他ドキュメントでの扱い |
|---|---|---|
| デプロイ方式 | design/cicd.md | design/architecture.md は方針一文+参照リンク |
| DB 準備確認の仕組み | design/batch.md | design/architecture.md は設計判断理由のみ |
| エラーハンドリング（アプリ実装） | design/batch.md | design/operation.md は運用対応手順のみ |
| エラーハンドリング（Step Functions） | specs/workflow.md | design/operation.md は運用対応手順のみ |
| 監視リソース定義（メトリクス名・閾値） | specs/workflow.md | design/operation.md は運用フロー+参照 |
| Secret 名規約 | design/security.md | 他ドキュメントは参照リンクのみ |
| IAM ロール権限定義 | design/security.md | design/architecture.md は方針のみ |
| S3 Lifecycle Policy | specs/infrastructure.md | design/architecture.md は方針のみ |
| 順次実行方針 | design/architecture.md | design/batch.md は処理フロー図で示す |

## 更新ルール

- 設計と異なる実装をした場合は、実装に合わせてドキュメントを修正する
- 各情報の SSOT を更新し、他ドキュメントは参照リンクで代替する
- 変更理由はドキュメントの備考に残す
