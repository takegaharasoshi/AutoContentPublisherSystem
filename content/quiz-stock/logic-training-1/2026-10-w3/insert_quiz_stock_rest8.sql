-- 2026-10-w3 問題ストック補充投入(14 問。レビュー承認後に実行)
-- 生成元: content/quiz-stock/logic-training-1/2026-10-w3/stock_items.py(単一ソース)。適用先: ローカル MySQL / Aurora(acps)
-- set_id は set_code から解決するため両環境共通で実行できる。
-- content_key はスロット内の既存最大連番 + 1 を適用時に解決する(V007。両環境で同一値になる)。

-- A72
INSERT INTO quiz_stock_items (set_id, content_key, quiz_type, difficulty, question_text, answer_text, content_fields, source_note, is_active)
VALUES ((SELECT id FROM batch_sets WHERE set_code = 'logic-training-1'),
        (SELECT CONCAT('morning-', LPAD(COALESCE(MAX(CAST(SUBSTRING_INDEX(t.content_key, '-', -1) AS UNSIGNED)), 0) + 1, 3, '0')) FROM (SELECT q.content_key FROM quiz_stock_items q JOIN batch_sets b ON b.id = q.set_id WHERE b.set_code = 'logic-training-1' AND q.content_key LIKE 'morning-%') t),
        'L1', 'light',
        '黒板のアルファベットは、ある決まりで上下2組に分かれている。では「W」は、上と下のどっちの組に入る?',
        '上の組(縦の線で折ると左右対称の文字)',
        '{"hook":"アルファベットの仲間分けだ","hint":"形の特徴を探してみろ!","question":"黒板のアルファベットは、ある決まりで上下2組に分かれている。では「W」は、上と下のどっちの組に入る?","answer":"上の組(縦の線で折ると左右対称の文字)","explanation":"上の組のA・H・I・M・O・Tは、縦の線で半分に折ると左右がぴったり重なる。Wも左右対称なので上の組だ。下の組の文字は左右で形が違う。","coach_comment":"形の決まりを見抜いたな!","tags":["なぞなぞ","朝の一問","法則発見"],"summary":"上の組 A H I M O T・下の組 B C D E K に分かれたアルファベットで、Wはどちらかを問う法則発見。答えは上の組。縦の軸で左右対称の文字。","illustration_scene":"朝日が差し込む教室の黒板に、白いチョークの太く大きなブロック体で2行。上の行に「A H I M O T」、下の行に「B C D E K」、その下に少し離して「W = ?」。文字は等間隔に並べる。右上に大きな「?」。人物・他の文字は描かない。"}',
        '類型: 左右対称のアルファベット(A H I M O T U V W X Y)の仲間分け(学校教材として広く流布)。流布例: https://learn.careers360.com/ncert/question-what-letters-of-the-english-alphabet-have-reflectional-symmetry-that-is-symmetry-related-to-mirror-reflection-about 。文字は問題文に書かず黒板の絵で提示。文面はオリジナルに書き下ろし(表現は書き直し済み)。', 1);

