-- 2026-10-w1 問題ストック補充投入(14 問。レビュー承認後に実行)
-- 生成元: content/quiz-stock/logic-training-1/2026-10-w1/stock_items.py(単一ソース)。適用先: ローカル MySQL / Aurora(acps)
-- set_id は set_code から解決するため両環境共通で実行できる。
-- content_key はスロット内の既存最大連番 + 1 を適用時に解決する(V007。両環境で同一値になる)。

-- A54
INSERT INTO quiz_stock_items (set_id, content_key, quiz_type, difficulty, question_text, answer_text, content_fields, source_note, is_active)
VALUES ((SELECT id FROM batch_sets WHERE set_code = 'logic-training-1'),
        (SELECT CONCAT('morning-', LPAD(COALESCE(MAX(CAST(SUBSTRING_INDEX(t.content_key, '-', -1) AS UNSIGNED)), 0) + 1, 3, '0')) FROM (SELECT q.content_key FROM quiz_stock_items q JOIN batch_sets b ON b.id = q.set_id WHERE b.set_code = 'logic-training-1' AND q.content_key LIKE 'morning-%') t),
        'L1', 'light',
        'カードに4つの式が並んでいる。どれも同じ決まりで答えが決まる。最後のカードの「?」に入る数はいくつ?',
        '2(数字の中の輪の数。8は輪が2つ)',
        '{"hook":"幼稚園児が先に解くらしいぞ","hint":"計算はいらないぞ!","question":"カードに4つの式が並んでいる。どれも同じ決まりで答えが決まる。最後のカードの「?」に入る数はいくつ?","answer":"2(数字の中の輪の数。8は輪が2つ)","explanation":"数字の中にある輪の数を数える。0・6・9は1つ、8は2つ、1・2・5は0。2581は8だけが輪2つなので答えは2。計算ではなく形を見る問題だ。","coach_comment":"数字を絵として見られたな!","tags":["なぞなぞ","朝の一問","法則発見"],"summary":"「8809=6」「1111=0」「6666=4」「2581=?」の?を当てる法則発見。数字の中の輪の数を数える決まりで答えは2。計算の法則を探すと詰まり、字形を見ると解ける。式はカードの絵で提示。","illustration_scene":"朝日の差す木の机の上に、白いカードが縦に4枚並ぶ。上から順に黒い太字で「8809=6」「1111=0」「6666=4」「2581=?」と1枚に1行ずつ書く。数字は輪がはっきり閉じた活字体で、2は輪のない形にする。カードの横に大きな「?」。他の文字・数字・人物は描かない。"}',
        '類型: 数字の輪(穴)の数を数える法則発見(作者不詳・「幼稚園児は5分で解く」として世界的に流布)。流布例: https://raw.org/puzzle/misc/pre-school-math-problem/ , https://mindyourdecisions.com/blog/2021/12/23/a-puzzle-that-stumps-adults-but-pre-schoolers-can-solve-easily/ 。元の長い式の一覧は使わず4枚に短縮。文面はオリジナルに書き下ろし(表現は書き直し済み)。', 1);

