-- V001__initial_schema.sql
-- AutoContentPublisherSystem 本スキーマ初期構築
--
-- 設計の詳細（ER図、各カラムの意図、S3キー設計、時刻の取り扱い、マイグレーション方針）は
-- docs/app/data-model.html を参照。DDL のバージョン管理は Flyway 風の命名規則
-- （V<連番>__<説明>.sql）に従い、本ファイルが最初の本スキーマ定義（V001）である。
-- database/V000__connection_test.sql（Phase 6-2 で作成した接続確認用テーブル）とは独立している。
--
-- 前提: 文字コード utf8mb4 / 照合順序 utf8mb4_unicode_ci。
-- 全 DATETIME カラムは UTC で保存する（アプリケーション側で変換してから格納する）。
-- 物理削除は行わない運用（is_active による論理無効化）のため、FK には CASCADE を使用しない
-- （デフォルトの RESTRICT のまま）。

-- ============================================================
-- batch_sets（セット）
-- ============================================================
CREATE TABLE batch_sets (
    id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '主キー',
    set_code VARCHAR(50) NOT NULL COMMENT 'セット識別コード（外部識別子。S3キー・Secret名・Scheduler入力・環境変数 SET_CODE に使用）',
    name VARCHAR(200) NOT NULL COMMENT 'セット名称',
    description TEXT NULL COMMENT '説明',
    is_active TINYINT(1) NOT NULL DEFAULT 1 COMMENT '有効フラグ（0 でセット廃止。両バッチはスキップして正常終了する）',
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '作成日時（UTC）',
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新日時（UTC）',
    PRIMARY KEY (id),
    UNIQUE KEY uq_batch_sets_set_code (set_code)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
COMMENT='バッチセット定義（1 セット = 1 テーマ = 画像生成バッチ + SNS 投稿バッチの組）';

-- ============================================================
-- prompt_configs（画像生成プロンプト設定）
-- ============================================================
CREATE TABLE prompt_configs (
    id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '主キー',
    set_id BIGINT UNSIGNED NOT NULL COMMENT 'バッチセット ID（FK）',
    prompt_text TEXT NOT NULL COMMENT 'プロンプト本文',
    negative_prompt TEXT NULL COMMENT 'ネガティブプロンプト',
    parameters JSON NULL COMMENT '生成パラメータ（モデル、アスペクト比、画像サイズ等）',
    is_active TINYINT(1) NOT NULL DEFAULT 1 COMMENT '有効フラグ。画像生成バッチは is_active=1 の全件をループ処理する',
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '作成日時（UTC）',
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新日時（UTC）',
    PRIMARY KEY (id),
    KEY idx_prompt_configs_set_active (set_id, is_active) COMMENT '画像生成バッチの is_active=1 全件取得クエリ向け',
    UNIQUE KEY uq_prompt_configs_set_id (set_id, id) COMMENT '複合 FK の参照先として使用',
    CONSTRAINT fk_prompt_configs_set FOREIGN KEY (set_id) REFERENCES batch_sets (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
COMMENT='画像生成プロンプト設定（セット : 設定 = 1 : N）';

-- ============================================================
-- caption_templates（投稿キャプションテンプレート）
-- ============================================================
CREATE TABLE caption_templates (
    id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '主キー',
    set_id BIGINT UNSIGNED NOT NULL COMMENT 'バッチセット ID（FK）',
    template_text TEXT NOT NULL COMMENT 'キャプション本文（ハッシュタグを含む固定文。Instagram の投稿本文はキャプション欄1本のため分割しない）',
    is_active TINYINT(1) NOT NULL DEFAULT 1 COMMENT '有効フラグ',
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '作成日時（UTC）',
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新日時（UTC）',
    PRIMARY KEY (id),
    KEY idx_caption_templates_set_active (set_id, is_active) COMMENT 'SNS 投稿バッチのテンプレート選定クエリ向け',
    UNIQUE KEY uq_caption_templates_set_id (set_id, id) COMMENT '複合 FK の参照先として使用',
    CONSTRAINT fk_caption_templates_set FOREIGN KEY (set_id) REFERENCES batch_sets (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
COMMENT='投稿キャプション・ハッシュタグの固定文テンプレート（紐づけ単位はセット）';

-- ============================================================
-- generation_runs（生成実行 = 投稿の単位）
-- ============================================================
CREATE TABLE generation_runs (
    id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '主キー',
    set_id BIGINT UNSIGNED NOT NULL COMMENT 'バッチセット ID（FK）',
    scheduled_at DATETIME NOT NULL COMMENT 'スケジュール実行時刻（UTC）。環境変数 SCHEDULED_AT を正規化した値。冪等性キー（set_id との組み合わせで一意）',
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '生成実行レコード作成日時（UTC）',
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新日時（UTC）',
    PRIMARY KEY (id),
    UNIQUE KEY uq_generation_runs_idempotency (set_id, scheduled_at) COMMENT '冪等性キー。画像生成バッチはこの制約への INSERT 成否で新規/再実行を判定する',
    UNIQUE KEY uq_generation_runs_set_id (set_id, id) COMMENT '複合 FK の参照先として使用。左端プレフィックスにより SNS 投稿バッチの投稿対象決定クエリ（WHERE set_id = ? ORDER BY scheduled_at）にも使用する',
    CONSTRAINT fk_generation_runs_set FOREIGN KEY (set_id) REFERENCES batch_sets (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
COMMENT='生成実行（1 回の画像生成バッチ起動 = 1 投稿分のコンテンツ）。posts・generated_images の親であり、投稿対象決定の基準単位';

-- ============================================================
-- generated_images（生成画像）
-- ============================================================
CREATE TABLE generated_images (
    id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '主キー',
    set_id BIGINT UNSIGNED NOT NULL COMMENT 'バッチセット ID（セット境界の整合性を保証する複合 FK 用に非正規化して保持）',
    generation_run_id BIGINT UNSIGNED NOT NULL COMMENT '生成実行 ID（FK）',
    prompt_config_id BIGINT UNSIGNED NOT NULL COMMENT '使用プロンプト設定 ID（FK）',
    output_index SMALLINT UNSIGNED NOT NULL DEFAULT 0 COMMENT '同一 (generation_run_id, prompt_config_id) 内での並び順（画像生成 API が返す image part の順序。0 始まり）',
    prompt_text_snapshot TEXT NOT NULL COMMENT '画像生成時に使用したプロンプト本文のスナップショット',
    negative_prompt_snapshot TEXT NULL COMMENT '画像生成時に使用したネガティブプロンプトのスナップショット',
    parameters_snapshot JSON NULL COMMENT '画像生成時に使用したパラメータのスナップショット',
    s3_key VARCHAR(500) NOT NULL COMMENT 'S3 オブジェクトキー（命名規約は docs/app/data-model.html セクション 5）',
    s3_bucket VARCHAR(200) NOT NULL COMMENT 'S3 バケット名',
    file_format VARCHAR(20) NOT NULL DEFAULT 'jpg' COMMENT 'ファイル形式（Instagram 要件により jpg に変換して保存する）',
    file_size_bytes BIGINT UNSIGNED NULL COMMENT 'ファイルサイズ（バイト）',
    width INT UNSIGNED NULL COMMENT '画像幅（ピクセル）',
    height INT UNSIGNED NULL COMMENT '画像高さ（ピクセル）',
    generation_api_response JSON NULL COMMENT 'API レスポンス（参考用）。保存前に認証情報・署名付き URL・個人情報に該当し得る値を除外する',
    generated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '画像生成 API から画像を取得した日時（UTC）',
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'DB レコード作成日時（UTC）',
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新日時（UTC）',
    PRIMARY KEY (id),
    UNIQUE KEY uq_generated_images_idempotency (generation_run_id, prompt_config_id, output_index) COMMENT '同一プロンプトからの同一順序の画像の二重登録を防止。左端プレフィックス (generation_run_id, prompt_config_id) は完了判定クエリ（存在確認）にも使用する',
    KEY idx_generated_images_set_run (set_id, generation_run_id) COMMENT '複合 FK (set_id, generation_run_id) 用インデックス',
    KEY idx_generated_images_set_prompt (set_id, prompt_config_id) COMMENT '複合 FK (set_id, prompt_config_id) 用インデックス。左端プレフィックス (set_id) は単純 FK にも使用する',
    CONSTRAINT fk_generated_images_set FOREIGN KEY (set_id) REFERENCES batch_sets (id),
    CONSTRAINT fk_generated_images_generation_run FOREIGN KEY (set_id, generation_run_id) REFERENCES generation_runs (set_id, id) COMMENT 'セット境界の整合性を保証する複合 FK',
    CONSTRAINT fk_generated_images_prompt_config FOREIGN KEY (set_id, prompt_config_id) REFERENCES prompt_configs (set_id, id) COMMENT 'セット境界の整合性を保証する複合 FK'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
COMMENT='生成画像のメタ情報。generation_runs の子（1 実行 : N 画像）。投稿ステータスは持たない（posts / post_images から導出）';

-- ============================================================
-- sns_accounts（SNS アカウント）
-- ============================================================
CREATE TABLE sns_accounts (
    id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '主キー',
    set_id BIGINT UNSIGNED NOT NULL COMMENT 'バッチセット ID（FK）',
    platform VARCHAR(50) NOT NULL COMMENT 'プラットフォーム（instagram 等）',
    account_code VARCHAR(50) NOT NULL COMMENT 'アカウント識別コード（作成後変更不可。Secret 名導出専用）',
    account_name VARCHAR(200) NOT NULL COMMENT 'アカウント表示名',
    is_active TINYINT(1) NOT NULL DEFAULT 1 COMMENT '有効フラグ。SNS 投稿バッチは is_active=1 の全件を処理対象にする',
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '作成日時（UTC）',
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新日時（UTC）',
    PRIMARY KEY (id),
    UNIQUE KEY uq_sns_accounts_set_platform_code (set_id, platform, account_code),
    UNIQUE KEY uq_sns_accounts_set_id (set_id, id) COMMENT '複合 FK の参照先として使用',
    CONSTRAINT fk_sns_accounts_set FOREIGN KEY (set_id) REFERENCES batch_sets (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
COMMENT='SNS 投稿先アカウント（セット : アカウント = 1 : N）。認証情報自体は Secrets Manager で管理し本テーブルには保持しない';

-- ============================================================
-- posts（投稿 = 生成実行 × アカウント）
-- ============================================================
CREATE TABLE posts (
    id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '主キー',
    set_id BIGINT UNSIGNED NOT NULL COMMENT 'バッチセット ID（セット境界の整合性を保証する複合 FK 用に非正規化して保持）',
    generation_run_id BIGINT UNSIGNED NOT NULL COMMENT '生成実行 ID（FK）',
    sns_account_id BIGINT UNSIGNED NOT NULL COMMENT '投稿先アカウント ID（FK）',
    caption_template_id BIGINT UNSIGNED NULL COMMENT '適用したキャプションテンプレート ID（FK。トレーサビリティ用。本文は caption_text_snapshot に固定化する）',
    caption_text_snapshot TEXT NULL COMMENT '投稿時に組み立てたキャプション本文のスナップショット。posts 作成直後は NULL で、本文組み立て後に設定する',
    status ENUM('pending', 'container_created', 'success', 'failed', 'published_unconfirmed') NOT NULL COMMENT '投稿状態遷移は docs/app/batch-flow.html セクション 3.2 を参照',
    platform_container_id VARCHAR(200) NULL COMMENT 'プラットフォーム側のコンテナ ID（Instagram の creation_id 等）',
    platform_post_id VARCHAR(200) NULL COMMENT 'プラットフォーム側の投稿 ID',
    error_message TEXT NULL COMMENT 'エラーメッセージ（failed / published_unconfirmed 時の原因記録）',
    api_response JSON NULL COMMENT 'API レスポンス（参考用）。保存前に認証情報・署名付き URL・個人情報に該当し得る値を除外する',
    posted_at DATETIME NULL COMMENT 'パブリッシュ成功日時（UTC）。status=success で設定する',
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '作成日時（UTC）',
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新日時（UTC）',
    PRIMARY KEY (id),
    UNIQUE KEY uq_posts_generation_run_account (generation_run_id, sns_account_id) COMMENT '1 生成実行 × 1 アカウントにつき 1 行のみ（attempt_number 相当のカラムは持たない。自動再試行なし方針のため）',
    KEY idx_posts_set_generation_run (set_id, generation_run_id) COMMENT '複合 FK (set_id, generation_run_id) 用インデックス。左端プレフィックス (set_id) は単純 FK にも使用する',
    KEY idx_posts_set_sns_account (set_id, sns_account_id) COMMENT '複合 FK (set_id, sns_account_id) 用インデックス',
    KEY idx_posts_set_caption_template (set_id, caption_template_id) COMMENT '複合 FK (set_id, caption_template_id) 用インデックス',
    CONSTRAINT fk_posts_set FOREIGN KEY (set_id) REFERENCES batch_sets (id),
    CONSTRAINT fk_posts_generation_run FOREIGN KEY (set_id, generation_run_id) REFERENCES generation_runs (set_id, id) COMMENT 'セット境界の整合性を保証する複合 FK',
    CONSTRAINT fk_posts_sns_account FOREIGN KEY (set_id, sns_account_id) REFERENCES sns_accounts (set_id, id) COMMENT 'セット境界の整合性を保証する複合 FK',
    CONSTRAINT fk_posts_caption_template FOREIGN KEY (set_id, caption_template_id) REFERENCES caption_templates (set_id, id) COMMENT 'セット境界の整合性を保証する複合 FK。caption_template_id が NULL の間は制約評価対象外'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
COMMENT='投稿 1 件（生成実行 × アカウント）。旧 post_records（画像 × アカウント × 試行）を「投稿」単位に再編したもの';

-- ============================================================
-- post_images（投稿と画像の中間テーブル）
-- ============================================================
CREATE TABLE post_images (
    id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '主キー',
    post_id BIGINT UNSIGNED NOT NULL COMMENT '投稿 ID（FK）',
    generated_image_id BIGINT UNSIGNED NOT NULL COMMENT '生成画像 ID（FK）',
    display_order SMALLINT UNSIGNED NOT NULL DEFAULT 0 COMMENT '投稿内での表示順（カルーセル対応。0 始まり）。初期構築では常に 1 行 = display_order 0 のみ',
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '作成日時（UTC）',
    PRIMARY KEY (id),
    UNIQUE KEY uq_post_images_post_image (post_id, generated_image_id) COMMENT '同一投稿への同一画像の重複登録を防止',
    UNIQUE KEY uq_post_images_post_order (post_id, display_order) COMMENT '同一投稿内での表示順の重複を防止',
    KEY idx_post_images_generated_image (generated_image_id) COMMENT 'FK 用インデックス',
    CONSTRAINT fk_post_images_post FOREIGN KEY (post_id) REFERENCES posts (id),
    CONSTRAINT fk_post_images_generated_image FOREIGN KEY (generated_image_id) REFERENCES generated_images (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
COMMENT='投稿に載せる画像の選択と表示順（1 投稿 : N 画像。当面の運用は 1 投稿 1 画像）。generated_image_id が post の generation_run に属することはアプリ層で保証する（DB では強制しない）';

-- ============================================================
-- batch_execution_logs（バッチ実行ログ）
-- ============================================================
CREATE TABLE batch_execution_logs (
    id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '主キー',
    set_id BIGINT UNSIGNED NOT NULL COMMENT 'バッチセット ID（FK）',
    batch_type ENUM('image_generation', 'sns_posting') NOT NULL COMMENT 'バッチ種別',
    execution_arn VARCHAR(500) NULL COMMENT 'Step Functions 実行 ARN（手動 RunTask 時は NULL）',
    status ENUM('running', 'succeeded', 'failed') NOT NULL COMMENT '実行結果',
    attempt_count INT UNSIGNED NOT NULL DEFAULT 1 COMMENT '同一 Step Functions 実行内で ECS タスクが起動された回数（Retry のたびに +1）',
    started_at DATETIME NOT NULL COMMENT '開始日時（UTC）',
    finished_at DATETIME NULL COMMENT '終了日時（UTC）',
    error_message TEXT NULL COMMENT 'エラーメッセージ',
    records_processed INT UNSIGNED NULL COMMENT '処理件数（画像生成: 生成完了画像件数 / SNS 投稿: 処理した投稿対象件数）',
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '作成日時（UTC）',
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新日時（UTC）',
    PRIMARY KEY (id),
    KEY idx_batch_execution_logs_set_type (set_id, batch_type),
    UNIQUE KEY uq_batch_execution_logs_execution_type (execution_arn, batch_type) COMMENT 'Step Functions 経由の同一実行・同一バッチ種別の二重 INSERT を防止。MySQL の UNIQUE は NULL を複数許容するため手動 RunTask は複数レコードを登録できる',
    CONSTRAINT fk_batch_execution_logs_set FOREIGN KEY (set_id) REFERENCES batch_sets (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
COMMENT='バッチ実行（Step Functions/ECS タスク起動単位）の運用ログ。業務データである generation_runs / posts とは役割が異なり、相互に FK を持たない';