-- A73
INSERT INTO quiz_stock_items (set_id, content_key, quiz_type, difficulty, question_text, answer_text, content_fields, source_note, is_active)
VALUES ((SELECT id FROM batch_sets WHERE set_code = 'logic-training-1'),
        (SELECT CONCAT('morning-', LPAD(COALESCE(MAX(CAST(SUBSTRING_INDEX(t.content_key, '-', -1) AS UNSIGNED)), 0) + 1, 3, '0')) FROM (SELECT q.content_key FROM quiz_stock_items q JOIN batch_sets b ON b.id = q.set_id WHERE b.set_code = 'logic-training-1' AND q.content_key LIKE 'morning-%') t),
        'L1', 'light',
        'どんな人に聞いても、「はい」と答えてもらうことが絶対にできない質問がある。どんな質問だ?',
        '「寝ていますか?」(寝ていたら答えられない)',
        '{"hook":"質問の名人も困る問題だ","hint":"相手の様子を考えてみろ!","question":"どんな人に聞いても、「はい」と答えてもらうことが絶対にできない質問がある。どんな質問だ?","answer":"「寝ていますか?」(寝ていたら答えられない)","explanation":"起きている人は「いいえ」と答え、寝ている人はそもそも答えられない。だから「はい」は返ってこない。ほかにも答えはたくさんあるぞ。探してみろ!","coach_comment":"質問の裏まで読んだな!","tags":["なぞなぞ","朝の一問","発想の転換"],"summary":"誰に聞いても「はい」と答えてもらえない質問を問う英語圏の定番なぞ。答えは「寝ていますか?」。起きていれば「いいえ」、寝ていれば答えられない。","illustration_scene":"朝日が差し込むリビングで、マイクを持った人の後ろ姿が、窓の外の明るい町に向かって立っている。マイクの横に大きな吹き出しと「?」。顔・「?」以外の文字は描かない。"}',
        '類型: 絶対に yes と答えられない質問=「寝ていますか?」(作者不詳・英語圏の定番なぞ)。流布例: https://learnenglishkids.britishcouncil.org/fun-games/riddles/yes 。文面はオリジナルに書き下ろし(表現は書き直し済み)。', 1);

-- A74
INSERT INTO quiz_stock_items (set_id, content_key, quiz_type, difficulty, question_text, answer_text, content_fields, source_note, is_active)
VALUES ((SELECT id FROM batch_sets WHERE set_code = 'logic-training-1'),
        (SELECT CONCAT('morning-', LPAD(COALESCE(MAX(CAST(SUBSTRING_INDEX(t.content_key, '-', -1) AS UNSIGNED)), 0) + 1, 3, '0')) FROM (SELECT q.content_key FROM quiz_stock_items q JOIN batch_sets b ON b.id = q.set_id WHERE b.set_code = 'logic-training-1' AND q.content_key LIKE 'morning-%') t),
        'L1', 'light',
        'カードの式は、ある決まりで答えが決まる。「1=2」「2=5」「4=4」「8=7」。では「0=?」',
        '6(デジタル数字に使う棒の本数)',
        '{"hook":"朝の頭の体操だ!","hint":"数字の形をよく見てみろ!","question":"カードの式は、ある決まりで答えが決まる。「1=2」「2=5」「4=4」「8=7」。では「0=?」","answer":"6(デジタル数字に使う棒の本数)","explanation":"計算では説明がつかない。電卓や時計のデジタル数字の棒を数えると、1は2本、2は5本、4は4本、8は7本。0は6本だ。","coach_comment":"見慣れた形に気づいたな!","tags":["なぞなぞ","朝の一問","法則発見"],"summary":"「1=2」「2=5」「4=4」「8=7」から「0=?」を問う法則発見。答えは6。電卓などのデジタル数字(7セグメント)で使う棒の本数。","illustration_scene":"朝日が差し込む机の上に横長の白いカード。黒い太い手書き風の字で縦に「1=2」「2=5」「4=4」「8=7」「0=?」の5行。数字はふつうの手書きの字形で描く。右上に大きな「?」。人物・他の文字は描かない。"}',
        '類型: デジタル表示(7セグメント)の棒の本数で数を対応させる謎(作者不詳)。流布例: https://linuxfr.org/users/ysabeau/journaux/petite-enigme-pseudo-mathematique-pour-commencer-l-annee-et-en-guise-de-voeux 。字形で本数が揺れる 7・6・9 は使わない(7 は 3 本 / 4 本で揺れるため 2 に替えた・2026-10-21)。文面はオリジナルに書き下ろし(表現は書き直し済み)。', 1);

