-- 2026-09-w3 問題ストック補充投入(14 問。レビュー承認後に実行)
-- 生成元: content/quiz-stock/logic-training-1/2026-09-w3/stock_items.py(単一ソース)。適用先: ローカル MySQL / Aurora(acps)
-- set_id は set_code から解決するため両環境共通で実行できる。
-- content_key はスロット内の既存最大連番 + 1 を適用時に解決する(V007。両環境で同一値になる)。

-- A40
INSERT INTO quiz_stock_items (set_id, content_key, quiz_type, difficulty, question_text, answer_text, content_fields, source_note, is_active)
VALUES ((SELECT id FROM batch_sets WHERE set_code = 'logic-training-1'),
        (SELECT CONCAT('morning-', LPAD(COALESCE(MAX(CAST(SUBSTRING_INDEX(t.content_key, '-', -1) AS UNSIGNED)), 0) + 1, 3, '0')) FROM (SELECT q.content_key FROM quiz_stock_items q JOIN batch_sets b ON b.id = q.set_id WHERE b.set_code = 'logic-training-1' AND q.content_key LIKE 'morning-%') t),
        'L1', 'light',
        '5+5+5=550。この式は間違っている。線をたった1本だけ足して、正しい式にしてくれ。',
        '545+5=550(=を≠にするのも正解)',
        '{"hook":"足し算なのに線を引くだけ?","hint":"数字じゃなく記号を見ろ!","question":"5+5+5=550。この式は間違っている。線をたった1本だけ足して、正しい式にしてくれ。","answer":"545+5=550(=を≠にするのも正解)","explanation":"左の「+」に斜線を1本足すと「4」になり、545+5=550で成立。数字をいじろうとすると詰まるが、記号なら一撃だ。「=」を「≠」にする裏技も正解。","coach_comment":"記号も数字の仲間だ、よく見たな!","tags":["なぞなぞ","朝の一問","式のパズル"],"summary":"「5+5+5=550」に線を1本足して正しい式にする定番の視覚パズル。「+」に斜線を足して「4」にし545+5=550。「=」を「≠」にする別解も正解に取り込む。","illustration_scene":"朝日が差し込む教室の黒板に、チョークで「5+5+5=550」と大きく1行だけ書かれ、その横に大きな「?」がある。文字はこの式と「?」だけを描き、他の文字・数字は描かない。人物は描かない。"}',
        '類型: 線を1本足して式を直す視覚パズル(作者不詳・国内外に流布)。流布例: https://detail.chiebukuro.yahoo.co.jp/qa/question_detail/q1034575295 , https://ddnavi.com/article/d532020/a/ , https://quiz.community.fmworld.net/nazonazo/content/63/answer3.html , https://nazoq.com/hardest/Q003458.html 。文面はオリジナルに書き下ろし(表現は書き直し済み)。', 1);

-- A42
INSERT INTO quiz_stock_items (set_id, content_key, quiz_type, difficulty, question_text, answer_text, content_fields, source_note, is_active)
VALUES ((SELECT id FROM batch_sets WHERE set_code = 'logic-training-1'),
        (SELECT CONCAT('morning-', LPAD(COALESCE(MAX(CAST(SUBSTRING_INDEX(t.content_key, '-', -1) AS UNSIGNED)), 0) + 1, 3, '0')) FROM (SELECT q.content_key FROM quiz_stock_items q JOIN batch_sets b ON b.id = q.set_id WHERE b.set_code = 'logic-training-1' AND q.content_key LIKE 'morning-%') t),
        'L1', 'light',
        '止まったままの時計と、1日に1分ずつ遅れていく時計。「正しい時刻を示す回数」が多いのはどっちだ?',
        '止まった時計(1日2回は正しい)',
        '{"hook":"動かない時計にも取り柄がある?","hint":"正しい時刻を示す回数を数えろ!","question":"止まったままの時計と、1日に1分ずつ遅れていく時計。「正しい時刻を示す回数」が多いのはどっちだ?","answer":"止まった時計(1日2回は正しい)","explanation":"止まった時計は1日に2回、必ず正しい時刻を指す。一方1分ずつ遅れる時計は、12時間ぶん遅れて再び合うまで720日。つまり約2年に1回しか正しくない。","coach_comment":"常識を疑え、それが頭の体操だ!","tags":["ひっかけ","朝の一問","時計"],"summary":"止まった時計と1日1分遅れる時計のどちらが正しい時刻を多く示すかを問うルイス・キャロル由来の古典。止まった時計は1日2回、遅れる時計は720日に1回で、止まった方が多い。","illustration_scene":"朝日が差し込む棚の上に、古い置き時計が2つ並んでいる。片方はほこりをかぶって針が止まり、もう片方は小さく傾いて動いている。その間に大きな「?」。文字盤の数字は描かず、文字・数字は描かない。人物は描かない。"}',
        '類型: 思い込み外し(止まった時計と遅れる時計。ルイス・キャロル『The Rectory Umbrella』由来で作者不詳の形で流布)。流布例: https://blog.goo.ne.jp/lemon-stoism/e/381964bfad6d0f3418f4e579663743ea , https://kzr-2.hatenadiary.org/entry/20090714/p2 , https://detail.chiebukuro.yahoo.co.jp/qa/question_detail/q1322931153 。文面はオリジナルに書き下ろし(表現は書き直し済み)。', 1);

