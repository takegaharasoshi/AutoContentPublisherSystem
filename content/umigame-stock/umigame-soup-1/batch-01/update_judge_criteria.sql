-- batch-01 既存 14 問の正解基準と U27 の事実・要点の更新（V014 適用後に実行）
-- 生成元: content/umigame-stock/umigame-soup-1/batch-01/stock_items.py（単一ソース）
-- 適用先: ローカル MySQL / Aurora（acps）。set_code と content_key で対象を特定する。
-- 出題済み行がある場合は umigame_items のスナップショット値も更新する。

-- 001-faint-shadow: 影が薄いと言われて喜ぶ男
UPDATE umigame_stock_items s
JOIN batch_sets b ON b.id = s.set_id
SET s.judge_criteria = '{"points":[{"hit":"影が病気の影（レントゲン等の検査画像）だと言うか、影が薄くなった＝病気が良くなったと結びつけている。「写真の影」「体の中の影」だけでは当てたにしない","touch":"影が体の中・病院の検査・体を写した写真のどれかに関係すると述べている（何の影かまでは言わない）"},{"hit":"影が薄くなった＝病気が良くなった（回復・快方・治ってきた）と結びつけている。「良い知らせ」だけでは当てたにしない","touch":"検査や診察で良い結果を聞いた、体の具合が悪くないと分かった、と述べている（病気の回復とまでは言わない）"}],"errors":["言った相手は医者ではない（友人・近所の人など）","病気が悪くなった・男が入院していた"]}'
WHERE b.set_code = 'umigame-soup-1' AND s.content_key = '001-faint-shadow';

UPDATE umigame_items i
JOIN batch_sets b ON b.id = i.set_id
SET i.judge_criteria = '{"points":[{"hit":"影が病気の影（レントゲン等の検査画像）だと言うか、影が薄くなった＝病気が良くなったと結びつけている。「写真の影」「体の中の影」だけでは当てたにしない","touch":"影が体の中・病院の検査・体を写した写真のどれかに関係すると述べている（何の影かまでは言わない）"},{"hit":"影が薄くなった＝病気が良くなった（回復・快方・治ってきた）と結びつけている。「良い知らせ」だけでは当てたにしない","touch":"検査や診察で良い結果を聞いた、体の具合が悪くないと分かった、と述べている（病気の回復とまでは言わない）"}],"errors":["言った相手は医者ではない（友人・近所の人など）","病気が悪くなった・男が入院していた"]}'
WHERE b.set_code = 'umigame-soup-1' AND i.content_key = '001-faint-shadow';

-- 003-silent-musicians: 階段に並ぶ、音を出さない男たち
UPDATE umigame_stock_items s
JOIN batch_sets b ON b.id = s.set_id
SET s.judge_criteria = '{"points":[{"hit":"ひな人形・五人囃子・ひな祭りの段飾りの人形など、ひな祭りの人形だと特定している。「人形」だけでは当てたにしない","touch":"男たちは人形（ひな祭りと結びつけない人形・フィギュア）だと述べている。銅像・絵・ロボットは触れたにしない"}],"errors":["人形の楽器から本当に音が鳴る","男たちは本物の人間や楽団である"]}'
WHERE b.set_code = 'umigame-soup-1' AND s.content_key = '003-silent-musicians';

UPDATE umigame_items i
JOIN batch_sets b ON b.id = i.set_id
SET i.judge_criteria = '{"points":[{"hit":"ひな人形・五人囃子・ひな祭りの段飾りの人形など、ひな祭りの人形だと特定している。「人形」だけでは当てたにしない","touch":"男たちは人形（ひな祭りと結びつけない人形・フィギュア）だと述べている。銅像・絵・ロボットは触れたにしない"}],"errors":["人形の楽器から本当に音が鳴る","男たちは本物の人間や楽団である"]}'
WHERE b.set_code = 'umigame-soup-1' AND i.content_key = '003-silent-musicians';

