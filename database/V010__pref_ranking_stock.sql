-- V010__pref_ranking_stock.sql
-- AutoContentPublisherSystem ランキングセット対応
-- （ランキングストック ranking_stock_items・ランキング投稿履歴 ranking_items の新設）
--
-- 設計の詳細（各カラムの意図、LRU 取得クエリ、2 尺の持ち方、在庫確認クエリ）は
-- docs/app/data-model.html のセクション 4.12 / 4.13 と
-- docs/app/generators/ranking-prebuilt.html のセクション 4 を参照。DDL の
-- バージョン管理は Flyway 風の命名規則（V<連番>__<説明>.sql）に従う。
--
-- 稼働中 DB への適用順序: 全変更が追加的（新テーブル 2 本のみ）で既存アプリの参照・INSERT と
-- 互換のため、アプリのデプロイとの順序調整は不要（V003 と同じ扱い）。ただし FK の向きにより
-- ranking_stock_items の CREATE を ranking_items の CREATE より先に実行する。
-- 適用は 17-3 でローカル MySQL と Aurora の両環境へ行う。初期ストックの INSERT は本 DDL に
-- 含めない（17-5 の投入作業。docs/app/operation.html セクション 3）。
--
-- 前提: 文字コード utf8mb4 / 照合順序 utf8mb4_unicode_ci。
-- 全 DATETIME カラムは UTC で保存する（アプリケーション側で変換してから格納する）。
-- DDL は暗黙コミットされるため、単一トランザクション化は行わない。