-- A44
INSERT INTO quiz_stock_items (set_id, content_key, quiz_type, difficulty, question_text, answer_text, content_fields, source_note, is_active)
VALUES ((SELECT id FROM batch_sets WHERE set_code = 'logic-training-1'),
        (SELECT CONCAT('morning-', LPAD(COALESCE(MAX(CAST(SUBSTRING_INDEX(t.content_key, '-', -1) AS UNSIGNED)), 0) + 1, 3, '0')) FROM (SELECT q.content_key FROM quiz_stock_items q JOIN batch_sets b ON b.id = q.set_id WHERE b.set_code = 'logic-training-1' AND q.content_key LIKE 'morning-%') t),
        'L1', 'light',
        '一、二、三…十。1から10を漢字で書いたとき、画数がいちばん多いのはどの数字だ?',
        '四(5画)',
        '{"hook":"漢字の一から十、書けるか?","hint":"全部書き出して数えろ!","question":"一、二、三…十。1から10を漢字で書いたとき、画数がいちばん多いのはどの数字だ?","answer":"四(5画)","explanation":"一1画、二2画、三3画、四5画、五4画、六4画、七2画、八2画、九2画、十2画。大きい数ほど画数が多いと思いきや、いちばん多いのは四の5画だ。","coach_comment":"思い込みを書き出して壊す、いいぞ!","tags":["漢字","朝の一問","数え上げ"],"summary":"1〜10を漢字で書いたとき画数が最多の字を問う。答えは四(5画)。数が大きいほど画数が多いという思い込みを、全部書き出して数える一手間で崩す。自作問題。","illustration_scene":"朝日が差し込む和室の机に半紙が広げられ、筆で「一 二 三 四 五 六 七 八 九 十」と横一列に大きく書かれている。その上に大きな「?」。文字はこの10字と「?」だけを描き、他の文字・数字は描かない。人物は描かない。"}',
        'オリジナル書き下ろし(自作問題)。類型: 画数の数え上げ(漢数字の画数を問題化)。画数は常用漢字表どおり(四=5画・五=4画・六=4画)で verify_logic.py に一覧を記録。', 1);

-- A45
INSERT INTO quiz_stock_items (set_id, content_key, quiz_type, difficulty, question_text, answer_text, content_fields, source_note, is_active)
VALUES ((SELECT id FROM batch_sets WHERE set_code = 'logic-training-1'),
        (SELECT CONCAT('morning-', LPAD(COALESCE(MAX(CAST(SUBSTRING_INDEX(t.content_key, '-', -1) AS UNSIGNED)), 0) + 1, 3, '0')) FROM (SELECT q.content_key FROM quiz_stock_items q JOIN batch_sets b ON b.id = q.set_id WHERE b.set_code = 'logic-training-1' AND q.content_key LIKE 'morning-%') t),
        'L1', 'light',
        '本棚に洋書の全集10巻が順に並ぶ。虫が1巻の1ページ目から10巻の最後のページまで一直線に食べ進んだ。各巻の厚さ3cm、表紙は無視すると食べた長さは?',
        '24cm(1巻と10巻はほぼ食べない)',
        '{"hook":"本を食べる虫の話だ","hint":"本棚での1ページ目の位置を思え!","question":"本棚に洋書の全集10巻が順に並ぶ。虫が1巻の1ページ目から10巻の最後のページまで一直線に食べ進んだ。各巻の厚さ3cm、表紙は無視すると食べた長さは?","answer":"24cm(1巻と10巻はほぼ食べない)","explanation":"洋書を棚に立てると表紙は右を向く。1巻の1ページ目は右端で2巻と隣り合い、10巻の最後のページは左端で9巻側。虫が食べるのは2〜9巻の8冊分=24cmだ。","coach_comment":"頭の中の本棚を疑ったな、見事だ!","tags":["ひっかけ","朝の一問","思い込み"],"summary":"本棚の全集10巻を1巻の1ページ目から10巻の最後まで食べる虫の距離を問う古典(bookworm puzzle)。1巻の1ページ目は2巻側にあるため2〜9巻の8冊分=24cm。30cmと早合点させる。","illustration_scene":"朝日が差し込む書斎の本棚に、背表紙を手前にした分厚い洋書の全集が10冊きっちり並び、その前に大きな「?」が浮かぶ。背表紙に文字や数字は描かない。虫は描かない。人物は描かない。"}',
        '類型: 思い込み外し(本棚の虫。作者不詳・英語圏で広く流布する古典)。流布例: https://www.braingle.com/brainteasers/8363/the-bookworm.html , https://mathlair.allfunandgames.ca/bookworm.php , https://www.science20.com/chatter_box/blog/bookworm_and_encyclopedias_solution , https://riddlesbrainteasers.com/bookworm/ 。日本の縦書き本(右開き)では並びが逆になるため「洋書」と明記した。文面はオリジナルに書き下ろし(表現は書き直し済み)。', 1);

