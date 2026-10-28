-- 2026-10-w4 問題ストック補充投入(14 問。レビュー承認後に実行)
-- 生成元: content/quiz-stock/logic-training-1/2026-10-w4/stock_items.py(単一ソース)。適用先: ローカル MySQL / Aurora(acps)
-- set_id は set_code から解決するため両環境共通で実行できる。
-- content_key はスロット内の既存最大連番 + 1 を適用時に解決する(V007。両環境で同一値になる)。

-- A76
INSERT INTO quiz_stock_items (set_id, content_key, quiz_type, difficulty, question_text, answer_text, content_fields, source_note, is_active)
VALUES ((SELECT id FROM batch_sets WHERE set_code = 'logic-training-1'),
        (SELECT CONCAT('morning-', LPAD(COALESCE(MAX(CAST(SUBSTRING_INDEX(t.content_key, '-', -1) AS UNSIGNED)), 0) + 1, 3, '0')) FROM (SELECT q.content_key FROM quiz_stock_items q JOIN batch_sets b ON b.id = q.set_id WHERE b.set_code = 'logic-training-1' AND q.content_key LIKE 'morning-%') t),
        'L1', 'light',
        '目がひとつあるのに、何も見えない。まわりは大荒れなのに、その目の中だけは静かで、青空がのぞくこともある。これなあに?',
        '台風',
        '{"hook":"天気予報、毎朝見てるか?","hint":"空の上から見てみろ!","question":"目がひとつあるのに、何も見えない。まわりは大荒れなのに、その目の中だけは静かで、青空がのぞくこともある。これなあに?","answer":"台風","explanation":"台風の中心は「台風の目」と呼ばれる。まわりは強い風と雨でも、目の中は風が弱く、晴れ間がのぞくこともある。何も見えない目の正体だ。","coach_comment":"目のつけどころが鋭いぞ!","tags":["なぞなぞ","朝の一問","言葉あそび"],"summary":"目が1つあるのに見えず、まわりは大荒れでも目の中だけ静かなものを問うなぞ。答えは台風(台風の目)。英語圏の定番 riddle の答えの1つを日本の台風に置き換えた。","illustration_scene":"朝日が差し込む和室で、コミカルな一つ目小僧が両手をぶんぶん振り回して大暴れしている。座布団や湯のみや紙くずが宙を舞い、障子が破れている。小僧の大きな1つの目はぐるぐる目を回している。部屋の上に大きな「?」。人間・「?」以外の文字は描かない。"}',
        '類型: 目があるのに見えないもの(英語圏の riddle「What has an eye but cannot see?」の答えの1つ hurricane / storm)を日本の台風に置き換え(作者不詳)。流布例: https://unanswered.io/guide/what-has-eyes-but-cannot-see-riddles 。要注意: 確認できたのは英語1ドメインのみ。文面はオリジナルに書き下ろし(表現は書き直し済み)。', 1);

-- A77
INSERT INTO quiz_stock_items (set_id, content_key, quiz_type, difficulty, question_text, answer_text, content_fields, source_note, is_active)
VALUES ((SELECT id FROM batch_sets WHERE set_code = 'logic-training-1'),
        (SELECT CONCAT('morning-', LPAD(COALESCE(MAX(CAST(SUBSTRING_INDEX(t.content_key, '-', -1) AS UNSIGNED)), 0) + 1, 3, '0')) FROM (SELECT q.content_key FROM quiz_stock_items q JOIN batch_sets b ON b.id = q.set_id WHERE b.set_code = 'logic-training-1' AND q.content_key LIKE 'morning-%') t),
        'L1', 'light',
        'この式はこのままでは正しくない。マッチ棒を1本も動かさず、足しも消しもせずに、正しい式にしてくれ。',
        '黒板を逆さにして見る(X=IX+I)',
        '{"hook":"動かさずに直せるか?","hint":"見る向きは1つじゃないぞ!","question":"この式はこのままでは正しくない。マッチ棒を1本も動かさず、足しも消しもせずに、正しい式にしてくれ。","answer":"黒板を逆さにして見る(X=IX+I)","explanation":"I+XI=Xは1+11=10でまちがい。黒板を逆さに見ると「X=IX+I」、10=9+1で正しくなる。鏡に映しても同じく読める。変えるのは見る向きだ。","coach_comment":"発想をひっくり返したな!","tags":["なぞなぞ","朝の一問","視覚パズル"],"summary":"マッチ棒のローマ数字の式I+XI=Xを、棒を動かさずに正す定番。黒板を逆さに見るとX=IX+I(10=9+1)になる。棒ではなく見る向きを変える。","illustration_scene":"朝日が差し込む教室の黒板に、平らな木の角棒のマッチ棒で作った式「I+XI=X」が大きく横一列に並ぶ。黒板の右上に大きな「?」。人物と、式と「?」以外の文字や数字は描かない。"}',
        '類型: マッチ棒のローマ数字の式を動かさずに正す=逆さに見る(作者不詳・英語圏のマッチ棒パズル)。流布例: https://www.riddles.com/6393 。要注意: 開いて確認できたのは1ドメインのみ。文面はオリジナルに書き下ろし(表現は書き直し済み)。', 1);

