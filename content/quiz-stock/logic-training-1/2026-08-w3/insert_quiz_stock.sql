-- 2026-08-w3 問題ストック補充投入(21 問。レビュー承認後に実行)
-- 生成元: content/quiz-stock/logic-training-1/2026-08-w3/stock_items.py(単一ソース)。適用先: ローカル MySQL / Aurora(acps)
-- set_id は set_code から解決するため両環境共通で実行できる。
-- content_key はスロット内の既存最大連番 + 1 を適用時に解決する(V007。両環境で同一値になる)。

-- A15
INSERT INTO quiz_stock_items (set_id, content_key, quiz_type, difficulty, question_text, answer_text, content_fields, source_note, is_active)
VALUES ((SELECT id FROM batch_sets WHERE set_code = 'logic-training-1'),
        (SELECT CONCAT('morning-', LPAD(COALESCE(MAX(CAST(SUBSTRING_INDEX(t.content_key, '-', -1) AS UNSIGNED)), 0) + 1, 3, '0')) FROM (SELECT q.content_key FROM quiz_stock_items q JOIN batch_sets b ON b.id = q.set_id WHERE b.set_code = 'logic-training-1' AND q.content_key LIKE 'morning-%') t),
        'L1', 'light',
        'どれだけこぼしても、不思議なことにまったく減らないものがある。それはなんだ?',
        '愚痴(こぼしても減らない)',
        '{"hook":"今日もため込んでないか?","hint":"口から出るのに減らない!","question":"どれだけこぼしても、不思議なことにまったく減らないものがある。それはなんだ?","answer":"愚痴(こぼしても減らない)","explanation":"答えは愚痴。水や砂はこぼせば減るが、愚痴は「こぼす」と言ってもいっこうに減らない。ため込まず、ほどほどに。","coach_comment":"たまには吐き出していいぞ!","tags":["なぞなぞ","朝の一問","言葉あそび"],"summary":"「こぼす」という言い回しを使い、こぼしても減らないものは愚痴、と導く逆説型の定番なぞなぞ。","illustration_scene":"朝日が差し込む台所のテーブル。倒れたコップから水がこぼれ、そばの袋からお米がこぼれ落ちている。その上に大きな「?」が浮かぶ。人物は描かない。"}',
        '類型: 逆説・言い回し(定番なぞなぞ・作者不詳の流布問題)。流布例: https://www.nazo2.net/tyuukyuu/011.html , https://nazoq.com/normal/Q003772.html 。文面はオリジナルに書き下ろし(表現は書き直し済み)。', 1);

-- A16
INSERT INTO quiz_stock_items (set_id, content_key, quiz_type, difficulty, question_text, answer_text, content_fields, source_note, is_active)
VALUES ((SELECT id FROM batch_sets WHERE set_code = 'logic-training-1'),
        (SELECT CONCAT('morning-', LPAD(COALESCE(MAX(CAST(SUBSTRING_INDEX(t.content_key, '-', -1) AS UNSIGNED)), 0) + 1, 3, '0')) FROM (SELECT q.content_key FROM quiz_stock_items q JOIN batch_sets b ON b.id = q.set_id WHERE b.set_code = 'logic-training-1' AND q.content_key LIKE 'morning-%') t),
        'L1', 'light',
        'さかさまにすると、とたんに体重が軽くなってしまう生き物がいる。それはなんだ?',
        'イルカ(逆から読むと「かるい」)',
        '{"hook":"言葉のマジックを見せよう","hint":"読む向きを変えてみろ!","question":"さかさまにすると、とたんに体重が軽くなってしまう生き物がいる。それはなんだ?","answer":"イルカ(逆から読むと「かるい」)","explanation":"「イルカ」を逆から読むと「かるい」。さかさまにするのは体ではなく、名前の読み方だった。","coach_comment":"逆から読む発想、いいぞ!","tags":["なぞなぞ","朝の一問","言葉あそび"],"summary":"イルカを逆から読むと「かるい」になる、逆さ読みの定番なぞなぞ。","illustration_scene":"朝日がのぼる海辺の砂浜。大きな体重計の上で、人が逆立ちをして両手で乗っている(後ろ姿・顔は描かない)。その上に大きな「?」が浮かぶ。イルカや魚など海の生き物は描かない。"}',
        '類型: 逆さ読み(定番なぞなぞ・作者不詳の流布問題)。流布例: https://nazoq.com/easy/Q000494.html , https://kabu-elife.sakura.ne.jp/inc/nazonazo/cat3/020.html 。文面はオリジナルに書き下ろし(表現は書き直し済み)。', 1);

-- A17
INSERT INTO quiz_stock_items (set_id, content_key, quiz_type, difficulty, question_text, answer_text, content_fields, source_note, is_active)
VALUES ((SELECT id FROM batch_sets WHERE set_code = 'logic-training-1'),
        (SELECT CONCAT('morning-', LPAD(COALESCE(MAX(CAST(SUBSTRING_INDEX(t.content_key, '-', -1) AS UNSIGNED)), 0) + 1, 3, '0')) FROM (SELECT q.content_key FROM quiz_stock_items q JOIN batch_sets b ON b.id = q.set_id WHERE b.set_code = 'logic-training-1' AND q.content_key LIKE 'morning-%') t),
        'L1', 'light',
        '目を開けているときには絶対に見えないのに、目を閉じるとはっきり見えてくるものは、なんだ?',
        '夢',
        '{"hook":"朝いちばんに聞きたい一問","hint":"さっきまで見ていたはずだ!","question":"目を開けているときには絶対に見えないのに、目を閉じるとはっきり見えてくるものは、なんだ?","answer":"夢","explanation":"答えは夢。まぶたを閉じた世界だけに映る映像だ。目を開けた瞬間に消えてしまうのも夢らしい。","coach_comment":"今朝はどんな夢を見た?","tags":["なぞなぞ","朝の一問","頭の体操"],"summary":"目を開けると見えず、目を閉じると見えるものは夢、という逆説型の定番なぞなぞ。","illustration_scene":"朝の視力検査の場面。人が椅子に座り、両目をぎゅっと閉じたまま、迷いなく前方の視力検査表を指さして自信に満ちた様子でいる。正面には黒いランドルト環(C字の輪)が並ぶ白い視力検査表が立つ。表の上に大きな「?」が浮かぶ。数字や文字は描かない。"}',
        '類型: 逆説(定番なぞなぞ・作者不詳の流布問題)。流布例: https://nazoq.com/normal/Q000576.html , https://nazo-nazo.net/level1/345/ 。文面はオリジナルに書き下ろし(表現は書き直し済み)。', 1);

