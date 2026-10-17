-- umigame-soup-1 改修 R-1-6 (1/2): 投稿順を 016 からやり直し、手動投稿の 1 本だけ「前回の真相」を付けない
-- 適用先: Aurora（acps）。ローカル MySQL にも同じものを流す（在庫の状態を揃えるため。テンプレートは 2/2 で元に戻る）
-- 実行後に手動投稿（画像生成 SFN を今の scheduled_at で起動）→ 投稿を確かめてから r1-6_restore_caption.sql を流す。
-- 旧版面で投稿した 3 件（016・001・008）の posts / post_insights / umigame_items は履歴として残す（削除しない）。

-- (1) 旧版面で使った 3 件を未使用に戻す（LRU は未使用を id 順に選ぶため 016 → 001 → 008 → 003 … の順になる）
UPDATE umigame_stock_items s
JOIN batch_sets b ON b.id = s.set_id AND b.set_code = 'umigame-soup-1'
SET s.use_count = 0, s.last_used_at = NULL
WHERE s.content_key IN ('016-umigame-soup', '001-faint-shadow', '008-who-made-the-mistake');

-- (2) キャプションテンプレートから前回の真相ブロックを一時的に外す（手動投稿の 1 本だけ。直前の成功投稿が旧版面の 008 のため）
UPDATE caption_templates c
JOIN batch_sets b ON b.id = c.set_id AND b.set_code = 'umigame-soup-1'
SET c.template_text = '{{caption}}'
WHERE c.is_active = 1 AND c.template_text = '{{caption}}{{prev_truth_block}}';

-- 確認: 次に選ばれる順（先頭が 016）とテンプレート
SELECT s.id, s.content_key, s.use_count, s.last_used_at
FROM umigame_stock_items s JOIN batch_sets b ON b.id = s.set_id
WHERE b.set_code = 'umigame-soup-1' AND s.is_active = 1 AND s.video_s3_key IS NOT NULL
ORDER BY s.last_used_at IS NULL DESC, s.last_used_at ASC, s.id ASC LIMIT 4;
SELECT c.id, c.template_text, c.is_active FROM caption_templates c JOIN batch_sets b ON b.id = c.set_id
WHERE b.set_code = 'umigame-soup-1';
