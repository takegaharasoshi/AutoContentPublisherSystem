# batch-01 第 1 バッチ: 進行状況（引き継ぎメモ）

最終更新: 2026-09-12。**21-4a-3 ① 完了（U02〜U10 の削除と連番整理）**。21-4a 初稿の 9 問（U02〜U10）を `stock_items.py` と `leak_count.py` の核心語辞書から削除し（2026-09-12 の方針再変更〔ユーザー決定〕。git 履歴で復元可）、通過済み 5 問（U01・U11〜U14）の content_key を 001〜005 に振り直した（no は管理 ID として不変・再利用しない。プローブキャッシュは no キーのため保持）。`research.md` は工程 7 の照合台帳として残置、`master_prompt.txt` は変更なし。**次は 21-4a-3 ②: スキルで U15〜U19（content_key 006〜010）を 1 問 1 /goal で作問**。
計画は `docs/plans/development-plan.html` 21-4a-3、記録は `development-log.html`。仕様の正はセット別設計書セクション 4、作問手順の正はスキル `umigame-problem-writer`。

## 現在のストック（5 問。全問スキル作問・人間ゲート通過済み）

- U01 `001-faint-shadow` 影が薄いと言われて喜ぶ男（misdirection / 難易度 4）
- U11 `002-mirror-letters` 鏡文字で早く着く男たち（misdirection / 難易度 4）
- U12 `003-silent-musicians` 階段に並ぶ、音を出さない男たち（misdirection / 難易度 2）
- U13 `004-fifty-year-letter` 50 年前の男の子から届いた手紙（misdirection / 難易度 4）
- U14 `005-bakers-egg` 店でいちばんのパンを焼く卵（misdirection / 難易度 4）

機械検査（21-4a-3 ① 時点）: validate 全 5 問 OK（警告 0）・leak_count 98 想定質問で核心語漏れ 0・冒頭語不一致 0・dry-run 5 件 OK。

## 21-4a-3 ② への申し送り（作問の勘所。詳細は SKILL.md と開発記録の各巡）

- **型・難易度の偏り**: 現 5 問は misdirection 5 / story 0、難易度 4 が 4 問・2 が 1 問。設計上の目安（story と misdirection を混ぜる）に対し story が 0 のため、**U15〜U19 の語選び（工程 1）で story 型を意識的に狙う**。既定難易度は 4（A 型手がかり 0 個・消去法動線。9 巡目のユーザー指示）
- **確定事実シートは周辺事実だけにする**（核心の定義文を書くと出題者が補足に引用して漏れる。U01 で確立、新作は最初からこの書き方で組む）
- 出題者プロンプトは「補足は原則付けない」に振り切り済み（`master_prompt.txt`・設計書 5.1 の決定）。プローブは probe_test.py（`--only` で 1 問分）→ leak_count.py で補足漏れを計測
- U01 は「肺に影」という言い回しを知らない若い層には難しめ。動線は「同じ相手・〜ましたね → 医者 → 写真 → 病気」で確保。「病気」を扱うが快復して喜ぶ結末で、誰も死なない（レビュー済みの残し書き）

## 21-4a-2 の経緯（完了。2026-09-07〜09-12・人間ゲート 10 巡）

- 21-4a の人間ゲートで U01 が 2 回落ちた（着想元が他者の自作問題 → コアのない知識クイズ）ことを受け、作問スキル `.claude/skills/umigame-problem-writer/` を先に作り、その手順で 1 問ずつ作問 → チャットレビューの反復に切り替えた
- 10 巡の反復で U01・U11・U12・U13・U14 の 5 問が通過。指摘は「問題の修正」「スキルの修正」に分け、スキル修正（工程 4.5 手がかりの棚卸し / コア検査〔誤読の強制・落差〕/ 既定難易度 4 / 失敗パターン「売り文句・宣伝への反転」「不可能文で誤読が自壊」等）はそのつど SKILL.md へ反映済み。各巡の詳細は開発記録 21-4a-2
- 2026-09-12 に作問方針を再変更（ユーザー決定）: 21-4a 初稿の 9 問（U02〜U10）は採否検査をせず削除し、スキル作問のみで全 10 問にする（21-4a-3 ① で実施済み）

## 成果物

- `database/V012__umigame_stock.sql`: ローカル MySQL（acps-mysql）へ適用済み（`umigame_stock_items` 25 カラム・`umigame_items`・`batch_sets.problem_snapshot_enabled`）。Aurora への適用は全問そろった後の人間ゲート
- `../master_prompt.txt`: 出題者プロンプトの正（21-3 案をプローブテストで 3 行補強 + 「補足は原則付けない」。セット別設計書 5.1 に反映済み）
- `stock_items.py` 5 問（上記）+ ツーリング（`validate.py` / `probe_test.py` / `leak_count.py` / `generate.py`）+ `../common/umigame_common.py`
- `research.md`: 着想の照合台帳（Codex `--search exec`・30 件。スキル工程 7 の既存問題照合に使う）

## 工程

- [x] DDL V012（ローカル適用）
- [x] ツーリング（validate / probe_test / generate）+ 共通モジュール + master_prompt.txt
- [x] リサーチ（Codex `--search exec`・30 件）→ `research.md`
- [x] 21-4a: 初稿 10 問執筆 → 機械検査（→ 2026-09-12 の方針再変更で U02〜U10 は削除）
- [x] 21-4a-2: 作問スキル新設 + `core` 管理項目 + 人間ゲート 10 巡で U01・U11〜U14 の 5 問通過（2026-09-12 完了）
- [x] 21-4a-3 ①: U02〜U10 を stock_items.py・leak_count.py から削除し、通過済み 5 問の content_key を 001〜005 に振り直し（no は不変）→ validate・dry-run・STATUS 整理（2026-09-12）
- [ ] 21-4a-3 ②: スキルで U15〜U19（content_key 006〜010）を 1 問 1 /goal で作問・人間ゲート反復（スキルのブラッシュアップ継続）
- [ ] 21-4a-3 ③: 10 問で validate → 全問プローブ（review.html）→ dry-run の全体検査
- [ ] Aurora へ V012 適用（ユーザー）→ 21-4b（投入）