-- A18
INSERT INTO quiz_stock_items (set_id, content_key, quiz_type, difficulty, question_text, answer_text, content_fields, source_note, is_active)
VALUES ((SELECT id FROM batch_sets WHERE set_code = 'logic-training-1'),
        (SELECT CONCAT('morning-', LPAD(COALESCE(MAX(CAST(SUBSTRING_INDEX(t.content_key, '-', -1) AS UNSIGNED)), 0) + 1, 3, '0')) FROM (SELECT q.content_key FROM quiz_stock_items q JOIN batch_sets b ON b.id = q.set_id WHERE b.set_code = 'logic-training-1' AND q.content_key LIKE 'morning-%') t),
        'L1', 'light',
        '1週間のうち、たった2日しか使えない楽器がある。それはなんだ?',
        '木琴(もっきん=木・金)',
        '{"hook":"世界に楽器は数あれど…","hint":"曜日を口に出してみろ!","question":"1週間のうち、たった2日しか使えない楽器がある。それはなんだ?","answer":"木琴(もっきん=木・金)","explanation":"木琴は「もっきん」。木曜と金曜の2日を並べた音になる。もちろん実物は毎日使える。","coach_comment":"音の並べ替え、お見事だ!","tags":["なぞなぞ","朝の一問","ダジャレ"],"summary":"木琴(もっきん)を木曜・金曜と読み替える、曜日ダジャレの定番なぞなぞ。","illustration_scene":"朝日が差し込む学校の音楽室。ピアノ・トランペット・たいこ・リコーダーが並び、その中央に大きな「?」が浮かぶ。木琴と鉄琴、カレンダーは描かない。人物は描かない。"}',
        '類型: 曜日ダジャレ(定番なぞなぞ・作者不詳の流布問題)。流布例: https://nazoq.com/hardest/Q000625.html , https://quiz.community.fmworld.net/nazonazo/content/23/answer3.html 。文面はオリジナルに書き下ろし(表現は書き直し済み)。', 1);

-- A19
INSERT INTO quiz_stock_items (set_id, content_key, quiz_type, difficulty, question_text, answer_text, content_fields, source_note, is_active)
VALUES ((SELECT id FROM batch_sets WHERE set_code = 'logic-training-1'),
        (SELECT CONCAT('morning-', LPAD(COALESCE(MAX(CAST(SUBSTRING_INDEX(t.content_key, '-', -1) AS UNSIGNED)), 0) + 1, 3, '0')) FROM (SELECT q.content_key FROM quiz_stock_items q JOIN batch_sets b ON b.id = q.set_id WHERE b.set_code = 'logic-training-1' AND q.content_key LIKE 'morning-%') t),
        'L1', 'light',
        '朝から鉄板の前に立ちつづける、たい焼き屋の店主。さて、この人の今の気持ちは?',
        'やきたい(焼きたい)',
        '{"hook":"朝から仕込みご苦労さん!","hint":"売り物の名前を入れかえろ!","question":"朝から鉄板の前に立ちつづける、たい焼き屋の店主。さて、この人の今の気持ちは?","answer":"やきたい(焼きたい)","explanation":"店主の気持ちは「やきたい」。売り物の「たいやき」を並べかえただけで、そのまま本音になる。","coach_comment":"並べかえの一発、見事だ!","tags":["なぞなぞ","朝の一問","文字あそび"],"summary":"たい焼き屋の店主の気持ちを問い、「たいやき」の並べかえ「やきたい」を導くアナグラム型のオリジナルなぞなぞ。","illustration_scene":"朝の商店街のたい焼き屋の屋台。鉄板の前に立つ店主が、焼きあがったたい焼きを並べている。店主の頭部は大きな「?」で覆われ、表情は見えない。のれんや看板に文字は描かない。"}',
        '類型: アナグラム(オリジナル書き下ろし・2026-08-19)。自作問題のため出典URLはなし。アイデア・文面とも書き下ろし。', 1);

-- A20
INSERT INTO quiz_stock_items (set_id, content_key, quiz_type, difficulty, question_text, answer_text, content_fields, source_note, is_active)
VALUES ((SELECT id FROM batch_sets WHERE set_code = 'logic-training-1'),
        (SELECT CONCAT('morning-', LPAD(COALESCE(MAX(CAST(SUBSTRING_INDEX(t.content_key, '-', -1) AS UNSIGNED)), 0) + 1, 3, '0')) FROM (SELECT q.content_key FROM quiz_stock_items q JOIN batch_sets b ON b.id = q.set_id WHERE b.set_code = 'logic-training-1' AND q.content_key LIKE 'morning-%') t),
        'L1', 'light',
        '細かくすればするほど、なぜか重たくなっていくものがある。それはなんだ?',
        'お金(紙幣を小銭にすると重い)',
        '{"hook":"常識が逆さまになる一問だ","hint":"小さくすると数が増えるぞ!","question":"細かくすればするほど、なぜか重たくなっていくものがある。それはなんだ?","answer":"お金(紙幣を小銭にすると重い)","explanation":"答えはお金。1万円札を1円玉に両替すると、同じ金額なのにずっしり重くなる。細かくするほど重さが増す。","coach_comment":"重さで損した気になるよな!","tags":["なぞなぞ","朝の一問","頭の体操"],"summary":"紙幣を小銭に両替すると重くなることを使い、細かくすると重くなるものを問うなぞなぞ。","illustration_scene":"朝日が差し込む部屋の机。細かくちぎった紙くず、砕いた氷、粉になった砂糖が小皿に分けて置かれている。その上に大きな「?」が浮かぶ。お金・硬貨・財布は描かない。人物は描かない。"}',
        '類型: 視点の切り替え(なぞなぞサイト掲載の流布問題)。出典: https://quiz-oukoku.jp/nazonazo-quz-adult/ 。アイデア・解法構造のみ借用し、文面はオリジナルに書き下ろし(表現は書き直し済み)。', 1);

