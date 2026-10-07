---
title: Codex 委譲のモデルを GPT-6.1 Sol へ早期に切り替える
slug: codex-model-gpt61-sol
status: 採用             # inbox | 醸成中 | 再醸成待ち | 待機 | 採用 | 見送り
kind: 単発               # 単発 | 構想
created: 2026-10-08
updated: 2026-10-08
condition: ""            # 再醸成待ち・待機のとき必須（再検討トリガー / 落とし込み条件）
parent: ""               # 構想の子の場合、親の slug
children: []             # 構想の場合、子の slug のリスト
detail: ""               # 詳細 HTML を作ったらファイル名（<slug>.html）
disposition: "CLAUDE.md の委譲ルールとメモリのモデル選択方針へ直接反映（Codex CLI 0.161.0 へ更新）"  # クローズ時の昇格先リンク / 見送り理由
---

## 要旨

Codex 委譲で大型・新規性の高い実装に使う上位モデルを、`gpt-6-sol` / `max` から **`gpt-6.1-sol` / `max`** に切り替えた（2026-10-08 採用・反映済み。詰まったら `ultra`）。
GPT-6.1 Sol は 2026-09-29 の DevDay で公開され、単価は旧 6 Sol と同じ（入力 $2・出力 $10 / 100 万トークン）で、DeepSWE v1.1 では Astra 並みのスコアを出す。同じ値段で性能だけ上がるので置き換えに損がない。
既定の `gpt-6-luna` / `max` は据え置く。6.1 の Luna は発表されておらず、既定を 6.1 Sol に寄せると単価が約 20 倍になり、サブスク利用枠の節約という[前回の切替](codex-model-gpt6-luna.md)の目的と食い違うため。ウミガメのコメント判定（Luna）にも影響はない。

## 前提条件・再検討トリガー

- （解消）モデル ID は `gpt-6.1-sol`（effort は low〜ultra）。Codex CLI 0.157.1 の一覧には出ず、0.161.0 で出た
- （解消）反映先は CLAUDE.md「委譲時のパラメータ・運用」とメモリのモデル選択方針。既定は変えないため `config.toml`（WSL・Windows とも）は触らない
- 再検討トリガー: GPT-6.1 Luna（または次の Luna）が出たら、既定の更新を同じ要領で捕捉する

## 原文メモ

新しいアイデアです。OpenAI から GPT 6.1 ソルが使えるようになったとニュースが出ていました。これをこのプロジェクトでもいち早く適用したいです。

諸々 Codex にタスクを現在移譲しているかと思いますが、その際に使うモデルをおそらく今は GPT-6 ソルを使うような設定だと思いますので、これを 6.1 に変更したいです。

## 壁打ち記録

### 2026-10-08

- **事実確認**: GPT-6.1 Sol は 2026-09-29 公開（DevDay）。Codex は Plus 以上で利用可・API ID `gpt-6.1-sol`。単価 $2 / $10 は旧 6 Sol と同じで、6 Luna（$0.10 / $0.50）の約 20 倍。DeepSWE v1.1 で Astra 並み・旧 Sol より低いエフォートで +6.4pt。6.1 Luna・6.1 Astra は出ていない（Astra は安全性の懸念で見送り）。出典: [OpenAI](https://openai.com/index/introducing-gpt-6-1-sol/)・[TechCrunch](https://techcrunch.com/2026/09/29/openai-launches-gpt-6-1-sol-says-it-nearly-matches-gpt-6-astra-and-costs-less/)・[Unite.AI](https://www.unite.ai/openai-unveils-gpt-6-1-sol-at-devday-with-new-codex-and-chatgpt-tools/)・[eesel（Luna 単価）](https://www.eesel.ai/blog/gpt-6-luna-pricing)
- **前提の訂正**: 原文メモの「今は GPT-6 Sol を使っている」は誤りで、既定は Luna max（Sol は大型タスクのみ）。論点は「既定を 6.1 Sol に寄せるか」と「上位モデルの置き換え」に分かれた
- **判断（ユーザー了承）**: 既定は Luna max のまま。上位モデルだけ `gpt-6.1-sol` へ置き換える
- **反映**: Codex CLI を 0.157.1 → 0.161.0 へ更新（`codex update`）。`codex exec -m gpt-6.1-sol` の疎通を確認し、モデル一覧に `gpt-6.1-sol` が出ることも確認した。CLAUDE.md の委譲ルールとメモリのモデル選択方針を更新。development-plan 内の `gpt-6-sol` の記述は実施記録なので書き換えない
- **積み残し**: Windows の Codex アプリ（直接セッション）は既定モデルの設定を変えないため対応不要。アプリ自体の更新は任意
