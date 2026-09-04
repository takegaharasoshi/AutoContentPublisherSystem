-- batch-01 ウミガメストック投入（10 問。人間レビュー + プローブテスト承認後に実行）
-- 生成元: content/umigame-stock/umigame-soup-1/batch-01/stock_items.py（単一ソース）。適用先: ローカル MySQL / Aurora（acps）
-- set_id は set_code から解決するため両環境共通で実行できる。content_key は stock_items.py で採番済み。

-- U01 毎月同じ本を借りる老人
INSERT INTO umigame_stock_items (set_id, content_key, title, difficulty, problem_text, truth, fact_sheet,
    expected_questions, hook, rule_text, narration, play_example, character_lines, illustration_prompt,
    caption, source_note, is_active)
VALUES ((SELECT id FROM batch_sets WHERE set_code = 'umigame-soup-1'),
        '001-library-card', '毎月同じ本を借りる老人', 4,
        'もう何年も、毎月同じ本を借りては期限どおりに返す老人。司書が気をきかせて同じ本を新品で贈ると、老人は困った顔をして、翌月もまた図書館でその本を借りにきた。なぜ？',
        '老人が欲しいのは本の中身ではなく、巻末に残っている古い貸出カードだった。そこには、老人が若い頃に恋をした女性、今の妻が学生時代に書いた名前が残っている。借りている 1 か月のあいだ、家でそのカードを眺めるのが老人の楽しみで、新品の本にはそのカードがない。',
        '["老人は本の内容を読むために借りているのではない","老人の目当ては、その本の巻末に残っている古い貸出カードである","貸出カードには、老人が若い頃に恋をした女性（今の妻）が学生時代に書いた名前が残っている","老人は借りている 1 か月のあいだ、家でそのカードを眺めるのが楽しみである","司書が贈ったのは同じ題名の新品の本で、貸出カードは付いていない","図書館の本は、借りなければ手元に置いておくことができない","妻は健在で、老人がこの本を借りていることを知らない","老人は本を汚したり書き込んだりしていない","司書に悪意はなく、老人を喜ばせるつもりだった","老人は図書館の中でカードを見るだけでは満足できず、家に持ち帰って手元に置いておきたい","老人がお金に困って本を買えないわけではない","本の題名・ジャンル・値段は問題に関係ない"]',
        '[{"q":"老人は本の内容を読んでいますか？","a":"いいえ"},{"q":"老人は本の題名や作者にこだわっていますか？","a":"関係ない"},{"q":"老人はお金に困っていますか？","a":"いいえ"},{"q":"老人は新品の本を受け取りましたか？","a":"はい"},{"q":"図書館の本と新品の本で、中身の文章は違いますか？","a":"いいえ"},{"q":"図書館の本には、新品の本にないものが付いていますか？","a":"はい"},{"q":"それは誰かの書き込みや落書きですか？","a":"いいえ"},{"q":"それは本の巻末にありますか？","a":"はい"},{"q":"貸出カードが関係ありますか？","a":"はい"},{"q":"カードに書かれた名前が大事なのですか？","a":"はい"},{"q":"それは老人自身の名前ですか？","a":"いいえ"},{"q":"亡くなった人の名前ですか？","a":"いいえ"},{"q":"老人の妻に関係がありますか？","a":"はい"},{"q":"司書は老人を困らせようとしましたか？","a":"いいえ"},{"q":"老人は図書館の中でカードを見るだけでも満足できますか？","a":"いいえ（借りて手元に置きたい）"},{"q":"図書館の場所や本のジャンルは重要ですか？","a":"関係ない"},{"q":"老人は司書に好意がありますか？","a":"関係ない"},{"q":"貸出カードに若い頃の奥さんが書いた名前が残っていて、それを手元で眺めたいから借りている？","a":"正解"}]',
        '新品なのに、いらない？', '「はい / いいえ / 関係ない」で答えられる質問をコメントしてね。出題者が全部返事します',
        '{"problem":"もう何年も、毎月同じ本を借りては、期限どおりに返す老人。司書が気をきかせて、同じ本を新品で贈ると、老人は困った顔をして、翌月もまた図書館でその本を借りにきた。なぜ？","rule":"はい、いいえ、関係ない、で答えられる質問をコメントしてね。全部返事するよ。"}',
        '[{"role":"questioner","text":"本を読みたいだけ？"},{"role":"master","text":"いいえ。"},{"role":"questioner","text":"新品と中身は違う？"},{"role":"master","text":"いいえ。"},{"role":"questioner","text":"古い本に何かある？"},{"role":"master","text":"はい！"}]',
        '{"master":{"intro":"質問してみて！","outro":"何度でも答えるよ。コメントで質問！"},"jr":{"outro":"面白かったら、いいね、フォローよろしくね！"}}',
        'A stylized 1990s Japanese OVA anime background painting (hand-painted cel-era background art, poster-color textures, clean shapes, thick brush-like outlines on key objects). Mid-key lighting: moonlight, lamps or candlelight keep the whole scene clearly visible, NOT dark.

Scene: Inside a small, quiet public library in the evening: an elderly man in a cardigan stands at a wooden counter holding a single well-worn hardcover book; a librarian behind the counter; tall bookshelves and a warm reading lamp; a window with dusk light.

Vertical 9:16 composition (1024x1536). No text, no letters, no numbers, no logos, no signs. Depict only the scene described in the problem statement; do not depict any clue to the story''s hidden truth. People: only the persons who appear in the problem, plus at most one distant silhouette. Keep the upper 55% of the image calm and simple (sky, wall, ceiling, window) so that text cards can be overlaid there.',
        '【探偵カメロックのウミガメのスープ】
今日の一問は、図書館に通うおじいさんのちょっと不思議な習慣。

もう何年も、毎月同じ本を借りては期限どおりに返す老人。司書が気をきかせて同じ本を新品で贈ると、老人は困った顔をして、翌月もまた図書館でその本を借りにきた。なぜ？

「はい / いいえ / 関係ない」で答えられる質問をコメントしてね。出題者の探偵カメロックが全部返事します。正解が出るまで何度でもどうぞ。

#ウミガメのスープ #水平思考 #推理クイズ #なぞなぞ #謎解き #クイズ #AIart',
        '完全オリジナル（既存問題の転載・改変ではない）。作問法は note 記事 https://note.com/suekai0217/n/n35128e606a9b の4 ステップ（モチーフ → 連想 → 言い方を変える → 不思議にする）と良い問題の 3 条件（コアが明確・動線がある・現実離れしない）に従う。着想の型は research.md（Codex Web リサーチ台帳）を参照。 型: 物語復元型（A→C 切り出し）。モチーフ「図書館」→ 連想「借りる・返す・貸出カード」→ 常識「本は読むために借りる」の逆。着想元の既存問題なし。', 1);

-- U02 反対方向の電車に乗る男
INSERT INTO umigame_stock_items (set_id, content_key, title, difficulty, problem_text, truth, fact_sheet,
    expected_questions, hook, rule_text, narration, play_example, character_lines, illustration_prompt,
    caption, source_note, is_active)