-- ============================================================
-- ranking_stock_items（ランキングストック）
-- ============================================================
CREATE TABLE ranking_stock_items (
    id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '主キー',
    set_id BIGINT UNSIGNED NOT NULL COMMENT 'バッチセット ID（FK）。ストックはセット専属',
    content_key VARCHAR(64) NOT NULL COMMENT '環境非依存の業務キー（{3 桁連番}-{slug}。例: 001-gyoza-spend。セット内一意）。事前動画・背景の S3 キーの構成要素。投入時に採番し、ローカル MySQL と Aurora へ同じ値を入れる',
    format VARCHAR(20) NOT NULL COMMENT '動画フォーマット（初期は top5-map のみ。フォーマット追加で DDL 変更を伴わせないため ENUM にしない）',
    title VARCHAR(100) NOT NULL COMMENT 'ランキングタイトル（版面タイトル帯・キャプションの title プレースホルダ）',
    content_fields JSON NOT NULL COMMENT '表示文言の構造化フィールド（hook・trivia・source_display・result_list・value_suffix・subtitle・bg_motif）。result_list はツーリングが ranking_data + value_suffix から機械整形する（手書き禁止）',
    ranking_data JSON NOT NULL COMMENT '換算済み TOP5 の構造化データ（{"entries":[{"rank":1,"pref_code":30,"value":...},...5 件]}）。数値と都道府県コードのみで言語文字列を含めない',
    narration JSON NOT NULL COMMENT '尺別の cue 台本（{"20s":{...},"30s":{...}}。cue ID 体系は docs/app/generators/ranking-prebuilt.html セクション 8.3）',
    source_note TEXT NOT NULL COMMENT '出典と県換算の証跡（出典 URL・データ年・取得日・換算方式〔世帯数加重平均〕と世帯数データの出典）',
    is_active TINYINT(1) NOT NULL DEFAULT 1 COMMENT '有効フラグ。品質問題が見つかったネタの取り下げ（retire）用',
    use_count INT UNSIGNED NOT NULL DEFAULT 0 COMMENT '投稿回数（再利用の観測用。2 尺共通）',
    last_used_at DATETIME NULL COMMENT '最後に投稿へ使用された日時（UTC）。NULL=未使用。LRU 順繰りの状態（2 尺共通）',
    video_s3_key_20s VARCHAR(512) NULL COMMENT '20 秒版事前動画マスターの S3 キー（assets/{set_code}/prebuilt/{content_key}_20s.mp4）。NULL=未ビルトで 20 秒スロットの候補から除外',
    video_s3_key_30s VARCHAR(512) NULL COMMENT '30 秒版事前動画マスターの S3 キー（同 _30s.mp4）。NULL=未ビルトで 30 秒スロットの候補から除外',
    video_audio_asset_id BIGINT UNSIGNED NULL COMMENT 'ビルド時に選曲し動画へベイクした BGM の audio_assets ID（2 尺共通の 1 曲。複合 FK でセット境界を保証。実行時に generated_media.audio_asset_id へ転記）',
    video_built_at DATETIME NULL COMMENT '事前動画の最終ビルド日時（UTC）。版面・仕様改訂時の再ビルド対象を識別する専用日時',
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '作成日時（UTC）',
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新日時（UTC）',
    PRIMARY KEY (id),
    UNIQUE KEY uq_ranking_stock_items_set_id (set_id, id) COMMENT '複合 FK の参照先として使用（ranking_items.stock_item_id）',
    UNIQUE KEY uq_ranking_stock_items_set_content_key (set_id, content_key) COMMENT 'content_key のセット内一意性を保証',
    KEY idx_ranking_stock_items_lru (set_id, is_active, last_used_at) COMMENT 'LRU 取得クエリ・在庫確認クエリの絞り込み用（型・難度の軸がないため 3 カラム）',
    KEY idx_ranking_stock_items_set_video_audio (set_id, video_audio_asset_id) COMMENT '複合 FK (set_id, video_audio_asset_id) 用インデックス',
    CONSTRAINT fk_ranking_stock_items_set FOREIGN KEY (set_id) REFERENCES batch_sets (id),
    CONSTRAINT fk_ranking_stock_items_video_audio FOREIGN KEY (set_id, video_audio_asset_id) REFERENCES audio_assets (set_id, id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
COMMENT='ランキングストック（人間レビュー済みのネタプール。2 尺の事前動画参照・LRU 消費状態・出典/県換算証跡・取り下げを管理）';

-- ============================================================
-- ranking_items（ランキング投稿履歴）
-- ============================================================
-- セット境界の整合性を保証する複合 FK（FK 制約に COMMENT 句は使えないため行コメントで記載）
CREATE TABLE ranking_items (
    id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '主キー',
    set_id BIGINT UNSIGNED NOT NULL COMMENT 'バッチセット ID（FK）。複合 FK 用に非正規化して保持',
    generation_run_id BIGINT UNSIGNED NOT NULL COMMENT 'このネタを使った生成実行（generation_runs への複合 FK）',
    format VARCHAR(20) NOT NULL COMMENT '動画フォーマットのスナップショット（top5-map 等）',
    title VARCHAR(100) NOT NULL COMMENT 'ランキングタイトルのスナップショット（キャプションの title プレースホルダの展開元）',
    content_fields JSON NOT NULL COMMENT '表示文言のスナップショット（ranking_stock_items.content_fields と同スキーマ。キャプション展開の入力）',
    ranking_data JSON NOT NULL COMMENT '換算済み TOP5 のスナップショット（ranking_stock_items.ranking_data と同スキーマ）',
    duration_seconds INT UNSIGNED NOT NULL COMMENT '投稿した尺（20 / 30。スロットの duration_seconds 由来）。2 尺検証の尺別集計キー',
    stock_item_id BIGINT UNSIGNED NOT NULL COMMENT '消費したランキングストック ID（ranking_stock_items への複合 FK。ストック方式のみのため NOT NULL）',
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '作成日時（UTC）',
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新日時（UTC）',
    PRIMARY KEY (id),
    UNIQUE KEY uq_ranking_items_generation_run (generation_run_id) COMMENT '1 実行 1 ネタ（再実行時の二重登録防止）',
    KEY idx_ranking_items_set_run (set_id, generation_run_id) COMMENT '複合 FK (set_id, generation_run_id) 用インデックス',
    KEY idx_ranking_items_set_stock (set_id, stock_item_id) COMMENT '複合 FK (set_id, stock_item_id) 用インデックス',
    CONSTRAINT fk_ranking_items_run FOREIGN KEY (set_id, generation_run_id) REFERENCES generation_runs (set_id, id),
    CONSTRAINT fk_ranking_items_stock_item FOREIGN KEY (set_id, stock_item_id) REFERENCES ranking_stock_items (set_id, id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
COMMENT='ランキング投稿履歴（ランキング方式が投稿したネタ内容 + 尺のスナップショット。キャプション展開の入力・尺別効果検証の記録）';
