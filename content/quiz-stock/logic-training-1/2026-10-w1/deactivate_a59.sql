-- 2026-10-w1 A59(候補 m08 マッチのグラス・morning-055)が動画レビューで完成稿 NG のため出題対象から外す(行は残し is_active=0。両環境共通・再適用しても同じ結果)
UPDATE quiz_stock_items s JOIN batch_sets b ON b.id = s.set_id SET s.is_active = 0 WHERE b.set_code = 'logic-training-1' AND s.content_key = 'morning-055' AND s.question_text LIKE 'マッチ4本で作ったグラスに%';