-- A21
INSERT INTO quiz_stock_items (set_id, content_key, quiz_type, difficulty, question_text, answer_text, content_fields, source_note, is_active)
VALUES ((SELECT id FROM batch_sets WHERE set_code = 'logic-training-1'),
        (SELECT CONCAT('morning-', LPAD(COALESCE(MAX(CAST(SUBSTRING_INDEX(t.content_key, '-', -1) AS UNSIGNED)), 0) + 1, 3, '0')) FROM (SELECT q.content_key FROM quiz_stock_items q JOIN batch_sets b ON b.id = q.set_id WHERE b.set_code = 'logic-training-1' AND q.content_key LIKE 'morning-%') t),
        'L1', 'light',
        '水の中を泳いでいることもあれば、空を飛んでいることもある。同じ名前で呼ばれるそれは、なんだ?',
        'タコ(海の蛸と空の凧)',
        '{"hook":"正体はひとつじゃないぞ!","hint":"片方は生き物じゃない!","question":"水の中を泳いでいることもあれば、空を飛んでいることもある。同じ名前で呼ばれるそれは、なんだ?","answer":"タコ(海の蛸と空の凧)","explanation":"答えはタコ。海を泳ぐ蛸と、空にあげる凧。読みは同じでも、まったく別のものだ。","coach_comment":"ひとつの音に二つの正体!","tags":["なぞなぞ","朝の一問","言葉あそび"],"summary":"海の蛸と空の凧が同じ読みであることを使い、泳ぎも飛びもするものを問うなぞなぞ。","illustration_scene":"朝の砂浜。2人が後ろ姿で並んで立ち(顔は描かない)、1人は海を指さし、もう1人は空を指さしている。海面にも空にも何もいない。2人の間に大きな「?」が浮かぶ。タコ・凧・魚・鳥は描かない。"}',
        '類型: 同音異義(なぞなぞサイト掲載の流布問題)。出典: https://quiz-oukoku.jp/nazonazo-quz-adult/ 。アイデア・解法構造のみ借用し、文面はオリジナルに書き下ろし(表現は書き直し済み)。', 1);

-- B15
INSERT INTO quiz_stock_items (set_id, content_key, quiz_type, difficulty, question_text, answer_text, content_fields, source_note, is_active)
VALUES ((SELECT id FROM batch_sets WHERE set_code = 'logic-training-1'),
        (SELECT CONCAT('noon-', LPAD(COALESCE(MAX(CAST(SUBSTRING_INDEX(t.content_key, '-', -1) AS UNSIGNED)), 0) + 1, 3, '0')) FROM (SELECT q.content_key FROM quiz_stock_items q JOIN batch_sets b ON b.id = q.set_id WHERE b.set_code = 'logic-training-1' AND q.content_key LIKE 'noon-%') t),
        'L3', 'standard',
        '日本全国に立っている電柱は、およそ何本あるだろう?電力用と通信用を合わせた数で考えよう。',
        '約3600万本(目安)',
        '{"hook":"毎年まだ増えてるらしいぞ!","hint":"電線をたどってみろ!","question":"日本全国に立っている電柱は、およそ何本あるだろう?電力用と通信用を合わせた数で考えよう。","answer":"約3600万本(目安)","explanation":"①前提: 電力柱・電信柱・共用柱をまとめて1本と数える。②ベース: 電柱は道路沿いに立つので「道路の長さ÷立っている密度」で数える。③分解: 人が暮らす地域の道路の総延長を約120万kmと仮定。さらに道路100mあたり約3本立っていると仮定する。④計算: 120万km=12億m。12億m÷100m×3本≒3600万本。⑤実勢チェック: 実際も約3600万本とされ、桁がぴたりと合う。","coach_comment":"街の景色を数で見られたな!","tags":["フェルミ推定","数字感覚","昼の一問"],"summary":"日本の電柱の本数を、居住地の道路総延長と100mあたりの設置本数から推定する問題。実勢は約3600万本。","illustration_scene":"昼下がりの住宅街の道路。手前から奥へ電柱がずらりと並び、電線が空に何本も伸びている。道の先まで電柱が続いて見える。青空に大きな「?」が浮かぶ。文字や数字は描かない。人物は描かない。"}',
        '類型: フェルミ推定(自作問題)。実勢値の出典: 国土交通省「電柱本数の推移」 https://www.mlit.go.jp/road/road/traffic/chicyuka/chi_13_03.html , 日本経済新聞 https://www.nikkei.com/article/DGXZQOUD226S70S2A720C2000000/ (約3600万本)。問題文・解説はオリジナルに書き下ろし(表現は書き直し済み)。', 1);

-- B16
INSERT INTO quiz_stock_items (set_id, content_key, quiz_type, difficulty, question_text, answer_text, content_fields, source_note, is_active)
VALUES ((SELECT id FROM batch_sets WHERE set_code = 'logic-training-1'),
        (SELECT CONCAT('noon-', LPAD(COALESCE(MAX(CAST(SUBSTRING_INDEX(t.content_key, '-', -1) AS UNSIGNED)), 0) + 1, 3, '0')) FROM (SELECT q.content_key FROM quiz_stock_items q JOIN batch_sets b ON b.id = q.set_id WHERE b.set_code = 'logic-training-1' AND q.content_key LIKE 'noon-%') t),
        'L3', 'standard',
        '日本全国の街角に立っている赤い郵便ポストは、およそ何本あるだろう?',
        '約19万本(目安)',
        '{"hook":"赤いあいつ、何本ある?","hint":"郵便局を思いうかべろ!","question":"日本全国の街角に立っている赤い郵便ポストは、およそ何本あるだろう?","answer":"約19万本(目安)","explanation":"①前提: 街角の郵便差出箱を1本と数える(郵便局の前のものも含む)。②ベース: ポストは郵便局の受け持ち区域に散らばるので「郵便局の数×1局あたりのポスト数」で数える。③分解: 全国の郵便局は約2万4千局。人が住める土地は約12万km²なので、1局の受け持ちは約5km²。ポストは出す人の徒歩圏に要るので一辺800mの四角に1本と仮定すると、1局に約8本。④計算: 2万4千局×8本≒19万本。⑤実勢チェック: 実際は17万5千本(2023年3月末)とされ、近い数になる。","coach_comment":"身近な赤に目をつけたな!","tags":["フェルミ推定","数字感覚","昼の一問"],"summary":"郵便ポストの本数を、郵便局数と1局あたりの受け持ち面積・徒歩圏の広さから推定する問題。実勢は約17万5千本。","illustration_scene":"昼の商店街の歩道。赤い郵便ポストが手前に大きく立ち、その奥の通りにも同じ赤いポストがいくつも並んで見える。空に大きな「?」が浮かぶ。文字や数字は描かない。人物は描かない。"}',
        '類型: フェルミ推定(自作問題)。実勢値の出典: 総務省「郵便差出箱(郵便ポスト)の現状」(日本郵便株式会社資料) https://www.soumu.go.jp/main_content/000893688.pdf (17万5145本・2023年3月末)。郵便局数の出典: 総務省「令和7年版 情報通信白書」 https://www.soumu.go.jp/johotsusintokei/whitepaper/ja/r07/html/nd21c120.html (2万4185局・2024年度末)。可住地面積の出典: 総務省統計局 統計FAQ https://www.stat.go.jp/library/faq/faq01/faq01a03.html (約12.3万km²)。問題文・解説はオリジナルに書き下ろし(表現は書き直し済み)。', 1);

