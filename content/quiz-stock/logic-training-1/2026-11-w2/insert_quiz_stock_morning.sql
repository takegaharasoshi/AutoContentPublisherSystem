-- 2026-11-w2 問題ストック補充投入(朝の先行分 8 問 A90〜A97。レビュー承認後に実行)
-- 生成元: content/quiz-stock/logic-training-1/2026-11-w2/stock_items.py(単一ソース)。適用先: ローカル MySQL / Aurora(acps)
-- set_id は set_code から解決するため両環境共通で実行できる。
-- content_key はスロット内の既存最大連番 + 1 を適用時に解決する(V007。両環境で同一値になる)。

-- A90
INSERT INTO quiz_stock_items (set_id, content_key, quiz_type, difficulty, question_text, answer_text, content_fields, source_note, is_active)
VALUES ((SELECT id FROM batch_sets WHERE set_code = 'logic-training-1'),
        (SELECT CONCAT('morning-', LPAD(COALESCE(MAX(CAST(SUBSTRING_INDEX(t.content_key, '-', -1) AS UNSIGNED)), 0) + 1, 3, '0')) FROM (SELECT q.content_key FROM quiz_stock_items q JOIN batch_sets b ON b.id = q.set_id WHERE b.set_code = 'logic-training-1' AND q.content_key LIKE 'morning-%') t),
        'L1', 'light',
        '0は2より強く、2は5より強く、5は0より強い。これは、なんの話?',
        'じゃんけん(出した指の本数)',
        '{"hook":"算数の先生もびっくりだ!","hint":"数は体のどこかにあるぞ!","question":"0は2より強く、2は5より強く、5は0より強い。これは、なんの話?","answer":"じゃんけん(出した指の本数)","explanation":"グーは指0本、チョキは2本、パーは5本。グーはチョキに、チョキはパーに、パーはグーに勝つ。数は、出した指の本数だった。","coach_comment":"あいこなしで一発正解だ!","tags":["なぞなぞ","朝の一問","法則発見"],"summary":"0は2より、2は5より、5は0より強いという三すくみを見せ、何の話かを問う法則発見。答えはじゃんけん(グー0本・チョキ2本・パー5本の指の本数)。","illustration_scene":"朝日が差し込む教室。黒板に白いチョークで大きく、上から「0 > 2」「2 > 5」「5 > 0」の3行だけが書いてある。黒板の右上に大きな「?」。教卓の上に金色の優勝カップが1つ。人物と、この3行と「?」以外の文字は描かない。"}',
        '類型: 数の大小に見えて実は出した指の本数の三すくみ(作者不詳のなぞなぞ)。流布例: https://answer-q.com/2013/11/blog-post_7.html/ ・ https://quiz.community.fmworld.net/nazonazo/content/328/answer1.html?answer=none (2026-11-12 に直接開いて確認)。文面はオリジナルに書き下ろし(表現は書き直し済み)。', 1);

-- A91
INSERT INTO quiz_stock_items (set_id, content_key, quiz_type, difficulty, question_text, answer_text, content_fields, source_note, is_active)
VALUES ((SELECT id FROM batch_sets WHERE set_code = 'logic-training-1'),
        (SELECT CONCAT('morning-', LPAD(COALESCE(MAX(CAST(SUBSTRING_INDEX(t.content_key, '-', -1) AS UNSIGNED)), 0) + 1, 3, '0')) FROM (SELECT q.content_key FROM quiz_stock_items q JOIN batch_sets b ON b.id = q.set_id WHERE b.set_code = 'logic-training-1' AND q.content_key LIKE 'morning-%') t),
        'L1', 'light',
        'まず着ているものをはがして捨て、残りをゆでる。次に外側だけを食べて、残った真ん中を捨てる。なんだ?',
        'とうもろこし',
        '{"hook":"捨てて食べて、また捨てる!","hint":"ひげも生えているぞ!","question":"まず着ているものをはがして捨て、残りをゆでる。次に外側だけを食べて、残った真ん中を捨てる。なんだ?","answer":"とうもろこし","explanation":"とうもろこしは、まず皮をむいて捨て、実をゆでる。食べるのは外側にならぶ粒だけで、真ん中に残った芯は捨てる。","coach_comment":"粒ぞろいの名答だったぞ!","tags":["なぞなぞ","朝の一問","言葉あそび"],"summary":"着ているものをはがして捨て、ゆでて、外側を食べ真ん中を捨てるものを問うなぞ。答えはとうもろこし(皮→粒→芯)。英語圏の伝承なぞを日本語に書き下ろした。","illustration_scene":"朝日が差す台所。湯気の立つ大きな鍋の前に後ろ姿の人が立ち、脱いだばかりの上着を片手でごみ箱に入れようとしている。調理台にまな板と塩のびん、窓の外に朝日。鍋の上に大きな「?」。顔は描かない。「?」以外の文字は描かない。"}',
        '類型: 外を捨て中を調理し、外を食べ中を捨てる 2 段の反転(作者不詳・英語圏の伝承なぞ。日本語サイトにも流布)。流布例: https://www.nazo2.net/suiri/025.html ・ https://quiz.community.fmworld.net/nazonazo/content/301/answer3.html?answer=none ・ https://www.fatherly.com/entertainment/66-brain-teasers-for-adults-kids-and-everyone-in-between (2026-11-12 に直接開いて確認)。文面はオリジナルに書き下ろし(表現は書き直し済み)。', 1);

