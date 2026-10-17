-- umigame-soup-1 改修 R-1-6 (2/2): キャプションテンプレートを元に戻す（手動投稿の後・当日 20:00 の定時投稿の前に必ず流す）
-- 適用先: Aurora（acps）とローカル MySQL。
UPDATE caption_templates c
JOIN batch_sets b ON b.id = c.set_id AND b.set_code = 'umigame-soup-1'
SET c.template_text = '{{caption}}{{prev_truth_block}}'
WHERE c.is_active = 1 AND c.template_text = '{{caption}}';

SELECT c.id, c.template_text, c.is_active FROM caption_templates c JOIN batch_sets b ON b.id = c.set_id
WHERE b.set_code = 'umigame-soup-1';