-- A55
INSERT INTO quiz_stock_items (set_id, content_key, quiz_type, difficulty, question_text, answer_text, content_fields, source_note, is_active)
VALUES ((SELECT id FROM batch_sets WHERE set_code = 'logic-training-1'),
        (SELECT CONCAT('morning-', LPAD(COALESCE(MAX(CAST(SUBSTRING_INDEX(t.content_key, '-', -1) AS UNSIGNED)), 0) + 1, 3, '0')) FROM (SELECT q.content_key FROM quiz_stock_items q JOIN batch_sets b ON b.id = q.set_id WHERE b.set_code = 'logic-training-1' AND q.content_key LIKE 'morning-%') t),
        'L1', 'light',
        '鍵をたくさん持っているのに、扉はひとつも開けられない。それはなんだ?',
        'ピアノ(オルガンなど鍵盤楽器も正解)',
        '{"hook":"朝から鍵を探してないか?","hint":"鍵の読み方は1つだけか?","question":"鍵をたくさん持っているのに、扉はひとつも開けられない。それはなんだ?","answer":"ピアノ(オルガンなど鍵盤楽器も正解)","explanation":"ピアノの白と黒の鍵は「鍵盤(けんばん)」の鍵。何十本並んでも扉は開かない。同じ漢字の別の読みに気づけば解ける。オルガンなども正解だ。","coach_comment":"読み替えの一手、お見事!","tags":["なぞなぞ","朝の一問","言葉あそび"],"summary":"鍵をたくさん持つのに扉を開けられないものは何かという定番なぞ。答えはピアノ(鍵盤楽器なら正解)。錠の鍵と鍵盤の鍵の掛け合わせ。","illustration_scene":"朝日が差し込む古い洋館の玄関。重そうな木の扉が閉まっていて、扉の前の床に、たくさんの鍵がついた大きな鍵束が置かれている。扉の上に大きな「?」。ピアノ・楽器・人物・文字は描かない。"}',
        '類型: 鍵がたくさんあるのに扉を開けられない=ピアノの定番なぞ(作者不詳・日英に流布。英語は What has keys but can''t open locks)。流布例: https://detail.chiebukuro.yahoo.co.jp/qa/question_detail/q1034410610 , https://riddlesacademy.com/keyboard-riddles/ 。文面はオリジナルに書き下ろし(表現は書き直し済み)。', 1);

-- A56
INSERT INTO quiz_stock_items (set_id, content_key, quiz_type, difficulty, question_text, answer_text, content_fields, source_note, is_active)
VALUES ((SELECT id FROM batch_sets WHERE set_code = 'logic-training-1'),
        (SELECT CONCAT('morning-', LPAD(COALESCE(MAX(CAST(SUBSTRING_INDEX(t.content_key, '-', -1) AS UNSIGNED)), 0) + 1, 3, '0')) FROM (SELECT q.content_key FROM quiz_stock_items q JOIN batch_sets b ON b.id = q.set_id WHERE b.set_code = 'logic-training-1' AND q.content_key LIKE 'morning-%') t),
        'L1', 'light',
        '黒板の式は、このままでは正しくない。数字を1つだけ動かして、正しい式にしてくれ。',
        '2⁶−63=1(6を2の右上へ動かす)',
        '{"hook":"暗算より柔らかい頭が勝つ","hint":"数字の置き場所は横並びだけか?","question":"黒板の式は、このままでは正しくない。数字を1つだけ動かして、正しい式にしてくれ。","answer":"2⁶−63=1(6を2の右上へ動かす)","explanation":"6を2の右上へ動かすと2の6乗。2⁶=64なので、64−63=1で正しくなる。数字を横に並べ替えるだけでは解けず、置く位置を変えるのが鍵だ。","coach_comment":"数字の居場所を変えたな!","tags":["なぞなぞ","朝の一問","視覚パズル"],"summary":"黒板の「62−63=1」を数字1つだけ動かして正しい式にする定番。6を2の右上へ動かし2の6乗(64)にして64−63=1。並べ替えではなく指数の位置へ動かす発想。式は黒板の絵で提示。","illustration_scene":"朝日が差し込む教室の黒板に、白いチョークで大きく「62−63=1」とだけ書かれ、その右に大きな「?」がある。文字は「62−63=1」と「?」だけを描き、他の文字・数字・人物は描かない。"}',
        '類型: 数字を1つ動かして式を成立させる定番(Move one digit。作者不詳・英語圏に流布)。流布例: https://bhavinionline.com/2015/01/correct-equation-62-63-1/ , https://puzzleaday.wordpress.com/2019/06/15/move-one-digit/ 。式は問題文に書かず黒板の絵で提示。文面はオリジナルに書き下ろし(表現は書き直し済み)。', 1);