-- A75
INSERT INTO quiz_stock_items (set_id, content_key, quiz_type, difficulty, question_text, answer_text, content_fields, source_note, is_active)
VALUES ((SELECT id FROM batch_sets WHERE set_code = 'logic-training-1'),
        (SELECT CONCAT('morning-', LPAD(COALESCE(MAX(CAST(SUBSTRING_INDEX(t.content_key, '-', -1) AS UNSIGNED)), 0) + 1, 3, '0')) FROM (SELECT q.content_key FROM quiz_stock_items q JOIN batch_sets b ON b.id = q.set_id WHERE b.set_code = 'logic-training-1' AND q.content_key LIKE 'morning-%') t),
        'L1', 'light',
        '机の上に、マッチ棒で作った「10」がある(1は1本、0は4本の四角)。1本だけ動かして、「1」にしてくれ。',
        '1の棒を0の四角の真ん中に立てる(サイコロの1の目)',
        '{"hook":"最後はひらめき勝負だ","hint":"立体的に考えてみろ!","question":"机の上に、マッチ棒で作った「10」がある(1は1本、0は4本の四角)。1本だけ動かして、「1」にしてくれ。","answer":"1の棒を0の四角の真ん中に立てる(サイコロの1の目)","explanation":"棒を寝かせたままでは「1」は作れない。1の棒を0の四角の真ん中に立てて上から見ると、四角の中に点が1つ。サイコロの1の目になる。","coach_comment":"立てる発想、見事だ!","tags":["なぞなぞ","朝の一問","視覚パズル"],"summary":"マッチ棒の「10」(1は1本・0は4本の四角)を1本動かして「1」にする定番。答えは1の棒を0の中央に立て、上から見てサイコロの1の目にする。","illustration_scene":"朝日が差し込む部屋の木の机を、斜め上から見下ろした奥行きのある立体的な絵。机の上に、厚みと影のある平らな木の角棒のマッチ棒5本が寝かせて置かれ、左に1本、右に4本で作った正方形が並び「10」の形になっている。どの棒も赤い頭は1つ。机の奥に大きな「?」。人物・「?」以外の文字や数字は描かない。"}',
        '類型: マッチ棒の「10」を1本動かして「1」にする=0の真ん中に立ててサイコロの1の目(ひっかけ問題として流布)。流布例: https://blog.nazo2.net/2076/ 、https://www.ragnet.co.jp/matchstick-quiz/5 。文面はオリジナルに書き下ろし(表現は書き直し済み)。', 1);

-- C73
INSERT INTO quiz_stock_items (set_id, content_key, quiz_type, difficulty, question_text, answer_text, content_fields, source_note, is_active)
VALUES ((SELECT id FROM batch_sets WHERE set_code = 'logic-training-1'),
        (SELECT CONCAT('night-', LPAD(COALESCE(MAX(CAST(SUBSTRING_INDEX(t.content_key, '-', -1) AS UNSIGNED)), 0) + 1, 3, '0')) FROM (SELECT q.content_key FROM quiz_stock_items q JOIN batch_sets b ON b.id = q.set_id WHERE b.set_code = 'logic-training-1' AND q.content_key LIKE 'night-%') t),
        'L1', 'deep',
        'ビルの30階で窓をふいていた男が、命綱なしで落ちた。それなのに、かすり傷ひとつない。なぜ?',
        '部屋の内側で窓をふいていて、室内に落ちたから',
        '{"hook":"高層ビルの夜の話だ","hint":"その場所をよく考えてみろ!","question":"ビルの30階で窓をふいていた男が、命綱なしで落ちた。それなのに、かすり傷ひとつない。なぜ?","answer":"部屋の内側で窓をふいていて、室内に落ちたから","explanation":"高い所から落ちたと考えると行き詰まる。男は部屋の内側から窓ガラスをふいていて、踏み台から床へ落ちただけだった。","coach_comment":"思い込みを外したな!","tags":["水平思考","夜の一問","ひっかけ"],"summary":"ビル30階で窓ふき中に命綱なしで落ちても無傷だった理由を問う水平思考の定番。答えは部屋の内側をふいていて室内に落ちた。外だという思い込み。","illustration_scene":"夜の高層ビルを外から見上げた絵。明かりのついた窓がずらりと並び、ビルの上には星の夜空。夜空に大きな「?」。人物・「?」以外の文字は描かない。"}',
        '類型: 高層階から落ちた窓ふきが無傷=室内側をふいていた(作者不詳・水平思考の定番)。流布例: https://www.puzzlesandriddles.com/LateralThinking28.html 。文面はオリジナルに書き下ろし(表現は書き直し済み)。', 1);

