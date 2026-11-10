-- 2026-11-w1 問題ストック補充投入(14 問。レビュー承認後に実行)
-- 生成元: content/quiz-stock/logic-training-1/2026-11-w1/stock_items.py(単一ソース)。適用先: ローカル MySQL / Aurora(acps)
-- set_id は set_code から解決するため両環境共通で実行できる。
-- content_key はスロット内の既存最大連番 + 1 を適用時に解決する(V007。両環境で同一値になる)。

-- A83
INSERT INTO quiz_stock_items (set_id, content_key, quiz_type, difficulty, question_text, answer_text, content_fields, source_note, is_active)
VALUES ((SELECT id FROM batch_sets WHERE set_code = 'logic-training-1'),
        (SELECT CONCAT('morning-', LPAD(COALESCE(MAX(CAST(SUBSTRING_INDEX(t.content_key, '-', -1) AS UNSIGNED)), 0) + 1, 3, '0')) FROM (SELECT q.content_key FROM quiz_stock_items q JOIN batch_sets b ON b.id = q.set_id WHERE b.set_code = 'logic-training-1' AND q.content_key LIKE 'morning-%') t),
        'L1', 'light',
        '山から掘り出され、細い木の中に閉じこめられて、二度と出してもらえない。それなのに、だれもが必ず使ったことがある。なんだ?',
        '鉛筆の芯',
        '{"hook":"一度は必ず使ったはずだ!","hint":"その木は細長いぞ!","question":"山から掘り出され、細い木の中に閉じこめられて、二度と出してもらえない。それなのに、だれもが必ず使ったことがある。なんだ?","answer":"鉛筆の芯","explanation":"鉛筆の芯は、山で掘った黒鉛と粘土から作る。細い木の軸にはさまれたまま、出されることなく、すり減って役目を終える。","coach_comment":"芯のある答えだったぞ!","tags":["なぞなぞ","朝の一問","言葉あそび"],"summary":"山から掘り出され、細い木の中に閉じこめられ、だれもが使ったことがあるものを問うなぞ。答えは鉛筆の芯(黒鉛)。英語圏の伝承 riddle を日本語だけで成り立つ形に書き下ろした。","illustration_scene":"朝日が差す山の中の森。1本の木の幹に細長い穴があいていて、後ろ姿の人が、両手で抱えた大きな「?」をその穴に押し込んでいる。足もとにつるはしと、掘ったばかりの土。顔は描かない。「?」以外の文字は描かない。"}',
        '類型: 鉱山から掘り出され木のケースに閉じこめられるもの=鉛筆の芯(作者不詳・英語圏の伝承 riddle)。流布例: https://waywordradio.org/pencil-riddle ・ https://riddlepedia.com/?p=81110 。要注意: 候補段階の確認は検索結果まで(本文は未読)。文面はオリジナルに書き下ろし(表現は書き直し済み)。', 1);

-- A84
INSERT INTO quiz_stock_items (set_id, content_key, quiz_type, difficulty, question_text, answer_text, content_fields, source_note, is_active)
VALUES ((SELECT id FROM batch_sets WHERE set_code = 'logic-training-1'),
        (SELECT CONCAT('morning-', LPAD(COALESCE(MAX(CAST(SUBSTRING_INDEX(t.content_key, '-', -1) AS UNSIGNED)), 0) + 1, 3, '0')) FROM (SELECT q.content_key FROM quiz_stock_items q JOIN batch_sets b ON b.id = q.set_id WHERE b.set_code = 'logic-training-1' AND q.content_key LIKE 'morning-%') t),
        'L1', 'light',
        '漢字の「木」に、2画だけ書き足してできる漢字はいくつ思いつく? 5つ見つけたら名人だ。',
        '休・米・朱・机・朽・朴 など',
        '{"hook":"木から漢字が生まれるぞ!","hint":"左にも上にも足せるぞ!","question":"漢字の「木」に、2画だけ書き足してできる漢字はいくつ思いつく? 5つ見つけたら名人だ。","answer":"休・米・朱・机・朽・朴 など","explanation":"左に足せば休、右に足せば机・朽・朴、上や中に足せば米・朱。どれも木の4画に2画を足した6画の字だ。いくつ見つけられた?","coach_comment":"木を見て字も見たな!","tags":["なぞなぞ","朝の一問","漢字パズル"],"summary":"漢字の「木」に2画足してできる漢字を挙げる定番の漢字パズル。休・米・朱・机・朽・朴など。数を競う参加型(口に二画の A78 と同じ画足しシリーズ)。","illustration_scene":"朝日が差し込む教室の黒板の真ん中に、白いチョークで大きな漢字「木」が1字だけ書いてある。黒板の右上に大きな「?」。黒板の下にチョークが数本。人物と、「木」と「?」以外の文字は描かない。"}',
        '類型: 木に二画足してできる漢字を挙げる漢字パズル(作者不詳・画足しクイズの定番)。流布例: https://jinshirakuma.hatenablog.com/entry/2025/12/07/001049 ・ https://www.dwc.doshisha.ac.jp/research/faculty_column/2018-11-08-09-20 (画足しの形式)。文面はオリジナルに書き下ろし(表現は書き直し済み)。', 1);

