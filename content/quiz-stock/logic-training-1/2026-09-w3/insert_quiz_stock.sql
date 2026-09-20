-- 2026-09-w3 問題ストック補充投入(14 問。レビュー承認後に実行)
-- 生成元: content/quiz-stock/logic-training-1/2026-09-w3/stock_items.py(単一ソース)。適用先: ローカル MySQL / Aurora(acps)
-- set_id は set_code から解決するため両環境共通で実行できる。
-- content_key はスロット内の既存最大連番 + 1 を適用時に解決する(V007。両環境で同一値になる)。

-- A40
INSERT INTO quiz_stock_items (set_id, content_key, quiz_type, difficulty, question_text, answer_text, content_fields, source_note, is_active)
VALUES ((SELECT id FROM batch_sets WHERE set_code = 'logic-training-1'),
        (SELECT CONCAT('morning-', LPAD(COALESCE(MAX(CAST(SUBSTRING_INDEX(t.content_key, '-', -1) AS UNSIGNED)), 0) + 1, 3, '0')) FROM (SELECT q.content_key FROM quiz_stock_items q JOIN batch_sets b ON b.id = q.set_id WHERE b.set_code = 'logic-training-1' AND q.content_key LIKE 'morning-%') t),
        'L1', 'light',
        '黒板の式は、計算が合っていない。線をたった1本だけ足して、計算がぴったり合う式にしてくれ。',
        '545+5=550(+に斜線を足して4にする)',
        '{"hook":"足し算なのに線を引くだけ?","hint":"数字じゃなく記号を見ろ!","question":"黒板の式は、計算が合っていない。線をたった1本だけ足して、計算がぴったり合う式にしてくれ。","answer":"545+5=550(+に斜線を足して4にする)","explanation":"左の「+」に斜線を足して「4」にすれば545+5=550で計算が合う(右の+でも可)。「=」に線を足して「≠」にしても計算は合わないので不正解。記号を疑え。","coach_comment":"記号も数字の仲間だ、よく見たな!","tags":["なぞなぞ","朝の一問","式のパズル"],"summary":"「5+5+5=550」に線を1本足して計算が合う式にする定番の視覚パズル。「+」に斜線を足して「4」にし545+5=550。式は問題文に書かず黒板の絵で見せ、「計算が合う」で「≠」の別解を封じた。","illustration_scene":"朝日が差し込む教室の黒板に、チョークで「5+5+5=550」と大きく1行だけ書かれ、その横に大きな「?」がある。文字はこの式と「?」だけを描き、他の文字・数字は描かない。人物は描かない。"}',
        '類型: 線を1本足して式を直す視覚パズル(作者不詳・国内外に流布)。流布例: https://detail.chiebukuro.yahoo.co.jp/qa/question_detail/q1034575295 , https://ddnavi.com/article/d532020/a/ , https://quiz.community.fmworld.net/nazonazo/content/63/answer3.html , https://nazoq.com/hardest/Q003458.html 。式は問題文に書かずイラスト(黒板)で提示し、「計算が合う式」の条件で「=」→「≠」の別解を封じた(2026-09-20 レビュー)。文面はオリジナルに書き下ろし(表現は書き直し済み)。', 1);

-- A42
INSERT INTO quiz_stock_items (set_id, content_key, quiz_type, difficulty, question_text, answer_text, content_fields, source_note, is_active)
VALUES ((SELECT id FROM batch_sets WHERE set_code = 'logic-training-1'),
        (SELECT CONCAT('morning-', LPAD(COALESCE(MAX(CAST(SUBSTRING_INDEX(t.content_key, '-', -1) AS UNSIGNED)), 0) + 1, 3, '0')) FROM (SELECT q.content_key FROM quiz_stock_items q JOIN batch_sets b ON b.id = q.set_id WHERE b.set_code = 'logic-training-1' AND q.content_key LIKE 'morning-%') t),
        'L1', 'light',
        '好きな数を1つ思い浮かべろ。それを2倍して10を足し、2で割って、最初に思い浮かべた数を引く。答えはいくつになった?',
        '必ず5(どんな数でも同じ)',
        '{"hook":"頭の中だけで魔法をかけるぞ","hint":"元の数をxと置いてみろ!","question":"好きな数を1つ思い浮かべろ。それを2倍して10を足し、2で割って、最初に思い浮かべた数を引く。答えはいくつになった?","answer":"必ず5(どんな数でも同じ)","explanation":"元の数をxとすると(2x+10)÷2−x=x+5−x=5。最初の数は途中で消え、10÷2の5だけが残る。誰がやっても答えが同じになる計算マジックだ。","coach_comment":"種明かしまでできたら本物だ!","tags":["なぞなぞ","朝の一問","計算マジック"],"summary":"好きな数を2倍→10を足す→2で割る→元の数を引くと必ず5になる計算マジック。式で(2x+10)÷2−x=5と種明かしする。答えが全員同じになる驚きでコメントを誘う。","illustration_scene":"朝日が差し込むリビングで、後ろ姿の人が頭の上に吹き出しを浮かべ、その吹き出しの中に大きな「?」がある。周りに小さな星や光の粒が魔法のように舞う。顔は描かない。数字・文字は描かない。"}',
        '類型: 計算マジック(2倍 → +10 → ÷2 → 元の数を引く = 必ず 5。作者不詳の定番)。流布例: https://detail.chiebukuro.yahoo.co.jp/qa/question_detail/q1417987009 , https://land.toss-online.com/lesson/kttB1ZHLIXoLyTIwlDrj , https://detail.chiebukuro.yahoo.co.jp/qa/question_detail/q1116589591 (必ず 3 になる同型) 。初稿「止まった時計と遅れる時計」は簡単すぎ、2 案目「トーナメントの試合数」は面白くない、により 2026-09-20 レビューで差し替え。文面はオリジナルに書き下ろし(表現は書き直し済み)。', 1);

