-- V012__umigame_stock.sql
-- AutoContentPublisherSystem ウミガメのスープ参加型セット（umigame-soup-1）対応
-- （batch_sets.problem_snapshot_enabled の追加・ウミガメストック umigame_stock_items・
--   ウミガメ出題履歴 umigame_items の新設）
--
-- 設計の詳細（各カラムの意図、LRU 取得クエリ、素材 14 項目、投稿後スナップショット）は
-- docs/app/data-model.html のセクション 4.1 / 4.14 / 4.15 と
-- docs/app/sets/umigame-soup-1.html セクション 4、
-- docs/app/generators/umigame-prebuilt.html セクション 4 を参照。DDL の
-- バージョン管理は Flyway 風の命名規則（V<連番>__<説明>.sql）に従う。
--
-- 稼働中 DB への適用順序: 全変更が追加的（新テーブル 2 本 + DEFAULT 付きカラム 1 本）で既存アプリの
-- 参照・INSERT と互換のため、アプリのデプロイとの順序調整は不要（V010 と同じ扱い）。ただし FK の向きにより
-- umigame_stock_items の CREATE を umigame_items の CREATE より先に実行する。
-- 適用は 21-4a でローカル MySQL へ、人間ゲート通過後に Aurora へ行う。初期ストックの INSERT は本 DDL に
-- 含めない（21-4b の投入作業）。batch_sets 行の INSERT・problem_snapshot_enabled の有効化は 21-7。
--
-- 前提: 文字コード utf8mb4 / 照合順序 utf8mb4_unicode_ci。
-- 全 DATETIME カラムは UTC で保存する（アプリケーション側で変換してから格納する）。
-- DDL は暗黙コミットされるため、単一トランザクション化は行わない。

-- ============================================================
-- batch_sets.problem_snapshot_enabled（投稿後スナップショット出力フラグ）
-- ============================================================
-- stories_enabled と同じ性質（バッチが実行時に参照するセット単位の挙動スイッチ）のため同じ形で置く。
-- 1 のセットは SNS 投稿バッチがリール投稿成功直後に assets/{set_code}/problems/{media_id}.json を出力する
-- （batch-flow.html 3.3 手順 6）。DEFAULT 0 により既存セットの挙動は不変。
ALTER TABLE batch_sets
    ADD COLUMN problem_snapshot_enabled TINYINT(1) NOT NULL DEFAULT 0
        COMMENT '投稿後の問題スナップショット出力フラグ（1=publish 成功直後に umigame_items と prompt_configs.prompt_text から problems/{media_id}.json を S3 へ出力。方式名から暗黙に決めない）'
        AFTER stories_enabled;