VALUES ((SELECT id FROM batch_sets WHERE set_code = 'umigame-soup-1'),
        '002-opposite-train', '反対方向の電車に乗る男', 2,
        '男は毎朝、駅で会社とは反対方向の電車に乗る。遠回りが好きなわけでも、途中で用事があるわけでもない。それでも男は毎朝、この乗り方を絶対にやめようとしない。なぜ？',
        '男の路線は朝の会社方向の電車が超満員で、男の駅からは座れない。男は反対方向に 2 駅戻って始発駅へ行き、そこから折り返しの電車に乗ることで、毎朝確実に座って通勤している。',
        '["男の通勤路線は、朝の会社方向の電車がとても混んでいる","男の家の最寄り駅では、会社方向の電車はいつも満員で座れない","男は反対方向の電車に乗り、2 駅先の始発駅で降りる","始発駅から折り返しの会社方向の電車に乗ると、確実に座れる","男の目的は、通勤中に座ることである（健康上の理由があるわけではない）","男は少し早く家を出ているが、遅刻はしていない","男は座って本を読んだり眠ったりして通勤時間を使っている","男に途中駅での用事や知り合いはいない","男の職業・会社の場所・電車の色は問題に関係ない","定期券や運賃の損得は問題に関係ない"]',
        '[{"q":"男は遠回りが好きですか？","a":"いいえ"},{"q":"男は反対方向の駅に用事がありますか？","a":"いいえ"},{"q":"男は反対方向の電車で会社まで行きますか？","a":"いいえ"},{"q":"男は途中で乗り換えますか？","a":"はい"},{"q":"男は途中で降りて、会社方向の電車に乗り直しますか？","a":"はい"},{"q":"男が降りる駅は特別な駅ですか？","a":"はい"},{"q":"男の会社の場所は重要ですか？","a":"関係ない"},{"q":"男は電車が好きですか？","a":"関係ない"},{"q":"会社方向の電車は混んでいますか？","a":"はい"},{"q":"男は電車の中でしたいことがありますか？","a":"はい"},{"q":"男は立って通勤するのが嫌なのですか？","a":"はい"},{"q":"男は健康上の理由で座る必要がありますか？","a":"いいえ"},{"q":"男が降りる駅は始発駅ですか？","a":"はい"},{"q":"男は遅刻していますか？","a":"いいえ"},{"q":"男は定期券を持っていますか？","a":"関係ない"},{"q":"始発駅まで戻って折り返しの電車に乗れば、確実に座れるから？","a":"正解"}]',
        'なぜ逆方向に乗る？', '「はい / いいえ / 関係ない」で答えられる質問をコメントしてね。出題者が全部返事します',
        '{"problem":"男は毎朝、駅で会社とは反対方向の電車に乗る。遠回りが好きなわけでも、途中で用事があるわけでもない。それでも男は毎朝、この乗り方を絶対にやめようとしない。なぜ？","rule":"はい、いいえ、関係ない、で答えられる質問をコメントしてね。全部返事するよ。"}',
        '[{"role":"questioner","text":"寄り道が目的？"},{"role":"master","text":"いいえ。"},{"role":"questioner","text":"電車は混んでる？"},{"role":"master","text":"はい！"},{"role":"questioner","text":"会社は駅から遠い？"},{"role":"master","text":"関係ありません。"}]',
        '{"master":{"intro":"質問してみて！","outro":"何度でも答えるよ。コメントで質問！"},"jr":{"outro":"面白かったら、いいね、フォローよろしくね！"}}',
        'A stylized 1990s Japanese OVA anime background painting (hand-painted cel-era background art, poster-color textures, clean shapes, thick brush-like outlines on key objects). Mid-key lighting: moonlight, lamps or candlelight keep the whole scene clearly visible, NOT dark.

Scene: Early morning at a suburban Japanese train station: a man in a suit with a briefcase stands alone on a platform, looking toward an approaching train; across the tracks the other platform is visible in the distance with a handful of commuters; soft morning light and a clear sky.

Vertical 9:16 composition (1024x1536). No text, no letters, no numbers, no logos, no signs. Depict only the scene described in the problem statement; do not depict any clue to the story''s hidden truth. People: only the persons who appear in the problem, plus at most one distant silhouette. Keep the upper 55% of the image calm and simple (sky, wall, ceiling, window) so that text cards can be overlaid there.',
        '【探偵カメロックのウミガメのスープ】
通勤の朝、男はいつも会社と反対の電車に乗ります。

男は毎朝、駅で会社とは反対方向の電車に乗る。遠回りが好きなわけでも、途中で用事があるわけでもない。それでも男は毎朝、この乗り方を絶対にやめようとしない。なぜ？

「はい / いいえ / 関係ない」で答えられる質問をコメントしてね。出題者の探偵カメロックが全部返事します。正解が出るまで何度でもどうぞ。

#ウミガメのスープ #水平思考 #推理クイズ #なぞなぞ #謎解き #クイズ #AIart',
        '完全オリジナル（既存問題の転載・改変ではない）。作問法は note 記事 https://note.com/suekai0217/n/n35128e606a9b の4 ステップ（モチーフ → 連想 → 言い方を変える → 不思議にする）と良い問題の 3 条件（コアが明確・動線がある・現実離れしない）に従う。着想の型は research.md（Codex Web リサーチ台帳）を参照。 型: 物語復元型（A→C 切り出し）。モチーフ「通勤電車」→ 連想「混雑・座る・始発」→ 具体化 → 常識「会社へは会社方向に乗る」の逆。着想元の既存問題なし（研究台帳の「遠回りが目的達成」構造を参照）。', 1);

-- U03 毎晩 9 時の小石
INSERT INTO umigame_stock_items (set_id, content_key, title, difficulty, problem_text, truth, fact_sheet,
    expected_questions, hook, rule_text, narration, play_example, character_lines, illustration_prompt,
    caption, source_note, is_active)