-- A85
INSERT INTO quiz_stock_items (set_id, content_key, quiz_type, difficulty, question_text, answer_text, content_fields, source_note, is_active)
VALUES ((SELECT id FROM batch_sets WHERE set_code = 'logic-training-1'),
        (SELECT CONCAT('morning-', LPAD(COALESCE(MAX(CAST(SUBSTRING_INDEX(t.content_key, '-', -1) AS UNSIGNED)), 0) + 1, 3, '0')) FROM (SELECT q.content_key FROM quiz_stock_items q JOIN batch_sets b ON b.id = q.set_id WHERE b.set_code = 'logic-training-1' AND q.content_key LIKE 'morning-%') t),
        'L1', 'light',
        '冬に生まれて、夏にはいなくなる。根っこは上にあって、下へ下へとのびていく。なんだ?',
        'つらら',
        '{"hook":"逆さまに育つやつがいる!","hint":"寒い朝に見上げてみろ!","question":"冬に生まれて、夏にはいなくなる。根っこは上にあって、下へ下へとのびていく。なんだ?","answer":"つらら","explanation":"つららは、屋根の雪どけ水が軒先で凍ってできる。根もとは上の軒にあり、しずくが凍るたびに下へのびる。暖かくなればとけて消える。","coach_comment":"冷たい謎を見事にとかした!","tags":["なぞなぞ","朝の一問","言葉あそび"],"summary":"冬に生まれ夏にいなくなり、根が上にあって下へのびるものを問うなぞ。答えはつらら。アイルランド等で採集された伝承 riddle を日本語に書き下ろした。","illustration_scene":"朝日に染まる空に、葉のない1本の木が上下逆さまに浮かんでいる。根っこが上で空に張りつき、幹と枝が地面に向かって下へのびている。下は枯れ草の野原。木の横に大きな「?」。人物・「?」以外の文字は描かない。"}',
        '類型: 冬に生まれ根が上で下へのびるもの=つらら(作者不詳の伝承 riddle。アイルランドの学校採集記録・1929 年のニュージーランドの新聞)。流布例: https://duchas.ie/en/cbes/4922123/4854312/4951095 ・ https://paperspast.natlib.govt.nz/newspapers/AS19291030.2.182.15 。要注意: 候補段階の確認は検索結果まで(本文は未読)。文面はオリジナルに書き下ろし(表現は書き直し済み)。', 1);