-- ============================================================
-- umigame_stock_items（ウミガメストック）
-- ============================================================
-- 1 行 = 素材 14 項目（docs/app/sets/umigame-soup-1.html セクション 4 が正）+ 単尺の事前動画参照。
-- ranking_stock_items（V010）の「セット配下の有効レコード + LRU 順繰り + 証跡カラム一元管理 +
-- セット境界の複合 FK + 環境非依存の業務キー content_key」パターンを踏襲する。
CREATE TABLE umigame_stock_items (
    id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '主キー',
    set_id BIGINT UNSIGNED NOT NULL COMMENT 'バッチセット ID（FK）。ストックはセット専属',
    content_key VARCHAR(64) NOT NULL COMMENT '環境非依存の業務キー（{3 桁連番}-{slug}。例: 001-lighthouse-letter。スロット接頭辞なし・セット内一意・連番は取り下げ後も再利用しない）。事前動画・背景の S3 キーの構成要素。投入時に採番し、ローカル MySQL と Aurora へ同じ値を入れる',
    title VARCHAR(100) NOT NULL COMMENT '管理用の題名（版面・キャプションには出さない）',
    difficulty TINYINT UNSIGNED NOT NULL COMMENT '難易度 1〜5（運用の目安・在庫の偏り確認用。取得の軸にはしない）',
    problem_text VARCHAR(255) NOT NULL COMMENT '問題文（78〜85 字。版面の問題カードに全文を常時表示）',
    truth TEXT NOT NULL COMMENT '真相（AI 出題者の判定根拠・正解宣言時の開示文。版面・キャプションには出さない）',
    fact_sheet JSON NOT NULL COMMENT '確定事実シート（文字列の配列・8〜12 件。「はい / いいえ / 関係ない」の判定根拠。問題に関係ない事項も明示）',
    expected_questions JSON NOT NULL COMMENT '想定質問と期待回答（[{"q": …, "a": …}]・15〜20 件。プローブテストの検証セット。レビュー済みの検証セットを投入物と一緒に残す）',
    hook VARCHAR(40) NOT NULL COMMENT 'フック文（12 字前後。版面のつかみ帯・{{hook}} の展開元）',
    rule_text VARCHAR(100) NOT NULL COMMENT 'ルール帯（45 字前後。常時表示の遊び方。セット既定文あり）',
    narration JSON NOT NULL COMMENT 'ナレーション cue（{"problem": …, "rule": …}。表示文と別の読み上げ用の文。予算検査は umigame-prebuilt.html 8.3）',
    play_example JSON NOT NULL COMMENT 'プレイ例（[{"role": "questioner"|"master", "text": …} × 6 の交互。3 往復のうち 1 つは「はい」）',
    character_lines JSON NOT NULL COMMENT 'キャラクターの台詞（{"master": {"intro": …, "outro": …}, "jr": {"outro": …}}。各 17 字以内。セット既定文あり）',
    illustration_prompt TEXT NOT NULL COMMENT 'イラスト作成用プロンプト（画風固定行 + 情景 + 禁止事項。背景 1 枚を imagegen で生成）',
    caption TEXT NOT NULL COMMENT 'キャプション（本文 + ハッシュタグ。#AIart 必須。{{caption}} の展開元）',
    source_note TEXT NOT NULL COMMENT '出典・オリジナル性メモ（完全オリジナル宣言と着想元の証跡）',
    video_s3_key VARCHAR(512) NULL COMMENT '事前動画マスターの S3 キー（assets/{set_code}/prebuilt/{content_key}.mp4）。NULL=未ビルドで投稿候補から除外',
    video_audio_asset_id BIGINT UNSIGNED NULL COMMENT 'ビルド時に選曲し動画へベイクした BGM の audio_assets ID（複合 FK でセット境界を保証。実行時に generated_media.audio_asset_id へ転記）',
    video_built_at DATETIME NULL COMMENT '事前動画の最終ビルド日時（UTC）。版面・仕様改訂時の再ビルド対象を識別する専用日時',
    is_active TINYINT(1) NOT NULL DEFAULT 1 COMMENT '有効フラグ。品質問題（矛盾・ネタバレ回答・不適切）の取り下げと在庫不足時の投稿スキップ用',
    use_count INT UNSIGNED NOT NULL DEFAULT 0 COMMENT '投稿回数（再利用の観測用）',
    last_used_at DATETIME NULL COMMENT '最後に投稿へ使用された日時（UTC）。NULL=未使用。LRU 順繰りの状態',
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '作成日時（UTC）',
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新日時（UTC）',
    PRIMARY KEY (id),
    UNIQUE KEY uq_umigame_stock_items_set_id (set_id, id) COMMENT '複合 FK の参照先として使用（umigame_items.stock_item_id）',
    UNIQUE KEY uq_umigame_stock_items_set_content_key (set_id, content_key) COMMENT 'content_key のセット内一意性を保証',
    KEY idx_umigame_stock_items_lru (set_id, is_active, last_used_at) COMMENT 'LRU 取得クエリ・在庫確認クエリの絞り込み用（難易度の軸は持たないため 3 カラム）',
    KEY idx_umigame_stock_items_set_video_audio (set_id, video_audio_asset_id) COMMENT '複合 FK (set_id, video_audio_asset_id) 用インデックス',
    CONSTRAINT fk_umigame_stock_items_set FOREIGN KEY (set_id) REFERENCES batch_sets (id),
    CONSTRAINT fk_umigame_stock_items_video_audio FOREIGN KEY (set_id, video_audio_asset_id) REFERENCES audio_assets (set_id, id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
COMMENT='ウミガメストック（人間レビュー + プローブテスト済みの問題プール。素材 14 項目・事前動画参照・LRU 消費状態・オリジナル性証跡・取り下げを管理）';

-- ============================================================
-- umigame_items（ウミガメ出題履歴）
-- ============================================================
-- ranking_items（V010）と同じ「生成実行と 1 : 1・行の作成は方式・commit は共通骨格」の契約。
-- 問題固有部分を投稿時点のスナップショットとして丸ごと持ち、SNS 投稿バッチがストックを再参照せずに
-- キャプション展開と問題スナップショット出力を行えるようにする（ストックの後日修正が投稿済み問題の
-- 返信ルールに波及しない）。SNS 投稿バッチが更新するのは snapshot_s3_key / snapshot_written_at の 2 カラムのみ。
-- セット境界の整合性を保証する複合 FK（FK 制約に COMMENT 句は使えないため行コメントで記載）
CREATE TABLE umigame_items (
    id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '主キー',
    set_id BIGINT UNSIGNED NOT NULL COMMENT 'バッチセット ID（FK）。複合 FK 用に非正規化して保持',
    generation_run_id BIGINT UNSIGNED NOT NULL COMMENT 'この問題を使った生成実行（generation_runs への複合 FK）',
    stock_item_id BIGINT UNSIGNED NOT NULL COMMENT '消費したウミガメストック ID（umigame_stock_items への複合 FK。再出題の検出・品質問題の遡及用）',
    content_key VARCHAR(64) NOT NULL COMMENT 'ストックの業務キーの転記（スナップショット JSON に載せ、環境をまたいで問題を特定する）',
    problem_text VARCHAR(255) NOT NULL COMMENT '問題文のスナップショット（版面に焼き込まれた文と一致）',
    truth TEXT NOT NULL COMMENT '真相のスナップショット（版面・キャプションには出さない。スナップショット JSON の判定根拠）',
    fact_sheet JSON NOT NULL COMMENT '確定事実シートのスナップショット（文字列の配列）',
    rule_text VARCHAR(100) NOT NULL COMMENT 'ルール帯のスナップショット（スナップショット JSON に載せる）',
    hook VARCHAR(40) NOT NULL COMMENT 'フック文のスナップショット（{{hook}} の展開元）',
    caption TEXT NOT NULL COMMENT 'キャプションのスナップショット（{{caption}} の展開元）',
    snapshot_s3_key VARCHAR(512) NULL COMMENT '投稿後の問題スナップショットの S3 キー（assets/{set_code}/problems/{media_id}.json）。NULL=未出力（posts.status=success との突合で運用が拾う）。SNS 投稿バッチが更新する',
    snapshot_written_at DATETIME NULL COMMENT 'スナップショット出力日時（UTC）。SNS 投稿バッチが更新する',
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '作成日時（UTC）',
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新日時（UTC）',
    PRIMARY KEY (id),
    UNIQUE KEY uq_umigame_items_generation_run (generation_run_id) COMMENT '1 実行 1 問（再実行時の二重登録防止）',
    KEY idx_umigame_items_set_run (set_id, generation_run_id) COMMENT '複合 FK (set_id, generation_run_id) 用インデックス',
    KEY idx_umigame_items_set_stock (set_id, stock_item_id) COMMENT '複合 FK (set_id, stock_item_id) 用インデックス',
    CONSTRAINT fk_umigame_items_run FOREIGN KEY (set_id, generation_run_id) REFERENCES generation_runs (set_id, id),
    CONSTRAINT fk_umigame_items_stock_item FOREIGN KEY (set_id, stock_item_id) REFERENCES umigame_stock_items (set_id, id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
COMMENT='ウミガメ出題履歴（ウミガメ方式が投稿した問題固有部分の投稿時点スナップショット。キャプション展開の入力・投稿後の問題スナップショット出力の記録）';