VALUES ((SELECT id FROM batch_sets WHERE set_code = 'umigame-soup-1'),
        '003-pebble-signal', '毎晩 9 時の小石', 3,
        '毎晩 9 時、ひとり暮らしの老人は隣の家の窓に小石を投げる。隣の家族は怒らない。それどころか、石の音がしなかったある夜、家族はあわてて老人の家へ走って行った。なぜ？',
        '老人は耳が遠く、電話が使えない。老人と隣の家族は「毎晩 9 時、無事なら窓に小石を当てる」と約束している。石の音が「今日も元気」の合図で、音がしなかった夜は何かあったのかもしれないと、家族が様子を見に行った。その夜、老人は転んで立てなくなっていた。',
        '["老人はひとり暮らしで、足腰が弱い","老人は耳が遠く、電話の音がほとんど聞こえない","老人と隣の家族は、毎晩 9 時に小石を窓に当てることを約束している","小石の音は「今日も無事」を伝える合図である","隣の家族は、石の音を聞いて老人が元気だと安心している","石の音がしない夜は、老人に何かあった可能性があるため様子を見に行く","その夜、老人は転んで立てなくなっており、家族が助けた","老人と隣の家族は仲が良い","窓ガラスが割れるような強い投げ方ではない","老人の家族構成や年齢、季節は問題に関係ない"]',
        '[{"q":"老人は隣の家族が嫌いですか？","a":"いいえ"},{"q":"老人は窓を壊したいのですか？","a":"いいえ"},{"q":"小石を投げるのは遊びですか？","a":"いいえ"},{"q":"小石は何かを伝える合図ですか？","a":"はい"},{"q":"老人は電話を使えますか？","a":"いいえ"},{"q":"老人は耳が悪いのですか？","a":"はい"},{"q":"合図は老人が無事だと伝えるものですか？","a":"はい"},{"q":"隣の家族に何かを届けてもらうためですか？","a":"いいえ"},{"q":"老人と隣の家族は約束をしていますか？","a":"はい"},{"q":"石の大きさは重要ですか？","a":"関係ない"},{"q":"音がしなかった夜、老人に何かありましたか？","a":"はい"},{"q":"老人は転んでいましたか？","a":"はい"},{"q":"老人は亡くなりましたか？","a":"いいえ"},{"q":"隣の家に子どもはいますか？","a":"関係ない"},{"q":"老人は誰かをおどかすためにやっていますか？","a":"いいえ"},{"q":"季節は関係ありますか？","a":"関係ない"},{"q":"小石は毎晩「無事だよ」と知らせる合図で、音がしなかったから心配して駆けつけた？","a":"正解"}]',
        '毎晩 9 時の小石', '「はい / いいえ / 関係ない」で答えられる質問をコメントしてね。出題者が全部返事します',
        '{"problem":"毎晩 9 時、ひとり暮らしの老人は、隣の家の窓に小石を投げる。隣の家族は怒らない。それどころか、石の音がしなかったある夜、家族はあわてて老人の家へ走って行った。なぜ？","rule":"はい、いいえ、関係ない、で答えられる質問をコメントしてね。全部返事するよ。"}',
        '[{"role":"questioner","text":"窓を壊したい？"},{"role":"master","text":"いいえ。"},{"role":"questioner","text":"石は合図？"},{"role":"master","text":"はい！"},{"role":"questioner","text":"隣に子どもはいる？"},{"role":"master","text":"関係ありません。"}]',
        '{"master":{"intro":"質問してみて！","outro":"何度でも答えるよ。コメントで質問！"},"jr":{"outro":"面白かったら、いいね、フォローよろしくね！"}}',
        'A stylized 1990s Japanese OVA anime background painting (hand-painted cel-era background art, poster-color textures, clean shapes, thick brush-like outlines on key objects). Mid-key lighting: moonlight, lamps or candlelight keep the whole scene clearly visible, NOT dark.

Scene: A quiet residential street at night: a small old house and a neighboring family house with a lit second-floor window; an elderly person stands in a tiny garden between the two houses under a bright moon; warm lamplight spilling from the windows; a calm night sky above.

Vertical 9:16 composition (1024x1536). No text, no letters, no numbers, no logos, no signs. Depict only the scene described in the problem statement; do not depict any clue to the story''s hidden truth. People: only the persons who appear in the problem, plus at most one distant silhouette. Keep the upper 55% of the image calm and simple (sky, wall, ceiling, window) so that text cards can be overlaid there.',
        '【探偵カメロックのウミガメのスープ】
毎晩 9 時、おじいさんは隣の家の窓に小石を投げます。

毎晩 9 時、ひとり暮らしの老人は隣の家の窓に小石を投げる。隣の家族は怒らない。それどころか、石の音がしなかったある夜、家族はあわてて老人の家へ走って行った。なぜ？

「はい / いいえ / 関係ない」で答えられる質問をコメントしてね。出題者の探偵カメロックが全部返事します。正解が出るまで何度でもどうぞ。

#ウミガメのスープ #水平思考 #推理クイズ #なぞなぞ #謎解き #クイズ #AIart',
        '完全オリジナル（既存問題の転載・改変ではない）。作問法は note 記事 https://note.com/suekai0217/n/n35128e606a9b の4 ステップ（モチーフ → 連想 → 言い方を変える → 不思議にする）と良い問題の 3 条件（コアが明確・動線がある・現実離れしない）に従う。着想の型は research.md（Codex Web リサーチ台帳）を参照。 型: 物語復元型（A→C 切り出し）。モチーフ「小石」→ 連想「投げる・窓・合図」→ 常識「窓に石を投げるのは迷惑行為」の逆。着想元の既存問題なし（研究台帳の「見えない目印・合図」構造を参照）。', 1);

-- U04 曲が鳴ると走り出す町
INSERT INTO umigame_stock_items (set_id, content_key, title, difficulty, problem_text, truth, fact_sheet,
    expected_questions, hook, rule_text, narration, play_example, character_lines, illustration_prompt,
    caption, source_note, is_active)
VALUES ((SELECT id FROM batch_sets WHERE set_code = 'umigame-soup-1'),
        '004-bus-stop-song', '曲が鳴ると走り出す町', 3,
        '町の小さな商店の主人は、毎日決まった時刻に、店の外へ向けて同じ曲を大きな音で流す。客を呼ぶためではない。近所の人はその曲を聞くと、あわてて家を飛び出す。なぜ？',
        '店の前にバス停があり、バスは 1 日に数本しか来ない。近所には時計を確かめるのが苦手なお年寄りが多く、乗り遅れる人がいた。店主はバスが来る 5 分前に決まった曲を流し、「今から出れば間に合う」と知らせている。',
        '["店の前に路線バスのバス停がある","バスは 1 日に数本しか来ず、来る時刻は毎日同じである","曲は毎日、バスが来る 5 分前の決まった時刻に流している","近所の人が曲を聞いて向かう先は、店の前のバス停である","店主はこの合図で報酬を受け取っていない（善意で続けている）","曲は近所の人に「今から出ればバスに間に合う」と知らせる合図である","近所には時計を確かめるのが苦手なお年寄りが多い","店主は乗り遅れて困る人を見て、この合図を始めた","店主は客を増やす目的で曲を流しているのではない","近所の人は曲の意味を知っていて、店主に感謝している","曲の種類やジャンルは問題に関係ない","店で売っている商品は問題に関係ない"]',
        '[{"q":"曲は店の宣伝ですか？","a":"いいえ"},{"q":"近所の人は曲が嫌いで逃げていますか？","a":"いいえ"},{"q":"近所の人は店に買い物に来るのですか？","a":"関係ない"},{"q":"曲は何かの時刻を知らせていますか？","a":"はい"},{"q":"曲は毎日同じ時刻に流れますか？","a":"はい"},{"q":"近所の人は曲を聞いて家を出て、どこかへ向かいますか？","a":"はい"},{"q":"向かう先は店ですか？","a":"いいえ"},{"q":"向かう先は学校ですか？","a":"いいえ"},{"q":"店の近くに乗り物の停留所がありますか？","a":"はい"},{"q":"それは電車ですか？","a":"いいえ"},{"q":"バスに関係がありますか？","a":"はい"},{"q":"バスは本数が少ないですか？","a":"はい"},{"q":"曲のジャンルは重要ですか？","a":"関係ない"},{"q":"店主はお金をもらってやっていますか？","a":"いいえ"},{"q":"近所の人は時計を持っていませんか？","a":"関係ない"},{"q":"店で何を売っていますか？","a":"関係ない"},{"q":"店主はバスが来る前に曲を流して、近所の人に知らせている？","a":"正解"}]',
        '曲が鳴ると走り出す町', '「はい / いいえ / 関係ない」で答えられる質問をコメントしてね。出題者が全部返事します',
        '{"problem":"町の小さな商店の主人は、毎日決まった時刻に、店の外へ向けて同じ曲を大きな音で流す。客を呼ぶためではない。近所の人はその曲を聞くと、あわてて家を飛び出す。なぜ？","rule":"はい、いいえ、関係ない、で答えられる質問をコメントしてね。全部返事するよ。"}',
        '[{"role":"questioner","text":"店の宣伝の曲？"},{"role":"master","text":"いいえ。"},{"role":"questioner","text":"時間を知らせてる？"},{"role":"master","text":"はい！"},{"role":"questioner","text":"店は何屋さん？"},{"role":"master","text":"関係ありません。"}]',
        '{"master":{"intro":"質問してみて！","outro":"何度でも答えるよ。コメントで質問！"},"jr":{"outro":"面白かったら、いいね、フォローよろしくね！"}}',
        'A stylized 1990s Japanese OVA anime background painting (hand-painted cel-era background art, poster-color textures, clean shapes, thick brush-like outlines on key objects). Mid-key lighting: moonlight, lamps or candlelight keep the whole scene clearly visible, NOT dark.

Scene: A small old-fashioned shop on a quiet street in a Japanese town in the late afternoon, with a loudspeaker mounted under the shop''s awning; a shopkeeper in an apron standing at the doorway; a few small houses along the street; a wide clear sky above.

Vertical 9:16 composition (1024x1536). No text, no letters, no numbers, no logos, no signs. Depict only the scene described in the problem statement; do not depict any clue to the story''s hidden truth. People: only the persons who appear in the problem, plus at most one distant silhouette. Keep the upper 55% of the image calm and simple (sky, wall, ceiling, window) so that text cards can be overlaid there.',
        '【探偵カメロックのウミガメのスープ】
毎日同じ時刻、商店から同じ曲が流れます。

町の小さな商店の主人は、毎日決まった時刻に、店の外へ向けて同じ曲を大きな音で流す。客を呼ぶためではない。近所の人はその曲を聞くと、あわてて家を飛び出す。なぜ？

「はい / いいえ / 関係ない」で答えられる質問をコメントしてね。出題者の探偵カメロックが全部返事します。正解が出るまで何度でもどうぞ。

#ウミガメのスープ #水平思考 #推理クイズ #なぞなぞ #謎解き #クイズ #AIart',
        '完全オリジナル（既存問題の転載・改変ではない）。作問法は note 記事 https://note.com/suekai0217/n/n35128e606a9b の4 ステップ（モチーフ → 連想 → 言い方を変える → 不思議にする）と良い問題の 3 条件（コアが明確・動線がある・現実離れしない）に従う。着想の型は research.md（Codex Web リサーチ台帳）を参照。 型: 物語復元型（A→C 切り出し）。モチーフ「商店街の音楽」→ 連想「客寄せ・時報・合図」→ 常識「店が流す音楽は客のため」の逆。着想元の既存問題なし（研究台帳の「BGM の実用的役割」構造を参照）。', 1);