-- 004-fifty-year-letter: 会ったことのない男の子からの手紙
UPDATE umigame_stock_items s
JOIN batch_sets b ON b.id = s.set_id
SET s.judge_criteria = '{"points":[{"hit":"手紙を書いた男の子は男自身（子どもの頃・昔の男）だと言っている。手紙が男の自分宛てだったと言うのも当てたに含める","touch":"書いた子は今は大人になっている、男と同じ学校の子だった、など書いた子が男の過去と重なる方向を述べている"},{"hit":"タイムカプセル、または将来読むために学校で埋めた・しまった企画から出てきたと言っている。「古い手紙」だけでは当てたにしない","touch":"手紙が何十年も保管されてから渡された・昔の学校の手紙が出てきた、と述べている。郵便の遅配・紛失は触れたにしない"}],"errors":["郵便が遅れて何十年後に届いた","書いた子は男の息子・孫・教え子など別人"]}'
WHERE b.set_code = 'umigame-soup-1' AND s.content_key = '004-fifty-year-letter';

UPDATE umigame_items i
JOIN batch_sets b ON b.id = i.set_id
SET i.judge_criteria = '{"points":[{"hit":"手紙を書いた男の子は男自身（子どもの頃・昔の男）だと言っている。手紙が男の自分宛てだったと言うのも当てたに含める","touch":"書いた子は今は大人になっている、男と同じ学校の子だった、など書いた子が男の過去と重なる方向を述べている"},{"hit":"タイムカプセル、または将来読むために学校で埋めた・しまった企画から出てきたと言っている。「古い手紙」だけでは当てたにしない","touch":"手紙が何十年も保管されてから渡された・昔の学校の手紙が出てきた、と述べている。郵便の遅配・紛失は触れたにしない"}],"errors":["郵便が遅れて何十年後に届いた","書いた子は男の息子・孫・教え子など別人"]}'
WHERE b.set_code = 'umigame-soup-1' AND i.content_key = '004-fifty-year-letter';

-- 005-bakers-egg: 割らない卵を自慢するパン屋
UPDATE umigame_stock_items s
JOIN batch_sets b ON b.id = s.set_id
SET s.judge_criteria = '{"points":[{"hit":"卵はパン職人の見習い（修業中の若者・弟子・職人の卵）だと言っている。「卵は人のこと」だけでは当てたにしない","touch":"卵は食べ物ではなく人や従業員を指す呼び名・たとえだと述べている（見習いとまでは言わない）"},{"hit":"その見習い（育てた職人）が、今は店のおいしいパンを焼いている・作っていると言っている","touch":"その人が店で働いている・パン作りを手伝っていると述べている（パンを焼く本人だとまでは言わない）"}],"errors":["主人はパン作りを教えていない（独学）","卵は主人の子ども・孫","卵をパンの材料に使っている"]}'
WHERE b.set_code = 'umigame-soup-1' AND s.content_key = '005-bakers-egg';

UPDATE umigame_items i
JOIN batch_sets b ON b.id = i.set_id
SET i.judge_criteria = '{"points":[{"hit":"卵はパン職人の見習い（修業中の若者・弟子・職人の卵）だと言っている。「卵は人のこと」だけでは当てたにしない","touch":"卵は食べ物ではなく人や従業員を指す呼び名・たとえだと述べている（見習いとまでは言わない）"},{"hit":"その見習い（育てた職人）が、今は店のおいしいパンを焼いている・作っていると言っている","touch":"その人が店で働いている・パン作りを手伝っていると述べている（パンを焼く本人だとまでは言わない）"}],"errors":["主人はパン作りを教えていない（独学）","卵は主人の子ども・孫","卵をパンの材料に使っている"]}'
WHERE b.set_code = 'umigame-soup-1' AND i.content_key = '005-bakers-egg';

-- 006-frozen-tag: 助けに来た女も凍りついた
UPDATE umigame_stock_items s
JOIN batch_sets b ON b.id = s.set_id
SET s.judge_criteria = '{"points":[{"hit":"氷鬼（凍り鬼。鬼にタッチされると動けず仲間のタッチで動ける鬼ごっこ）をしていたと言っている。「鬼ごっこ」だけでは当てたにしない","touch":"鬼ごっこ・だるまさんがころんだなど、子どもとの遊びのルールで動けないと述べている（氷鬼とまでは言わない）"}],"errors":["本当に寒い場所で凍えていた","女は助けるふりで鬼の側だった"]}'
WHERE b.set_code = 'umigame-soup-1' AND s.content_key = '006-frozen-tag';