-- B17
INSERT INTO quiz_stock_items (set_id, content_key, quiz_type, difficulty, question_text, answer_text, content_fields, source_note, is_active)
VALUES ((SELECT id FROM batch_sets WHERE set_code = 'logic-training-1'),
        (SELECT CONCAT('noon-', LPAD(COALESCE(MAX(CAST(SUBSTRING_INDEX(t.content_key, '-', -1) AS UNSIGNED)), 0) + 1, 3, '0')) FROM (SELECT q.content_key FROM quiz_stock_items q JOIN batch_sets b ON b.id = q.set_id WHERE b.set_code = 'logic-training-1' AND q.content_key LIKE 'noon-%') t),
        'L3', 'standard',
        '日本全国にある歯医者さん(歯科診療所)は、およそ何軒あるだろう?',
        '約6万軒(目安)',
        '{"hook":"痛くなってから探すよな!","hint":"歯科医師の数から攻めろ!","question":"日本全国にある歯医者さん(歯科診療所)は、およそ何軒あるだろう?","answer":"約6万軒(目安)","explanation":"①前提: 歯科診療所の施設数を数える。②ベース: 「診療所で働く歯科医師の数÷1軒あたりの人数」で数える。③分解: 国家試験には毎年約2400人が受かる。働く期間を40年と仮定すると2400人×40年で歯科医師は約10万人。大学病院や総合病院に勤める人を1割ほどと見ると、診療所で働くのは約9万人。1軒は院長に勤務医が時々つく形なので平均1.5人と仮定。④計算: 9万人÷1.5人≒6万軒。⑤実勢チェック: 実際は66,818軒(2023年)。コンビニ(約5万6千店)より多い。","coach_comment":"定期検診、行ってるか?","tags":["フェルミ推定","数字感覚","昼の一問"],"summary":"歯科診療所の数を、診療所で働く歯科医師の数(国家試験合格者×就業年数から算出)と1軒あたりの人数で推定する問題。実勢は約6万7千軒。","illustration_scene":"昼の街並み。通り沿いのビルに歯のマークの看板を出した診療所がいくつも並び、奥の通りにも同じ看板が続いて見える。空に大きな「?」が浮かぶ。看板に文字や数字は描かない。人物は描かない。"}',
        '類型: フェルミ推定(自作問題)。実勢値の出典: 厚生労働省「令和5年医療施設(静態・動態)調査」の歯科診療所数 66,818施設(2023年10月1日現在)。要約記事: https://www.fp-soken.or.jp/fpnews/medical-fpnews/no349-2/ 。歯科医師数・国家試験合格者数の出典: 厚生労働省「歯科医師の需給問題に関するワーキンググループ 参考資料」 https://www.mhlw.go.jp/file/05-Shingikai-10801000-Iseikyoku-Soumuka/0000087739.pdf (歯科医師 約10万7千人・合格者 約2400人/年)。問題文・解説はオリジナルに書き下ろし(表現は書き直し済み)。', 1);

-- B18
INSERT INTO quiz_stock_items (set_id, content_key, quiz_type, difficulty, question_text, answer_text, content_fields, source_note, is_active)
VALUES ((SELECT id FROM batch_sets WHERE set_code = 'logic-training-1'),
        (SELECT CONCAT('noon-', LPAD(COALESCE(MAX(CAST(SUBSTRING_INDEX(t.content_key, '-', -1) AS UNSIGNED)), 0) + 1, 3, '0')) FROM (SELECT q.content_key FROM quiz_stock_items q JOIN batch_sets b ON b.id = q.set_id WHERE b.set_code = 'logic-training-1' AND q.content_key LIKE 'noon-%') t),
        'L3', 'standard',
        '日本全国の道路にかかっている橋は、およそ何本あるだろう?小さな橋も1本として数える。',
        '約70万橋(目安)',
        '{"hook":"毎日わたっても気づかない","hint":"川の長さから攻めろ!","question":"日本全国の道路にかかっている橋は、およそ何本あるだろう?小さな橋も1本として数える。","answer":"約70万橋(目安)","explanation":"①前提: 長さ2m以上の道路橋を1橋と数える。②ベース: 橋は川と道路が交わる所にできるので「川の総延長×川1kmあたりに道路と交わる回数」で数える。③分解: 全国の川の総延長は約14万km。道路は網の目状に走っており、山あいも含めた平均の間隔を200mと仮定すると、川は1km進むごとに約5回道路と交わる。④計算: 14万km×5回≒70万橋。⑤実勢チェック: 実際は約73万橋とされ、ほぼ一致する。","coach_comment":"足元のインフラ、見直したな!","tags":["フェルミ推定","数字感覚","昼の一問"],"summary":"道路橋の数を、全国の川の総延長と、川1kmあたりに道路と交わる回数から推定する問題。実勢は約73万橋。","illustration_scene":"昼の川沿いの風景。手前に道路の橋がかかり、その奥にも小さな橋がいくつも連なって見える。青空に大きな「?」が浮かぶ。文字や数字は描かない。人物は描かない。"}',
        '類型: フェルミ推定(自作問題)。実勢値の出典: 国土交通省「道路施策の展開」(道路統計) https://www.mlit.go.jp/road/toukei_chousa/road_db/pdf/2025/14-1-1.pdf (道路橋 約73万橋)。河川総延長の出典: 総務省統計局 統計FAQ https://www.stat.go.jp/library/faq/faq01/faq01a08.html (一級・二級・準用河川の合計 144,046km)。問題文・解説はオリジナルに書き下ろし(表現は書き直し済み)。', 1);

