-- 2026-10-w2 問題ストック補充投入(14 問。レビュー承認後に実行)
-- 生成元: content/quiz-stock/logic-training-1/2026-10-w2/stock_items.py(単一ソース)。適用先: ローカル MySQL / Aurora(acps)
-- set_id は set_code から解決するため両環境共通で実行できる。
-- content_key はスロット内の既存最大連番 + 1 を適用時に解決する(V007。両環境で同一値になる)。

-- A62
INSERT INTO quiz_stock_items (set_id, content_key, quiz_type, difficulty, question_text, answer_text, content_fields, source_note, is_active)
VALUES ((SELECT id FROM batch_sets WHERE set_code = 'logic-training-1'),
        (SELECT CONCAT('morning-', LPAD(COALESCE(MAX(CAST(SUBSTRING_INDEX(t.content_key, '-', -1) AS UNSIGNED)), 0) + 1, 3, '0')) FROM (SELECT q.content_key FROM quiz_stock_items q JOIN batch_sets b ON b.id = q.set_id WHERE b.set_code = 'logic-training-1' AND q.content_key LIKE 'morning-%') t),
        'L1', 'light',
        'お店で買うときは黒。使っているあいだは赤。捨てるときは白っぽいグレー。1つの物なのに、色が3回も変わる。それはなんだ?',
        '炭(木炭。燃えると赤、燃え尽きると灰)',
        '{"hook":"色が3回も変わるらしいぞ","hint":"使い道を思い浮かべてみろ!","question":"お店で買うときは黒。使っているあいだは赤。捨てるときは白っぽいグレー。1つの物なのに、色が3回も変わる。それはなんだ?","answer":"炭(木炭。燃えると赤、燃え尽きると灰)","explanation":"炭は買ったときは黒い。火がつくと赤く光り、燃え尽きると白っぽい灰になって捨てられる。使う順に色が変わる物を探すのが鍵だ。","coach_comment":"流れで考えたな、見事だ!","tags":["なぞなぞ","朝の一問","状態の変化"],"summary":"買うと黒・使うと赤・捨てるとグレーと色が3回変わる物は何かを問う英語圏の古典なぞ。答えは炭(木炭)。使う順に色が変わる。","illustration_scene":"朝日が差し込む庭先の木のテーブルに、無地の丸い紙が3枚、左から黒・赤・グレーの順に横一列に並ぶ。紙の間には右だけを向いた一方向の矢印が2本(黒→赤、赤→グレー)。グレーの紙の右には何もない。3枚とも塗りつぶしただけの単色。3枚の紙の上の空中、画面上部の中央に大きな「?」。人物・「?」以外の文字は描かない。"}',
        '類型: 買うと黒・使うと赤・捨てると灰色=炭の古典なぞ(作者不詳・英語圏に流布。What is black when you buy it, red when you use it, and grey when you throw it away?)。流布例: https://folklore.usc.edu/?p=4557 。文面はオリジナルに書き下ろし(表現は書き直し済み)。', 1);

