-- V015__umigame_items_title.sql
-- ウミガメ出題履歴（umigame_items）に問題タイトル（title）のスナップショットを追加
--
-- SNS 投稿バッチが次回の投稿キャプション末尾に「前回の問題の真相ブロック」（前回の title と truth）を
-- 差し込むため（21-6h）。umigame_items は投稿時点のスナップショットを持ち、ストックを再参照しない契約
-- （V012）なので、title もここへ転記する。あわせて title・truth のカラム COMMENT を公開前提へ改める
-- （21-6d3e で title をキャプション見出し、truth を翌日のキャプションで公開する文に変えた）。
--
-- 適用順序（順序厳守）:
--   1. V015 を Aurora に適用する（既存行の title はストックから埋めてから NOT NULL にする）。
--   2. image-batch / sns-post-batch をデプロイする。
-- umigame-soup-1 は is_active=0 のため現状の実害はないが、逆順でデプロイすると image-batch の
-- umigame_items INSERT が title カラムを参照して失敗する。
--
-- 前提: 文字コード utf8mb4 / 照合順序 utf8mb4_unicode_ci。
-- DDL は暗黙コミットされるため、単一トランザクション化は行わない。

-- ============================================================
-- umigame_stock_items（ウミガメストック）
-- ============================================================
ALTER TABLE umigame_stock_items
    MODIFY COLUMN title VARCHAR(100) NOT NULL
        COMMENT '問題タイトル（キャプション見出し【title】・次回投稿の前回の真相ブロックで公開する）',
    MODIFY COLUMN truth TEXT NOT NULL
        COMMENT '真相（AI 出題者の判定根拠。版面には出さず、次回投稿のキャプション末尾〔前回の真相ブロック〕で全文を公開する）';

-- ============================================================
-- umigame_items（ウミガメ出題履歴）
-- ============================================================
ALTER TABLE umigame_items
    ADD COLUMN title VARCHAR(100) NULL
        COMMENT '問題タイトルのスナップショット（次回投稿の前回の真相ブロックの見出しに使う）'
        AFTER content_key;

UPDATE umigame_items ui
JOIN umigame_stock_items s ON s.set_id = ui.set_id AND s.id = ui.stock_item_id
SET ui.title = s.title
WHERE ui.title IS NULL;

ALTER TABLE umigame_items
    MODIFY COLUMN title VARCHAR(100) NOT NULL
        COMMENT '問題タイトルのスナップショット（次回投稿の前回の真相ブロックの見出しに使う）',
    MODIFY COLUMN truth TEXT NOT NULL
        COMMENT '真相のスナップショット（スナップショット JSON の判定根拠。次回投稿の前回の真相ブロックで全文を公開する）';
