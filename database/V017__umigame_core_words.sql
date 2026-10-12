-- V017__umigame_core_words.sql
-- ウミガメのスープ問題の核心語（core_words）を追加
--
-- 適用順序（順序厳守）:
--   1. V017 を Aurora に適用する。
--   2. content/umigame-stock/umigame-soup-1/batch-01/update_core_words.sql を実行する
--      （ストック 14 問の UPDATE + 投稿済み umigame_items の補完）。
--   3. image-batch / sns-post-batch / comment-reply をデプロイする。
--   4. 必要なら content/umigame-stock/umigame-soup-1/tools/write_snapshot.py --rewrite で対象を確認し、
--      --apply を付けて投稿済みのスナップショットを書き直す。
-- NULL は未設定を表す。既存行は V017 適用後、上記 UPDATE で別途埋める。
--
-- 前提: 文字コード utf8mb4 / 照合順序 utf8mb4_unicode_ci。
-- DDL は暗黙コミットされるため、単一トランザクション化は行わない。

-- ============================================================
-- umigame_stock_items（ウミガメストック）
-- ============================================================
ALTER TABLE umigame_stock_items
    ADD COLUMN core_words JSON NULL
        COMMENT '核心語（words と except の文字列配列。返信の出力ガードとプローブの漏れ検査に使う）'
        AFTER judge_criteria;

-- ============================================================
-- umigame_items（ウミガメ出題履歴）
-- ============================================================
-- V017 適用前に作られた行のため NULL 許容。新規出題では image-batch がストック値を転記する。
ALTER TABLE umigame_items
    ADD COLUMN core_words JSON NULL
        COMMENT '核心語のスナップショット（words と except の文字列配列。返信の出力ガードに使う）'
        AFTER judge_criteria;
