-- 2026-11-w2 問題ストック補充投入(夜の 7 問 C91〜C97。レビュー承認後に実行)
-- 生成元: content/quiz-stock/logic-training-1/2026-11-w2/stock_items.py(単一ソース)。適用先: ローカル MySQL / Aurora(acps)
-- set_id は set_code から解決するため両環境共通で実行できる。
-- content_key はスロット内の既存最大連番 + 1 を適用時に解決する(V007。両環境で同一値になる)。

-- C91
INSERT INTO quiz_stock_items (set_id, content_key, quiz_type, difficulty, question_text, answer_text, content_fields, source_note, is_active)
VALUES ((SELECT id FROM batch_sets WHERE set_code = 'logic-training-1'),
        (SELECT CONCAT('night-', LPAD(COALESCE(MAX(CAST(SUBSTRING_INDEX(t.content_key, '-', -1) AS UNSIGNED)), 0) + 1, 3, '0')) FROM (SELECT q.content_key FROM quiz_stock_items q JOIN batch_sets b ON b.id = q.set_id WHERE b.set_code = 'logic-training-1' AND q.content_key LIKE 'night-%') t),
        'L1', 'deep',
        '夜の駅に列車が定刻どおりすべりこんだ。ホームの人々は同じ姿勢のまま、だれひとり動かない。乗る人も降りる人もなく、列車はまた走り去った。何があった?',
        '鉄道模型のジオラマだった(ゲームやおもちゃも正解だぞ)',
        '{"hook":"だれも乗らない駅がある!","hint":"見ている位置を変えてみろ!","question":"夜の駅に列車が定刻どおりすべりこんだ。ホームの人々は同じ姿勢のまま、だれひとり動かない。乗る人も降りる人もなく、列車はまた走り去った。何があった?","answer":"鉄道模型のジオラマだった(ゲームやおもちゃも正解だぞ)","explanation":"駅も列車も人も、部屋の中に作られた鉄道模型だった。ホームの人は人形だから、列車が来ても同じ姿勢のまま動かない。","coach_comment":"視点を引けば全体が見える!","tags":["水平思考","夜の一問","状況パズル"],"summary":"夜の駅に列車が来てもホームの人々が同じ姿勢のまま動かず、だれも乗り降りしない理由を問う水平思考。鉄道模型のジオラマだった。場面の大きさの読み替え。","illustration_scene":"夜の駅のホームを低い目線で見た情景。明かりのついた列車がホームに入ってくる。コートや帽子の人々が後ろ姿で、間をあけて立っている。ホームの屋根に丸い照明、遠くに信号の明かりと星空。列車の上の夜空に大きな「?」。顔は描かない。「?」以外の文字は描かない。"}',
        '類型: 列車が来ても待つ客が動かない = 鉄道模型(作者不詳・英語圏の situation puzzle。1990 年代の rec.puzzles の一覧に収録)。流布例: https://www.djm.cc/rpa-output/logic/situation.puzzles.s ・ https://boards.straightdope.com/t/the-return-of-three-minute-mysteries/47654 (2026-11-12 に直接開いて確認)。文面はオリジナルに書き下ろし(表現は書き直し済み)。', 1);

-- C92
INSERT INTO quiz_stock_items (set_id, content_key, quiz_type, difficulty, question_text, answer_text, content_fields, source_note, is_active)
VALUES ((SELECT id FROM batch_sets WHERE set_code = 'logic-training-1'),
        (SELECT CONCAT('night-', LPAD(COALESCE(MAX(CAST(SUBSTRING_INDEX(t.content_key, '-', -1) AS UNSIGNED)), 0) + 1, 3, '0')) FROM (SELECT q.content_key FROM quiz_stock_items q JOIN batch_sets b ON b.id = q.set_id WHERE b.set_code = 'logic-training-1' AND q.content_key LIKE 'night-%') t),
        'L1', 'deep',
        '自分ではどう調べても区別できない薬AとBを、毎晩1錠ずつ飲む。最後のA2錠とB2錠が混ざってしまった。1錠も捨てず、人にも頼らずに、今夜も明日も正しく飲むには?',
        '4錠とも半分に割り、半分ずつ飲む(粉にして分けても正解だぞ)',
        '{"hook":"まちがえずに飲めるか!?","hint":"見分ける必要はないぞ!","question":"自分ではどう調べても区別できない薬AとBを、毎晩1錠ずつ飲む。最後のA2錠とB2錠が混ざってしまった。1錠も捨てず、人にも頼らずに、今夜も明日も正しく飲むには?","answer":"4錠とも半分に割り、半分ずつ飲む(粉にして分けても正解だぞ)","explanation":"4錠をどれも半分に割り、片方ずつを今夜飲めば、AもBも1錠分になる。残りの半分は明日の分。全部を粉にして2つに分けても同じだ。","coach_comment":"分からないなら分ければいい!","tags":["水平思考","夜の一問","発想転換"],"summary":"自分ではどう調べても区別できない薬 A・B の最後の 2 錠ずつが混ざったとき、捨てずに 2 晩とも 1 錠ずつ飲む方法を問う。4 錠とも半分に割り半分ずつ飲む(粉にして分けても可)。","illustration_scene":"夜の洗面台。ふちの小皿に、そっくり同じ白い丸い錠剤が4つのっている。手前に、ふたのあいた空の薬びんが2本と、水の入ったコップ。鏡には窓の月だけが映っている。小皿の上に大きな「?」。人物と「?」以外の文字は描かない。"}',
        '類型: 混ざった 2 種の錠剤を見分けずに正しく飲む(作者不詳・英語圏の定番。原型の「目の見えない人」の設定は外した)。流布例: https://loquiz.com/2024/09/16/20-famous-lateral-thinking-riddles-and-their-answer/ ・ https://www.geeksforgeeks.org/?p=217545 (2026-11-12 に直接開いて確認)。文面はオリジナルに書き下ろし(表現は書き直し済み)。', 1);

