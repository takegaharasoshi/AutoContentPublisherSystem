---
title: ウミガメのスープのコメント判定に OpenAI の Decisions API（Jev 相当）を候補として加える
slug: umigame-reply-openai-decisions
status: 採用             # inbox | 醸成中 | 再醸成待ち | 待機 | 採用 | 見送り
kind: 単発               # 単発 | 構想
created: 2026-10-03
updated: 2026-10-08
condition: "(a) Jev に問題が出たとき（値上げ・提供停止・MCA / Acceptable Use Policy の変更）、または (b) Decisions API が一般公開され、公開ドキュメントで料金と確率を返すかが分かったとき、壁打ちを再開する。再開時は「Jev が使えなくなった場合の代わり」として、luna と同じモデルである弱みと天秤にかける"  # 再醸成待ち・待機のとき必須（再検討トリガー / 落とし込み条件）
parent: ""               # 構想の子の場合、親の slug
children: []             # 構想の場合、子の slug のリスト
detail: ""               # 詳細 HTML を作ったらファイル名（<slug>.html）
disposition: "開発計画 21-6d10a・21-6d10b（パターン ⑥ Decisions + luna）として採用。21-6d11 の全件プローブで評価し、21-6e で方式選定"  # クローズ時の昇格先リンク / 見送り理由
---

## 要旨