-- A44
INSERT INTO quiz_stock_items (set_id, content_key, quiz_type, difficulty, question_text, answer_text, content_fields, source_note, is_active)
VALUES ((SELECT id FROM batch_sets WHERE set_code = 'logic-training-1'),
        (SELECT CONCAT('morning-', LPAD(COALESCE(MAX(CAST(SUBSTRING_INDEX(t.content_key, '-', -1) AS UNSIGNED)), 0) + 1, 3, '0')) FROM (SELECT q.content_key FROM quiz_stock_items q JOIN batch_sets b ON b.id = q.set_id WHERE b.set_code = 'logic-training-1' AND q.content_key LIKE 'morning-%') t),
        'L1', 'light',
        'カードの5文字は、ある決まりで並んでいる。「?」のカードに入るひらがな1文字はなんだ?',
        'な(親指・人差し指・中指・薬指・小指)',
        '{"hook":"たった5文字の暗号だ","hint":"自分の手を見てみろ!","question":"カードの5文字は、ある決まりで並んでいる。「?」のカードに入るひらがな1文字はなんだ?","answer":"な(親指・人差し指・中指・薬指・小指)","explanation":"お・ひ・?・く・こは、親指・人差し指・中指・薬指・小指の頭文字。だから「?」は中指の「な」。文字だけを見ていると気づけないが、手を広げれば一発だ。","coach_comment":"答えはいつも手元にあるぞ!","tags":["なぞなぞ","朝の一問","法則発見"],"summary":"「お・ひ・?・く・こ」の?を問う法則発見なぞなぞ。親指〜小指の頭文字で答えは「な」(中指)。5文字は問題文に書かずカードの絵で見せる。五十音や数字を疑わせて身体の名前に気づかせる。","illustration_scene":"朝日が差し込む木の机に、白いカードが5枚横一列に並び、左から「お」「ひ」「?」「く」「こ」と1文字ずつ大きく書かれている。文字はこの5枚のカードの文字だけを描き、他の文字・数字は描かない。手や人物は描かない。"}',
        '類型: 法則発見(指の名前の頭文字。作者不詳の定番)。流布例: https://nazoq.com/hard/Q002762.html , https://www.nazo2.net/jyoukyuu/062.html 。5 文字は問題文に書かずイラスト(カード)で提示する(2026-09-20 レビュー)。初稿「一〜十の画数(四)」は簡単、2 案目「3 時 15 分の針の角度(7.5 度)」は数学っぽい、により 2026-09-20 レビューで差し替え。文面はオリジナルに書き下ろし(表現は書き直し済み)。', 1);

