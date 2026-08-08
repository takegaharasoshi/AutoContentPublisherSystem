-- V007__quiz_stock_content_key.sql
-- AutoContentPublisherSystem 問題ストックの業務キー（content_key）導入
-- （quiz_stock_items への環境非依存キーの追加と事前動画 S3 キー規約の改訂）
--
-- 背景: quiz_stock_items.id は AUTO_INCREMENT の環境ローカルな代理キーであり、
-- ローカル MySQL と Aurora で同じ問題でも値が一致しない（16-3d で確認）。
-- 事前動画の S3 キーが id を埋め込む旧規約（assets/{set_code}/prebuilt/{stock_item_id}.mp4）
-- では S3 のファイル名が環境依存の番号を騙るため、人間可読の安定キー content_key
-- （{slot_code}-{3 桁連番}。例: morning-001）を新設し、S3 キーをこれに揃える。
-- 設計の詳細は docs/app/data-model.html のセクション 4.10 / 5 を参照。
--
-- 適用順序: 本 DDL（NULL 可で追加）→ 既存行のバックフィル
-- （content/quiz-stock/logic-training-1/2026-08-initial/backfill_content_key.sql）
-- → V008（NOT NULL 化）の 3 段で適用する。
--
-- 前提: 文字コード utf8mb4 / 照合順序 utf8mb4_unicode_ci。
-- DDL は暗黙コミットされるため、単一トランザクション化は行わない。

-- ============================================================
-- quiz_stock_items（業務キーの追加・S3 キー規約の改訂）
-- ============================================================
ALTER TABLE quiz_stock_items
    ADD COLUMN content_key VARCHAR(64) NULL COMMENT '環境非依存の業務キー（{slot_code}-{3 桁連番}。例: morning-001。セット内一意）。事前動画の S3 キーの構成要素。投入時に採番し、ローカル MySQL と Aurora へ同じ値を入れる（id は環境ごとの AUTO_INCREMENT で一致しないため）' AFTER difficulty,
    ADD UNIQUE KEY uq_quiz_stock_items_set_content_key (set_id, content_key) COMMENT 'content_key のセット内一意性を保証',
    MODIFY COLUMN video_s3_key VARCHAR(512) NULL COMMENT '事前動画マスターの S3 キー（assets/{set_code}/prebuilt/{content_key}.mp4）。NULL=未ビルトで実行時の出題候補から除外';