-- A57
INSERT INTO quiz_stock_items (set_id, content_key, quiz_type, difficulty, question_text, answer_text, content_fields, source_note, is_active)
VALUES ((SELECT id FROM batch_sets WHERE set_code = 'logic-training-1'),
        (SELECT CONCAT('morning-', LPAD(COALESCE(MAX(CAST(SUBSTRING_INDEX(t.content_key, '-', -1) AS UNSIGNED)), 0) + 1, 3, '0')) FROM (SELECT q.content_key FROM quiz_stock_items q JOIN batch_sets b ON b.id = q.set_id WHERE b.set_code = 'logic-training-1' AND q.content_key LIKE 'morning-%') t),
        'L1', 'light',
        'すみっこから一歩も動かないのに、世界中を旅できるものがある。それはなんだ?',
        '切手(封筒のすみに貼られたまま旅する)',
        '{"hook":"世界一周、してみたくないか?","hint":"そのすみっこ、何のすみだ?","question":"すみっこから一歩も動かないのに、世界中を旅できるものがある。それはなんだ?","answer":"切手(封筒のすみに貼られたまま旅する)","explanation":"切手は封筒のすみに貼られたまま、海を越えて世界中へ届く。本人はすみっこから一歩も動いていない。「旅=自分で動く」の思い込みを外そう。","coach_comment":"すみっこの主役を見つけたな!","tags":["なぞなぞ","朝の一問","逆説"],"summary":"すみっこから動かないのに世界中を旅できるものは何かという英語圏の定番なぞ。答えは切手。封筒のすみに貼られたまま運ばれる。","illustration_scene":"朝焼けの空を旅客機が飛び、眼下に青い海と大陸が広がる。空に大きな「?」。手紙・封筒・切手・郵便ポスト・人物・文字は描かない。"}',
        '類型: すみにいたまま世界を旅する=切手の定番なぞ(作者不詳・英語圏に流布。What can travel around the world while staying in a corner)。流布例: https://www.brainzilla.com/brain-teasers/riddles/oRVN3MKm/what-can-travel-around-the-world-while-staying-in-a-corner/ , https://www.mindyourlogic.com/riddle-of-the-day/what-can-travel-around-the-world 。文面はオリジナルに書き下ろし(表現は書き直し済み)。', 1);

-- A58
INSERT INTO quiz_stock_items (set_id, content_key, quiz_type, difficulty, question_text, answer_text, content_fields, source_note, is_active)
VALUES ((SELECT id FROM batch_sets WHERE set_code = 'logic-training-1'),
        (SELECT CONCAT('morning-', LPAD(COALESCE(MAX(CAST(SUBSTRING_INDEX(t.content_key, '-', -1) AS UNSIGNED)), 0) + 1, 3, '0')) FROM (SELECT q.content_key FROM quiz_stock_items q JOIN batch_sets b ON b.id = q.set_id WHERE b.set_code = 'logic-training-1' AND q.content_key LIKE 'morning-%') t),
        'L1', 'light',
        '1961年は、紙を逆さにしても「1961」と読める年だった。次にそうなる年は、西暦何年?',
        '6009年',
        '{"hook":"カレンダーの不思議な年","hint":"逆さで読める数字は何個ある?","question":"1961年は、紙を逆さにしても「1961」と読める年だった。次にそうなる年は、西暦何年?","answer":"6009年","explanation":"逆さにしても数字に見えるのは0・1・6・8・9だけ。2000年代は2が入るので全部ダメで、6で始まり9で終わる6009年が次。約4000年先だ。","coach_comment":"数字の形まで見られたら上出来!","tags":["なぞなぞ","朝の一問","逆さ読み"],"summary":"1961年のように紙を逆さにしても同じに読める次の年を問う。使える数字は0・1・6・8・9だけで、答えは6009年。字形から候補を絞る。年は紙の絵で提示。","illustration_scene":"朝日が差し込む木の机の上に白い紙が1枚。紙には黒い太字で大きく「1961」とだけ書かれている。2つの1は、上下のひげも左上のはねもない、ただの縦棒1本にする。6と9は、180度回すとちょうど重なる同じ形にする。紙の横に、くるりと回る矢印と大きな「?」。他の文字・数字・人物は描かない。"}',
        '類型: 上下逆さでも同じに読める年(Strobogrammatic year。作者不詳・英語圏に流布)。流布例: https://en.wikipedia.org/wiki/Strobogrammatic_number , https://www.engineering.com/brain-teaser-what-happened-in-1961-and-will-not-happen-again-until-6009/ 。文面はオリジナルに書き下ろし(表現は書き直し済み)。', 1);

