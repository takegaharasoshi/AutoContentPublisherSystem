-- V004__life_fit_extension.sql
-- AutoContentPublisherSystem 生活溶け込み拡張（Phase 15-10）
-- （BGM の時間帯スロット対応・ストーリーズ連続投稿対応・セット単位のストーリーズ有効化）
--
-- 設計の詳細（時間帯スロット選曲、ストーリーズ投稿フロー、UNIQUE 拡張の意図）は
-- docs/app/data-model.html のセクション 4.1 / 4.6 / 4.8 / 8 と
-- docs/app/batch-flow.html セクション 3 を参照。DDL のバージョン管理は
-- Flyway 風の命名規則（V<連番>__<説明>.sql）に従う。
--
-- 稼働中 DB への適用順序: 全変更が追加的（NULL/DEFAULT 付きカラム追加・ENUM 値の末尾追加・
-- UNIQUE 制約の緩和方向の拡張のみ）で既存アプリ（image-batch / sns-post-batch）の参照・INSERT と
-- 互換のため、アプリのデプロイと順序調整は不要（V003 と同じ扱い。適用後も旧アプリをそのまま実行してよい）。
-- 既存 posts 行は (generation_run_id, sns_account_id) で一意のため、拡張後の UNIQUE を自明に満たす。
--
-- 前提: 文字コード utf8mb4 / 照合順序 utf8mb4_unicode_ci。
-- 全 DATETIME カラムは UTC で保存する（アプリケーション側で変換してから格納する）。
-- DDL は暗黙コミットされるため、単一トランザクション化は行わない。

-- ============================================================
-- audio_assets（BGM の時間帯スロット対応）
-- ============================================================
ALTER TABLE audio_assets
    ADD COLUMN time_slot VARCHAR(20) NULL DEFAULT NULL COMMENT '時間帯スロット（parameters.slots の slot_code と同一の文字列。morning / noon / night 等）。NULL = スロット無関係（スロット非対応方式・全スロット共通曲）。スロット追加で DDL 変更を伴わせないため ENUM にしない' AFTER asset_type;

-- ============================================================
-- posts（ストーリーズ連続投稿対応）
-- ============================================================
-- media_type に 'story' を追加（末尾追加のため既存値の並び替えなし）。
-- feed_image / reel は先頭メディアの file_format から導出、story はリール success 後の
-- 連続投稿行としてアプリが明示設定する（docs/app/batch-flow.html セクション 3.3）
ALTER TABLE posts
    MODIFY COLUMN media_type ENUM('feed_image','reel','story') NOT NULL DEFAULT 'feed_image' COMMENT 'メディア種別（投稿 API 分岐用）。feed_image / reel は先頭メディアの file_format から導出、story はリール成功後の連続投稿行として明示設定（V004）';

-- 1 生成実行 × 1 アカウントを media_type 別に独立記録できるよう UNIQUE を拡張する。
-- 投稿対象決定クエリの NOT EXISTS 部分検索は左端プレフィックス
-- (generation_run_id, sns_account_id) で引き続き本インデックスを使用する
ALTER TABLE posts
    DROP INDEX uq_posts_generation_run_account,
    ADD UNIQUE KEY uq_posts_generation_run_account_media (generation_run_id, sns_account_id, media_type) COMMENT '1 生成実行 × 1 アカウント × 1 メディア種別につき 1 行のみ（リール行とストーリーズ行を独立記録する。自動再試行なし方針は不変）';

-- ============================================================
-- batch_sets（セット単位のストーリーズ有効化）
-- ============================================================
ALTER TABLE batch_sets
    ADD COLUMN stories_enabled TINYINT(1) NOT NULL DEFAULT 0 COMMENT 'ストーリーズ連続投稿の有効化フラグ（セット単位）。1 = リール成功後に同一動画を media_type=STORIES で再掲する。DEFAULT 0 により既存セットは無効のまま' AFTER generator_name;
