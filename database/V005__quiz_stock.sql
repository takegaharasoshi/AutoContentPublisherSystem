-- V005__quiz_stock.sql
-- AutoContentPublisherSystem 問題ストック（quiz_stock_items）対応
-- （問題ストック quiz_stock_items 新設・quiz_items への stock_item_id 追加）
--
-- 設計の詳細（各カラムの意図、LRU 取得クエリ、在庫確認クエリ、マイグレーション方針）は
-- docs/app/data-model.html のセクション 4.9 / 4.10 / 8 を参照。DDL のバージョン管理は
-- Flyway 風の命名規則（V<連番>__<説明>.sql）に従う。
--
-- 稼働中 DB への適用順序: 全変更が追加的（新テーブル・NULL 可カラム追加のみ）で
-- 既存アプリ（image-batch / sns-post-batch）の参照・INSERT と互換のため、アプリのデプロイと
-- 順序調整は不要（V003 と同じ扱い）。ただし新テーブルへの FK の向きにより
-- quiz_stock_items の CREATE を quiz_items の ALTER より先に実行する。
-- 初期ストックの INSERT は本 DDL に含めない（16-2 の投入作業。docs/app/operation.html セクション 3）。
--
-- 前提: 文字コード utf8mb4 / 照合順序 utf8mb4_unicode_ci。
-- 全 DATETIME カラムは UTC で保存する（アプリケーション側で変換してから格納する）。
-- DDL は暗黙コミットされるため、単一トランザクション化は行わない。

-- ============================================================
-- quiz_stock_items（問題ストック）
-- ============================================================
CREATE TABLE quiz_stock_items (
    id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '主キー',
    set_id BIGINT UNSIGNED NOT NULL COMMENT 'バッチセット ID（FK）。ストックはセット専属（世界観・文体がセット固有のため共有しない）',
    quiz_type VARCHAR(20) NOT NULL COMMENT '出題の型（L1=論理パズル / L3=フェルミ推定。型の追加で DDL 変更を伴わせないため ENUM にしない）。取得絞り込みキー',
    difficulty VARCHAR(20) NOT NULL COMMENT '難度ラベル（parameters.slots の difficulty と同一の文字列）。取得絞り込みキー',
    question_text TEXT NOT NULL COMMENT '問題文（書き直し済みの表現。文字数上限は方式のフィールド仕様に従う）',
    answer_text TEXT NOT NULL COMMENT '答え（書き直し済みの表現。L3 は「約◯◯（目安）」の幅表現に統一する）',
    content_fields JSON NOT NULL COMMENT '出題の構造化フィールド全体（hook・explanation・coach_comment・tags・summary・illustration_scene。quiz_items.content_fields と同スキーマ）',
    source_note TEXT NOT NULL COMMENT '出典と書き直しの証跡（元ネタの類型・参照 URL・表現は書き直し済みの旨。運用は docs/app/operation.html セクション 3）',
    is_active TINYINT(1) NOT NULL DEFAULT 1 COMMENT '有効フラグ。品質問題が見つかった問題の取り下げ（retire）用',
    use_count INT UNSIGNED NOT NULL DEFAULT 0 COMMENT '出題回数（再利用の観測用）',
    last_used_at DATETIME NULL COMMENT '最後に出題へ使用された日時（UTC）。NULL=未使用。LRU 順繰りの状態',
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '作成日時（UTC）',
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新日時（UTC）',
    PRIMARY KEY (id),
    UNIQUE KEY uq_quiz_stock_items_set_id (set_id, id) COMMENT '複合 FK の参照先として使用（quiz_items.stock_item_id）',
    KEY idx_quiz_stock_items_lru (set_id, quiz_type, difficulty, is_active, last_used_at) COMMENT 'LRU 取得クエリ・在庫確認クエリの絞り込み用',
    CONSTRAINT fk_quiz_stock_items_set FOREIGN KEY (set_id) REFERENCES batch_sets (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
COMMENT='問題ストック（人間レビュー済みの出題プール。LRU 順繰りの消費状態・出典証跡・取り下げを管理）';

-- ============================================================
-- quiz_items（消費した問題ストックへの参照）
-- ============================================================
-- セット境界の整合性を保証する複合 FK（FK 制約に COMMENT 句は使えないため行コメントで記載）
ALTER TABLE quiz_items
    ADD COLUMN stock_item_id BIGINT UNSIGNED NULL COMMENT '消費した問題ストック ID（quiz_stock_items への複合 FK。生成チェーン由来の既存行は NULL）' AFTER generation_run_id,
    ADD KEY idx_quiz_items_set_stock (set_id, stock_item_id) COMMENT '複合 FK (set_id, stock_item_id) 用インデックス',
    ADD CONSTRAINT fk_quiz_items_stock_item FOREIGN KEY (set_id, stock_item_id) REFERENCES quiz_stock_items (set_id, id);