UPDATE umigame_items i
JOIN batch_sets b ON b.id = i.set_id
SET i.judge_criteria = '{"points":[{"hit":"氷鬼（凍り鬼。鬼にタッチされると動けず仲間のタッチで動ける鬼ごっこ）をしていたと言っている。「鬼ごっこ」だけでは当てたにしない","touch":"鬼ごっこ・だるまさんがころんだなど、子どもとの遊びのルールで動けないと述べている（氷鬼とまでは言わない）"}],"errors":["本当に寒い場所で凍えていた","女は助けるふりで鬼の側だった"]}'
WHERE b.set_code = 'umigame-soup-1' AND i.content_key = '006-frozen-tag';

-- 007-blank-letter: 白紙に戻った約束
UPDATE umigame_stock_items s
JOIN batch_sets b ON b.id = s.set_id
SET s.judge_criteria = '{"points":[{"hit":"約束を書いた紙（手紙）の文字が消えて、紙が白紙になったと言っている。紙が破れた・なくなっただけでは当てたにしない","touch":"約束を書いた紙の文字が読めなくなった（にじんだ・薄れた・濡れた）と述べている。破れた・燃えたは触れたにしない"},{"hit":"消せるボールペン（熱やこすりで消えるインクのペン）で書かれていたと言っている。「インクが薄かった」では当てたにしない","touch":"書いた道具やインクに特徴があって、水や熱で文字が消えたと述べている（消せるペンとまでは言わない）"}],"errors":["誰かが破った・いたずらで消した","2人がけんかして約束を取り消した"]}'
WHERE b.set_code = 'umigame-soup-1' AND s.content_key = '007-blank-letter';

UPDATE umigame_items i
JOIN batch_sets b ON b.id = i.set_id
SET i.judge_criteria = '{"points":[{"hit":"約束を書いた紙（手紙）の文字が消えて、紙が白紙になったと言っている。紙が破れた・なくなっただけでは当てたにしない","touch":"約束を書いた紙の文字が読めなくなった（にじんだ・薄れた・濡れた）と述べている。破れた・燃えたは触れたにしない"},{"hit":"消せるボールペン（熱やこすりで消えるインクのペン）で書かれていたと言っている。「インクが薄かった」では当てたにしない","touch":"書いた道具やインクに特徴があって、水や熱で文字が消えたと述べている（消せるペンとまでは言わない）"}],"errors":["誰かが破った・いたずらで消した","2人がけんかして約束を取り消した"]}'
WHERE b.set_code = 'umigame-soup-1' AND i.content_key = '007-blank-letter';

-- 008-who-made-the-mistake: 完璧な演奏に「あ、間違えた」
UPDATE umigame_stock_items s
JOIN batch_sets b ON b.id = s.set_id
SET s.judge_criteria = '{"points":[{"hit":"男は娘（家族の子ども）が毎日の練習で間違えて弾くのを聞いて、その間違いごと曲を覚えていたと言っている","touch":"男が覚えていた曲（覚え方）のほうが間違っていた、誰かの弾き間違いで覚えた、と述べている。別の編曲は触れたにしない"}],"errors":["ピアニストが本当に音を外した","演奏会で弾いていたのは娘","別の編曲・別の版の楽譜だった"]}'
WHERE b.set_code = 'umigame-soup-1' AND s.content_key = '008-who-made-the-mistake';

UPDATE umigame_items i
JOIN batch_sets b ON b.id = i.set_id
SET i.judge_criteria = '{"points":[{"hit":"男は娘（家族の子ども）が毎日の練習で間違えて弾くのを聞いて、その間違いごと曲を覚えていたと言っている","touch":"男が覚えていた曲（覚え方）のほうが間違っていた、誰かの弾き間違いで覚えた、と述べている。別の編曲は触れたにしない"}],"errors":["ピアニストが本当に音を外した","演奏会で弾いていたのは娘","別の編曲・別の版の楽譜だった"]}'
WHERE b.set_code = 'umigame-soup-1' AND i.content_key = '008-who-made-the-mistake';