-- C93
INSERT INTO quiz_stock_items (set_id, content_key, quiz_type, difficulty, question_text, answer_text, content_fields, source_note, is_active)
VALUES ((SELECT id FROM batch_sets WHERE set_code = 'logic-training-1'),
        (SELECT CONCAT('night-', LPAD(COALESCE(MAX(CAST(SUBSTRING_INDEX(t.content_key, '-', -1) AS UNSIGNED)), 0) + 1, 3, '0')) FROM (SELECT q.content_key FROM quiz_stock_items q JOIN batch_sets b ON b.id = q.set_id WHERE b.set_code = 'logic-training-1' AND q.content_key LIKE 'night-%') t),
        'L1', 'deep',
        '橋の重さ制限とぴったり同じ重さのトラックが、長い橋を渡りはじめた。真ん中で屋根に小鳥が1羽とまった。荷物も人もそのままなのに、制限は超えていない。なぜ?',
        '走った分だけ燃料が減り、軽くなっていた',
        '{"hook":"鳥1羽で橋が落ちる!?","hint":"渡りはじめと今では何がちがう?","question":"橋の重さ制限とぴったり同じ重さのトラックが、長い橋を渡りはじめた。真ん中で屋根に小鳥が1羽とまった。荷物も人もそのままなのに、制限は超えていない。なぜ?","answer":"走った分だけ燃料が減り、軽くなっていた","explanation":"トラックは走るあいだ燃料を使いつづける。長い橋の真ん中まで来るころには、小鳥1羽の重さよりも多くの燃料が減って、車は軽くなっている。","coach_comment":"減るものにも目を向けろ!","tags":["水平思考","夜の一問","ひっかけ"],"summary":"重さ制限ぴったりのトラックが橋の真ん中で小鳥にとまられても制限を超えない理由を問う。走った分だけ燃料が減って軽くなっていた。答えの対象は問題文に出ない。","illustration_scene":"夜の長いつり橋を、荷台に木箱を山積みにしたトラックが走っている。橋のたもとに、文字のない丸い標識。屋根の上へ小鳥が1羽、とまろうと舞いおりてくる。橋の下は月の映る川、遠くに町の明かり。トラックの上の夜空に大きな「?」。運転席の中と人物は描かない。「?」以外の文字は描かない。"}',
        '類型: 制限ぴったりのトラックに鳥がとまっても平気 = 燃料が減っている(作者不詳・英語圏の定番)。流布例: https://www.riddles.com/9981 ・ https://riddlesbrainteasers.com/?p=122 (2026-11-12 に直接開いて確認)。文面はオリジナルに書き下ろし(表現は書き直し済み)。', 1);