-- A60
INSERT INTO quiz_stock_items (set_id, content_key, quiz_type, difficulty, question_text, answer_text, content_fields, source_note, is_active)
VALUES ((SELECT id FROM batch_sets WHERE set_code = 'logic-training-1'),
        (SELECT CONCAT('morning-', LPAD(COALESCE(MAX(CAST(SUBSTRING_INDEX(t.content_key, '-', -1) AS UNSIGNED)), 0) + 1, 3, '0')) FROM (SELECT q.content_key FROM quiz_stock_items q JOIN batch_sets b ON b.id = q.set_id WHERE b.set_code = 'logic-training-1' AND q.content_key LIKE 'morning-%') t),
        'L1', 'light',
        'カードに書かれた文字は、ある飲み物を表している。なんの飲み物だ?',
        '水(H から O まで = H to O = H₂O)',
        '{"hook":"朝の一杯、何を飲む?","hint":"理科の授業を思い出せ!","question":"カードに書かれた文字は、ある飲み物を表している。なんの飲み物だ?","answer":"水(H から O まで = H to O = H₂O)","explanation":"HからOまでの文字が並んでいる。英語で「H to O」、声に出すと「H two O」。水の化学式H₂Oになる。文字を順番でなく範囲として読む問題だ。","coach_comment":"理科と英語の合わせ技だな!","tags":["なぞなぞ","朝の一問","文字パズル"],"summary":"カードの「HIJKLMNO」が表す飲み物を当てる英語圏の定番。HからOまで=H to Oで、水の化学式H₂Oと読める。答えは水。文字はカードの絵で提示。","illustration_scene":"朝日が差し込むキッチンのテーブルに、横長の白いカードが1枚立ててある。カードには黒い太字で大きく「HIJKLMNO」とだけ書く。カードの横に空のコップと大きな「?」。水・ペットボトル・蛇口・人物・他の文字は描かない。"}',
        '類型: HIJKLMNO=H to O=水の定番(作者不詳・英語圏に流布)。流布例: https://www.riddles.com/2012 , https://www.braingle.com/brainteasers/900/h-i-j-k-l-m-n-o.html 。文字は問題文に書かずカードの絵で提示。文面はオリジナルに書き下ろし(表現は書き直し済み)。', 1);

-- A61
INSERT INTO quiz_stock_items (set_id, content_key, quiz_type, difficulty, question_text, answer_text, content_fields, source_note, is_active)
VALUES ((SELECT id FROM batch_sets WHERE set_code = 'logic-training-1'),
        (SELECT CONCAT('morning-', LPAD(COALESCE(MAX(CAST(SUBSTRING_INDEX(t.content_key, '-', -1) AS UNSIGNED)), 0) + 1, 3, '0')) FROM (SELECT q.content_key FROM quiz_stock_items q JOIN batch_sets b ON b.id = q.set_id WHERE b.set_code = 'logic-training-1' AND q.content_key LIKE 'morning-%') t),
        'L1', 'light',
        'アルファベットが2組に分かれている。上の組と下の組には、それぞれ共通点がある。では、Rはどっちの組に入る?',
        '下の組(上は直線だけ、下は曲線のある文字)',
        '{"hook":"英語が苦手でも解けるぞ","hint":"ペンの動きを思い出せ!","question":"アルファベットが2組に分かれている。上の組と下の組には、それぞれ共通点がある。では、Rはどっちの組に入る?","answer":"下の組(上は直線だけ、下は曲線のある文字)","explanation":"上の組は直線だけで書ける文字、下の組は曲線がまじる文字。Rは右上が丸くふくらんでいるので下の組。ABC順や母音を探すと迷子になる。","coach_comment":"形で分けたら一目瞭然だ!","tags":["なぞなぞ","朝の一問","法則発見"],"summary":"上の組A E F H I K L・下の組B C D J O P Qの分け方からRの組を当てる法則発見。上は直線だけ、下は曲線を含む文字で、Rは下。ABC順を探すと詰まる。文字は積み木の絵で提示。","illustration_scene":"朝日の差す子ども部屋の床に、アルファベットの積み木が上下2列に並ぶ。上の列は「A E F H I K L」、下の列は「B C D J O P Q」。2列から少し離れて「R」の積み木が1つ置かれ、その上に大きな「?」。積み木の文字は太く単純な書体にする。他の文字・数字・人物は描かない。"}',
        '類型: アルファベットを直線だけの文字と曲線を含む文字に分ける定番(AEFHIKLMNTVWXYZ / BCDGJOPQRSU。作者不詳・英語圏に流布)。流布例: https://www.braingle.com/brainteasers/112/aefhiklmntvwxyz.html , https://puzzleaday.wordpress.com/2025/04/03/three-alphabet-puzzles/ 。文字は問題文に書かず積み木の絵で提示。文面はオリジナルに書き下ろし(表現は書き直し済み)。', 1);

