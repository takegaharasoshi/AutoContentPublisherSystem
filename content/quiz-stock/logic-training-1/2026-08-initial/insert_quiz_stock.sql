-- 16-2 問題ストック初期投入(42 問。レビュー承認後に実行)
-- 生成元: plans/16-2-stock/stock_items.py(単一ソース)。適用先: ローカル MySQL / Aurora(acps)
-- set_id は set_code から解決するため両環境共通で実行できる。

-- A01
INSERT INTO quiz_stock_items (set_id, quiz_type, difficulty, question_text, answer_text, content_fields, source_note, is_active)
VALUES ((SELECT id FROM batch_sets WHERE set_code = 'logic-training-1'), 'L1', 'light',
        'サイとラクダとカメの3匹が、そろって家電量販店にやって来た。さて、何を買いに来た?',
        'カメラ(カメ・ラクダ・サイ)',
        '{"hook":"朝イチ、動物なぞなぞ!","hint":"並び順の入れ替えがカギだ!","question":"サイとラクダとカメの3匹が、そろって家電量販店にやって来た。さて、何を買いに来た?","answer":"カメラ(カメ・ラクダ・サイ)","explanation":"3匹の順番を入れ替えて「カメ・ラクダ・サイ」と読むと「カメラください」。お店で言うセリフが隠れている。","coach_comment":"並べ替えのひらめき、見事だ!","tags":["なぞなぞ","朝の一問","ダジャレ"],"summary":"サイ・ラクダ・カメを「カメ・ラクダ・サイ」に並べ替えると「カメラください」になる定番の動物ダジャレなぞなぞ。","illustration_scene":"朝の家電量販店の入り口で、サイとラクダとカメの3匹が自動ドアから店内へ入っていく後ろ姿。売り場の明るい照明が奥に見える。"}',
        '類型: 動物名の読み合わせダジャレ(定番なぞなぞ・作者不詳の流布問題)。流布例: https://www.nazo2.net/syokyuu/048.html 。文面はオリジナルに書き下ろし(表現は書き直し済み)。', 1);

-- A02
INSERT INTO quiz_stock_items (set_id, quiz_type, difficulty, question_text, answer_text, content_fields, source_note, is_active)
VALUES ((SELECT id FROM batch_sets WHERE set_code = 'logic-training-1'), 'L1', 'light',
        '9匹の虎が乗っている乗り物ってなんだ?',
        'トラック(トラが9)',
        '{"hook":"通勤中にクスッと一問","hint":"数字も声に出して読むんだ!","question":"9匹の虎が乗っている乗り物ってなんだ?","answer":"トラック(トラが9)","explanation":"トラが9匹で「トラ・ク(9)」=トラック。数字の読み方を言葉に変える定番の言葉あそび。","coach_comment":"数字も読めば言葉になる!","tags":["なぞなぞ","朝の一問","ダジャレ"],"summary":"トラ9匹=トラ+ク(9)でトラックになる定番の数字読みダジャレなぞなぞ。","illustration_scene":"朝の動物園の入り口ゲートの前に、トラの親子が並んで歩いている風景。ゲートの奥に緑の木々が見える。"}',
        '類型: 数字読みダジャレ(定番なぞなぞ・作者不詳の流布問題)。流布例: https://kabu-elife.sakura.ne.jp/inc/nazonazo/cat4/015.html 。文面はオリジナルに書き下ろし(表現は書き直し済み)。', 1);

-- A03
INSERT INTO quiz_stock_items (set_id, quiz_type, difficulty, question_text, answer_text, content_fields, source_note, is_active)
VALUES ((SELECT id FROM batch_sets WHERE set_code = 'logic-training-1'), 'L1', 'light',
        '「世界」の真ん中にいる虫は、なんだ?',
        '蚊(せ「か」い)',
        '{"hook":"虫は世界に100万種いるらしいぞ!","hint":"言葉を文字に分解してみろ!","question":"「世界」の真ん中にいる虫は、なんだ?","answer":"蚊(せ「か」い)","explanation":"「世界」をひらがなにすると「せかい」。その真ん中の文字は「か」。世界の中心には蚊がいた、という文字なぞなぞ。","coach_comment":"視点を言葉の中に向けたな!","tags":["なぞなぞ","朝の一問","文字あそび"],"summary":"「世界(せかい)」の真ん中の文字が「か」=蚊になる定番の文字位置なぞなぞ。","illustration_scene":"宇宙から見た青く輝く地球に朝日が昇りはじめ、光の縁が金色に輝いている。地球の中心に「虫」という文字が大きく浮かび、まわりには星空が広がっている。"}',
        '類型: 文字の位置なぞなぞ(定番・作者不詳の流布問題)。流布例: https://www.nazo2.net/syokyuu/008.html 。文面はオリジナルに書き下ろし(表現は書き直し済み)。', 1);

-- A04
INSERT INTO quiz_stock_items (set_id, quiz_type, difficulty, question_text, answer_text, content_fields, source_note, is_active)
VALUES ((SELECT id FROM batch_sets WHERE set_code = 'logic-training-1'), 'L1', 'light',
        '相手を乾かせば乾かすほど、自分はどんどん濡れていくものは、なんだ?',
        'タオル',
        '{"hook":"働き者はずぶ濡れ?","hint":"お風呂上がりを思い出せ!","question":"相手を乾かせば乾かすほど、自分はどんどん濡れていくものは、なんだ?","answer":"タオル","explanation":"体や食器を拭いて乾かすたびに、水分は全部自分が引き受ける。働き者ほど濡れていく、それがタオル。","coach_comment":"逆の視点に立てた人は強い!","tags":["なぞなぞ","朝の一問","頭の体操"],"summary":"乾かす側が濡れていく逆説でタオルを当てる世界的な定番なぞなぞ。","illustration_scene":"朝の浴室のドアが半分開き、白い湯気がふわりと脱衣所へ流れ出している。曇った鏡と水滴のついた洗面台に、窓から朝日が差し込んでいる。"}',
        '類型: 逆説なぞなぞ(乾かすと濡れる。英語圏でも流布する定番)。流布例: https://quiz.community.fmworld.net/nazonazo/content/194/answer2.html 。文面はオリジナルに書き下ろし(表現は書き直し済み)。', 1);

-- A05
INSERT INTO quiz_stock_items (set_id, quiz_type, difficulty, question_text, answer_text, content_fields, source_note, is_active)
VALUES ((SELECT id FROM batch_sets WHERE set_code = 'logic-training-1'), 'L1', 'light',
        '体じゅう穴だらけなのに、水をたっぷり蓄えられるものは、なんだ?',
        'スポンジ',
        '{"hook":"穴だらけの働き者","hint":"キッチンにいる働き者だぞ!","question":"体じゅう穴だらけなのに、水をたっぷり蓄えられるものは、なんだ?","answer":"スポンジ","explanation":"穴だらけ=水が漏れそうなのに、その穴こそが水を吸い込んで蓄える仕組み。弱点に見えて武器という逆転。","coach_comment":"弱点が武器になる、いい話だ!","tags":["なぞなぞ","朝の一問","頭の体操"],"summary":"穴だらけなのに水を蓄えられる逆説でスポンジを当てる定番なぞなぞ。","illustration_scene":"朝の庭先で、穴だらけのバケツから水が何本もの細い筋になって漏れ出している。足元に小さな水たまりができ、朝日が水しぶきにきらめいている。"}',
        '類型: 逆説なぞなぞ(穴と保水。英語圏でも流布する定番)。流布例: https://nazoq.com/normal/Q000642.html 。文面はオリジナルに書き下ろし(表現は書き直し済み)。', 1);

