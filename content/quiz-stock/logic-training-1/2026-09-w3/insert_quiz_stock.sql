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

-- A46
INSERT INTO quiz_stock_items (set_id, content_key, quiz_type, difficulty, question_text, answer_text, content_fields, source_note, is_active)
VALUES ((SELECT id FROM batch_sets WHERE set_code = 'logic-training-1'),
        (SELECT CONCAT('morning-', LPAD(COALESCE(MAX(CAST(SUBSTRING_INDEX(t.content_key, '-', -1) AS UNSIGNED)), 0) + 1, 3, '0')) FROM (SELECT q.content_key FROM quiz_stock_items q JOIN batch_sets b ON b.id = q.set_id WHERE b.set_code = 'logic-training-1' AND q.content_key LIKE 'morning-%') t),
        'L1', 'light',
        '黒板の磁石を3個だけ動かし、10個全部で同じ大きさの下向きの正三角形を作ってくれ。磁石を重ねたり、黒板を回したりしてはいけない。',
        '①を一番下へ、⑦と⑩を②③の両外側へ',
        '{"hook":"ほとんどそのままで逆向きに!","hint":"動かさずに残せる形を探せ!","question":"黒板の磁石を3個だけ動かし、10個全部で同じ大きさの下向きの正三角形を作ってくれ。磁石を重ねたり、黒板を回したりしてはいけない。","answer":"①を一番下へ、⑦と⑩を②③の両外側へ","explanation":"①⑦⑩だけを動かして、この配置にする。\\n⑦　②　③　⑩\\n　④　⑤　⑥\\n　　⑧　⑨\\n　　　①\\n真ん中の7個はそのまま。三角形全体を回す必要はない。","coach_comment":"残せる形を見抜いたな、見事だ!","tags":["視覚パズル","朝の一問","配置転換"],"summary":"正三角形に1・2・3・4個と並ぶ磁石10個を3個だけ動かし、同じ大きさの下向きの正三角形へ。頂点①を最下段へ、底辺両端⑦⑩を②③の両外側へ移す。中央7個を共有する配置を見抜く。","illustration_scene":"朝日が差す教室の黒板を正面から見る。同色・同寸の白い丸型磁石10個を、中心が正三角形の格子になるよう等間隔で並べる。上から1・2・3・4個の4段で左右対称。各磁石に黒字で、上段から左→右に「1」「2」「3」「4」「5」「6」「7」「8」「9」「10」と記す。上下左右に十分な余白。矢印・補助線・完成形・他の文字・人物は描かない。"}',
        '類型: 10枚のコインを3枚動かして三角形を逆向きにする古典配置パズル。流布例: https://suugaku-kyousitu.com/blog/14560/ (問題2), https://arxiv.org/abs/1810.02202 。2026-09-20 Codexが直接開いて確認。コインを黒板の丸型磁石に置き換え、文面は書き直し済み。数値を計算する問題ではなく移動位置を問う。番号は解説との対応用で、磁石の位置以外の区別はしない。', 1);

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
        '黒板の上の3組には、同じ仕掛けがある。最後の「?」に入る生き物は何だろう?',
        'オオカミ(flowを逆につづるとwolf)',
        '{"hook":"つながるはずのない言葉たち","hint":"別の言語に着替えてみろ!","question":"黒板の上の3組には、同じ仕掛けがある。最後の「?」に入る生き物は何だろう?","answer":"オオカミ(flowを逆につづるとwolf)","explanation":"英語にして逆から読む。dog→god、net→ten、star→rats。流れはflow。逆につづるとwolf、オオカミだ。","coach_comment":"言葉の境界を越えたな、見事だ!","tags":["言葉あそび","朝の一問","法則発見"],"summary":"犬→神、網→十、星→ネズミたちを英訳し、つづりを逆順にする法則を発見。流れ→flow→wolf→オオカミを導く。英語への領域転換と逆順操作を組み合わせる。","illustration_scene":"朝日が差す教室の黒板に「犬 → 神」「網 → 十」「星 → ネズミたち」「流れ → ?」の4行を上から順に大きく、同じ白いチョークで書く。指定の4行だけを正確な字形で描き、英字・他の文字・絵・人物・動物は描かない。"}',
        'オリジナル書き下ろし(自作問題)。英単語の逆つづりという既知の言葉あそびを、日本語の対応から発見する形式に構成。流布例: https://www.sightwordsgame.com/vocabulary-words/word-play/reverse-pair/ , https://www.enigami.fun/semordnilaps 。2026-09-20 Codex が直接開いて確認。前者に dog/God・net/ten・star/rats・flow/wolf の全組が掲載。日本語の問題文・組み合わせは自作で、特定の既存問題の転載ではない。', 1);