-- C94
INSERT INTO quiz_stock_items (set_id, content_key, quiz_type, difficulty, question_text, answer_text, content_fields, source_note, is_active)
VALUES ((SELECT id FROM batch_sets WHERE set_code = 'logic-training-1'),
        (SELECT CONCAT('night-', LPAD(COALESCE(MAX(CAST(SUBSTRING_INDEX(t.content_key, '-', -1) AS UNSIGNED)), 0) + 1, 3, '0')) FROM (SELECT q.content_key FROM quiz_stock_items q JOIN batch_sets b ON b.id = q.set_id WHERE b.set_code = 'logic-training-1' AND q.content_key LIKE 'night-%') t),
        'L1', 'deep',
        '見た目がまったく同じ鉄の棒が2本。片方だけが磁石だ。ほかの物は何も使わず、2本だけで、どちらが磁石かを見分けるには?',
        '片方の端を、もう片方の真ん中に当てる',
        '{"hook":"くっつくだけでは分からん!","hint":"当て方を工夫してみろ!","question":"見た目がまったく同じ鉄の棒が2本。片方だけが磁石だ。ほかの物は何も使わず、2本だけで、どちらが磁石かを見分けるには?","answer":"片方の端を、もう片方の真ん中に当てる","explanation":"棒磁石は両端が強く真ん中は弱い。端を相手の真ん中に当て、つけば当てた棒、つかなければ当てられた棒が磁石。指先で釣り合わせ南北を向くか見る手もある。","coach_comment":"弱点を知る者が勝つ!","tags":["論理パズル","夜の一問","発想転換"],"summary":"同じ見た目の鉄の棒 2 本のうち磁石を道具なしで見分ける方法を問う。片方の端をもう片方の真ん中に当てる(棒磁石の真ん中はほとんど引きつけない)。指先で釣り合わせ南北を向くかを見る別解も可。","illustration_scene":"夜の作業机。ランプの明かりの下に、そっくり同じ銀色の鉄の棒が2本、少し離して平行に置いてある。机の奥に本立てとマグカップ、窓の外に三日月。2本の棒の間に大きな「?」。人物と「?」以外の文字は描かない。"}',
        '類型: 2 本の棒のどちらが磁石かを T 字に当てて見分ける(作者不詳・理科パズルの定番)。流布例: https://sigh.github.io/puzzles/find-the-magnet ・ https://van.physics.illinois.edu/ask/listing/16626 (2026-11-12 に直接開いて確認。T 字の解法は前者、後者は同じ問いで説明の言い方が別)。文面はオリジナルに書き下ろし(表現は書き直し済み)。', 1);

-- C95
INSERT INTO quiz_stock_items (set_id, content_key, quiz_type, difficulty, question_text, answer_text, content_fields, source_note, is_active)
VALUES ((SELECT id FROM batch_sets WHERE set_code = 'logic-training-1'),
        (SELECT CONCAT('night-', LPAD(COALESCE(MAX(CAST(SUBSTRING_INDEX(t.content_key, '-', -1) AS UNSIGNED)), 0) + 1, 3, '0')) FROM (SELECT q.content_key FROM quiz_stock_items q JOIN batch_sets b ON b.id = q.set_id WHERE b.set_code = 'logic-training-1' AND q.content_key LIKE 'night-%') t),
        'L1', 'deep',
        '男が持ちものを1つ手放すたびに、手にさげたかばんが重くなっていく。かばんの中身は何も変わっていない。なぜ?',
        '手放したのは、かばんに結んだ風船だった',
        '{"hook":"捨てるほど重くなる!?","hint":"重さは中身だけで決まるか?","question":"男が持ちものを1つ手放すたびに、手にさげたかばんが重くなっていく。かばんの中身は何も変わっていない。なぜ?","answer":"手放したのは、かばんに結んだ風船だった","explanation":"かばんには、空気より軽いガスの入った風船がいくつも結んであった。風船が上へ引く分だけ軽かったので、1つ手放すたびに手にかかる重さが増えた。","coach_comment":"軽さの正体を見抜いたな!","tags":["水平思考","夜の一問","状況パズル"],"summary":"持ちものを1つ手放すたびに手にさげたかばんが重くなる理由を問う水平思考。手放したのはかばんに結んだ浮く風船で、上へ引く力が減った。中身は変わらない。","illustration_scene":"夜の石だたみの坂道。街灯の下で、後ろ姿の男が、ふくらんだ大きな革のかばんを両手でさげ、重そうに腰を落としている。道ばたにベンチと、明かりのついた家々、広い夜空に星。かばんの上に大きな「?」。顔は描かない。「?」以外の文字は描かない。"}',
        '類型: 手放すたびに荷物が重くなる = 浮く風船を手放していた(日常の矛盾が 1 つの事実で解ける水平思考)。流布例: https://ichigo-drill.jp/quiz-horizontal (2026-10-29 に直接開いて確認)。要注意: 確認できたのは1ドメインのみ(同サイト独自の作の可能性あり)。文面はオリジナルに書き下ろし(表現は書き直し済み)。', 1);

