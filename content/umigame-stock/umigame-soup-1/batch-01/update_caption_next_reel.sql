-- 21-6i（2026-10-12）: 投稿を週 4 回（日・火・木・土）にしたため、キャプションの予告
-- 「真相は明日のリールのキャプションにて公開するよ。」を「真相は次のリールのキャプションにて公開するよ。」に直す。
-- 適用先: ローカル MySQL / Aurora（acps）。何度流しても結果は同じ（置換済みの行は変わらない）。
-- ストック行に加え、出題済みのスナップショット（umigame_items。2026-10-12 時点で 0 行）も直す。
-- 生成元の定型文は common/umigame_common.py の CAPTION_PLAY（insert / update_judge_points.sql は generate.py で再生成済み）。

UPDATE umigame_stock_items s
JOIN batch_sets b ON b.id = s.set_id
SET s.caption = REPLACE(s.caption, '真相は明日のリールのキャプションにて公開するよ。', '真相は次のリールのキャプションにて公開するよ。')
WHERE b.set_code = 'umigame-soup-1';

UPDATE umigame_items i
JOIN batch_sets b ON b.id = i.set_id
SET i.caption = REPLACE(i.caption, '真相は明日のリールのキャプションにて公開するよ。', '真相は次のリールのキャプションにて公開するよ。')
WHERE b.set_code = 'umigame-soup-1';

-- 確認（期待値: tomorrow_rows = 0 / next_rows = 14）
SELECT SUM(s.caption LIKE '%明日のリール%') AS tomorrow_rows, SUM(s.caption LIKE '%次のリール%') AS next_rows
FROM umigame_stock_items s JOIN batch_sets b ON b.id = s.set_id
WHERE b.set_code = 'umigame-soup-1';