-- A43
INSERT INTO quiz_stock_items (set_id, content_key, quiz_type, difficulty, question_text, answer_text, content_fields, source_note, is_active)
VALUES ((SELECT id FROM batch_sets WHERE set_code = 'logic-training-1'),
        (SELECT CONCAT('morning-', LPAD(COALESCE(MAX(CAST(SUBSTRING_INDEX(t.content_key, '-', -1) AS UNSIGNED)), 0) + 1, 3, '0')) FROM (SELECT q.content_key FROM quiz_stock_items q JOIN batch_sets b ON b.id = q.set_id WHERE b.set_code = 'logic-training-1' AND q.content_key LIKE 'morning-%') t),
        'L1', 'light',
        'ペンを一度も離さず、一筆書きで黒板の9つの点すべての中心を通ってくれ。使えるのは、つながった4本の直線。同じ線をなぞらず、どう描く?',
        '点の並びからはみ出す(右→左下→上→右下)',
        '{"hook":"頭の中で線を引けるか?","hint":"折り返す場所を疑ってみろ!","question":"ペンを一度も離さず、一筆書きで黒板の9つの点すべての中心を通ってくれ。使えるのは、つながった4本の直線。同じ線をなぞらず、どう描く?","answer":"点の並びからはみ出す(右→左下→上→右下)","explanation":"●1　●2　●3　A\\n●4　●5　●6\\n●7　●8　●9\\nB\\n1→A→B→1→9と一筆書き。A・Bは折り返し位置で、点の間隔1つ分外。","coach_comment":"見えない枠を飛び出せたな!","tags":["視覚パズル","朝の一問","発想転換"],"summary":"縦横等間隔の9点を4本の直線で一筆書きする古典。右上の右と左下の下へはみ出して折り返す。点の並びが作る見えない枠を越え、4本が連続する経路を組み立てる。","illustration_scene":"朝日が差す教室の大きな黒板。中央に同じ大きさの白い丸を縦3個・横3個、縦横同じ間隔の正方形配置で描く。9個の丸の周囲には点の間隔2つ分以上の余白を均等に残す。結ぶ線・矢印・枠線・文字・数字・他の記号・人物は描かない。黒板を正面から見た構図。"}',
        '類型: ナインドットパズル(9点を4直線で一筆書きする古典)。流布例: https://www.a-spcc.jp/promotion/1/blog_detail.html?key=entry&value=116 , https://detail.chiebukuro.yahoo.co.jp/qa/question_detail/q11149057731 。2026-09-20 Codex が直接開いて確認。文面は書き直し済み。点の中心を通る条件で太い線や点の縁を利用する抜け道を除外。同じ点の再通過は許容し、同じ線の重複だけを禁止。過去w3/w5のresearchでは候補に挙がったがstock_itemsには未採用。', 1);

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
        '王が、各自の馬を持つ2人に競走を命じた。「後にゴールした馬の元の持ち主が勝ち」。2人は動かない。どんな一言で、2人とも全力で走り出す?',
        '互いの馬に乗り換えろ',
        '{"hook":"勝負を動かす、たった一言","hint":"勝つのは騎手か、持ち主か?考えろ!","question":"王が、各自の馬を持つ2人に競走を命じた。「後にゴールした馬の元の持ち主が勝ち」。2人は動かない。どんな一言で、2人とも全力で走り出す?","answer":"互いの馬に乗り換えろ","explanation":"所有者は変えず、乗る馬だけ交換する。相手の馬で先着すれば、自分の馬は後着して自分の勝ち。同じルールのまま、相手の馬を速く走らせるほど有利になる。","coach_comment":"自分が乗る馬と、自分の馬を分けて考えたな!","tags":["水平思考","夜の一問","立場の転換"],"summary":"後着した馬の元の持ち主が勝つ競走で、所有者を変えず互いの馬に乗り換える。自分の先着が自分の馬の後着になるよう、騎手と所有者の関係を入れ替える古典。","illustration_scene":"夜、松明に照らされた馬場に、2頭の馬が並んで立ち止まり、その上に大きな「?」が浮かぶ。馬に乗る2人の騎手は後ろ姿で顔は描かない。遠くのゴールの旗には文字を入れない。文字・数字は描かない。"}',
        '類型: 水平思考(のろのろ馬レース。作者不詳の古典)。流布例: https://diamond.jp/articles/-/341503 , https://www.oricon.co.jp/article/2556546/ , https://sist8.com/2horse 。文面はオリジナルに書き下ろし(表現は書き直し済み)。', 1);