-- A86
INSERT INTO quiz_stock_items (set_id, content_key, quiz_type, difficulty, question_text, answer_text, content_fields, source_note, is_active)
VALUES ((SELECT id FROM batch_sets WHERE set_code = 'logic-training-1'),
        (SELECT CONCAT('morning-', LPAD(COALESCE(MAX(CAST(SUBSTRING_INDEX(t.content_key, '-', -1) AS UNSIGNED)), 0) + 1, 3, '0')) FROM (SELECT q.content_key FROM quiz_stock_items q JOIN batch_sets b ON b.id = q.set_id WHERE b.set_code = 'logic-training-1' AND q.content_key LIKE 'morning-%') t),
        'L1', 'light',
        'このカードの「?」に入るひらがなはなんだ? 五十音の順でも、数の読みでもないぞ。',
        'れ(明治・大正・昭和・平成・令和)',
        '{"hook":"日本人なら解けるはずだ!","hint":"生まれた年を言ってみろ!","question":"このカードの「?」に入るひらがなはなんだ? 五十音の順でも、数の読みでもないぞ。","answer":"れ(明治・大正・昭和・平成・令和)","explanation":"め・た・し・へは、明治・大正・昭和・平成の読みの頭文字。平成の次は令和だから、?は「れ」。書類の生年月日の欄でおなじみの並びだ。","coach_comment":"時代を読む目があるな!","tags":["なぞなぞ","朝の一問","法則発見"],"summary":"め・た・し・へ・?の並びから元号(明治・大正・昭和・平成・令和)の頭文字と見抜き、?=れを答える法則発見。指の頭文字の A44 と同じ領域の飛躍。","illustration_scene":"朝日が差し込む窓辺の木の机に、白い無地のカードが5枚、横一列に並ぶ。左から順に、ひらがなで「め」「た」「し」「へ」「?」と1枚に1字ずつ大きく書いてある。人物と、「め」「た」「し」「へ」「?」以外の文字は描かない。"}',
        '類型: 元号の頭文字の並びの法則発見(事実ベースの並び。M・T・S・H の略記は書類で広く使われる)。流布例: https://dic.pixiv.net/history/M/5780544/source (略記の存在)。要注意: 法則クイズとしての流布例は未確認。文面はオリジナルに書き下ろし(表現は書き直し済み)。', 1);

-- A87
INSERT INTO quiz_stock_items (set_id, content_key, quiz_type, difficulty, question_text, answer_text, content_fields, source_note, is_active)
VALUES ((SELECT id FROM batch_sets WHERE set_code = 'logic-training-1'),
        (SELECT CONCAT('morning-', LPAD(COALESCE(MAX(CAST(SUBSTRING_INDEX(t.content_key, '-', -1) AS UNSIGNED)), 0) + 1, 3, '0')) FROM (SELECT q.content_key FROM quiz_stock_items q JOIN batch_sets b ON b.id = q.set_id WHERE b.set_code = 'logic-training-1' AND q.content_key LIKE 'morning-%') t),
        'L1', 'light',
        '白いまま空へ上がっていって、地面に落ちたあとは黄色と白になっている。なんだ?',
        '卵(投げ上げて、受けそこねた)',
        '{"hook":"朝ごはんの前に解けるか?","hint":"落ちたらどうなるか考えろ!","question":"白いまま空へ上がっていって、地面に落ちたあとは黄色と白になっている。なんだ?","answer":"卵(投げ上げて、受けそこねた)","explanation":"白い殻の卵を投げ上げて受けそこねると、割れて黄身が流れ出す。上がるときは白一色、落ちたあとは黄身の黄色と、割れた殻の白。食べ物は投げずに解こう。","coach_comment":"答えは落とさず受け取れ!","tags":["なぞなぞ","朝の一問","言葉あそび"],"summary":"白いまま上がり、地面に落ちたあとは黄色と白になるものを問うなぞ。答えは卵(投げ上げて割れる)。英語圏の定番 riddle を日本語に書き下ろした。A14(使う前に壊す)とは仕掛けが別。","illustration_scene":"朝の青空の下、公園の芝生で、後ろ姿の子どもが両手を上にのばして空を見上げている。空には白い雲がいくつか浮かび、空の高いところに大きな「?」。顔は描かない。「?」以外の文字は描かない。"}',
        '類型: 白いまま上がり黄色と白で落ちてくるもの=卵(作者不詳・英語圏の定番 riddle。なぞなぞ本の書名にもなっている)。流布例: https://nflibrary.ca/catalogue/what-goes-up-white-comes-down-yellow-262455 ・ https://www.penguin.co.uk/books/446097/what-goes-up-white-and-comes-down-yellow-by-brandreth-gyles/9780241544488 。要注意: 候補段階の確認は検索結果まで(本文は未読)。文面はオリジナルに書き下ろし(表現は書き直し済み)。', 1);

