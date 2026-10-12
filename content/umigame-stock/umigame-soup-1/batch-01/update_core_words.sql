-- batch-01 既存 14 問の核心語の更新（V017 適用後、バッチと返信 Lambda のデプロイ前に実行）
-- 生成元: content/umigame-stock/umigame-soup-1/batch-01/stock_items.py（単一ソース）
-- 適用先: ローカル MySQL / Aurora（acps）。set_code と content_key で対象を特定する。
-- 出題済み umigame_items は core_words が NULL の行だけ補完する。

-- 001-faint-shadow: 影が薄いと言われて喜ぶ男
UPDATE umigame_stock_items SET core_words = '{"words":["レントゲン","病気","医者","主治医","病院","治療","写真"],"except":[]}'
WHERE content_key = '001-faint-shadow'
  AND set_id = (SELECT id FROM batch_sets WHERE set_code = 'umigame-soup-1');

-- 003-silent-musicians: 階段に並ぶ、音を出さない男たち
UPDATE umigame_stock_items SET core_words = '{"words":["人形","ひな","雛","五人囃子","段飾り","お祝い","ひな祭り"],"except":[]}'
WHERE content_key = '003-silent-musicians'
  AND set_id = (SELECT id FROM batch_sets WHERE set_code = 'umigame-soup-1');

-- 004-fifty-year-letter: 会ったことのない男の子からの手紙
UPDATE umigame_stock_items SET core_words = '{"words":["タイムカプセル","本人","同一人物","自分自身","未来の自分","埋め","同窓会","掘り"],"except":[]}'
WHERE content_key = '004-fifty-year-letter'
  AND set_id = (SELECT id FROM batch_sets WHERE set_code = 'umigame-soup-1');

-- 005-bakers-egg: 割らない卵を自慢するパン屋
UPDATE umigame_stock_items SET core_words = '{"words":["見習い","弟子","修行","一人前","人間","職人"],"except":[]}'
WHERE content_key = '005-bakers-egg'
  AND set_id = (SELECT id FROM batch_sets WHERE set_code = 'umigame-soup-1');

-- 006-frozen-tag: 助けに来た女も凍りついた
UPDATE umigame_stock_items SET core_words = '{"words":["氷鬼","鬼ごっこ","鬼","タッチ","遊び","遊ん","ルール"],"except":["遊び方"]}'
WHERE content_key = '006-frozen-tag'
  AND set_id = (SELECT id FROM batch_sets WHERE set_code = 'umigame-soup-1');

-- 007-blank-letter: 白紙に戻った約束
UPDATE umigame_stock_items SET core_words = '{"words":["消せる","フリクション","熱で","熱を","熱い","熱く","加熱","透明","ドライヤー","インク","こする","摩擦"],"except":[]}'
WHERE content_key = '007-blank-letter'
  AND set_id = (SELECT id FROM batch_sets WHERE set_code = 'umigame-soup-1');

-- 008-who-made-the-mistake: 完璧な演奏に「あ、間違えた」
UPDATE umigame_stock_items SET core_words = '{"words":["娘","子ども","子供","練習","習い","つっかえ","毎晩","リビング","間違えて弾"],"except":[]}'
WHERE content_key = '008-who-made-the-mistake'
  AND set_id = (SELECT id FROM batch_sets WHERE set_code = 'umigame-soup-1');

-- 009-year-late-verdict: 庭のすみに実ったすいか
UPDATE umigame_stock_items SET core_words = '{"words":["種を","種が","種は","種も","種飛ばし","飛ばし","吐き","吐い","吐く","吹き","縁側","芽が","芽を","発芽","芽吹"],"except":[]}'
WHERE content_key = '009-year-late-verdict'
  AND set_id = (SELECT id FROM batch_sets WHERE set_code = 'umigame-soup-1');

-- 010-two-hour-dentist: 2時間かけて通う歯医者
UPDATE umigame_stock_items SET core_words = '{"words":["育った","生家","実家","住んでいた家","背丈","背比べ","柱の傷","自分の家"],"except":[]}'
WHERE content_key = '010-two-hour-dentist'
  AND set_id = (SELECT id FROM batch_sets WHERE set_code = 'umigame-soup-1');

-- 012-early-morning-run: 早く走った朝
UPDATE umigame_stock_items SET core_words = '{"words":["時計代わり","目印","合図にし","時刻を決め","時間を決め","見て家を出"],"except":[]}'
WHERE content_key = '012-early-morning-run'
  AND set_id = (SELECT id FROM batch_sets WHERE set_code = 'umigame-soup-1');

-- 013-fifty-five-year-nengajo: 55年目の年賀状
UPDATE umigame_stock_items SET core_words = '{"words":["将棋","一手","参りました","投了","将棋盤","盤上","盤面","盤を","駒","指し","一年に"],"except":[]}'
WHERE content_key = '013-fifty-five-year-nengajo'
  AND set_id = (SELECT id FROM batch_sets WHERE set_code = 'umigame-soup-1');

-- 014-kind-interpreter: 日本語を覚えた日から
UPDATE umigame_stock_items SET core_words = '{"words":["通訳","言い換え","褒め言葉","作り変え","訳し","息子"],"except":[]}'
WHERE content_key = '014-kind-interpreter'
  AND set_id = (SELECT id FROM batch_sets WHERE set_code = 'umigame-soup-1');

-- 015-unlicensed-driver: 免許のない男のドライブ
UPDATE umigame_stock_items SET core_words = '{"words":["人生ゲーム","駒","ピンを","ピンが","ピンの","家族のピン","ボードゲーム","すごろく","ルーレット","ゲーム盤","盤上","盤面","盤を"],"except":[]}'
WHERE content_key = '015-unlicensed-driver'
  AND set_id = (SELECT id FROM batch_sets WHERE set_code = 'umigame-soup-1');

-- 016-umigame-soup: 本物のウミガメのスープ
UPDATE umigame_stock_items SET core_words = '{"words":["人肉","人の肉","仲間の肉","遺体","死体"],"except":[]}'
WHERE content_key = '016-umigame-soup'
  AND set_id = (SELECT id FROM batch_sets WHERE set_code = 'umigame-soup-1');

UPDATE umigame_items ui
JOIN umigame_stock_items s ON s.set_id = ui.set_id AND s.content_key = ui.content_key
JOIN batch_sets b ON b.id = ui.set_id
SET ui.core_words = s.core_words
WHERE ui.core_words IS NULL AND b.set_code = 'umigame-soup-1';

-- 両表の件数と設定済み件数を確認する。
SELECT 'umigame_stock_items' AS table_name, COUNT(*) AS item_rows,
       SUM(i.core_words IS NOT NULL) AS core_words_set
FROM umigame_stock_items i JOIN batch_sets b ON b.id = i.set_id
WHERE b.set_code = 'umigame-soup-1';

SELECT 'umigame_items' AS table_name, COUNT(*) AS item_rows,
       SUM(i.core_words IS NOT NULL) AS core_words_set
FROM umigame_items i JOIN batch_sets b ON b.id = i.set_id
WHERE b.set_code = 'umigame-soup-1';