-- C43
INSERT INTO quiz_stock_items (set_id, content_key, quiz_type, difficulty, question_text, answer_text, content_fields, source_note, is_active)
VALUES ((SELECT id FROM batch_sets WHERE set_code = 'logic-training-1'),
        (SELECT CONCAT('night-', LPAD(COALESCE(MAX(CAST(SUBSTRING_INDEX(t.content_key, '-', -1) AS UNSIGNED)), 0) + 1, 3, '0')) FROM (SELECT q.content_key FROM quiz_stock_items q JOIN batch_sets b ON b.id = q.set_id WHERE b.set_code = 'logic-training-1' AND q.content_key LIKE 'night-%') t),
        'L1', 'deep',
        '机にあるものを使って、ロウソクをコルクの壁に固定したい。火をつけても下の机にロウを落とさない方法は?',
        '箱を空にして壁に留め、ロウ受け兼台にする',
        '{"hook":"見慣れた道具が化けるぞ","hint":"道具の使い道を決めつけるな!","question":"机にあるものを使って、ロウソクをコルクの壁に固定したい。火をつけても下の机にロウを落とさない方法は?","answer":"箱を空にして壁に留め、ロウ受け兼台にする","explanation":"空にした箱の側面を画びょうで壁に留め、底にロウソクを立てる。箱が台とロウ受けを兼ねる。画びょうの入れ物も、使える道具の一つなのだ。","coach_comment":"入れ物まで道具にできたな、見事だ!","tags":["水平思考","夜の一問","道具"],"summary":"ロウソク・マッチ・画びょうの箱でロウソクを壁に固定する古典(ドゥンカーのロウソク問題)。箱を画びょうで壁に留めて台にする。機能的固着を外す発想を問う。","illustration_scene":"夜、室内灯に照らされた机に、火のついていないロウソク1本、表紙を開いた無地のブックマッチ1冊、たくさんの画びょうがぎっしり入った、浅く丈夫な厚紙製のふたなしの箱。紙の質感と角の折り目を見せる。ブックマッチは薄い紙の表紙に平たい紙製マッチが一列につながる冊子型で、箱型にしない。背後は平らなコルク壁。箱は机に置き、中の画びょうがよく見える。壁に大きな「?」。他の文字・数字・人物は描かない。"}',
        '類型: 水平思考(ロウソク問題。1945 年ドゥンカーの心理学実験に由来し、作者を離れて古典として流布)。流布例: https://ja.wikipedia.org/wiki/%E3%83%AD%E3%82%A6%E3%82%BD%E3%82%AF%E5%95%8F%E9%A1%8C , https://www.weblio.jp/content/%E3%83%AD%E3%82%A6%E3%82%BD%E3%82%AF%E5%95%8F%E9%A1%8C , https://mitani3.com/blog/2010/07/post-223.html 。文面はオリジナルに書き下ろし(表現は書き直し済み)。', 1);