-- C74
INSERT INTO quiz_stock_items (set_id, content_key, quiz_type, difficulty, question_text, answer_text, content_fields, source_note, is_active)
VALUES ((SELECT id FROM batch_sets WHERE set_code = 'logic-training-1'),
        (SELECT CONCAT('night-', LPAD(COALESCE(MAX(CAST(SUBSTRING_INDEX(t.content_key, '-', -1) AS UNSIGNED)), 0) + 1, 3, '0')) FROM (SELECT q.content_key FROM quiz_stock_items q JOIN batch_sets b ON b.id = q.set_id WHERE b.set_code = 'logic-training-1' AND q.content_key LIKE 'night-%') t),
        'L1', 'deep',
        '粗末な服で宴会に行った男は相手にされなかった。上等な上着で戻ると大歓迎。すると男は、料理を上着のそでに入れ始めた。なぜ?',
        'もてなされたのは上着だから、上着に食べさせた',
        '{"hook":"宴会で起きた珍事件だ","hint":"主役はだれか考えろ!","question":"粗末な服で宴会に行った男は相手にされなかった。上等な上着で戻ると大歓迎。すると男は、料理を上着のそでに入れ始めた。なぜ?","answer":"もてなされたのは上着だから、上着に食べさせた","explanation":"服を着替えただけで扱いが変わった。歓迎されたのは自分ではなく上着だと皮肉って、男は「さあ食べろ」と上着に料理をふるまったのだ。","coach_comment":"皮肉の意味がわかったな!","tags":["とんち","夜の一問","世界の昔話"],"summary":"粗末な服で相手にされず上等な上着で戻ると歓迎された男が、料理を上着のそでに入れた理由を問う。ナスレッディン・ホジャの昔話。上着に食べさせた。","illustration_scene":"夜、天井の照明で明るい和室の宴会場。座卓にごちそうが並び、上等な刺しゅう入りの羽織を着た男の後ろ姿が、箸でつまんだ料理を羽織の広い袖の中へ入れている。まわりには座って驚く客たちの後ろ姿。座卓の上に大きな「?」。顔・「?」以外の文字は描かない。"}',
        '類型: ナスレッディン・ホジャ「食べろ、上着よ」(国際話型 ATU 1558 Clothes Make the Man)。流布例: https://sites.pitt.edu/~dash/type1558.html 。人名は出さず書き下ろし(表現は書き直し済み)。', 1);