-- A41
INSERT INTO quiz_stock_items (set_id, content_key, quiz_type, difficulty, question_text, answer_text, content_fields, source_note, is_active)
VALUES ((SELECT id FROM batch_sets WHERE set_code = 'logic-training-1'),
        (SELECT CONCAT('morning-', LPAD(COALESCE(MAX(CAST(SUBSTRING_INDEX(t.content_key, '-', -1) AS UNSIGNED)), 0) + 1, 3, '0')) FROM (SELECT q.content_key FROM quiz_stock_items q JOIN batch_sets b ON b.id = q.set_id WHERE b.set_code = 'logic-training-1' AND q.content_key LIKE 'morning-%') t),
        'L1', 'light',
        '黒板の3つの言葉から、ある決まりで1文字ずつ取り出すと、別の言葉が現れる。その言葉はなんだ?',
        'けんか(各語の2文字目)',
        '{"hook":"3つの言葉に暗号が隠れてる","hint":"全部そろえて縦に読め!","question":"黒板の3つの言葉から、ある決まりで1文字ずつ取り出すと、別の言葉が現れる。その言葉はなんだ?","answer":"けんか(各語の2文字目)","explanation":"たけやぶ、ほんだな、さかみち。2文字目だけを順に拾うと、け・ん・か。つなげて「けんか」だ。1文字目も3文字目も言葉にならない。位置をそろえるのが鍵。","coach_comment":"文字の居場所を疑えたな、見事!","tags":["なぞなぞ","朝の一問","暗号"],"summary":"「たけやぶ・ほんだな・さかみち」から同じ位置の文字を拾う規則を見つけ、2文字目でけんかを導く暗号なぞなぞ。3語は問題文に書かず黒板の絵で見せる。位置をそろえる発想が鍵。","illustration_scene":"朝日が差し込む教室の黒板に、チョークで「たけやぶ」「ほんだな」「さかみち」の3語が縦に大きく書かれている。文字はこの3語だけを描き、他の文字・数字は描かない。人物は描かない。"}',
        'オリジナル書き下ろし(自作問題)。類型: 暗号(各語の同じ位置の文字を拾う縦読み)。形式は定番の位置抽出暗号で、語の組み合わせは自作(1 文字目「たほさ」・3 文字目「やだみ」・4 文字目「ぶなち」はいずれも語にならないことを verify_logic.py で確認)。初稿「8 を 8 個使って 1000」・2 案目「つく = 嘘」は 2026-09-20 レビューで単純な計算問題 / 簡単により差し替え。', 1);

-- A43
INSERT INTO quiz_stock_items (set_id, content_key, quiz_type, difficulty, question_text, answer_text, content_fields, source_note, is_active)
VALUES ((SELECT id FROM batch_sets WHERE set_code = 'logic-training-1'),
        (SELECT CONCAT('morning-', LPAD(COALESCE(MAX(CAST(SUBSTRING_INDEX(t.content_key, '-', -1) AS UNSIGNED)), 0) + 1, 3, '0')) FROM (SELECT q.content_key FROM quiz_stock_items q JOIN batch_sets b ON b.id = q.set_id WHERE b.set_code = 'logic-training-1' AND q.content_key LIKE 'morning-%') t),
        'L1', 'light',
        '黒板に漢字の部品が4つ。全部を使って2文字の熟語を1つ作ってくれ。身のまわりにある道具の名前だ。',
        '時計(日+寺=時、言+十=計)',
        '{"hook":"バラバラの部品を組み立てろ","hint":"2つずつ組んで、熟語にしろ!","question":"黒板に漢字の部品が4つ。全部を使って2文字の熟語を1つ作ってくれ。身のまわりにある道具の名前だ。","answer":"時計(日+寺=時、言+十=計)","explanation":"日と寺を組むと「時」、言と十を組むと「計」。合わせて「時計」だ。4つを一度に眺めても見えないが、2つずつ組む発想に切り替えると現れる。","coach_comment":"部品を2つずつ、それが正解だ!","tags":["漢字","朝の一問","合体漢字"],"summary":"「日・寺・言・十」の4部品を2つずつ組んで熟語「時計」を作る合体漢字パズル。4つを一度に組もうとすると詰まり、2つずつに分ける発想が要る。部品は問題文に書かず黒板の絵で見せる。","illustration_scene":"朝日が差し込む教室の黒板に、チョークで「日」「寺」「言」「十」の4文字がバラバラの位置に大きく書かれている。文字はこの4字だけを描き、他の文字・数字は描かない。人物は描かない。"}',
        '類型: 合体漢字パズル(部品を組んで熟語を作る。作者不詳の定番形式)。形式の流布例: https://web.quizknock.com/tag/%E5%90%88%E4%BD%93%E6%BC%A2%E5%AD%97 , https://kaigoshoku.mynavi.jp/contents/kaigonomirailab/recreation/kanji/1moji04/ , https://utages.net/entry/2023/11/25/210014 。部品の組み合わせ(日・寺・言・十 → 時計)は自作問題。文面はオリジナルに書き下ろし(表現は書き直し済み)。初稿「時計の文字盤を直線 2 本で 3 分割」・2 案目「大に一画足して天」は 2026-09-20 レビューで単純な計算問題 / 簡単により差し替え。', 1);