-- C45
INSERT INTO quiz_stock_items (set_id, content_key, quiz_type, difficulty, question_text, answer_text, content_fields, source_note, is_active)
VALUES ((SELECT id FROM batch_sets WHERE set_code = 'logic-training-1'),
        (SELECT CONCAT('night-', LPAD(COALESCE(MAX(CAST(SUBSTRING_INDEX(t.content_key, '-', -1) AS UNSIGNED)), 0) + 1, 3, '0')) FROM (SELECT q.content_key FROM quiz_stock_items q JOIN batch_sets b ON b.id = q.set_id WHERE b.set_code = 'logic-training-1' AND q.content_key LIKE 'night-%') t),
        'L1', 'deep',
        '高さ制限の橋に、トラックの屋根が数センチつかえて進めない。荷台は空で、橋を壊すことも車を切ることもできない。どうやって通す?',
        'タイヤの空気を抜いて車高を下げる',
        '{"hook":"橋を壊す話まで出たらしいぞ!","hint":"橋じゃなく、車の方を見てみろ!","question":"高さ制限の橋に、トラックの屋根が数センチつかえて進めない。荷台は空で、橋を壊すことも車を切ることもできない。どうやって通す?","answer":"タイヤの空気を抜いて車高を下げる","explanation":"タイヤの空気を抜けば車体全体が数センチ沈み、屋根が橋を抜ける。通り過ぎたら空気を入れ直せばいい。橋か荷物ばかり見てしまうが、答えは足元にあった。","coach_comment":"答えは足元にあったな、よく気づいた!","tags":["水平思考","夜の一問","視点転換"],"summary":"高さ制限の橋につかえたトラックを、タイヤの空気を抜いて車高を下げて通す古典。橋や荷物へ向かう注意を足元へ向け直す視点転換を問う。水も計算も使わない。","illustration_scene":"夜の街灯に照らされた高架橋の下。大型トラックの箱型の屋根が橋げたに当たり、すき間なく止まっている。屋根と橋げたの接点が見える真横からの構図。橋の上に大きな「?」。空気の抜けたタイヤ・空気を抜く動作・工具・レッカー車・人物・文字・数字は描かない。"}',
        '類型: 高さ制限の橋につかえたトラック(Stuck Truck。作者不詳で広く流布する水平思考の説話)。流布例: https://philipchircop.wordpress.com/2012/08/08/let-some-air-out-of-the-tyres/ (本文末に Source unknown 表記) , https://reasontestprep.com/stuck-truck/ 。2026-09-20 Claude が両本文を直接確認。原話の子ども・レッカー車の場面描写は使わず、道具と制約だけを示す日本語の出題へ書き直し済み。物理的な沈下量を機械検証したものではない。', 1);

-- C46
INSERT INTO quiz_stock_items (set_id, content_key, quiz_type, difficulty, question_text, answer_text, content_fields, source_note, is_active)
VALUES ((SELECT id FROM batch_sets WHERE set_code = 'logic-training-1'),
        (SELECT CONCAT('night-', LPAD(COALESCE(MAX(CAST(SUBSTRING_INDEX(t.content_key, '-', -1) AS UNSIGNED)), 0) + 1, 3, '0')) FROM (SELECT q.content_key FROM quiz_stock_items q JOIN batch_sets b ON b.id = q.set_id WHERE b.set_code = 'logic-training-1' AND q.content_key LIKE 'night-%') t),
        'L1', 'deep',
        '輪が3個ずつつながった鎖が4本ある。12個全部をつなぎ合わせて、枝分かれのない大きな輪にしたい。つなぐために開いて閉じられる輪は3個だけ。どうつなぐ?',
        '1本の3輪を全部開き、残り3本のつなぎに使う',
        '{"hook":"つなぐ前に、何をする?","hint":"今あるまとまりを疑ってみろ!","question":"輪が3個ずつつながった鎖が4本ある。12個全部をつなぎ合わせて、枝分かれのない大きな輪にしたい。つなぐために開いて閉じられる輪は3個だけ。どうつなぐ?","answer":"1本の3輪を全部開き、残り3本のつなぎに使う","explanation":"1本だけをばらし、3個の輪をつなぎ部品にする。残る3本を三角形状に置き、隣り合う端を1個ずつでつないで閉じる。12個が一周する鎖になる。","coach_comment":"つなぐために一度ばらす、いい発想だ!","tags":["水平思考","夜の一問","組み替え"],"summary":"3輪の鎖4本を、3輪だけ開閉して12輪の閉じた鎖にする古典。1本を全てばらして接続部品に転用し、残る3本をつなぐ。切る場所を分散せず一組に集中させる。","illustration_scene":"夜の作業台を照らす卓上灯。銀色の輪が3個ずつつながった短い鎖を4本、互いに離して横一列に置く。全12個の輪は閉じていて、端同士はつながっていない。そばにペンチと大きな「?」。完成した輪・開いた輪・矢印・文字・数字・人物は描かない。"}',
        '類型: 4本の鎖をつなぐ古典(Four Chains)。流布例: https://www.puzzleprime.com/puzzles/brain-teasers/insight/four-chains/ , https://suresolv.com/brain-teaser/make-a-circular-chain-riddle 。2026-09-20 Codexが両本文を直接確認(前者にUnknown Author表記)。金額や最少回数を答えにせず、3輪だけ開閉する手順を問う形に書き直し済み。', 1);