-- A06
INSERT INTO quiz_stock_items (set_id, quiz_type, difficulty, question_text, answer_text, content_fields, source_note, is_active)
VALUES ((SELECT id FROM batch_sets WHERE set_code = 'logic-training-1'), 'L1', 'light',
        'ナイフで切っても、ハンマーでたたいても、絶対に壊れないものは、なんだ?',
        '水',
        '{"hook":"無敵の相手、現る","hint":"形がないものは強いんだ!","question":"ナイフで切っても、ハンマーでたたいても、絶対に壊れないものは、なんだ?","answer":"水","explanation":"切ってもたたいても、すぐ元どおりにつながってしまう。形を持たない水は、どんな攻撃も受け流す。","coach_comment":"柔らかいものほど強い、名言だ!","tags":["なぞなぞ","朝の一問","頭の体操"],"summary":"切ってもたたいても元に戻る水を当てる、世界のなぞなぞ集にも載る古典型。","illustration_scene":"朝日の差す河原に、ごつごつと硬そうな大きな岩がひとつ。その表面に大きな「?」が刻まれている。"}',
        '類型: 逆説なぞなぞ(切れない・割れない水。『世界なぞなぞ大事典』にも水の古典なぞが多数)。流布例: https://news.yahoo.co.jp/expert/articles/5bf182195e367d213eb8e651abdd21863ca8f9b2 。文面はオリジナルに書き下ろし(表現は書き直し済み)。', 1);

-- A07
INSERT INTO quiz_stock_items (set_id, quiz_type, difficulty, question_text, answer_text, content_fields, source_note, is_active)
VALUES ((SELECT id FROM batch_sets WHERE set_code = 'logic-training-1'), 'L1', 'light',
        'とても壊れやすくて、名前を口にした瞬間に壊れてしまうものは、なんだ?',
        '沈黙(言ったら終わり)',
        '{"hook":"こわれもの注意!","hint":"静かな場所を思い浮かべろ!","question":"とても壊れやすくて、名前を口にした瞬間に壊れてしまうものは、なんだ?","answer":"沈黙(言ったら終わり)","explanation":"「ちんもく」と声に出したら、もう沈黙ではない。答えを言うことが答えを壊す、自己矛盾のなぞなぞ。","coach_comment":"静けさの中で考えたか、渋い!","tags":["なぞなぞ","朝の一問","頭の体操"],"summary":"名前を言うと壊れる=沈黙という英語圏古典(Silence riddle)の定番なぞなぞ。","illustration_scene":"朝の光の中にシャボン玉がいくつもふわふわ浮かび、いちばん大きなひとつに「?」が映り込んでいる。"}',
        '類型: 自己言及の逆説なぞなぞ(英語圏古典 Silence riddle)。流布例: https://www.riddles.com/1175 。文面はオリジナルに書き下ろし(表現は書き直し済み)。', 1);

-- A08
INSERT INTO quiz_stock_items (set_id, quiz_type, difficulty, question_text, answer_text, content_fields, source_note, is_active)
VALUES ((SELECT id FROM batch_sets WHERE set_code = 'logic-training-1'), 'L1', 'light',
        '自分の持ち物なのに、自分よりも他人のほうがたくさん使っているものは、なんだ?',
        '自分の名前',
        '{"hook":"あなたのものなのに?","hint":"呼ばれるものを考えてみろ!","question":"自分の持ち物なのに、自分よりも他人のほうがたくさん使っているものは、なんだ?","answer":"自分の名前","explanation":"自分で自分の名前を呼ぶことはめったにない。呼ぶのはいつも周りの人。持ち主ほど使わない持ち物。","coach_comment":"身近すぎて見えない盲点だ!","tags":["なぞなぞ","朝の一問","頭の体操"],"summary":"持ち主より他人がよく使う=名前という英語圏古典の定番なぞなぞ。","illustration_scene":"朝の玄関のテーブルに通勤かばん・スマホ・腕時計・家の鍵が並び、その真ん中に大きな「?」が浮かんでいる。"}',
        '類型: 逆説なぞなぞ(英語圏古典 Name riddle)。流布例: https://www.riddles.com/1938 。文面はオリジナルに書き下ろし(表現は書き直し済み)。', 1);

-- A09
INSERT INTO quiz_stock_items (set_id, quiz_type, difficulty, question_text, answer_text, content_fields, source_note, is_active)
VALUES ((SELECT id FROM batch_sets WHERE set_code = 'logic-training-1'), 'L1', 'light',
        '毎日必ずやって来るはずなのに、待っていても永遠にたどり着かない日は、いつ?',
        '明日(来たら今日になる)',
        '{"hook":"永遠の待ちぼうけ","hint":"カレンダーの先を見てみろ!","question":"毎日必ずやって来るはずなのに、待っていても永遠にたどり着かない日は、いつ?","answer":"明日(来たら今日になる)","explanation":"明日は毎日近づいてくるのに、着いた瞬間に「今日」へ変わってしまう。だから永遠に明日のまま。","coach_comment":"時間のトリック、見破ったな!","tags":["なぞなぞ","朝の一問","頭の体操"],"summary":"来た瞬間に今日へ変わるので永遠に来ない=明日という英語圏古典(Tomorrow riddle)。","illustration_scene":"朝の玄関ポストに新聞が差さっていて、その上に大きな「?」が浮かんでいる。奥に朝焼けの住宅街。"}',
        '類型: 時間の逆説なぞなぞ(英語圏古典 Tomorrow riddle)。流布例: https://www.riddles.com/3592 。文面はオリジナルに書き下ろし(表現は書き直し済み)。', 1);

-- A10
INSERT INTO quiz_stock_items (set_id, quiz_type, difficulty, question_text, answer_text, content_fields, source_note, is_active)
VALUES ((SELECT id FROM batch_sets WHERE set_code = 'logic-training-1'), 'L1', 'light',
        '「とればとるほど」減るどころか、どんどん増えていくものは、なんだ?',
        '年(写真も正解)',
        '{"hook":"増える一方のアレ","hint":"「とる」の言い回しを探すんだ!","question":"「とればとるほど」減るどころか、どんどん増えていくものは、なんだ?","answer":"年(写真も正解)","explanation":"普通はとったら減るのに、「年を取る」は取るたび増えていく。カメラで「写真を撮る」も同じで、どちらも正解。","coach_comment":"言葉の裏をかく、いい着眼だ!","tags":["なぞなぞ","朝の一問","言葉あそび"],"summary":"「とる」のに増える=年(年を取る)・写真(撮る)という日本語の定番言い回しなぞなぞ。","illustration_scene":"朝のテーブルの上の箱ティッシュから、白いティッシュが何枚も勢いよく引き出されて宙に舞っている。そばに大きな「?」が浮かんでいる。"}',
        '類型: 言い回しなぞなぞ(「年を取る」。定番・作者不詳の流布問題)。流布例: https://ameblo.jp/nazonazo/entry-10789734339.html 。文面はオリジナルに書き下ろし(表現は書き直し済み)。', 1);

-- A11
INSERT INTO quiz_stock_items (set_id, quiz_type, difficulty, question_text, answer_text, content_fields, source_note, is_active)
VALUES ((SELECT id FROM batch_sets WHERE set_code = 'logic-training-1'), 'L1', 'light',
        '「弟」には2つあるのに、「妹」には1つしかないもの、なんだ?',
        '「と」の字',
        '{"hook":"きょうだいのヒミツ","hint":"ひらがなで書いてみるんだ!","question":"「弟」には2つあるのに、「妹」には1つしかないもの、なんだ?","answer":"「と」の字","explanation":"「弟」をひらがなにすると「おとうと」で「と」が2つ。「妹」は「いもうと」で1つ。文字を数える発想の切り替えが鍵。","coach_comment":"文字を数える頭、柔らかい!","tags":["なぞなぞ","朝の一問","文字あそび"],"summary":"弟(おとうと)に2つ・妹(いもうと)に1つ=「と」の字を数える定番の文字なぞなぞ。","illustration_scene":"朝のリビングで、男の子と女の子が積み木・ミニカー・ぬいぐるみ・ボールなどたくさんのオモチャに囲まれて遊んでいる後ろ姿。窓から朝の光が差し込んでいる。"}',
        '類型: 文字数えなぞなぞ(定番・作者不詳の流布問題)。流布例: http://nazo-nazo.com/sp/cat398/post-63.html 。文面はオリジナルに書き下ろし(表現は書き直し済み)。', 1);