-- A88
INSERT INTO quiz_stock_items (set_id, content_key, quiz_type, difficulty, question_text, answer_text, content_fields, source_note, is_active)
VALUES ((SELECT id FROM batch_sets WHERE set_code = 'logic-training-1'),
        (SELECT CONCAT('morning-', LPAD(COALESCE(MAX(CAST(SUBSTRING_INDEX(t.content_key, '-', -1) AS UNSIGNED)), 0) + 1, 3, '0')) FROM (SELECT q.content_key FROM quiz_stock_items q JOIN batch_sets b ON b.id = q.set_id WHERE b.set_code = 'logic-training-1' AND q.content_key LIKE 'morning-%') t),
        'L1', 'light',
        '木の上に立って、朝から晩までじっと見ている人がいる。だれだ?',
        '親(立 + 木 + 見)',
        '{"hook":"木登りの名人か!?","hint":"漢字で考えてみろ!","question":"木の上に立って、朝から晩までじっと見ている人がいる。だれだ?","answer":"親(立 + 木 + 見)","explanation":"「親」の字は、立・木・見でできている。木の上に立って子どもを見守る人、と覚えると忘れない。本当の成り立ちは別だが、昔からの覚え方だ。","coach_comment":"たまには親に連絡しろよ!","tags":["なぞなぞ","朝の一問","漢字なぞ"],"summary":"木の上に立ってじっと見ている人を問う漢字なぞ(問題文では漢字とも子どもとも言わない)。答えは親(立+木+見)。漢字の覚え方として流布する俗解をなぞなぞにした。","illustration_scene":"朝日が差す丘の上に、枝を大きく広げた1本の大きな木。木のてっぺんに、後ろ姿の人が1人まっすぐ立ち、片手をひたいにかざして遠くをじっと見ている。幹には長いはしご。丘の下には朝の町並み。人の頭の上に大きな「?」。顔は描かない。「?」以外の文字は描かない。"}',
        '類型: 「親」=木の上に立って見る、の覚え方(作者不詳の俗解)。流布例: https://www.kanji-trainer.org/Phrase_mnemo/Mnemonique_親.html ・ https://jpdb.io/kanji/親 。要注意: 漢字の覚え方としての流布で、なぞなぞとしての流布例は未確認。文面はオリジナルに書き下ろし(表現は書き直し済み)。', 1);

-- A89
INSERT INTO quiz_stock_items (set_id, content_key, quiz_type, difficulty, question_text, answer_text, content_fields, source_note, is_active)
VALUES ((SELECT id FROM batch_sets WHERE set_code = 'logic-training-1'),
        (SELECT CONCAT('morning-', LPAD(COALESCE(MAX(CAST(SUBSTRING_INDEX(t.content_key, '-', -1) AS UNSIGNED)), 0) + 1, 3, '0')) FROM (SELECT q.content_key FROM quiz_stock_items q JOIN batch_sets b ON b.id = q.set_id WHERE b.set_code = 'logic-training-1' AND q.content_key LIKE 'morning-%') t),
        'L1', 'light',
        '水の中で生まれたのに、水にふれると消えてしまう。なんだ?',
        '塩(氷も正解)',
        '{"hook":"生まれ故郷が苦手だと!?","hint":"毎日口にしているぞ!","question":"水の中で生まれたのに、水にふれると消えてしまう。なんだ?","answer":"塩(氷も正解)","explanation":"塩は、海の水を煮つめたり干したりして作る。水から生まれたのに、水に入れるととけて見えなくなる。氷と答えた人も正解だ。","coach_comment":"しょっぱい謎を解いたな!","tags":["なぞなぞ","朝の一問","言葉あそび"],"summary":"水の中で生まれたのに水にふれると消えるものを問うなぞ。答えは塩(海水から作り、水にとける)。氷の別解も取り込む。中世のアルドヘルムの謎以来の伝承 riddle を日本語に書き下ろした。","illustration_scene":"朝日がのぼる海。きらきら光る波の間から、色とりどりの魚たちが元気にはねている。遠くに小さな島とカモメ。海の上の空に大きな「?」。人物・「?」以外の文字は描かない。"}',
        '類型: 水の中で生まれ水にふれると消えるもの=塩(作者不詳の伝承 riddle。中世ラテン語のアルドヘルムの謎 Salis 以来)。流布例: https://theriddleages.com/riddles/post/aldhelm-riddle-19-salis/ ・ https://riddles.com/post/98/water-riddles 。要注意: 候補段階の確認は検索結果まで(本文は未読)。文面はオリジナルに書き下ろし(表現は書き直し済み)。', 1);

