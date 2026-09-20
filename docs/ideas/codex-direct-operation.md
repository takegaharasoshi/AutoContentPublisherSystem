---
title: Codex から直接プロジェクトを動かす（AGENTS.md の docs 制約緩和 + スキルの両エージェント共用）
slug: codex-direct-operation
status: 採用             # inbox | 醸成中 | 再醸成待ち | 待機 | 採用 | 見送り
kind: 単発               # 単発 | 構想
created: 2026-09-20
updated: 2026-09-20
condition: ""            # 再醸成待ち・待機のとき必須（再検討トリガー / 落とし込み条件）
parent: ""               # 構想の子の場合、親の slug
children: []             # 構想の場合、子の slug のリスト
detail: ""               # 詳細 HTML を作ったらファイル名（<slug>.html）
disposition: "開発計画 Phase 23（転記下書きは本ファイル末尾。転記は開発レーンで行う）"
---

## 要旨

**2026-09-20 に採用**。開発計画 Phase 23（Codex 直接セッションの導入）へ展開する。転記下書きは末尾の「転記下書き」節。

決めたこと:
- Codex を「Claude から MCP で呼ばれる実装ワーカー」に加えて「単独で作業を回すエージェント」としても使う。対象は**常に並行可のレーン**（アイデアレーン・課題レーン・セットレーン）に限り、**開発レーンは Codex 直接セッション禁止**（Claude 側の並行作業ルールは変えない）
- スキルの実体を `.agents/skills/` に集約し、`.claude/skills/<name>` は相対シンボリックリンク（Remotion スキルで既に運用中の形）。Codex 0.144.1 が `.agents/skills/` を拾うことは `codex exec` で検証済み
- 両エージェント対応に中立化するスキルは `idea`・`issue`・`quiz-stock-replenish` の 3 本。残り 5 本は「Claude Code 専用」の注記のみ
- `AGENTS.md` は「docs 全面禁止」をやめ、レーン規則と 1 対 1 の許可パス列挙に書き換える。MCP ワーカー時の docs 書き込みは、AGENTS.md の条件（スキル起動時 / 指示文で明示された場合のみ）+ CLAUDE.md の委譲ルール（指示文に「docs/ は触らない」を含める）で防ぐ
- 週次補充は最初から G1〜G3 通しで Codex に任せ、Aurora 到達（サンドボックスのネットワーク設定）まで込みで試す
- `umigame-problem-writer` は当面対象外
- Codex 側の枠は ChatGPT サブスクの利用枠（Claude のトークンを Codex の枠へ付け替える）

## 前提条件・再検討トリガー

- （解消）Codex のスキル探索パス: リポジトリの `.agents/skills/` を拾う（2026-09-20 に `codex exec --sandbox read-only` で Remotion スキル 6 本の列挙を確認。明示起動は `$<skill-name>`）
- （解消）スキル本文の Claude 依存の棚卸し: `/goal`（quiz-stock-replenish の G1〜G3・step の前提）、「Codex に委譲」の記述（quiz のリサーチ・imagegen）、スラッシュ参照と主語「Claude」の 3 種類のみ
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

## 転記下書き（開発計画 Phase 23 へ。4 項目様式・5.1 チェックリスト通過済み）

**Phase 23: Codex 直接セッションの導入（スキルの両エージェント共用 + AGENTS.md の線引き）**
狙い: Claude Code のトークン節約。常に並行可のレーン（アイデア・課題・セット）の定型作業を Codex 直接セッションで回す。開発レーン。23-1 は `docs/plans/index.html` を触るためフリーズ窓で単独実施。
課題表: I-030（`docs/plans/index.html` セクション 2・CLAUDE.md 並行作業ルール）が対象パスで該当。本フェーズは開発レーンの 1 セッション制約を変えない（Codex 直接セッションを開発レーン禁止と明記する側）ため据え置き継続・トリガー更新なし。I-035 は解消済みで対象外。

