-- V016__umigame_comment_logs.sql
-- AutoContentPublisherSystem ウミガメのコメント記録（umigame_comment_logs）と振り返り用ビューの新設（21-7b）
--
-- コメント返信経路（services/comment-reply の Reply Lambda）は Aurora 停止中でも動く設計のため Aurora へ直接書かず、
-- 1 コメント 1 件のコメント記録 JSON（schema_version=1）を S3 の comment-log/{set_code}/dt={UTC 日付}/{comment_id}.json
-- に置く。インサイト収集バッチ（insights-batch）が 06:00 / 18:00 JST の実行に相乗りして本テーブルへ取り込む
-- （Aurora の起動回数を増やさない）。設計の詳細は docs/app/data-model.html セクション 4.16 と
-- docs/app/sets/umigame-soup-1.html の「コメント記録」を参照。
--
-- 取り込みの契約:
--   ・comment_id 主キー + INSERT IGNORE で冪等（再実行・朝夕の重複読み込みで行が増えない。最初に取り込んだ版が残る）
--   ・コメント者は Instagram のユーザー ID（commenter_id）のみ保存し、username は持たない（JSON 側にも無い）
--   ・保持期限は Webhook 受信日時（= 取得日時）から 365 日。insights-batch が取り込みのたびに期限切れ行を DELETE する
--     （プライバシーポリシー infra/assets/umigame-privacy-policy/index.html と揃える）
--   ・record_json は S3 の JSON 全体（判定の reason・debug を含む）。抽出カラムは振り返りで絞り込む項目だけ
--
-- 稼働中 DB への適用順序: 追加のみ（新テーブル 1 本 + ビュー 1 本）。insights-batch のデプロイより先に適用する
-- （逆順だと取り込みが「テーブルなし」で失敗し、インサイト収集の実行が failed になる）。
-- 前提: 文字コード utf8mb4 / 照合順序 utf8mb4_unicode_ci。全 DATETIME カラムは UTC で保存する。
-- DDL は暗黙コミットされるため、単一トランザクション化は行わない。

-- ============================================================
-- umigame_comment_logs（ウミガメのコメント記録）
-- ============================================================
CREATE TABLE umigame_comment_logs (
    comment_id VARCHAR(64) NOT NULL COMMENT 'Instagram のコメント ID（主キー。INSERT IGNORE による冪等取り込みの単位）',
    set_id BIGINT UNSIGNED NOT NULL COMMENT 'バッチセット ID（FK。JSON の set_code から引く）',
    parent_id VARCHAR(64) NULL COMMENT '返信先のコメント ID（スレッド内の返信なら値あり。トップレベルは NULL）',
    media_id VARCHAR(64) NOT NULL COMMENT '投稿（リール）のメディア ID（posts.platform_post_id と突合できる）',
    content_key VARCHAR(64) NULL COMMENT '問題の業務キー（問題スナップショットが引けなかった回は NULL）',
    problem_schema_version INT NULL COMMENT '問題スナップショットのスキーマ版',
    fact_sheet_hash CHAR(12) NULL COMMENT '確定事実シートのハッシュ（シート修正の前後を区別する）',
    commenter_id VARCHAR(64) NULL COMMENT 'コメント者の Instagram ユーザー ID（username は保存しない。削除依頼はこの ID で行を消す）',
    comment_text TEXT NOT NULL COMMENT 'コメント本文',
    comment_created_at DATETIME NULL COMMENT 'コメント投稿日時（UTC）',
    webhook_received_at DATETIME NOT NULL COMMENT 'Webhook 受信日時（UTC。S3 キーの dt= はこの日付。保持期限 365 日の起点）',
    judged_at DATETIME NULL COMMENT '判定日時（UTC）',
    replied_at DATETIME NULL COMMENT '返信日時（UTC。返信しなかった回は NULL）',
    judge_mode VARCHAR(20) NULL COMMENT '判定モード（luna / jev / haiku）',
    reply_variant VARCHAR(40) NULL COMMENT '返信文の案（例: 1b-haiku）',
    prompt_version VARCHAR(20) NULL COMMENT '同梱プロンプトのハッシュ（プロンプト修正の前後を区別する）',
    final_kind VARCHAR(40) NULL COMMENT '最終判定の種別（例: guess_correct）',
    final_decision VARCHAR(20) NULL COMMENT '最終判定を出した方式（luna / jev / haiku）',
    reply_text TEXT NULL COMMENT '返信文（返信しなかった回は NULL）',
    reply_source VARCHAR(20) NULL COMMENT '返信文の出どころ（llm / no_reply 等）',
    reply_id VARCHAR(64) NULL COMMENT '返信コメントの ID',
    error_count INT NOT NULL DEFAULT 0 COMMENT 'errors 配列の件数（0 以外は振り返りの優先対象）',
    record_json JSON NOT NULL COMMENT 'コメント記録 JSON の全体（判定の理由・debug を含む。username は含まない）',
    s3_key VARCHAR(512) NOT NULL COMMENT '取り込み元の S3 キー',
    imported_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '取り込み日時（UTC）',
    PRIMARY KEY (comment_id),
    KEY idx_umigame_comment_logs_set_received (set_id, webhook_received_at) COMMENT 'セット・期間での振り返りと保持期限切れの削除用',
    KEY idx_umigame_comment_logs_commenter (commenter_id) COMMENT 'データ削除依頼への対応用',
    CONSTRAINT fk_umigame_comment_logs_set FOREIGN KEY (set_id) REFERENCES batch_sets (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
COMMENT='ウミガメのコメント記録（コメント返信経路が S3 に書いた 1 コメント 1 件の JSON を insights-batch が取り込む。継続改善の振り返り用。保持 365 日）';

-- ============================================================
-- v_umigame_comment_review（振り返り用ビュー。1 コメント 1 行）
-- ============================================================
-- 誤判定を拾う → 確定事実シート / プロンプトを直す → 回帰プローブに足す、の 1 段目に使う。
-- 時刻は JST（+9 時間）で出す。judge_reason は最終判定を出した方式の reason。
-- 問題タイトルはストック（set_id + content_key で一意）から引く。
CREATE OR REPLACE VIEW v_umigame_comment_review AS
SELECT
    bs.set_code,
    c.comment_id,
    DATE_ADD(c.webhook_received_at, INTERVAL 9 HOUR) AS received_at_jst,
    c.media_id,
    c.content_key,
    s.title AS problem_title,
    c.parent_id IS NOT NULL AS is_thread_reply,
    c.comment_text,
    c.final_kind,
    c.final_decision,
    JSON_UNQUOTE(JSON_EXTRACT(c.record_json, CONCAT('$.judgements.', c.final_decision, '.reason'))) AS judge_reason,
    c.reply_source,
    c.reply_text,
    TIMESTAMPDIFF(SECOND, c.webhook_received_at, c.replied_at) AS reply_latency_s,
    c.error_count,
    c.judge_mode,
    c.reply_variant,
    c.prompt_version,
    c.fact_sheet_hash
FROM umigame_comment_logs c
JOIN batch_sets bs ON bs.id = c.set_id
LEFT JOIN umigame_stock_items s ON s.set_id = c.set_id AND s.content_key = c.content_key;