-- A63
INSERT INTO quiz_stock_items (set_id, content_key, quiz_type, difficulty, question_text, answer_text, content_fields, source_note, is_active)
VALUES ((SELECT id FROM batch_sets WHERE set_code = 'logic-training-1'),
        (SELECT CONCAT('morning-', LPAD(COALESCE(MAX(CAST(SUBSTRING_INDEX(t.content_key, '-', -1) AS UNSIGNED)), 0) + 1, 3, '0')) FROM (SELECT q.content_key FROM quiz_stock_items q JOIN batch_sets b ON b.id = q.set_id WHERE b.set_code = 'logic-training-1' AND q.content_key LIKE 'morning-%') t),
        'L1', 'light',
        'マッチ棒を1本だけ動かして、正方形を作ってくれ。棒を折ったり重ねたりしてはいけない。',
        '1本を少し外へずらし、中央に小さな正方形を作る',
        '{"hook":"マッチ棒4本の頭の体操だ","hint":"正方形の大きさは自由だぞ!","question":"マッチ棒を1本だけ動かして、正方形を作ってくれ。棒を折ったり重ねたりしてはいけない。","answer":"1本を少し外へずらし、中央に小さな正方形を作る","explanation":"1本を外側へ少しずらすと、4本の端に囲まれた中央のすきまが小さな正方形になる。大きな正方形を作ろうとすると、棒が足りずに行き詰まる。","coach_comment":"すきまに目をつけたな!","tags":["なぞなぞ","朝の一問","視覚パズル"],"summary":"マッチ棒4本の十字から1本だけ動かして正方形を作る定番パズル。1本を外へ少しずらし、中央のすきまを小さな正方形にする。十字は黒板の絵で提示。","illustration_scene":"朝日が差し込む教室の黒板に、マッチ棒4本で大きな「+」の形。どの棒も赤い頭は外側の端に1つだけで、内側の端は頭のない平らな木口。左の棒だけが中央を通り越して少し突き出し、上・下・右の3本の平らな木口がその左の棒の側面にぴたりと接している。右に大きな「?」。人物・「?」以外の文字・数字は描かない。"}',
        '類型: マッチ棒4本の十字を1本動かして正方形にする定番(作者不詳・英語圏に流布。plus sign to square)。流布例: https://www.geeksforgeeks.org/puzzles/puzzle-4-matchstick-problem/ , https://blog.tanyakhovanova.com/?p=2108 。十字は問題文に書かず黒板の絵で提示。文面はオリジナルに書き下ろし(表現は書き直し済み)。', 1);

-- A64
INSERT INTO quiz_stock_items (set_id, content_key, quiz_type, difficulty, question_text, answer_text, content_fields, source_note, is_active)
VALUES ((SELECT id FROM batch_sets WHERE set_code = 'logic-training-1'),
        (SELECT CONCAT('morning-', LPAD(COALESCE(MAX(CAST(SUBSTRING_INDEX(t.content_key, '-', -1) AS UNSIGNED)), 0) + 1, 3, '0')) FROM (SELECT q.content_key FROM quiz_stock_items q JOIN batch_sets b ON b.id = q.set_id WHERE b.set_code = 'logic-training-1' AND q.content_key LIKE 'morning-%') t),
        'L1', 'light',
        '進めば進むほど、うしろにどんどん置いていく。でも、拾って持ち帰ることはできない。それはなんだ?',
        '足あと',
        '{"hook":"持ち帰れない落とし物だ","hint":"置いていくのは物とは限らないぞ!","question":"進めば進むほど、うしろにどんどん置いていく。でも、拾って持ち帰ることはできない。それはなんだ?","answer":"足あと","explanation":"歩けば歩くほど、うしろには足あとが増えていく。置いていくのに拾えない。「置いていく」を落とし物の話だと思うと迷う。","coach_comment":"振り返る目、見事だった!","tags":["なぞなぞ","朝の一問","言葉あそび"],"summary":"進むほど後ろに置いていくのに拾えないものは何かを問う英語圏の古典なぞ。答えは足あと。置いていく=落とし物と思わせる。","illustration_scene":"朝日が差し込む公園の木のベンチに、だれかの忘れ物の青い帽子が1つぽつんと置かれ、ベンチの上に大きな「?」がある。地面は短い芝生。人物・足あと・動物・「?」以外の文字は描かない。"}',
        '類型: 進むほど後ろに残す=足あとの古典なぞ(作者不詳・英語圏に流布。The more you take, the more you leave behind)。流布例: https://blogs.tpl.ca/word-out-2013/2013/06/riddle-contest-june-29-july-5/ 。文面はオリジナルに書き下ろし(表現は書き直し済み)。', 1);