-- U05 割れた皿と焦げた鍋
INSERT INTO umigame_stock_items (set_id, content_key, title, difficulty, problem_text, truth, fact_sheet,
    expected_questions, hook, rule_text, narration, play_example, character_lines, illustration_prompt,
    caption, source_note, is_active)
VALUES ((SELECT id FROM batch_sets WHERE set_code = 'umigame-soup-1'),
        '005-broken-plate', '割れた皿と焦げた鍋', 2,
        '夜、仕事から帰った母は、台所で割れた皿と黒く焦げた鍋を見つけた。ところが母は、小学生の子どもを叱るどころか、涙を流しながら子どもを何度も強く抱きしめた。なぜ？',
        'その日は母の誕生日。子どもは母を驚かせようと、初めて一人で料理を作ろうとして失敗した。テーブルには焦げたけれど盛りつけられた料理と「おたんじょうびおめでとう」と書いた紙があり、母はその気持ちに泣いた。',
        '["その日は母の誕生日である","子どもは母を驚かせるため、初めて一人で料理を作ろうとした","料理の途中で皿を割り、鍋を焦がしてしまった","テーブルには、焦げた料理と「おたんじょうびおめでとう」と書いた紙が置かれていた","母は子どもの気持ちがうれしくて泣いた","子どもはけがをしていない","家は火事になっていない","母は子どもの行動を叱っていない","父親や兄弟の有無は問題に関係ない","料理の種類は問題に関係ない"]',
        '[{"q":"子どもはけがをしましたか？","a":"いいえ"},{"q":"家は火事になりましたか？","a":"いいえ"},{"q":"母は子どもに怒っていますか？","a":"いいえ"},{"q":"子どもは料理をしようとしましたか？","a":"はい"},{"q":"子どもは自分のために料理をしたのですか？","a":"いいえ"},{"q":"子どもは母のために料理をしましたか？","a":"はい"},{"q":"その日は特別な日ですか？","a":"はい"},{"q":"それは子どもの誕生日ですか？","a":"いいえ"},{"q":"母の誕生日ですか？","a":"はい"},{"q":"母は悲しくて泣いたのですか？","a":"いいえ"},{"q":"母はうれしくて泣いたのですか？","a":"はい"},{"q":"料理は何ですか？","a":"関係ない"},{"q":"父親は関係ありますか？","a":"関係ない"},{"q":"子どもは何歳ですか？","a":"関係ない"},{"q":"割れた皿は高価な皿でしたか？","a":"関係ない"},{"q":"子どもは泥棒に襲われましたか？","a":"いいえ"},{"q":"子どもがお母さんの誕生日に料理を作ろうとして失敗して、お母さんはその気持ちに泣いた？","a":"正解"}]',
        '叱らずに抱きしめた理由', '「はい / いいえ / 関係ない」で答えられる質問をコメントしてね。出題者が全部返事します',
        '{"problem":"夜、仕事から帰った母は、台所で割れた皿と、黒く焦げた鍋を見つけた。ところが母は、小学生の子どもを叱るどころか、涙を流しながら子どもを何度も強く抱きしめた。なぜ？","rule":"はい、いいえ、関係ない、で答えられる質問をコメントしてね。全部返事するよ。"}',
        '[{"role":"questioner","text":"子どもはけがした？"},{"role":"master","text":"いいえ。"},{"role":"questioner","text":"その日は特別な日？"},{"role":"master","text":"はい！"},{"role":"questioner","text":"料理は何？"},{"role":"master","text":"関係ありません。"}]',
        '{"master":{"intro":"質問してみて！","outro":"何度でも答えるよ。コメントで質問！"},"jr":{"outro":"面白かったら、いいね、フォローよろしくね！"}}',
        'A stylized 1990s Japanese OVA anime background painting (hand-painted cel-era background art, poster-color textures, clean shapes, thick brush-like outlines on key objects). Mid-key lighting: moonlight, lamps or candlelight keep the whole scene clearly visible, NOT dark.

Scene: A small home kitchen in the evening: a mother in work clothes with a handbag stands frozen at the kitchen doorway; on the floor, pieces of a broken plate; a blackened pot on the stove; a young child in an oversized apron stands nearby looking down; warm ceiling light; plain wall and cupboard above.

Vertical 9:16 composition (1024x1536). No text, no letters, no numbers, no logos, no signs. Depict only the scene described in the problem statement; do not depict any clue to the story''s hidden truth. People: only the persons who appear in the problem, plus at most one distant silhouette. Keep the upper 55% of the image calm and simple (sky, wall, ceiling, window) so that text cards can be overlaid there.',
        '【探偵カメロックのウミガメのスープ】
台所には割れた皿と焦げた鍋。それでもお母さんは叱りませんでした。

夜、仕事から帰った母は、台所で割れた皿と黒く焦げた鍋を見つけた。ところが母は、小学生の子どもを叱るどころか、涙を流しながら子どもを何度も強く抱きしめた。なぜ？

「はい / いいえ / 関係ない」で答えられる質問をコメントしてね。出題者の探偵カメロックが全部返事します。正解が出るまで何度でもどうぞ。

#ウミガメのスープ #水平思考 #推理クイズ #なぞなぞ #謎解き #クイズ #AIart',
        '完全オリジナル（既存問題の転載・改変ではない）。作問法は note 記事 https://note.com/suekai0217/n/n35128e606a9b の4 ステップ（モチーフ → 連想 → 言い方を変える → 不思議にする）と良い問題の 3 条件（コアが明確・動線がある・現実離れしない）に従う。着想の型は research.md（Codex Web リサーチ台帳）を参照。 型: 物語復元型（A→C 切り出し）。モチーフ「台所の失敗」→ 連想「叱る・片づける・料理」→ 常識「皿を割った子は叱られる」の逆。着想元の既存問題なし。', 1);

