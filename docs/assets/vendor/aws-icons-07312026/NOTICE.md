# AWS Architecture Icons（2026-07-31 版）

- 出典: AWS 公式の Architecture Icons（https://aws.amazon.com/architecture/icons/ ）の Asset Package `Icon-package_07312026`（2026-10-18 取得）
- 同梱したもの: `svg/` の 17 枚（サービスアイコン 48 px 版 16 枚 + EventBridge Scheduler のリソースアイコン 1 枚）。パッケージから手を加えずに複写した
- `aws-icons.js` は `svg/` から `tools/docs_aws_icons.py` で生成した Mermaid 用のアイコンパック（Iconify 形式。`<title>` と `id` 属性だけを外している）
- 利用条件: AWS は、顧客とパートナーがこのアイコンを使ってアーキテクチャ図を作ることを認めている（上記の公式ページの記載）。オープンソースのライセンスではないため、本リポジトリでは**設計書の構成図に使う用途に限る**。アイコンの形や色は変えない。AWS の商標（サービス名・ロゴ）の権利は Amazon Web Services, Inc. またはその関連会社に帰属する
- 足し方: 公式パッケージから SVG を `svg/` に複写し、`tools/docs_aws_icons.py` の `ICON_NAMES` に名前を足して実行する。版を上げるときはフォルダ名の日付も変え、設計書体系ガイドのライブラリ一覧を直す