-- A65
INSERT INTO quiz_stock_items (set_id, content_key, quiz_type, difficulty, question_text, answer_text, content_fields, source_note, is_active)
VALUES ((SELECT id FROM batch_sets WHERE set_code = 'logic-training-1'),
        (SELECT CONCAT('morning-', LPAD(COALESCE(MAX(CAST(SUBSTRING_INDEX(t.content_key, '-', -1) AS UNSIGNED)), 0) + 1, 3, '0')) FROM (SELECT q.content_key FROM quiz_stock_items q JOIN batch_sets b ON b.id = q.set_id WHERE b.set_code = 'logic-training-1' AND q.content_key LIKE 'morning-%') t),
        'L1', 'light',
        'カードの7文字を全部使って並べ替え、ひとつの単語にしてくれ。',
        'ONE WORD(そのまま「ひとつの単語」)',
        '{"hook":"英語が苦手でも解けるぞ","hint":"「ひとつの単語」という言葉に注目だ","question":"カードの7文字を全部使って並べ替え、ひとつの単語にしてくれ。","answer":"ONE WORD(そのまま「ひとつの単語」)","explanation":"NEW DOORの7文字を並べ替えるとONE WORD。英単語を探すと行き詰まるが、答えは問題が求めた「ひとつの単語」を英語にした言葉そのものだった。","coach_comment":"問題文ごと解いたな!","tags":["なぞなぞ","朝の一問","言葉あそび"],"summary":"カードのNEW DOORを並べ替えてひとつの単語にせよという英語圏の定番。答えはONE WORD。指示文そのものが答え。文字はカードの絵で提示。","illustration_scene":"朝日が差し込む玄関の新しい木の扉を正面から見た絵。扉の中央に横長の白いカードが大きく貼ってあり、カードには黒い極太の文字で、カードの幅いっぱいに「NEW DOOR」とだけ書く。文字は画面の横幅の半分以上を占める大きさ。カードの右上に大きな「?」。人物・他の文字は描かない。"}',
        '類型: NEW DOOR を並べ替えて one word にする定番(作者不詳・英語圏に流布)。流布例: https://waywordradio.org/new-door-word-puzzle/ 。文字は問題文に書かずカードの絵で提示。文面はオリジナルに書き下ろし(表現は書き直し済み)。', 1);

-- A66
INSERT INTO quiz_stock_items (set_id, content_key, quiz_type, difficulty, question_text, answer_text, content_fields, source_note, is_active)
VALUES ((SELECT id FROM batch_sets WHERE set_code = 'logic-training-1'),
        (SELECT CONCAT('morning-', LPAD(COALESCE(MAX(CAST(SUBSTRING_INDEX(t.content_key, '-', -1) AS UNSIGNED)), 0) + 1, 3, '0')) FROM (SELECT q.content_key FROM quiz_stock_items q JOIN batch_sets b ON b.id = q.set_id WHERE b.set_code = 'logic-training-1' AND q.content_key LIKE 'morning-%') t),
        'L1', 'light',
        '使いたいときには外へ放り投げ、使わないときには中へしまいこむ。それはなんだ?',
        'いかり(船の錨)',
        '{"hook":"捨てるのとは違うらしいぞ","hint":"投げる=手放す、とは限らないぞ!","question":"使いたいときには外へ放り投げ、使わないときには中へしまいこむ。それはなんだ?","answer":"いかり(船の錨)","explanation":"船を止めたいときは錨を海へ投げ入れ、出発するときは船の中へ引き上げる。投げる=手放すと思うと迷うが、錨は投げてこそ働く道具だ。","coach_comment":"投げて使う発想、見事だ!","tags":["なぞなぞ","朝の一問","逆転の発想"],"summary":"使いたいときは外へ投げ、使わないときは中へしまうものは何かを問う英語圏の古典なぞ。答えは船の錨。投げる=手放すの思い込みを裏切る。","illustration_scene":"朝日が差し込む野原に立つ木の物置を正面から見た絵。扉が大きく開いていて、中の棚はすべて空っぽ。棚の前に大きな「?」がある。物置のまわりは草と花だけ。人物・「?」以外の文字は描かない。"}',
        '類型: 使うときは投げ、使わないときはしまう=錨の古典なぞ(作者不詳・英語圏に流布。What do you throw out when you want to use it…? An anchor)。流布例: https://blocs.xtec.cat/annalozano/category/riddles/ 。文面はオリジナルに書き下ろし(表現は書き直し済み)。', 1);