-- U06 妻に打たれたものを食べる男
INSERT INTO umigame_stock_items (set_id, content_key, title, difficulty, problem_text, truth, fact_sheet,
    expected_questions, hook, rule_text, narration, play_example, character_lines, illustration_prompt,
    caption, source_note, is_active)
VALUES ((SELECT id FROM batch_sets WHERE set_code = 'umigame-soup-1'),
        '006-udon-strike', '妻に打たれたものを食べる男', 2,
        '男は毎朝、妻に打たれたものをうれしそうに食べる。しかも近所の人たちは、お金を払ってまで妻に打たれたものを持ち帰る。妻が打ち始めて、もう 30 年になる。なぜ？',
        '妻はうどん職人。「打つ」のは手打ちうどんの麺のことで、男は毎朝妻の打ったうどんを食べ、近所の人は妻の店で手打ちうどんを買っている。',
        '["妻はうどん店を営むうどん職人である","「打たれたもの」とは、妻が手打ちしたうどんの麺である","妻が「打つ」のは麺であり、人を叩いているのではない","男は毎朝、妻の作った手打ちうどんを朝食に食べている","近所の人は妻の店で手打ちうどんを買って持ち帰る","男と妻の夫婦仲は良い","暴力や事件は一切起きていない","男の職業は問題に関係ない","うどんの味付けや値段は問題に関係ない"]',
        '[{"q":"妻は男を殴っていますか？","a":"いいえ"},{"q":"男はけがをしていますか？","a":"いいえ"},{"q":"「打つ」は人を叩くことですか？","a":"いいえ"},{"q":"打たれたものは食べ物ですか？","a":"はい"},{"q":"打たれたものは太鼓ですか？","a":"いいえ"},{"q":"打たれたものは麺ですか？","a":"はい"},{"q":"それはそばですか？","a":"いいえ"},{"q":"それはうどんですか？","a":"はい"},{"q":"妻は料理の仕事をしていますか？","a":"はい"},{"q":"妻はお店を持っていますか？","a":"はい"},{"q":"男の職業は関係ありますか？","a":"関係ない"},{"q":"男は妻が怖いのですか？","a":"いいえ"},{"q":"夫婦の仲は良いですか？","a":"はい"},{"q":"30 年前に何か事件がありましたか？","a":"いいえ"},{"q":"うどんの値段はいくらですか？","a":"関係ない"},{"q":"奥さんは手打ちうどんの職人で、打たれたものはうどんのこと？","a":"正解"}]',
        '妻に打たれて、うれしい？', '「はい / いいえ / 関係ない」で答えられる質問をコメントしてね。出題者が全部返事します',
        '{"problem":"男は毎朝、妻に打たれたものを、うれしそうに食べる。しかも近所の人たちは、お金を払ってまで、妻に打たれたものを持ち帰る。妻が打ち始めて、もう 30 年になる。なぜ？","rule":"はい、いいえ、関係ない、で答えられる質問をコメントしてね。全部返事するよ。"}',
        '[{"role":"questioner","text":"奥さんは怖い人？"},{"role":"master","text":"いいえ。"},{"role":"questioner","text":"打つのは人じゃない？"},{"role":"master","text":"はい！"},{"role":"questioner","text":"旦那さんの仕事は？"},{"role":"master","text":"関係ありません。"}]',
        '{"master":{"intro":"質問してみて！","outro":"何度でも答えるよ。コメントで質問！"},"jr":{"outro":"面白かったら、いいね、フォローよろしくね！"}}',
        'A stylized 1990s Japanese OVA anime background painting (hand-painted cel-era background art, poster-color textures, clean shapes, thick brush-like outlines on key objects). Mid-key lighting: moonlight, lamps or candlelight keep the whole scene clearly visible, NOT dark.

Scene: Early morning in a modest Japanese home dining room: a middle-aged man sits at a low table smiling with chopsticks in hand, a steaming bowl in front of him; a woman in a work apron and head towel stands at the doorway to the kitchen with her arms folded, smiling; soft morning light through a paper screen window; plain wall above.

Vertical 9:16 composition (1024x1536). No text, no letters, no numbers, no logos, no signs. Depict only the scene described in the problem statement; do not depict any clue to the story''s hidden truth. People: only the persons who appear in the problem, plus at most one distant silhouette. Keep the upper 55% of the image calm and simple (sky, wall, ceiling, window) so that text cards can be overlaid there.',
        '【探偵カメロックのウミガメのスープ】
奥さんに打たれたものを、毎朝うれしそうに食べる男の話。

男は毎朝、妻に打たれたものをうれしそうに食べる。しかも近所の人たちは、お金を払ってまで妻に打たれたものを持ち帰る。妻が打ち始めて、もう 30 年になる。なぜ？

「はい / いいえ / 関係ない」で答えられる質問をコメントしてね。出題者の探偵カメロックが全部返事します。正解が出るまで何度でもどうぞ。

#ウミガメのスープ #水平思考 #推理クイズ #なぞなぞ #謎解き #クイズ #AIart',
        '完全オリジナル（既存問題の転載・改変ではない）。作問法は note 記事 https://note.com/suekai0217/n/n35128e606a9b の4 ステップ（モチーフ → 連想 → 言い方を変える → 不思議にする）と良い問題の 3 条件（コアが明確・動線がある・現実離れしない）に従う。着想の型は research.md（Codex Web リサーチ台帳）を参照。 型: 意味誤誘導型。モチーフ「うどん」→ 連想「打つ・手打ち」→ 抽象化（麺を打つ → 打たれたもの）→ 常識「打たれる = 暴力」の逆。着想元の既存問題なし（研究台帳の「作業と事件の両方に使える動詞」構造を参照）。', 1);

-- U07 30 人全員を落とした先生
INSERT INTO umigame_stock_items (set_id, content_key, title, difficulty, problem_text, truth, fact_sheet,
    expected_questions, hook, rule_text, narration, play_example, character_lines, illustration_prompt,
    caption, source_note, is_active)