-- C56
INSERT INTO quiz_stock_items (set_id, content_key, quiz_type, difficulty, question_text, answer_text, content_fields, source_note, is_active)
VALUES ((SELECT id FROM batch_sets WHERE set_code = 'logic-training-1'),
        (SELECT CONCAT('night-', LPAD(COALESCE(MAX(CAST(SUBSTRING_INDEX(t.content_key, '-', -1) AS UNSIGNED)), 0) + 1, 3, '0')) FROM (SELECT q.content_key FROM quiz_stock_items q JOIN batch_sets b ON b.id = q.set_id WHERE b.set_code = 'logic-training-1' AND q.content_key LIKE 'night-%') t),
        'L1', 'deep',
        '妻は夫を水に沈め、そのあとひもで吊るした。なのに夫はぴんぴんしていて、その晩2人で夕食を楽しんだ。どういうこと?',
        '夫の写真を現像して、干して乾かした',
        '{"hook":"物騒な話…じゃないらしい","hint":"沈められたのは本当に夫か?","question":"妻は夫を水に沈め、そのあとひもで吊るした。なのに夫はぴんぴんしていて、その晩2人で夕食を楽しんだ。どういうこと?","answer":"夫の写真を現像して、干して乾かした","explanation":"妻が水に沈めて吊るしたのは、夫を撮ったフィルム写真。現像液に浸けた印画紙は、ひもに吊るして乾かす。本人は無事で、その晩も元気に夕食だ。","coach_comment":"言葉の裏を読んだな、見事だ!","tags":["水平思考","夜の一問","思い込み"],"summary":"妻が夫を水に沈めて吊るしたのに2人で夕食を楽しんだ理由を問う水平思考の古典。夫の写真を現像して干した。原形の「撃つ(撮る)」の掛け言葉は外した。","illustration_scene":"夜の家を描いた明るくコミカルな絵。画面を左右に分ける。左は電灯の下の浴室で、妻が湯船の夫の両肩を押して肩まで水に沈めている。右は夜の庭で、お腹にロープをぐるぐる巻きにされた夫が物干しの横棒から宙に吊るされ、妻がロープの端を引いている。首にロープはかけない。2人とも後ろ姿。中央に大きな「?」。顔・写真・カメラ・文字は描かない。"}',
        '類型: 水平思考の古典(A woman shoots her husband…。作者不詳・英語圏に流布)。流布例: https://www.braingle.com/brainteasers/1477/woman-and-her-husband.html , https://www.tolearnenglish.com/free/riddle/15.php 。原形の「撃つ」はプラットフォーム配慮で外し、現像の工程だけで構成。文面はオリジナルに書き下ろし(表現は書き直し済み)。', 1);