-- A67
INSERT INTO quiz_stock_items (set_id, content_key, quiz_type, difficulty, question_text, answer_text, content_fields, source_note, is_active)
VALUES ((SELECT id FROM batch_sets WHERE set_code = 'logic-training-1'),
        (SELECT CONCAT('morning-', LPAD(COALESCE(MAX(CAST(SUBSTRING_INDEX(t.content_key, '-', -1) AS UNSIGNED)), 0) + 1, 3, '0')) FROM (SELECT q.content_key FROM quiz_stock_items q JOIN batch_sets b ON b.id = q.set_id WHERE b.set_code = 'logic-training-1' AND q.content_key LIKE 'morning-%') t),
        'L1', 'light',
        '座ったまま右足を時計回りにくるくる回す。回し続けながら、右手の指で空中に数字の6を書いてみてくれ。足はどうなる?',
        '勝手に逆回り(反時計回り)になってしまう',
        '{"hook":"1分でできる体の実験だ","hint":"やってみれば分かる、試せ!","question":"座ったまま右足を時計回りにくるくる回す。回し続けながら、右手の指で空中に数字の6を書いてみてくれ。足はどうなる?","answer":"勝手に逆回り(反時計回り)になってしまう","explanation":"6を書く手の動きは反時計回り。同じ側の手足に逆向きの回転を同時にさせるのは難しく、足が手につられて逆回りになる。止められる人はまれだ。","coach_comment":"体で確かめた答えは強いぞ!","tags":["なぞなぞ","朝の一問","参加型"],"summary":"座って右足を時計回りに回しながら右手で空中に6を書くと、足が勝手に逆回りになる体のふしぎ。視聴者がその場で試せる参加型。","illustration_scene":"朝日が差し込むリビングで、木の椅子に座った人の斜め後ろ姿。右足を少し前へ浮かせ、足先のまわりに時計回りの丸い矢印が描かれている。右手は人差し指を立てて顔の横の空中に上げ、指先から短い点線が出て、空中に字を書き始めたところ。頭上に大きな「?」。顔・数字・「?」以外の文字は描かない。"}',
        '類型: 右足を時計回りに回しながら右手で6を書くと足が逆回りになる体のふしぎ(作者不詳・英語圏に流布)。流布例: https://boards.straightdope.com/t/right-foot-and-6/230262 。文面はオリジナルに書き下ろし(表現は書き直し済み)。', 1);

-- A68
INSERT INTO quiz_stock_items (set_id, content_key, quiz_type, difficulty, question_text, answer_text, content_fields, source_note, is_active)
VALUES ((SELECT id FROM batch_sets WHERE set_code = 'logic-training-1'),
        (SELECT CONCAT('morning-', LPAD(COALESCE(MAX(CAST(SUBSTRING_INDEX(t.content_key, '-', -1) AS UNSIGNED)), 0) + 1, 3, '0')) FROM (SELECT q.content_key FROM quiz_stock_items q JOIN batch_sets b ON b.id = q.set_id WHERE b.set_code = 'logic-training-1' AND q.content_key LIKE 'morning-%') t),
        'L1', 'light',
        'カードの文のまちがいを3つ、全部見つけてくれ。',
        '分→文・わ→は、3つ目は「三つ」という数',
        '{"hook":"国語のテストの時間だ","hint":"字だけがまちがいとは限らないぞ!","question":"カードの文のまちがいを3つ、全部見つけてくれ。","answer":"分→文・わ→は、3つ目は「三つ」という数","explanation":"字のまちがいは「分章」と「にわ」の2つだけ。だから「三つある」という文の言い分そのものが3つ目のまちがいになる。文を外から見られるかが勝負だ。","coach_comment":"一段上から見たな、見事!","tags":["なぞなぞ","朝の一問","言葉あそび"],"summary":"「この分章にわ、まちがいが三つあります。」の誤りを3つ探す自己言及の定番。字の誤りは2つで、3つ目は「三つ」という主張そのもの。文はカードの絵で提示。","illustration_scene":"朝日が差し込む机の上に、横長の白いカードが1枚。カードには黒い字で大きく一字一句「この分章にわ、まちがいが三つあります。」とだけ書く。カードの横に赤ペンと大きな「?」。人物・他の文字は描かない。"}',
        '類型: 「この文にはまちがいが三つある」の自己言及ジョーク(作者不詳・英語圏に流布。Their are three erors in this sentence)。流布例: https://geoff-hart.com/home/whyedit-1.html 。日本語の文は書き下ろし。文はカードの絵で提示。文面はオリジナルに書き下ろし(表現は書き直し済み)。', 1);

