-- V006__prebuilt_video.sql
-- AutoContentPublisherSystem 事前ビルド済みクイズ動画対応
-- （quiz_stock_items への事前動画マスター・ビルド時 BGM・ビルド日時の追加）
--
-- 設計の詳細（各カラムの意図、事前ビルド運用、S3 キー規約）は
-- docs/app/data-model.html のセクション 4.10 / 5 と
-- docs/app/generators/quiz-prebuilt.html のセクション 4〜8 を参照。DDL の
-- バージョン管理は Flyway 風の命名規則（V<連番>__<説明>.sql）に従う。
--
-- 稼働中 DB への適用順序: 全変更は NULL 可カラム・インデックス・FK の追加であり、
-- 既存アプリとの互換性を保つ。事前動画の S3 配置と 3 カラム同時更新は
-- content/video-build/<set_code>/ の publish.py で行う。
--
-- 前提: 文字コード utf8mb4 / 照合順序 utf8mb4_unicode_ci。
-- 全 DATETIME カラムは UTC で保存する（アプリケーション側で変換してから格納する）。
-- DDL は暗黙コミットされるため、単一トランザクション化は行わない。

-- ============================================================
-- quiz_stock_items（事前ビルド済み動画の紐づけ）
-- ============================================================
ALTER TABLE quiz_stock_items
    ADD COLUMN video_s3_key VARCHAR(512) NULL COMMENT '事前動画マスターの S3 キー（assets/{set_code}/prebuilt/{stock_item_id}.mp4）。NULL=未ビルトで実行時の出題候補から除外' AFTER last_used_at,
    ADD COLUMN video_audio_asset_id BIGINT UNSIGNED NULL COMMENT 'ビルド時に選曲し動画へベイクした BGM の audio_assets ID（複合 FK でセット境界を保証。実行時に generated_media.audio_asset_id へ転記）' AFTER video_s3_key,
    ADD COLUMN video_built_at DATETIME NULL COMMENT '事前動画のビルド日時（UTC）。版面・仕様改訂時の再ビルド対象を識別する専用日時' AFTER video_audio_asset_id,
    ADD KEY idx_quiz_stock_items_set_video_audio (set_id, video_audio_asset_id) COMMENT '複合 FK (set_id, video_audio_asset_id) 用インデックス',
    ADD CONSTRAINT fk_quiz_stock_items_video_audio FOREIGN KEY (set_id, video_audio_asset_id) REFERENCES audio_assets (set_id, id);