-- C96
INSERT INTO quiz_stock_items (set_id, content_key, quiz_type, difficulty, question_text, answer_text, content_fields, source_note, is_active)
VALUES ((SELECT id FROM batch_sets WHERE set_code = 'logic-training-1'),
        (SELECT CONCAT('night-', LPAD(COALESCE(MAX(CAST(SUBSTRING_INDEX(t.content_key, '-', -1) AS UNSIGNED)), 0) + 1, 3, '0')) FROM (SELECT q.content_key FROM quiz_stock_items q JOIN batch_sets b ON b.id = q.set_id WHERE b.set_code = 'logic-training-1' AND q.content_key LIKE 'night-%') t),
        'L1', 'deep',
        '深夜に帰宅すると、柱時計が1回鳴った。30分後も1回、次も1回、その次も1回。ちょうど3時なら3回、3時半なら1回鳴る時計だ。帰宅したのは何時?',
        '12時(12回の最後の1回を聞いた)',
        '{"hook":"耳だけで時刻を当てろ!","hint":"ありえる時刻を全部試してみろ!","question":"深夜に帰宅すると、柱時計が1回鳴った。30分後も1回、次も1回、その次も1回。ちょうど3時なら3回、3時半なら1回鳴る時計だ。帰宅したのは何時?","answer":"12時(12回の最後の1回を聞いた)","explanation":"1回だけ鳴るのは30分と1時。12時半・1時・1時半で3回つづく。4回つづくには、最初の1回が、12時を打つ12回の最後の1回でなければならない。","coach_comment":"最後の一打まで聞きのがすな!","tags":["論理パズル","夜の一問","推理"],"summary":"帰宅時から30分おきに柱時計が1回ずつ4度鳴った。毎時ちょうどは時の数・30分は1回鳴る時計で帰宅時刻を問う。12時(12回の最後の1打を聞き、12時半・1時・1時半とつづく)。","illustration_scene":"深夜の玄関。暗い廊下の奥に、振り子のついた古い柱時計が立っている。文字盤は影になっていて針も数字も見えない。手前に、脱ぎかけの革靴とかばん、壁に小さな明かり。時計の上に大きな「?」。人物と、「?」以外の文字・数字は描かない。"}',
        '類型: 1 回の時報が続いたことから帰宅時刻を推理する(作者不詳。学校の宿題として出た同型〔1 回が 5 連続〕が掲示板に流布)。流布例: https://singletrackworld.com/forum/off-topic/help-a-10-year-olds-maths-question/ (2026-11-12 に直接開いて確認)。要注意: 確認できたのは1ドメインのみ。4 連続に変えて答えを一意にした。文面はオリジナルに書き下ろし(表現は書き直し済み)。', 1);

-- C97
INSERT INTO quiz_stock_items (set_id, content_key, quiz_type, difficulty, question_text, answer_text, content_fields, source_note, is_active)
VALUES ((SELECT id FROM batch_sets WHERE set_code = 'logic-training-1'),
        (SELECT CONCAT('night-', LPAD(COALESCE(MAX(CAST(SUBSTRING_INDEX(t.content_key, '-', -1) AS UNSIGNED)), 0) + 1, 3, '0')) FROM (SELECT q.content_key FROM quiz_stock_items q JOIN batch_sets b ON b.id = q.set_id WHERE b.set_code = 'logic-training-1' AND q.content_key LIKE 'night-%') t),
        'L1', 'deep',
        '同じ大きさ・同じ重さの金属の球が2個。片方は中が空洞だが、見ても、たたいても区別がつかない。傷つけずに、板1枚だけで空洞の球を見つけるには?',
        '板を坂にして同時に転がす。遅い方が空洞',
        '{"hook":"割らずに中身を当てろ!","hint":"板の使い方を考えろ!","question":"同じ大きさ・同じ重さの金属の球が2個。片方は中が空洞だが、見ても、たたいても区別がつかない。傷つけずに、板1枚だけで空洞の球を見つけるには?","answer":"板を坂にして同時に転がす。遅い方が空洞","explanation":"板を坂にして2個を同時に転がす。空洞の球は重さが外側にかたよっていて回りにくく、転がるのが遅い。あとから着いたほうが空洞だ。","coach_comment":"中身は動きに表れるぞ!","tags":["論理パズル","夜の一問","発想転換"],"summary":"同じ大きさ・重さの球 2 個から空洞のほうを板 1 枚で見つける方法を問う。板を坂にして同時に転がすと、重さが外側に寄った空洞の球のほうが遅い。","illustration_scene":"夜の工房の作業台。ランプの明かりの下に、同じ大きさの赤い金属の球が2個ならび、その手前に長い木の板が1枚、平らに置いてある。奥の棚に本とびん、窓の外に星。2個の球の上に大きな「?」。人物と「?」以外の文字は描かない。"}',
        '類型: 同じ大きさ・重さの球から空洞のほうを坂で見分ける(作者不詳・rec.puzzles のアーカイブに収録の物理パズル)。流布例: https://www.djm.cc/rpa-output/physics/spheres.p ・ https://van.physics.illinois.edu/ask/listing/319 (2026-11-12 に直接開いて確認。後者は原理の説明)。文面はオリジナルに書き下ろし(表現は書き直し済み)。', 1);
