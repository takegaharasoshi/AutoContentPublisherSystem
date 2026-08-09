-- V009__insights_support.sql
-- AutoContentPublisherSystem インサイト収集（post_insights / account_insights_daily）対応
--
-- 設計の詳細（各カラムの意図、冪等性、収集ウィンドウ、バックフィル方針）は
-- docs/app/data-model.html のセクション 4.11、処理フローは
-- docs/app/batch-flow.html のセクション 4 を参照。DDL のバージョン管理は
-- Flyway 風の命名規則（V<連番>__<説明>.sql）に従う。
--
-- 稼働中 DB への適用順序: 全変更が追加的（新テーブル 2 本・UNIQUE 追加・ENUM 値の末尾追加）で
-- 既存アプリ（image-batch / sns-post-batch）の参照・INSERT と互換のため、アプリのデプロイとの
-- 順序調整は不要（V003 と同じ扱い）。ただし FK の向きにより posts の ALTER（UNIQUE 追加）を
-- post_insights の CREATE より先に実行する。
--
-- 前提: 文字コード utf8mb4 / 照合順序 utf8mb4_unicode_ci。
-- 全 DATETIME カラムは UTC で保存する（アプリケーション側で変換してから格納する）。
-- DDL は暗黙コミットされるため、単一トランザクション化は行わない。

-- ============================================================
-- posts（post_insights の複合 FK 参照先）
-- ============================================================
ALTER TABLE posts
    ADD UNIQUE KEY uq_posts_set_id (set_id, id) COMMENT '複合 FK の参照先として使用（post_insights.post_id）';

-- ============================================================
-- batch_execution_logs（インサイト収集バッチ種別の追加）
-- ============================================================
ALTER TABLE batch_execution_logs
    MODIFY COLUMN batch_type ENUM('image_generation', 'sns_posting', 'insights_collection') NOT NULL COMMENT 'バッチ種別';

-- ============================================================
-- post_insights（投稿別インサイトのスナップショット）
-- ============================================================
CREATE TABLE post_insights (
    id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '主キー',
    set_id BIGINT UNSIGNED NOT NULL COMMENT 'バッチセット ID（セット境界の複合 FK 用に非正規化して保持）',
    post_id BIGINT UNSIGNED NOT NULL COMMENT '投稿 ID（posts.id への複合 FK。対象メディアの IG メディア ID は posts.platform_post_id を使うため本テーブルには保持しない）',
    scheduled_at DATETIME NOT NULL COMMENT '収集ランの識別子（Scheduler の実行予定時刻・UTC）。冪等性キー',
    collected_at DATETIME NOT NULL COMMENT '実際に API を呼んだ時刻（UTC）',
    metrics JSON NOT NULL COMMENT 'メディアレベル Insights 全メトリクスの生値マップ（breakdown 付きメトリクスは構造ごと保存）',
    api_version VARCHAR(20) NOT NULL COMMENT '取得時の Graph API バージョン（例 v25.0）',
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '作成日時（UTC）',
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新日時（UTC）',
    PRIMARY KEY (id),
    UNIQUE KEY uq_post_insights_post_scheduled (post_id, scheduled_at) COMMENT '冪等性キー。Step Functions Retry による再実行は INSERT-or-skip とし、欠測分だけを埋める',
    KEY idx_post_insights_set_post (set_id, post_id) COMMENT '複合 FK (set_id, post_id) 用インデックス。左端プレフィックス (set_id) は単純 FK にも使用する',
    CONSTRAINT fk_post_insights_set FOREIGN KEY (set_id) REFERENCES batch_sets (id),
    -- 以下はセット境界の整合性を保証する複合 FK（FK 制約に COMMENT 句は使えないため行コメントで記載）
    CONSTRAINT fk_post_insights_post FOREIGN KEY (set_id, post_id) REFERENCES posts (set_id, id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
COMMENT='投稿別インサイトのスナップショット（追記型。伸び曲線を残すため収集のたびに 1 行追加する）';

-- ============================================================
-- account_insights_daily（アカウント日次インサイト）
-- ============================================================
CREATE TABLE account_insights_daily (
    id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '主キー',
    set_id BIGINT UNSIGNED NOT NULL COMMENT 'バッチセット ID（複合 FK 用に非正規化して保持）',
    sns_account_id BIGINT UNSIGNED NOT NULL COMMENT 'SNS アカウント ID（sns_accounts.id への複合 FK）',
    metric_date DATE NOT NULL COMMENT 'UTC 日。UTC 日が閉じてから取得した確定値のみを書き、以後更新しない（INSERT IGNORE の upsert-once）',
    metrics JSON NOT NULL COMMENT 'アカウントレベル Insights 全メトリクスの生値マップ（breakdown 付きメトリクスは構造ごと保存）',
    followers_count INT UNSIGNED NULL COMMENT '行作成時点の IG User followers_count スナップショット（日締値ではなく収集時点の残高。バックフィルで作られた過去日行は NULL）',
    collected_at DATETIME NOT NULL COMMENT '実際に API を呼んだ時刻（UTC）',
    api_version VARCHAR(20) NOT NULL COMMENT '取得時の Graph API バージョン（例 v25.0）',
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '作成日時（UTC）',
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新日時（UTC）',
    PRIMARY KEY (id),
    UNIQUE KEY uq_account_insights_daily_account_date (sns_account_id, metric_date) COMMENT '1 アカウント・UTC 日につき 1 行のみ',
    KEY idx_account_insights_daily_set_account (set_id, sns_account_id) COMMENT '複合 FK (set_id, sns_account_id) 用インデックス',
    CONSTRAINT fk_account_insights_daily_set FOREIGN KEY (set_id) REFERENCES batch_sets (id),
    -- 以下はセット境界の整合性を保証する複合 FK（FK 制約に COMMENT 句は使えないため行コメントで記載）
    CONSTRAINT fk_account_insights_daily_account FOREIGN KEY (set_id, sns_account_id) REFERENCES sns_accounts (set_id, id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
COMMENT='アカウント日次インサイト（API 保持 90 日の制約に対する自前の長期時系列）';
