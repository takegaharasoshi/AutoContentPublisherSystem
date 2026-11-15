# account-growth-dashboard — アカウント成長ノートの PoC

アイデア `docs/ideas/account-growth-visualization.md` の試作。3 アカウントのフォロワー・再生・リーチを
週単位で見せるスマホ向けのページを、集計ランナーの結果から組み立てる。設計書ではなく試作の資材。

- 公開先（非公開のアーティファクト）: https://claude.ai/artifact/NMPNxbEYTwtC8AVQDSFwBk
- `template.html`: ページ本体。`/*DATA*/` に集計結果が入る。節目の人数・表示名・色は冒頭の `SETS` にある
- `build.py`: 集計結果を埋め込んで `out/growth.html` を書き出す（`out/` は git 管理外）
- `report.py`: 週 1 回の届くレポート（LINE 用の数行の文面）を集計結果から組み立てて標準出力に出す。`--send` を付けたときだけ LINE へ送る（`LINE_CHANNEL_ACCESS_TOKEN`・`LINE_USER_ID`。環境変数に無ければ `~/.bashrc` の `export` 行から読む。値はリポジトリに置かない。2026-11-12 に送信を確認）

## 更新の手順（週 1 回。火曜の朝 8 時 — 日曜の分は月曜 18 時の収集で入るため）

```bash
cd content/insights-analysis && python3 run_queries.py growth_account_weekly growth_post_weekly
```

```bash
python3 poc/account-growth-dashboard/build.py
```

そのあと Claude Code で `out/growth.html` を上の公開先へ公開し直す
（Artifact の publish に `url` として公開先を渡す。渡さないと別のページができる）。

レポートの文面は次で確認できる（`--send` を付けると LINE へ送る）。

```bash
python3 poc/account-growth-dashboard/report.py
```

## クラウドの定期実行（本線。開発計画 Phase 34）

毎週火曜の朝 8 時に、クラウドの Claude Code の定期実行（https://claude.ai/code/routines ）が
「集計 → ページの組み立て → 公開し直し → LINE 送信」を行う。PC の起動に左右されない。
クラウドから本番 DB へは、読み取り専用の経路だけを使う（権限の設計は `docs/infra/security.html` 2.8・D-09）。

下の仕様は 2026-11-15 に公式ドキュメント（code.claude.com の cloud-environments / routines / artifacts）で確認した内容。
**2026-11-15 に定期実行「アカウント成長ノート」を登録し、手動の実行で 4 つの操作すべてが通ることを確かめた**
（https://claude.ai/code/routines/trig_014nrD6d89yZtU2AzUgzU3Cd 。専用の環境 + 専用 IAM ユーザーのキー。所要は 30 秒〜1 分）。
定期実行は試験提供中の機能で、仕様が変わることがある。

### クラウド環境に置く値（名前だけ。値はここにも記録にも書かない）

環境の設定の「Environment variables」に `名前=値` の形で入れる。

| 名前 | 何を入れるか |
|---|---|
| `AWS_ACCESS_KEY_ID` | IAM ユーザー `acps-prod-growth-note-reader` のアクセスキー（登録の直前に発行する） |
| `AWS_SECRET_ACCESS_KEY` | 同じアクセスキーのシークレット |
| `AWS_DEFAULT_REGION` | `ap-northeast-1` |
| `AURORA_CLUSTER_ARN` | 本番クラスターの ARN（下のコマンドで調べる） |
| `AURORA_SECRET_ARN` | **読み取り専用**のシークレット `acps/prod/db/readonly-report` の ARN（下のコマンドで調べる。管理者のシークレットの ARN を入れない） |
| `LINE_CHANNEL_ACCESS_TOKEN` | LINE のチャネルアクセストークン（WSL の `~/.bashrc` にあるものと同じ） |
| `LINE_USER_ID` | LINE の送り先のユーザー ID（同上） |

ARN の調べ方（WSL で実行。どちらも秘密ではない）:

```bash
aws rds describe-db-clusters --query 'DBClusters[0].DBClusterArn' --output text
```

```bash
aws secretsmanager describe-secret --secret-id acps/prod/db/readonly-report --query ARN --output text
```

