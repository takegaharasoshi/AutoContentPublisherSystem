---
title: Claude Code から委譲する Codex のモデルを GPT-6 Luna（エフォート MAX）へ更新する
slug: codex-model-gpt6-luna
status: 採用             # inbox | 醸成中 | 再醸成待ち | 待機 | 採用 | 見送り
kind: 単発               # 単発 | 構想
created: 2026-09-23
updated: 2026-09-26
condition: ""            # 再醸成待ち・待機のとき必須（再検討トリガー / 落とし込み条件）
parent: ""               # 構想の子の場合、親の slug
children: []             # 構想の場合、子の slug のリスト
detail: ""               # 詳細 HTML を作ったらファイル名（<slug>.html）
disposition: "CLAUDE.md・.mcp.json・~/.codex/config.toml へ直接反映 + 開発計画 21-6b（ウミガメ判定のモデル）へ転記"  # クローズ時の昇格先リンク / 見送り理由
---

## 要旨

Claude Code から Codex へ委譲するときの既定モデルを、`gpt-5.6-terra` / `high` から **`gpt-6-luna` / effort `max`** に切り替えた（2026-09-26 採用・反映済み）。
根拠は OpenAI が公開した DeepSWE v1.1 のグラフで、Luna max が Sol の中間エフォート並みのスコア（約 67%）をタスクあたり数分の 1 のコストで出すこと。API 単価が安いモデルほどサブスクの利用枠の減りも少ないので、同じ枠でより多く委譲できる。
大型・新規性の高い実装だけ `gpt-6-sol` / `max` 以上（詰まったら `ultra`）に上げる。派生で、ウミガメのコメント判定（パターン 1）も `gpt-6-luna` / `max` に確定した。

## 前提条件・再検討トリガー

- （解消）モデル ID は `gpt-6-luna`、effort は `max`（`xhigh` の上。Luna の上限。Sol / Astra はさらに `ultra` あり）。Codex CLI 0.144.1 では一覧に出ず、0.157.1 で出た
- （解消）根拠は DeepSWE v1.1 のグラフ（下記）。使い分けは「既定 = Luna max・横展開も Luna max・大型 = Sol max 以上」

## 原文メモ

新しいアイデアです。

Claude Code から Codex を使う際に、Codex 側の呼び出すモデルをアップデートする。

具体的には、GPT-6 Luna（エフォートレベル MAX）を呼び出すようにする。こちらが一番コスパがいいようなので、こちらを呼び出すようにする。

## 壁打ち記録

### 2026-09-26 壁打ち 1 回目（採用）

- **事実確認**: GPT-6 Sol / Luna は 2026-09-22 リリース（序列 Astra > Sol > Luna。Terra 相当はない。API 単価は 5.6 系の半分で Luna は入力 $0.10・出力 $0.50 / 100 万トークン）。Codex CLI を 0.144.1 → 0.157.1 に上げるとモデル一覧に `gpt-6-*` が出て、`codex exec -m gpt-6-luna -c model_reasoning_effort=max` で応答を確認した。出典: [OpenAI](https://openai.com/index/introducing-gpt-6-sol-and-luna/)・[TechCrunch](https://techcrunch.com/2026/09/22/openai-launches-gpt-6-sol-and-luna/)・[Artificial Analysis](https://artificialanalysis.ai/models/releases/gpt-6-luna)・ユーザー提示の @OpenAIDevs 投稿（DeepSWE v1.1 のコスト × スコア図）
- **論点と判断**: Claude は当初「Luna は定型作業向け（OpenAI の位置づけ・AA の知能指数 37 < 5.6 Terra 42）で、委譲の主力（新モジュール・複数ファイルの実装）には荷が重い」「サブスク運用なので API 単価は効かない」と懸念した。ユーザーは DeepSWE で Luna max ≈ Sol 中間エフォートのスコアを数分の 1 のコストで出すこと、単価が安ければ利用枠の消費も少ないことを示し、Claude も同意 → 既定を Luna max に。上限の差（Luna は 67% 付近で頭打ち、Sol 上位・Astra は 70〜74%）は、大型を Sol max 以上に上げることで吸収する
- **範囲**: `.mcp.json` と WSL の `~/.codex/config.toml`（Claude の直接実行用）を変更。Windows の Codex アプリ（直接セッション）は変えない（ユーザー判断）。横展開もエフォートは下げず max
- **派生（ユーザー判断で確定）**: ウミガメのコメント判定のパターン 1 を `gpt-6-luna` / `max` にし、開発計画 21-6b・セット設計書・方式設計書へ転記。本番の API 従量課金なので単価半減がそのまま効く。effort max は推論トークンが増えるため、`max_completion_tokens` 400 と応答時間を 21-6b の試走で測り直す
- **訂正の記録**: logic-training-1 の実行時 LLM 生成（15-5・`gpt-5.6-terra`）は 16-1 で休止済みで、現在本番が OpenAI API を呼ぶ箇所はない
- **課題表**: 該当なし（CLAUDE.md を対象パスに持つ I-030 は並行作業ルールの課題で無関係）
- **積み残し（確認待ち）**: 切替後の委譲 2〜3 回で、差し戻し回数と利用枠の減り方を見る。手戻りが目立てば既定を Sol に戻すか検討する