-- C84
INSERT INTO quiz_stock_items (set_id, content_key, quiz_type, difficulty, question_text, answer_text, content_fields, source_note, is_active)
VALUES ((SELECT id FROM batch_sets WHERE set_code = 'logic-training-1'),
        (SELECT CONCAT('night-', LPAD(COALESCE(MAX(CAST(SUBSTRING_INDEX(t.content_key, '-', -1) AS UNSIGNED)), 0) + 1, 3, '0')) FROM (SELECT q.content_key FROM quiz_stock_items q JOIN batch_sets b ON b.id = q.set_id WHERE b.set_code = 'logic-training-1' AND q.content_key LIKE 'night-%') t),
        'L1', 'deep',
        '女性があるボタンを1つ押し、すぐ体重計に乗ると、体重が何キロも減っていた。運動も食事制限もしておらず、荷物も服もそのまま。体重計も壊れていない。なぜ?',
        '下りはじめたエレベーターの中で量ったから',
        '{"hook":"数秒でやせる方法!?","hint":"立っている場所を考えろ!","question":"女性があるボタンを1つ押し、すぐ体重計に乗ると、体重が何キロも減っていた。運動も食事制限もしておらず、荷物も服もそのまま。体重計も壊れていない。なぜ?","answer":"下りはじめたエレベーターの中で量ったから","explanation":"押したのは下の階のボタン。エレベーターが下りはじめる瞬間は、体が床を押す力が弱まり、体重計の数字が何キロも減る。動きが一定になれば元に戻る。","coach_comment":"楽してやせる道はないぞ!","tags":["水平思考","夜の一問","状況パズル"],"summary":"ボタンを押してすぐ体重計に乗ると体重が何キロも減っていた理由を問う水平思考。下りはじめたエレベーターの中で量った(加速で表示が一時的に減る)。体重計は正常。場所の読み替え。","illustration_scene":"夜景の見える部屋で、後ろ姿の女性が両手を上げて喜んでいる。部屋のすみには、ほこりをかぶったダンベルとランニングシューズ、テーブルには大きなケーキ。女性の頭の上に大きな「?」。顔は描かない。「?」以外の文字は描かない。"}',
        '類型: ボタン1つで体重が減る=下りのエレベーターの中の体重計(作者不詳・英語圏の lateral thinking)。流布例: https://arkadium.com/blog/lateral-thinking-puzzles 。要注意: 確認できたのは1ドメインのみ。文面はオリジナルに書き下ろし(表現は書き直し済み)。', 1);

-- C85
INSERT INTO quiz_stock_items (set_id, content_key, quiz_type, difficulty, question_text, answer_text, content_fields, source_note, is_active)
VALUES ((SELECT id FROM batch_sets WHERE set_code = 'logic-training-1'),
        (SELECT CONCAT('night-', LPAD(COALESCE(MAX(CAST(SUBSTRING_INDEX(t.content_key, '-', -1) AS UNSIGNED)), 0) + 1, 3, '0')) FROM (SELECT q.content_key FROM quiz_stock_items q JOIN batch_sets b ON b.id = q.set_id WHERE b.set_code = 'logic-training-1' AND q.content_key LIKE 'night-%') t),
        'L1', 'deep',
        '王さまが黒板に1本の線を引いた。「この線に触れず、消しもせず、黒板も動かさずに、この線を短くしてみよ」。賢い家来はどうした?',
        '下に、もっと長い線を引いた',
        '{"hook":"王さまの無理難題だ!","hint":"黒板は広いぞ!","question":"王さまが黒板に1本の線を引いた。「この線に触れず、消しもせず、黒板も動かさずに、この線を短くしてみよ」。賢い家来はどうした?","answer":"下に、もっと長い線を引いた","explanation":"家来は、王さまの線の下に、もっと長い線を引いた。比べれば、元の線は「短いほう」になる。長い短いは、比べる相手で決まる。インドに伝わるとんち話だ。","coach_comment":"比べ方ひとつで変わるぞ!","tags":["とんち","夜の一問","発想転換"],"summary":"引かれた線に触れず消さずに短くせよという難題を、下にもっと長い線を引いて解くとんち。インドのアクバルとビルバルの民話。長さは比べる相手で決まる。","illustration_scene":"夜の宮殿の広間。ろうそくの明かりに照らされた大きな黒板に、白いチョークの横線が1本だけ引いてある。黒板の前に玉座と赤いじゅうたん。黒板の右上に大きな「?」。人物・「?」以外の文字は描かない。"}',
        '類型: 線に触れずに短くする=となりに長い線を引く(アクバルとビルバルの民話のとんち。インドの教科書にも収録)。流布例: https://puzzles-world.com/2015/12/how-did-birbal-make-line-shorter.html ・ https://www.orchidsinternationalschool.com/class2-english-ncert-solutions-chapter-14-make-it-shorter 。文面はオリジナルに書き下ろし(表現は書き直し済み)。', 1);