2 つの ARN を必ず入れる。入れないと集計スクリプトが一覧から自動で探そうとし、IAM ユーザーにその権限がないため失敗する。

**注意**: 公式ドキュメントは、環境変数の値は「その環境を使える人なら誰でも読める」ので秘密を入れないよう注意している。
この環境を使うのは運用者 1 人だけにし、環境をほかの人と共有しない。AWS のキーで読めるのは本番 DB の読み取りだけ、
LINE のトークンでできるのは公式アカウントからの送信だけ、という範囲に絞ってある（漏れたらキーの無効化・トークンの再発行で止める）。

### 環境のそのほかの設定

- **Setup script**: `pip install awscli`（集計スクリプトが `aws` コマンドを呼ぶため。2 回目以降は前回の結果が使い回される）
- **Network access**: Limited のまま、Allowed domains に `api.line.me` を足す（AWS への通信は既定の許可で通った）
- **リポジトリ**: このリポジトリ（main）

### 定期実行の登録

- 時刻: 毎週火曜 7:55（日本時間）で登録してある（8 時ごろに届く。数分遅れることがある）。UTC の cron で書くなら `55 22 * * 1`
- 手動で 1 回動かすときは、詳細画面の「Run now」
- 指示文（そのまま貼る）:

```
アカウント成長ノートを更新してください。この実行は無人で動きます。下の 4 つの操作だけを、順に 1 つずつ実行してください（コマンドを書き換えない。cd や && でつながない）。

1. python3 content/insights-analysis/run_queries.py growth_account_weekly growth_post_weekly
2. python3 poc/account-growth-dashboard/build.py
3. ページを公開し直す。次の 2 つを順に行う。
   3a. Artifact の read で https://claude.ai/artifact/NMPNxbEYTwtC8AVQDSFwBk を読む（公開の前に必ず読む。読まずに公開すると拒否される。読んだ中身は使わない）
   3b. poc/account-growth-dashboard/out/growth.html を、Artifact の publish に url として https://claude.ai/artifact/NMPNxbEYTwtC8AVQDSFwBk を渡して公開する（新しいページを作らない）。このファイルは 2 で全体を作り直したもので、公開中のページをまるごと置き換えてよい（公開中の内容を取り込む必要はない。ファイルは編集しない）
4. python3 poc/account-growth-dashboard/report.py --send

守ること:
- リポジトリのファイルを変更しない。コミット・push をしない。
- 環境変数の値を表示しない（env・printenv・echo・cat などで出さない）。エラーの調査でも同じ。
- 1 か 2 が失敗したら 3 と 4 はしない。3 が失敗しても 4 は行う。
- 失敗した操作をやり直したり、別の方法を試したりしない。例外は 3b だけで、拒否されたら同じ内容でもう 1 回だけ公開を試してよい（それでも拒否されたら止める）。

最後に、何日収集分までを載せたか（2 の出力に出る）と、4 つの操作それぞれの成否を 3 行以内で書いてください。失敗があれば、どの操作で何が出たかをそのまま書いてください。
```

### うまく届かないとき

- LINE が届かない / ページが古い → 定期実行の一覧からその回の記録を開き、最後の報告でどの操作が失敗したかを見る
- 1 が `AccessDenied` → 環境変数の ARN が違う（管理者のシークレットを指している・未設定）か、アクセスキーが無効
- 1 が `aws: command not found` → Setup script が走っていない
- 4 が通信エラー → Allowed domains に `api.line.me` が入っていない
- 3 だけ失敗する → 新しいセッションは、公開の前にそのページを一度読んでおかないと拒否される（初回の試行で起きた。指示文の 3a が読む手順）。指示文が上のとおりかを確かめる
- 手元で同じことをする（つなぎ）: 上の「更新の手順」を WSL で実行する

## 採らなかった案

デスクトップアプリのスケジュールタスクからは WSL のフォルダを作業フォルダに選べず、`wsl.exe` も呼べなかった（2026-11-14〜15）。
Windows のタスクスケジューラから `wsl.exe` で集計と送信を呼ぶ形は、火曜の朝に PC が起動していることが前提になるため採らなかった
（そのためのスクリプト `weekly.sh` は、クラウドで通った 2026-11-15 に削除した）。