VALUES ((SELECT id FROM batch_sets WHERE set_code = 'umigame-soup-1'),
        '007-weight-loss-teacher', '30 人全員を落とした先生', 2,
        '先生はこの 1 か月で、教え子 30 人を全員落とした。落とされた 30 人はそれをまわりに自慢し、そろって先生に感謝している。先生は落とした人数で評価が上がる。なぜ？',
        '先生はスポーツジムのトレーナー。「落とした」のは会員の体重で、30 人全員が目標どおり減量に成功した。',
        '["先生はスポーツジムのトレーナーである","「落とした」のは、教え子たちの体重である","教え子 30 人は 1 か月の減量プログラムに参加しているジムの会員で、会費を払っている","教え子は病人ではなく、健康な一般の会員である","落としたのは物ではなく、体重という数値である","30 人全員が目標どおりに体重を落とすことに成功した","教え子たちは減量できたことを喜び、先生に感謝している","先生は会員の減量の成果で評価される","試験や成績の合否は一切関係していない","先生が人を高いところから落としたわけではない","教え子の年齢や性別は問題に関係ない","ジムの場所や料金の額は問題に関係ない"]',
        '[{"q":"先生は学校の先生ですか？","a":"いいえ"},{"q":"落としたのは試験の成績ですか？","a":"いいえ"},{"q":"落としたのは人そのものですか？","a":"いいえ"},{"q":"落としたのは物ですか？","a":"いいえ"},{"q":"落としたのは教え子の体に関係がありますか？","a":"はい"},{"q":"体重のことですか？","a":"はい"},{"q":"先生はスポーツに関わる仕事ですか？","a":"はい"},{"q":"先生はジムで働いていますか？","a":"はい"},{"q":"教え子は病人ですか？","a":"いいえ"},{"q":"教え子は喜んでいますか？","a":"はい"},{"q":"教え子の年齢は重要ですか？","a":"関係ない"},{"q":"先生は男性ですか？","a":"関係ない"},{"q":"教え子はお金を払っていますか？","a":"はい"},{"q":"先生は誰かをいじめていますか？","a":"いいえ"},{"q":"落とした数が多いほど先生の評価は上がりますか？","a":"はい"},{"q":"先生はジムのトレーナーで、落としたのは体重？","a":"正解"}]',
        '30 人全員を落とした先生', '「はい / いいえ / 関係ない」で答えられる質問をコメントしてね。出題者が全部返事します',
        '{"problem":"先生はこの 1 か月で、教え子 30 人を全員落とした。落とされた 30 人は、それをまわりに自慢し、そろって先生に感謝している。先生は、落とした人数で評価が上がる。なぜ？","rule":"はい、いいえ、関係ない、で答えられる質問をコメントしてね。全部返事するよ。"}',
        '[{"role":"questioner","text":"テストで落とした？"},{"role":"master","text":"いいえ。"},{"role":"questioner","text":"体に関係ある？"},{"role":"master","text":"はい！"},{"role":"questioner","text":"先生は男の人？"},{"role":"master","text":"関係ありません。"}]',
        '{"master":{"intro":"質問してみて！","outro":"何度でも答えるよ。コメントで質問！"},"jr":{"outro":"面白かったら、いいね、フォローよろしくね！"}}',
        'A stylized 1990s Japanese OVA anime background painting (hand-painted cel-era background art, poster-color textures, clean shapes, thick brush-like outlines on key objects). Mid-key lighting: moonlight, lamps or candlelight keep the whole scene clearly visible, NOT dark.

Scene: A plain community hall with a polished wooden floor in the morning: an instructor in a track jacket holding a clipboard stands in front of rows of cheerful adults of various ages in casual clothes; tall windows with bright daylight; a simple high ceiling and bare wall above.

Vertical 9:16 composition (1024x1536). No text, no letters, no numbers, no logos, no signs. Depict only the scene described in the problem statement; do not depict any clue to the story''s hidden truth. People: only the persons who appear in the problem, plus at most one distant silhouette. Keep the upper 55% of the image calm and simple (sky, wall, ceiling, window) so that text cards can be overlaid there.',
        '【探偵カメロックのウミガメのスープ】
教え子を全員落として、感謝される先生がいます。

先生はこの 1 か月で、教え子 30 人を全員落とした。落とされた 30 人はそれをまわりに自慢し、そろって先生に感謝している。先生は落とした人数で評価が上がる。なぜ？

「はい / いいえ / 関係ない」で答えられる質問をコメントしてね。出題者の探偵カメロックが全部返事します。正解が出るまで何度でもどうぞ。

#ウミガメのスープ #水平思考 #推理クイズ #なぞなぞ #謎解き #クイズ #AIart',
        '完全オリジナル（既存問題の転載・改変ではない）。作問法は note 記事 https://note.com/suekai0217/n/n35128e606a9b の4 ステップ（モチーフ → 連想 → 言い方を変える → 不思議にする）と良い問題の 3 条件（コアが明確・動線がある・現実離れしない）に従う。着想の型は research.md（Codex Web リサーチ台帳）を参照。 型: 意味誤誘導型。モチーフ「ダイエット」→ 連想「体重を落とす」→ 抽象化（落とす）→ 常識「先生に落とされる = 不合格」の逆。着想元の既存問題なし。', 1);

-- U08 毎朝みんなを泣かせる男
INSERT INTO umigame_stock_items (set_id, content_key, title, difficulty, problem_text, truth, fact_sheet,
    expected_questions, hook, rule_text, narration, play_example, character_lines, illustration_prompt,
    caption, source_note, is_active)
