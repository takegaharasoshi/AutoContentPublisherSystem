---
title: LLM の出力を読みやすい日本語にするスキル「読みやす」を導入する
slug: yomiyasu-japanese-writing-skill
status: 再醸成待ち       # inbox | 醸成中 | 再醸成待ち | 待機 | 採用 | 見送り
kind: 単発               # 単発 | 構想
created: 2026-10-11
updated: 2026-10-17
condition: "「読みにくくて困った」具体例が出たとき、または外に出す長文（note 記事・LP・プラットフォーム展開の説明文など）を書く事業の動きが出たときに壁打ちを再開し、その文章を素材に yomiyasu を試して採用 / 見送りを判断する"  # 再醸成待ち・待機のとき必須（再検討トリガー / 落とし込み条件）
parent: ""               # 構想の子の場合、親の slug
children: []             # 構想の場合、子の slug のリスト
detail: ""               # 詳細 HTML を作ったらファイル名（<slug>.html）
disposition: ""          # クローズ時の昇格先リンク / 見送り理由
---

## 要旨

「読みやす」の正体は [nanaism/yomiyasu](https://github.com/nanaism/yomiyasu)（大賀愛一郎氏・MIT・2026-10-17 時点で v2.0.1）。
AI が書いた日本語の比喩・主述のねじれ・装飾・コピー調を、意味を変えず情報を足さずに推敲する Agent Skill で、Python の lint / 差分検査で数値や否定の変化を確かめる。
Claude Code・Codex の両方で動き、`.agents/skills/` 配置にも合う。
ただし対象は `.md` / `.txt` で HTML（設計書・計画書）には使えず、1 本ずつかける重いパイプラインなので「全体の品質の底上げ」には向かない。
現時点で読みにくさの強い痛みはないため、2026-10-17 の壁打ちで**再醸成待ち**に着地した。

## 前提条件・再検討トリガー

- ~~スキルの出典（URL・配布元）と SKILL.md の中身を確認すること~~ → 2026-10-17 に確認済み（壁打ち記録）
- 再検討トリガー: 「読みにくくて困った」具体例が出たとき、または外に出す長文（note 記事・LP・プラットフォーム展開の説明文など）を書く事業の動きが出たときに壁打ちを再開し、その文章を素材に yomiyasu を試して採用 / 見送りを判断する
- 導入する場合の前提: 検査記録 `.yomiyasu/`（原文と最終稿の全文が入る）を `.gitignore` に入れる / 版を固定して取り込むか `npx skills` で追うかを決める / 既存の執筆ルール（WRITING-NOTES・作問スキル）と適用先を重ねない

## 原文メモ

新しいアイデアです。「読みやす」というスキルがあるようです。

このスキルは、LLMが出力する文章について、読みやすい日本語にすることができるようなスキルみたいです。

このスキルをこのプロジェクトで導入することを検討しています。

## 壁打ち記録

### 2026-10-17

- 出典を確認: 正本は nanaism/yomiyasu（v2.0.1・MIT・最終コミット 2026-10-17）。同名の nakatatsu/yomiyasu・Shun5/yomiyasu は別物。中身は SKILL.md 362 行 + references 約 1,200 行（文書の種類別・分野別）+ Python 検査スクリプト約 2 万行（lint / diff / check / 任意の hook）。表記ゆれの統一はしない（他スキルに任せる方針）
- 当プロジェクトとの不整合: ① HTML 非対応（docs の大半に使えない。そのまま使えるのは ideas / issues の MD のみ）② 推敲 1 本ごとに lint → 書き直し → check → diff → verify と重く、会話の報告に毎回かけるのは割に合わない ③ `.yomiyasu/` に全文の記録が残る（gitignore と並行セッションの巻き込みに注意）④ 作者自身が他の校正スキルとの併用で指示が食い違うと明記（WRITING-NOTES・作問スキルの文体ルールと衝突しうる）⑤ 更新が速く版の追い方を決める必要がある
- ユーザーの実感: 読みにくいと強くは感じていない。全体的に品質が上がればよい程度（会話・docs・アイデア / 課題 MD・投稿文言のいずれも弱い関心）
- 判断: 痛みがなく効果の物差しもないため、重い推敲パイプラインは今は入れない → 再醸成待ち（条件は frontmatter の condition）。小さく試す案（スクラッチパッドの clone で 2〜3 本を推敲して差分を見る）は再開時の最初の一手として残す
- 別の筋（未捕捉）: 「全体の底上げ」が目的なら、CLAUDE.md / AGENTS.md に日本語の書き方の規範を数行足す（yomiyasu の slop-catalog から抜き出す）方が全出力に効き軽い。ユーザーが必要なら別アイデアとして捕捉する
- 出典: https://github.com/nanaism/yomiyasu / https://smartscope.blog/en/blog/yomiyasu-installation-guide-ai-japanese-agent-skill-differences-2026/ / https://gist.github.com/yuuichieguchi/de2bcab38daba836e1898939630c344e