-- A13
INSERT INTO quiz_stock_items (set_id, quiz_type, difficulty, question_text, answer_text, content_fields, source_note, is_active)
VALUES ((SELECT id FROM batch_sets WHERE set_code = 'logic-training-1'), 'L1', 'light',
        'どんなに全力で走っても、絶対に追い越せない相手がいる。それはだれ?',
        '自分の影',
        '{"hook":"絶対に勝てない相手","hint":"晴れた日の足元を見てみろ!","question":"どんなに全力で走っても、絶対に追い越せない相手がいる。それはだれ?","answer":"自分の影","explanation":"走れば走るほど、影もまったく同じ速さでついてくる。追いかけても永遠に追いつけない、一番身近な相手。","coach_comment":"今朝も影と一緒にダッシュだ!","tags":["なぞなぞ","朝の一問","頭の体操"],"summary":"全力で走っても追い越せない=自分の影という定番なぞなぞ。","illustration_scene":"朝の広い道で、追いかけて走る人の後ろ姿の前方を、カメ・ウサギ・チーター・馬・自転車・バイク・車・電車など様々なものが一斉に走っていくにぎやかなレースの風景。地面に影は描かない。"}',
        '類型: 逆説なぞなぞ(追いつけない影。定番・作者不詳の流布問題)。流布例: https://nazoq.com/easiest/Q001174.html 。文面はオリジナルに書き下ろし(表現は書き直し済み)。', 1);

-- A14
INSERT INTO quiz_stock_items (set_id, quiz_type, difficulty, question_text, answer_text, content_fields, source_note, is_active)
VALUES ((SELECT id FROM batch_sets WHERE set_code = 'logic-training-1'), 'L1', 'light',
        '使う前に、必ず一度壊さなければいけないものは、なんだ?',
        '卵(割ってから使う)',
        '{"hook":"壊しても使えるのか!","hint":"朝ごはんにも登場するぞ!","question":"使う前に、必ず一度壊さなければいけないものは、なんだ?","answer":"卵(割ってから使う)","explanation":"料理で使うには、まず殻を割るしかない。「壊す=ダメにする」という思い込みを裏切る定番なぞなぞ。","coach_comment":"壊すのが正解、痛快だな!","tags":["なぞなぞ","朝の一問","頭の体操"],"summary":"使う前に壊す必要がある=卵という英語圏古典の定番なぞなぞ。","illustration_scene":"朝の部屋に「こわれもの注意」と書かれた段ボール箱がひとつ置かれ、箱の上に大きな「?」が浮かんでいる。"}',
        '類型: 逆説なぞなぞ(英語圏古典 Egg riddle)。流布例: https://parade.com/947956/parade/riddles/ 。文面はオリジナルに書き下ろし(表現は書き直し済み)。', 1);

-- A12
INSERT INTO quiz_stock_items (set_id, quiz_type, difficulty, question_text, answer_text, content_fields, source_note, is_active)
VALUES ((SELECT id FROM batch_sets WHERE set_code = 'logic-training-1'), 'L1', 'light',
        '「1日」には2回もあるのに、「1年」には1回しかない。そんな不思議なもの、なんだ?',
        'ひらがなの「ち」',
        '{"hook":"1日に2回あるもの?","hint":"読み方をひらがなにするんだ!","question":"「1日」には2回もあるのに、「1年」には1回しかない。そんな不思議なもの、なんだ?","answer":"ひらがなの「ち」","explanation":"「いちにち」には「ち」が2回、「いちねん」には1回だけ。時間の話に見せかけた文字数えのなぞなぞ。","coach_comment":"ひらがなに直した瞬間の勝利!","tags":["なぞなぞ","朝の一問","文字あそび"],"summary":"いちにちに2回・いちねんに1回=「ち」の字という定番の文字数えなぞなぞ。","illustration_scene":"朝のデスクに置かれた日めくりカレンダーと腕時計。ブラインドの隙間から朝日が差している。"}',
        '類型: 文字数えなぞなぞ(定番・作者不詳の流布問題)。流布例: https://www.nazo2.net/tyuukyuu/002.html 。文面はオリジナルに書き下ろし(表現は書き直し済み)。', 1);

-- B01
INSERT INTO quiz_stock_items (set_id, quiz_type, difficulty, question_text, answer_text, content_fields, source_note, is_active)
VALUES ((SELECT id FROM batch_sets WHERE set_code = 'logic-training-1'), 'L3', 'standard',
        '人が一生のあいだに眠る時間は、全部合計するとおよそ何年分になる?',
        '約25年(目安)',
        '{"hook":"寝てる時間、実は…","hint":"1日の何分の1寝てるかだ!","question":"人が一生のあいだに眠る時間は、全部合計するとおよそ何年分になる?","answer":"約25年(目安)","explanation":"1日8時間眠ると仮定すると1日の3分の1。人生80年なら×1/3で25〜27年ほど。人生の4分の1以上は布団の中で過ぎていく。","coach_comment":"だから睡眠の質にこだわろう!","tags":["フェルミ推定","数字感覚","昼の一問"],"summary":"一生の睡眠時間の合計を、1日8時間×人生80年の3分の1で約25年と概算する規模感クイズ。","illustration_scene":"明るい昼の部屋にふかふかの布団と枕がぽつんと敷かれ、布団の真上に大きな「?」が浮かんでいる。窓から昼の光が差し込んでいる。"}',
        '類型: 身近な量の積み上げ推定(時間×比率のフェルミ分解)。参照: https://en.wikipedia.org/wiki/Fermi_problem (research.md B-01 の応用)。題材・文面はオリジナルに書き下ろし(表現は書き直し済み)。', 1);

-- B02
INSERT INTO quiz_stock_items (set_id, quiz_type, difficulty, question_text, answer_text, content_fields, source_note, is_active)
VALUES ((SELECT id FROM batch_sets WHERE set_code = 'logic-training-1'), 'L3', 'standard',
        '毎日のなにげない歩き。一生分を合計すると、距離はおよそどれくらいになる?',
        '約15万km(地球3周半・目安)',
        '{"hook":"毎日の一歩の行き先","hint":"1日の距離×一生の日数だ!","question":"毎日のなにげない歩き。一生分を合計すると、距離はおよそどれくらいになる?","answer":"約15万km(地球3周半・目安)","explanation":"1日7000歩・歩幅0.7m・人生80年と仮定。1日約5km×365日×80年≈15万km。地球1周4万kmを3周半している計算。","coach_comment":"君の足はもう地球級だ!","tags":["フェルミ推定","数字感覚","昼の一問"],"summary":"一生に歩く距離を、1日7000歩×歩幅0.7m×80年で約15万km(地球3周半)と概算する規模感クイズ。","illustration_scene":"昼の公園の道にスニーカーがひと組置かれ、その先へ足あとが点々と延びている。足あとの行き先に大きな「?」が浮かんでいる。"}',
        '類型: 身近な量の積み上げ推定(歩数×歩幅×年数のフェルミ分解)。参照: https://en.wikipedia.org/wiki/Fermi_problem 。題材・文面はオリジナルに書き下ろし(表現は書き直し済み)。', 1);

-- B03
INSERT INTO quiz_stock_items (set_id, quiz_type, difficulty, question_text, answer_text, content_fields, source_note, is_active)
VALUES ((SELECT id FROM batch_sets WHERE set_code = 'logic-training-1'), 'L3', 'standard',
        'あなたの心臓が1日に打つ回数は、およそ何回?',
        '約10万回(目安)',
        '{"hook":"胸の中の働き者","hint":"1分の回数から積み上げろ!","question":"あなたの心臓が1日に打つ回数は、およそ何回?","answer":"約10万回(目安)","explanation":"1分に70回打つと仮定すると、70×60分×24時間≈10万回。生まれてから一度も休まずこのペースで働いている。","coach_comment":"心臓に負けないよう動こう!","tags":["フェルミ推定","数字感覚","昼の一問"],"summary":"心臓の1日の拍動数を、毎分70回×60分×24時間で約10万回と概算する規模感クイズ。","illustration_scene":"明るい昼の空の下、大きな赤いハートのモチーフが元気に跳ねているコミカルな絵。まわりにリズムを表す線と音符が飛び、そばに大きな「?」が浮かんでいる。"}',
        '類型: 身近な量の積み上げ推定(頻度×時間のフェルミ分解)。参照: https://en.wikipedia.org/wiki/Fermi_problem 。題材・文面はオリジナルに書き下ろし(表現は書き直し済み)。', 1);