-- A46
INSERT INTO quiz_stock_items (set_id, content_key, quiz_type, difficulty, question_text, answer_text, content_fields, source_note, is_active)
VALUES ((SELECT id FROM batch_sets WHERE set_code = 'logic-training-1'),
        (SELECT CONCAT('morning-', LPAD(COALESCE(MAX(CAST(SUBSTRING_INDEX(t.content_key, '-', -1) AS UNSIGNED)), 0) + 1, 3, '0')) FROM (SELECT q.content_key FROM quiz_stock_items q JOIN batch_sets b ON b.id = q.set_id WHERE b.set_code = 'logic-training-1' AND q.content_key LIKE 'morning-%') t),
        'L1', 'light',
        'さんま、しいたけ、ごぼう。この3つはある順番で並んでいる。では、次に来る言葉には何が隠れている?',
        '数字の6(さんま3・しいたけ4・ごぼう5)',
        '{"hook":"3つの言葉が順番に並ぶ","hint":"声に出して頭から読め!","question":"さんま、しいたけ、ごぼう。この3つはある順番で並んでいる。では、次に来る言葉には何が隠れている?","answer":"数字の6(さんま3・しいたけ4・ごぼう5)","explanation":"さんま(3)、しいたけ(4)、ごぼう(5)。どれも頭に数字が隠れていて、3から1つずつ増えている。だから次は6が隠れた言葉、たとえば「ろくろ」だ。","coach_comment":"言葉の中の数字に気づいたな!","tags":["なぞなぞ","朝の一問","法則発見"],"summary":"さんま・しいたけ・ごぼうに隠れた3・4・5に気づき、次は6と答える法則発見なぞなぞ。隠れた数字に気づく段と、増えていることに気づく段の2段構え。","illustration_scene":"朝日が差し込む台所のまな板の上に、さんま1匹、しいたけ1つ、ごぼう1本が左から順に並び、その右に大きな「?」が浮かんでいる。文字・数字は描かない。人物は描かない。"}',
        'オリジナル書き下ろし(自作問題)。類型: 法則発見(語頭に隠れた数字 + 数列)。隠れ数字・隠れ言葉の形式は定番だが、語の組み合わせと「数が 1 つずつ増える」を重ねた点は自作。初稿「地球の赤道に巻いたロープ(約 16cm)」・2 案目「たてる = 顔」は 2026-09-20 レビューで単純な計算問題(数学) / 簡単により差し替え。', 1);

-- A45
INSERT INTO quiz_stock_items (set_id, content_key, quiz_type, difficulty, question_text, answer_text, content_fields, source_note, is_active)
VALUES ((SELECT id FROM batch_sets WHERE set_code = 'logic-training-1'),
        (SELECT CONCAT('morning-', LPAD(COALESCE(MAX(CAST(SUBSTRING_INDEX(t.content_key, '-', -1) AS UNSIGNED)), 0) + 1, 3, '0')) FROM (SELECT q.content_key FROM quiz_stock_items q JOIN batch_sets b ON b.id = q.set_id WHERE b.set_code = 'logic-training-1' AND q.content_key LIKE 'morning-%') t),
        'L1', 'light',
        '黒板の3組は、ある決まりで結ばれている。同じ決まりなら、最後の「馬」は何になる?',
        'えみ=笑み(母音を1つ先へずらす)',
        '{"hook":"今日は朝いちばんの難問だ","hint":"あいうえお表を思い出せ!","question":"黒板の3組は、ある決まりで結ばれている。同じ決まりなら、最後の「馬」は何になる?","answer":"えみ=笑み(母音を1つ先へずらす)","explanation":"かき→きく、あめ→いも、かに→きぬ。どの字も、あいうえお表で母音を1つ先へ送っている(か→き、き→く)。だから、うま→えみ。答えは笑みだ。","coach_comment":"この難問を越えたか、たいしたものだ!","tags":["なぞなぞ","朝の一問","法則発見"],"summary":"「柿→菊」「雨→芋」「蟹→絹」から「読みの各文字の母音を1つ先へずらす(あ→い→う→え→お)」法則を見つけ、馬→えみ(笑み)を導く朝の最難問。3組は問題文に書かず黒板の絵で見せる。","illustration_scene":"朝日が差し込む教室の黒板に、チョークで「柿 → 菊」「雨 → 芋」「蟹 → 絹」「馬 → ?」の4行が縦に大きく書かれている。文字はこの4行だけを描き、他の文字・数字は描かない。人物・動物は描かない。"}',
        'オリジナル書き下ろし(自作問題)。類型: 法則発見(読みの母音を 1 段送る)。形式は A32(柿=傘・星=端・足=飯 → 西=腰。w5 で承認済み)と同じ対応当てで、語の組み合わせは自作。初稿「本棚の虫」・2 案目「マラソンの順位」・3 案目「鏡に映せない顔」・4 案目「濁点の法則」・5 案目「循環並べ替え」は 2026-09-20 レビューで面白くない / 簡単により差し替え。', 1);

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