-- 009-year-late-verdict: 庭のすみに実ったすいか
UPDATE umigame_stock_items s
JOIN batch_sets b ON b.id = s.set_id
SET s.judge_criteria = '{"points":[{"hit":"兄弟が去年すいかの種飛ばしで勝負したと言っている。「すいかを食べた」だけでは当てたにしない","touch":"兄弟が去年すいかを食べながら何かで競った、種で遊んだ、と述べている。すいかを育てる競争は触れたにしない"},{"hit":"庭の奥のすいかは弟が飛ばした（吐いた）種から育ったと言っている","touch":"すいかは誰も植えておらず、落ちた・飛んだ種から自然に生えたと述べている（弟の種とまでは言わない）"}],"errors":["弟は勝負に負けていて兄が譲った","誰かがすいかを植えて育てた"]}'
WHERE b.set_code = 'umigame-soup-1' AND s.content_key = '009-year-late-verdict';

UPDATE umigame_items i
JOIN batch_sets b ON b.id = i.set_id
SET i.judge_criteria = '{"points":[{"hit":"兄弟が去年すいかの種飛ばしで勝負したと言っている。「すいかを食べた」だけでは当てたにしない","touch":"兄弟が去年すいかを食べながら何かで競った、種で遊んだ、と述べている。すいかを育てる競争は触れたにしない"},{"hit":"庭の奥のすいかは弟が飛ばした（吐いた）種から育ったと言っている","touch":"すいかは誰も植えておらず、落ちた・飛んだ種から自然に生えたと述べている（弟の種とまでは言わない）"}],"errors":["弟は勝負に負けていて兄が譲った","誰かがすいかを植えて育てた"]}'
WHERE b.set_code = 'umigame-soup-1' AND i.content_key = '009-year-late-verdict';

-- 010-two-hour-dentist: 2時間かけて通う歯医者
UPDATE umigame_stock_items s
JOIN batch_sets b ON b.id = s.set_id
SET s.judge_criteria = '{"points":[{"hit":"歯医者の建物は男が子どもの頃に住んでいた家（生家・実家）を改装したものだと言っている","touch":"歯医者の建物が男の思い出の場所・昔関わった場所だと述べている（育った家とまでは言わない）。人に会いに行くは触れたにしない"}],"errors":["先生や受付が男の知り合い・家族","柱の傷は歯医者を開いた人が刻んだ"]}'
WHERE b.set_code = 'umigame-soup-1' AND s.content_key = '010-two-hour-dentist';

UPDATE umigame_items i
JOIN batch_sets b ON b.id = i.set_id
SET i.judge_criteria = '{"points":[{"hit":"歯医者の建物は男が子どもの頃に住んでいた家（生家・実家）を改装したものだと言っている","touch":"歯医者の建物が男の思い出の場所・昔関わった場所だと述べている（育った家とまでは言わない）。人に会いに行くは触れたにしない"}],"errors":["先生や受付が男の知り合い・家族","柱の傷は歯医者を開いた人が刻んだ"]}'
WHERE b.set_code = 'umigame-soup-1' AND i.content_key = '010-two-hour-dentist';

-- 012-early-morning-run: 早く走った朝
UPDATE umigame_stock_items s
JOIN batch_sets b ON b.id = s.set_id
SET s.judge_criteria = '{"points":[{"hit":"子どもたちは毎朝決まった時刻に通る男を見て、家を出る合図（時計代わり）にしていたと言っている","touch":"男が通る時刻と子どもたちが家を出る時刻に関係があると述べている（合図にしていたとまでは言わない）"}],"errors":["その朝、男がいつもより遅く通った","男が子どもたちに声をかけた・合図した"]}'
WHERE b.set_code = 'umigame-soup-1' AND s.content_key = '012-early-morning-run';

UPDATE umigame_items i
JOIN batch_sets b ON b.id = i.set_id
SET i.judge_criteria = '{"points":[{"hit":"子どもたちは毎朝決まった時刻に通る男を見て、家を出る合図（時計代わり）にしていたと言っている","touch":"男が通る時刻と子どもたちが家を出る時刻に関係があると述べている（合図にしていたとまでは言わない）"}],"errors":["その朝、男がいつもより遅く通った","男が子どもたちに声をかけた・合図した"]}'
WHERE b.set_code = 'umigame-soup-1' AND i.content_key = '012-early-morning-run';