-- B04
INSERT INTO quiz_stock_items (set_id, quiz_type, difficulty, question_text, answer_text, content_fields, source_note, is_active)
VALUES ((SELECT id FROM batch_sets WHERE set_code = 'logic-training-1'), 'L3', 'standard',
        '人が一生のあいだにまばたきする回数は、およそ何回?',
        '約4億回(目安)',
        '{"hook":"無意識の累計回数","hint":"1分×起きてる時間で計算だ!","question":"人が一生のあいだにまばたきする回数は、およそ何回?","answer":"約4億回(目安)","explanation":"1分に15回・起床16時間・人生80年と仮定。1日約1.4万回×365日×80年≈4億回。無意識の動きも積もれば天文学的。","coach_comment":"無意識の積み重ねを侮るな!","tags":["フェルミ推定","数字感覚","昼の一問"],"summary":"一生のまばたき回数を、毎分15回×起床16時間×80年で約4億回と概算する規模感クイズ。","illustration_scene":"昼の明るいデスクでノートパソコンの横に目薬がひとつ置かれ、そばに大きな「?」が浮かんでいる。窓の外は明るい昼の空。"}',
        '類型: 身近な量の積み上げ推定(頻度×時間のフェルミ分解)。参照: https://en.wikipedia.org/wiki/Fermi_problem 。題材・文面はオリジナルに書き下ろし(表現は書き直し済み)。', 1);

-- B05
INSERT INTO quiz_stock_items (set_id, quiz_type, difficulty, question_text, answer_text, content_fields, source_note, is_active)
VALUES ((SELECT id FROM batch_sets WHERE set_code = 'logic-training-1'), 'L3', 'standard',
        '健康な人でも、髪の毛は1日におよそ何本、自然に抜けている?',
        '約50〜100本(目安)',
        '{"hook":"排水口を見て焦る前に","hint":"髪の本数と寿命から攻めろ!","question":"健康な人でも、髪の毛は1日におよそ何本、自然に抜けている?","answer":"約50〜100本(目安)","explanation":"髪は約10万本で、1本の寿命は4〜5年=約1600日。毎日その1600分の1、10万×1/1600≈60本が入れ替わる。","coach_comment":"数字を知れば怖くない!","tags":["フェルミ推定","数字感覚","昼の一問"],"summary":"1日の自然な抜け毛を、総本数10万本÷毛の寿命4〜5年で約50〜100本と概算する規模感クイズ。","illustration_scene":"昼の明るい部屋で、後ろ姿の人が髪をとかし、頭から抜けた髪の毛が数本はらはらと宙に舞っている。そばに大きな「?」が浮かんでいる。窓から昼の光が差し込んでいる。顔は描かない。"}',
        '類型: ストック・フロー分解(総量÷寿命のフェルミ分解)。参照: https://en.wikipedia.org/wiki/Fermi_problem (research.md B-02 と同型)。題材・文面はオリジナルに書き下ろし(表現は書き直し済み)。', 1);

-- B06
INSERT INTO quiz_stock_items (set_id, quiz_type, difficulty, question_text, answer_text, content_fields, source_note, is_active)
VALUES ((SELECT id FROM batch_sets WHERE set_code = 'logic-training-1'), 'L3', 'standard',
        '朝・昼・晩の食事。一生分を合計すると、およそ何回ごはんを食べることになる?',
        '約9万回(目安)',
        '{"hook":"メシの回数、数えた?","hint":"1日3回×一生の年数だ!","question":"朝・昼・晩の食事。一生分を合計すると、およそ何回ごはんを食べることになる?","answer":"約9万回(目安)","explanation":"1日3回・人生80年と仮定すると、3×365日で年約1100回。1100×80年≈9万回。1回1回の食事は、9万分の1の貴重な機会。","coach_comment":"次の一食も大事に食べよう!","tags":["フェルミ推定","数字感覚","昼の一問"],"summary":"一生の食事回数を、1日3回×365日×80年で約9万回と概算する規模感クイズ。","illustration_scene":"昼の食堂の長いテーブルに、湯気の立つ定食が奥までずらりと無限に並んでいる。手前の定食の真上に大きな「?」が浮かんでいる。窓から明るい昼の光。"}',
        '類型: 身近な量の積み上げ推定(頻度×年数のフェルミ分解)。参照: https://en.wikipedia.org/wiki/Fermi_problem 。題材・文面はオリジナルに書き下ろし(表現は書き直し済み)。', 1);

-- B07
INSERT INTO quiz_stock_items (set_id, quiz_type, difficulty, question_text, answer_text, content_fields, source_note, is_active)
VALUES ((SELECT id FROM batch_sets WHERE set_code = 'logic-training-1'), 'L3', 'standard',
        '毎日の通勤時間。働く40年分を合計すると、およそどれくらいの長さになる?',
        '約1年分(目安)',
        '{"hook":"通勤の合計、まさかの長さ","hint":"往復1時間×働く日数だ!","question":"毎日の通勤時間。働く40年分を合計すると、およそどれくらいの長さになる?","answer":"約1年分(目安)","explanation":"往復1時間・年240日・40年勤務と仮定。1×240×40=9600時間を24時間で割ると400日。まる1年を通勤に使う計算。","coach_comment":"移動時間も鍛える時間にな!","tags":["フェルミ推定","数字感覚","昼の一問"],"summary":"40年分の通勤時間を、往復1時間×年240日×40年=9600時間≈約1年と概算する規模感クイズ。","illustration_scene":"昼の駅の改札前に大きな駅時計が立ち、その下を通勤かばんを提げた人が後ろ姿で通り過ぎていく。時計のそばに大きな「?」が浮かんでいる。"}',
        '類型: 身近な量の積み上げ推定(時間×日数×年数のフェルミ分解)。参照: https://en.wikipedia.org/wiki/Fermi_problem 。題材・文面はオリジナルに書き下ろし(表現は書き直し済み)。', 1);

-- B09
INSERT INTO quiz_stock_items (set_id, quiz_type, difficulty, question_text, answer_text, content_fields, source_note, is_active)
VALUES ((SELECT id FROM batch_sets WHERE set_code = 'logic-training-1'), 'L3', 'standard',
        '日本全国で、1日に飲まれる缶コーヒーはおよそ何本?',
        '約2000万本(目安)',
        '{"hook":"自販機の前で一問","hint":"何人に1人飲むか見積もれ!","question":"日本全国で、1日に飲まれる缶コーヒーはおよそ何本?","answer":"約2000万本(目安)","explanation":"働く人は約6000万人。3人に1人が1日1本飲むと仮定すると、6000万×1/3=2000万本。","coach_comment":"「何人に1人」の感覚が効いたな!","tags":["フェルミ推定","数字感覚","昼の一問"],"summary":"缶コーヒーの1日の全国消費本数を、就業者6000万人×3人に1人が1日1本で約2000万本と概算する推定。","illustration_scene":"昼のオフィス街の路地に自動販売機が1台立ち、取り出し口から缶コーヒーがひとつ転がり出ている。自販機の上に大きな「?」が浮かび、昼の日差しが路面に反射している。"}',
        '類型: 利用者・購買頻度分解(セグメント化)。参照: https://en.wikipedia.org/wiki/Fermi_problem (research.md B-16)。題材・文面はオリジナルに書き下ろし(表現は書き直し済み)。', 1);