-- C44
INSERT INTO quiz_stock_items (set_id, content_key, quiz_type, difficulty, question_text, answer_text, content_fields, source_note, is_active)
VALUES ((SELECT id FROM batch_sets WHERE set_code = 'logic-training-1'),
        (SELECT CONCAT('night-', LPAD(COALESCE(MAX(CAST(SUBSTRING_INDEX(t.content_key, '-', -1) AS UNSIGNED)), 0) + 1, 3, '0')) FROM (SELECT q.content_key FROM quiz_stock_items q JOIN batch_sets b ON b.id = q.set_id WHERE b.set_code = 'logic-training-1' AND q.content_key LIKE 'night-%') t),
        'L1', 'deep',
        '校庭の地面に埋まった細い鉄パイプの中にピンポン玉が落ちた。手は届かないし、棒でも取れない。パイプは抜けそうにない。校庭にあるものだけを使い、玉を取り出すには?',
        'パイプに水を注いで玉を浮かせる',
        '{"hook":"みんな棒を探しに行ったらしい","hint":"取りに行くな、上げてこい!","question":"校庭の地面に埋まった細い鉄パイプの中にピンポン玉が落ちた。手は届かないし、棒でも取れない。パイプは抜けそうにない。校庭にあるものだけを使い、玉を取り出すには?","answer":"パイプに水を注いで玉を浮かせる","explanation":"水を注げば、軽い玉は水面と一緒に上がってくる。道具を細く長くする方向ではなく、玉の方を持ち上げる方向へ切り替える。水は校庭の水道で汲める。","coach_comment":"浮かせる手があったな、お見事!","tags":["水平思考","夜の一問","発想転換"],"summary":"校庭の地面に刺さったパイプの底のピンポン玉を、水を注いで浮かせて取り出す古典。道具で取りに行く方向から玉を上げる方向へ発想を変える。パイプを抜く別解と持ち込み道具は文面で塞ぐ。","illustration_scene":"夜の校庭、外灯の明かり。乾いた地面から少しだけ顔を出した細い鉄パイプ。その口に人の指先が差し込まれているが、深い底にある白いピンポン玉には全く届いていない。パイプの中が断面で見える構図で、指先と玉の距離が分かる。上に大きな「?」。顔・水・バケツ・ボトル・棒・道具・文字・数字は描かない。"}',
        '類型: Ping Pong Ball(作者不詳で広く流布する水平思考パズル)。流布例: https://www.puzzleprime.com/puzzles/brain-teasers/insight/ping-pong-ball/ (Unknown Author 表記) , https://puzzlefry.com/puzzles/ping-pong-ball-stuck-into-the-pipe-puzzle/ 。2026-09-21 Claude が両本文を直接確認。原話が並べる道具一覧(ラケット・靴ひも・水のボトル)は答えへの道順になるため使わず、状況だけを示す日本語の出題へ書き直し済み。浮力の条件を機械検証したものではない。', 1);

