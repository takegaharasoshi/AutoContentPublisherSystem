# infra — AWS CDK プロジェクト（TypeScript）

AutoContentPublisherSystem のインフラ定義。
スタック構成・リソース仕様は [docs/infra/stacks.html](../docs/infra/stacks.html) を参照。

## 前提

- すべての CDK コマンドに `-c env=prod` の指定が必要（未指定・未対応の値はエラーで失敗する）
- CDK コマンドでは論理スタック ID（`FoundationStack` など）を指定する。CloudFormation 上の実スタック名は `Prod-FoundationStack` のように環境名プレフィックス付きで作成される

## よく使うコマンド

```bash
npm run build            # TypeScript コンパイル
npm test                 # Jest テスト実行
npx cdk ls -c env=prod                       # スタック一覧
npx cdk synth -c env=prod                    # テンプレート出力
npx cdk diff -c env=prod <StackName>         # デプロイ前の差分確認
npx cdk deploy -c env=prod <StackName>       # デプロイ（手動実行。docs/infra/cicd.html 参照）
```