-- C57
INSERT INTO quiz_stock_items (set_id, content_key, quiz_type, difficulty, question_text, answer_text, content_fields, source_note, is_active)
VALUES ((SELECT id FROM batch_sets WHERE set_code = 'logic-training-1'),
        (SELECT CONCAT('night-', LPAD(COALESCE(MAX(CAST(SUBSTRING_INDEX(t.content_key, '-', -1) AS UNSIGNED)), 0) + 1, 3, '0')) FROM (SELECT q.content_key FROM quiz_stock_items q JOIN batch_sets b ON b.id = q.set_id WHERE b.set_code = 'logic-training-1' AND q.content_key LIKE 'night-%') t),
        'L1', 'deep',
        '犬が森へ走り込んでいく。この犬は、森のどこまで「走り込む」ことができる?',
        '真ん中まで(その先は森から走り出ていく)',
        '{"hook":"夜の森を駆ける一問","hint":"「込む」の向きを考えろ!","question":"犬が森へ走り込んでいく。この犬は、森のどこまで「走り込む」ことができる?","answer":"真ん中まで(その先は森から走り出ていく)","explanation":"森の真ん中を過ぎると、犬は森の出口へ向かって走ることになる。それはもう「走り込む」ではなく「走り出る」だ。距離ではなく言葉の意味で答える。","coach_comment":"言葉の向きを見抜いたな!","tags":["とんち","夜の一問","言葉の罠"],"summary":"犬が森のどこまで走り込めるかを問う英語圏の定番。真ん中を過ぎると走り出ていくので、答えは真ん中まで。距離ではなく言葉の意味で答える。","illustration_scene":"月明かりの夜、森の入り口から1匹の犬が後ろ姿で森の奥へ駆けていく。森の上空に大きな「?」。地図・矢印・人物・文字は描かない。"}',
        '類型: 犬は森のどこまで走り込めるかの定番(作者不詳・英語圏に流布)。流布例: https://www.riddles.com/298 , https://www.brainzilla.com/brain-teasers/riddles/RVNJZeVK/how-far-can-a-dog-run-into-the-woods/ 。文面はオリジナルに書き下ろし(表現は書き直し済み)。', 1);

-- C58
INSERT INTO quiz_stock_items (set_id, content_key, quiz_type, difficulty, question_text, answer_text, content_fields, source_note, is_active)
VALUES ((SELECT id FROM batch_sets WHERE set_code = 'logic-training-1'),
        (SELECT CONCAT('night-', LPAD(COALESCE(MAX(CAST(SUBSTRING_INDEX(t.content_key, '-', -1) AS UNSIGNED)), 0) + 1, 3, '0')) FROM (SELECT q.content_key FROM quiz_stock_items q JOIN batch_sets b ON b.id = q.set_id WHERE b.set_code = 'logic-training-1' AND q.content_key LIKE 'night-%') t),
        'L1', 'deep',
        '同じ年の同じ日に、同じお母さんから男の子が2人生まれた。でも2人は双子ではない。どういうこと?',
        '三つ子(以上)のうちの2人',
        '{"hook":"家族の謎、解けるか?","hint":"数え忘れはないか?","question":"同じ年の同じ日に、同じお母さんから男の子が2人生まれた。でも2人は双子ではない。どういうこと?","answer":"三つ子(以上)のうちの2人","explanation":"2人は三つ子のうちの2人。もう1人は問題文に出てこないだけだ。「2人生まれた=双子」の思い込みを外そう。四つ子でも成り立つ。","coach_comment":"数えられていない1人に気づいたな!","tags":["水平思考","夜の一問","思い込み"],"summary":"同じ日に同じ母から生まれた男の子2人が双子でない理由を問う定番。三つ子のうちの2人。3人目は問題文に出てこない。","illustration_scene":"月明かりの夜の子ども部屋。ベビーベッドが2つ並び、青い毛布にくるまった男の子の赤ちゃんが1人ずつ眠っている。赤ちゃんは後ろ頭と毛布だけを描き、顔は描かない。ベッドの上に大きな「?」。3つ目のベッド・大人・文字・数字は描かない。"}',
        '類型: 双子ではない2人=三つ子の定番(作者不詳・日英に流布)。流布例: https://kabu-elife.sakura.ne.jp/inc/nazonazo/cat2/047.html , https://www.riddles.com/5644 。文面はオリジナルに書き下ろし(表現は書き直し済み)。', 1);

