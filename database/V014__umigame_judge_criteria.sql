-- V014__umigame_judge_criteria.sql
-- ウミガメのスープ問題の正解基準（judge_criteria）を追加
--
-- 適用順序（順序厳守）:
--   1. V014 を Aurora に適用する。
--   2. 既存 14 問へ content/umigame-stock/umigame-soup-1/batch-01/update_judge_criteria.sql を実行する。
--   3. image-batch / sns-post-batch をデプロイする。
-- NULL は未設定を表す。既存行は V014 適用後、上記 UPDATE で別途埋める。
--
-- 前提: 文字コード utf8mb4 / 照合順序 utf8mb4_unicode_ci。
-- DDL は暗黙コミットされるため、単一トランザクション化は行わない。

-- ============================================================
-- umigame_stock_items（ウミガメストック）
-- ============================================================
ALTER TABLE umigame_stock_items
    ADD COLUMN judge_criteria JSON NULL
        COMMENT '正解基準（コアの要点ごとの当てた / 触れたの境目と誤りの例。④⑤⑥ の判定に使う）'
        AFTER core_points;

-- ============================================================
-- umigame_items（ウミガメ出題履歴）
-- ============================================================
-- V014 適用前に作られた行のため NULL 許容。新規出題では image-batch がストック値を転記する。
ALTER TABLE umigame_items
    ADD COLUMN judge_criteria JSON NULL
        COMMENT '正解基準のスナップショット（コアの要点ごとの当てた / 触れたの境目と誤りの例。④⑤⑥ の判定に使う）'
        AFTER core_points;
