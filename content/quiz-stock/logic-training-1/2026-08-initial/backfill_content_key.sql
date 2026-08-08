-- backfill_content_key.sql
-- V007 適用後・V008 適用前に、ローカル MySQL と Aurora の両方へ適用する。
-- 環境間で AUTO_INCREMENT id が一致しないため、安定キー（set_code + question_text）で行を解決する。
-- 採番: slot_code ごとに 16-2 投入順（ローカル id 昇順）で 001〜014。適用後の更新行数 = 42 を確認すること。

UPDATE quiz_stock_items q JOIN batch_sets b ON b.id = q.set_id SET q.content_key = 'morning-001' WHERE b.set_code = 'logic-training-1' AND q.question_text = 'サイとラクダとカメの3匹が、そろって家電量販店にやって来た。さて、何を買いに来た?';
UPDATE quiz_stock_items q JOIN batch_sets b ON b.id = q.set_id SET q.content_key = 'morning-002' WHERE b.set_code = 'logic-training-1' AND q.question_text = '9匹の虎が乗っている乗り物ってなんだ?';
UPDATE quiz_stock_items q JOIN batch_sets b ON b.id = q.set_id SET q.content_key = 'morning-003' WHERE b.set_code = 'logic-training-1' AND q.question_text = '「世界」の真ん中にいる虫は、なんだ?';
UPDATE quiz_stock_items q JOIN batch_sets b ON b.id = q.set_id SET q.content_key = 'morning-004' WHERE b.set_code = 'logic-training-1' AND q.question_text = '相手を乾かせば乾かすほど、自分はどんどん濡れていくものは、なんだ?';
UPDATE quiz_stock_items q JOIN batch_sets b ON b.id = q.set_id SET q.content_key = 'morning-005' WHERE b.set_code = 'logic-training-1' AND q.question_text = '体じゅう穴だらけなのに、水をたっぷり蓄えられるものは、なんだ?';
UPDATE quiz_stock_items q JOIN batch_sets b ON b.id = q.set_id SET q.content_key = 'morning-006' WHERE b.set_code = 'logic-training-1' AND q.question_text = 'ナイフで切っても、ハンマーでたたいても、絶対に壊れないものは、なんだ?';
UPDATE quiz_stock_items q JOIN batch_sets b ON b.id = q.set_id SET q.content_key = 'morning-007' WHERE b.set_code = 'logic-training-1' AND q.question_text = 'とても壊れやすくて、名前を口にした瞬間に壊れてしまうものは、なんだ?';
UPDATE quiz_stock_items q JOIN batch_sets b ON b.id = q.set_id SET q.content_key = 'morning-008' WHERE b.set_code = 'logic-training-1' AND q.question_text = '自分の持ち物なのに、自分よりも他人のほうがたくさん使っているものは、なんだ?';
UPDATE quiz_stock_items q JOIN batch_sets b ON b.id = q.set_id SET q.content_key = 'morning-009' WHERE b.set_code = 'logic-training-1' AND q.question_text = '毎日必ずやって来るはずなのに、待っていても永遠にたどり着かない日は、いつ?';
UPDATE quiz_stock_items q JOIN batch_sets b ON b.id = q.set_id SET q.content_key = 'morning-010' WHERE b.set_code = 'logic-training-1' AND q.question_text = '「とればとるほど」減るどころか、どんどん増えていくものは、なんだ?';
UPDATE quiz_stock_items q JOIN batch_sets b ON b.id = q.set_id SET q.content_key = 'morning-011' WHERE b.set_code = 'logic-training-1' AND q.question_text = '「弟」には2つあるのに、「妹」には1つしかないもの、なんだ?';
UPDATE quiz_stock_items q JOIN batch_sets b ON b.id = q.set_id SET q.content_key = 'morning-012' WHERE b.set_code = 'logic-training-1' AND q.question_text = 'どんなに全力で走っても、絶対に追い越せない相手がいる。それはだれ?';
UPDATE quiz_stock_items q JOIN batch_sets b ON b.id = q.set_id SET q.content_key = 'morning-013' WHERE b.set_code = 'logic-training-1' AND q.question_text = '使う前に、必ず一度壊さなければいけないものは、なんだ?';
UPDATE quiz_stock_items q JOIN batch_sets b ON b.id = q.set_id SET q.content_key = 'morning-014' WHERE b.set_code = 'logic-training-1' AND q.question_text = '「1日」には2回もあるのに、「1年」には1回しかない。そんな不思議なもの、なんだ?';
UPDATE quiz_stock_items q JOIN batch_sets b ON b.id = q.set_id SET q.content_key = 'noon-001' WHERE b.set_code = 'logic-training-1' AND q.question_text = '人が一生のあいだに眠る時間は、全部合計するとおよそ何年分になる?';
UPDATE quiz_stock_items q JOIN batch_sets b ON b.id = q.set_id SET q.content_key = 'noon-002' WHERE b.set_code = 'logic-training-1' AND q.question_text = '毎日のなにげない歩き。一生分を合計すると、距離はおよそどれくらいになる?';
UPDATE quiz_stock_items q JOIN batch_sets b ON b.id = q.set_id SET q.content_key = 'noon-003' WHERE b.set_code = 'logic-training-1' AND q.question_text = 'あなたの心臓が1日に打つ回数は、およそ何回?';
UPDATE quiz_stock_items q JOIN batch_sets b ON b.id = q.set_id SET q.content_key = 'noon-004' WHERE b.set_code = 'logic-training-1' AND q.question_text = '人が一生のあいだにまばたきする回数は、およそ何回?';
UPDATE quiz_stock_items q JOIN batch_sets b ON b.id = q.set_id SET q.content_key = 'noon-005' WHERE b.set_code = 'logic-training-1' AND q.question_text = '健康な人でも、髪の毛は1日におよそ何本、自然に抜けている?';
UPDATE quiz_stock_items q JOIN batch_sets b ON b.id = q.set_id SET q.content_key = 'noon-006' WHERE b.set_code = 'logic-training-1' AND q.question_text = '朝・昼・晩の食事。一生分を合計すると、およそ何回ごはんを食べることになる?';
UPDATE quiz_stock_items q JOIN batch_sets b ON b.id = q.set_id SET q.content_key = 'noon-007' WHERE b.set_code = 'logic-training-1' AND q.question_text = '毎日の通勤時間。働く40年分を合計すると、およそどれくらいの長さになる?';
UPDATE quiz_stock_items q JOIN batch_sets b ON b.id = q.set_id SET q.content_key = 'noon-008' WHERE b.set_code = 'logic-training-1' AND q.question_text = '日本全国で、1日に飲まれる缶コーヒーはおよそ何本?';
UPDATE quiz_stock_items q JOIN batch_sets b ON b.id = q.set_id SET q.content_key = 'noon-009' WHERE b.set_code = 'logic-training-1' AND q.question_text = '日本全国で、1日に配達される宅配便はおよそ何個?';
UPDATE quiz_stock_items q JOIN batch_sets b ON b.id = q.set_id SET q.content_key = 'noon-010' WHERE b.set_code = 'logic-training-1' AND q.question_text = '朝のラッシュ時、都心の通勤電車1編成(10両)にはおよそ何人乗っている?';
UPDATE quiz_stock_items q JOIN batch_sets b ON b.id = q.set_id SET q.content_key = 'noon-011' WHERE b.set_code = 'logic-training-1' AND q.question_text = '日本全国にある自動販売機は、およそ何台?';
UPDATE quiz_stock_items q JOIN batch_sets b ON b.id = q.set_id SET q.content_key = 'noon-012' WHERE b.set_code = 'logic-training-1' AND q.question_text = '日本全国で、1日に生まれる赤ちゃんはおよそ何人?';
UPDATE quiz_stock_items q JOIN batch_sets b ON b.id = q.set_id SET q.content_key = 'noon-013' WHERE b.set_code = 'logic-training-1' AND q.question_text = '大好きな人も多いカレーライス。一生で食べる回数は、およそ何皿になる?';
UPDATE quiz_stock_items q JOIN batch_sets b ON b.id = q.set_id SET q.content_key = 'noon-014' WHERE b.set_code = 'logic-training-1' AND q.question_text = 'なんとなく見ているスマホ。1年分を合計すると、どれくらいの時間になる?';
UPDATE quiz_stock_items q JOIN batch_sets b ON b.id = q.set_id SET q.content_key = 'night-001' WHERE b.set_code = 'logic-training-1' AND q.question_text = '10階に住む人は、雨の日はエレベーターで10階まで行くのに、晴れの日は7階で降りて階段を使う。なぜ?';
UPDATE quiz_stock_items q JOIN batch_sets b ON b.id = q.set_id SET q.content_key = 'night-002' WHERE b.set_code = 'logic-training-1' AND q.question_text = '「水を1杯ください」と頼んだ客に、店員はいきなり大きな物音を立てて驚かせた。なのに客はお礼を言って帰った。なぜ?';
UPDATE quiz_stock_items q JOIN batch_sets b ON b.id = q.set_id SET q.content_key = 'night-003' WHERE b.set_code = 'logic-training-1' AND q.question_text = '「この屏風の絵の虎が夜な夜な抜け出して暴れる。捕まえてくれ」と無茶を言われた。とんちで有名な小僧さんは、どう切り返した?';
UPDATE quiz_stock_items q JOIN batch_sets b ON b.id = q.set_id SET q.content_key = 'night-004' WHERE b.set_code = 'logic-training-1' AND q.question_text = 'ゲームで3つの扉から1つを選ぶ。①火が燃えさかる部屋 ②毒ガスが充満した部屋 ③3年間なにも食べていないライオンの部屋。安全なのは?';
UPDATE quiz_stock_items q JOIN batch_sets b ON b.id = q.set_id SET q.content_key = 'night-005' WHERE b.set_code = 'logic-training-1' AND q.question_text = '父と息子が事故にあい、別々の病院へ運ばれた。息子の手術室に入ってきた外科医が言った。「この子は私の息子です」。外科医は誰?';
UPDATE quiz_stock_items q JOIN batch_sets b ON b.id = q.set_id SET q.content_key = 'night-006' WHERE b.set_code = 'logic-training-1' AND q.question_text = '橋のたもとに「このはしわたるべからず」の立て札。それでもとんちで有名な小僧さんは堂々と渡ってみせた。どうやって?';
UPDATE quiz_stock_items q JOIN batch_sets b ON b.id = q.set_id SET q.content_key = 'night-007' WHERE b.set_code = 'logic-training-1' AND q.question_text = '冬の山小屋にストーブ・ランプ・ろうそくがある。でもマッチは1本しかない。さて、最初に火をつけるべきものは?';
UPDATE quiz_stock_items q JOIN batch_sets b ON b.id = q.set_id SET q.content_key = 'night-008' WHERE b.set_code = 'logic-training-1' AND q.question_text = '2人の父と2人の息子で釣りに行き、釣れた魚はちょうど3匹。それでも全員が1匹ずつ持ち帰れた。どういうこと?';
UPDATE quiz_stock_items q JOIN batch_sets b ON b.id = q.set_id SET q.content_key = 'night-009' WHERE b.set_code = 'logic-training-1' AND q.question_text = '財布から2枚の硬貨で、ちょうど110円を払った。片方は10円玉ではない。さて、何と何で払った?';
UPDATE quiz_stock_items q JOIN batch_sets b ON b.id = q.set_id SET q.content_key = 'night-010' WHERE b.set_code = 'logic-training-1' AND q.question_text = '停電の夜、ろうそく10本に火をつけた。しばらくして風で3本が消えた。そのまま朝まで置いておくと、残っているろうそくは何本?';
UPDATE quiz_stock_items q JOIN batch_sets b ON b.id = q.set_id SET q.content_key = 'night-011' WHERE b.set_code = 'logic-training-1' AND q.question_text = '「誰にもほどけないこの結び目をほどいた者が、王になる」という伝説の固い結び目。ある若者は一瞬で解決してみせた。どうやって?';
UPDATE quiz_stock_items q JOIN batch_sets b ON b.id = q.set_id SET q.content_key = 'night-012' WHERE b.set_code = 'logic-training-1' AND q.question_text = '1人の赤ん坊を、2人の女性が「私の子です」と譲らない。王は「では子を半分に分けよ」と命じた。すると本当の母親はどうした?';
UPDATE quiz_stock_items q JOIN batch_sets b ON b.id = q.set_id SET q.content_key = 'night-013' WHERE b.set_code = 'logic-training-1' AND q.question_text = 'あなたはバスの運転手。始発で9人乗り、次の停留所で4人降りて2人乗り、その次で4人乗って1人降りた。さて、運転手の誕生日はいつ?';
UPDATE quiz_stock_items q JOIN batch_sets b ON b.id = q.set_id SET q.content_key = 'night-014' WHERE b.set_code = 'logic-training-1' AND q.question_text = '若いときは背が高く、年を取るほど背が低くなっていく。最後には消えてしまうものは、なんだ?';
