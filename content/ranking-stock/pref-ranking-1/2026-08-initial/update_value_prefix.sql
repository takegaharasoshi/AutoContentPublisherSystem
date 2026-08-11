-- 投入済み 10 件への value_prefix 追記（17-4a で新設したフィールド。17-4b で適用）
-- 生成元: content/ranking-stock/pref-ranking-1/2026-08-initial/data/*.json の meta.prefix
-- 適用先: ローカル MySQL / Aurora(acps)。冪等（再実行しても同じ値を書く）

UPDATE ranking_stock_items r JOIN batch_sets b ON b.id = r.set_id
   SET r.content_fields = JSON_SET(r.content_fields, '$.value_prefix', CAST('"年間"' AS JSON))
 WHERE b.set_code = 'pref-ranking-1' AND r.content_key = '001-gyoza-spend';
UPDATE ranking_stock_items r JOIN batch_sets b ON b.id = r.set_id
   SET r.content_fields = JSON_SET(r.content_fields, '$.value_prefix', CAST('"年間"' AS JSON))
 WHERE b.set_code = 'pref-ranking-1' AND r.content_key = '002-ramen-out';
UPDATE ranking_stock_items r JOIN batch_sets b ON b.id = r.set_id
   SET r.content_fields = JSON_SET(r.content_fields, '$.value_prefix', CAST('"年間"' AS JSON))
 WHERE b.set_code = 'pref-ranking-1' AND r.content_key = '003-bread-spend';
UPDATE ranking_stock_items r JOIN batch_sets b ON b.id = r.set_id
   SET r.content_fields = JSON_SET(r.content_fields, '$.value_prefix', CAST('"年間"' AS JSON))
 WHERE b.set_code = 'pref-ranking-1' AND r.content_key = '004-natto-spend';
UPDATE ranking_stock_items r JOIN batch_sets b ON b.id = r.set_id
   SET r.content_fields = JSON_SET(r.content_fields, '$.value_prefix', CAST('"年間"' AS JSON))
 WHERE b.set_code = 'pref-ranking-1' AND r.content_key = '005-icecream-spend';
UPDATE ranking_stock_items r JOIN batch_sets b ON b.id = r.set_id
   SET r.content_fields = JSON_SET(r.content_fields, '$.value_prefix', CAST('"年間"' AS JSON))
 WHERE b.set_code = 'pref-ranking-1' AND r.content_key = '006-coffee-spend';
UPDATE ranking_stock_items r JOIN batch_sets b ON b.id = r.set_id
   SET r.content_fields = JSON_SET(r.content_fields, '$.value_prefix', CAST('"年間"' AS JSON))
 WHERE b.set_code = 'pref-ranking-1' AND r.content_key = '007-tuna-spend';
UPDATE ranking_stock_items r JOIN batch_sets b ON b.id = r.set_id
   SET r.content_fields = JSON_SET(r.content_fields, '$.value_prefix', CAST('"年間"' AS JSON))
 WHERE b.set_code = 'pref-ranking-1' AND r.content_key = '008-cafe-spend';
UPDATE ranking_stock_items r JOIN batch_sets b ON b.id = r.set_id
   SET r.content_fields = JSON_SET(r.content_fields, '$.value_prefix', CAST('null' AS JSON))
 WHERE b.set_code = 'pref-ranking-1' AND r.content_key = '009-onsen-sources';
UPDATE ranking_stock_items r JOIN batch_sets b ON b.id = r.set_id
   SET r.content_fields = JSON_SET(r.content_fields, '$.value_prefix', CAST('null' AS JSON))
 WHERE b.set_code = 'pref-ranking-1' AND r.content_key = '010-fishing-rate';