-- C86
INSERT INTO quiz_stock_items (set_id, content_key, quiz_type, difficulty, question_text, answer_text, content_fields, source_note, is_active)
VALUES ((SELECT id FROM batch_sets WHERE set_code = 'logic-training-1'),
        (SELECT CONCAT('night-', LPAD(COALESCE(MAX(CAST(SUBSTRING_INDEX(t.content_key, '-', -1) AS UNSIGNED)), 0) + 1, 3, '0')) FROM (SELECT q.content_key FROM quiz_stock_items q JOIN batch_sets b ON b.id = q.set_id WHERE b.set_code = 'logic-training-1' AND q.content_key LIKE 'night-%') t),
        'L1', 'deep',
        '夜の倉庫の警備員が、朝、社長に言った。「ゆうべ、社長の出張先が大雪になる夢を見ました」。本当に大雪になり、社長は礼を言ったあと、彼をクビにした。なぜ?',
        '夜の勤務中に眠って、夢を見ていたから',
        '{"hook":"社長の判断、わかるか?","hint":"当たったことは関係ないぞ!","question":"夜の倉庫の警備員が、朝、社長に言った。「ゆうべ、社長の出張先が大雪になる夢を見ました」。本当に大雪になり、社長は礼を言ったあと、彼をクビにした。なぜ?","answer":"夜の勤務中に眠って、夢を見ていたから","explanation":"夢を見たということは、眠っていたということ。夜の倉庫を見張るのが仕事の警備員が、勤務中に居眠りしたと自分で白状してしまった。","coach_comment":"口は災いのもとだな!","tags":["水平思考","夜の一問","状況パズル"],"summary":"夢で大雪を言い当てた夜の警備員が、礼を言われたのにクビになった理由を問う水平思考の定番。夜の勤務中に眠っていたと自白したから。原典の飛行機事故の夢は大雪に置き換えた。","illustration_scene":"大雪の夜の駅。ホームも線路も深い雪にうもれ、電車が1両、雪をかぶって立ち往生している。街灯の明かりの中を雪がはげしく降り、ホームのベンチには置き去りの旅行かばんが1つ。駅の屋根の上に大きな「?」。人物・「?」以外の文字は描かない。"}',
        '類型: 夢で危険を言い当てた夜警がクビになる=勤務中に眠っていた(作者不詳・英語圏の situation puzzle の定番)。流布例: https://www.kith.org/jed/situation-puzzles/answers-to-jeds-list-of-situation-puzzles/ ・ https://www.puzzleprime.com/puzzles/brain-teasers/lateral/rewarded-and-fired/ 。文面はオリジナルに書き下ろし(表現は書き直し済み)。', 1);

-- C87
INSERT INTO quiz_stock_items (set_id, content_key, quiz_type, difficulty, question_text, answer_text, content_fields, source_note, is_active)
VALUES ((SELECT id FROM batch_sets WHERE set_code = 'logic-training-1'),
        (SELECT CONCAT('night-', LPAD(COALESCE(MAX(CAST(SUBSTRING_INDEX(t.content_key, '-', -1) AS UNSIGNED)), 0) + 1, 3, '0')) FROM (SELECT q.content_key FROM quiz_stock_items q JOIN batch_sets b ON b.id = q.set_id WHERE b.set_code = 'logic-training-1' AND q.content_key LIKE 'night-%') t),
        'L1', 'deep',
        'よく切れるハサミで、写真を半分に切ろうとした。でも、どうしても切れない。ハサミは壊れていない。なぜ?',
        'スマホの画面に映っている写真だった',
        '{"hook":"力じゃ解決しないぞ!","hint":"ハサミのせいじゃないぞ!","question":"よく切れるハサミで、写真を半分に切ろうとした。でも、どうしても切れない。ハサミは壊れていない。なぜ?","answer":"スマホの画面に映っている写真だった","explanation":"切ろうとしたのは、スマホの画面に映った写真。紙に焼いた写真ではないから、ハサミでは切れない。写真と聞くと、つい紙の1枚を思い浮かべてしまう。","coach_comment":"思い込みを切り取ったな!","tags":["水平思考","夜の一問","状況パズル"],"summary":"よく切れるハサミで写真が切れない理由を問う水平思考。写真はスマホの画面に映っているものだった。写真=紙という思い込みを突く。","illustration_scene":"夜の机。電気スタンドの明かりの下に、大きなハサミが1本と、細かく切られた色紙の切りくずがたくさん散らばっている。ハサミの上に大きな「?」。人物・「?」以外の文字は描かない。"}',
        '類型: 切れない写真=画面に映った写真(作者不詳の水平思考クイズ)。流布例: https://ichigo-drill.jp/quiz-horizontal 。要注意: 確認できたのは1ドメインのみ(同サイト独自の作の可能性あり)。文面はオリジナルに書き下ろし(表現は書き直し済み)。', 1);

