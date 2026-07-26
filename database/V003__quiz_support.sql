-- V003__quiz_support.sql
-- AutoContentPublisherSystem クイズ方式（gpt-quiz-multicut）対応
-- （出題履歴 quiz_items 新設・audio_assets の音源種別追加・file_format COMMENT の実態合わせ）
--
-- 設計の詳細（各カラムの意図、重複検査・選曲クエリ、S3 キー設計、マイグレーション方針)は
-- docs/app/data-model.html のセクション 4.8 / 4.9 / 5 / 8 を参照。DDL のバージョン管理は
-- Flyway 風の命名規則（V<連番>__<説明>.sql）に従う。
--
-- 稼働中 DB への適用順序: 全変更が追加的（新テーブル・DEFAULT 付きカラム追加・COMMENT 修正のみ）で
-- 既存アプリ（image-batch / sns-post-batch）の参照と互換のため、アプリのデプロイと順序調整は不要
-- （V002 のような無停止コーディネートは行わない。適用後も旧アプリをそのまま実行してよい）。
--
-- 前提: 文字コード utf8mb4 / 照合順序 utf8mb4_unicode_ci。
-- 全 DATETIME カラムは UTC で保存する（アプリケーション側で変換してから格納する）。
-- DDL は暗黙コミットされるため、単一トランザクション化は行わない。

-- ============================================================
-- quiz_items（出題履歴）
-- ============================================================
CREATE TABLE quiz_items (
    id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '主キー',
    set_id BIGINT UNSIGNED NOT NULL COMMENT 'バッチセット ID（セット境界の整合性を保証する複合 FK 用に非正規化して保持）',
    generation_run_id BIGINT UNSIGNED NOT NULL COMMENT '生成実行 ID（FK）。1 実行 1 問',
    quiz_type VARCHAR(20) NOT NULL COMMENT '出題の型（L1=論理パズル / L3=フェルミ推定。型の追加で DDL 変更を伴わせないため ENUM にしない）',
    difficulty VARCHAR(20) NULL COMMENT '難度ラベル（時間帯スロット設定 parameters.slots 由来のスナップショット）',
    summary VARCHAR(100) NOT NULL COMMENT '問題の要旨（重複検査でプロンプトの除外リストに渡す短文。LLM が字数上限付きで生成）',
    question_text TEXT NOT NULL COMMENT '問題文スナップショット（生成後の類似度検査の比較対象）',
    answer_text TEXT NOT NULL COMMENT '答えスナップショット（L3 は「約◯◯（目安）」の幅表現に統一する）',
    content_fields JSON NOT NULL COMMENT 'LLM が生成した構造化フィールド全体のスナップショット（フック文・解説・コーチの一言・タグ等）',
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '作成日時（UTC）',
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新日時（UTC）',
    PRIMARY KEY (id),
    UNIQUE KEY uq_quiz_items_generation_run (generation_run_id) COMMENT '1 実行 1 問（再実行時の二重登録防止）',
    KEY idx_quiz_items_set_type_created (set_id, quiz_type, created_at) COMMENT '重複検査の直近履歴取得クエリ（WHERE set_id=? AND quiz_type=? ORDER BY created_at DESC LIMIT ?）用',
    KEY idx_quiz_items_set_run (set_id, generation_run_id) COMMENT '複合 FK (set_id, generation_run_id) 用インデックス。左端プレフィックス (set_id) は単純 FK にも使用する',
    CONSTRAINT fk_quiz_items_set FOREIGN KEY (set_id) REFERENCES batch_sets (id),
    -- セット境界の整合性を保証する複合 FK（FK 制約に COMMENT 句は使えないため行コメントで記載）
    CONSTRAINT fk_quiz_items_generation_run FOREIGN KEY (set_id, generation_run_id) REFERENCES generation_runs (set_id, id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
COMMENT='出題履歴（クイズ方式が生成した問題のスナップショット。重複検査の参照元・Phase 16 インサイト突合の拡張余地）';

-- ============================================================
-- audio_assets（音源種別: BGM / SE）
-- ============================================================
ALTER TABLE audio_assets
    ADD COLUMN asset_type ENUM('bgm','se') NOT NULL DEFAULT 'bgm' COMMENT '音源種別（bgm=順繰り選曲の対象 / se=カットタイミング固定の効果音。順繰り選曲クエリは bgm のみを対象とする）' AFTER s3_key;

-- ============================================================
-- generated_media.file_format の COMMENT 実態合わせ（設計課題リスト 2026-07-25 の解消）
-- ============================================================
ALTER TABLE generated_media
    MODIFY COLUMN file_format VARCHAR(20) NOT NULL DEFAULT 'jpg' COMMENT 'ファイル形式（jpg / mp4 等）。S3 キーのプレフィックス・拡張子と posts.media_type 導出（sns-post-batch）の入力';