-- C59
INSERT INTO quiz_stock_items (set_id, content_key, quiz_type, difficulty, question_text, answer_text, content_fields, source_note, is_active)
VALUES ((SELECT id FROM batch_sets WHERE set_code = 'logic-training-1'),
        (SELECT CONCAT('night-', LPAD(COALESCE(MAX(CAST(SUBSTRING_INDEX(t.content_key, '-', -1) AS UNSIGNED)), 0) + 1, 3, '0')) FROM (SELECT q.content_key FROM quiz_stock_items q JOIN batch_sets b ON b.id = q.set_id WHERE b.set_code = 'logic-training-1' AND q.content_key LIKE 'night-%') t),
        'L1', 'deep',
        'ボールを思いきり投げた。壁にも地面にも当たらず、ひもも付いておらず、だれも投げ返していないのに、手元に戻ってきた。なぜ?',
        '真上に投げたから',
        '{"hook":"夜の公園で一投だ","hint":"どこに向かって投げた?","question":"ボールを思いきり投げた。壁にも地面にも当たらず、ひもも付いておらず、だれも投げ返していないのに、手元に戻ってきた。なぜ?","answer":"真上に投げたから","explanation":"真上に投げたボールは、重力で同じ場所へ落ちてくる。何にも当たらず、だれも触らない。「投げる=前へ」の思い込みを外せば一瞬だ。","coach_comment":"上を向いた者の勝ちだ!","tags":["水平思考","夜の一問","発想の転換"],"summary":"壁にも当たらず誰も投げ返さないのに、思いきり投げたボールが手元に戻る理由を問う英語圏の定番。真上に投げた。投げる向きの思い込みを外す。","illustration_scene":"夜の公園、街灯の下の広場に、後ろ姿の人が腕を前へ振り抜いたポーズで立つ。正面の遠くに大きな「?」。ボール・顔・文字は描かない。"}',
        '類型: 投げたボールが戻る=真上に投げたの定番(作者不詳・英語圏に流布)。流布例: https://www.riddles.com/archives/4396 , https://riddles.guru/riddles/throw-ball-come-back/215/ 。文面はオリジナルに書き下ろし(表現は書き直し済み)。', 1);

-- C60
INSERT INTO quiz_stock_items (set_id, content_key, quiz_type, difficulty, question_text, answer_text, content_fields, source_note, is_active)
VALUES ((SELECT id FROM batch_sets WHERE set_code = 'logic-training-1'),
        (SELECT CONCAT('night-', LPAD(COALESCE(MAX(CAST(SUBSTRING_INDEX(t.content_key, '-', -1) AS UNSIGNED)), 0) + 1, 3, '0')) FROM (SELECT q.content_key FROM quiz_stock_items q JOIN batch_sets b ON b.id = q.set_id WHERE b.set_code = 'logic-training-1' AND q.content_key LIKE 'night-%') t),
        'L1', 'deep',
        '写真を見て男が言う。「私にきょうだいはいない。でも、この人の父親は、私の父の息子だ」。写真の人はだれ?',
        '男の息子(私の父の息子=私自身)',
        '{"hook":"家系図を頭に描けるか?","hint":"「私の父の息子」とはだれだ?","question":"写真を見て男が言う。「私にきょうだいはいない。でも、この人の父親は、私の父の息子だ」。写真の人はだれ?","answer":"男の息子(私の父の息子=私自身)","explanation":"きょうだいがいないので「私の父の息子」は男自身。つまり「この人の父親は私」となり、写真の人は男の息子だ。言葉を1段ずつほどけば見える。","coach_comment":"1段ずつほどけば必ず解ける!","tags":["論理","夜の一問","言葉の罠"],"summary":"きょうだいのいない男が写真を見て「この人の父親は私の父の息子だ」と言うとき写真の人はだれかを問う英語圏の古典。私の父の息子=私なので、答えは男の息子。","illustration_scene":"夜、スタンドの明かりに照らされた書斎。後ろ姿の男が、壁に掛かった額縁を見上げている。額縁の中は白くぼかして何も描かない。額縁の上に大きな「?」。額縁の中の人物・顔・文字は描かない。"}',
        '類型: Brothers and sisters have I none の古典(作者不詳・英語圏に流布)。流布例: https://puzzles.nigelcoldwell.co.uk/fifty.htm , https://www.riddles.com/767 。「兄弟」は姉妹を含めるため「きょうだい」と表記。文面はオリジナルに書き下ろし(表現は書き直し済み)。', 1);

