-- 2026-10-w3 問題ストック補充投入(14 問。レビュー承認後に実行)
-- 生成元: content/quiz-stock/logic-training-1/2026-10-w3/stock_items.py(単一ソース)。適用先: ローカル MySQL / Aurora(acps)
-- set_id は set_code から解決するため両環境共通で実行できる。
-- content_key はスロット内の既存最大連番 + 1 を適用時に解決する(V007。両環境で同一値になる)。

-- C70
INSERT INTO quiz_stock_items (set_id, content_key, quiz_type, difficulty, question_text, answer_text, content_fields, source_note, is_active)
VALUES ((SELECT id FROM batch_sets WHERE set_code = 'logic-training-1'),
        (SELECT CONCAT('night-', LPAD(COALESCE(MAX(CAST(SUBSTRING_INDEX(t.content_key, '-', -1) AS UNSIGNED)), 0) + 1, 3, '0')) FROM (SELECT q.content_key FROM quiz_stock_items q JOIN batch_sets b ON b.id = q.set_id WHERE b.set_code = 'logic-training-1' AND q.content_key LIKE 'night-%') t),
        'L1', 'deep',
        '春先の朝、庭の芝生に、炭が5個、ニンジンが1本、マフラーが1本落ちていた。きのうまでは、芝生に何も落ちていなかった。なぜ?',
        '雪だるまがとけたから',
        '{"hook":"春の朝のミステリーだ","hint":"季節をさかのぼってみろ!","question":"春先の朝、庭の芝生に、炭が5個、ニンジンが1本、マフラーが1本落ちていた。きのうまでは、芝生に何も落ちていなかった。なぜ?","answer":"雪だるまがとけたから","explanation":"だれかが落としたと考えると行き詰まる。冬に作った雪だるまの目とボタンの炭、鼻のニンジン、首のマフラーが、雪がとけて残ったのだ。","coach_comment":"季節ごと推理したな!","tags":["水平思考","夜の一問","推理"],"summary":"春先の芝生に炭5個・ニンジン・マフラーが落ちていた理由を問う水平思考の定番。答えは雪だるまがとけた。落とし物ではなく、とけて残ったもの。","illustration_scene":"夜、窓の明かりに照らされた家の庭。乾いた緑一色の芝生の上に、ピンポン玉ほどの大きさの黒い炭のかたまりが5個、手のひらほどの長さのニンジンが1本、赤い毛糸のマフラーが1本、ばらばらに落ちている。芝生の上に大きな「?」。人物・「?」以外の文字は描かない。"}',
        '類型: 芝生に石炭・ニンジン・スカーフ=雪だるまがとけた(作者不詳・水平思考の定番)。流布例: https://soma.sbcc.edu/Users/Russotti/118/puzzles/brainteasers.html 。文面はオリジナルに書き下ろし(表現は書き直し済み)。', 1);

-- C71
INSERT INTO quiz_stock_items (set_id, content_key, quiz_type, difficulty, question_text, answer_text, content_fields, source_note, is_active)
VALUES ((SELECT id FROM batch_sets WHERE set_code = 'logic-training-1'),
        (SELECT CONCAT('night-', LPAD(COALESCE(MAX(CAST(SUBSTRING_INDEX(t.content_key, '-', -1) AS UNSIGNED)), 0) + 1, 3, '0')) FROM (SELECT q.content_key FROM quiz_stock_items q JOIN batch_sets b ON b.id = q.set_id WHERE b.set_code = 'logic-training-1' AND q.content_key LIKE 'night-%') t),
        'L1', 'deep',
        '新月の夜に停電して、家じゅう真っ暗。明かりは1つもないのに、男は分厚い本を最後まで読み続けた。なぜ?',
        '目の見えない人で、点字の本を読んでいたから',
        '{"hook":"停電の夜の不思議だ","hint":"読み方は1つじゃないぞ!","question":"新月の夜に停電して、家じゅう真っ暗。明かりは1つもないのに、男は分厚い本を最後まで読み続けた。なぜ?","answer":"目の見えない人で、点字の本を読んでいたから","explanation":"明かりの代わりを探すと行き詰まる。男は目の見えない人で、指先で点字を読んでいた。暗くても読書には何の問題もなかったのだ。","coach_comment":"前提をひっくり返したな!","tags":["水平思考","夜の一問","ひっかけ"],"summary":"新月の夜の停電で真っ暗な家で、明かりもなく分厚い本を最後まで読んだ理由を問う水平思考の定番。答えは目の見えない人が点字の本を読んでいた。","illustration_scene":"夜、停電で真っ暗な部屋。ソファに座った男の後ろ姿の輪郭だけがかすかに見え、その膝の上に分厚い本が開いている。本のページは暗がりで無地に見える。窓の外は真っ黒な夜空。男の頭上に大きな「?」。顔・「?」以外の文字は描かない。"}',
        '類型: 暗い部屋で本を読み続ける男=目の見えない人が点字を読んでいた(作者不詳・水平思考の定番)。流布例: https://www.scienceforums.net/topic/57479-my-questions 。文面はオリジナルに書き下ろし(表現は書き直し済み)。', 1);

-- C72
INSERT INTO quiz_stock_items (set_id, content_key, quiz_type, difficulty, question_text, answer_text, content_fields, source_note, is_active)
VALUES ((SELECT id FROM batch_sets WHERE set_code = 'logic-training-1'),
        (SELECT CONCAT('night-', LPAD(COALESCE(MAX(CAST(SUBSTRING_INDEX(t.content_key, '-', -1) AS UNSIGNED)), 0) + 1, 3, '0')) FROM (SELECT q.content_key FROM quiz_stock_items q JOIN batch_sets b ON b.id = q.set_id WHERE b.set_code = 'logic-training-1' AND q.content_key LIKE 'night-%') t),
        'L1', 'deep',
        '村じゅうの塀に描かれた的は、どれもど真ん中に矢が1本ずつ刺さっている。名人は必ず50m離れて弓で射ていたのに、外れは1本もない。秘密は?',
        '先に矢を射て、あとから矢の周りに的を描いた',
        '{"hook":"百発百中の名人の話だ","hint":"腕前の話とは限らないぞ!","question":"村じゅうの塀に描かれた的は、どれもど真ん中に矢が1本ずつ刺さっている。名人は必ず50m離れて弓で射ていたのに、外れは1本もない。秘密は?","answer":"先に矢を射て、あとから矢の周りに的を描いた","explanation":"腕前の秘密を探すと行き詰まる。名人は50m先の塀に好きなように矢を射てから、刺さった矢を囲むように的を描いていた。外れようがない。","coach_comment":"順番の裏を見抜いたな!","tags":["水平思考","夜の一問","逆転の発想"],"summary":"村じゅうの塀の的すべてのど真ん中に矢が刺さる弓の名人の秘密を問う。ユダヤの寓話(ドゥブノのマギード)の定番。答えは先に射てから的を描いた。","illustration_scene":"夜、ちょうちんの明かりに照らされた村の長い木の塀。塀には赤と白の丸い的がいくつも描かれ、どの的もど真ん中に矢が1本ずつ刺さっている。塀の上の夜空に大きな「?」。人物・「?」以外の文字は描かない。"}',
        '類型: 百発百中の射手=先に射てから的を描いた(18世紀ユダヤの寓話・ドゥブノのマギードとして伝わる)。流布例: https://www.bayesianspectacles.org/origin-of-the-texas-sharpshooter-ii-the-dubner-maggid/ 。文面はオリジナルに書き下ろし(表現は書き直し済み)。', 1);