-- B10
INSERT INTO quiz_stock_items (set_id, quiz_type, difficulty, question_text, answer_text, content_fields, source_note, is_active)
VALUES ((SELECT id FROM batch_sets WHERE set_code = 'logic-training-1'), 'L3', 'standard',
        '日本全国で、1日に配達される宅配便はおよそ何個?',
        '約1000万個(目安)',
        '{"hook":"置き配の箱、全国では?","hint":"自分が月に受け取る数からだ!","question":"日本全国で、1日に配達される宅配便はおよそ何個?","answer":"約1000万個(目安)","explanation":"1人が月に2〜3個受け取ると仮定すると年約30個。人口1.2億×30個÷365日≈1000万個。","coach_comment":"自分の生活から出発した推定だ!","tags":["フェルミ推定","数字感覚","昼の一問"],"summary":"宅配便の1日の配達個数を、1人あたり年30個×人口1.2億の日割りで約1000万個と概算する推定。","illustration_scene":"昼の玄関先に段ボール箱が高く積み上がり、いちばん上の箱に大きな「?」が描かれている。明るい昼の光が差している。"}',
        '類型: 消費者数・利用頻度分解。参照: https://en.wikipedia.org/wiki/Fermi_problem (research.md B-01/B-13)。題材・文面はオリジナルに書き下ろし(表現は書き直し済み)。', 1);

-- B08
INSERT INTO quiz_stock_items (set_id, quiz_type, difficulty, question_text, answer_text, content_fields, source_note, is_active)
VALUES ((SELECT id FROM batch_sets WHERE set_code = 'logic-training-1'), 'L3', 'standard',
        '朝のラッシュ時、都心の通勤電車1編成(10両)にはおよそ何人乗っている?',
        '約2000人(目安)',
        '{"hook":"満員電車を数字にする","hint":"定員×両数×混雑率で勝負だ!","question":"朝のラッシュ時、都心の通勤電車1編成(10両)にはおよそ何人乗っている?","answer":"約2000人(目安)","explanation":"1両の定員を約150人、ラッシュは定員の1.4倍の混雑と仮定する。150×1.4×10両≈2000人。","coach_comment":"定員×混雑率、現場感ある分解!","tags":["フェルミ推定","数字感覚","昼の一問"],"summary":"ラッシュ時の通勤電車1編成の乗客数を、1両定員150人×混雑率140%×10両で約2000人と概算する推定。","illustration_scene":"明るい昼の空の下、高架を走る通勤電車を真横から見た構図。並んだ窓の中は小さなシルエットでぎっしり埋まり、車両の上に大きな「?」が浮かんでいる。"}',
        '類型: 通勤者・利用率・車両容量分解。参照: https://en.wikipedia.org/wiki/Fermi_problem (research.md B-12)。題材・文面はオリジナルに書き下ろし(表現は書き直し済み)。', 1);

-- B11
INSERT INTO quiz_stock_items (set_id, quiz_type, difficulty, question_text, answer_text, content_fields, source_note, is_active)
VALUES ((SELECT id FROM batch_sets WHERE set_code = 'logic-training-1'), 'L3', 'standard',
        '日本全国にある自動販売機は、およそ何台?',
        '約400万台(目安)',
        '{"hook":"自販機密度、世界一らしいぞ!","hint":"1台で何人カバーするかだ!","question":"日本全国にある自動販売機は、およそ何台?","answer":"約400万台(目安)","explanation":"30人に1台の割合と仮定すると、人口1.2億×1/30=400万台。歩けばすぐ見つかる密度の正体。","coach_comment":"人口で割る、王道の一手だ!","tags":["フェルミ推定","数字感覚","昼の一問"],"summary":"全国の自動販売機の台数を、人口1.2億÷30人に1台で約400万台と概算する密度型の推定。","illustration_scene":"昼の住宅街の角に色違いの自動販売機が2台並び、その上に大きな「?」が浮かんでいる。奥に電柱と明るい昼の青空。"}',
        '類型: 人口・密度分解。参照: https://en.wikipedia.org/wiki/Fermi_problem (research.md B-15 と同型)。題材・文面はオリジナルに書き下ろし(表現は書き直し済み)。', 1);

-- B12
INSERT INTO quiz_stock_items (set_id, quiz_type, difficulty, question_text, answer_text, content_fields, source_note, is_active)
VALUES ((SELECT id FROM batch_sets WHERE set_code = 'logic-training-1'), 'L3', 'standard',
        '日本全国で、1日に生まれる赤ちゃんはおよそ何人?',
        '約1900人(目安)',
        '{"hook":"きょうも生まれてくる命","hint":"1年分を365日で割るんだ!","question":"日本全国で、1日に生まれる赤ちゃんはおよそ何人?","answer":"約1900人(目安)","explanation":"年間の出生数は約70万人。70万×1/365≈1900人。この動画を見ている間にも、どこかで生まれている。","coach_comment":"この数字、ちょっと沁みるだろ","tags":["フェルミ推定","数字感覚","昼の一問"],"summary":"1日の出生数を、年間出生数70万人÷365日で約1900人と概算する日割り型の推定。","illustration_scene":"昼の明るい病院の新生児室に、新生児用の透明なベビーベッドがずらりとたくさん並んでいる。中央に大きな「?」が浮かび、窓からやわらかい昼の光が差し込んでいる。赤ちゃんの顔は描かない。"}',
        '類型: 年間量の日割り分解(コホート型)。参照: https://en.wikipedia.org/wiki/Fermi_problem (research.md B-06/B-14 と同型)。題材・文面はオリジナルに書き下ろし(表現は書き直し済み)。', 1);

-- B13
INSERT INTO quiz_stock_items (set_id, quiz_type, difficulty, question_text, answer_text, content_fields, source_note, is_active)
VALUES ((SELECT id FROM batch_sets WHERE set_code = 'logic-training-1'), 'L3', 'standard',
        '大好きな人も多いカレーライス。一生で食べる回数は、およそ何皿になる?',
        '約1700皿(目安)',
        '{"hook":"カレー人生、何皿分?","hint":"月に何回×何年で計算だ!","question":"大好きな人も多いカレーライス。一生で食べる回数は、およそ何皿になる?","answer":"約1700皿(目安)","explanation":"月に2回と仮定すると2×12か月で年24皿。カレーを食べない幼少期を除いた70年で24×70≈1700皿。好物の回数も、数えてみれば有限。","coach_comment":"次の一皿がもう楽しみだな!","tags":["フェルミ推定","数字感覚","昼の一問"],"summary":"一生で食べるカレーの皿数を、月2回×12か月×70年で約1700皿と概算する規模感クイズ。","illustration_scene":"昼のキッチンで大きな鍋からカレーの湯気が上がり、そばにスプーンとお皿がどちらも山のように高く積み上げてある。鍋の真上に大きな「?」が浮かんでいる。"}',
        '類型: 身近な量の積み上げ推定(頻度×年数のフェルミ分解)。参照: https://en.wikipedia.org/wiki/Fermi_problem 。題材・文面はオリジナルに書き下ろし(表現は書き直し済み)。', 1);

-- B14
INSERT INTO quiz_stock_items (set_id, quiz_type, difficulty, question_text, answer_text, content_fields, source_note, is_active)
VALUES ((SELECT id FROM batch_sets WHERE set_code = 'logic-training-1'), 'L3', 'standard',
        'なんとなく見ているスマホ。1年分を合計すると、どれくらいの時間になる?',
        '約50日分(目安)',
        '{"hook":"スマホ時間の正体","hint":"1日何時間×365日だ!","question":"なんとなく見ているスマホ。1年分を合計すると、どれくらいの時間になる?","answer":"約50日分(目安)","explanation":"1日3.5時間見ると仮定すると3.5×365≈1300時間。24時間で割ると約53日。1年の7分の1がスマホの中。","coach_comment":"その5分、ロジトレに使おう!","tags":["フェルミ推定","数字感覚","昼の一問"],"summary":"1年間のスマホ利用時間を、1日3.5時間×365日≈1300時間=約50日分と概算する規模感クイズ。","illustration_scene":"昼のカフェのテーブルでスマートフォンが画面を上にして光り、画面から小さな時計のマークがいくつも飛び出している。そばに大きな「?」。窓の外は明るい昼の通り。"}',
        '類型: 身近な量の積み上げ推定(時間×日数のフェルミ分解)。参照: https://en.wikipedia.org/wiki/Fermi_problem 。題材・文面はオリジナルに書き下ろし(表現は書き直し済み)。', 1);