-- 013-fifty-five-year-nengajo: 55年目の年賀状
UPDATE umigame_stock_items s
JOIN batch_sets b ON b.id = s.set_id
SET s.judge_criteria = '{"points":[{"hit":"2人が毎年の年賀状で将棋を1手ずつ指し続けていたと言っている。「年賀状で勝負」だけでは当てたにしない","touch":"年賀状で何かの勝負・対局を続けていたと述べている（将棋と言わない・囲碁やチェスと言うのを含む）"}],"errors":["2人は毎年会う・電話で指していた","お金や物を賭けていた"]}'
WHERE b.set_code = 'umigame-soup-1' AND s.content_key = '013-fifty-five-year-nengajo';

UPDATE umigame_items i
JOIN batch_sets b ON b.id = i.set_id
SET i.judge_criteria = '{"points":[{"hit":"2人が毎年の年賀状で将棋を1手ずつ指し続けていたと言っている。「年賀状で勝負」だけでは当てたにしない","touch":"年賀状で何かの勝負・対局を続けていたと述べている（将棋と言わない・囲碁やチェスと言うのを含む）"}],"errors":["2人は毎年会う・電話で指していた","お金や物を賭けていた"]}'
WHERE b.set_code = 'umigame-soup-1' AND i.content_key = '013-fifty-five-year-nengajo';

-- 014-kind-interpreter: 日本語を覚えた日から
UPDATE umigame_stock_items s
JOIN batch_sets b ON b.id = s.set_id
SET s.judge_criteria = '{"points":[{"hit":"通訳していた息子（2人の間の子ども）が、2人の言葉を良い言葉に作り替えて伝えていたと言っている。「誰か」だけでは当てたにしない","touch":"誰かが2人の言葉を訳して伝えていて、その伝え方に原因があると述べている。悪口を吹き込んだ人は触れたにしない"}],"errors":["夫が通訳していた","近所の人などが悪口を吹き込んだ"]}'
WHERE b.set_code = 'umigame-soup-1' AND s.content_key = '014-kind-interpreter';

UPDATE umigame_items i
JOIN batch_sets b ON b.id = i.set_id
SET i.judge_criteria = '{"points":[{"hit":"通訳していた息子（2人の間の子ども）が、2人の言葉を良い言葉に作り替えて伝えていたと言っている。「誰か」だけでは当てたにしない","touch":"誰かが2人の言葉を訳して伝えていて、その伝え方に原因があると述べている。悪口を吹き込んだ人は触れたにしない"}],"errors":["夫が通訳していた","近所の人などが悪口を吹き込んだ"]}'
WHERE b.set_code = 'umigame-soup-1' AND i.content_key = '014-kind-interpreter';

-- 015-unlicensed-driver: 免許のない男のドライブ
UPDATE umigame_stock_items s
JOIN batch_sets b ON b.id = s.set_id
SET s.judge_criteria = '{"points":[{"hit":"人生ゲームの車の駒だと言うか、すごろくの車の駒に家族のピンを乗せて進めると言っている。「すごろくの駒」だけでは当てたにしない","touch":"車がボードゲーム・すごろく・おもちゃの駒だと述べている（家族がピンだとまでは言わない）。ラジコン・遊園地は触れたにしない"}],"errors":["家族は嫌々付き合っている","ラジコン・テレビゲーム・遊園地の車"]}',
    s.fact_sheet = '["男は運転免許を一度も取ったことがない（取り消されたのでも、取り上げられたのでもない）","男は決まりや法律を破っていない。警察に注意されることもない","車を動かしているのは男自身。自動運転の車ではなく、妻や他の人が代わりに運転しているのでもない","男の車は本物の自動車ではない。男は車の中に座ってハンドルを握る「運転」はしておらず、車の外から動かしている","車が何で、車に乗っている妻と子どもたちが何なのかは、この問題の答えの核心である（正解宣言のとき以外は補足で言わない）","車に乗っている妻と子どもたちは、本物の人間ではない。誰もけがをせず、危ないこともない","車が走るのは家の中。私有地・サーキット・遊園地・ゲームセンターではない","テレビやスマホの画面、コントローラーは使わない。ラジコンでもない","休みの日に本物の家族みんなで集まり、順番に楽しんでいる。家族が楽しそうなのはそのためである","車が一度にどこまで進むかは、男が決めるのではなく毎回変わる","車が走る道の途中では、仕事・結婚・家を買うといった人生の出来事が起きる","男の年齢・職業・車の色・家族の人数は問題に関係ない"]',
    s.core_points = '["車は人生ゲームの駒、家族はピン"]'