-- A92
INSERT INTO quiz_stock_items (set_id, content_key, quiz_type, difficulty, question_text, answer_text, content_fields, source_note, is_active)
VALUES ((SELECT id FROM batch_sets WHERE set_code = 'logic-training-1'),
        (SELECT CONCAT('morning-', LPAD(COALESCE(MAX(CAST(SUBSTRING_INDEX(t.content_key, '-', -1) AS UNSIGNED)), 0) + 1, 3, '0')) FROM (SELECT q.content_key FROM quiz_stock_items q JOIN batch_sets b ON b.id = q.set_id WHERE b.set_code = 'logic-training-1' AND q.content_key LIKE 'morning-%') t),
        'L1', 'light',
        'ひとりのときは男なのに、「人」がとなりに来たとたん女になってしまう漢字がある。どの字だ?',
        '夫(「夫人」になると女性)',
        '{"hook":"男が女に早変わりだ!","hint":"二字の言葉にしてみろ!","question":"ひとりのときは男なのに、「人」がとなりに来たとたん女になってしまう漢字がある。どの字だ?","answer":"夫(「夫人」になると女性)","explanation":"「夫」は結婚した男性を指す字。ところが後ろに「人」がつくと「夫人」になり、他人の妻をうやまって呼ぶ言葉に変わる。","coach_comment":"字も人も、となり次第だな!","tags":["なぞなぞ","朝の一問","漢字パズル"],"summary":"単独では男を表すが「人」がつくと女性を指す言葉になる漢字を問う。答えは夫(夫人)。字形ではなく熟語の意味で解く漢字なぞ。","illustration_scene":"朝日が差す公園のベンチ。左に帽子と背広の男性が後ろ姿で座り、その右どなりの空いた席に大きな「?」が置かれている。ベンチの後ろに花壇と噴水、木々の間から朝日。顔は描かない。「?」以外の文字は描かない。"}',
        '類型: 夫 → 夫人で性別が変わる漢字なぞ(作者不詳)。流布例: https://answer-q.com/2013/04/q_1441.html/ ・ https://nazoq.com/hardest/Q031045.html (2026-11-12 に直接開いて確認)。文面はオリジナルに書き下ろし(表現は書き直し済み)。', 1);

-- A93
INSERT INTO quiz_stock_items (set_id, content_key, quiz_type, difficulty, question_text, answer_text, content_fields, source_note, is_active)
VALUES ((SELECT id FROM batch_sets WHERE set_code = 'logic-training-1'),
        (SELECT CONCAT('morning-', LPAD(COALESCE(MAX(CAST(SUBSTRING_INDEX(t.content_key, '-', -1) AS UNSIGNED)), 0) + 1, 3, '0')) FROM (SELECT q.content_key FROM quiz_stock_items q JOIN batch_sets b ON b.id = q.set_id WHERE b.set_code = 'logic-training-1' AND q.content_key LIKE 'morning-%') t),
        'L1', 'light',
        'マッチ棒が4本ある。折らず、切らずに、この4本だけで漢字の「田」を作ってくれ。',
        '4本を束ねて、軸の切り口を見る',
        '{"hook":"たった4本でできるぞ!","hint":"並べるとは言ってないぞ!","question":"マッチ棒が4本ある。折らず、切らずに、この4本だけで漢字の「田」を作ってくれ。","answer":"4本を束ねて、軸の切り口を見る","explanation":"日本のマッチ棒の軸は、ふつう四角い。4本を2本ずつ2段に束ねて、頭の反対側から見ると、4つの四角い切り口がならんで「田」の形になる。","coach_comment":"見る向きを変えれば道は開く!","tags":["なぞなぞ","朝の一問","マッチ棒パズル"],"summary":"マッチ棒4本を折らず切らずに「田」を作る視覚パズル。並べるのではなく2本ずつ2段に束ね、四角い軸の端の面を見ると田に見える。見る向きの転換。","illustration_scene":"朝日が差す木の机の上に、角ばった木の軸に赤い頭のマッチ棒が4本、ばらばらの向きで横たわっている。そばに、引き出しを半分あけた無地のマッチ箱と湯のみ。机の右上の空いたところに大きな「?」。人物と「?」以外の文字は描かない。"}',
        '類型: マッチ棒 4 本を束ねて端の面で田を作る視覚パズル(作者不詳)。流布例: https://nazoq.com/hardest/Q030994.html ・ https://king.mineo.jp/reports/102150 (2026-11-12 に直接開いて確認)。文面はオリジナルに書き下ろし(表現は書き直し済み)。', 1);