-- C01
INSERT INTO quiz_stock_items (set_id, quiz_type, difficulty, question_text, answer_text, content_fields, source_note, is_active)
VALUES ((SELECT id FROM batch_sets WHERE set_code = 'logic-training-1'), 'L1', 'deep',
        '10階に住む人は、雨の日はエレベーターで10階まで行くのに、晴れの日は7階で降りて階段を使う。なぜ?',
        '傘があれば10階を押せる',
        '{"hook":"今夜は名作パズルだ","hint":"その人の「体」に理由があるぞ!","question":"10階に住む人は、雨の日はエレベーターで10階まで行くのに、晴れの日は7階で降りて階段を使う。なぜ?","answer":"傘があれば10階を押せる","explanation":"この人は背が低くて、届くボタンが7階まで。雨の日だけは持っている傘の先で10階のボタンを押せる。","coach_comment":"見えない前提を探せたか!","tags":["水平思考","夜の一問","名作パズル"],"summary":"晴れの日だけ7階で降りる理由を「背が届かず、傘がある日だけ10階を押せる」と見抜く水平思考の古典(The elevator man)。","illustration_scene":"夜のエレベーターの中で階数ボタンのパネルが光り、その横に大きな「?」が浮かんでいる。扉の金属面に夜の照明が映り込んでいる。"}',
        '類型: 水平思考パズルの古典(The elevator man)。参照: https://en.wikipedia.org/wiki/Situation_puzzle (research3.md B-01)。人物設定・文面はオリジナルに書き下ろし(表現は書き直し済み)。', 1);

-- C02
INSERT INTO quiz_stock_items (set_id, quiz_type, difficulty, question_text, answer_text, content_fields, source_note, is_active)
VALUES ((SELECT id FROM batch_sets WHERE set_code = 'logic-training-1'), 'L1', 'deep',
        '「水を1杯ください」と頼んだ客に、店員はいきなり大きな物音を立てて驚かせた。なのに客はお礼を言って帰った。なぜ?',
        'しゃっくりが止まったから',
        '{"hook":"たった一杯の水の物語だ","hint":"水がほしい理由を考えるんだ!","question":"「水を1杯ください」と頼んだ客に、店員はいきなり大きな物音を立てて驚かせた。なのに客はお礼を言って帰った。なぜ?","answer":"しゃっくりが止まったから","explanation":"客はしゃっくりを止めたくて水を頼んだ。驚かせるのも止める方法のひとつ。目的は水ではなく、しゃっくり退治。","coach_comment":"頼みの奥の目的を読んだな!","tags":["水平思考","夜の一問","名作パズル"],"summary":"水を頼んだ客が驚かされて感謝する理由を「しゃっくりを止めたかった」と見抜く水平思考の世界的古典。","illustration_scene":"夜のバーで店員が客を驚かせた瞬間。カウンター越しに両手を大きく広げた店員と、肩を跳ね上げて驚く客を遠景のシルエットで描き、顔は描かない。二人の間に大きな音の衝撃線が走る。カウンターには水の入ったグラスがひとつと大きな「?」。暖色の間接照明が夜の店内を照らしている。"}',
        '類型: 水平思考パズルの古典(A man walks into a bar / しゃっくり)。参照: https://en.wikipedia.org/wiki/Situation_puzzle (research3.md B-02)。銃を物音に置き換えるなど状況・文面はオリジナルに書き下ろし(表現は書き直し済み)。', 1);

-- C03
INSERT INTO quiz_stock_items (set_id, quiz_type, difficulty, question_text, answer_text, content_fields, source_note, is_active)
VALUES ((SELECT id FROM batch_sets WHERE set_code = 'logic-training-1'), 'L1', 'deep',
        '「この屏風の絵の虎が夜な夜な抜け出して暴れる。捕まえてくれ」と無茶を言われた。とんちで有名な小僧さんは、どう切り返した?',
        '「では虎を追い出して」',
        '{"hook":"日本一有名なとんちだぞ!","hint":"無理な注文は相手に返すんだ!","question":"「この屏風の絵の虎が夜な夜な抜け出して暴れる。捕まえてくれ」と無茶を言われた。とんちで有名な小僧さんは、どう切り返した?","answer":"「では虎を追い出して」","explanation":"「絵から出られるなら、まず屏風から追い出してください。出てきたら捕まえます」と返した。無理な前提を相手に返すとんち。","coach_comment":"前提ごとひっくり返す、天才!","tags":["とんち","夜の一問","一休さん"],"summary":"屏風の虎を捕まえろという無茶ぶりに「まず追い出して」と返す一休咄の古典とんち(屏風の虎退治)。","illustration_scene":"夜の和室に金色の屏風が立ち、屏風の中に描かれた虎が今にも飛び出しそうなポーズで吠えている。屏風の前に子どもの小僧さんが後ろ姿で立ち、腕を組んで首をかしげて考え込んでいる(顔は描かない)。行灯の明かりが畳を照らし、虎の上に大きな「?」が浮かんでいる。"}',
        '類型: 一休咄の古典とんち(屏風の虎退治。頓智咄を原作とする民話)。参照: https://ja.wikipedia.org/wiki/一休さん (research3.md B-03)。文面はオリジナルに書き下ろし(表現は書き直し済み)。', 1);

-- C05
INSERT INTO quiz_stock_items (set_id, quiz_type, difficulty, question_text, answer_text, content_fields, source_note, is_active)
VALUES ((SELECT id FROM batch_sets WHERE set_code = 'logic-training-1'), 'L1', 'deep',
        'ゲームで3つの扉から1つを選ぶ。①火が燃えさかる部屋 ②毒ガスが充満した部屋 ③3年間なにも食べていないライオンの部屋。安全なのは?',
        '③(ライオンはもう死んでいる)',
        '{"hook":"間違えたら即アウトだぞ!","hint":"「3年間」の意味をよく考えろ!","question":"ゲームで3つの扉から1つを選ぶ。①火が燃えさかる部屋 ②毒ガスが充満した部屋 ③3年間なにも食べていないライオンの部屋。安全なのは?","answer":"③(ライオンはもう死んでいる)","explanation":"3年間なにも食べていないライオンは、生きていられない。一番危険に見える扉が、実は一番安全。","coach_comment":"条件を最後まで読んだ者の勝ちだ!","tags":["ひっかけ","夜の一問","頭の体操"],"summary":"3年間何も食べていないライオンはすでに死んでいるため③が安全、という定番ひっかけクイズ。","illustration_scene":"夜のダンジョン風の石造りの通路に装飾の異なる3つの扉が並び、3つの扉の真上に大きな「?」が浮かんでいる。壁のたいまつが通路を照らすファンタジー調の絵。"}',
        '類型: 定番ひっかけクイズ(3つの部屋とライオン。広く流布・作者不詳)。流布例: https://quiz-oukoku.jp/super-hard-hikkake-quiz/ (research3.md B-05)。死刑囚の設定をゲームに置き換えるなど文面はオリジナルに書き下ろし(表現は書き直し済み)。', 1);

