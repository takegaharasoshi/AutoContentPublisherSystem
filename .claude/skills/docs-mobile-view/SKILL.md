---
name: docs-mobile-view
description: 設計書(docs/)をスマホ・外出先から閲覧できるようにする。WSL で HTTP サーバーを起動し Windows の tailscale serve で tailnet 内に公開する手順・URL の調べ方・停止・トラブルシュート。「スマホで設計書を見たい」「外出先から docs を見たい」「昨日のあれをスマホで開けるようにして」等で使う。
---

# 設計書のスマホ閲覧スキル(docs-mobile-view)

`docs/` 配下の HTML 設計書を、同じ Tailscale アカウントのスマホから閲覧できるようにする。
実体は 2 ファイルのツールで、**通常はコマンド 1 本で終わる**。

- `tools/serve-docs.sh` — 起動・停止・状態確認(`start` / `stop` / `status` / `restart`)
- `tools/docs_server.py` — 配信サーバー本体(`docs/` をルートに配信。`.md` は `text/plain` で返しブラウザ上で読めるようにする)

## 1. 通常の依頼(「スマホで見たい」)

```bash
./tools/serve-docs.sh start
```

出力される URL をそのままユーザーに伝える(既定ポート 8765)。

```
http://takegaharapc:8765/            ← MagicDNS の短い名前
http://takegaharapc.tailc2aa8e.ts.net:8765/
```

トップは `docs/index.html`(設計書体系ガイド)で、そこからインフラ/アプリ設計書へリンクで辿れる。
スクリプトは冪等なので、既に動いていても `start` を再実行してよい。

## 2. 仕組み(トラブル時の切り分けに必要)

WSL は NAT で独自の IP を持つため、Windows の Tailscale IP から WSL のサーバーは直接見えない。そこで 2 段構成:

1. WSL: `docs_server.py` が **127.0.0.1:8765 のみ**に bind(LAN には出さない)
2. Windows: `tailscale serve --http=8765 http://127.0.0.1:8765` が tailnet からの接続を Windows の localhost へプロキシ → WSL の localhost 転送で 1 に届く

切り分けの順序 —

| 症状 | 確認 |
|---|---|
| スマホで開けない | `./tools/serve-docs.sh status` で HTTP サーバー稼働 + `tailscale serve` 設定の両方を見る |
| 1 が死んでいる | PC 再起動後は WSL 側だけ落ちる(`tailscale serve` の設定は Windows 側に永続化される)。`start` で復帰 |
| 2 だけ消えている | `tailscale serve status` が空。`start` で再設定 |
| サーバーは生きているのに届かない | Windows から `/mnt/c/Windows/System32/curl.exe -s -o NUL -w "%{http_code}\n" http://localhost:8765/index.html` で 1 の生死、続けて `http://<tailscale名>:8765/index.html` で 2 の生死を確認して層を特定する |
| スマホ側 | Tailscale アプリが接続中か、同じアカウント(`tailscale status` にスマホが並んでいるか)を確認 |

Windows 側 Tailscale CLI: `/mnt/c/Program Files/Tailscale/tailscale.exe`(WSL からそのまま実行できる。管理者権限は不要)。

## 3. 停止

```bash
./tools/serve-docs.sh stop
```

HTTP サーバーを止め、`tailscale serve` の公開設定も解除する。
外出が終わったら止める運用でよいが、**tailnet 内限定公開なので付けっぱなしでも外部からは見えない**。

## 4. 制約・禁止事項

- **Funnel(`tailscale funnel`)は使わない**。インターネット全体に設計書が公開される。ユーザーが明示的に求めた場合のみ、リスクを説明した上で検討する
- 外出先から見るには**自宅 PC が起動していて WSL とサーバーが動いている**必要がある。スリープすると切れる
- ポートを変えたい場合は `DOCS_PORT=9000 ./tools/serve-docs.sh start`(stop / status も同じ環境変数を付ける)
- 配信対象は `docs/` のみ。`content/` の動画やレビュー HTML を見せたい要望が出たら、配信ルートを増やすのではなく `docs_server.py` の `DOCS_DIR` を見直すか、別ポートで起動する判断をユーザーに確認する