WHERE b.set_code = 'umigame-soup-1' AND s.content_key = '015-unlicensed-driver';

UPDATE umigame_items i
JOIN batch_sets b ON b.id = i.set_id
SET i.judge_criteria = '{"points":[{"hit":"人生ゲームの車の駒だと言うか、すごろくの車の駒に家族のピンを乗せて進めると言っている。「すごろくの駒」だけでは当てたにしない","touch":"車がボードゲーム・すごろく・おもちゃの駒だと述べている（家族がピンだとまでは言わない）。ラジコン・遊園地は触れたにしない"}],"errors":["家族は嫌々付き合っている","ラジコン・テレビゲーム・遊園地の車"]}',
    i.fact_sheet = '["男は運転免許を一度も取ったことがない（取り消されたのでも、取り上げられたのでもない）","男は決まりや法律を破っていない。警察に注意されることもない","車を動かしているのは男自身。自動運転の車ではなく、妻や他の人が代わりに運転しているのでもない","男の車は本物の自動車ではない。男は車の中に座ってハンドルを握る「運転」はしておらず、車の外から動かしている","車が何で、車に乗っている妻と子どもたちが何なのかは、この問題の答えの核心である（正解宣言のとき以外は補足で言わない）","車に乗っている妻と子どもたちは、本物の人間ではない。誰もけがをせず、危ないこともない","車が走るのは家の中。私有地・サーキット・遊園地・ゲームセンターではない","テレビやスマホの画面、コントローラーは使わない。ラジコンでもない","休みの日に本物の家族みんなで集まり、順番に楽しんでいる。家族が楽しそうなのはそのためである","車が一度にどこまで進むかは、男が決めるのではなく毎回変わる","車が走る道の途中では、仕事・結婚・家を買うといった人生の出来事が起きる","男の年齢・職業・車の色・家族の人数は問題に関係ない"]',
    i.core_points = '["車は人生ゲームの駒、家族はピン"]'
WHERE b.set_code = 'umigame-soup-1' AND i.content_key = '015-unlicensed-driver';

-- 016-umigame-soup: 本物のウミガメのスープ
UPDATE umigame_stock_items s
JOIN batch_sets b ON b.id = s.set_id
SET s.judge_criteria = '{"points":[{"hit":"男は昔（遭難・漂流中など）ウミガメのスープだと言われて、別の物のスープを飲んだことがあると言っている","touch":"男は以前にもウミガメのスープ（と呼ばれる物）を飲んだことがあり、今日の味と違った、と述べている"},{"hit":"前に飲んだスープは仲間（亡くなった人間）の肉だったと言っている","touch":"前のスープの材料はウミガメではない口にしてはいけない物だったと述べている（人の肉とまでは言わない）"}],"errors":["仲間は全員助かった","今日のスープが偽物だった"]}'
WHERE b.set_code = 'umigame-soup-1' AND s.content_key = '016-umigame-soup';

UPDATE umigame_items i
JOIN batch_sets b ON b.id = i.set_id
SET i.judge_criteria = '{"points":[{"hit":"男は昔（遭難・漂流中など）ウミガメのスープだと言われて、別の物のスープを飲んだことがあると言っている","touch":"男は以前にもウミガメのスープ（と呼ばれる物）を飲んだことがあり、今日の味と違った、と述べている"},{"hit":"前に飲んだスープは仲間（亡くなった人間）の肉だったと言っている","touch":"前のスープの材料はウミガメではない口にしてはいけない物だったと述べている（人の肉とまでは言わない）"}],"errors":["仲間は全員助かった","今日のスープが偽物だった"]}'
WHERE b.set_code = 'umigame-soup-1' AND i.content_key = '016-umigame-soup';