VALUES ((SELECT id FROM batch_sets WHERE set_code = 'umigame-soup-1'),
        '008-onion-tears', '毎朝みんなを泣かせる男', 2,
        '男が毎朝、店の奥で仕事を始めると、店の人たちは次々に泣き出す。泣いた人たちは男を責めず、翌朝もまた同じ店で同じように泣く。男は意地悪もいじめも一度もしていない。なぜ？',
        '男は食堂の厨房の下ごしらえ係で、毎朝大量の玉ねぎを刻んでいる。その刺激で厨房の仲間たちは目にしみて涙が出る。',
        '["男は食堂の厨房で働く下ごしらえ係である","男は毎朝、大量の玉ねぎをみじん切りにしている","店の人たちが泣くのは、玉ねぎの刺激で目にしみるからである","泣いているのは厨房で一緒に働く仲間たちである","泣いている人たちは悲しいわけではない","男は誰にも意地悪やいじめをしていない","泣いた人たちは男を責めず、いつものことだと分かっている","客は泣いていない","店で出す料理の種類や店の場所は問題に関係ない","男の年齢や性格は問題に関係ない"]',
        '[{"q":"泣いている人は悲しいのですか？","a":"いいえ"},{"q":"男は人をいじめていますか？","a":"いいえ"},{"q":"男は音楽や映画で人を感動させていますか？","a":"いいえ"},{"q":"泣いているのは客ですか？","a":"いいえ"},{"q":"泣いているのは店で働く人ですか？","a":"はい"},{"q":"男の仕事は料理に関係がありますか？","a":"はい"},{"q":"男は何かを切っていますか？","a":"はい"},{"q":"泣くのは目にしみるからですか？","a":"はい"},{"q":"それは玉ねぎですか？","a":"はい"},{"q":"それは唐辛子ですか？","a":"いいえ"},{"q":"店の場所は重要ですか？","a":"関係ない"},{"q":"男は泣いている人に謝りますか？","a":"関係ない"},{"q":"男は人を殴っていますか？","a":"いいえ"},{"q":"店は何のお店ですか？","a":"関係ない"},{"q":"男は泣かせて楽しんでいますか？","a":"いいえ"},{"q":"男が毎朝玉ねぎを刻んでいて、目にしみて周りの人が泣く？","a":"正解"}]',
        '毎朝みんなを泣かせる男', '「はい / いいえ / 関係ない」で答えられる質問をコメントしてね。出題者が全部返事します',
        '{"problem":"男が毎朝、店の奥で仕事を始めると、店の人たちは次々に泣き出す。泣いた人たちは男を責めず、翌朝もまた同じ店で、同じように泣く。男は意地悪もいじめも、一度もしていない。なぜ？","rule":"はい、いいえ、関係ない、で答えられる質問をコメントしてね。全部返事するよ。"}',
        '[{"role":"questioner","text":"悲しくて泣いてる？"},{"role":"master","text":"いいえ。"},{"role":"questioner","text":"男は料理をしてる？"},{"role":"master","text":"はい！"},{"role":"questioner","text":"店の場所はどこ？"},{"role":"master","text":"関係ありません。"}]',
        '{"master":{"intro":"質問してみて！","outro":"何度でも答えるよ。コメントで質問！"},"jr":{"outro":"面白かったら、いいね、フォローよろしくね！"}}',
        'A stylized 1990s Japanese OVA anime background painting (hand-painted cel-era background art, poster-color textures, clean shapes, thick brush-like outlines on key objects). Mid-key lighting: moonlight, lamps or candlelight keep the whole scene clearly visible, NOT dark.

Scene: The back area of a small restaurant kitchen in the early morning: a man in a white cook''s uniform and cap stands at a steel counter with his back to the viewer, working on something hidden from view; two coworkers nearby wipe their eyes with their sleeves; a little steam and soft morning light; a simple tiled wall above.

Vertical 9:16 composition (1024x1536). No text, no letters, no numbers, no logos, no signs. Depict only the scene described in the problem statement; do not depict any clue to the story''s hidden truth. People: only the persons who appear in the problem, plus at most one distant silhouette. Keep the upper 55% of the image calm and simple (sky, wall, ceiling, window) so that text cards can be overlaid there.',
        '【探偵カメロックのウミガメのスープ】
この男が仕事を始めると、店のみんなが泣き出します。

男が毎朝、店の奥で仕事を始めると、店の人たちは次々に泣き出す。泣いた人たちは男を責めず、翌朝もまた同じ店で同じように泣く。男は意地悪もいじめも一度もしていない。なぜ？

「はい / いいえ / 関係ない」で答えられる質問をコメントしてね。出題者の探偵カメロックが全部返事します。正解が出るまで何度でもどうぞ。

#ウミガメのスープ #水平思考 #推理クイズ #なぞなぞ #謎解き #クイズ #AIart',
        '完全オリジナル（既存問題の転載・改変ではない）。作問法は note 記事 https://note.com/suekai0217/n/n35128e606a9b の4 ステップ（モチーフ → 連想 → 言い方を変える → 不思議にする）と良い問題の 3 条件（コアが明確・動線がある・現実離れしない）に従う。着想の型は research.md（Codex Web リサーチ台帳）を参照。 型: 意味誤誘導型。モチーフ「玉ねぎ」→ 連想「切ると涙」→ 抽象化（泣かせる）→ 常識「人を泣かせる = ひどいことをする」の逆。着想元の既存問題なし。', 1);

-- U09 負けるほど給料が上がる男
INSERT INTO umigame_stock_items (set_id, content_key, title, difficulty, problem_text, truth, fact_sheet,
    expected_questions, hook, rule_text, narration, play_example, character_lines, illustration_prompt,
    caption, source_note, is_active)
VALUES ((SELECT id FROM batch_sets WHERE set_code = 'umigame-soup-1'),
        '009-villain-actor', '負けるほど給料が上がる男', 2,
        '男は毎週、大勢の子どもたちの前で戦い、必ず負ける。子どもたちに「やめろ」と叫ばれ、最後には殴られて倒れる。それでも男は、負けるたびに給料が上がっていった。なぜ？',
        '男は遊園地のヒーローショーで悪役を演じるスーツアクター。子どもたちを盛り上げ、ヒーローに派手にやられる演技が上手で、ショーの人気が出るほど評価と給料が上がった。',
        '["男は遊園地のヒーローショーで悪役を演じる俳優（スーツアクター）である","男はマスクとスーツで顔を隠している","男を殴って倒すのは、ショーのヒーロー役である","子どもたちが「やめろ」と叫ぶのはショーの盛り上がりであり、本気の怒りではない","戦いは台本どおりの演技で、男は本当にけがをしていない","男は負ける演技が上手で、ショーの人気に貢献している","ショーの人気が上がるほど男の評価と給料が上がる","男は犯罪者でも本物の悪人でもない","子どもたちは男の正体（役者）を知らない","ヒーローの名前・遊園地の場所・男の体格は問題に関係ない"]',
        '[{"q":"男は本当にけがをしますか？","a":"いいえ"},{"q":"男はスポーツ選手ですか？","a":"いいえ"},{"q":"男は本当に悪いことをしていますか？","a":"いいえ"},{"q":"戦いは演技ですか？","a":"はい"},{"q":"男は俳優のような仕事ですか？","a":"はい"},{"q":"男を殴るのは子どもですか？","a":"いいえ"},{"q":"男を殴るのはヒーローですか？","a":"はい"},{"q":"男は悪役を演じていますか？","a":"はい"},{"q":"子どもたちは男を本気で嫌っていますか？","a":"いいえ"},{"q":"これはテレビの撮影ですか？","a":"いいえ"},{"q":"これは遊園地などのショーですか？","a":"はい"},{"q":"男は顔を隠していますか？","a":"はい"},{"q":"ヒーローの名前は重要ですか？","a":"関係ない"},{"q":"男の身長は重要ですか？","a":"関係ない"},{"q":"給料を払っているのは子どもですか？","a":"いいえ"},{"q":"男はヒーローショーの悪役で、やられ役が上手いから給料が上がる？","a":"正解"}]',
        '負けるほど給料が上がる', '「はい / いいえ / 関係ない」で答えられる質問をコメントしてね。出題者が全部返事します',
        '{"problem":"男は毎週、大勢の子どもたちの前で戦い、必ず負ける。子どもたちに、やめろと叫ばれ、最後には殴られて倒れる。それでも男は、負けるたびに給料が上がっていった。なぜ？","rule":"はい、いいえ、関係ない、で答えられる質問をコメントしてね。全部返事するよ。"}',
        '[{"role":"questioner","text":"本当に殴られてる？"},{"role":"master","text":"いいえ。"},{"role":"questioner","text":"男は演技してる？"},{"role":"master","text":"はい！"},{"role":"questioner","text":"男の身長は高い？"},{"role":"master","text":"関係ありません。"}]',
        '{"master":{"intro":"質問してみて！","outro":"何度でも答えるよ。コメントで質問！"},"jr":{"outro":"面白かったら、いいね、フォローよろしくね！"}}',
        'A stylized 1990s Japanese OVA anime background painting (hand-painted cel-era background art, poster-color textures, clean shapes, thick brush-like outlines on key objects). Mid-key lighting: moonlight, lamps or candlelight keep the whole scene clearly visible, NOT dark.

Scene: An outdoor stage on a sunny weekend afternoon: rows of excited children sitting on the ground in front of a low stage with colorful curtains; a single figure stands on the stage seen from behind in a dramatic pose; a few balloons; a wide bright sky above.

Vertical 9:16 composition (1024x1536). No text, no letters, no numbers, no logos, no signs. Depict only the scene described in the problem statement; do not depict any clue to the story''s hidden truth. People: only the persons who appear in the problem, plus at most one distant silhouette. Keep the upper 55% of the image calm and simple (sky, wall, ceiling, window) so that text cards can be overlaid there.',
        '【探偵カメロックのウミガメのスープ】
負けるたびに給料が上がる、ちょっと変わった男の仕事。

男は毎週、大勢の子どもたちの前で戦い、必ず負ける。子どもたちに「やめろ」と叫ばれ、最後には殴られて倒れる。それでも男は、負けるたびに給料が上がっていった。なぜ？

「はい / いいえ / 関係ない」で答えられる質問をコメントしてね。出題者の探偵カメロックが全部返事します。正解が出るまで何度でもどうぞ。

#ウミガメのスープ #水平思考 #推理クイズ #なぞなぞ #謎解き #クイズ #AIart',
        '完全オリジナル（既存問題の転載・改変ではない）。作問法は note 記事 https://note.com/suekai0217/n/n35128e606a9b の4 ステップ（モチーフ → 連想 → 言い方を変える → 不思議にする）と良い問題の 3 条件（コアが明確・動線がある・現実離れしない）に従う。着想の型は research.md（Codex Web リサーチ台帳）を参照。 型: 意味誤誘導型（常識の逆）。モチーフ「ヒーローショー」→ 連想「悪役・やられ役・子ども」→ 常識「負ける・殴られる = 悪いこと」の逆。着想元の既存問題なし。', 1);

