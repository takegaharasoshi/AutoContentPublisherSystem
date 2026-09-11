---
title: 設計書 HTML をレスポンシブ対応にする（スマホ閲覧の常態化）
slug: docs-responsive-mobile
status: inbox
kind: 単発
created: 2026-09-12
updated: 2026-09-12
condition: ""
parent: ""
children: []
detail: ""
disposition: ""
---

## 要旨

スマホから設計書（`docs/` 配下の HTML）を読む機会が増えたため、狭い画面でも読める版面に作り替えたい開発プロセス改善アイデア。

現状の実態:

- 共通スタイル `docs/assets/style.css`（206 行）に**幅のブレークポイント（`@media (max-width: …)`）が 1 つも無い**。`@media` は `prefers-color-scheme`（ダークモード）のみ
- viewport meta は 42 本の HTML 全部に入っているので、スマホで開いても等倍にはならない。横スクロール対策も表（`.table-wrap`）・コード・図には `overflow-x: auto` が入っている
- つまり「全く読めない」ではなく、`container` の `max-width: 60rem` / 余白・フォントサイズ・見出し・表の密度が PC 前提のまま、という段階の問題
- 閲覧経路は既存スキル `docs-mobile-view`（WSL の HTTP サーバー + Windows の `tailscale serve`）で確立済み。本アイデアは「配信」ではなく「版面」の話

触るのは共通 CSS 1 本が中心になる見込みで、影響範囲は設計書体系の全ページ（42 本）。

## 前提条件・再検討トリガー

- 閲覧経路の前提: スキル `docs-mobile-view`（tailnet 内公開）。これ自体の変更は本アイデアのスコープ外
- レーン判定: `docs/assets/style.css` + 各 HTML は設計書体系の共通資産のため、**採用時の実作業は開発レーン**（`docs/plans/index.html` セクション 2 のパス基準で確認する）
- 壁打ちで詰めるべき点（叩き台）: どの画面幅を基準にするか / 表をスマホでどう見せるか（横スクロール継続 or カード化）/ 目次・パンくずの扱い / セット別設計書やインライン SVG 図の扱い / 「全 42 本を触る」か「共通 CSS だけで済ませる」か
- 同系統（開発プロセス改善）のアイデア: [voice-input-tooling](voice-input-tooling.md)（採用済み）、[claude-code-loop-goal-skills](claude-code-loop-goal-skills.md)（採用済み・Phase 19）

## 原文メモ

### 2026-09-12

> 新しいアイデアです。
>
> 最近、スマホで設計書を見たり、このプロジェクトの HTML ファイルを読んだりすることが結構多いので、レスポンシブな感じの設計書にすることを検討しています。

## 壁打ち記録

（未実施）