-- C63
INSERT INTO quiz_stock_items (set_id, content_key, quiz_type, difficulty, question_text, answer_text, content_fields, source_note, is_active)
VALUES ((SELECT id FROM batch_sets WHERE set_code = 'logic-training-1'),
        (SELECT CONCAT('night-', LPAD(COALESCE(MAX(CAST(SUBSTRING_INDEX(t.content_key, '-', -1) AS UNSIGNED)), 0) + 1, 3, '0')) FROM (SELECT q.content_key FROM quiz_stock_items q JOIN batch_sets b ON b.id = q.set_id WHERE b.set_code = 'logic-training-1' AND q.content_key LIKE 'night-%') t),
        'L1', 'deep',
        '古い金貨を見つけた男が叫んだ。「表に『紀元前50年』と刻んである、大発見だ!」。専門家はひと目で偽物だと見抜いた。なぜ?',
        '紀元前の人は「紀元前」と刻めないから',
        '{"hook":"歴史好きほどだまされる","hint":"刻まれた言葉をよく読んでみろ!","question":"古い金貨を見つけた男が叫んだ。「表に『紀元前50年』と刻んである、大発見だ!」。専門家はひと目で偽物だと見抜いた。なぜ?","answer":"紀元前の人は「紀元前」と刻めないから","explanation":"「紀元前」は、紀元が始まった後の人が過去を数える呼び方。紀元前50年の人は、あと何年で紀元が始まるか知らない。そう刻んだ金貨は後世の作り物だ。","coach_comment":"時間の向きを見抜いたな!","tags":["水平思考","夜の一問","思い込み"],"summary":"「紀元前50年」と刻んだ古い金貨が偽物と見抜かれた理由を問う水平思考の古典。紀元前の人は紀元前と刻めない。年号が後世の数え方だと気づかせる。","illustration_scene":"夜、ランプの明かりだけの書斎。机の上に古びた金貨が1枚と大きな虫めがねが置かれ、金貨の上に大きな「?」がある。金貨の表面は模様だけで、文字・数字は描かない。人物・「?」以外の文字は描かない。"}',
        '類型: 「紀元前」と刻んだ金貨は偽物という水平思考の古典(作者不詳・英語圏に流布。coin dated B.C.)。流布例: https://einsteinathome.org/content/numb3rs-just-fun?page=3 。文面はオリジナルに書き下ろし(表現は書き直し済み)。', 1);

-- C64
INSERT INTO quiz_stock_items (set_id, content_key, quiz_type, difficulty, question_text, answer_text, content_fields, source_note, is_active)
VALUES ((SELECT id FROM batch_sets WHERE set_code = 'logic-training-1'),
        (SELECT CONCAT('night-', LPAD(COALESCE(MAX(CAST(SUBSTRING_INDEX(t.content_key, '-', -1) AS UNSIGNED)), 0) + 1, 3, '0')) FROM (SELECT q.content_key FROM quiz_stock_items q JOIN batch_sets b ON b.id = q.set_id WHERE b.set_code = 'logic-training-1' AND q.content_key LIKE 'night-%') t),
        'L1', 'deep',
        '丸いケーキを、包丁でまっすぐ3回だけ切って、同じ大きさの8切れにしたい。切ったケーキを動かしてはいけない。どう切る?',
        '十字に2回、最後に横から厚みを半分に切る',
        '{"hook":"誕生日の夜に役立つぞ","hint":"ケーキの形をよく見てみろ!","question":"丸いケーキを、包丁でまっすぐ3回だけ切って、同じ大きさの8切れにしたい。切ったケーキを動かしてはいけない。どう切る?","answer":"十字に2回、最後に横から厚みを半分に切る","explanation":"上から十字に切ると4切れ。最後の1回を横から入れて、ケーキの厚みを上下半分に分ければ8切れになる。上から切ることしか考えないと解けない。","coach_comment":"立体で考えられたな!","tags":["水平思考","夜の一問","立体の発想"],"summary":"丸いケーキを包丁で3回だけまっすぐ切って同じ大きさの8切れにする古典パズル。十字に2回、横から厚みを半分に1回。上から切る思い込みを外す。","illustration_scene":"夜、電灯の下のテーブルに、真っ白なクリームだけでなめらかに覆われた丸いホールケーキが1つと包丁が置かれている。ケーキの上面は平らで飾りは何ものっておらず、どこを切っても同じに見える。ケーキはまだ切られていない。ケーキの上に大きな「?」。人物・「?」以外の文字は描かない。"}',
        '類型: 3回の切断でケーキを8等分する古典パズル(作者不詳・英語圏に流布)。流布例: https://www.cut-the-knot.org/htdocs/dcforum/DCForumID4/643.shtml 。重ねて切る別解は「動かしてはいけない」で塞いだ。文面はオリジナルに書き下ろし(表現は書き直し済み)。', 1);