-- A78
INSERT INTO quiz_stock_items (set_id, content_key, quiz_type, difficulty, question_text, answer_text, content_fields, source_note, is_active)
VALUES ((SELECT id FROM batch_sets WHERE set_code = 'logic-training-1'),
        (SELECT CONCAT('morning-', LPAD(COALESCE(MAX(CAST(SUBSTRING_INDEX(t.content_key, '-', -1) AS UNSIGNED)), 0) + 1, 3, '0')) FROM (SELECT q.content_key FROM quiz_stock_items q JOIN batch_sets b ON b.id = q.set_id WHERE b.set_code = 'logic-training-1' AND q.content_key LIKE 'morning-%') t),
        'L1', 'light',
        '漢字の「口」に、2画だけ書き足してできる漢字はいくつ思いつく? 15個見つけたら名人だ。',
        '田・目・由・甲・申・旧・古・右・石・兄 など',
        '{"hook":"漢字の名人、いるか?","hint":"外にも中にも足していいぞ!","question":"漢字の「口」に、2画だけ書き足してできる漢字はいくつ思いつく? 15個見つけたら名人だ。","answer":"田・目・由・甲・申・旧・古・右・石・兄 など","explanation":"中に足せば田・目・由・甲・申・四、外に足せば旧・古・右・石・兄・只・史・台・叶・加・可・句。全部で20字以上ある。いくつ見つけられた?","coach_comment":"漢字博士の素質ありだ!","tags":["なぞなぞ","朝の一問","漢字パズル"],"summary":"漢字の「口」に2画足してできる漢字を挙げる定番の漢字パズル。田・目・由・甲・申・旧・古・右・石・兄など20字以上ある。数を競う参加型。","illustration_scene":"朝日が差し込む教室の黒板の真ん中に、白いチョークで大きな漢字「口」が1字だけ書いてある。黒板の右上に大きな「?」。黒板の下にチョークが数本。人物と、「口」と「?」以外の文字は描かない。"}',
        '類型: 口に二画足してできる漢字を挙げる漢字パズル(作者不詳・テレビのクイズ番組等で流布)。流布例: https://www.dwc.doshisha.ac.jp/research/faculty_column/2018-11-08-09-20 。要注意: 字の一覧まで開いて確認できたのは1ドメインのみ。文面はオリジナルに書き下ろし(表現は書き直し済み)。', 1);