-- B20
INSERT INTO quiz_stock_items (set_id, content_key, quiz_type, difficulty, question_text, answer_text, content_fields, source_note, is_active)
VALUES ((SELECT id FROM batch_sets WHERE set_code = 'logic-training-1'),
        (SELECT CONCAT('noon-', LPAD(COALESCE(MAX(CAST(SUBSTRING_INDEX(t.content_key, '-', -1) AS UNSIGNED)), 0) + 1, 3, '0')) FROM (SELECT q.content_key FROM quiz_stock_items q JOIN batch_sets b ON b.id = q.set_id WHERE b.set_code = 'logic-training-1' AND q.content_key LIKE 'noon-%') t),
        'L3', 'standard',
        '日本全国の道路にある信号機は、およそ何基あるだろう?信号のある交差点を1基と数える。',
        '約21万基(目安)',
        '{"hook":"青は本当は緑らしいぞ!","hint":"市街地の広さで割り出せ!","question":"日本全国の道路にある信号機は、およそ何基あるだろう?信号のある交差点を1基と数える。","answer":"約21万基(目安)","explanation":"①前提: 信号機のある交差点を1基と数える。②ベース: 信号は市街地の交差点に置かれるので「市街地の面積×面積あたりの交差点の数」で数える。③分解: 人が集まって暮らす市街地を国土の約5%(約1.9万km²)と仮定。市街地では約300m四方に1つ信号のある交差点があると仮定する(1km²あたり約11基)。④計算: 1.9万km²×11基≒21万基。⑤実勢チェック: 実際は約21万基(2024年3月末)とされ、ほぼ一致する。","coach_comment":"渡るときに思い出してくれ!","tags":["フェルミ推定","数字感覚","昼の一問"],"summary":"信号機の数を、市街地の面積と信号のある交差点の間隔から推定する問題。実勢は約21万基(2024年3月末)。","illustration_scene":"昼の交差点を少し高い位置から見た風景。手前の交差点にも、その先の通りの交差点にも信号機が立ち並んで見える。空に大きな「?」が浮かぶ。文字や数字は描かない。人物は描かない。"}',
        '類型: フェルミ推定(自作問題)。実勢値の出典: 警察庁「都道府県別交通信号機等ストック数」に基づく集計(2024年3月末で約21万基)。流布例: https://ja.wikipedia.org/wiki/日本の交通信号機 , https://mc-web.jp/life/column/97929/ 。問題文・解説はオリジナルに書き下ろし(表現は書き直し済み)。', 1);

-- B19
INSERT INTO quiz_stock_items (set_id, content_key, quiz_type, difficulty, question_text, answer_text, content_fields, source_note, is_active)
VALUES ((SELECT id FROM batch_sets WHERE set_code = 'logic-training-1'),
        (SELECT CONCAT('noon-', LPAD(COALESCE(MAX(CAST(SUBSTRING_INDEX(t.content_key, '-', -1) AS UNSIGNED)), 0) + 1, 3, '0')) FROM (SELECT q.content_key FROM quiz_stock_items q JOIN batch_sets b ON b.id = q.set_id WHERE b.set_code = 'logic-training-1' AND q.content_key LIKE 'noon-%') t),
        'L3', 'standard',
        '日本で育てられている肉用のニワトリは、今このときおよそ何羽いるだろう?',
        '約1億3千万羽(目安)',
        '{"hook":"今日、鶏肉を食べたか?","hint":"食べる量から逆算しろ!","question":"日本で育てられている肉用のニワトリは、今このときおよそ何羽いるだろう?","answer":"約1億3千万羽(目安)","explanation":"①前提: ある時点で飼われる肉用鶏の数。②ベース: 年間の出荷羽数を、鶏舎が1年に入れ替わる回数で割る。③分解: 1人が年に食べる鶏肉(身)を約14kg、1羽から取れる身を約1.7kgと仮定。自給率は約3分の2。鶏舎は50日で出荷し掃除を挟み70日で1回転と仮定。④計算: 1.2億人×14kg÷1.7kg≒年10億羽。国産は約6.6億羽。365日÷70日で年に約5回入れ替わるので、6.6億羽÷5≒1億3千万羽。⑤実勢チェック: 実際は約1億4千万羽(令和4年)。人より多い。","coach_comment":"食卓の裏側が見えたな!","tags":["フェルミ推定","数字感覚","昼の一問"],"summary":"肉用鶏の飼養羽数を、鶏肉の年間消費量・1羽から取れる肉の量・自給率・鶏舎の回転日数から推定する問題。実勢は約1億4千万羽。","illustration_scene":"昼の明るい養鶏場。白いニワトリが数えきれないほど群れている広い鶏舎が、奥までずっと続いている。空に大きな「?」が浮かぶ。文字や数字は描かない。人物は描かない。"}',
        '類型: フェルミ推定(自作問題)。実勢値の出典: 農林水産省「畜産統計(令和4年2月1日現在)」 https://www.maff.go.jp/j/tokei/kekka_gaiyou/tiku_toukei/r4/ (ブロイラー飼養羽数 1億3923万羽), 同「鶏(ブロイラー)の飼養戸数・羽数の推移」 https://www.maff.go.jp/j/chikusan/kikaku/tikusan_sogo/attach/pdf/tori-5.pdf 。鶏肉自給率の出典: 農林水産省「その2: お肉の自給率」 https://www.maff.go.jp/j/zyukyu/zikyu_ritu/ohanasi01/01-04.html (重量ベース約64%)。問題文・解説はオリジナルに書き下ろし(表現は書き直し済み)。', 1);

