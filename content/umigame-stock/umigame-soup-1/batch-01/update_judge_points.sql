-- batch-01 既存ストックの判定要点更新（V013 適用後に実行）
-- 生成元: content/umigame-stock/umigame-soup-1/batch-01/stock_items.py（単一ソース）
-- 適用先: ローカル MySQL / Aurora（acps）。content_key で対象を特定する。

-- 001-faint-shadow: 影が薄いと言われて喜ぶ男
UPDATE umigame_stock_items s
JOIN batch_sets b ON b.id = s.set_id
SET s.core_points = '["影はレントゲンの影","病気が良くなった"]',
    s.reveal_text = '男の「影」はレントゲンに写った病気の跡。3か月ぶりの診察で回復を知り、主治医に感謝した。'
WHERE b.set_code = 'umigame-soup-1' AND s.content_key = '001-faint-shadow';

-- 003-silent-musicians: 階段に並ぶ、音を出さない男たち
UPDATE umigame_stock_items s
JOIN batch_sets b ON b.id = s.set_id
SET s.core_points = '["男たちはひな人形"]',
    s.reveal_text = '男たちはひな人形の五人囃子。段飾りに並ぶ人形なので音は出さず、家族は飾っている間毎日眺めて楽しんでいる。'
WHERE b.set_code = 'umigame-soup-1' AND s.content_key = '003-silent-musicians';

-- 004-fifty-year-letter: 会ったことのない男の子からの手紙
UPDATE umigame_stock_items s
JOIN batch_sets b ON b.id = s.set_id
SET s.core_points = '["手紙の主は子どもの頃の自分","手紙はタイムカプセルに入っていた"]',
    s.reveal_text = '手紙は小学生の男が未来の自分へ書いたもの。50年後、同窓会でタイムカプセルから受け取った。'
WHERE b.set_code = 'umigame-soup-1' AND s.content_key = '004-fifty-year-letter';

-- 005-bakers-egg: 割らない卵を自慢するパン屋
UPDATE umigame_stock_items s
JOIN batch_sets b ON b.id = s.set_id
SET s.core_points = '["卵はパン職人の見習い","その見習いがパンを焼いている"]',
    s.reveal_text = '「卵」はパン職人の卵、つまり見習いのこと。主人が一人前に育てたその職人が、いまおいしいパンを焼いている。'
WHERE b.set_code = 'umigame-soup-1' AND s.content_key = '005-bakers-egg';

-- 006-frozen-tag: 助けに来た女も凍りついた
UPDATE umigame_stock_items s
JOIN batch_sets b ON b.id = s.set_id
SET s.core_points = '["2人は氷鬼をしていた"]',
    s.reveal_text = '2人は子どもと氷鬼をしていた。男は鬼にタッチされて凍り、助けに来た女も男に触れる直前にタッチされて凍った。'
WHERE b.set_code = 'umigame-soup-1' AND s.content_key = '006-frozen-tag';

-- 007-blank-letter: 白紙に戻った約束
UPDATE umigame_stock_items s
JOIN batch_sets b ON b.id = s.set_id
SET s.core_points = '["約束を書いた紙の文字が消えた","文字は消せるペンで書かれていた"]',
    s.reveal_text = '夕立で濡れた手紙をドライヤーで乾かし、消せるペンの文字が消えた。2人は約束を書き直して果たした。'
WHERE b.set_code = 'umigame-soup-1' AND s.content_key = '007-blank-letter';

-- 008-who-made-the-mistake: 間違えたのは誰か
UPDATE umigame_stock_items s
JOIN batch_sets b ON b.id = s.set_id
SET s.core_points = '["男は娘の間違った弾き方で曲を覚えた"]',
    s.reveal_text = '男は娘が毎晩間違えて弾く曲を覚えていた。正しく弾くピアニストを間違いと思い、妻はその理由に笑った。'
WHERE b.set_code = 'umigame-soup-1' AND s.content_key = '008-who-made-the-mistake';

-- 009-year-late-verdict: 1年越しの判定
UPDATE umigame_stock_items s
JOIN batch_sets b ON b.id = s.set_id
SET s.core_points = '["兄弟で種飛ばしの勝負をした","すいかは弟が飛ばした種から育った"]',
    s.reveal_text = '去年の種飛ばしで弟の種は庭の奥まで飛んでいた。その種が育ってすいかが実り、1年越しに兄は負けを認めた。'
WHERE b.set_code = 'umigame-soup-1' AND s.content_key = '009-year-late-verdict';

-- 010-two-hour-dentist: 2時間かけて通う歯医者
UPDATE umigame_stock_items s
JOIN batch_sets b ON b.id = s.set_id
SET s.core_points = '["歯医者は男が育った家だった"]',
    s.reveal_text = 'その歯医者は男が育った家を改装したもの。男は検診を口実に通い、背丈の傷が残る柱の前で過ごしてから帰る。'
WHERE b.set_code = 'umigame-soup-1' AND s.content_key = '010-two-hour-dentist';

-- 012-early-morning-run: 早く走った朝
UPDATE umigame_stock_items s
JOIN batch_sets b ON b.id = s.set_id
SET s.core_points = '["子どもたちは毎日男を合図に家を出ていた"]',
    s.reveal_text = '子どもたちは毎朝同じ時刻に走る男を合図に家を出ていた。男が早く走った朝、遅刻だと思い込んで飛び出した。'
WHERE b.set_code = 'umigame-soup-1' AND s.content_key = '012-early-morning-run';

-- 013-fifty-five-year-nengajo: 55年目の年賀状
UPDATE umigame_stock_items s
JOIN batch_sets b ON b.id = s.set_id
SET s.core_points = '["年賀状で将棋を1手ずつ指していた"]',
    s.reveal_text = '2人は年賀状に将棋を1手ずつ書き、55年かけて1局を指していた。友人の年賀状に「参りました」とあり、男が勝った。'
WHERE b.set_code = 'umigame-soup-1' AND s.content_key = '013-fifty-five-year-nengajo';

-- 014-kind-interpreter: 日本語を覚えた日から
UPDATE umigame_stock_items s
JOIN batch_sets b ON b.id = s.set_id
SET s.core_points = '["息子が悪口を良い言葉に変えて通訳した"]',
    s.reveal_text = '息子が嫁と義母の言葉を作り替えて通訳していた。女が日本語を覚えて本音が伝わり、けんかが始まった。'
WHERE b.set_code = 'umigame-soup-1' AND s.content_key = '014-kind-interpreter';

-- 015-unlicensed-driver: 免許のない男のドライブ
UPDATE umigame_stock_items s
JOIN batch_sets b ON b.id = s.set_id
SET s.core_points = '["人生ゲームの車の駒を動かしていた"]',
    s.reveal_text = '男が走らせているのは人生ゲームの車の駒。妻と子どもはピンで乗せていて、おもちゃなので免許はいらない。'
WHERE b.set_code = 'umigame-soup-1' AND s.content_key = '015-unlicensed-driver';

-- 016-umigame-soup: 本物のウミガメのスープ
UPDATE umigame_stock_items s
JOIN batch_sets b ON b.id = s.set_id
SET s.core_points = '["昔ウミガメのスープと言われて飲んだ","それは仲間の肉だった"]',
    s.reveal_text = '男は遭難中、ウミガメのスープだと言われて亡くなった仲間の肉を飲んでいた。本物の味でそれに気づいた。'
WHERE b.set_code = 'umigame-soup-1' AND s.content_key = '016-umigame-soup';