-- A79
INSERT INTO quiz_stock_items (set_id, content_key, quiz_type, difficulty, question_text, answer_text, content_fields, source_note, is_active)
VALUES ((SELECT id FROM batch_sets WHERE set_code = 'logic-training-1'),
        (SELECT CONCAT('morning-', LPAD(COALESCE(MAX(CAST(SUBSTRING_INDEX(t.content_key, '-', -1) AS UNSIGNED)), 0) + 1, 3, '0')) FROM (SELECT q.content_key FROM quiz_stock_items q JOIN batch_sets b ON b.id = q.set_id WHERE b.set_code = 'logic-training-1' AND q.content_key LIKE 'morning-%') t),
        'L1', 'light',
        'Tで始まり、Tで終わり、中にもTが入っているものは? 台所にあるぞ。',
        'teapot(ティーポット。中にtea=ティーが入っている)',
        '{"hook":"英語のなぞなぞ、いくぞ!","hint":"中のTは文字ではないぞ!","question":"Tで始まり、Tで終わり、中にもTが入っているものは? 台所にあるぞ。","answer":"teapot(ティーポット。中にtea=ティーが入っている)","explanation":"teapot(ティーポット)はTで始まりTで終わる。そして中に入っているのはtea(ティー=お茶)。文字のTと飲み物のティーを掛けたなぞなぞだ。","coach_comment":"お茶でも飲んで一息だ!","tags":["なぞなぞ","朝の一問","英語なぞ"],"summary":"Tで始まりTで終わり、中にTが入っているものを問う英語圏の定番なぞ。答えはteapot。つづりのTと、中に入っているtea(お茶)を掛ける。","illustration_scene":"朝日が差し込む台所のテーブルに、白い無地のカードが1枚立ててある。カードには大きく「T … T」と書いてある。テーブルの上はカードと、緑の葉の小さな観葉植物の鉢だけ。カードの右上に大きな「?」。人物と、「T … T」「?」以外の文字は描かない。"}',
        '類型: Tで始まりTで終わり中にTがあるもの=teapot(作者不詳・英語圏の定番 riddle)。流布例: https://eikaiwa.dmm.com/blog/learning-english/tips/riddle/ ・ https://nativecamp.net/blog/20200704_riddle 。文面はオリジナルに書き下ろし(表現は書き直し済み)。', 1);

-- A80
INSERT INTO quiz_stock_items (set_id, content_key, quiz_type, difficulty, question_text, answer_text, content_fields, source_note, is_active)
VALUES ((SELECT id FROM batch_sets WHERE set_code = 'logic-training-1'),
        (SELECT CONCAT('morning-', LPAD(COALESCE(MAX(CAST(SUBSTRING_INDEX(t.content_key, '-', -1) AS UNSIGNED)), 0) + 1, 3, '0')) FROM (SELECT q.content_key FROM quiz_stock_items q JOIN batch_sets b ON b.id = q.set_id WHERE b.set_code = 'logic-training-1' AND q.content_key LIKE 'morning-%') t),
        'L1', 'light',
        '片手の指は5本。ふつうに数えれば5までだ。でも数え方を工夫すると、片手だけで31まで数えられる。どうやる?',
        '指の立て・曲げを2進数の各けたに使う',
        '{"hook":"朝の指体操、いくぞ!","hint":"指ごとに重さを変えてみろ!","question":"片手の指は5本。ふつうに数えれば5までだ。でも数え方を工夫すると、片手だけで31まで数えられる。どうやる?","answer":"指の立て・曲げを2進数の各けたに使う","explanation":"親指を1、人差し指を2、中指を4、薬指を8、小指を16と決め、立てた指の値を足す。全部立てれば31。両手なら1023まで数えられるぞ。","coach_comment":"指の使い方が天才的だ!","tags":["なぞなぞ","朝の一問","参加型"],"summary":"片手の指だけで31まで数える方法を問う定番。指に1・2・4・8・16を割り当て、立てた指の値を足す2進数の数え方。視聴者がその場で試せる参加型。","illustration_scene":"自分の目で手元を見下ろした一人称視点の構図。画面の右下の角から自分の右手が手首から先だけ伸び、5本の指を開いた手のひらを上に向けて(右手の手のひらなので親指は手の右側)、真上から見下ろしている。手の下は朝日が差し込む窓辺の木の机。手の上に大きな「?」。手以外の人物は描かない。「?」以外の文字や数字は描かない。"}',
        '類型: 指を2進数のけたに使って片手で31まで数える(作者不詳の数え方の小技)。流布例: https://gigazine.net/news/20080512_count_to_31_on_one_hand ・ https://mail.keithwiley.com/mindWanderings/fingerCounting.shtml 。文面はオリジナルに書き下ろし(表現は書き直し済み)。', 1);

