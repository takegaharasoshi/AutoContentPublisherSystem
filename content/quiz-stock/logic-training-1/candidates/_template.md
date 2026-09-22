---
# 1 候補 1 ファイル。ファイル名 = <id>.md(例: m01.md / n03.md)。フロントマターの値は「key: value」1 行ずつ
id: m01                      # 必須。バッチ内で一意。m = 朝(morning)・n = 夜(night)+ 2 桁連番
batch: 2026-09-w4            # 必須。作った週次補充のバッチ名(stock_items.py のバッチ名と同じ)
slot: morning                # 必須。morning | night
state: unreviewed            # 必須。unreviewed | ok | ng | hold | drafting | approved | final_ng | withdrawn(意味は README.md)
version: 1                   # 必須。本文の最新の「版 N」と一致させる(修正版を足したら +1)
supersedes:                  # 任意。別ファイルへ切り出した修正版のときだけ元の id(元は集計から外れる)
stock_no:                    # 完成稿へ進めたら stock_items.py の no(A47 等)。候補 OK の段階では空
source: https://example.com/ # 必須。流布例 URL を 1 件以上(候補段階で裏取り。問題文の転載は禁止)
example: false               # 投稿対象外の検証例だけ true(実際の候補は false か省略)
---

# m01(朝)候補

## 版 1(原案・YYYY-MM-DD)
- 問題文: (80 字以内。候補段階は骨子でよいが、仕上げで守る上限を意識する)
- 答え: (30 字以内)
- 必要な図の内容: (なし / イラストで見せる必要のあるものを 1 行で)
- 出典メモ: (類型・解法構造の要約と流布の確認結果。転載しない)

### 判定
- 判定: (空欄 = 未レビュー / OK / NG / 保留。理由は書かなくてよい)
- 日付:
- 段階: 候補
- 理由(任意):

<!-- 修正版は下に「## 版 2(修正版・YYYY-MM-DD)」として追記する。版 1 の原案と判定は書き換えない。
     完成稿にしてから NG になったときも、その版の下に「### 判定」を足して「段階: 完成稿」「判定: NG」を記録し、
     フロントマターの state を final_ng にする(再選別待ち)。 -->