OpenAI の Decisions API（2026-09-29 発表・GPT-6 Luna 上で動く判定専用 API・限定プレビュー）を、umigame-soup-1 のコメント判定に取り入れるかを検討した。**結論は再醸成待ち**（2026-10-03）。
21-6b の暫定方針で Jev は「見張り役」と「真相を開示する前の二重確認」を担い（21-6c2 で `hybrid` モードとして実装済み）、Decisions API が代わりうるのはこの役割。ただしこの役割は **luna とは別のモデルの意見であることが前提**で、中身が同じ GPT-6 Luna の Decisions API では luna の劣化・読み違いと誤りが連動しやすく、誤った開示を止められない。
加えて、限定プレビューのため呼び出せず、料金・確率を返すかも未公開で設計もできない。評価データ（21-6d2）は方式に依存しないので、使えるようになってから 21-6d3 のプローブ実行器にパターンを足せば手戻りは出ない。
再開時に検討する役割は「Jev が使えなくなった場合の代わり」（OpenAI キーの流用・契約先が減る・SLA のない Jev より安定、という利点と、独立性の喪失を天秤にかける）。
**2026-10-07 に採用**: 一般公開を受け、⑤ jev + 2c-luna と同じ形のパターン ⑥（判定 = Decisions・返信文 = 2c-luna）を評価に加える（ユーザー決定）。開発計画 [21-6d10a](../plans/development-plan.html#step-21-6d10a)（公開ドキュメントの確認と設計）→ [21-6d10b](../plans/development-plan.html#step-21-6d10b)（実装と小試走）→ [21-6d11](../plans/development-plan.html#step-21-6d11)（6 パターンの全件プローブ）。独立性の懸念は 21-6d11 の結果で評価する。

## 前提条件・再検討トリガー

- 再検討トリガー: (a) Jev の値上げ・提供停止・規約（MCA・Acceptable Use Policy）の変更 / (b) Decisions API の一般公開と公開ドキュメント（料金・確率を返すか・選択肢の上限・日本語対応）
- 親の検討: [Jev 案](umigame-yesno-jev.md)（開発計画 21-6a〜g）。Jev の役割の設計は `docs/app/sets/umigame-soup-1.html` 5.1.2

## 原文メモ

新しいアイデアです。

OpenAI から Jevのような API が出たということを聞きました。これを「ウミガメのスープ」のコメント返信の部分に取り入れたいと考えています。

（2026-10-03 壁打ちでの発言）

方針問題ないです

## 壁打ち記録

### 2026-10-03

- 一次調べ: 2026-09-29 の OpenAI DevDay で発表、一部の API 顧客向けの限定プレビュー（一般公開は「数日以内」）。開発者が決めた選択肢から 1 つ選ぶ・判断材料はテキストか画像・約 150 ms・中身は GPT-6 Luna。API リファレンス・料金・確率を返すか・選択肢の上限・日本語対応は未公開（10-02 時点で Docs・changelog・料金ページに記載なし）
  - 出典: https://openai.com/index/devday-2026-recap/ ・ https://modelsystem.one/news/openai-decisions-api-preview/ ・ https://modelsystem.one/runtimes/openai-decisions-api/ ・ https://pasqualepillitteri.it/en/news/19372/openai-decisions-api-jev ・ https://www.valyu.ai/blogs/jev-vs-decisions-api
- 捉え直し: 21-6b の暫定方針（luna が主役・Jev は見張り役と開示前の二重確認）では、Decisions API が代わりうるのは Jev の役割。この役割は別モデルの意見であることが前提で、同じ GPT-6 Luna の Decisions API では誤りが luna と連動しやすい（luna の劣化にも気づけず、誤った開示を止められない）
- 利点（OpenAI キーの流用・契約先が 1 社減る・SLA のない Jev より安定しそう）は、独立性の喪失を上回らない
- 実務面: プレビューに選ばれないと呼べない。21-6d2 は方式に依存しないため、今入れなくても後で 21-6d3 にパターンを足すだけで手戻りはない
- 判断（ユーザー合意）: 再醸成待ち。トリガーは (a) Jev 側の問題 / (b) 一般公開と公開ドキュメント。再開時は「Jev の代わり」として独立性の弱みと天秤にかける

### 2026-10-07

- トリガー (b) の発火: ユーザーから「Decisions API が一般公開された」。公開ドキュメント（料金・確率を返すか・選択肢の上限・日本語対応）の確認は 21-6d10a で行う
- 判断（ユーザー）: ⑤ jev + 2c-luna と同じ形で ⑥ Decisions + luna も試す。採用し、開発計画 21-6d10a・21-6d10b・21-6d11 に展開した。luna と同じモデルである点（独立性）は、全件プローブの結果（誤りが luna と連動するか）で評価する

### 2026-10-08（開発計画 21-6d10a）

- 公開ドキュメントで確認（2026-10-06 にパブリックベータ・GA は数週間以内の見込み）: 料金は入力 100 万トークンあたり $0.10（出力・キャッシュは無料）、`predicate` は確率・`choice` は選択肢ごとの確率 + `confidence` を返す、1 リクエストに独立した問いを複数入れられる、学習に使わない・不正利用監視 30 日・ZDR 対象。問いの数・選択肢の数の上限、対応言語、応答時間の数値は記載なし（第三者記事の数値は未確認扱い）
  - 出典: https://developers.openai.com/api/docs/guides/decisions ・ https://developers.openai.com/api/reference/resources/decisions/methods/create ・ https://developers.openai.com/api/docs/guides/your-data ・ https://community.openai.com/t/decisions-api-is-now-available-in-public-beta/1403877
- 2026-10-03 の「料金・確率を返すかが分からず設計できない」は解消した。Jev の段・入力・リクエストの分け方をそのままにし、API の呼び方だけを差し替える形で設計した（当初のリクエストをまとめる案は、⑤ との比較が濁るためユーザー合意で取りやめ）（`docs/app/sets/umigame-soup-1.html` 10.3.6）。独立性がない点は設計書に警告として明記し、21-6d11 で luna と誤りが重なるかを見て評価する
- 費用見積もり: 21-6d10b + 21-6d11 で約 $0.45（上限 $3）。Jev と違い契約先が増えない（OpenAI キーを流用）
- 料金・規約と設計の承認待ち（ユーザー）。疎通確認はユーザーがキーを入れてスクリプトを実行する