-- A41
INSERT INTO quiz_stock_items (set_id, content_key, quiz_type, difficulty, question_text, answer_text, content_fields, source_note, is_active)
VALUES ((SELECT id FROM batch_sets WHERE set_code = 'logic-training-1'),
        (SELECT CONCAT('morning-', LPAD(COALESCE(MAX(CAST(SUBSTRING_INDEX(t.content_key, '-', -1) AS UNSIGNED)), 0) + 1, 3, '0')) FROM (SELECT q.content_key FROM quiz_stock_items q JOIN batch_sets b ON b.id = q.set_id WHERE b.set_code = 'logic-training-1' AND q.content_key LIKE 'morning-%') t),
        'L1', 'light',
        '数字の8をちょうど8個使い、足し算だけで合計を1000にしてくれ。8を並べて88や888にしてもいい。',
        '888+88+8+8+8=1000',
        '{"hook":"8だけで1000を作れるか?","hint":"一の位を0にする数を考えろ!","question":"数字の8をちょうど8個使い、足し算だけで合計を1000にしてくれ。8を並べて88や888にしてもいい。","answer":"888+88+8+8+8=1000","explanation":"一の位を0にするには8を5個足す必要がある(8×5=40)。そこから888+88+8+8+8を試すと1000。足し算だけならこの組み合わせしかない。","coach_comment":"一の位から攻める、それが王道だ!","tags":["なぞなぞ","朝の一問","数字パズル"],"summary":"8を8個使って足し算だけで1000を作る古典の数字パズル。答えは888+88+8+8+8。一の位を0にするには8が5個要ることから逆算する。足し算限定では一意。","illustration_scene":"朝日が差し込む木の机の上に、木製の数字ブロック「8」が8個バラバラに転がっていて、その上に大きな「?」が浮かんでいる。文字は「8」のブロック8個と「?」だけを描き、他の文字・数字は描かない。人物は描かない。"}',
        '類型: 数字パズル(8 を 8 個で 1000。作者不詳・国内外に流布)。流布例: https://detail.chiebukuro.yahoo.co.jp/qa/question_detail/q1298194207 , https://detail.chiebukuro.yahoo.co.jp/qa/question_detail/q13314261373 , https://themathmompuzzles.blogspot.com/2011/04/eight-eights-that-are-thousand.html 。文面はオリジナルに書き下ろし(表現は書き直し済み)。', 1);