-- U10 電車が一本も来ない駅
INSERT INTO umigame_stock_items (set_id, content_key, title, difficulty, problem_text, truth, fact_sheet,
    expected_questions, hook, rule_text, narration, play_example, character_lines, illustration_prompt,
    caption, source_note, is_active)
VALUES ((SELECT id FROM batch_sets WHERE set_code = 'umigame-soup-1'),
        '010-station-no-train', '電車が一本も来ない駅', 1,
        '男は毎朝、駅で野菜を買い、駅で朝ごはんを食べてから仕事へ向かう。この駅には線路もなく、電車もバスも一本も来ない。それでも毎日、朝から大勢の人でにぎわっている。なぜ？',
        'それは「道の駅」。幹線道路沿いにある、車で立ち寄る休憩施設で、地元の野菜の直売所や食堂がある。男は車で通勤する途中に立ち寄っている。',
        '["この「駅」は道の駅である","道の駅は幹線道路沿いにある、車で立ち寄る休憩施設である","道の駅には地元の農産物の直売所と食堂がある","男は毎朝、車で通勤する途中に道の駅へ立ち寄っている","にぎわっている人々も車で来ている","線路・電車・バスはこの駅には関係がない","男は鉄道関係の仕事ではない","道の駅の名前や場所（県）は問題に関係ない","男が買う野菜の種類や朝ごはんの内容は問題に関係ない"]',
        '[{"q":"この駅は鉄道の駅ですか？","a":"いいえ"},{"q":"昔は電車が来ていましたか？","a":"いいえ"},{"q":"人々は歩いて来ますか？","a":"いいえ"},{"q":"人々は車で来ますか？","a":"はい"},{"q":"この駅は道路のそばにありますか？","a":"はい"},{"q":"ここでは野菜を売っていますか？","a":"はい"},{"q":"ここに食堂はありますか？","a":"はい"},{"q":"男は駅で働いていますか？","a":"いいえ"},{"q":"男の仕事は重要ですか？","a":"関係ない"},{"q":"男は車で通勤していますか？","a":"はい"},{"q":"これは空港ですか？","a":"いいえ"},{"q":"「駅」という名前がついた施設ですか？","a":"はい"},{"q":"男が買う野菜は何ですか？","a":"関係ない"},{"q":"その駅は海の近くですか？","a":"関係ない"},{"q":"それは道の駅ですか？","a":"正解"}]',
        '電車が一本も来ない駅', '「はい / いいえ / 関係ない」で答えられる質問をコメントしてね。出題者が全部返事します',
        '{"problem":"男は毎朝、駅で野菜を買い、駅で朝ごはんを食べてから仕事へ向かう。この駅には線路もなく、電車もバスも一本も来ない。それでも毎日、朝から大勢の人でにぎわっている。なぜ？","rule":"はい、いいえ、関係ない、で答えられる質問をコメントしてね。全部返事するよ。"}',
        '[{"role":"questioner","text":"昔は電車が来た？"},{"role":"master","text":"いいえ。"},{"role":"questioner","text":"みんな車で来る？"},{"role":"master","text":"はい！"},{"role":"questioner","text":"男の仕事は？"},{"role":"master","text":"関係ありません。"}]',
        '{"master":{"intro":"質問してみて！","outro":"何度でも答えるよ。コメントで質問！"},"jr":{"outro":"面白かったら、いいね、フォローよろしくね！"}}',
        'A stylized 1990s Japanese OVA anime background painting (hand-painted cel-era background art, poster-color textures, clean shapes, thick brush-like outlines on key objects). Mid-key lighting: moonlight, lamps or candlelight keep the whole scene clearly visible, NOT dark.

Scene: A bright early morning at the entrance of a low wooden building in the countryside: an open-air market stall with baskets of fresh vegetables and a small eatery with a steaming pot; a man holding a shopping bag; green mountains behind and a wide clear sky above.

Vertical 9:16 composition (1024x1536). No text, no letters, no numbers, no logos, no signs. Depict only the scene described in the problem statement; do not depict any clue to the story''s hidden truth. People: only the persons who appear in the problem, plus at most one distant silhouette. Keep the upper 55% of the image calm and simple (sky, wall, ceiling, window) so that text cards can be overlaid there.',
        '【探偵カメロックのウミガメのスープ】
電車もバスも来ないのに、毎朝にぎわう駅があります。

男は毎朝、駅で野菜を買い、駅で朝ごはんを食べてから仕事へ向かう。この駅には線路もなく、電車もバスも一本も来ない。それでも毎日、朝から大勢の人でにぎわっている。なぜ？

「はい / いいえ / 関係ない」で答えられる質問をコメントしてね。出題者の探偵カメロックが全部返事します。正解が出るまで何度でもどうぞ。

#ウミガメのスープ #水平思考 #推理クイズ #なぞなぞ #謎解き #クイズ #AIart',
        '完全オリジナル（既存問題の転載・改変ではない）。作問法は note 記事 https://note.com/suekai0217/n/n35128e606a9b の4 ステップ（モチーフ → 連想 → 言い方を変える → 不思議にする）と良い問題の 3 条件（コアが明確・動線がある・現実離れしない）に従う。着想の型は research.md（Codex Web リサーチ台帳）を参照。 型: 意味誤誘導型。モチーフ「駅」→ 連想「電車・野菜の直売・道の駅」→ 抽象化（駅）→ 常識「駅には電車が来る」の逆。着想元の既存問題なし（研究台帳の「建物以外にも成立する場所語」構造を参照）。', 1);