-- A94
INSERT INTO quiz_stock_items (set_id, content_key, quiz_type, difficulty, question_text, answer_text, content_fields, source_note, is_active)
VALUES ((SELECT id FROM batch_sets WHERE set_code = 'logic-training-1'),
        (SELECT CONCAT('morning-', LPAD(COALESCE(MAX(CAST(SUBSTRING_INDEX(t.content_key, '-', -1) AS UNSIGNED)), 0) + 1, 3, '0')) FROM (SELECT q.content_key FROM quiz_stock_items q JOIN batch_sets b ON b.id = q.set_id WHERE b.set_code = 'logic-training-1' AND q.content_key LIKE 'morning-%') t),
        'L1', 'light',
        '作った人は、だれにも言わない。受け取った人は、気づかない。気づいた人は、受け取らない。なんだ?',
        'にせ札(にせブランド品など、にせ物全般も正解だぞ)',
        '{"hook":"3人とも態度がちがうぞ!","hint":"なぜ言わないのか考えろ!","question":"作った人は、だれにも言わない。受け取った人は、気づかない。気づいた人は、受け取らない。なんだ?","answer":"にせ札(にせブランド品など、にせ物全般も正解だぞ)","explanation":"にせ札を作った人は、もちろん黙っている。受け取る人は本物だと思うから受け取り、にせ物と気づいた人は受け取らない。","coach_comment":"本物を見抜く目をきたえろ!","tags":["なぞなぞ","朝の一問","言葉あそび"],"summary":"作った人は言わず、受け取った人は気づかず、気づいた人は受け取らないものを問うなぞ。答えはにせ札(にせ物全般も正解)。3者の態度から当てる伝承なぞ(英語圏・日本語サイトにも流布)。","illustration_scene":"朝日が差す木のテーブルを斜め上から見た構図。左から伸びた手が、リボンのかかった小さな箱を差し出し、右から伸びた手は手のひらを立てて断っている。箱の上に大きな「?」。テーブルには湯気の立つカップと花びん。手より先の体と顔は描かない。「?」以外の文字は描かない。"}',
        '類型: 作る人・受け取る人・気づく人の 3 者の態度から当てる伝承なぞ(作者不詳)。流布例: https://www.nazo2.net/tyuukyuu/134.html ・ https://nazoq.com/hardest/Q002698.html (2026-11-12 に直接開いて確認。後者は答えの表記が「偽物」寄り)。文面はオリジナルに書き下ろし(表現は書き直し済み)。', 1);

-- A95
INSERT INTO quiz_stock_items (set_id, content_key, quiz_type, difficulty, question_text, answer_text, content_fields, source_note, is_active)
VALUES ((SELECT id FROM batch_sets WHERE set_code = 'logic-training-1'),
        (SELECT CONCAT('morning-', LPAD(COALESCE(MAX(CAST(SUBSTRING_INDEX(t.content_key, '-', -1) AS UNSIGNED)), 0) + 1, 3, '0')) FROM (SELECT q.content_key FROM quiz_stock_items q JOIN batch_sets b ON b.id = q.set_id WHERE b.set_code = 'logic-training-1' AND q.content_key LIKE 'morning-%') t),
        'L1', 'light',
        'ひっくり返すと、ひらがなの「と」になってしまう漢字が1文字ある。どの字だ?',
        '歩(将棋の駒。裏返すと「と」)',
        '{"hook":"漢字がひらがなに化ける!","hint":"紙に書いた字とは限らないぞ!","question":"ひっくり返すと、ひらがなの「と」になってしまう漢字が1文字ある。どの字だ?","answer":"歩(将棋の駒。裏返すと「と」)","explanation":"将棋の「歩」は、敵の陣地に入ると裏返して「成る」ことができる。裏に書かれた字は「と」と読まれ、この駒を「と金」と呼ぶ。","coach_comment":"一歩ずつ進めば金になる!","tags":["なぞなぞ","朝の一問","発想転換"],"summary":"ひっくり返すとひらがなの「と」になる漢字を問う。答えは将棋の歩(成ると裏の「と」= と金)。文字の反転に見せて将棋の駒へ領域を飛ばす。","illustration_scene":"朝日が差す教室の前。後ろ姿の人が、白い大きなフリップを両手で上下逆さまに持って掲げている。フリップには太い黒字のひらがな「と」が1文字だけ、上下逆さまの向きで書かれて見える。フリップの右上に大きな「?」。窓の外に朝日。顔は描かない。逆さの「と」と「?」以外の文字は描かない。"}',
        '類型: ひっくり返すと「と」になる漢字 = 将棋の歩(作者不詳のなぞなぞ)。流布例: https://answer-q.com/2013/04/blog-post_9383.html/ (2026-11-12 に直接開いて確認)。要注意: 確認できたのは1ドメインのみ。文面はオリジナルに書き下ろし(表現は書き直し済み)。', 1);

