-- 2026-10-w2 動画レビュー(2026-10-12)の指摘でイラストの illustration_scene を修正(326・327・329・334・336・337)
-- 適用先: ローカル MySQL / Aurora(content_key で解決)

-- A62
UPDATE quiz_stock_items q JOIN batch_sets b ON b.id = q.set_id SET q.content_fields = JSON_SET(q.content_fields, '$.illustration_scene', '朝日が差し込む庭先の木のテーブルに、無地の丸い紙が3枚、左から黒・赤・グレーの順に横一列に並ぶ。矢印は黒と赤の間、赤とグレーの間の2本だけで、グレーの紙の右には何もない。3枚とも塗りつぶしただけの単色で、中には何も描かれていない。3枚の紙の上の空中、画面上部の中央に大きな「?」。人物・「?」以外の文字は描かない。') WHERE b.set_code = 'logic-training-1' AND q.content_key = 'morning-058';

-- A63
UPDATE quiz_stock_items q JOIN batch_sets b ON b.id = q.set_id SET q.content_fields = JSON_SET(q.content_fields, '$.illustration_scene', '朝日が差し込む教室の黒板に、赤い頭のマッチ棒4本で大きな「+」の形。棒は太さが均一なまっすぐの角棒で、頭と反対の端は平らに切りそろえてある。左の棒だけが中央の交差点を通り越して突き出し、上・下・右の3本の平らな端がその左の棒の先にぴたりと接している。右に大きな「?」。人物・「?」以外の文字・数字は描かない。') WHERE b.set_code = 'logic-training-1' AND q.content_key = 'morning-059';

-- A65
UPDATE quiz_stock_items q JOIN batch_sets b ON b.id = q.set_id SET q.content_fields = JSON_SET(q.content_fields, '$.illustration_scene', '朝日が差し込む玄関の新しい木の扉を正面から見た絵。扉の中央に横長の白いカードが大きく貼ってあり、カードには黒い極太の文字で、カードの幅いっぱいに「NEW DOOR」とだけ書く。文字は画面の横幅の半分以上を占める大きさ。カードの右上に大きな「?」。人物・他の文字は描かない。') WHERE b.set_code = 'logic-training-1' AND q.content_key = 'morning-061';

-- C64
UPDATE quiz_stock_items q JOIN batch_sets b ON b.id = q.set_id SET q.content_fields = JSON_SET(q.content_fields, '$.illustration_scene', '夜、電灯の下のテーブルに、真っ白なクリームだけでなめらかに覆われた丸いホールケーキが1つと包丁が置かれている。ケーキの上面は平らで飾りは何ものっておらず、どこを切っても同じに見える。ケーキはまだ切られていない。ケーキの上に大きな「?」。人物・「?」以外の文字は描かない。') WHERE b.set_code = 'logic-training-1' AND q.content_key = 'night-058';

-- C66
UPDATE quiz_stock_items q JOIN batch_sets b ON b.id = q.set_id SET q.content_fields = JSON_SET(q.content_fields, '$.illustration_scene', '夜、大きく明るい満月を背にした庭の石のテーブル。首の細い背の高い白い水差しが1つだけ立ち、そのふちに黒いカラスが1羽とまって中をのぞいている。カラスは満月の明るい円の前に重なり、羽は青紫のつやで縁取られてくっきり見える。テーブルの上は水差しのほかに何もない。水差しの上に大きな「?」。人物・「?」以外の文字は描かない。') WHERE b.set_code = 'logic-training-1' AND q.content_key = 'night-060';

-- C67
UPDATE quiz_stock_items q JOIN batch_sets b ON b.id = q.set_id SET q.content_fields = JSON_SET(q.content_fields, '$.illustration_scene', '夜、街灯に照らされた住宅街の一軒家。玄関から出た白い矢印の道すじが、まっすぐ進んで1回だけ左へ曲がり、画面の外へ続いている。曲がり角は1つだけ。家の上に大きな「?」。人物・「?」以外の文字は描かない。') WHERE b.set_code = 'logic-training-1' AND q.content_key = 'night-061';
