---
title: Claude Code から委譲する Codex のモデルを GPT-6 Luna（エフォート MAX）へ更新する
slug: codex-model-gpt6-luna
status: inbox            # inbox | 醸成中 | 再醸成待ち | 待機 | 採用 | 見送り
kind: 単発               # 単発 | 構想
created: 2026-09-23
updated: 2026-09-23
condition: ""            # 再醸成待ち・待機のとき必須（再検討トリガー / 落とし込み条件）
parent: ""               # 構想の子の場合、親の slug
children: []             # 構想の場合、子の slug のリスト
detail: ""               # 詳細 HTML を作ったらファイル名（<slug>.html）
disposition: ""          # クローズ時の昇格先リンク / 見送り理由
---

## 要旨

Claude Code から Codex へ実装を委譲するとき（MCP `codex`）の既定モデルを、現行の `gpt-5.6-terra` / effort `high` から **GPT-6 Luna / effort MAX** に切り替える案。
動機はコスパ: GPT-6 Luna を MAX で回すのが、現時点でいちばん費用対効果がよいらしい。
変更先の候補は `.mcp.json` の起動引数（MCP 委譲の既定）と CLAUDE.md「委譲時のパラメータ・運用」の方針記述。直接実行用の `~/.codex/config.toml` と Windows 側の Codex アプリ設定まで揃えるかは未定。

## 前提条件・再検討トリガー

- GPT-6 Luna の正式なモデル ID と、effort の「MAX」に当たる設定値（`xhigh` なのか、別の値なのか）を確認する
- 「コスパが一番よい」の根拠（単価・品質・速度）を確かめる。現行の使い分け（luna: 機械的な作業 / terra: 既定 / sol: 大型）をどう置き換えるかも決める

## 原文メモ

新しいアイデアです。

Claude Code から Codex を使う際に、Codex 側の呼び出すモデルをアップデートする。

具体的には、GPT-6 Luna（エフォートレベル MAX）を呼び出すようにする。こちらが一番コスパがいいようなので、こちらを呼び出すようにする。

## 壁打ち記録