-- C65
INSERT INTO quiz_stock_items (set_id, content_key, quiz_type, difficulty, question_text, answer_text, content_fields, source_note, is_active)
VALUES ((SELECT id FROM batch_sets WHERE set_code = 'logic-training-1'),
        (SELECT CONCAT('night-', LPAD(COALESCE(MAX(CAST(SUBSTRING_INDEX(t.content_key, '-', -1) AS UNSIGNED)), 0) + 1, 3, '0')) FROM (SELECT q.content_key FROM quiz_stock_items q JOIN batch_sets b ON b.id = q.set_id WHERE b.set_code = 'logic-training-1' AND q.content_key LIKE 'night-%') t),
        'L1', 'deep',
        '男は大雨の中を、傘も帽子もなしで1時間歩いた。服はびしょぬれなのに、髪の毛は1本もぬれなかった。なぜ?',
        '髪の毛が1本もなかった(スキンヘッドだった)',
        '{"hook":"傘を忘れた夜の話だ","hint":"当たり前を1つ疑ってみろ!","question":"男は大雨の中を、傘も帽子もなしで1時間歩いた。服はびしょぬれなのに、髪の毛は1本もぬれなかった。なぜ?","answer":"髪の毛が1本もなかった(スキンヘッドだった)","explanation":"ぬれなかった理由を道具や場所に探すと行き詰まる。男の頭には、そもそもぬれる髪の毛が1本もなかった。「髪がある」という前提を疑えたかが勝負だ。","coach_comment":"前提を疑えたな、見事!","tags":["水平思考","夜の一問","ひっかけ"],"summary":"大雨の中を傘も帽子もなしで歩いたのに髪が1本もぬれなかった理由を問う英語圏の定番ひっかけ。髪がなかった。髪があるという前提を外す。","illustration_scene":"夜、街灯に照らされた大雨の石畳の通り。色とりどりの傘を差した大勢の人が行き交い、みんな後ろ姿か遠景で描かれている。通りの上に大きな「?」。顔・帽子・「?」以外の文字は描かない。"}',
        '類型: 雨の中で髪がぬれなかった=はげていたの定番ひっかけ(作者不詳・英語圏に流布)。流布例: https://www.lessonup.com/en/lesson/nxRXiZDMyR4QvuEZW 。文面はオリジナルに書き下ろし(表現は書き直し済み)。', 1);

-- C66
INSERT INTO quiz_stock_items (set_id, content_key, quiz_type, difficulty, question_text, answer_text, content_fields, source_note, is_active)
VALUES ((SELECT id FROM batch_sets WHERE set_code = 'logic-training-1'),
        (SELECT CONCAT('night-', LPAD(COALESCE(MAX(CAST(SUBSTRING_INDEX(t.content_key, '-', -1) AS UNSIGNED)), 0) + 1, 3, '0')) FROM (SELECT q.content_key FROM quiz_stock_items q JOIN batch_sets b ON b.id = q.set_id WHERE b.set_code = 'logic-training-1' AND q.content_key LIKE 'night-%') t),
        'L1', 'deep',
        'のどがかわいたカラス。細い水差しの底に少しだけ水があるが、くちばしが届かない。水差しは重くて倒れない。どうする?',
        '小石を何個も入れて、水面を上げて飲む',
        '{"hook":"カラスはかなり賢いらしいぞ","hint":"カラスになったつもりで、まわりを見ろ!","question":"のどがかわいたカラス。細い水差しの底に少しだけ水があるが、くちばしが届かない。水差しは重くて倒れない。どうする?","answer":"小石を何個も入れて、水面を上げて飲む","explanation":"くちばしを水へ近づけられないなら、水をくちばしへ近づければいい。小石を1つずつ落とすと、そのぶん水面が上がって届く。イソップの寓話の知恵だ。","coach_comment":"発想の向きを変えたな!","tags":["水平思考","夜の一問","逆転の発想"],"summary":"細い水差しの底の水にくちばしが届かないカラスがどうするかを問う。小石を入れて水面を上げる。イソップ『カラスと水差し』が原形。","illustration_scene":"夜、大きく明るい満月を背にした庭の石のテーブル。首の細い背の高い白い水差しが1つだけ立ち、そのふちに黒いカラスが1羽とまって中をのぞいている。カラスは満月の明るい円の前に重なり、羽は青紫のつやで縁取られてくっきり見える。テーブルの上は水差しのほかに何もない。水差しの上に大きな「?」。人物・「?」以外の文字は描かない。"}',
        '類型: イソップ寓話『カラスと水差し』(作者不詳の古典)。流布例: https://www.read.gov/aesop/012.html 。問いの形は書き下ろし。文面はオリジナルに書き下ろし(表現は書き直し済み)。', 1);