-- A46
INSERT INTO quiz_stock_items (set_id, content_key, quiz_type, difficulty, question_text, answer_text, content_fields, source_note, is_active)
VALUES ((SELECT id FROM batch_sets WHERE set_code = 'logic-training-1'),
        (SELECT CONCAT('morning-', LPAD(COALESCE(MAX(CAST(SUBSTRING_INDEX(t.content_key, '-', -1) AS UNSIGNED)), 0) + 1, 3, '0')) FROM (SELECT q.content_key FROM quiz_stock_items q JOIN batch_sets b ON b.id = q.set_id WHERE b.set_code = 'logic-training-1' AND q.content_key LIKE 'morning-%') t),
        'L1', 'light',
        '地球の赤道にロープをぴったり1周巻く。次にロープを1mだけ長くして、地面から均等に浮かせた。地面との隙間はどれくらい?',
        '約16cm(ネコが通れる)',
        '{"hook":"地球一周ぶんのロープだ","hint":"円周と半径の関係を思い出せ!","question":"地球の赤道にロープをぴったり1周巻く。次にロープを1mだけ長くして、地面から均等に浮かせた。地面との隙間はどれくらい?","answer":"約16cm(ネコが通れる)","explanation":"円周が1m増えると半径は1÷(2×3.14)≒0.16m増える。地球の大きさは関係ない。1mでは紙1枚も入らない気がするが、実際は約16cmも浮く。","coach_comment":"直感より計算を信じろ!","tags":["ひっかけ","朝の一問","規模感"],"summary":"赤道に巻いたロープを1m長くしたときの地面との隙間を問う古典。円周1m増で半径は1/(2π)≒16cm増え、地球の大きさに依存しない。直感(紙1枚)と計算の差を突く。","illustration_scene":"宇宙から見た青い地球に太いロープが赤道に1周巻かれ、地球の縁から朝日が昇っている。ロープのそばに大きな「?」。文字・数字は描かない。人物は描かない。"}',
        '類型: 規模感の直感外し(地球に巻いたロープ。作者不詳・国内外に流布)。流布例: https://plaza.rakuten.co.jp/umidas21/diary/200612240000/ , https://hama-1987.cocolog-nifty.com/blog/2013/07/post-a49b.html , https://www.omoshiro-suugaku.com/entry/sekidounirope , https://nazesuugaku.com/rope_surrounds_earth/ 。文面はオリジナルに書き下ろし(表現は書き直し済み)。', 1);

-- A43
INSERT INTO quiz_stock_items (set_id, content_key, quiz_type, difficulty, question_text, answer_text, content_fields, source_note, is_active)
VALUES ((SELECT id FROM batch_sets WHERE set_code = 'logic-training-1'),
        (SELECT CONCAT('morning-', LPAD(COALESCE(MAX(CAST(SUBSTRING_INDEX(t.content_key, '-', -1) AS UNSIGNED)), 0) + 1, 3, '0')) FROM (SELECT q.content_key FROM quiz_stock_items q JOIN batch_sets b ON b.id = q.set_id WHERE b.set_code = 'logic-training-1' AND q.content_key LIKE 'morning-%') t),
        'L1', 'light',
        '時計の文字盤に直線を2本引いて、3つの部分に分ける。どの部分も数字の合計が同じになる引き方は?',
        '11〜2、3・4・9・10、5〜8の3組(各26)',
        '{"hook":"時計を3つに割るとは?","hint":"まず1〜12の合計を3で割れ!","question":"時計の文字盤に直線を2本引いて、3つの部分に分ける。どの部分も数字の合計が同じになる引き方は?","answer":"11〜2、3・4・9・10、5〜8の3組(各26)","explanation":"1〜12の合計は78なので1部分は26。11+12+1+2=26、5+6+7+8=26になるよう横向きの平行線を2本引くと、残る3・4・9・10も26になる。","coach_comment":"合計から逆算、それが近道だ!","tags":["なぞなぞ","朝の一問","時計"],"summary":"時計の文字盤を直線2本で3分割し各部分の数字の合計を等しくする古典パズル。合計78÷3=26から逆算し、11・12・1・2/3・4・9・10/5・6・7・8に分ける平行線2本。","illustration_scene":"朝日が差し込むリビングの壁に、1から12の数字がはっきり書かれた丸いアナログ時計が掛かり、その横に大きな「?」が浮かぶ。文字は時計の数字1〜12と「?」だけを描き、他の文字・数字は描かない。人物は描かない。"}',
        '類型: 文字盤の分割(作者不詳・国内外に流布)。流布例: https://nrich.maths.org/problems/split-clock-face , https://www.quora.com/How-do-I-draw-2-straight-lines-on-a-clock-face-to-separate-it-into-3-parts-and-that-each-parts-numbers-add-up-to-26 , https://puzzleaday.wordpress.com/2019/02/06/dividing-a-clock-face-into-sections/ 。文面はオリジナルに書き下ろし(表現は書き直し済み)。', 1);

