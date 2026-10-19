-- 2026-10-w3 問題ストック補充投入(14 問。レビュー承認後に実行)
-- 生成元: content/quiz-stock/logic-training-1/2026-10-w3/stock_items.py(単一ソース)。適用先: ローカル MySQL / Aurora(acps)
-- set_id は set_code から解決するため両環境共通で実行できる。
-- content_key はスロット内の既存最大連番 + 1 を適用時に解決する(V007。両環境で同一値になる)。

-- A69
INSERT INTO quiz_stock_items (set_id, content_key, quiz_type, difficulty, question_text, answer_text, content_fields, source_note, is_active)
VALUES ((SELECT id FROM batch_sets WHERE set_code = 'logic-training-1'),
        (SELECT CONCAT('morning-', LPAD(COALESCE(MAX(CAST(SUBSTRING_INDEX(t.content_key, '-', -1) AS UNSIGNED)), 0) + 1, 3, '0')) FROM (SELECT q.content_key FROM quiz_stock_items q JOIN batch_sets b ON b.id = q.set_id WHERE b.set_code = 'logic-training-1' AND q.content_key LIKE 'morning-%') t),
        'L1', 'light',
        '朝ごはんに、どうしても食べられないものが2つある。好き嫌いでもアレルギーでもない。なんだ?',
        '昼ごはんと晩ごはん',
        '{"hook":"朝ごはん、ちゃんと食べたか?","hint":"「朝」に注目してみろ!","question":"朝ごはんに、どうしても食べられないものが2つある。好き嫌いでもアレルギーでもない。なんだ?","answer":"昼ごはんと晩ごはん","explanation":"食べ物の名前を探すと行き詰まる。朝に食べたら、それは昼ごはんでも晩ごはんでもなく朝ごはんだ。食事の呼び名そのものが答えだった。","coach_comment":"朝から頭が冴えてるな!","tags":["なぞなぞ","朝の一問","言葉あそび"],"summary":"朝ごはんにどうしても食べられないもの2つを問う英語圏の定番なぞ。答えは昼ごはんと晩ごはん。食べ物ではなく食事の呼び名に目を向ける。","illustration_scene":"朝日が差し込む台所のテーブルに、トースト・目玉焼き・サラダ・牛乳の朝食が並ぶ。窓の外に朝の青空。テーブルの上に大きな「?」。人物・「?」以外の文字は描かない。"}',
        '類型: 朝食に食べられない2つ=昼食と夕食(作者不詳・ボードビル起源とみられる英語圏の定番なぞ)。流布例: https://barrypopik.com/blog/what_are_the_two_things_you_cant_eat_for_breakfast_riddle 。文面はオリジナルに書き下ろし(表現は書き直し済み)。', 1);

-- A70
INSERT INTO quiz_stock_items (set_id, content_key, quiz_type, difficulty, question_text, answer_text, content_fields, source_note, is_active)
VALUES ((SELECT id FROM batch_sets WHERE set_code = 'logic-training-1'),
        (SELECT CONCAT('morning-', LPAD(COALESCE(MAX(CAST(SUBSTRING_INDEX(t.content_key, '-', -1) AS UNSIGNED)), 0) + 1, 3, '0')) FROM (SELECT q.content_key FROM quiz_stock_items q JOIN batch_sets b ON b.id = q.set_id WHERE b.set_code = 'logic-training-1' AND q.content_key LIKE 'morning-%') t),
        'L1', 'light',
        '黒板にマッチ棒が6本、縦に並んでいる。ここにマッチ棒をあと5本だけ足して、「9」にしてくれ。',
        '英語で NINE と書く(N・I・N・E の11本)',
        '{"hook":"マッチ棒の頭の体操だ","hint":"数字の書き方は1つじゃないぞ!","question":"黒板にマッチ棒が6本、縦に並んでいる。ここにマッチ棒をあと5本だけ足して、「9」にしてくれ。","answer":"英語で NINE と書く(N・I・N・E の11本)","explanation":"数字の9を作ろうとすると本数が合わない。縦の6本を生かして5本を足し、英語でNINEと書けば、11本でちょうど「9」になる。","coach_comment":"数字を言葉にしたな!","tags":["なぞなぞ","朝の一問","視覚パズル"],"summary":"縦に並んだマッチ棒6本に5本足して9にする英語圏の定番パズル。答えは英語でNINEと綴る(N・I・N・E=11本)。数字から文字への飛躍。","illustration_scene":"朝日が差し込む教室の黒板に、平らな木の角棒のマッチ棒6本が、縦向きに等間隔で横一列に並ぶ。どの棒も赤い頭は上の端に1つだけ。黒板の右上に大きな「?」。人物・「?」以外の文字や数字は描かない。"}',
        '類型: マッチ棒6本に5本足して9=NINEと綴る定番(作者不詳・英語圏のマッチ棒パズル集に流布)。流布例: https://amagicclassroom.com/uploads/3/4/5/2/34528828/matchstick_puzzles.pdf 。文面はオリジナルに書き下ろし(表現は書き直し済み)。', 1);

-- A71
INSERT INTO quiz_stock_items (set_id, content_key, quiz_type, difficulty, question_text, answer_text, content_fields, source_note, is_active)
VALUES ((SELECT id FROM batch_sets WHERE set_code = 'logic-training-1'),
        (SELECT CONCAT('morning-', LPAD(COALESCE(MAX(CAST(SUBSTRING_INDEX(t.content_key, '-', -1) AS UNSIGNED)), 0) + 1, 3, '0')) FROM (SELECT q.content_key FROM quiz_stock_items q JOIN batch_sets b ON b.id = q.set_id WHERE b.set_code = 'logic-training-1' AND q.content_key LIKE 'morning-%') t),
        'L1', 'light',
        '「あした」が「きのう」より先にやってくる。そんな場所がある。どこだ?',
        '辞書(あいうえお順で「あ」が先)',
        '{"hook":"時間が逆戻りする話だ","hint":"並び方に注目してみろ!","question":"「あした」が「きのう」より先にやってくる。そんな場所がある。どこだ?","answer":"辞書(あいうえお順で「あ」が先)","explanation":"時間の流れで考えると行き詰まる。辞書はあいうえお順に言葉が並ぶので、「あした」は「きのう」より前のページに載っている。","coach_comment":"順番の見方を変えたな!","tags":["なぞなぞ","朝の一問","発想の転換"],"summary":"「あした」が「きのう」より先に来る場所を問う。英語圏の定番(today が yesterday より先=辞書)を五十音順に置き換えた。答えは辞書。","illustration_scene":"朝日が差し込む部屋の壁に、無地の日めくりカレンダーと、目盛りだけの丸い掛け時計。窓の外に朝の青空。壁の前に大きな「?」。人物・「?」以外の文字や数字は描かない。"}',
        '類型: today が yesterday より先に来る場所=辞書(作者不詳・英語圏の定番なぞ)を五十音順(あした・きのう)に置き換え。流布例: https://www.freejobalert.com/article/when-does-today-come-before-yesterday-riddle-answer-11575 。文面はオリジナルに書き下ろし(表現は書き直し済み)。', 1);

