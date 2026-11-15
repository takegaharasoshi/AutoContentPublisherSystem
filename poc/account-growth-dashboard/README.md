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
定期実行は試験提供中の機能で、**実際に通るかは開発計画 34-3 の手動実行で確かめる**（まだ通していない）。

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

- **Setup script**: `pip install awscli`（集計スクリプトが `aws` コマンドを呼ぶため。AWS CLI が最初から入っているかはドキュメントに記載がない）
- **Network access**: Limited のまま、Allowed domains に `api.line.me` を足す（AWS への通信は既定の許可に入っている見込み）
- **リポジトリ**: このリポジトリ（main）

### 定期実行の登録

- 時刻: 毎週火曜 8:00（日本時間）。cron で書くなら UTC で `0 23 * * 1`（月曜 23:00 UTC = 火曜 8:00 JST）。数分遅れることがある
- 手動で 1 回動かすときは、詳細画面の「Run now」
- 指示文（そのまま貼る）:

```
アカウント成長ノートを更新してください。この実行は無人で動きます。下の 4 つの操作だけを、順に 1 つずつ実行してください（コマンドを書き換えない。cd や && でつながない）。

1. python3 content/insights-analysis/run_queries.py growth_account_weekly growth_post_weekly
2. python3 poc/account-growth-dashboard/build.py
3. poc/account-growth-dashboard/out/growth.html を、Artifact の publish に url として https://claude.ai/artifact/NMPNxbEYTwtC8AVQDSFwBk を渡して公開し直す（新しいページを作らない）
4. python3 poc/account-growth-dashboard/report.py --send

守ること:
- リポジトリのファイルを変更しない。コミット・push をしない。
- 環境変数の値を表示しない（env・printenv・echo・cat などで出さない）。エラーの調査でも同じ。
- 1 か 2 が失敗したら 3 と 4 はしない。3 が失敗しても 4 は行う。失敗した操作をやり直したり、別の方法を試したりしない。

最後に、何日収集分までを載せたか（2 の出力に出る）と、4 つの操作それぞれの成否を 3 行以内で書いてください。失敗があれば、どの操作で何が出たかをそのまま書いてください。
```

### うまく届かないとき

- LINE が届かない / ページが古い → 定期実行の一覧からその回の記録を開き、最後の報告でどの操作が失敗したかを見る
- 1 が `AccessDenied` → 環境変数の ARN が違う（管理者のシークレットを指している・未設定）か、アクセスキーが無効
- 1 が `aws: command not found` → Setup script が走っていない
- 4 が通信エラー → Allowed domains に `api.line.me` が入っていない
- 3 だけ失敗する → 既存のページをクラウドから上書きできていない。公開先を作り直し、この README と `report.py` の `PAGE_URL` を新しい URL に差し替える
- 手元で同じことをする（つなぎ）: 上の「更新の手順」を WSL で実行する

## 手元で無人で動かす案（使っていない。クラウドが通ったら `weekly.sh` ごと消す）

デスクトップアプリのスケジュールタスクからは WSL のフォルダを作業フォルダに選べず、`wsl.exe` も呼べなかった（2026-11-14〜15）。
Windows のタスクスケジューラから `wsl.exe` で `weekly.sh build`（集計とページの書き出し）・`weekly.sh send`（LINE 送信）を呼び、
ページの公開し直しだけを Claude に任せる形は作れるが、火曜の朝に PC が起動していることが前提になるため採らなかった。
