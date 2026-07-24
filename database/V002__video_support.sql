-- V002__video_support.sql
-- AutoContentPublisherSystem 動画投稿対応（生成メディア・音源ストック）
--
-- 設計の詳細（ER図、各カラムの意図、S3キー設計、時刻の取り扱い、マイグレーション方針）は
-- docs/app/data-model.html のセクション 4.5 / 4.6 / 4.8 / 5 / 8 を参照。DDL のバージョン管理は
-- Flyway 風の命名規則（V<連番>__<説明>.sql）に従う。
--
-- 稼働中 DB への適用順序: (1) EventBridge Scheduler を停止し、実行中タスクの完了を確認する。
-- (2) 本DDLを適用する。(3) 新テーブル名を参照するアプリケーションをデプロイする。(4) Scheduler
-- を再開する。本DDL適用後は generated_images / post_images を参照する旧アプリケーションを
-- 実行してはならない。
--
-- 前提: 文字コード utf8mb4 / 照合順序 utf8mb4_unicode_ci。
-- 全 DATETIME カラムは UTC で保存する（アプリケーション側で変換してから格納する）。
-- DDL は暗黙コミットされるため、単一トランザクション化は行わない。

-- ============================================================
-- audio_assets（音源ストック）
-- ============================================================
CREATE TABLE audio_assets (
    id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '主キー',
    set_id BIGINT UNSIGNED NOT NULL COMMENT 'バッチセット ID（FK）。音源はセット専属',
    s3_key VARCHAR(500) NOT NULL COMMENT '前処理済み完成音源の S3 キー（audio/{set_code}/...m4a）',
    title VARCHAR(200) NOT NULL COMMENT '曲名・管理用表示名',
    source_url VARCHAR(500) NOT NULL COMMENT '出典 URL・ライセンス証跡',
    license_type VARCHAR(50) NOT NULL COMMENT 'ライセンス種別（CC0 / Pixabay License 等）',
    license_note TEXT NULL COMMENT 'クレジット要件・利用条件の補足',
    acquired_at DATETIME NOT NULL COMMENT '取得日・ライセンス証跡（UTC）',
    duration_seconds INT UNSIGNED NULL COMMENT '前処理済み音源の尺（秒）。参考情報',
    is_active TINYINT(1) NOT NULL DEFAULT 1 COMMENT '有効フラグ。ミュート検知時の無効化・差し替え用',
    last_used_at DATETIME NULL COMMENT '最後に生成へ使用した日時（UTC）。順繰り選曲のローテーション状態',
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '作成日時（UTC）',
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新日時（UTC）',
    PRIMARY KEY (id),
    KEY idx_audio_assets_set_active (set_id, is_active) COMMENT '選曲クエリ WHERE set_id=? AND is_active=1 ORDER BY last_used_at,id 用',
    UNIQUE KEY uq_audio_assets_set_id (set_id, id) COMMENT '複合 FK の参照先として使用',
    CONSTRAINT fk_audio_assets_set FOREIGN KEY (set_id) REFERENCES batch_sets (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
COMMENT='セット配下の音源ストック（リール用 BGM。前処理済み完成音源・ライセンス証跡・ローテーション状態を管理）';

-- ============================================================
-- generated_media（旧 generated_images）
-- ============================================================
RENAME TABLE generated_images TO generated_media;

ALTER TABLE generated_media
    RENAME INDEX uq_generated_images_idempotency TO uq_generated_media_idempotency,
    RENAME INDEX idx_generated_images_set_run TO idx_generated_media_set_run,
    RENAME INDEX idx_generated_images_set_prompt TO idx_generated_media_set_prompt,
    DROP FOREIGN KEY fk_generated_images_set,
    DROP FOREIGN KEY fk_generated_images_generation_run,
    DROP FOREIGN KEY fk_generated_images_prompt_config,
    ADD COLUMN duration_seconds INT UNSIGNED NULL COMMENT '動画の尺（秒）。画像は NULL' AFTER height,
    ADD COLUMN audio_asset_id BIGINT UNSIGNED NULL COMMENT '合成音源 ID（audio_assets への複合 FK。画像／音源なしは NULL）' AFTER duration_seconds,
    ADD KEY idx_generated_media_set_audio (set_id, audio_asset_id),
    ADD CONSTRAINT fk_generated_media_set FOREIGN KEY (set_id) REFERENCES batch_sets (id),
    ADD CONSTRAINT fk_generated_media_generation_run FOREIGN KEY (set_id, generation_run_id) REFERENCES generation_runs (set_id, id),
    ADD CONSTRAINT fk_generated_media_prompt_config FOREIGN KEY (set_id, prompt_config_id) REFERENCES prompt_configs (set_id, id),
    ADD CONSTRAINT fk_generated_media_audio_asset FOREIGN KEY (set_id, audio_asset_id) REFERENCES audio_assets (set_id, id);

-- リネームで引き継いだ旧名参照のテーブル COMMENT を新名に更新する
ALTER TABLE generated_media
    COMMENT='生成メディアのメタ情報（画像・動画）。generation_runs の子（1 実行 : N メディア）。投稿ステータスは持たない（posts / post_media から導出）';

-- ============================================================
-- posts（メディア種別）
-- ============================================================
ALTER TABLE posts
    ADD COLUMN media_type ENUM('feed_image','reel') NOT NULL DEFAULT 'feed_image' COMMENT 'メディア種別（投稿 API 分岐用）。先頭メディアの file_format から導出' AFTER status;

-- ============================================================
-- post_media（旧 post_images）
-- ============================================================
RENAME TABLE post_images TO post_media;

ALTER TABLE post_media
    DROP FOREIGN KEY fk_post_images_post,
    DROP FOREIGN KEY fk_post_images_generated_image;

ALTER TABLE post_media
    CHANGE COLUMN generated_image_id generated_media_id BIGINT UNSIGNED NOT NULL COMMENT '生成メディア ID（FK）',
    RENAME INDEX uq_post_images_post_image TO uq_post_media_post_media,
    RENAME INDEX uq_post_images_post_order TO uq_post_media_post_order,
    RENAME INDEX idx_post_images_generated_image TO idx_post_media_generated_media,
    ADD CONSTRAINT fk_post_media_post FOREIGN KEY (post_id) REFERENCES posts (id),
    ADD CONSTRAINT fk_post_media_generated_media FOREIGN KEY (generated_media_id) REFERENCES generated_media (id);

-- リネームで引き継いだ旧名参照のテーブル COMMENT を新名に更新する
ALTER TABLE post_media
    COMMENT='投稿に載せるメディアの選択と表示順（1 投稿 : N メディア。当面の運用は 1 投稿 1 メディア）。generated_media_id が post の generation_run に属することはアプリ層で保証する（DB では強制しない）';