-- A81
INSERT INTO quiz_stock_items (set_id, content_key, quiz_type, difficulty, question_text, answer_text, content_fields, source_note, is_active)
VALUES ((SELECT id FROM batch_sets WHERE set_code = 'logic-training-1'),
        (SELECT CONCAT('morning-', LPAD(COALESCE(MAX(CAST(SUBSTRING_INDEX(t.content_key, '-', -1) AS UNSIGNED)), 0) + 1, 3, '0')) FROM (SELECT q.content_key FROM quiz_stock_items q JOIN batch_sets b ON b.id = q.set_id WHERE b.set_code = 'logic-training-1' AND q.content_key LIKE 'morning-%') t),
        'L1', 'light',
        'この7本のマッチ棒を、折ったり裂いたりせずに「10本」にしてくれ。動かすのはOKだ。',
        '漢字で「十本」と並べる(十が2本・本が5本で7本)',
        '{"hook":"棒が増える魔法、あるか?","hint":"数字だけが「10」じゃないぞ!","question":"この7本のマッチ棒を、折ったり裂いたりせずに「10本」にしてくれ。動かすのはOKだ。","answer":"漢字で「十本」と並べる(十が2本・本が5本で7本)","explanation":"棒の数は増やせない。でも7本で漢字の「十」(2本)と「本」(5本)を作れば、黒板には「十本」と書いてある。数ではなく文字にするのが答えだ。","coach_comment":"言葉の力で増やしたな!","tags":["なぞなぞ","朝の一問","視覚パズル"],"summary":"マッチ棒7本を折らずに「10本」にするとんちパズル。7本で漢字の「十本」(十が2本・本が5本)を作る。本数ではなく文字にする発想。","illustration_scene":"朝日が差し込む教室の黒板に、平らな木の角棒のマッチ棒7本が、縦向きに等間隔で横一列に並ぶ。どの棒も赤い頭は上の端に1つだけ。黒板の右上に大きな「?」。人物・「?」以外の文字や数字は描かない。"}',
        '類型: マッチ棒7本を折らずに「10本」にする=漢字で十本と並べる(作者不詳のとんちクイズ)。流布例: https://www.ragnet.co.jp/matchstick-quiz 。要注意: 問題と答えを確認できたのは1ドメインのみ。文面はオリジナルに書き下ろし(表現は書き直し済み)。', 1);

-- A82
INSERT INTO quiz_stock_items (set_id, content_key, quiz_type, difficulty, question_text, answer_text, content_fields, source_note, is_active)
VALUES ((SELECT id FROM batch_sets WHERE set_code = 'logic-training-1'),
        (SELECT CONCAT('morning-', LPAD(COALESCE(MAX(CAST(SUBSTRING_INDEX(t.content_key, '-', -1) AS UNSIGNED)), 0) + 1, 3, '0')) FROM (SELECT q.content_key FROM quiz_stock_items q JOIN batch_sets b ON b.id = q.set_id WHERE b.set_code = 'logic-training-1' AND q.content_key LIKE 'morning-%') t),
        'L1', 'light',
        '漢字の「大」に、1画だけ書き足してできる漢字はいくつ思いつく? 4つ見つけたら合格だ。',
        '犬・太・天・夫 など',
        '{"hook":"たった1画で別の字だ!","hint":"点や線をどこに足すかだ!","question":"漢字の「大」に、1画だけ書き足してできる漢字はいくつ思いつく? 4つ見つけたら合格だ。","answer":"犬・太・天・夫 など","explanation":"右上に点で犬、下に点で太、上に横線で天、上のほうに横線を通して夫。たった1画で、まったく別の字になる。","coach_comment":"1画の差に気づけたな!","tags":["なぞなぞ","朝の一問","漢字パズル"],"summary":"漢字の「大」に1画足してできる漢字を挙げる定番の漢字パズル。犬・太・天・夫など。点や横線1本の位置で別の字になる。数を競う参加型。","illustration_scene":"朝日が差し込む教室の黒板の真ん中に、白いチョークで大きな漢字「大」が1字だけ書いてある。黒板の右上に大きな「?」。黒板の下にチョークが数本。人物と、「大」と「?」以外の文字は描かない。"}',
        '類型: 大に一画足してできる漢字を挙げる漢字パズル(作者不詳・一画足しの漢字遊び)。流布例: https://kotonohaweb.net/kanji-1kaku/ 。要注意: 開いて確認できたのは1ドメインのみ(犬・太は字形から確認)。文面はオリジナルに書き下ろし(表現は書き直し済み)。', 1);

