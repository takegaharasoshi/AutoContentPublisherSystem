---
title: Codex 委譲のモデルを GPT-6.1 Sol へ早期に切り替える
slug: codex-model-gpt61-sol
status: inbox            # inbox | 醸成中 | 再醸成待ち | 待機 | 採用 | 見送り
kind: 単発               # 単発 | 構想
created: 2026-10-08
updated: 2026-10-08
condition: ""            # 再醸成待ち・待機のとき必須（再検討トリガー / 落とし込み条件）
parent: ""               # 構想の子の場合、親の slug
children: []             # 構想の場合、子の slug のリスト
detail: ""               # 詳細 HTML を作ったらファイル名（<slug>.html）
disposition: ""          # クローズ時の昇格先リンク / 見送り理由
---

## 要旨

OpenAI から GPT-6.1 Sol が出たというニュースを受けて、Codex 委譲で使うモデルをいち早く 6.1 系に切り替えたい。
現状（[codex-model-gpt6-luna](codex-model-gpt6-luna.md) で 2026-09-26 採用）は**既定 = `gpt-6-luna` / `max`**、大型・新規性の高い実装だけ `gpt-6-sol` / `max` 以上。したがって「Sol → 6.1 Sol」の置き換えだけなら大型タスクの上げ先が変わるだけで、既定の Luna は 6.1 に Luna 版があるか・既定を Sol 6.1 に寄せるかが別の論点になる。
壁打ちで確かめること: 6.1 のモデル ID と提供範囲（Luna / Astra の 6.1 はあるか）・必要な Codex CLI のバージョン・ベンチマークとサブスク枠の消費・ウミガメ判定（パターン ⑥ = luna）への波及。

## 前提条件・再検討トリガー

- 6.1 の正式なモデル ID と、Codex CLI で選べるようになる最低バージョンを確認する（6 Luna のときは 0.157.1 が必要だった）
- 反映先の候補: CLAUDE.md「委譲時のパラメータ・運用」・`~/.codex/config.toml`（WSL）・Windows 側 `%USERPROFILE%\.codex\config.toml`（Codex 直接セッション）・メモリのモデル選択方針

## 原文メモ

新しいアイデアです。OpenAI から GPT 6.1 ソルが使えるようになったとニュースが出ていました。これをこのプロジェクトでもいち早く適用したいです。

諸々 Codex にタスクを現在移譲しているかと思いますが、その際に使うモデルをおそらく今は GPT-6 ソルを使うような設定だと思いますので、これを 6.1 に変更したいです。

## 壁打ち記録