-- C42
INSERT INTO quiz_stock_items (set_id, content_key, quiz_type, difficulty, question_text, answer_text, content_fields, source_note, is_active)
VALUES ((SELECT id FROM batch_sets WHERE set_code = 'logic-training-1'),
        (SELECT CONCAT('night-', LPAD(COALESCE(MAX(CAST(SUBSTRING_INDEX(t.content_key, '-', -1) AS UNSIGNED)), 0) + 1, 3, '0')) FROM (SELECT q.content_key FROM quiz_stock_items q JOIN batch_sets b ON b.id = q.set_id WHERE b.set_code = 'logic-training-1' AND q.content_key LIKE 'night-%') t),
        'L1', 'deep',
        '王が2人の騎手に「馬で競走せよ。ただし後にゴールした馬の持ち主の勝ち」と告げた。2人は動かない。賢者の一言で全力疾走したのは、なぜ?',
        '「馬を交換しろ」(相手の馬で先にゴール)',
        '{"hook":"遅い方が勝ちのレース?","hint":"ルールは変えずに立場を変えろ!","question":"王が2人の騎手に「馬で競走せよ。ただし後にゴールした馬の持ち主の勝ち」と告げた。2人は動かない。賢者の一言で全力疾走したのは、なぜ?","answer":"「馬を交換しろ」(相手の馬で先にゴール)","explanation":"勝つのは「自分の馬」が後にゴールすること。馬を交換すれば、相手の馬に乗って先にゴールするほど自分の馬が後になる。ルールはそのまま、立場を入れ替える発想だ。","coach_comment":"視点をひっくり返す、それが水平思考だ!","tags":["水平思考","夜の一問","発想転換"],"summary":"「後にゴールした馬の持ち主が勝ち」の膠着レースを賢者の一言「馬を交換しろ」で動かす古典の水平思考。相手の馬で先にゴールすれば自分の馬が後になる。","illustration_scene":"夜、松明に照らされた馬場に、2頭の馬が並んで立ち止まり、その上に大きな「?」が浮かぶ。馬に乗る2人の騎手は後ろ姿で顔は描かない。遠くのゴールの旗には文字を入れない。文字・数字は描かない。"}',
        '類型: 水平思考(のろのろ馬レース。作者不詳の古典)。流布例: https://diamond.jp/articles/-/341503 , https://www.oricon.co.jp/article/2556546/ , https://sist8.com/2horse 。文面はオリジナルに書き下ろし(表現は書き直し済み)。', 1);

-- C43
INSERT INTO quiz_stock_items (set_id, content_key, quiz_type, difficulty, question_text, answer_text, content_fields, source_note, is_active)
VALUES ((SELECT id FROM batch_sets WHERE set_code = 'logic-training-1'),
        (SELECT CONCAT('night-', LPAD(COALESCE(MAX(CAST(SUBSTRING_INDEX(t.content_key, '-', -1) AS UNSIGNED)), 0) + 1, 3, '0')) FROM (SELECT q.content_key FROM quiz_stock_items q JOIN batch_sets b ON b.id = q.set_id WHERE b.set_code = 'logic-training-1' AND q.content_key LIKE 'night-%') t),
        'L1', 'deep',
        '机の上にロウソク・マッチ・画びょうの入った箱。ロウソクを壁に固定し、火をつけてもロウが机にたれないようにしたい。どうする?',
        '箱を画びょうで壁に留め、台にする',
        '{"hook":"ロウがたれない工夫とは","hint":"箱はただの入れ物か?","question":"机の上にロウソク・マッチ・画びょうの入った箱。ロウソクを壁に固定し、火をつけてもロウが机にたれないようにしたい。どうする?","answer":"箱を画びょうで壁に留め、台にする","explanation":"画びょうを出して空いた箱を壁に留め、その上にロウソクを立てる。箱を「画びょうの入れ物」としか見ないと解けない。物の役割を固定しない発想が鍵だ。","coach_comment":"道具の役割を疑え、それが突破口だ!","tags":["水平思考","夜の一問","道具"],"summary":"ロウソク・マッチ・画びょうの箱でロウソクを壁に固定する古典(ドゥンカーのロウソク問題)。箱を画びょうで壁に留めて台にする。機能的固着を外す発想を問う。","illustration_scene":"夜、ランプに照らされた木の机の上に、1本のロウソク、マッチ箱、画びょうがぎっしり入った小さな紙箱が並び、後ろの壁に大きな「?」が浮かぶ。ロウソクは壁に付いていない。文字・数字は描かない。人物は描かない。"}',
        '類型: 水平思考(ロウソク問題。1945 年ドゥンカーの心理学実験に由来し、作者を離れて古典として流布)。流布例: https://ja.wikipedia.org/wiki/%E3%83%AD%E3%82%A6%E3%82%BD%E3%82%AF%E5%95%8F%E9%A1%8C , https://www.weblio.jp/content/%E3%83%AD%E3%82%A6%E3%82%BD%E3%82%AF%E5%95%8F%E9%A1%8C , https://mitani3.com/blog/2010/07/post-223.html 。文面はオリジナルに書き下ろし(表現は書き直し済み)。', 1);