-- B21
INSERT INTO quiz_stock_items (set_id, content_key, quiz_type, difficulty, question_text, answer_text, content_fields, source_note, is_active)
VALUES ((SELECT id FROM batch_sets WHERE set_code = 'logic-training-1'),
        (SELECT CONCAT('noon-', LPAD(COALESCE(MAX(CAST(SUBSTRING_INDEX(t.content_key, '-', -1) AS UNSIGNED)), 0) + 1, 3, '0')) FROM (SELECT q.content_key FROM quiz_stock_items q JOIN batch_sets b ON b.id = q.set_id WHERE b.set_code = 'logic-training-1' AND q.content_key LIKE 'noon-%') t),
        'L3', 'standard',
        '日本全国の道路にあるトンネルは、およそ何か所あるだろう?鉄道のトンネルは数えない。',
        '約1万3千か所(目安)',
        '{"hook":"山だらけの国ならではだ!","hint":"山の多さがカギだ!","question":"日本全国の道路にあるトンネルは、およそ何か所あるだろう?鉄道のトンネルは数えない。","answer":"約1万3千か所(目安)","explanation":"①前提: 道路トンネルを1か所と数える。②ベース: 「山あいを走る道路の長さ÷トンネルが要る間隔」で数える。③分解: 国土37.8万km²×0.7で山地は約26万km²。山道は谷沿いに通り、谷は約4kmおきにあると仮定すると、山あいの道路は26万÷4≒6.5万km。山道は約5kmに1本トンネルが要ると仮定。④計算: 6.5万km÷5km≒1万3千か所。⑤実勢チェック: 実際は約1.2万か所とされ、ほぼ一致する。","coach_comment":"地形から攻めたな、見事!","tags":["フェルミ推定","数字感覚","昼の一問"],"summary":"道路トンネルの数を、山地の面積から求めた山あいの道路の長さと、トンネルが要る間隔から推定する問題。実勢は約1.2万か所。","illustration_scene":"昼の山あいの道路。手前にトンネルの入り口が大きく口を開け、その奥の山にも別のトンネルの入り口がいくつか見える。青空に大きな「?」が浮かぶ。文字や数字は描かない。人物は描かない。"}',
        '類型: フェルミ推定(自作問題)。実勢値の出典: 国土交通省「道路施策の展開」(道路統計) https://www.mlit.go.jp/road/toukei_chousa/road_db/pdf/2025/14-1-1.pdf (道路トンネル 約1.2万箇所)。問題文・解説はオリジナルに書き下ろし(表現は書き直し済み)。', 1);

-- C15
INSERT INTO quiz_stock_items (set_id, content_key, quiz_type, difficulty, question_text, answer_text, content_fields, source_note, is_active)
VALUES ((SELECT id FROM batch_sets WHERE set_code = 'logic-training-1'),
        (SELECT CONCAT('night-', LPAD(COALESCE(MAX(CAST(SUBSTRING_INDEX(t.content_key, '-', -1) AS UNSIGNED)), 0) + 1, 3, '0')) FROM (SELECT q.content_key FROM quiz_stock_items q JOIN batch_sets b ON b.id = q.set_id WHERE b.set_code = 'logic-training-1' AND q.content_key LIKE 'night-%') t),
        'L1', 'deep',
        '砂漠の父が17頭のラクダを残した。遺言は「長男に2分の1、次男に3分の1、三男に9分の1を」。1頭も切らずに分けるには?',
        'ラクダを1頭借りて18頭で分ける',
        '{"hook":"ラクダのコブは脂肪らしいぞ!","hint":"17のままでは分けられないぞ!","question":"砂漠の父が17頭のラクダを残した。遺言は「長男に2分の1、次男に3分の1、三男に9分の1を」。1頭も切らずに分けるには?","answer":"ラクダを1頭借りて18頭で分ける","explanation":"1頭借りて18頭にすると長男9頭・次男6頭・三男2頭で分けられ、合計17頭。借りた1頭はそのまま返せる。3つの分は足しても1にならないのがミソ。","coach_comment":"借りて返す、粋なやり方だ!","tags":["とんち","夜の一問","名作パズル"],"summary":"17頭のラクダを2分の1・3分の1・9分の1で分ける遺言を、1頭借りて18頭にして解く古典の分配パズル。借りた1頭は最後に返る。","illustration_scene":"夜の砂漠。満天の星空と月明かりの下、テントのそばにラクダの群れが静かに座っている。ラクダたちの上に大きな「?」が浮かぶ。ラクダは群れとして重なって見えるように描き、頭数を数えられる構図にはしない。人物は描かない。文字や数字は描かない。"}',
        '類型: 古典の分配パズル(17頭のラクダ。中東の民話由来・作者不詳の流布問題)。流布例: https://note.com/41semicolon/n/n0015da90e581 , https://diamond.jp/articles/-/342620?page=2 , https://sist8.com/17c 。文面はオリジナルに書き下ろし(表現は書き直し済み)。', 1);

-- C16
INSERT INTO quiz_stock_items (set_id, content_key, quiz_type, difficulty, question_text, answer_text, content_fields, source_note, is_active)
VALUES ((SELECT id FROM batch_sets WHERE set_code = 'logic-training-1'),
        (SELECT CONCAT('night-', LPAD(COALESCE(MAX(CAST(SUBSTRING_INDEX(t.content_key, '-', -1) AS UNSIGNED)), 0) + 1, 3, '0')) FROM (SELECT q.content_key FROM quiz_stock_items q JOIN batch_sets b ON b.id = q.set_id WHERE b.set_code = 'logic-training-1' AND q.content_key LIKE 'night-%') t),
        'L1', 'deep',
        '分かれ道に番人が2人。一方は必ず本当を、もう一方は必ずうそを言うが、どちらがどちらか分からない。1回だけ質問して正しい道を知るには?',
        '「もう一人はどっちと言う?」と聞き、逆へ進む',
        '{"hook":"うそつきも役に立つらしいぞ!","hint":"2人まとめて使う手はないか?","question":"分かれ道に番人が2人。一方は必ず本当を、もう一方は必ずうそを言うが、どちらがどちらか分からない。1回だけ質問して正しい道を知るには?","answer":"「もう一人はどっちと言う?」と聞き、逆へ進む","explanation":"正直者に聞けば、うそつきが答える「まちがった道」をそのまま伝える。うそつきに聞けば、正直者の正しい答えを逆にして、やはりまちがった道。だから逆が正解。","coach_comment":"うそを味方につけたな!","tags":["水平思考","夜の一問","名作パズル"],"summary":"正直者とうそつきの番人に1回だけ質問して正しい道を見抜く古典の論理パズル。「もう一人は何と言うか」を聞き、返答の逆へ進む。","illustration_scene":"夜の分かれ道。松明の灯りに照らされて、二股に分かれた道の前に2つの人影が並んで立っている(後ろ姿・顔は描かない)。道の上に大きな「?」が浮かぶ。どちらかの道だけを明るく描いたり、安全そうに見せる描き分けはしない。文字や数字は描かない。"}',
        '類型: 論理の古典パズル(正直者とうそつきの番人 / Knights and Knaves 型・作者不詳の流布問題)。流布例: https://diamond.jp/articles/-/345844 , https://shiraberu.net/quiz/knight-knave-puzzle/ 。文面はオリジナルに書き下ろし(表現は書き直し済み。天国・地獄の宗教色は分かれ道と番人に置き換え)。', 1);