-- C61
INSERT INTO quiz_stock_items (set_id, content_key, quiz_type, difficulty, question_text, answer_text, content_fields, source_note, is_active)
VALUES ((SELECT id FROM batch_sets WHERE set_code = 'logic-training-1'),
        (SELECT CONCAT('night-', LPAD(COALESCE(MAX(CAST(SUBSTRING_INDEX(t.content_key, '-', -1) AS UNSIGNED)), 0) + 1, 3, '0')) FROM (SELECT q.content_key FROM quiz_stock_items q JOIN batch_sets b ON b.id = q.set_id WHERE b.set_code = 'logic-training-1' AND q.content_key LIKE 'night-%') t),
        'L1', 'deep',
        '高さ10mのはしごから落ちたのに、かすり傷ひとつなかった。なぜ?',
        '一番下の段から落ちたから',
        '{"hook":"高所作業の夜の謎","hint":"10mは、はしごの高さだぞ!","question":"高さ10mのはしごから落ちたのに、かすり傷ひとつなかった。なぜ?","answer":"一番下の段から落ちたから","explanation":"10mなのは、はしごの高さ。落ちたのは一番下の段からなので、地面まではほんの数十センチ。数字の大きさに気を取られると見落とす。","coach_comment":"数字に惑わされなかったな!","tags":["ひっかけ","夜の一問","思い込み"],"summary":"高さ10mのはしごから落ちたのに無傷だった理由を問う定番のひっかけ。一番下の段から落ちた。はしごの高さと落ちた高さの違い。","illustration_scene":"夜の工事現場。投光器に照らされて、高い建物の壁に長いはしごが立てかけてある。はしごのてっぺんの横に大きな「?」。人物・ヘルメット・文字・数字は描かない。"}',
        '類型: 高いはしごから落ちて無傷=一番下の段の定番のひっかけ(作者不詳・英語圏に流布。日本では階段版が多い)。流布例: https://www.riddles.com/4080 , https://solveordie.com/riddle-152/ 。文面はオリジナルに書き下ろし(表現は書き直し済み)。', 1);

-- C62
INSERT INTO quiz_stock_items (set_id, content_key, quiz_type, difficulty, question_text, answer_text, content_fields, source_note, is_active)
VALUES ((SELECT id FROM batch_sets WHERE set_code = 'logic-training-1'),
        (SELECT CONCAT('night-', LPAD(COALESCE(MAX(CAST(SUBSTRING_INDEX(t.content_key, '-', -1) AS UNSIGNED)), 0) + 1, 3, '0')) FROM (SELECT q.content_key FROM quiz_stock_items q JOIN batch_sets b ON b.id = q.set_id WHERE b.set_code = 'logic-training-1' AND q.content_key LIKE 'night-%') t),
        'L1', 'deep',
        'タロウとハナコが床に倒れて動かない。そばには水たまりとガラスの破片。窓は開いている。何があった?',
        '2匹は金魚で、風で金魚鉢が落ちて割れた',
        '{"hook":"夜の部屋で何が起きた?","hint":"開いた窓から何が入った?","question":"タロウとハナコが床に倒れて動かない。そばには水たまりとガラスの破片。窓は開いている。何があった?","answer":"2匹は金魚で、風で金魚鉢が落ちて割れた","explanation":"タロウとハナコは金魚。開いた窓から風が吹き込み、金魚鉢が床に落ちて割れた。水たまりもガラスも鉢のもの。名前で人だと思い込ませる問題だ。","coach_comment":"名前の罠を見破ったな!","tags":["水平思考","夜の一問","思い込み"],"summary":"タロウとハナコが水たまりとガラス片のそばで倒れている理由を問う水平思考の定番。2匹は金魚で、風で金魚鉢が落ちて割れた。名前で人だと思い込ませる。","illustration_scene":"夜の部屋、開いた窓からカーテンが風で大きくなびき、月明かりが床を照らす。床に水たまりと割れたガラスの破片。窓の上に大きな「?」。金魚・金魚鉢・魚・人物・文字は描かない。"}',
        '類型: 水平思考の定番(ロミオとジュリエットの類型。作者不詳・英語圏に流布。原形は列車の振動で水槽が落ちる)。流布例: https://www.riddles.com/2 , https://solveordie.com/riddle-868/ 。文面はオリジナルに書き下ろし(表現は書き直し済み)。', 1);