-- C77
INSERT INTO quiz_stock_items (set_id, content_key, quiz_type, difficulty, question_text, answer_text, content_fields, source_note, is_active)
VALUES ((SELECT id FROM batch_sets WHERE set_code = 'logic-training-1'),
        (SELECT CONCAT('night-', LPAD(COALESCE(MAX(CAST(SUBSTRING_INDEX(t.content_key, '-', -1) AS UNSIGNED)), 0) + 1, 3, '0')) FROM (SELECT q.content_key FROM quiz_stock_items q JOIN batch_sets b ON b.id = q.set_id WHERE b.set_code = 'logic-training-1' AND q.content_key LIKE 'night-%') t),
        'L1', 'deep',
        '線路の上を歩いていた男。前から列車が来た。男は後ろへ逃げずに、なんと列車のほうへ走りだして、助かった。なぜ?',
        '鉄橋の上にいて、列車側の橋のたもとが近かったから',
        '{"hook":"列車に向かって走るだと!?","hint":"男がいた場所をよく考えろ!","question":"線路の上を歩いていた男。前から列車が来た。男は後ろへ逃げずに、なんと列車のほうへ走りだして、助かった。なぜ?","answer":"鉄橋の上にいて、列車側の橋のたもとが近かったから","explanation":"男がいたのは鉄橋の上で、横には逃げ場がなかった。残りの距離は前のほうが短い。列車に向かって走り、先に渡りきって線路の外へよけたのだ。","coach_comment":"逃げ方にも知恵がいるな!","tags":["水平思考","夜の一問","状況パズル"],"summary":"線路で列車に向かって走った男が助かった理由を問う水平思考の定番。男は鉄橋の上にいて、列車側の橋のたもとのほうが近かった。橋は答えの側で明かす。","illustration_scene":"夜、まっすぐ伸びる線路のずっと先に、近づいてくる列車の丸いライトが2つ光る。線路の両わきは闇に沈んで何も見えない。見えるのはライトに照らされた2本のレールと枕木だけ。線路の上に大きな「?」。人物・「?」以外の文字は描かない。"}',
        '類型: 線路で列車に向かって走った=鉄橋の上で列車側のたもとが近かった(作者不詳・英語圏の lateral thinking の定番)。流布例: https://ahaslides.com/blog/lateral-thinking-puzzles/ ・ https://mathlair.allfunandgames.ca/lateralanswers.php 。文面はオリジナルに書き下ろし(表現は書き直し済み)。', 1);

-- C78
INSERT INTO quiz_stock_items (set_id, content_key, quiz_type, difficulty, question_text, answer_text, content_fields, source_note, is_active)
VALUES ((SELECT id FROM batch_sets WHERE set_code = 'logic-training-1'),
        (SELECT CONCAT('night-', LPAD(COALESCE(MAX(CAST(SUBSTRING_INDEX(t.content_key, '-', -1) AS UNSIGNED)), 0) + 1, 3, '0')) FROM (SELECT q.content_key FROM quiz_stock_items q JOIN batch_sets b ON b.id = q.set_id WHERE b.set_code = 'logic-training-1' AND q.content_key LIKE 'night-%') t),
        'L1', 'deep',
        'コーヒーにハエが入っていた。作り直しを頼んだが、出てきたコーヒーをひと口飲んで怒った。「作り直していない、さっきのハエが入っていたコーヒーだ!」なぜ分かった?',
        '先に砂糖を入れていて、甘かったから',
        '{"hook":"この客、鋭すぎる!","hint":"男が先にしたことは何だ?","question":"コーヒーにハエが入っていた。作り直しを頼んだが、出てきたコーヒーをひと口飲んで怒った。「作り直していない、さっきのハエが入っていたコーヒーだ!」なぜ分かった?","answer":"先に砂糖を入れていて、甘かったから","explanation":"男はハエに気づく前に、もう砂糖を入れていた。新しいはずのコーヒーが甘かったので、ハエだけ取り出した同じカップだと分かったのだ。","coach_comment":"味で見抜くとは名探偵だ!","tags":["水平思考","夜の一問","推理"],"summary":"ハエ入りのコーヒーを取り替えてもらった男が、同じコーヒーだと見抜いた理由を問う水平思考の定番。先に砂糖を入れていたので甘かった。","illustration_scene":"夜の喫茶店のカウンター。暖かい電球の明かりの下に、湯気の立つコーヒーカップが1つ。カップの横は伝票と、一輪挿しの小さな花だけ。カップの上に大きな「?」。人物・「?」以外の文字は描かない。"}',
        '類型: 取り替えたはずのコーヒーが同じだと見抜く=先に砂糖を入れていた(作者不詳・英語圏の lateral thinking の定番)。流布例: https://www.puzzlesandriddles.com/LateralThinking10.html ・ https://www.riddlesandanswers.com/v/231004/a-man-walks-into-a-diner-and-sits-down-theres-a-new-waitress-working-that-hes-never-seen-before/ 。文面はオリジナルに書き下ろし(表現は書き直し済み)。', 1);