-- C46
INSERT INTO quiz_stock_items (set_id, content_key, quiz_type, difficulty, question_text, answer_text, content_fields, source_note, is_active)
VALUES ((SELECT id FROM batch_sets WHERE set_code = 'logic-training-1'),
        (SELECT CONCAT('night-', LPAD(COALESCE(MAX(CAST(SUBSTRING_INDEX(t.content_key, '-', -1) AS UNSIGNED)), 0) + 1, 3, '0')) FROM (SELECT q.content_key FROM quiz_stock_items q JOIN batch_sets b ON b.id = q.set_id WHERE b.set_code = 'logic-training-1' AND q.content_key LIKE 'night-%') t),
        'L1', 'deep',
        'かごにリンゴが6個。6人の子どもが1人1個ずつ受け取ったのに、かごの中にはまだリンゴが1個残っている。切ったり分けたりはしていない。なぜ?',
        '最後の1人はかごごと受け取った',
        '{"hook":"かごのリンゴが消えない?","hint":"最後の1人の受け取り方だ!","question":"かごにリンゴが6個。6人の子どもが1人1個ずつ受け取ったのに、かごの中にはまだリンゴが1個残っている。切ったり分けたりはしていない。なぜ?","answer":"最後の1人はかごごと受け取った","explanation":"5人が1個ずつ取り、最後の1人はリンゴ入りのかごごと受け取った。だから6人とも1個ずつ持ち、かごの中にも1個ある。「かごの中=誰のものでもない」が思い込みだ。","coach_comment":"言葉の隙間を見つけたな、見事だ!","tags":["水平思考","夜の一問","ひっかけ"],"summary":"6個のリンゴを6人が1個ずつ受け取ったのにかごに1個残る理由を問う古典の水平思考。最後の1人がかごごと受け取った。「かごの中のリンゴは誰のものでもない」という思い込みを外す。","illustration_scene":"夜、台所の照明の下、木のテーブルに籐のかごが1つ置かれ、その中に赤いリンゴが1個だけ入っている。かごの横に大きな「?」。リンゴは1個だけ描く。人物は描かない。文字・数字は描かない。"}',
        '類型: 水平思考(残ったリンゴ。作者不詳の定番)。流布例: https://detail.chiebukuro.yahoo.co.jp/qa/question_detail/q1431927394 , https://ameblo.jp/01180622/entry-10290556264.html , https://mixi.jp/view_bbs.pl?comm_id=4284716&id=43356568 。文面はオリジナルに書き下ろし(表現は書き直し済み)。', 1);

-- C45
INSERT INTO quiz_stock_items (set_id, content_key, quiz_type, difficulty, question_text, answer_text, content_fields, source_note, is_active)
VALUES ((SELECT id FROM batch_sets WHERE set_code = 'logic-training-1'),
        (SELECT CONCAT('night-', LPAD(COALESCE(MAX(CAST(SUBSTRING_INDEX(t.content_key, '-', -1) AS UNSIGNED)), 0) + 1, 3, '0')) FROM (SELECT q.content_key FROM quiz_stock_items q JOIN batch_sets b ON b.id = q.set_id WHERE b.set_code = 'logic-training-1' AND q.content_key LIKE 'night-%') t),
        'L1', 'deep',
        '昔の中国。王に贈られたゾウの重さを知りたいが、ゾウが乗れる秤はない。あるのは大きな船と、たくさんの石と普通の秤。幼い王子はどう量った?',
        '船の喫水線に印、同じ沈みまで石を積んで石を量る',
        '{"hook":"巨大なゾウの体重を量れ","hint":"ゾウを何かに置き換えろ!","question":"昔の中国。王に贈られたゾウの重さを知りたいが、ゾウが乗れる秤はない。あるのは大きな船と、たくさんの石と普通の秤。幼い王子はどう量った?","answer":"船の喫水線に印、同じ沈みまで石を積んで石を量る","explanation":"ゾウを船に乗せ、水面の位置に印をつける。ゾウを降ろし、同じ印まで沈むよう石を積めば、石の総重量がゾウの重さ。三国志の曹沖が幼くして示したという故事だ。","coach_comment":"大きな問題は小分けにして量れ!","tags":["故事","夜の一問","発想転換"],"summary":"秤に乗らないゾウの重さを、船の喫水線に印をつけて同じ沈みまで石を積み替えて量る三国志の故事(曹沖称象)。等価置換の発想を問う。前バッチC41(王冠)と同じく水を使うが手順は別。","illustration_scene":"月夜の川岸に大きな木造の船が浮かび、岸には1頭の大きなゾウと石の山がある。船は空で、ゾウはまだ乗っていない。上に大きな「?」。人物は遠景の後ろ姿のみで顔は描かない。文字・数字は描かない。"}',
        '類型: 故事(曹沖称象。『三国志』魏書 由来の逸話で作者不詳の形で流布)。流布例: https://ja.wikipedia.org/wiki/%E6%9B%B9%E6%B2%96 , https://hajimete-sangokushi.com/2015/01/25/post-1231/ , https://history-ancient.com/soucyuu-sangokusi/ , https://baike.baidu.com/item/%E6%9B%B9%E5%86%B2%E7%A7%B0%E8%B1%A1/5085 。文面はオリジナルに書き下ろし(表現は書き直し済み)。', 1);