-- C17
INSERT INTO quiz_stock_items (set_id, content_key, quiz_type, difficulty, question_text, answer_text, content_fields, source_note, is_active)
VALUES ((SELECT id FROM batch_sets WHERE set_code = 'logic-training-1'),
        (SELECT CONCAT('night-', LPAD(COALESCE(MAX(CAST(SUBSTRING_INDEX(t.content_key, '-', -1) AS UNSIGNED)), 0) + 1, 3, '0')) FROM (SELECT q.content_key FROM quiz_stock_items q JOIN batch_sets b ON b.id = q.set_id WHERE b.set_code = 'logic-training-1' AND q.content_key LIKE 'night-%') t),
        'L1', 'deep',
        '「この卵をテーブルに立ててみろ」と言われ、居合わせた誰もができなかった。コロンブスはどうやって立てた?',
        '卵の底を割って平らにした',
        '{"hook":"500年語りつがれる一手だ","hint":"ルールを一度読み直せ!","question":"「この卵をテーブルに立ててみろ」と言われ、居合わせた誰もができなかった。コロンブスはどうやって立てた?","answer":"卵の底を割って平らにした","explanation":"コロンブスは卵の底を軽く割って平らにし、そのまま立てた。誰も「割るな」とは言っていない。答えを聞けば簡単でも、最初に思いつくのは難しい。","coach_comment":"前提を疑う力、それが武器だ!","tags":["とんち","夜の一問","故事"],"summary":"コロンブスの卵。禁じられていない操作(底を割る)に気づけば立つ、という発想転換の古典の故事。","illustration_scene":"夜の食堂のテーブル。ろうそくの灯りに照らされて、白いゆで卵が1つころんと横たわっている。そのまわりに大きな「?」が浮かぶ。卵は割れていない状態で描く。人物は描かない。"}',
        '類型: 故事(コロンブスの卵。史実性には異説があり「故事として流布」の扱い)。流布例: https://kotobank.jp/word/%E3%82%B3%E3%83%AD%E3%83%B3%E3%83%96%E3%82%B9%E3%81%AE%E5%8D%B5-67780 , https://en.wikipedia.org/wiki/Columbus%27s_egg 。文面はオリジナルに書き下ろし(表現は書き直し済み)。', 1);

-- C18
INSERT INTO quiz_stock_items (set_id, content_key, quiz_type, difficulty, question_text, answer_text, content_fields, source_note, is_active)
VALUES ((SELECT id FROM batch_sets WHERE set_code = 'logic-training-1'),
        (SELECT CONCAT('night-', LPAD(COALESCE(MAX(CAST(SUBSTRING_INDEX(t.content_key, '-', -1) AS UNSIGNED)), 0) + 1, 3, '0')) FROM (SELECT q.content_key FROM quiz_stock_items q JOIN batch_sets b ON b.id = q.set_id WHERE b.set_code = 'logic-training-1' AND q.content_key LIKE 'night-%') t),
        'L1', 'deep',
        '夜の吊り橋を4人で渡る。渡れるのは同時に2人まで、灯りは1つで必ず持って渡る。速さは1分・2分・5分・10分。全員渡る最短は?',
        '17分(19分ではなく、おそい2人を組ませる)',
        '{"hook":"実は近道があるらしいぞ!","hint":"おそい2人を組ませてみろ!","question":"夜の吊り橋を4人で渡る。渡れるのは同時に2人まで、灯りは1つで必ず持って渡る。速さは1分・2分・5分・10分。全員渡る最短は?","answer":"17分(19分ではなく、おそい2人を組ませる)","explanation":"1分が毎回付き添うと2+1+5+1+10=19分。ここで止まると惜しい。おそい5分と10分を一緒に渡らせれば、2+1+10+2+2=17分まで縮む。","coach_comment":"おそさをまとめたな、うまい!","tags":["水平思考","夜の一問","名作パズル"],"summary":"灯り1つ・同時2人までの吊り橋を4人が渡る最短時間を問う古典パズル。おそい2人を組ませるのが鍵で答えは17分。","illustration_scene":"夜の深い谷にかかる細い吊り橋。手前の岸に4人の人影が並んで立ち、そのうち1人がランタンを持っている(遠景の後ろ姿・顔は描かない)。橋の先は暗闇に沈んでいる。橋の上に大きな「?」が浮かぶ。文字や数字は描かない。"}',
        '類型: 水平思考の古典パズル(吊り橋と1つの灯り / Bridge and torch problem・作者不詳の流布問題)。流布例: https://inakadaisuki.com/suspension-bridge_question/ , https://note.com/marupeke296/n/n2c85e3085453 。文面はオリジナルに書き下ろし(表現は書き直し済み)。', 1);