-- C79
INSERT INTO quiz_stock_items (set_id, content_key, quiz_type, difficulty, question_text, answer_text, content_fields, source_note, is_active)
VALUES ((SELECT id FROM batch_sets WHERE set_code = 'logic-training-1'),
        (SELECT CONCAT('night-', LPAD(COALESCE(MAX(CAST(SUBSTRING_INDEX(t.content_key, '-', -1) AS UNSIGNED)), 0) + 1, 3, '0')) FROM (SELECT q.content_key FROM quiz_stock_items q JOIN batch_sets b ON b.id = q.set_id WHERE b.set_code = 'logic-training-1' AND q.content_key LIKE 'night-%') t),
        'L1', 'deep',
        '男は車の中でぐっすり眠った。エンジンは一度もかけていない。なのに目を覚ますと、車ごと300kmも離れた町にいた。なぜ?',
        '車ごと運ばれていた(キャリアカー・フェリーなど)',
        '{"hook":"寝てる間に300km!?","hint":"車が動いたとは限らないぞ!","question":"男は車の中でぐっすり眠った。エンジンは一度もかけていない。なのに目を覚ますと、車ごと300kmも離れた町にいた。なぜ?","answer":"車ごと運ばれていた(キャリアカー・フェリーなど)","explanation":"車を何台も載せて運ぶトラック(キャリアカー)やフェリーに、車ごと載っていた。エンジンは止めたままでも、寝ている間に300km先へ。動いたのは車ではない。","coach_comment":"動いたのは車じゃなかったな!","tags":["水平思考","夜の一問","状況パズル"],"summary":"エンジンをかけずに眠っていた男が、目を覚ますと車ごと300km先の町にいた理由を問う水平思考。車ごと何かに載せられて運ばれていた(キャリアカー・フェリーなど。別解を取り込む)。","illustration_scene":"夜、車の運転席から見た暗い車内。フロントガラスの外は一面の暗い紺色だけで、景色も明かりも見えない。車内はメーターのほのかな明かりで、ハンドルとダッシュボードの形が見分けられる。ハンドルの上に大きな「?」。人物・「?」以外の文字は描かない。"}',
        '類型: 寝ている間に車ごと遠くへ=カーフェリー(作者不詳の水平思考クイズ)。日本のフェリーは航行中に車内にとどまれないため、答えをキャリアカー等へ広げて別解を取り込んだ。流布例: https://ichigo-drill.jp/quiz-horizontal 。要注意: 確認できたのは1ドメインのみ。文面はオリジナルに書き下ろし(表現は書き直し済み)。', 1);

