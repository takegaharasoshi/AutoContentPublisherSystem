-- 2026-10-w2 G2: イラスト生成で答えの物が描かれた 3 問の illustration_scene を修正(描かない物の名前を外し、描く物だけを書く)
-- 適用先: ローカル MySQL / Aurora(content_key で解決)

-- A62
UPDATE quiz_stock_items q JOIN batch_sets b ON b.id = q.set_id SET q.content_fields = JSON_SET(q.content_fields, '$.illustration_scene', '朝日が差し込む庭先の木のテーブルに、無地の丸い紙が3枚、左から黒・赤・グレーの順に並び、矢印でつながっている。3枚とも塗りつぶしただけの単色で、中には何も描かれていない。右端に大きな「?」。テーブルの上には紙と矢印と「?」だけがある。人物・「?」以外の文字は描かない。') WHERE b.set_code = 'logic-training-1' AND q.content_key = 'morning-058';

-- A66
UPDATE quiz_stock_items q JOIN batch_sets b ON b.id = q.set_id SET q.content_fields = JSON_SET(q.content_fields, '$.illustration_scene', '朝日が差し込む野原に立つ木の物置を正面から見た絵。扉が大きく開いていて、中の棚はすべて空っぽ。棚の前に大きな「?」がある。物置のまわりは草と花だけ。人物・「?」以外の文字は描かない。') WHERE b.set_code = 'logic-training-1' AND q.content_key = 'morning-062';

-- C66
UPDATE quiz_stock_items q JOIN batch_sets b ON b.id = q.set_id SET q.content_fields = JSON_SET(q.content_fields, '$.illustration_scene', '夜、月明かりの庭の石のテーブルに、首の細い背の高い水差しが1つだけ立ち、そのふちに黒いカラスが1羽とまって中をのぞいている。テーブルの上は水差しのほかに何もなく、つるりとしている。水差しの上に大きな「?」。人物・「?」以外の文字は描かない。') WHERE b.set_code = 'logic-training-1' AND q.content_key = 'night-060';