-- A96
INSERT INTO quiz_stock_items (set_id, content_key, quiz_type, difficulty, question_text, answer_text, content_fields, source_note, is_active)
VALUES ((SELECT id FROM batch_sets WHERE set_code = 'logic-training-1'),
        (SELECT CONCAT('morning-', LPAD(COALESCE(MAX(CAST(SUBSTRING_INDEX(t.content_key, '-', -1) AS UNSIGNED)), 0) + 1, 3, '0')) FROM (SELECT q.content_key FROM quiz_stock_items q JOIN batch_sets b ON b.id = q.set_id WHERE b.set_code = 'logic-training-1' AND q.content_key LIKE 'morning-%') t),
        'L1', 'light',
        '1つだと赤いのに、2つならぶと白くなる。なんだ?',
        'ひらがなの「ち」(血と乳)',
        '{"hook":"赤が白に変わる!?","hint":"声に出して2回言え!","question":"1つだと赤いのに、2つならぶと白くなる。なんだ?","answer":"ひらがなの「ち」(血と乳)","explanation":"「ち」は血で、赤い。2つならべた「ちち」は乳で、白い。同じ1文字が、ならぶ数で色まで変わる。","coach_comment":"血のめぐりがよくなったな!","tags":["なぞなぞ","朝の一問","言葉あそび"],"summary":"1つだと赤く、2つならぶと白くなるものを問う言葉なぞ。答えはひらがなの「ち」(血は赤・ちち=乳は白)。morning-014 と同じ字だが解き方は別(同音の意味)。","illustration_scene":"朝日が差す窓辺の木のテーブル。左の皿に赤いボールが1つ、右の皿に白いボールが2つならんでいる。2つの皿の間に大きな「?」。奥に花びんと、風でゆれるカーテン、窓の外に朝日。人物と「?」以外の文字は描かない。"}',
        '類型: ち = 血(赤)・ちち = 乳(白)の同音の言葉なぞ(作者不詳)。流布例: https://answer-q.com/2013/03/blog-post_5272.html/ (2026-11-12 に直接開いて確認)。要注意: 確認できたのは1ドメインのみ。文面はオリジナルに書き下ろし(表現は書き直し済み)。', 1);

-- A97
INSERT INTO quiz_stock_items (set_id, content_key, quiz_type, difficulty, question_text, answer_text, content_fields, source_note, is_active)
VALUES ((SELECT id FROM batch_sets WHERE set_code = 'logic-training-1'),
        (SELECT CONCAT('morning-', LPAD(COALESCE(MAX(CAST(SUBSTRING_INDEX(t.content_key, '-', -1) AS UNSIGNED)), 0) + 1, 3, '0')) FROM (SELECT q.content_key FROM quiz_stock_items q JOIN batch_sets b ON b.id = q.set_id WHERE b.set_code = 'logic-training-1' AND q.content_key LIKE 'morning-%') t),
        'L1', 'light',
        '黒い犬と白い犬がいる。どんなときも絶対にほえないのは、どっちだ?',
        '黒い犬(黒+犬=黙)',
        '{"hook":"静かな犬には訳がある!","hint":"字を書いて考えてみろ!","question":"黒い犬と白い犬がいる。どんなときも絶対にほえないのは、どっちだ?","answer":"黒い犬(黒+犬=黙)","explanation":"「黒」と「犬」を横にならべると、だまるという意味の「黙」になる。「白」と「犬」をならべても、そういう字にはならない。","coach_comment":"黙って解くとは見事だ!","tags":["なぞなぞ","朝の一問","漢字パズル"],"summary":"黒い犬と白い犬のうち絶対にほえないほうを問う漢字なぞ。答えは黒い犬(黒+犬=黙)。字の成り立ちで解く。","illustration_scene":"朝日が差す庭の芝生に、黒い犬と白い犬がならんで座っている。2匹とも口を閉じてこちらを見ている。後ろに犬小屋と木の柵、木の向こうに朝日。2匹の間の上に大きな「?」。人物と「?」以外の文字は描かない。"}',
        '類型: 黒 + 犬 = 黙の漢字なぞ(作者不詳)。流布例: https://www.nazo2.net/kanji/061.html (2026-11-12 に直接開いて確認)。要注意: 確認できたのは1ドメインのみ。文面はオリジナルに書き下ろし(表現は書き直し済み)。', 1);

