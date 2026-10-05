-- 2026-10-w1 動画レビューでのイラスト修正: illustration_scene を 1 問更新(A58 = morning-054。1 を縦棒 1 本・6 と 9 を 180 度対称に)。set_code + question_text で解決(ローカル / Aurora 共通・再適用しても同じ結果)
-- A58
UPDATE quiz_stock_items s JOIN batch_sets b ON b.id = s.set_id SET s.content_fields = JSON_SET(s.content_fields, '$.illustration_scene', '朝日が差し込む木の机の上に白い紙が1枚。紙には黒い太字で大きく「1961」とだけ書かれている。2つの1は、上下のひげも左上のはねもない、ただの縦棒1本にする。6と9は、180度回すとちょうど重なる同じ形にする。紙の横に、くるりと回る矢印と大きな「?」。他の文字・数字・人物は描かない。') WHERE b.set_code = 'logic-training-1' AND s.question_text = '1961年は、紙を逆さにしても「1961」と読める年だった。次にそうなる年は、西暦何年?';
