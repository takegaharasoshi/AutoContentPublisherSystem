-- 2026-09-w4 動画レビューでのヒント修正: A47 の hint を「駐車をする際の視点を考えよう」へ(後ろ向き駐車の絵に合わせる。ユーザー指定文)。set_code + question_text で解決(ローカル / Aurora 共通)
UPDATE quiz_stock_items s JOIN batch_sets b ON b.id = s.set_id SET s.content_fields = JSON_SET(s.content_fields, '$.hint', '駐車をする際の視点を考えよう') WHERE b.set_code = 'logic-training-1' AND s.question_text = '上から見た駐車場の絵だ。マスの番号には、ある決まりがある。車が止まっている「?」のマスは何番?';