-- C06
INSERT INTO quiz_stock_items (set_id, quiz_type, difficulty, question_text, answer_text, content_fields, source_note, is_active)
VALUES ((SELECT id FROM batch_sets WHERE set_code = 'logic-training-1'), 'L1', 'deep',
        '父と息子が事故にあい、別々の病院へ運ばれた。息子の手術室に入ってきた外科医が言った。「この子は私の息子です」。外科医は誰?',
        '息子の母親',
        '{"hook":"解けない大人が続出だぞ!","hint":"思い込みを1つ外してみろ!","question":"父と息子が事故にあい、別々の病院へ運ばれた。息子の手術室に入ってきた外科医が言った。「この子は私の息子です」。外科医は誰?","answer":"息子の母親","explanation":"外科医=男性という思い込みがあると解けない。医師は母親。頭の中の「当たり前」に気づかせる有名な問題。","coach_comment":"思い込みを1枚はがせたな!","tags":["ひっかけ","夜の一問","思い込み"],"summary":"手術室の外科医が「私の息子」と言う矛盾を、外科医=母親と見抜く思い込み(アンコンシャスバイアス)の有名問題。","illustration_scene":"夜の手術室の中で、手術着を着た外科医が後ろ姿で手術台に向かって立っている。頭部は大きな「?」ですっぽり覆い、体型や髪型で性別が分からないように描く。無影灯の明かりが室内を照らす。患者や他の人物の顔は描かない。"}',
        '類型: 思い込み(アンコンシャスバイアス)を突く有名問題。研修教材にも使われる定番。流布例: https://www.nazo2.net/nanmon/042.html (research3.md B-06)。文面はオリジナルに書き下ろし(表現は書き直し済み)。', 1);

-- C04
INSERT INTO quiz_stock_items (set_id, quiz_type, difficulty, question_text, answer_text, content_fields, source_note, is_active)
VALUES ((SELECT id FROM batch_sets WHERE set_code = 'logic-training-1'), 'L1', 'deep',
        '橋のたもとに「このはしわたるべからず」の立て札。それでもとんちで有名な小僧さんは堂々と渡ってみせた。どうやって?',
        '真ん中を歩いて渡った',
        '{"hook":"立て札のナゾを解け","hint":"「はし」は橋だけじゃないぞ!","question":"橋のたもとに「このはしわたるべからず」の立て札。それでもとんちで有名な小僧さんは堂々と渡ってみせた。どうやって?","answer":"真ん中を歩いて渡った","explanation":"「はし」を橋ではなく「端」と読み替えた。端を渡るなと書いてあるだけだから、真ん中なら堂々と渡れる。","coach_comment":"言葉の二枚目の顔を見たな!","tags":["とんち","夜の一問","一休さん"],"summary":"「このはし渡るべからず」を端と読み替えて真ん中を渡る一休咄の古典とんち。","illustration_scene":"夜の小さな太鼓橋のたもとに立て札が立ち、札の面に大きな「?」が描かれている。立て札の前に子どもの小僧さんが後ろ姿で立ち、腕を組んで考え込んでいる(顔は描かない)。灯籠の明かりが川面に揺れている和風の情景。"}',
        '類型: 一休咄の古典とんち(このはし渡るべからず。同音異義の読み替え)。参照: https://ja.wikipedia.org/wiki/一休さん (research3.md B-04)。文面はオリジナルに書き下ろし(表現は書き直し済み)。', 1);

-- C07
INSERT INTO quiz_stock_items (set_id, quiz_type, difficulty, question_text, answer_text, content_fields, source_note, is_active)
VALUES ((SELECT id FROM batch_sets WHERE set_code = 'logic-training-1'), 'L1', 'deep',
        '冬の山小屋にストーブ・ランプ・ろうそくがある。でもマッチは1本しかない。さて、最初に火をつけるべきものは?',
        'マッチ(最初の火はここから)',
        '{"hook":"サバイバル力が試されるぞ!","hint":"道具を使う「順番」の話だぞ!","question":"冬の山小屋にストーブ・ランプ・ろうそくがある。でもマッチは1本しかない。さて、最初に火をつけるべきものは?","answer":"マッチ(最初の火はここから)","explanation":"ストーブもランプもろうそくも、火をつけるにはまずマッチをする必要がある。最初の火は必ずマッチ。","coach_comment":"順番の盲点、突かれたか?","tags":["ひっかけ","夜の一問","頭の体操"],"summary":"ストーブ・ランプ・ろうそくの前に、まずマッチに火をつけるという順番の盲点を突く定番ひっかけ。","illustration_scene":"夜の山小屋の木のテーブルにランプ・ろうそく・薪ストーブが並び、どれにも火がついていない。真ん中に大きな「?」が浮かんでいる。マッチは描かない。"}',
        '類型: 定番ひっかけクイズ(最初に火をつけるのはマッチ。広く流布・作者不詳)。流布例: https://kabu-elife.sakura.ne.jp/inc/nazonazo/cat2/057.html (research3.md B-09)。文面はオリジナルに書き下ろし(表現は書き直し済み)。', 1);

-- C08
INSERT INTO quiz_stock_items (set_id, quiz_type, difficulty, question_text, answer_text, content_fields, source_note, is_active)
VALUES ((SELECT id FROM batch_sets WHERE set_code = 'logic-training-1'), 'L1', 'deep',
        '2人の父と2人の息子で釣りに行き、釣れた魚はちょうど3匹。それでも全員が1匹ずつ持ち帰れた。どういうこと?',
        '祖父・父・息子の3人だった',
        '{"hook":"不思議な夜釣りの話をしよう","hint":"1人が2つの顔を持てるんだ!","question":"2人の父と2人の息子で釣りに行き、釣れた魚はちょうど3匹。それでも全員が1匹ずつ持ち帰れた。どういうこと?","answer":"祖父・父・息子の3人だった","explanation":"真ん中の父は「祖父の息子」であり「息子の父」でもある。2人の父と2人の息子は、合わせて3人で成立する。","coach_comment":"1人2役に気づけば一撃だ!","tags":["ひっかけ","夜の一問","頭の体操"],"summary":"2人の父と2人の息子=祖父・父・息子の3人という、役割の重なりを見抜く定番ひっかけ。","illustration_scene":"夜の防波堤に常夜灯が灯り、開いたクーラーボックスの中で魚が3匹跳ねている。そばに大きな「?」が浮かび、海面に月明かりが揺れている。釣り竿は描かない。"}',
        '類型: 家族の数えひっかけ(2人の父と2人の息子。広く流布・作者不詳)。流布例: https://note.com/kazunext/n/nd2456105c2db (research3.md B-11)。文面はオリジナルに書き下ろし(表現は書き直し済み)。', 1);

-- C09
INSERT INTO quiz_stock_items (set_id, quiz_type, difficulty, question_text, answer_text, content_fields, source_note, is_active)
VALUES ((SELECT id FROM batch_sets WHERE set_code = 'logic-training-1'), 'L1', 'deep',
        '財布から2枚の硬貨で、ちょうど110円を払った。片方は10円玉ではない。さて、何と何で払った?',
        '100円玉と10円玉',
        '{"hook":"たった110円の難問だ!","hint":"「片方は」の範囲に注意だ!","question":"財布から2枚の硬貨で、ちょうど110円を払った。片方は10円玉ではない。さて、何と何で払った?","answer":"100円玉と10円玉","explanation":"「片方は10円玉ではない」の片方とは100円玉のこと。もう片方が10円玉でも、この文は嘘をついていない。","coach_comment":"言葉の射程を見切ったな!","tags":["ひっかけ","夜の一問","言葉あそび"],"summary":"「片方は10円玉ではない」が100円玉を指すだけ、という量化の言葉ひっかけ(110円=100円+10円)。","illustration_scene":"夜のコンビニのレジカウンターにキャッシュトレーが置かれ、その真上に大きな「?」が浮かんでいる。窓の外に夜の街の明かり。硬貨は描かない。"}',
        '類型: 量化の言葉ひっかけ(「片方は〜ではない」。英語圏の two coins 型の日本語定番)。流布例: https://quiz-tairiku.com/logic/a111.html (research3.md B-14)。金額・文面はオリジナルに書き下ろし(表現は書き直し済み)。', 1);

