-- batch-01 既存 14 問のフックの更新（セット改修 R-1-3。動画の差し替え〔R-1-5〕と同時に実行する）
-- 生成元: content/umigame-stock/umigame-soup-1/batch-01/stock_items.py（単一ソース）
-- 適用先: ローカル MySQL / Aurora（acps）。set_code と content_key で対象を特定する。
-- 出題済み umigame_items のスナップショットは投稿当時の記録のため更新しない。

-- 001-faint-shadow
UPDATE umigame_stock_items SET hook = '影が薄いと言われて喜ぶ謎の男'
WHERE content_key = '001-faint-shadow'
  AND set_id = (SELECT id FROM batch_sets WHERE set_code = 'umigame-soup-1');

-- 003-silent-musicians
UPDATE umigame_stock_items SET hook = '音を出さない謎の男たち'
WHERE content_key = '003-silent-musicians'
  AND set_id = (SELECT id FROM batch_sets WHERE set_code = 'umigame-soup-1');

-- 004-fifty-year-letter
UPDATE umigame_stock_items SET hook = '会ったことのない男の子からの手紙の謎'
WHERE content_key = '004-fifty-year-letter'
  AND set_id = (SELECT id FROM batch_sets WHERE set_code = 'umigame-soup-1');

-- 005-bakers-egg
UPDATE umigame_stock_items SET hook = '割らない卵を自慢する謎のパン屋'
WHERE content_key = '005-bakers-egg'
  AND set_id = (SELECT id FROM batch_sets WHERE set_code = 'umigame-soup-1');

-- 006-frozen-tag
UPDATE umigame_stock_items SET hook = '凍りつく謎の男女'
WHERE content_key = '006-frozen-tag'
  AND set_id = (SELECT id FROM batch_sets WHERE set_code = 'umigame-soup-1');

-- 007-blank-letter
UPDATE umigame_stock_items SET hook = '白紙なのに果たされた約束謎の真相'
WHERE content_key = '007-blank-letter'
  AND set_id = (SELECT id FROM batch_sets WHERE set_code = 'umigame-soup-1');

-- 008-who-made-the-mistake
UPDATE umigame_stock_items SET hook = '完璧な演奏を間違えと思った男の謎'
WHERE content_key = '008-who-made-the-mistake'
  AND set_id = (SELECT id FROM batch_sets WHERE set_code = 'umigame-soup-1');

-- 009-year-late-verdict
UPDATE umigame_stock_items SET hook = 'スイカを見て謎の敗北宣言した兄'
WHERE content_key = '009-year-late-verdict'
  AND set_id = (SELECT id FROM batch_sets WHERE set_code = 'umigame-soup-1');

-- 010-two-hour-dentist
UPDATE umigame_stock_items SET hook = '2時間かけて歯医者に通う謎の男'
WHERE content_key = '010-two-hour-dentist'
  AND set_id = (SELECT id FROM batch_sets WHERE set_code = 'umigame-soup-1');

-- 012-early-morning-run
UPDATE umigame_stock_items SET hook = '男を追い抜く謎の子供たち'
WHERE content_key = '012-early-morning-run'
  AND set_id = (SELECT id FROM batch_sets WHERE set_code = 'umigame-soup-1');

-- 013-fifty-five-year-nengajo
UPDATE umigame_stock_items SET hook = '55年後の勝利の謎の真相'
WHERE content_key = '013-fifty-five-year-nengajo'
  AND set_id = (SELECT id FROM batch_sets WHERE set_code = 'umigame-soup-1');

-- 014-kind-interpreter
UPDATE umigame_stock_items SET hook = '嫁姑、突然の不仲の謎の真相'
WHERE content_key = '014-kind-interpreter'
  AND set_id = (SELECT id FROM batch_sets WHERE set_code = 'umigame-soup-1');

-- 015-unlicensed-driver
UPDATE umigame_stock_items SET hook = '週末にドライブする無免許男の謎'
WHERE content_key = '015-unlicensed-driver'
  AND set_id = (SELECT id FROM batch_sets WHERE set_code = 'umigame-soup-1');

-- 016-umigame-soup
UPDATE umigame_stock_items SET hook = 'ウミガメのスープを飲んで泣き崩れる謎の男'
WHERE content_key = '016-umigame-soup'
  AND set_id = (SELECT id FROM batch_sets WHERE set_code = 'umigame-soup-1');

-- 反映後のフックを確認する。
SELECT s.content_key, s.hook FROM umigame_stock_items s JOIN batch_sets b ON b.id = s.set_id
WHERE b.set_code = 'umigame-soup-1' ORDER BY s.content_key;