-- C88
INSERT INTO quiz_stock_items (set_id, content_key, quiz_type, difficulty, question_text, answer_text, content_fields, source_note, is_active)
VALUES ((SELECT id FROM batch_sets WHERE set_code = 'logic-training-1'),
        (SELECT CONCAT('night-', LPAD(COALESCE(MAX(CAST(SUBSTRING_INDEX(t.content_key, '-', -1) AS UNSIGNED)), 0) + 1, 3, '0')) FROM (SELECT q.content_key FROM quiz_stock_items q JOIN batch_sets b ON b.id = q.set_id WHERE b.set_code = 'logic-training-1' AND q.content_key LIKE 'night-%') t),
        'L1', 'deep',
        '夜、男は馬に乗って進んでいた。前にも馬、後ろには馬車。馬車を引く馬はいないのにどれだけ進んでも、前との差は縮まらず、後ろとの差も開かない。男はどこにいる?',
        '遊園地のメリーゴーラウンドの上',
        '{"hook":"夜の乗馬、いいものだな!","hint":"草原とは言っていないぞ!","question":"夜、男は馬に乗って進んでいた。前にも馬、後ろには馬車。馬車を引く馬はいないのにどれだけ進んでも、前との差は縮まらず、後ろとの差も開かない。男はどこにいる?","answer":"遊園地のメリーゴーラウンドの上","explanation":"男が乗っていたのは、メリーゴーラウンドの木馬。前の馬も後ろの馬車も、同じ台の上で一緒に回っている。だから、いくら進んでも差は変わらない。","coach_comment":"目が回る名推理だ!","tags":["水平思考","夜の一問","状況パズル"],"summary":"馬に乗った男が、前の馬にも後ろの馬車にも差が変わらないまま進み続ける場所を問う水平思考。メリーゴーラウンドの上。「馬車を引く馬はいない」で、馬車を引く馬に乗っている・隊列で進むという別解を塞ぐ。場所の読み替え。","illustration_scene":"月明かりの夜の草原を、遠くから横向きに見た黒い影絵。先頭にたてがみをなびかせて走る馬、その後ろに男を乗せて走る馬、いちばん後ろに1台の馬車が、一列に並んで走っている。空には星と大きな三日月。男の頭の上に大きな「?」。顔は描かない。「?」以外の文字は描かない。"}',
        '類型: 前の馬にも後ろの馬車にも差が変わらない=メリーゴーラウンド(作者不詳・英語圏の lateral puzzle)。流布例: https://www.puzzleprime.com/puzzles/brain-teasers/lateral/a-horse-in-front-a-car-behind/ ・ https://www.photoshopgurus.com/forum/threads/dilema.4213/post-37396 。文面はオリジナルに書き下ろし(表現は書き直し済み)。', 1);