-- C10
INSERT INTO quiz_stock_items (set_id, quiz_type, difficulty, question_text, answer_text, content_fields, source_note, is_active)
VALUES ((SELECT id FROM batch_sets WHERE set_code = 'logic-training-1'), 'L1', 'deep',
        '停電の夜、ろうそく10本に火をつけた。しばらくして風で3本が消えた。そのまま朝まで置いておくと、残っているろうそくは何本?',
        '3本(消えた分だけ残る)',
        '{"hook":"停電の夜って、ワクワクするよな!","hint":"朝まで時間を進めてみるんだ!","question":"停電の夜、ろうそく10本に火をつけた。しばらくして風で3本が消えた。そのまま朝まで置いておくと、残っているろうそくは何本?","answer":"3本(消えた分だけ残る)","explanation":"火がついたままの7本は朝までに燃え尽きる。途中で消えた3本だけが、ろうそくの姿のまま残っている。","coach_comment":"時間を最後まで進めたか?","tags":["ひっかけ","夜の一問","頭の体操"],"summary":"燃え続けた7本は燃え尽き、消えた3本だけが残るという時間経過の盲点を突く定番ひっかけ。","illustration_scene":"停電の夜の窓辺で火のついたろうそくが数本ゆらめき、カーテン越しに月明かりが差し込んでいる。そばに大きな「?」が浮かぶ。ろうそくの本数は数えられない構図にする。"}',
        '類型: 定番ひっかけクイズ(残るろうそく。広く流布・作者不詳)。流布例: http://nazo-nazo.com/sp/cat398/103.html (research3.md B-10 代替)。文面はオリジナルに書き下ろし(表現は書き直し済み)。', 1);

-- C11
INSERT INTO quiz_stock_items (set_id, quiz_type, difficulty, question_text, answer_text, content_fields, source_note, is_active)
VALUES ((SELECT id FROM batch_sets WHERE set_code = 'logic-training-1'), 'L1', 'deep',
        '「誰にもほどけないこの結び目をほどいた者が、王になる」という伝説の固い結び目。ある若者は一瞬で解決してみせた。どうやって?',
        '剣で断ち切った',
        '{"hook":"伝説の結び目に挑め","hint":"「ほどく」にこだわるな!","question":"「誰にもほどけないこの結び目をほどいた者が、王になる」という伝説の固い結び目。ある若者は一瞬で解決してみせた。どうやって?","answer":"剣で断ち切った","explanation":"「ほどく」という前提にとらわれず、剣でひと太刀。ルールの外に答えを見つける発想転換の古典的な故事。","coach_comment":"前提を疑う者が道を開く!","tags":["とんち","夜の一問","発想転換"],"summary":"ほどけない結び目を剣で断ち切ったゴルディアスの結び目の故事。発想転換(ラテラルシンキング)の古典。","illustration_scene":"夜の神殿風の広場の台座の上に太い縄の巨大な結び目が置かれ、たいまつの明かりに照らされている。結び目の真上に大きな「?」が浮かんでいる。剣は描かない。"}',
        '類型: 発想転換の古典的故事(ゴルディアスの結び目)。参照: https://en.wikipedia.org/wiki/Gordian_Knot (research3.md B-09 代替)。文面はオリジナルに書き下ろし(表現は書き直し済み)。', 1);

-- C12
INSERT INTO quiz_stock_items (set_id, quiz_type, difficulty, question_text, answer_text, content_fields, source_note, is_active)
VALUES ((SELECT id FROM batch_sets WHERE set_code = 'logic-training-1'), 'L1', 'deep',
        '1人の赤ん坊を、2人の女性が「私の子です」と譲らない。王は「では子を半分に分けよ」と命じた。すると本当の母親はどうした?',
        '「相手に渡して」と身を引いた',
        '{"hook":"3000年前の裁判らしいぞ!","hint":"本当の親の気持ちになるんだ!","question":"1人の赤ん坊を、2人の女性が「私の子です」と譲らない。王は「では子を半分に分けよ」と命じた。すると本当の母親はどうした?","answer":"「相手に渡して」と身を引いた","explanation":"本当の母親は、子の命を守るために自分が身を引いた。その反応こそが親の証だと、王は見抜いていた。","coach_comment":"答えは論理の先の愛だった…!","tags":["とんち","夜の一問","名裁き"],"summary":"「半分に分けよ」への反応で本当の母親を見抜くソロモンの審判。人の心を読む名裁きの古典。","illustration_scene":"夜の荘厳な広間の奥に玉座が淡い光に照らされて立ち、その手前のかごの中で1人の赤ん坊がすやすや眠っている。かごの前に2人の女性が立つ姿を後ろ姿のシルエットで描き、顔は描かない。赤ん坊の顔も見えない角度にする。そばに大きな「?」が浮かび、長い赤い絨毯が手前まで延びている。"}',
        '類型: 名裁きの古典説話(ソロモンの審判)。参照: https://en.wikipedia.org/wiki/Judgement_of_Solomon (research3.md B-08 代替)。文面はオリジナルに書き下ろし(表現は書き直し済み)。', 1);

-- C13
INSERT INTO quiz_stock_items (set_id, quiz_type, difficulty, question_text, answer_text, content_fields, source_note, is_active)
VALUES ((SELECT id FROM batch_sets WHERE set_code = 'logic-training-1'), 'L1', 'deep',
        'あなたはバスの運転手。始発で9人乗り、次の停留所で4人降りて2人乗り、その次で4人乗って1人降りた。さて、運転手の誕生日はいつ?',
        'あなたの誕生日',
        '{"hook":"深夜バス、発車するぞ!","hint":"問題文の最初を思い出すんだ!","question":"あなたはバスの運転手。始発で9人乗り、次の停留所で4人降りて2人乗り、その次で4人乗って1人降りた。さて、運転手の誕生日はいつ?","answer":"あなたの誕生日","explanation":"運転手は最初から「あなた」。乗り降りの人数は全部ただの目くらまし。1行目を覚えていた人だけが解ける。","coach_comment":"問題文の1行目、戻れたか?","tags":["ひっかけ","夜の一問","記憶力"],"summary":"乗降人数で目をくらませて「運転手=あなた」を忘れさせる定番ひっかけ(バスの運転手問題)。","illustration_scene":"夜のバス停に車内灯のついた路線バスが停まり、開いた前後のドアから複数の乗客が乗り降りしている。乗客は後ろ姿やシルエットで描き、顔は描かない。バスの真上に大きな「?」が浮かび、街灯が歩道を照らしている。"}',
        '類型: 定番ひっかけクイズ(あなたはバスの運転手。広く流布・作者不詳)。流布例: https://www.nazo2.net/ijiwaru/017.html (research3.md A-11)。人数・文面はオリジナルに書き下ろし(表現は書き直し済み)。', 1);

-- C14
INSERT INTO quiz_stock_items (set_id, quiz_type, difficulty, question_text, answer_text, content_fields, source_note, is_active)
VALUES ((SELECT id FROM batch_sets WHERE set_code = 'logic-training-1'), 'L1', 'deep',
        '若いときは背が高く、年を取るほど背が低くなっていく。最後には消えてしまうものは、なんだ?',
        'ろうそく',
        '{"hook":"今夜最後の一問","hint":"身を削って働くものだぞ!","question":"若いときは背が高く、年を取るほど背が低くなっていく。最後には消えてしまうものは、なんだ?","answer":"ろうそく","explanation":"火をともして働くほど、身を削って短くなっていく。一生を燃えて過ごす、ろうそくの姿のなぞなぞ。鉛筆と答えた君も鋭い!","coach_comment":"今日も燃え尽きるまでやったな","tags":["なぞなぞ","夜の一問","頭の体操"],"summary":"若いとき高く年を取ると低くなる=ろうそくという英語圏古典(Candle riddle)の定番なぞなぞ。","illustration_scene":"夜の子ども部屋の柱に背くらべの印が上へ上へと刻まれ、いちばん高い印の横に大きな「?」が浮かんでいる。柱のそばに小さな子どもと背の高い大人が並んで立ち、背の差が分かるように後ろ姿で描く(顔は描かない)。窓の外に月と夜空。ろうそくは描かない。"}',
        '類型: 擬人化なぞなぞ(英語圏古典 Candle riddle)。流布例: https://www.brainzilla.com/brain-teasers/riddles/B8MJ8rOD/im-tall-when-im-young-and-im-short-when-im-old-what-am-i/ (research3.md B-12)。文面はオリジナルに書き下ろし(表現は書き直し済み)。', 1);