-- C67
INSERT INTO quiz_stock_items (set_id, content_key, quiz_type, difficulty, question_text, answer_text, content_fields, source_note, is_active)
VALUES ((SELECT id FROM batch_sets WHERE set_code = 'logic-training-1'),
        (SELECT CONCAT('night-', LPAD(COALESCE(MAX(CAST(SUBSTRING_INDEX(t.content_key, '-', -1) AS UNSIGNED)), 0) + 1, 3, '0')) FROM (SELECT q.content_key FROM quiz_stock_items q JOIN batch_sets b ON b.id = q.set_id WHERE b.set_code = 'logic-training-1' AND q.content_key LIKE 'night-%') t),
        'L1', 'deep',
        '男は家を出て、左へ3回曲がって、また家に戻ってきた。家ではマスクをした男が2人待っていた。何が起きている?',
        '野球。走者がホームに戻り、捕手と審判が待つ',
        '{"hook":"夏の夜にぴったりの一問","hint":"「家」は1種類だけか?","question":"男は家を出て、左へ3回曲がって、また家に戻ってきた。家ではマスクをした男が2人待っていた。何が起きている?","answer":"野球。走者がホームに戻り、捕手と審判が待つ","explanation":"家は野球のホームベース。走者は一塁・二塁・三塁と左へ3回曲がって本塁へ戻る。そこでマスクをつけて待つのは捕手と球審だ。","coach_comment":"「家」を読み替えたな!","tags":["水平思考","夜の一問","言葉あそび"],"summary":"家を出て左へ3回曲がって戻るとマスクの男2人が待っていた状況を問う水平思考の定番。野球の走者が本塁へ戻り、捕手と球審が待つ。","illustration_scene":"夜、街灯に照らされた住宅街を少し上から見た絵。一軒家の玄関から手前へまっすぐ出た白い矢印が、道路の上で直角に1回だけ左へ曲がり、そのまま画面の左端までまっすぐ伸びる。矢印の折れ目は1つだけで、ほかに曲がりはない。家の上に大きな「?」。人物・「?」以外の文字は描かない。"}',
        '類型: 左へ3回曲がって家へ戻るとマスクの男が待つ=野球の水平思考の定番(作者不詳・英語圏に流布)。流布例: https://boards.straightdope.com/t/solve-this-riddle/213508?page=3 。文面はオリジナルに書き下ろし(表現は書き直し済み)。', 1);

