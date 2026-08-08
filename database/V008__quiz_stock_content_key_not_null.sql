-- V008__quiz_stock_content_key_not_null.sql
-- AutoContentPublisherSystem 問題ストック業務キー（content_key）の NOT NULL 化
--
-- 前提: V007 適用後、既存全行に content_key がバックフィル済みであること
-- （content/quiz-stock/logic-training-1/2026-08-initial/backfill_content_key.sql）。
-- NOT NULL 化により、content_key を省いた投入は ERROR 1364 で失敗する
-- （採番漏れが静かに進行しない = 週次補充の投入時に必ず気づける）。
--
-- 前提: 文字コード utf8mb4 / 照合順序 utf8mb4_unicode_ci。
-- DDL は暗黙コミットされるため、単一トランザクション化は行わない。

-- ============================================================
-- quiz_stock_items（content_key の NOT NULL 化）
-- ============================================================
ALTER TABLE quiz_stock_items
    MODIFY COLUMN content_key VARCHAR(64) NOT NULL COMMENT '環境非依存の業務キー（{slot_code}-{3 桁連番}。例: morning-001。セット内一意）。事前動画の S3 キーの構成要素。投入時に採番し、ローカル MySQL と Aurora へ同じ値を入れる（id は環境ごとの AUTO_INCREMENT で一致しないため）';
