-- V013__umigame_judge_points.sql
-- ウミガメのスープ問題の判定要点（core_points）と正解時の開示要約（reveal_text）を追加
--
-- 適用順序（順序厳守）:
--   1. V013 を Aurora に適用する。
--   2. 既存 14 問へ content/umigame-stock/umigame-soup-1/batch-01/update_judge_points.sql を実行する。
--   3. image-batch / sns-post-batch をデプロイする。
-- umigame-soup-1 は is_active=0 のため現状の実害はないが、逆順でデプロイすると image-batch の
-- ストック SELECT が新カラムを参照して失敗する。
-- NULL は未設定を表す。既存行は V013 適用後、上記 UPDATE で別途埋める。
--
-- 前提: 文字コード utf8mb4 / 照合順序 utf8mb4_unicode_ci。
-- DDL は暗黙コミットされるため、単一トランザクション化は行わない。

-- ============================================================
-- umigame_stock_items（ウミガメストック）
-- ============================================================
ALTER TABLE umigame_stock_items
    ADD COLUMN core_points JSON NULL
        COMMENT 'コア（問題文の不思議の真相を説明するのに最低限必要な要点の配列。④正解/⑤惜しいの判定に使う）'
        AFTER fact_sheet,
    ADD COLUMN reveal_text VARCHAR(255) NULL
        COMMENT '正解時に開示する真相の要約（70 字以内）'
        AFTER core_points;

-- ============================================================
-- umigame_items（ウミガメ出題履歴）
-- ============================================================
-- V013 適用前に作られた行のため NULL 許容。新規出題では image-batch がストック値を転記する。
ALTER TABLE umigame_items
    ADD COLUMN core_points JSON NULL
        COMMENT 'コアのスナップショット（問題文の不思議の真相を説明するのに最低限必要な要点の配列）'
        AFTER fact_sheet,
    ADD COLUMN reveal_text VARCHAR(255) NULL
        COMMENT '正解時に開示する真相の要約のスナップショット（70 字以内）'
        AFTER core_points;