-- C80
INSERT INTO quiz_stock_items (set_id, content_key, quiz_type, difficulty, question_text, answer_text, content_fields, source_note, is_active)
VALUES ((SELECT id FROM batch_sets WHERE set_code = 'logic-training-1'),
        (SELECT CONCAT('night-', LPAD(COALESCE(MAX(CAST(SUBSTRING_INDEX(t.content_key, '-', -1) AS UNSIGNED)), 0) + 1, 3, '0')) FROM (SELECT q.content_key FROM quiz_stock_items q JOIN batch_sets b ON b.id = q.set_id WHERE b.set_code = 'logic-training-1' AND q.content_key LIKE 'night-%') t),
        'L1', 'deep',
        '体長10cmの赤いカニと、15cmの青いカニがかけっこをした。勝ったのは青いカニ。でも大きさのせいではない。なぜ?',
        '赤いカニはゆでてあったから',
        '{"hook":"カニのかけっこ、勝つのは?","hint":"赤い色の理由を考えろ!","question":"体長10cmの赤いカニと、15cmの青いカニがかけっこをした。勝ったのは青いカニ。でも大きさのせいではない。なぜ?","answer":"赤いカニはゆでてあったから","explanation":"カニは生きている間は青っぽい色のものが多く、ゆでると赤くなる。赤いカニはもうゆでてあったので、最初から走れなかったのだ。","coach_comment":"色に気づけば一瞬だな!","tags":["水平思考","夜の一問","ひっかけ"],"summary":"10cmの赤いカニと15cmの青いカニの競走で青が勝った理由を問う水平思考の定番。赤いカニはゆでてあった。大きさに目を向けさせる。","illustration_scene":"夜の浜辺の砂の上を、青いカニが1匹、はさみを上げて横向きに歩いている。遠くに暗い海と星空。カニの上に大きな「?」。人物・「?」以外の文字は描かない。"}',
        '類型: 赤いカニが青いカニに負ける=赤いカニはゆでてあった(作者不詳・英語圏の lateral thinking の定番)。流布例: https://ahaslides.com/blog/lateral-thinking-puzzles/ ・ https://mytour.vn/en/blog/bai-viet/brain-teasers-with-answers.html 。文面はオリジナルに書き下ろし(表現は書き直し済み)。', 1);

-- C81
INSERT INTO quiz_stock_items (set_id, content_key, quiz_type, difficulty, question_text, answer_text, content_fields, source_note, is_active)
VALUES ((SELECT id FROM batch_sets WHERE set_code = 'logic-training-1'),
        (SELECT CONCAT('night-', LPAD(COALESCE(MAX(CAST(SUBSTRING_INDEX(t.content_key, '-', -1) AS UNSIGNED)), 0) + 1, 3, '0')) FROM (SELECT q.content_key FROM quiz_stock_items q JOIN batch_sets b ON b.id = q.set_id WHERE b.set_code = 'logic-training-1' AND q.content_key LIKE 'night-%') t),
        'L1', 'deep',
        '雲ひとつない晴れた日、男が車で角を曲がると、突然どしゃぶりの雨。続いて車がゆれるほどの強い風。数分後、男は乾いた道を家に帰った。何があった?',
        '自動の洗車機の中を通っていた',
        '{"hook":"天気予報、大外れ!?","hint":"角の先がどんな場所か考えろ!","question":"雲ひとつない晴れた日、男が車で角を曲がると、突然どしゃぶりの雨。続いて車がゆれるほどの強い風。数分後、男は乾いた道を家に帰った。何があった?","answer":"自動の洗車機の中を通っていた","explanation":"男が角を曲がって入ったのは、ガソリンスタンドの自動洗車機。どしゃぶりの雨は洗車の水、強い風は車を乾かす風。空に雲はなく、外は一滴も降っていない。","coach_comment":"雨の正体を見抜いたな!","tags":["水平思考","夜の一問","状況パズル"],"summary":"晴れた日に車だけが大雨と強風にあい、数分後に乾いた道を帰った理由を問う水平思考。雲ひとつない・道が乾いているでゲリラ豪雨の別解を塞ぐ。自動洗車機の中を通っていた。場所の読み替え。","illustration_scene":"雲ひとつない夕焼けの空の下、まっすぐな道を走る1台の乗用車を後ろから見た絵。道の先の角に、街灯がともり始めている。車の上に大きな「?」。人物・「?」以外の文字は描かない。"}',
        '類型: 晴れの日に車だけ大雨と強風=自動洗車機の中(作者不詳・英語圏の lateral thinking)。流布例: https://icebreakerideas.com/lateral-thinking-puzzles/ ・ https://mumlyfe.com.au/lateral-thinking-puzzles-answers/ 。文面はオリジナルに書き下ろし(表現は書き直し済み)。', 1);