-- C44
INSERT INTO quiz_stock_items (set_id, content_key, quiz_type, difficulty, question_text, answer_text, content_fields, source_note, is_active)
VALUES ((SELECT id FROM batch_sets WHERE set_code = 'logic-training-1'),
        (SELECT CONCAT('night-', LPAD(COALESCE(MAX(CAST(SUBSTRING_INDEX(t.content_key, '-', -1) AS UNSIGNED)), 0) + 1, 3, '0')) FROM (SELECT q.content_key FROM quiz_stock_items q JOIN batch_sets b ON b.id = q.set_id WHERE b.set_code = 'logic-training-1' AND q.content_key LIKE 'night-%') t),
        'L1', 'deep',
        '和尚が「この水あめは子どもが食べたら死ぬ毒だ」と言って出かけた。小僧たちは全部食べてしまった。戻った和尚に叱られない、とんちの一言は?',
        '茶碗を割ったお詫びに毒を食べて死のうとしました',
        '{"hook":"叱られる前の一手とは","hint":"和尚の嘘を逆手に取れ!","question":"和尚が「この水あめは子どもが食べたら死ぬ毒だ」と言って出かけた。小僧たちは全部食べてしまった。戻った和尚に叱られない、とんちの一言は?","answer":"茶碗を割ったお詫びに毒を食べて死のうとしました","explanation":"和尚の大事な茶碗をわざと割り「お詫びに死のうと毒を全部食べたのに死ねません」と泣く。毒と言った和尚の嘘を逆手に取れば、叱ると嘘がばれる。一休の古典とんちだ。","coach_comment":"相手の言葉で相手を封じる、見事だ!","tags":["とんち","夜の一問","古典"],"summary":"「子どもが食べたら死ぬ毒」と偽った和尚の水あめを食べた小僧が、茶碗を割って「死んでお詫びしようと毒を食べた」と返す一休咄の古典とんち(水あめの毒)。相手の嘘を逆手に取る。","illustration_scene":"夜、行灯に照らされた寺の板の間に、ふたの開いた空の壺が置かれ、その前に小さな小僧が3人、後ろ姿で正座している。上に大きな「?」。顔は描かない。茶碗は描かない。文字・数字は描かない。"}',
        '類型: とんち(一休咄「水あめの毒」。作者不詳・江戸期の一休咄に由来し広く流布)。流布例: http://hukumusume.com/douwa/amime/jap/j03_19.html , https://news.mynavi.jp/article/20220928-2465292/ , https://tap-biz.jp/lifestyle/trivia/1038435?page=2 , https://detail.chiebukuro.yahoo.co.jp/qa/question_detail/q1011556050 。文面はオリジナルに書き下ろし(表現は書き直し済み)。', 1);