-- C75
INSERT INTO quiz_stock_items (set_id, content_key, quiz_type, difficulty, question_text, answer_text, content_fields, source_note, is_active)
VALUES ((SELECT id FROM batch_sets WHERE set_code = 'logic-training-1'),
        (SELECT CONCAT('night-', LPAD(COALESCE(MAX(CAST(SUBSTRING_INDEX(t.content_key, '-', -1) AS UNSIGNED)), 0) + 1, 3, '0')) FROM (SELECT q.content_key FROM quiz_stock_items q JOIN batch_sets b ON b.id = q.set_id WHERE b.set_code = 'logic-training-1' AND q.content_key LIKE 'night-%') t),
        'L1', 'deep',
        '深くて広い川の向こう岸にいる犬を呼んだ。橋も船もないのに、犬は一度もぬれずに、まっすぐこちらへ来れた。なぜ?',
        '川が凍っていて、氷の上を走ってきたから',
        '{"hook":"冬の川辺のミステリーだ","hint":"川のようすを想像してみろ!","question":"深くて広い川の向こう岸にいる犬を呼んだ。橋も船もないのに、犬は一度もぬれずに、まっすぐこちらへ来れた。なぜ?","answer":"川が凍っていて、氷の上を走ってきたから","explanation":"泳ぎ方や渡り方を考えると行き詰まる。真冬の夜、川は一面凍っていた。犬は氷の上を走ってきたので、一度もぬれなかったのだ。","coach_comment":"季節まで読み切ったな!","tags":["水平思考","夜の一問","ひっかけ"],"summary":"深く広い川の向こう岸の犬が、橋も船もないのにぬれずにまっすぐ来れた理由を問う英語圏の定番なぞ。答えは川が凍っていた。","illustration_scene":"冬の夜、月明かりの川辺。手前の岸から見た深く広い川と、向こう岸にちょこんと座ってこちらを見る犬。川面は波ひとつなく鏡のように平らで、月明かりを白っぽく映している。空に星。川の上に大きな「?」。人物・「?」以外の文字は描かない。"}',
        '類型: 橋も舟もなく、ぬれずに川を渡る犬=川が凍っていた(作者不詳・英語圏の定番なぞ)。流布例: https://www.fatherly.com/entertainment/tricky-hard-riddles-with-answers 。文面はオリジナルに書き下ろし(表現は書き直し済み)。', 1);

-- C76
INSERT INTO quiz_stock_items (set_id, content_key, quiz_type, difficulty, question_text, answer_text, content_fields, source_note, is_active)
VALUES ((SELECT id FROM batch_sets WHERE set_code = 'logic-training-1'),
        (SELECT CONCAT('night-', LPAD(COALESCE(MAX(CAST(SUBSTRING_INDEX(t.content_key, '-', -1) AS UNSIGNED)), 0) + 1, 3, '0')) FROM (SELECT q.content_key FROM quiz_stock_items q JOIN batch_sets b ON b.id = q.set_id WHERE b.set_code = 'logic-training-1' AND q.content_key LIKE 'night-%') t),
        'L1', 'deep',
        'かごに卵が6個入っていた。6人が1個ずつ卵を持っていったのに、かごの中にはまだ卵が1個残っている。なぜ?',
        '最後の人が、卵の入ったかごごと持っていったから',
        '{"hook":"台所で起きた不思議だ","hint":"取り方は1つじゃないぞ!","question":"かごに卵が6個入っていた。6人が1個ずつ卵を持っていったのに、かごの中にはまだ卵が1個残っている。なぜ?","answer":"最後の人が、卵の入ったかごごと持っていったから","explanation":"卵の数を計算すると行き詰まる。5人目までは卵を1個ずつ持っていき、6人目は最後の1個をかごに入れたまま、かごごと持っていった。だから卵はかごの中だ。","coach_comment":"取り方の裏まで読んだな!","tags":["水平思考","夜の一問","ひっかけ"],"summary":"卵6個のかごから6人が1個ずつ持っていったのに、かごに1個残っている理由を問う水平思考の定番。答えは最後の人がかごごと持っていった。","illustration_scene":"夜、天井の明かりに照らされた台所の木のテーブルに、取っ手のついた編みかごが1つ。かごの中に白い卵がちょうど6個入っている。かごの横に大きな「?」。人物・「?」以外の文字は描かない。"}',
        '類型: 卵6個を6人が1個ずつ取ってもかごに1個残る=最後の人がかごごと持っていった(作者不詳・水平思考の定番)。流布例: https://bosburyhistoryresource.org.uk/Puzzles/LTpuzzles/ltpuzzles.html 。文面はオリジナルに書き下ろし(表現は書き直し済み)。', 1);
