---
title: Codex から直接プロジェクトを動かす（AGENTS.md の docs 制約緩和 + スキルの両エージェント共用）
slug: codex-direct-operation
status: 待機             # inbox | 醸成中 | 再醸成待ち | 待機 | 採用 | 見送り
kind: 単発               # 単発 | 構想
created: 2026-09-20
updated: 2026-09-20
condition: "開発レーンのフリーズ窓（docs/plans/index.html を触るため）で development-plan.html に Phase 23（23-1〜23-3 + 確認待ち 2 件）を起票する。転記下書きは codex-direct-operation.html セクション 8。起票が終わったら採用へ更新"
parent: ""               # 構想の子の場合、親の slug
children: []             # 構想の場合、子の slug のリスト
detail: "codex-direct-operation.html"
disposition: ""          # 転記完了で採用に更新し、Phase 23 へのリンクを書く
---

## 要旨

**2026-09-20 の壁打ちで「やる」と決定（待機。開発計画への転記待ち）**。整理された現在形（検証事実・線引き・リスク・ユーザー決定・Phase 23 の転記下書き）は `codex-direct-operation.html` を参照。

## 前提条件・再検討トリガー

- （解消）Codex のスキル探索パス: リポジトリの `.agents/skills/` を拾う（2026-09-20 に `codex exec --sandbox read-only` で Remotion スキル 6 本の列挙を確認。明示起動は `$<skill-name>`）
- （解消）スキル本文の Claude 依存の棚卸し: `/goal`（quiz-stock-replenish の G1〜G3・step の前提。**ただし Codex にも `/goal` があり〔stable・既定で有効〕、差は stop after 句と評価者〔独立評価 vs 自己申告〕のみ**）、「Codex に委譲」の記述（quiz のリサーチ・imagegen）、スラッシュ参照と主語「Claude」の 3 種類のみ
- （解消）線引き: 並行可レーンのパス = 許可、開発レーンのパス = 禁止。`docs/plans/index.html` セクション 2 の判定表と 1 対 1
- 品質差の検証は Phase 23 の確認待ち項目で行う（1 バッチの差し戻し率を Claude 実績と比較）
- `step` の Claude 固有フロントマター `disable-model-invocation: true` を Codex が無視するかは 23-1 の完了条件で確認

## 原文メモ

（2026-09-20）

新しいアイデアです。

Claude Code のトークン消費を少なくするために、一部の作業について Codex からタスクを行うことを検討しています。

例えば：
• 脳みそコーチの在庫補充
• アイデアの壁打ち
• 課題の棚卸し

上記のように、システム設計書やコードの品質に影響が少ないタスクについては、Codex から作業したいと考えております。

現状は MCP を使って Claude Code から Codex を呼び出すところまではできていると思うのですが、このプロジェクトを Codex から直接動かすということはまだやっていなかったと思うので、そのための環境を整備したいです。

具体的には、現状 agents.md ファイルが設計書配下（docs 配下）を一切触れないような状態になっているかと思いますので、そのあたりを修正し、Codex から動かしても問題なく動くようにしたいと考えています。

また、各種スキルについてもClaude Codeのスキルになっていると思うので、コーデックスでも動くようなスキルに変換し、どちらでも使えるようにしたいと考えております。
確かスキルの共有には、シンボリックリンクみたいなものを使えば、両方のエージェントから全く同じスキルを使えると記憶しているので、その方針で考えてます。

以上です。

### 2026-09-20

**論点と判断**（観点 ③④⑤⑥⑦）:
- 置き場は検証で決着。`.agents/skills/` を Codex が拾い、Claude Code は `.claude/skills/` のリンク経由で同じ実体を読む（Remotion スキルの前例・リンク 6 本は git 追跡済み）。新規要素なし
- 線引きはレーン規則をそのまま使う。3 作業（週次補充・アイデア壁打ち・課題棚卸し）は全部「常に並行可」のレーンなので、「Codex 直接セッションは開発レーン禁止」と宣言すれば docs の許可パスが自動的に決まる（`docs/ideas/` `docs/issues/` `docs/plans/<set_code>*.html` `content/<set>/` `.agents/skills/`。禁止は `docs/app/` `docs/infra/` `docs/strategy/` `docs/plans/development-*` `docs/index.html` `services/` `shared/` `infra/` `database/` `CLAUDE.md`）
- MCP ワーカー時との両立が最大のリスク。AGENTS.md を素朴に緩めると委譲タスクで docs を書き換える事故が起きる。対策は AGENTS.md の条件付き許可 + CLAUDE.md 委譲ルールへの明記（Codex はプロンプト指示を AGENTS.md より優先する仕様）
- git ルールは CLAUDE.md への参照で逃がす（二重記述禁止）。直接セッションはスキルの終了規律に従ってコミット + push まで行う
- `/goal` の代替: SKILL.md に「エージェント別の差分」節を設け、Claude = `/goal` 起動、Codex = 同じ完了条件文を `update_plan` の項目に立てて証跡を貼る。骨格は共通
- Codex 直接実行では quiz の「Codex 委譲」工程（curl 裏取り・imagegen）が「自分でやる」に変わり工程が短くなる。Web 検索は `--search`
- 品質差は人間ゲートが残るので事故にならず「差し戻し率」として現れる → 確認待ちで測る
- Aurora 到達は Codex サンドボックスのネットワーク設定（`~/.codex/config.toml` のプロジェクト設定）が要る。ユーザー回答で「G1〜G3 通しで試す」に決定
- `umigame-problem-writer` は対象外（ユーザー回答）。`/step` `/incident` も対象外（開発レーン / 本番操作の人間ゲートが濃い）
- 採用時のメモリ更新: Codex への制約 3 点のうち「docs 編集禁止・コミットは Claude」が条件付きに変わる。「独立レビュー（Codex 成果物は Claude がレビュー）」は維持

**積み残し**: なし（Phase 23 の確認待ちへ）

**事実の訂正**（同日・ユーザーの問いで判明）: 「Codex に `/goal` の等価物なし・`update_plan` で代替」は誤り。`codex features list` で `goals = stable / true`、`/goal [<objective>|clear|edit|pause|resume]` が使える。差は (a) Claude は独立評価者 + `stop after N turns`、Codex は自己申告 + 上限なし（`token_budget` は未提供）、(b) 停止はユーザーの `/goal pause` / `clear`。スキルのゴール行は両エージェント共通資産になり、差分節は「stop after 句」と「完了申告前の実コマンド再確認」の 2 点に縮む。詳細 HTML 2・4.3・5・8 を訂正済み

**着地の訂正**（同日）: 当初「採用」で置いたが、体系ルール（index.html セクション 4: 採用 = ステップとして展開済み。開発レーン行きはアイデアレーン内では転記下書きまでで**待機**）に照らして待機へ訂正。転記完了で採用へ更新する

## 転記下書き

`codex-direct-operation.html` セクション 8 を参照（開発計画 Phase 23。転記は開発レーンで行う）。