-- C89
INSERT INTO quiz_stock_items (set_id, content_key, quiz_type, difficulty, question_text, answer_text, content_fields, source_note, is_active)
VALUES ((SELECT id FROM batch_sets WHERE set_code = 'logic-training-1'),
        (SELECT CONCAT('night-', LPAD(COALESCE(MAX(CAST(SUBSTRING_INDEX(t.content_key, '-', -1) AS UNSIGNED)), 0) + 1, 3, '0')) FROM (SELECT q.content_key FROM quiz_stock_items q JOIN batch_sets b ON b.id = q.set_id WHERE b.set_code = 'logic-training-1' AND q.content_key LIKE 'night-%') t),
        'L1', 'deep',
        '赤いペンで、白い紙に大きく字を書いた。インクはちゃんと出ているのに、書いた本人にも字がまったく見えない。目は正常で、目も開けている。なぜ?',
        '部屋の明かりが真っ赤だった',
        '{"hook":"インクは出ているのに!?","hint":"部屋のようすを想像しろ!","question":"赤いペンで、白い紙に大きく字を書いた。インクはちゃんと出ているのに、書いた本人にも字がまったく見えない。目は正常で、目も開けている。なぜ?","answer":"部屋の明かりが真っ赤だった","explanation":"赤い明かりの下では、白い紙も赤く見える。赤い字は紙の色にとけこんで、見分けがつかない。昔の写真の暗室などが、そんな部屋だ。普通の明かりに戻せば字は現れる。","coach_comment":"見えないものを見抜いたな!","tags":["水平思考","夜の一問","状況パズル"],"summary":"赤いペンで白い紙に書いた字が、インクが出ているのに本人にも見えない理由を問う水平思考。部屋の明かりが真っ赤で、紙も赤く見えて字がとけこんだ(暗室など)。","illustration_scene":"夜の机を真上から見た絵。机の上に大きな紙が1枚と、キャップを外したペンが1本。紙には何も見えない。机のすみにインクのびんとメガネ。紙の上に大きな「?」。人物・「?」以外の文字は描かない。"}',
        '類型: 赤いペンの字が見えない=赤い明かりの部屋(作者不詳の水平思考クイズ)。流布例: https://ichigo-drill.jp/quiz-horizontal 。要注意: 確認できたのは1ドメインのみ(同サイト独自の作の可能性あり)。文面はオリジナルに書き下ろし(表現は書き直し済み)。', 1);

-- C90
INSERT INTO quiz_stock_items (set_id, content_key, quiz_type, difficulty, question_text, answer_text, content_fields, source_note, is_active)
VALUES ((SELECT id FROM batch_sets WHERE set_code = 'logic-training-1'),
        (SELECT CONCAT('night-', LPAD(COALESCE(MAX(CAST(SUBSTRING_INDEX(t.content_key, '-', -1) AS UNSIGNED)), 0) + 1, 3, '0')) FROM (SELECT q.content_key FROM quiz_stock_items q JOIN batch_sets b ON b.id = q.set_id WHERE b.set_code = 'logic-training-1' AND q.content_key LIKE 'night-%') t),
        'L1', 'deep',
        '夜ふけ、男はマグカップのココアを電子レンジで2分温めた。チンと鳴ったのに、扉を開けて閉め、2秒だけ追加した。もう十分に熱いのに、なぜ?',
        '回る皿で、取っ手を手前に向けるため',
        '{"hook":"たった2秒の追加!?","hint":"熱いカップをどう持つ?","question":"夜ふけ、男はマグカップのココアを電子レンジで2分温めた。チンと鳴ったのに、扉を開けて閉め、2秒だけ追加した。もう十分に熱いのに、なぜ?","answer":"回る皿で、取っ手を手前に向けるため","explanation":"止まったとき、カップの取っ手が奥を向いていた。熱いカップの奥へ手を回すのは危ない。2秒だけ回せば、皿が半周して取っ手が手前に来る。","coach_comment":"2秒の工夫が光るな!","tags":["水平思考","夜の一問","状況パズル"],"summary":"十分に温まったココアを電子レンジで2秒だけ追加した理由を問う水平思考。回る皿を半周させ、奥を向いたマグカップの取っ手を手前に向けるため。","illustration_scene":"夜ふけの台所。扉の閉まった電子レンジの窓がオレンジ色に光り、中から湯気がもれている。窓の外に星空、流しの横にココアの缶。電子レンジの上に大きな「?」。人物・「?」以外の文字や数字は描かない。"}',
        '類型: 温め終わったカップを2秒だけ追加=取っ手を手前に回す(作者不詳・英語圏の situation puzzle)。流布例: https://www.kith.org/jed/situation-puzzles/answers-to-jeds-list-of-situation-puzzles/ ・ https://www.riddlesandanswers.com/puzzles-brain-teasers/coffee-mugs-riddles 。文面はオリジナルに書き下ろし(表現は書き直し済み)。', 1);