-- C19
INSERT INTO quiz_stock_items (set_id, content_key, quiz_type, difficulty, question_text, answer_text, content_fields, source_note, is_active)
VALUES ((SELECT id FROM batch_sets WHERE set_code = 'logic-training-1'),
        (SELECT CONCAT('night-', LPAD(COALESCE(MAX(CAST(SUBSTRING_INDEX(t.content_key, '-', -1) AS UNSIGNED)), 0) + 1, 3, '0')) FROM (SELECT q.content_key FROM quiz_stock_items q JOIN batch_sets b ON b.id = q.set_id WHERE b.set_code = 'logic-training-1' AND q.content_key LIKE 'night-%') t),
        'L1', 'deep',
        '少年が言った。「ぼくはおととい12歳だった。でも来年には15歳になるんだ」。うそはついていない。今日は何月何日?',
        '1月1日(誕生日は12月31日)',
        '{"hook":"言ってることが合わないぞ?","hint":"きのう、何かなかったか?","question":"少年が言った。「ぼくはおととい12歳だった。でも来年には15歳になるんだ」。うそはついていない。今日は何月何日?","answer":"1月1日(誕生日は12月31日)","explanation":"誕生日が12月31日なら、おととい(12月30日)は12歳。きのう13歳になり、今日は1月1日。今年の大みそかに14歳、その次の大みそか=来年に15歳になる。","coach_comment":"日付の境目を見つけたな!","tags":["ひっかけ","夜の一問","思い込み"],"summary":"「おととい12歳・来年15歳」という矛盾に見える発言から、今日が1月1日で誕生日が12月31日と導く古典のひっかけ。","illustration_scene":"夜。窓の外に雪が舞う部屋で、テーブルに置かれた小さなケーキのろうそくが1本だけ静かにともっている。窓の外の遠くには初日の出前の暗い空が広がる。空に大きな「?」が浮かぶ。カレンダー・時計・数字・文字は描かない。人物は描かない。"}',
        '類型: 定番ひっかけ(年齢と年またぎを使う古典型・作者不詳の流布問題)。流布例: https://detail.chiebukuro.yahoo.co.jp/qa/question_detail/q1061837825 , https://sist8.com/wonday 。文面はオリジナルに書き下ろし(表現は書き直し済み)。', 1);

-- C20
INSERT INTO quiz_stock_items (set_id, content_key, quiz_type, difficulty, question_text, answer_text, content_fields, source_note, is_active)
VALUES ((SELECT id FROM batch_sets WHERE set_code = 'logic-training-1'),
        (SELECT CONCAT('night-', LPAD(COALESCE(MAX(CAST(SUBSTRING_INDEX(t.content_key, '-', -1) AS UNSIGNED)), 0) + 1, 3, '0')) FROM (SELECT q.content_key FROM quiz_stock_items q JOIN batch_sets b ON b.id = q.set_id WHERE b.set_code = 'logic-training-1' AND q.content_key LIKE 'night-%') t),
        'L1', 'deep',
        '殿様が「灰で縄を作ってみせよ」と無理を言った。灰はさらさらで、より合わせることなどできない。どうやってやりとげた?',
        '先に縄を作り、それを焼いて灰にした',
        '{"hook":"できっこないと思うだろ?","hint":"灰はどうやってできる?","question":"殿様が「灰で縄を作ってみせよ」と無理を言った。灰はさらさらで、より合わせることなどできない。どうやってやりとげた?","answer":"先に縄を作り、それを焼いて灰にした","explanation":"灰から縄は作れないが、順番を逆にすればいい。まず縄を作り、形がくずれないよう静かに焼く。すると形をたもったまま、灰でできた縄ができあがる。","coach_comment":"順番をひっくり返したな!","tags":["とんち","夜の一問","昔話"],"summary":"「灰で縄を作れ」という無理難題を、先に縄を作ってから焼くという順序の逆転で解く日本の昔話の難題。","illustration_scene":"夜の囲炉裏端。赤くおきた炭が静かに光り、天井から下がる自在鉤が影を落とす。そばの床に、作ったばかりの新しい縄が一束置かれている。縄の上に大きな「?」が浮かぶ。焼けた縄や灰になった縄は描かない。人物は描かない。文字や数字は描かない。"}',
        '類型: 日本の昔話の難題譚(灰の縄。『雑宝蔵経』「棄老因縁」に由来し『今昔物語集』などに流布した古典)。流布例: https://kotobank.jp/word/%E5%A7%A5%E6%8D%A8%E5%B1%B1%E4%BC%9D%E8%AA%AC-1508502 , https://ja.wikipedia.org/wiki/%E3%81%86%E3%81%B0%E3%81%99%E3%81%A6%E3%82%84%E3%81%BE 。文面はオリジナルに書き下ろし(表現は書き直し済み。棄老の筋は用いず、殿様の無理難題として書き起こした)。', 1);

-- C21
INSERT INTO quiz_stock_items (set_id, content_key, quiz_type, difficulty, question_text, answer_text, content_fields, source_note, is_active)
VALUES ((SELECT id FROM batch_sets WHERE set_code = 'logic-training-1'),
        (SELECT CONCAT('night-', LPAD(COALESCE(MAX(CAST(SUBSTRING_INDEX(t.content_key, '-', -1) AS UNSIGNED)), 0) + 1, 3, '0')) FROM (SELECT q.content_key FROM quiz_stock_items q JOIN batch_sets b ON b.id = q.set_id WHERE b.set_code = 'logic-training-1' AND q.content_key LIKE 'night-%') t),
        'L1', 'deep',
        '「りんご」「みかん」「両方」の3箱。ラベルは全部まちがい。1箱から1個だけ見て、全部言い当てるには?',
        '「両方」の箱から1個取る',
        '{"hook":"たった1個で全部わかるぞ","hint":"全部まちがい、を武器にしろ!","question":"「りんご」「みかん」「両方」の3箱。ラベルは全部まちがい。1箱から1個だけ見て、全部言い当てるには?","answer":"「両方」の箱から1個取る","explanation":"「両方」のラベルは必ずまちがいなので、その箱は片方だけ入っている。取り出した果物がその箱の正体だ。残り2箱もラベルが違うので、連鎖ですべて決まる。","coach_comment":"1手で全部を確定させたな!","tags":["水平思考","夜の一問","名作パズル"],"summary":"ラベルが全て誤りの3箱を1個の取り出しで確定する古典パズル。「両方」の箱から取るのが鍵。","illustration_scene":"夜の倉庫。裸電球の灯りの下に、木の箱が3つ並んでいる。それぞれに白い紙のラベルが貼られ、左からりんごの絵、みかんの絵、りんごとみかんが並んだ絵が描かれている(絵だけで文字は一切書かない)。箱の上に大きな「?」が浮かぶ。箱はふたを閉じて中身が見えないように描き、箱の外に果物は置かない。人物は描かない。数字や文字は描かない。"}',
        '類型: 古典論理パズル(誤ラベルの3箱。作者不詳の流布問題)。流布例: https://www.mathsisfun.com/puzzles/fruit-boxes-solution.html , https://en.wikipedia.org/wiki/Logic_puzzle 。文面はオリジナルに書き下ろし(表現は書き直し済み)。', 1);