-- C68
INSERT INTO quiz_stock_items (set_id, content_key, quiz_type, difficulty, question_text, answer_text, content_fields, source_note, is_active)
VALUES ((SELECT id FROM batch_sets WHERE set_code = 'logic-training-1'),
        (SELECT CONCAT('night-', LPAD(COALESCE(MAX(CAST(SUBSTRING_INDEX(t.content_key, '-', -1) AS UNSIGNED)), 0) + 1, 3, '0')) FROM (SELECT q.content_key FROM quiz_stock_items q JOIN batch_sets b ON b.id = q.set_id WHERE b.set_code = 'logic-training-1' AND q.content_key LIKE 'night-%') t),
        'L1', 'deep',
        '国境の橋は渡りきるのに8分。国の側の見張りは5分ごとに橋を見て、出ていく者は国へ、入ってくる者は向こう岸まで追い返す。通行証のない男は、どうやって国を出た?',
        '5分近く歩いて向きを変え、入国者に見せて追い返させた',
        '{"hook":"国境越えの頭脳戦だ","hint":"見張りの決まりをよく読め!","question":"国境の橋は渡りきるのに8分。国の側の見張りは5分ごとに橋を見て、出ていく者は国へ、入ってくる者は向こう岸まで追い返す。通行証のない男は、どうやって国を出た?","answer":"5分近く歩いて向きを変え、入国者に見せて追い返させた","explanation":"見張りが目を離した直後に渡り始め、5分近く進んだら国の方へ向き直る。見張りには国へ入る者に見え、向こう岸まで追い返されて国を出られる。","coach_comment":"決まりの裏をかいたな!","tags":["水平思考","夜の一問","逆転の発想"],"summary":"渡るのに8分、見張りが5分ごとに出る者を国へ・入る者を向こう岸へ追い返す橋を、通行証なしで出国する方法を問う定番。5分近く歩いて向きを変え、追い返させる。","illustration_scene":"夜の川にかかる長い木の橋を遠くから見た絵。手前の門のそばに見張り小屋の窓明かり、橋の向こうは暗い森。橋の上に大きな「?」。人物・時計・数字・「?」以外の文字は描かない。"}',
        '類型: 見張りの決まりを逆手に取って橋を渡る定番の水平思考(作者不詳・英語圏の面接パズル集に流布。best time to escape)。流布例: https://www.geeksforgeeks.org/?p=218086 。文面はオリジナルに書き下ろし(表現は書き直し済み)。', 1);

-- C69
INSERT INTO quiz_stock_items (set_id, content_key, quiz_type, difficulty, question_text, answer_text, content_fields, source_note, is_active)
VALUES ((SELECT id FROM batch_sets WHERE set_code = 'logic-training-1'),
        (SELECT CONCAT('night-', LPAD(COALESCE(MAX(CAST(SUBSTRING_INDEX(t.content_key, '-', -1) AS UNSIGNED)), 0) + 1, 3, '0')) FROM (SELECT q.content_key FROM quiz_stock_items q JOIN batch_sets b ON b.id = q.set_id WHERE b.set_code = 'logic-training-1' AND q.content_key LIKE 'night-%') t),
        'L1', 'deep',
        '殿様に「褒美は何がよい?」と聞かれた家来は、「毎日、殿の耳のにおいをかがせてください」と願った。これで家来は大もうけした。なぜ?',
        '耳元に顔を寄せる姿が告げ口に見え、家臣が贈り物をした',
        '{"hook":"欲のない家来の話らしいぞ","hint":"殿様のまわりに目を向けてみろ!","question":"殿様に「褒美は何がよい?」と聞かれた家来は、「毎日、殿の耳のにおいをかがせてください」と願った。これで家来は大もうけした。なぜ?","answer":"耳元に顔を寄せる姿が告げ口に見え、家臣が贈り物をした","explanation":"毎日、皆の前で殿の耳元に顔を寄せる。家臣たちには告げ口をしているように見え、悪口を言われまいと贈り物を届けた。秀吉の家来・曽呂利の逸話だ。","coach_comment":"人の目まで読んだな!","tags":["とんち","夜の一問","思い込み"],"summary":"褒美に殿の耳のにおいを毎日かぎたいと願った家来が大もうけした理由を問うとんち話。耳打ちが告げ口に見え、家臣が贈り物をした。曽呂利新左衛門の逸話。","illustration_scene":"夜、ろうそくの明かりがゆれる城の広間。上座に殿様が1人座った後ろ姿。広間の床に、ふたをした漆塗りの箱がいくつも積まれ、その上に大きな「?」。顔・家来・「?」以外の文字は描かない。"}',
        '類型: 曽呂利新左衛門が秀吉の耳をかいで福を得たとんち話(作者不詳の伝承。『絵本太閤記』にも描かれる)。流布例: https://www.osaka21.or.jp/web_magazine/osaka100/025.html 。問題文では人名を出さず書き下ろし(表現は書き直し済み)。', 1);
