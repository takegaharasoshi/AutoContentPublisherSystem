-- 2026-10-w2 動画レビュー(2026-10-12)の再生成 2 回目: 326・327・337 の illustration_scene を再修正
-- 適用先: ローカル MySQL / Aurora(content_key で解決)

-- A62
UPDATE quiz_stock_items q JOIN batch_sets b ON b.id = q.set_id SET q.content_fields = JSON_SET(q.content_fields, '$.illustration_scene', '朝日が差し込む庭先の木のテーブルに、無地の丸い紙が3枚、左から黒・赤・グレーの順に横一列に並ぶ。紙の間には右だけを向いた一方向の矢印が2本(黒→赤、赤→グレー)。グレーの紙の右には何もない。3枚とも塗りつぶしただけの単色。3枚の紙の上の空中、画面上部の中央に大きな「?」。人物・「?」以外の文字は描かない。') WHERE b.set_code = 'logic-training-1' AND q.content_key = 'morning-058';

-- A63
UPDATE quiz_stock_items q JOIN batch_sets b ON b.id = q.set_id SET q.content_fields = JSON_SET(q.content_fields, '$.illustration_scene', '朝日が差し込む教室の黒板に、マッチ棒4本で大きな「+」の形。どの棒も赤い頭は外側の端に1つだけで、内側の端は頭のない平らな木口。左の棒だけが中央を通り越して少し突き出し、上・下・右の3本の平らな木口がその左の棒の側面にぴたりと接している。右に大きな「?」。人物・「?」以外の文字・数字は描かない。') WHERE b.set_code = 'logic-training-1' AND q.content_key = 'morning-059';

-- C67
UPDATE quiz_stock_items q JOIN batch_sets b ON b.id = q.set_id SET q.content_fields = JSON_SET(q.content_fields, '$.illustration_scene', '夜、街灯に照らされた住宅街を少し上から見た絵。一軒家の玄関から手前へまっすぐ出た白い矢印が、道路の上で直角に1回だけ左へ曲がり、そのまま画面の左端までまっすぐ伸びる。矢印の折れ目は1つだけで、ほかに曲がりはない。家の上に大きな「?」。人物・「?」以外の文字は描かない。') WHERE b.set_code = 'logic-training-1' AND q.content_key = 'night-061';