**23-1 器の整備（スキル実体の集約 + AGENTS.md / CLAUDE.md / レーン規則）**
- 内容: `.claude/skills/` 直下の実体 8 本（docs-mobile-view / idea / incident / issue / quiz-stock-replenish / ranking-stock-replenish / step / umigame-problem-writer）を `git mv` で `.agents/skills/` へ移し、`.claude/skills/<name>` を相対シンボリックリンクに置換。`AGENTS.md` を書き換え（直接セッションの許可レーン = アイデア / 課題 / セット、開発レーン禁止、許可パス / 禁止パスの列挙、docs 書き込みは「スキル起動時 or 指示文で明示」の条件付き、スキルは `$<name>` で起動、Git 運用ルールは CLAUDE.md 参照、MCP ワーカー時の「commit は指示された場合のみ」は維持）。`CLAUDE.md` の Codex 連携節に「委譲指示文に『docs/ は触らない』を含める」と直接セッション運用の参照を追記。`docs/plans/index.html` セクション 2 に「Codex 直接セッションは並行可レーンのみ」の 1 行。触るパス: `.claude/skills/` `.agents/skills/` `AGENTS.md` `CLAUDE.md` `docs/plans/index.html`
- 完了条件: `git ls-files -s .claude/skills | grep -c ^120000` = 14（既存 6 + 8）・`.agents/skills/` に実体 14 本（出力を貼る）。Claude Code から `/idea` が起動できる（本セッションで Skill 起動して手順の先頭が返ることを貼る）。`codex exec --sandbox read-only` にスキル列挙をさせ、8 本が `.agents/skills/` のパスで出る（出力を貼る）。`step` の `disable-model-invocation` が Codex の列挙を壊していないこと（同出力）。`docs/plans/index.html` のタグ対応の機械チェック
- 人間ゲート: AGENTS.md の許可 / 禁止パスと条件文のレビュー
- 停止点・上限: push まで。stop after 20 turns

**23-2 スキル 3 本の中立化（23-1 完了後）**
- 内容: `idea`・`issue`・`quiz-stock-replenish` の SKILL.md を両エージェント対応に書き換え（主語「Claude」→「エージェント」、`/idea` `/issue` の参照は「スキル idea を起動（Claude Code は `/idea`、Codex は `$idea`）」形式、末尾に「エージェント別の差分」節: Claude = `/goal` 起動 / Codex = 同じ完了条件文を `update_plan` に立て証跡を貼る・リサーチは `--search` と curl で自分で行う・イラストは組み込み imagegen で自分で生成）。残り 5 本の冒頭に「Claude Code 専用（Codex は起動しない）」を 1 行。`quiz-stock-replenish` には Codex 直接セッションでの Aurora 到達に必要な `~/.codex/config.toml` のプロジェクト設定例（`sandbox_workspace_write.network_access = true` 等）を記載。触るパス: `.agents/skills/{idea,issue,quiz-stock-replenish,docs-mobile-view,incident,ranking-stock-replenish,step,umigame-problem-writer}/SKILL.md`
- 完了条件: 3 本の SKILL.md に無条件の `/goal` 記述・「Codex に委譲」の記述が残っていないことを `grep -n` で示す（差分節内の記述のみ許容）。`codex exec --sandbox read-only "$quiz-stock-replenish の工程を見出しだけ列挙して"` で工程が読めることを貼る。残り 5 本の先頭 5 行に注記があることを `head` で示す
- 人間ゲート: 3 本の差分節のレビュー + ユーザーが `~/.codex/config.toml` に設定例を反映（リポジトリ外のローカル設定）
- 停止点・上限: push まで。stop after 20 turns

**23-3 Codex 直接セッションでの試行（ユーザー判断・ゴール対象外）**
- 内容: ユーザーが `codex` を起動し、`$idea` で壁打ち 1 回・`$issue` で棚卸し 1 回・logic-training-1 の週次補充 1 バッチを G1〜G3 通しで実施する。結果の判定は下の確認待ち項目
- 停止点: —（ゴールにしない）

**確認待ち項目（5.2）**
- 開発計画へ: トリガー = 節目型「Codex 直接セッションで `$idea`・`$issue` を各 1 回使い終えた後（目安 2026-10-04 まで）」。確認内容 = 終了規律（表更新・コミット・push）まで完走したか、許可パス外に触っていないか（`git show --stat` の出力）。NG 時 = AGENTS.md / 差分節を直すステップを起票、または課題起票
- logic-training-1 セット計画書へ: トリガー = セット型「logic-training-1 の次の週次補充を Codex 直接セッションで行った回（2026-09-w4 以降の最初の回）」。確認内容 = G1〜G3 が完走したか（Aurora 適用の更新行数 = 承認件数・unbuilt=0 の出力）、差し戻し率（人間レビューの却下数 / 提出数）を 2026-09-w3 の Claude 実績と比較。NG 時 = 課題起票（線引き / スキル差分節 / 執筆勘所の不足）

**Phase 完了時の付随作業**: CLAUDE.md の開発計画パラグラフ更新・メモリ（Codex への制約 3 点）の書き換え・本 MD の disposition にフェーズへのリンク