-- C48
INSERT INTO quiz_stock_items (set_id, content_key, quiz_type, difficulty, question_text, answer_text, content_fields, source_note, is_active)
VALUES ((SELECT id FROM batch_sets WHERE set_code = 'logic-training-1'),
        (SELECT CONCAT('night-', LPAD(COALESCE(MAX(CAST(SUBSTRING_INDEX(t.content_key, '-', -1) AS UNSIGNED)), 0) + 1, 3, '0')) FROM (SELECT q.content_key FROM quiz_stock_items q JOIN batch_sets b ON b.id = q.set_id WHERE b.set_code = 'logic-training-1' AND q.content_key LIKE 'night-%') t),
        'L1', 'deep',
        '丸いホールケーキを、ナイフで直線に3回だけ切って8等分にしたい。切ったあとに動かしたり重ねたりしてはいけない。どう切る?',
        '上から十字に2回、横から水平に1回',
        '{"hook":"切り方ひとつで差がつくぞ","hint":"上から見るだけじゃないぞ!","question":"丸いホールケーキを、ナイフで直線に3回だけ切って8等分にしたい。切ったあとに動かしたり重ねたりしてはいけない。どう切る?","answer":"上から十字に2回、横から水平に1回","explanation":"上から十字に切って4等分、最後に横から水平に切って上下に分ければ8等分。平面で4本目を探すと詰まる。ケーキは立体だと思い出せるかが分かれ目だ。","coach_comment":"高さを忘れるな、世界は立体だ!","tags":["発想転換","夜の一問","立体"],"summary":"丸いケーキを直線3回で8等分にする古典パズル。上から十字に2回、横から水平に1回。平面思考から立体へ切り替える(前バッチC39の棒6本と同じ立体化の発想。バッチは別)。","illustration_scene":"夜のダイニングテーブルの上に、切っていない丸いホールケーキと1本のナイフが置かれ、ケーキの上に大きな「?」が浮かぶ。周りに小皿が8枚。文字・数字は描かない。人物は描かない。"}',
        '類型: 立体への発想転換(ケーキを3回で8等分。作者不詳の定番)。流布例: https://nazoq.com/hard/Q030995.html , https://detail.chiebukuro.yahoo.co.jp/qa/question_detail/q1468155074 , https://www.torito.jp/puzzles/308.shtml , https://smart-flash.jp/lifemoney/158343/ 。文面はオリジナルに書き下ろし(表現は書き直し済み)。', 1);

-- C47
INSERT INTO quiz_stock_items (set_id, content_key, quiz_type, difficulty, question_text, answer_text, content_fields, source_note, is_active)
VALUES ((SELECT id FROM batch_sets WHERE set_code = 'logic-training-1'),
        (SELECT CONCAT('night-', LPAD(COALESCE(MAX(CAST(SUBSTRING_INDEX(t.content_key, '-', -1) AS UNSIGNED)), 0) + 1, 3, '0')) FROM (SELECT q.content_key FROM quiz_stock_items q JOIN batch_sets b ON b.id = q.set_id WHERE b.set_code = 'logic-training-1' AND q.content_key LIKE 'night-%') t),
        'L1', 'deep',
        '橋を渡るのに10分かかるが、番人が5分ごとに見回りに来て、見つかると来た方へ追い返される。番人と話さず、誰も傷つけずに向こう岸へ渡るには?',
        '5分弱歩いたら向きを変え、追い返してもらう',
        '{"hook":"見つかると追い返される橋","hint":"追い返される向きを利用しろ!","question":"橋を渡るのに10分かかるが、番人が5分ごとに見回りに来て、見つかると来た方へ追い返される。番人と話さず、誰も傷つけずに向こう岸へ渡るには?","answer":"5分弱歩いたら向きを変え、追い返してもらう","explanation":"渡り始めて5分弱で反対を向いて歩くふりをする。見回りの番人は「向こう岸から来た」と思い、こちらが行きたい岸へ「戻れ」と追い返す。番人の指示に従うだけで渡れる。","coach_comment":"敵のルールを味方につけろ!","tags":["水平思考","夜の一問","逆転"],"summary":"10分かかる橋を5分ごとの番人に追い返されずに渡る古典の水平思考。5分手前で向きを変え、番人に「戻れ」と目的の岸へ追い返してもらう。ルールをそのまま利用する逆転の発想。","illustration_scene":"月明かりの下、長い石橋が霧の川に架かり、橋の中ほどに番人小屋の明かりがともる。橋のたもとに旅人が後ろ姿で立ち、上に大きな「?」。顔は描かない。文字・数字は描かない。"}',
        '類型: 水平思考(橋の番人。作者不詳の定番)。流布例: http://sui-hei.net/mondai/show/5849 , https://www.quiz-puzzle.com/question/74_q.html , https://www.quora.com/If-a-bridge-which-takes-30-mins-to-cross-has-a-guard-situated-in-house-half-way-along-the-bridge-who-checks-every-15mins-to-catch-people-crossing-and-if-caught-he-sends-them-back-the-way-they-came-how-can-you-get 。文面はオリジナルに書き下ろし(表現は書き直し済み)。', 1);