-- C48
INSERT INTO quiz_stock_items (set_id, content_key, quiz_type, difficulty, question_text, answer_text, content_fields, source_note, is_active)
VALUES ((SELECT id FROM batch_sets WHERE set_code = 'logic-training-1'),
        (SELECT CONCAT('night-', LPAD(COALESCE(MAX(CAST(SUBSTRING_INDEX(t.content_key, '-', -1) AS UNSIGNED)), 0) + 1, 3, '0')) FROM (SELECT q.content_key FROM quiz_stock_items q JOIN batch_sets b ON b.id = q.set_id WHERE b.set_code = 'logic-training-1' AND q.content_key LIKE 'night-%') t),
        'L1', 'deep',
        '病院に急ぐ老人、運転できる親友、ずっと話したかった人が雨宿り中。二人乗りの車で来た君は、老人をすぐ送りつつ会話の機会も逃したくない。どうする?',
        '親友に車を託して老人を送り、自分は残って話す',
        '{"hook":"一人を選ぶしかないのか?","hint":"席の使い方から考え直してみろ!","question":"病院に急ぐ老人、運転できる親友、ずっと話したかった人が雨宿り中。二人乗りの車で来た君は、老人をすぐ送りつつ会話の機会も逃したくない。どうする?","answer":"親友に車を託して老人を送り、自分は残って話す","explanation":"親友に運転を頼み、老人を助手席に乗せて病院へ。自分は降りて、話したかった人と雨宿りを続ける。二人乗りでも、自分が運転席に居続ける必要はない。","coach_comment":"選ぶのは同乗者だけじゃないと気づいたな!","tags":["水平思考","夜の一問","役割分担"],"summary":"二人乗りの車と雨宿りする3人の古典。病院へ急ぐ人は運転できる親友に送りを任せ、自分は話したかった人と残る。運転席を自分の固定席と考える前提を外す。","illustration_scene":"雨の夜、屋根のあるバス停に3人の大人が後ろ姿で雨宿りしている。そばに、前席2つだけの小さな車が停まり、運転席にもう1人の後ろ姿。大きな「?」が浮かぶ。顔・文字・数字・鍵の受け渡し・乗り降りの動作は描かない。"}',
        '類型: 二人乗りの車とバス停の3人(Tough Decisions / Bus-stop)。流布例: https://www.puzzleprime.com/puzzles/brain-teasers/insight/tough-decisions/ , https://www.youthfutureproject.org/wp-content/uploads/SportsPeaceWorkshop2013-Descriptions-of-the-games.pdf 。2026-09-20 Codexが両本文を直接確認。前者にUnknown Author表記。死の切迫や理想の恋人の表現を、病院へ急ぐ人と話したかった人へ変更。運転可能な親友を明示し書き直し済み。唯一の最善策や医療上の対応を問う問題ではない。', 1);

-- C47
INSERT INTO quiz_stock_items (set_id, content_key, quiz_type, difficulty, question_text, answer_text, content_fields, source_note, is_active)
VALUES ((SELECT id FROM batch_sets WHERE set_code = 'logic-training-1'),
        (SELECT CONCAT('night-', LPAD(COALESCE(MAX(CAST(SUBSTRING_INDEX(t.content_key, '-', -1) AS UNSIGNED)), 0) + 1, 3, '0')) FROM (SELECT q.content_key FROM quiz_stock_items q JOIN batch_sets b ON b.id = q.set_id WHERE b.set_code = 'logic-training-1' AND q.content_key LIKE 'night-%') t),
        'L1', 'deep',
        '初心者がチェスの達人2人と別々の盤で同時に対局。片方で白の先手、もう片方で黒の後手を持つ。時間制限なし。少なくとも1局は負けずに終える作戦は?',
        '達人の指し手を別の盤に写し、達人同士を対戦させる',
        '{"hook":"強敵が二人なら道が開ける?","hint":"二つの勝負を別々に考えるな!","question":"初心者がチェスの達人2人と別々の盤で同時に対局。片方で白の先手、もう片方で黒の後手を持つ。時間制限なし。少なくとも1局は負けずに終える作戦は?","answer":"達人の指し手を別の盤に写し、達人同士を対戦させる","explanation":"白の達人が指した手を、自分が白の盤でまねる。黒の達人の返し手を、もう一方でまねる。これを続ければ実質は達人同士の1局。自分は1勝1敗か、2引き分けになる。","coach_comment":"相手の強さを、もう一つの勝負に借りたな!","tags":["水平思考","夜の一問","作戦"],"summary":"チェスの達人2人との同時対局で白と黒を持ち、互いの指し手をもう一方の盤へ写す古典。実質的に達人同士を対戦させ、初心者でも1勝1敗か2引き分けにする。時計は使わない。","illustration_scene":"夜の室内を照らす卓上灯。離れた2つの机にチェス盤が1面ずつあり、駒は対局開始前の配置。中央に立つ1人と、各机の奥に座る1人ずつを遠景の後ろ姿で描く。大きな「?」。顔・指し手の矢印・文字・数字・時計は描かない。"}',
        '類型: 達人2人とのチェス同時対局で指し手を中継する古典。流布例: https://groups.google.com/g/rec.puzzles/c/oadPpJyrGus (1995年の議論) , https://simonrs.com/eulercircle/cgt2021/yutao-dongshen-scoring.pdf (Scoring Gamesのman-in-the-middleの例)。2026-09-20 Codexが両本文を直接確認。複数の小説・手品でも使われる一般的な解法構造で、特定作品の場面は用いず書き直し済み。時間切れによる反例を防ぐため時間制限なし。競技大会の不正可否でなく、盤を使う仮想の作戦問題。', 1);