-- C82
INSERT INTO quiz_stock_items (set_id, content_key, quiz_type, difficulty, question_text, answer_text, content_fields, source_note, is_active)
VALUES ((SELECT id FROM batch_sets WHERE set_code = 'logic-training-1'),
        (SELECT CONCAT('night-', LPAD(COALESCE(MAX(CAST(SUBSTRING_INDEX(t.content_key, '-', -1) AS UNSIGNED)), 0) + 1, 3, '0')) FROM (SELECT q.content_key FROM quiz_stock_items q JOIN batch_sets b ON b.id = q.set_id WHERE b.set_code = 'logic-training-1' AND q.content_key LIKE 'night-%') t),
        'L1', 'deep',
        '空港で「荷物が出てくるのが遅い」と苦情が続いた。荷物が出てくる速さは変えずに、苦情をほとんどなくした。どうした?',
        '歩く道を長くした(待ちを短く感じさせる工夫なら正解)',
        '{"hook":"苦情がピタッと止まった!","hint":"じっと待つのがつらいんだ!","question":"空港で「荷物が出てくるのが遅い」と苦情が続いた。荷物が出てくる速さは変えずに、苦情をほとんどなくした。どうした?","answer":"歩く道を長くした(待ちを短く感じさせる工夫なら正解)","explanation":"到着口を受取所から遠くに移し、歩く道を長くした。歩く間に荷物が出てくるので、じっと待つ時間が減った。テレビを置くなど、待ち時間を短く感じさせる工夫も正解だ。","coach_comment":"待ち時間も工夫しだいだ!","tags":["水平思考","夜の一問","発想転換"],"summary":"空港で荷物が遅いという苦情を、出てくる速さを変えずに減らした方法を問う。到着口から受取所までの歩く道を長くし、待つ時間を歩く時間に変えた。待ちを短く感じさせる別解も取り込む。","illustration_scene":"夜の空港の手荷物受取所。明るい照明の下、空っぽのベルトコンベアがぐるりと回っている。大きな窓の外に夜の滑走路の明かり。コンベアの上に大きな「?」。人物・「?」以外の文字は描かない。"}',
        '類型: 手荷物の待ち時間の苦情を歩く距離で減らした(ヒューストン空港の話として流布)。流布例: https://news.livedoor.com/article/detail/7214698/ ・ https://www.psychologicalscience.org/news/why-waiting-is-torture.html 。文面はオリジナルに書き下ろし(表現は書き直し済み)。', 1);

-- C83
INSERT INTO quiz_stock_items (set_id, content_key, quiz_type, difficulty, question_text, answer_text, content_fields, source_note, is_active)
VALUES ((SELECT id FROM batch_sets WHERE set_code = 'logic-training-1'),
        (SELECT CONCAT('night-', LPAD(COALESCE(MAX(CAST(SUBSTRING_INDEX(t.content_key, '-', -1) AS UNSIGNED)), 0) + 1, 3, '0')) FROM (SELECT q.content_key FROM quiz_stock_items q JOIN batch_sets b ON b.id = q.set_id WHERE b.set_code = 'logic-training-1' AND q.content_key LIKE 'night-%') t),
        'L1', 'deep',
        '大会でいちばん足の速いランナーが、ゴールまで走りきったのに、ぶっちぎりの最下位だった。体調は万全で、けがもズルも手抜きもしていない。なぜ?',
        '走り以外でも競う種目だった(トライアスロンなど)',
        '{"hook":"最速なのに最下位!?","hint":"走るだけの大会とは限らない!","question":"大会でいちばん足の速いランナーが、ゴールまで走りきったのに、ぶっちぎりの最下位だった。体調は万全で、けがもズルも手抜きもしていない。なぜ?","answer":"走り以外でも競う種目だった(トライアスロンなど)","explanation":"トライアスロンなら泳ぎ・自転車・走りの合計で競う。足が速くても泳ぎで大きく遅れれば最下位だ。二人三脚や障害物競走など、足の速さだけで決まらない種目なら正解。","coach_comment":"得意だけじゃ勝てないな!","tags":["水平思考","夜の一問","状況パズル"],"summary":"最も足の速いランナーが、走りきったのに体調万全・手抜きなしで最下位の理由を問う水平思考。走り以外でも競う種目だった(トライアスロン等。二人三脚等の別解も取り込む)。","illustration_scene":"夜の競技場。照明に照らされたトラックのゴールテープだけが白く光り、観客席は空っぽ。ゴールの上に大きな「?」。人物・「?」以外の文字は描かない。"}',
        '類型: 最速のランナーが最下位=トライアスロン(作者不詳の水平思考クイズ)。流布例: https://ichigo-drill.jp/quiz-horizontal 。要注意: 確認できたのは1ドメインのみ。文面はオリジナルに書き下ろし(表現は書き直し済み)。', 1);
