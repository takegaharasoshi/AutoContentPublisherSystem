-- batch-01 ウミガメストック投入（14 問。人間レビュー + プローブテスト承認後に実行）
-- 生成元: content/umigame-stock/umigame-soup-1/batch-01/stock_items.py（単一ソース）。適用先: ローカル MySQL / Aurora（acps）
-- set_id は set_code から解決するため両環境共通で実行できる。content_key は stock_items.py で採番済み。

-- batch_sets 行（is_active = 0 で登録。稼働化は 21-7 の人間ゲート。既存なら作らない）
INSERT INTO batch_sets (set_code, name, generator_name, is_active)
SELECT 'umigame-soup-1', '探偵カメロックのウミガメのスープ', 'umigame-prebuilt', 0
WHERE NOT EXISTS (SELECT 1 FROM batch_sets WHERE set_code = 'umigame-soup-1');

-- U01 影が薄いと言われて喜ぶ男
INSERT INTO umigame_stock_items (set_id, content_key, title, difficulty, problem_text, truth, fact_sheet,
    expected_questions, hook, rule_text, narration, play_example, character_lines, illustration_prompt,
    caption, source_note, is_active)
VALUES ((SELECT id FROM batch_sets WHERE set_code = 'umigame-soup-1'),
        '001-faint-shadow', '影が薄いと言われて喜ぶ男', 4,
        '久しぶりに会った相手から「影がずいぶん薄くなった」と言われて、男は泣いて喜んだ。そう言った相手もにこにこ笑っていて、男は相手に何度も頭を下げた。どういうこと？',
        '「影」は男の存在感のことではなく、レントゲン写真に白く写る病気の跡のこと。男は以前、健康診断のレントゲンで肺に影が見つかり、影が濃くなっていると告げられて治療を続けてきた。今日、3 か月ぶりの検査で主治医から「影がずいぶん薄くなった」と言われた。病気が良くなっている証拠なので、男はうれしくて泣き、治してくれた医者に何度も頭を下げた。医者も回復を喜んで笑っていた。',
        '["「影」は太陽や照明でできる足元の影のことではない","「影」は男の存在感や性格のことでもない","「影」は男の体を写した写真の中にある","「影」が何に写った何の影なのかは、この問題の答えの核心である（正解宣言のとき以外は補足で言わない）","言った相手は男の友だち・家族・恋人・職場の人ではない","男はその相手のところへ以前から定期的に通っていて、今日は 3 か月ぶりに会った（入院はしていない）","以前、影が濃くなっていると分かって、男はひどく落ち込んだことがある","今日の涙はうれし涙で、良い知らせだったからである","男が頭を下げたのは相手への感謝で、相手が笑っていたのは良い知らせを伝えられたからである","相手は男をからかったり、意地悪で言ったりしていない","男の年齢・職業・家族の有無は問題に関係ない","病気の名前・治療の内容は問題に関係ない"]',
        '[{"q":"影は男の足元にできる影のことですか？","a":"いいえ"},{"q":"影は太陽や電気の光でできる影ですか？","a":"いいえ"},{"q":"影というのは男の存在感のことですか？","a":"いいえ"},{"q":"相手は男をからかっていますか？","a":"いいえ"},{"q":"相手は男の友だちですか？","a":"いいえ"},{"q":"相手は男の家族や恋人ですか？","a":"いいえ"},{"q":"男と相手は前にも会ったことがありますか？","a":"はい"},{"q":"男は相手に感謝していますか？","a":"はい"},{"q":"相手は男のために何かをしてくれた人ですか？","a":"はい"},{"q":"相手は医者ですか？","a":"はい"},{"q":"影は写真に写っていますか？","a":"はい"},{"q":"その写真は病院で撮ったものですか？","a":"はい"},{"q":"影は男の体の中にありますか？","a":"はい"},{"q":"影は病気と関係がありますか？","a":"はい"},{"q":"影が濃いほうが良いことですか？","a":"いいえ"},{"q":"男は入院していましたか？","a":"いいえ"},{"q":"男の年齢は重要ですか？","a":"関係ない"},{"q":"病気の名前は重要ですか？","a":"関係ない"},{"q":"男に家族がいるかどうかは重要ですか？","a":"関係ない"},{"q":"影はレントゲン写真に写った病気の跡で、薄くなったのは病気が良くなった証拠だから男は泣いて喜び、治してくれた医者に頭を下げた。","a":"正解"}]',
        '影が薄いと言われて大喜び', '「はい / いいえ / 関係ない」で答えられる質問をコメントしてね。出題者が全部返事します',
        '{"problem":"久しぶりに会った相手から、影がずいぶん薄くなった、と言われて、男は泣いて喜んだ。そう言った相手もにこにこ笑っていて、男は相手に何度も頭を下げた。どういうこと？","rule":"はい、いいえ、関係ない、で答えられる質問をコメントしてね。全部返事するよ。"}',
        '[{"role":"questioner","text":"男は悪口を言われるのが好きな人？"},{"role":"master","text":"いいえ。"},{"role":"questioner","text":"相手は男の友だち？"},{"role":"master","text":"いいえ。"},{"role":"questioner","text":"二人は前にも会った？"},{"role":"master","text":"はい！"}]',
        '{"master":{"intro":"質問してみて！","outro":"何度でも答えるよ。コメントで質問！"},"jr":{"outro":"面白かったら、いいね、フォローよろしくね！"}}',
        'A stylized 1990s Japanese OVA anime background painting (hand-painted cel-era background art, poster-color textures, clean shapes, thick brush-like outlines on key objects). Mid-key lighting: moonlight, lamps or candlelight keep the whole scene clearly visible, NOT dark.

Scene: A middle-aged man in a plain shirt seen from behind, walking alone along a quiet residential street in late afternoon; his long shadow stretches ahead of him on the pavement; low houses, a utility pole and a hedge along the street; soft warm sunlight, no other people.

Vertical 9:16 composition (1024x1536). No text, no letters, no numbers, no logos, no signs. Depict only the scene described in the problem statement; do not depict any clue to the story''s hidden truth. People: only the persons who appear in the problem, plus at most one distant silhouette. Keep the upper 55% of the image calm and simple (sky, wall, ceiling, window) so that text cards can be overlaid there.',
        '【探偵カメロックのウミガメのスープ】

久しぶりに会った相手から「影がずいぶん薄くなった」と言われて、男は泣いて喜んだ。そう言った相手もにこにこ笑っていて、男は相手に何度も頭を下げた。どういうこと？

「はい / いいえ / 関係ない」で答えられる質問をコメントしてね。出題者の探偵カメロックが全部返事します。正解が出るまで何度でもどうぞ。

#ウミガメのスープ #水平思考 #推理クイズ #なぞなぞ #謎解き #クイズ #AIart',
        '完全オリジナル（既存問題の転載・改変ではない）。作問法は note 記事 https://note.com/suekai0217/n/n35128e606a9b の4 ステップ（モチーフ → 連想 → 言い方を変える → 不思議にする）と良い問題の 3 条件（コアが明確・動線がある・現実離れしない）に従う。着想の型は research.md（Codex Web リサーチ台帳）を参照。 型: 意味誤誘導型。モチーフ「影」（作問スキル umigame-problem-writer の抽選 3 語〔影・鉛筆・ゴミ出し〕から選択）→ 連想「影が薄い（慣用句）・レントゲンの影」→ 抽象化（影が薄い = 存在感 / 写真に写る影）→ 常識「影が薄いと言われたら傷つく」の逆。着想元の既存問題なし（台帳 #22「外科医は母親」の役割の思い込みとは構造が異なり、言った相手が医者であることは核ではない。核は「影」の多義）。2026-09-07 のレビューで「分かりやすすぎる」の指摘を受け、対称形（半年前に濃くなった）・丁寧語・「同じ相手」の手がかりを外して難易度を 3 → 4 に上げた。差し替え前の 2 案（貸出カード / カシオペヤ座）の経緯は STATUS.md。', 1);

-- U11 鏡文字で早く着く男たち
INSERT INTO umigame_stock_items (set_id, content_key, title, difficulty, problem_text, truth, fact_sheet,
    expected_questions, hook, rule_text, narration, play_example, character_lines, illustration_prompt,
    caption, source_note, is_active)
VALUES ((SELECT id FROM batch_sets WHERE set_code = 'umigame-soup-1'),
        '002-mirror-letters', '鏡文字で早く着く男たち', 4,
        '働く男たちは自分たちの名前を、わざと鏡文字で大きく書いている。そのままではとても読みにくいのに、このおかげで男たちの仕事がやりやすくなっている。どういうこと？',
        '男たちは救急隊員。救急車の前の面に書いた「救急」の文字を、左右を裏返した鏡文字にしてある。前を走る車の運転手がバックミラーで見ると正しく「救急」と読めるので、後ろから救急車が来たことにすぐ気づいて道を譲ってくれる。だから現場や病院に早く着ける。',
        '["男たちは名前を隠したくて鏡文字にしたのではなく、読んでほしくて書いた","鏡文字は間違えて書いたのではなく、わざとそうした","文字は男たちの持ち物に書いてあり、男たちはそれと一緒に移動する","文字を読むのは男たちではなく、男たちより先を進んでいる他の人である。読む人は振り返らず、鏡に映して正しく読む","文字がどこに書いてあり、誰がどんな鏡で読むかは、この問題の答えの核心である（正解宣言のとき以外は補足で言わない）","男たちの仕事は、急いで行き先へ着かなければならない仕事である","文字は仕事で使う物に書いてあり、仕事中に他の人に見せている","文字を読んだ人が男たちのために何かをしてくれるので、早く着けて仕事がやりやすい","男たちは芸術家・子ども・暗号の専門家・警察官ではない","行き先は毎回違う。鏡文字にすることは法律で禁じられていない","男たちの名前が何か・年齢・人数は問題に関係ない"]',
        '[{"q":"男たちは名前を隠したいのですか？","a":"いいえ"},{"q":"鏡文字は間違えて書いたのですか？","a":"いいえ"},{"q":"男たちは芸術家ですか？","a":"いいえ"},{"q":"鏡文字は暗号ですか？","a":"いいえ"},{"q":"文字を読むのは男たち自身ですか？","a":"いいえ"},{"q":"文字を読む人は鏡を使って読みますか？","a":"はい"},{"q":"文字は建物に書いてありますか？","a":"いいえ"},{"q":"文字は乗り物に書いてありますか？","a":"はい"},{"q":"男たちはその乗り物に乗って移動しますか？","a":"はい"},{"q":"文字を読む人は、男たちより先を進んでいますか？","a":"はい"},{"q":"読む人も乗り物に乗っていますか？","a":"はい"},{"q":"読む人が使う鏡は、車についている鏡ですか？","a":"はい"},{"q":"読んだ人は男たちに道を譲りますか？","a":"はい"},{"q":"男たちの仕事は急ぐ必要がありますか？","a":"はい"},{"q":"文字は仕事で使う物に書いてありますか？","a":"はい"},{"q":"文字を読むのは仕事の相手（客）ですか？","a":"いいえ"},{"q":"男たちは警察官ですか？","a":"いいえ"},{"q":"男たちの名前が何かは重要ですか？","a":"関係ない"},{"q":"行き先がどこかは重要ですか？","a":"関係ない"},{"q":"男たちは救急隊員で、救急車の前に書いた文字を鏡文字にしたのは、前を走る車の運転手がバックミラーで正しく読めるようにするため。気づいた車が道を譲るので早く着けて仕事がやりやすい。","a":"正解"}]',
        '鏡文字で仕事がはかどる', '「はい / いいえ / 関係ない」で答えられる質問をコメントしてね。出題者が全部返事します',
        '{"problem":"働く男たちは自分たちの名前を、わざと鏡文字で大きく書いている。そのままではとても読みにくいのに、このおかげで男たちの仕事がやりやすくなっている。どういうこと？","rule":"はい、いいえ、関係ない、で答えられる質問をコメントしてね。全部返事するよ。"}',
        '[{"role":"questioner","text":"名前を隠したい？"},{"role":"master","text":"いいえ。"},{"role":"questioner","text":"文字は建物にある？"},{"role":"master","text":"いいえ。"},{"role":"questioner","text":"読む人は鏡を使う？"},{"role":"master","text":"はい！"}]',
        '{"master":{"intro":"質問してみて！","outro":"何度でも答えるよ。コメントで質問！"},"jr":{"outro":"面白かったら、いいね、フォローよろしくね！"}}',
        'A stylized 1990s Japanese OVA anime background painting (hand-painted cel-era background art, poster-color textures, clean shapes, thick brush-like outlines on key objects). Mid-key lighting: moonlight, lamps or candlelight keep the whole scene clearly visible, NOT dark.

Scene: Two men in plain work clothes seen from behind, standing in an open yard at dawn and holding a large blank white board between them; a small hand mirror resting on a wooden crate nearby; a low wall and a tree; soft morning light, no vehicles, no other people, no text or letters anywhere.

Vertical 9:16 composition (1024x1536). No text, no letters, no numbers, no logos, no signs. Depict only the scene described in the problem statement; do not depict any clue to the story''s hidden truth. People: only the persons who appear in the problem, plus at most one distant silhouette. Keep the upper 55% of the image calm and simple (sky, wall, ceiling, window) so that text cards can be overlaid there.',
        '【探偵カメロックのウミガメのスープ】

働く男たちは自分たちの名前を、わざと鏡文字で大きく書いている。そのままではとても読みにくいのに、このおかげで男たちの仕事がやりやすくなっている。どういうこと？

「はい / いいえ / 関係ない」で答えられる質問をコメントしてね。出題者の探偵カメロックが全部返事します。正解が出るまで何度でもどうぞ。

#ウミガメのスープ #水平思考 #推理クイズ #なぞなぞ #謎解き #クイズ #AIart',
        '完全オリジナル（既存問題の転載・改変ではない）。作問法は note 記事 https://note.com/suekai0217/n/n35128e606a9b の4 ステップ（モチーフ → 連想 → 言い方を変える → 不思議にする）と良い問題の 3 条件（コアが明確・動線がある・現実離れしない）に従う。着想の型は research.md（Codex Web リサーチ台帳）を参照。 型: 意味誤誘導型。モチーフ「鏡」（作問スキル umigame-problem-writer の抽選 3 語〔時計・毛糸・鏡〕から。初稿「時計台の下で満足する女」はコアが弱く 2026-09-07 のレビューで取り下げ、工程 2 からやり直した）→ 連想「鏡文字・合わせ鏡・鏡開き・バックミラー」→ 具体化（鏡文字 → 鏡で読ませるための文字）→ 常識「鏡文字は読ませたくない・遊び」の逆（読ませたい・そのおかげで早く着く）。着想元の既存問題なし（救急車の前面が鏡文字なのは一般知識だが、台帳・記憶にウミガメとしての出題なし。問題文は 2026-09-07 のレビューでユーザー案（「書いている」の状態形・「読みにくい」・「仕事がやりやすい」で仕事の枠を先に置く。字数下限のため「とても」を補った）に差し替え、難易度 3 → 4。捨てた案: 時計を止める〔新記録と試合終了の 2 通りで核が定まらない〕/ 編んだ網を海に投げる〔U06 と同じ作業動詞の多義〕/ 鏡開き〔なぞなぞとして有名〕/ 針が逆回りの時計〔理髪店の逆回り時計として既知〕）。', 1);

-- U12 階段に並ぶ、音を出さない男たち
INSERT INTO umigame_stock_items (set_id, content_key, title, difficulty, problem_text, truth, fact_sheet,
    expected_questions, hook, rule_text, narration, play_example, character_lines, illustration_prompt,
    caption, source_note, is_active)
VALUES ((SELECT id FROM batch_sets WHERE set_code = 'umigame-soup-1'),
        '003-silent-musicians', '階段に並ぶ、音を出さない男たち', 2,
        '男たちは階段に横一列に並び、楽器を構えている。しかし、男たちは今まで一度も音を出したことがない。それでも見ている人たちは、うれしそうに毎日眺めている。どういうこと？',
        '男たちはひな人形の五人囃子。階段に見えるのは、ひな祭りの段飾りの段である。人形なので、太鼓や笛を構えたまま一度も音を出したことがない。家族は毎年ひな祭りの時期に飾り、飾っている間は毎日うれしそうに眺めている。',
        '["男たちは生きている人間ではない。男たちの正体はこの問題の答えの核心である（正解宣言のとき以外は補足で言わない）","男たちは自分の意思で動いたり話したりしない。演奏の練習をしているのでも、音を出すのを止められているのでもない","楽器は壊れていない。楽器の種類は問題に関係ない","男たちは家の中にいる。階段は建物の階段ではなく、そのために組み立てた段である","男たちの上の段にも並んでいる者がいる（男たちは一番上ではない）","男たちが並ぶのは一年のうち決まった時期だけで、その時期が終わると片づけられ、次の年にまた並ぶ","見ている人たちは、男たちを家に置いている家族である。男たちが音を出さないことを、家族は初めから知っている","家族がうれしそうなのは、その時期のお祝いを楽しんでいるから。女の子のためのお祝いである","男たちのうち 1 人は楽器を持たず、別の物を持っている（全員が楽器を持つのではない）","男たちは楽団・音楽家・パントマイム・銅像・おもちゃではない","男たちの年齢・人数・家の場所は問題に関係ない"]',
        '[{"q":"楽器は壊れていますか？","a":"いいえ"},{"q":"男たちは演奏の練習中ですか？","a":"いいえ"},{"q":"男たちは誰かに音を出すのを止められていますか？","a":"いいえ"},{"q":"男たちは生きている人間ですか？","a":"いいえ"},{"q":"男たちは楽団ですか？","a":"いいえ"},{"q":"男たちは人形ですか？","a":"はい"},{"q":"男たちはおもちゃですか？","a":"いいえ"},{"q":"男たちは家の中にいますか？","a":"はい"},{"q":"階段は建物の階段ですか？","a":"いいえ"},{"q":"男たちは一年中そこにいますか？","a":"いいえ"},{"q":"決まった季節にだけ並びますか？","a":"はい"},{"q":"男たちの上の段にも誰かいますか？","a":"はい"},{"q":"見ている人たちは、男たちを家に置いている人ですか？","a":"はい"},{"q":"見ている人たちは何かをお祝いしていますか？","a":"はい"},{"q":"女の子のためのお祝いですか？","a":"はい"},{"q":"男たちが音を出せないことを、見ている人は知っていますか？","a":"はい"},{"q":"男たちは全員楽器を持っていますか？","a":"いいえ"},{"q":"楽器の種類は重要ですか？","a":"関係ない"},{"q":"男たちの年齢は関係ありますか？","a":"関係ない"},{"q":"男たちはひな人形の五人囃子で、階段はひな祭りの段飾り。人形だから楽器を構えたまま音を出さない。家族はひな祭りの飾りとして毎日眺めて楽しんでいる。","a":"正解"}]',
        '音を出さない男たち', '「はい / いいえ / 関係ない」で答えられる質問をコメントしてね。出題者が全部返事します',
        '{"problem":"男たちは階段に横一列に並び、楽器を構えている。しかし、男たちは今まで一度も音を出したことがない。それでも見ている人たちは、うれしそうに毎日眺めている。どういうこと？","rule":"はい、いいえ、関係ない、で答えられる質問をコメントしてね。全部返事するよ。"}',
        '[{"role":"questioner","text":"楽器は壊れている？"},{"role":"master","text":"いいえ。"},{"role":"questioner","text":"男たちは人間？"},{"role":"master","text":"いいえ。"},{"role":"questioner","text":"家の中にいる？"},{"role":"master","text":"はい！"}]',
        '{"master":{"intro":"質問してみて！","outro":"何度でも答えるよ。コメントで質問！"},"jr":{"outro":"面白かったら、いいね、フォローよろしくね！"}}',
        'A stylized 1990s Japanese OVA anime background painting (hand-painted cel-era background art, poster-color textures, clean shapes, thick brush-like outlines on key objects). Mid-key lighting: moonlight, lamps or candlelight keep the whole scene clearly visible, NOT dark.

Scene: Five young men in plain clothes standing in a row on a short flight of wide steps, holding small drums and a flute but not playing, perfectly still; two or three people watching from below with delighted faces; warm soft light, simple background, no text or letters anywhere.

Vertical 9:16 composition (1024x1536). No text, no letters, no numbers, no logos, no signs. Depict only the scene described in the problem statement; do not depict any clue to the story''s hidden truth. People: only the persons who appear in the problem, plus at most one distant silhouette. Keep the upper 55% of the image calm and simple (sky, wall, ceiling, window) so that text cards can be overlaid there.',
        '【探偵カメロックのウミガメのスープ】

男たちは階段に横一列に並び、楽器を構えている。しかし、男たちは今まで一度も音を出したことがない。それでも見ている人たちは、うれしそうに毎日眺めている。どういうこと？

「はい / いいえ / 関係ない」で答えられる質問をコメントしてね。出題者の探偵カメロックが全部返事します。正解が出るまで何度でもどうぞ。

#ウミガメのスープ #水平思考 #推理クイズ #なぞなぞ #謎解き #クイズ #AIart',
        '完全オリジナル（既存問題の転載・改変ではない）。作問法は note 記事 https://note.com/suekai0217/n/n35128e606a9b の4 ステップ（モチーフ → 連想 → 言い方を変える → 不思議にする）と良い問題の 3 条件（コアが明確・動線がある・現実離れしない）に従う。着想の型は research.md（Codex Web リサーチ台帳）を参照。 型: 意味誤誘導型。モチーフ「階段」（作問スキル umigame-problem-writer の抽選 3 語〔テント・のど飴・階段〕から）→ 連想「ひな壇・段・踊り場・はしご・上っても着かない」→ 具体化（階段に並ぶ男たち → 段飾りに並ぶ五人囃子）→ 常識「楽器を構える人は音を出す」の逆（一度も音を出したことがない）。着想元の既存問題なし（人を人形に反転する構造は台帳 #07〔玩具〕の型のみ借用。モチーフ・真相・問題文は新規）。捨てた案: 上っても 2 階に着かない階段〔ランニングマシン型として既知・落差なし〕/ 違う足音で泣く女〔語の強制なし・U01 と結末が重なる〕/ 踊り場〔誤読が起きない〕/ 棚田〔階段と呼ばない〕/ 引っ越し屋の階段料金・段位〔知識クイズ〕。', 1);

-- U13 会ったことのない男の子からの手紙
INSERT INTO umigame_stock_items (set_id, content_key, title, difficulty, problem_text, truth, fact_sheet,
    expected_questions, hook, rule_text, narration, play_example, character_lines, illustration_prompt,
    caption, source_note, is_active)
VALUES ((SELECT id FROM batch_sets WHERE set_code = 'umigame-soup-1'),
        '004-fifty-year-letter', '会ったことのない男の子からの手紙', 4,
        'ある日、一人の男のもとに、男の子が書いた手紙が届いた。男はその子に、これまで一度も会ったことがない。それなのに、その子がどんな子なのか、誰よりもよく知っていた。なぜ？',
        '手紙は、男が 50 年前の小学生のころ、学校の記念行事で「未来の自分」に宛てて書き、タイムカプセルに入れて校庭に埋めたもの。50 年後の同窓会で掘り出され、男の手に渡った。手紙を書いた男の子は50 年前の男自身。自分のことだから、その子がどんな子で、どんな大人になったのかも誰よりもよく知っている。人は自分自身と「会う」ことはできないので、男がその子に一度も会ったことがないのも本当である。',
        '["手紙を書いた男の子が誰なのかは、この問題の答えの核心である（正解宣言のとき以外は補足で言わない）","手紙は書かれてから届くまでに何十年もたっている。郵便局が配達に何十年もかけたのではなく、配達が遅れたのでも、途中で失くされていたのでもない","手紙はあとで読まれるように、わざと保管されていたものである","手紙は男の子が小学生のとき、学校の行事で書いたものである","手紙には宛先があり、男はその宛先のとおりの正しい受け取り手である（誤配ではない）","手紙は男の家のポストに届いたのではなく、集まりの場で男に手渡された","男の子は今も生きていて、今はもう大人になっている。男の子は男の息子・孫・親戚・友だち・教え子ではない","男の子は有名人ではない。男はテレビや本で男の子のことを知ったのでもない","男が男の子のことをよく知っているのは、誰かから聞いたからでも、調べたからでもない","手紙には男の子の将来の夢が書いてあった（夢の中身は問題に関係ない）","男は手紙を受け取っても驚かず、読んで懐かしそうに笑った","男の名前・住んでいる場所は問題に関係ない"]',
        '[{"q":"手紙は最近書かれたものですか？","a":"いいえ"},{"q":"手紙は何十年も前に書かれたものですか？","a":"はい"},{"q":"手紙はどこかで失くされていたのですか？","a":"いいえ"},{"q":"手紙は郵便局のミスで届くのが遅れたのですか？","a":"いいえ"},{"q":"手紙はあとで読まれるように、わざと取っておかれたのですか？","a":"はい"},{"q":"手紙は学校の行事と関係がありますか？","a":"はい"},{"q":"手紙はタイムカプセルに入っていましたか？","a":"はい"},{"q":"男の子は手紙を書いたとき、小学生でしたか？","a":"はい"},{"q":"男の子は今も子どもですか？","a":"いいえ"},{"q":"男の子は今も生きていますか？","a":"はい"},{"q":"男の子は男の息子や孫ですか？","a":"いいえ"},{"q":"男は男の子の先生でしたか？","a":"いいえ"},{"q":"男の子は有名人ですか？","a":"いいえ"},{"q":"手紙はもともと男に宛てて書かれたものですか？","a":"はい"},{"q":"男は誰かから男の子のことを聞いたのですか？","a":"いいえ"},{"q":"男は男の子と同じ小学校に通っていましたか？","a":"はい"},{"q":"手紙には将来の夢が書いてありましたか？","a":"はい"},{"q":"夢の中身は答えに関係ありますか？","a":"関係ない"},{"q":"男の住んでいる場所は関係ありますか？","a":"関係ない"},{"q":"手紙は男が小学生のとき、学校の行事でタイムカプセルに入れた未来の自分宛てのもの。書いた男の子は昔の男自身だから、どんな子なのかを誰よりもよく知っていた。","a":"正解"}]',
        '会ったことのない子の手紙', '「はい / いいえ / 関係ない」で答えられる質問をコメントしてね。出題者が全部返事します',
        '{"problem":"ある日、一人の男のもとに、男の子が書いた手紙が届いた。男はその子に、これまで一度も会ったことがない。それなのに、その子がどんな子なのか、誰よりもよく知っていた。なぜ？","rule":"はい、いいえ、関係ない、で答えられる質問をコメントしてね。全部返事するよ。"}',
        '[{"role":"questioner","text":"その子は男の息子？"},{"role":"master","text":"いいえ。"},{"role":"questioner","text":"最近書かれた手紙？"},{"role":"master","text":"いいえ。"},{"role":"questioner","text":"昔書かれた手紙？"},{"role":"master","text":"はい！"}]',
        '{"master":{"intro":"質問してみて！","outro":"何度でも答えるよ。コメントで質問！"},"jr":{"outro":"面白かったら、いいね、フォローよろしくね！"}}',
        'A stylized 1990s Japanese OVA anime background painting (hand-painted cel-era background art, poster-color textures, clean shapes, thick brush-like outlines on key objects). Mid-key lighting: moonlight, lamps or candlelight keep the whole scene clearly visible, NOT dark.

Scene: An elderly man with gentle eyes sitting by a window in warm evening light, holding an old worn envelope with both hands and smiling nostalgically; behind him a faint dream-like image of a small schoolboy writing at a desk; simple background, no text or letters anywhere.

Vertical 9:16 composition (1024x1536). No text, no letters, no numbers, no logos, no signs. Depict only the scene described in the problem statement; do not depict any clue to the story''s hidden truth. People: only the persons who appear in the problem, plus at most one distant silhouette. Keep the upper 55% of the image calm and simple (sky, wall, ceiling, window) so that text cards can be overlaid there.',
        '【探偵カメロックのウミガメのスープ】

ある日、一人の男のもとに、男の子が書いた手紙が届いた。男はその子に、これまで一度も会ったことがない。それなのに、その子がどんな子なのか、誰よりもよく知っていた。なぜ？

「はい / いいえ / 関係ない」で答えられる質問をコメントしてね。出題者の探偵カメロックが全部返事します。正解が出るまで何度でもどうぞ。

#ウミガメのスープ #水平思考 #推理クイズ #なぞなぞ #謎解き #クイズ #AIart',
        '完全オリジナル（既存問題の転載・改変ではない）。作問法は note 記事 https://note.com/suekai0217/n/n35128e606a9b の4 ステップ（モチーフ → 連想 → 言い方を変える → 不思議にする）と良い問題の 3 条件（コアが明確・動線がある・現実離れしない）に従う。着想の型は research.md（Codex Web リサーチ台帳）を参照。 型: 意味誤誘導型。モチーフ「郵便」（作問スキル umigame-problem-writer の抽選 3 語〔片づけ・郵便・たまご〕から）→ 連想「タイムカプセル・卒業式に書く未来の自分への手紙」→ 具体化（昔の男の子が書いた手紙を受け取る男）→ 常識「手紙は書いた人と受け取る人が別人」の逆（差出人 = 受取人）。着想元の既存問題なし（別々に見せた人物を同一人物と明かす構造は台帳 #21〔人数の省略の補完〕の型のみ借用。モチーフ・真相・問題文は新規）。捨てた案: 他人の手紙を毎日読んで怒られない男〔代読。語の強制がない状況型〕/ サンタ宛ての手紙に毎年返事を書く係〔誤認がなく知識・雑学寄り〕。', 1);

-- U14 焼かない卵を自慢するパン屋
INSERT INTO umigame_stock_items (set_id, content_key, title, difficulty, problem_text, truth, fact_sheet,
    expected_questions, hook, rule_text, narration, play_example, character_lines, illustration_prompt,
    caption, source_note, is_active)
VALUES ((SELECT id FROM batch_sets WHERE set_code = 'umigame-soup-1'),
        '005-bakers-egg', '焼かない卵を自慢するパン屋', 4,
        'パン屋の主人は、店の卵をとても大切にしている。焼くことも、割ることもしない。それなのに主人は、うちのパンがおいしいのはこの卵のおかげだ、といつも自慢している。なぜ？',
        '「卵」とは、パン職人の卵、つまり見習いの若者のこと。主人は十年前に店へ来た見習いを、自分の店の「卵」と呼んでかわいがり、パン作りを教えて一人前に育て上げた。いまでは店でいちばんおいしいパンをその卵が焼いているので、「パンがおいしいのはこの卵のおかげ」という自慢は本当のこと。食べ物の卵ではないので、焼くことも割ることもしない。',
        '["「卵」が何（誰）なのかは、この問題の答えの核心である（正解宣言のとき以外は補足で言わない）","卵はひよこや鶏になったのではない。温めてかえしたのでもない","魔法・おとぎ話・作り話ではない。現実にどこの町でも起こることである","卵はお守り・縁起物・飾り・置き物ではない","主人は卵をいつか食べたり売ったりするつもりはない","卵は冷蔵庫にも巣にも入っていない","卵はパンの材料として使われていない。それでも卵はパン作りに深く関係している","「大切にしている」は、えさや水をやるという意味ではない。教えて育てているという意味である","卵は毎日、主人といっしょに店で働いている","主人の自慢は嘘や冗談ではなく、本当のことである","店の場所・パンの種類は問題に関係ない"]',
        '[{"q":"卵はお守りや縁起物として大切にされているのですか？","a":"いいえ"},{"q":"卵はひよこにかえったのですか？","a":"いいえ"},{"q":"卵は鶏になったのですか？","a":"いいえ"},{"q":"これは魔法やおとぎ話の出来事ですか？","a":"いいえ"},{"q":"主人は卵をいつか食べるつもりですか？","a":"いいえ"},{"q":"卵は冷蔵庫に入っていますか？","a":"いいえ"},{"q":"主人の自慢は嘘や冗談ですか？","a":"いいえ"},{"q":"卵はパンの材料として使われていますか？","a":"いいえ"},{"q":"「卵」は食べ物の卵ですか？","a":"いいえ"},{"q":"卵はパン作りに関係がありますか？","a":"はい"},{"q":"卵は生き物ですか？","a":"はい"},{"q":"卵は人ですか？","a":"はい"},{"q":"卵は店でパンを焼いていますか？","a":"はい"},{"q":"主人は卵にパンの作り方を教えましたか？","a":"はい"},{"q":"卵は主人の家族ですか？","a":"いいえ"},{"q":"パンの種類は答えに関係ありますか？","a":"関係ない"},{"q":"店の場所は答えに関係ありますか？","a":"関係ない"},{"q":"「卵」とはパン職人の卵、つまり見習いの人のこと。主人が育てた見習いがいまは店でいちばんおいしいパンを焼いているので、パンがおいしいのはこの卵のおかげ。","a":"正解"}]',
        '焼かない卵を自慢するパン屋', '「はい / いいえ / 関係ない」で答えられる質問をコメントしてね。出題者が全部返事します',
        '{"problem":"パン屋の主人は、店の卵をとても大切にしている。焼くことも、割ることもしない。それなのに主人は、うちのパンがおいしいのはこの卵のおかげだ、といつも自慢している。なぜ？","rule":"はい、いいえ、関係ない、で答えられる質問をコメントしてね。全部返事するよ。"}',
        '[{"role":"questioner","text":"卵はお守りみたいなもの？"},{"role":"master","text":"いいえ。"},{"role":"questioner","text":"卵は材料として使う？"},{"role":"master","text":"いいえ。"},{"role":"questioner","text":"卵は生き物？"},{"role":"master","text":"はい！"}]',
        '{"master":{"intro":"質問してみて！","outro":"何度でも答えるよ。コメントで質問！"},"jr":{"outro":"面白かったら、いいね、フォローよろしくね！"}}',
        'A stylized 1990s Japanese OVA anime background painting (hand-painted cel-era background art, poster-color textures, clean shapes, thick brush-like outlines on key objects). Mid-key lighting: moonlight, lamps or candlelight keep the whole scene clearly visible, NOT dark.

Scene: A kind old baker in a warm bakery at dawn, gently cradling a large white egg in both hands like a treasure, shelves of freshly baked bread glowing behind him; soft morning light, simple background, no text anywhere.

Vertical 9:16 composition (1024x1536). No text, no letters, no numbers, no logos, no signs. Depict only the scene described in the problem statement; do not depict any clue to the story''s hidden truth. People: only the persons who appear in the problem, plus at most one distant silhouette. Keep the upper 55% of the image calm and simple (sky, wall, ceiling, window) so that text cards can be overlaid there.',
        '【探偵カメロックのウミガメのスープ】

パン屋の主人は、店の卵をとても大切にしている。焼くことも、割ることもしない。それなのに主人は、うちのパンがおいしいのはこの卵のおかげだ、といつも自慢している。なぜ？

「はい / いいえ / 関係ない」で答えられる質問をコメントしてね。出題者の探偵カメロックが全部返事します。正解が出るまで何度でもどうぞ。

#ウミガメのスープ #水平思考 #推理クイズ #なぞなぞ #謎解き #クイズ #AIart',
        '完全オリジナル（既存問題の転載・改変ではない）。作問法は note 記事 https://note.com/suekai0217/n/n35128e606a9b の4 ステップ（モチーフ → 連想 → 言い方を変える → 不思議にする）と良い問題の 3 条件（コアが明確・動線がある・現実離れしない）に従う。着想の型は research.md（Codex Web リサーチ台帳）を参照。 型: 意味誤誘導型。モチーフ「たまご」（作問スキル umigame-problem-writer の抽選 3 語〔ベンチ・たまご・階段〕から。前 3 回の抽選〔自転車・すいか・花火 → 初案取り下げ / 帽子・体重計・お守り → 猫をかぶる案が差し戻し / のど飴・鍵・迷子 → 全滅で引き直し〕も記録）→ 連想「医者の卵・役者の卵 = 見習い」→ 抽象化（店の卵を大切にする → 職人の卵を育てる）→ 常識「卵は焼いて割って使う材料」の逆（焼くことも割ることもしないのに、パンがおいしいのはこの卵のおかげだと自慢する）。初稿の逆「その卵が焼いている」「十年間育てた」は誤認の読みで不可能文となり誤読が自壊するためレビューで言い換え（情報は真相・シートへ）。着想元の既存問題なし（語の多義で場面を反転する構造は台帳 #16〔ホーム = 本塁〕・#23〔撃つ = 撮影〕の型のみ借用。モチーフ・真相・問題文は新規）。捨てた案: タネはありません = 種なしスイカの売り文句〔人間ゲートで「コアが弱い」と取り下げ〕/ 猫をかぶる = かぶりもの〔コア宣言で差し戻し〕/ 白い鍵と黒い鍵 = ピアノ〔英語圏の有名なぞなぞと同構造〕/ 迷子は大人〔決めつけ反転の classic 構造〕/ ベンチを温める〔落差なし・競技用語反転は台帳明示例と同構造〕/ コロンブスの卵・金の卵〔知識クイズ〕。', 1);

-- U16 助けに来た女も凍りついた
INSERT INTO umigame_stock_items (set_id, content_key, title, difficulty, problem_text, truth, fact_sheet,
    expected_questions, hook, rule_text, narration, play_example, character_lines, illustration_prompt,
    caption, source_note, is_active)
VALUES ((SELECT id FROM batch_sets WHERE set_code = 'umigame-soup-1'),
        '006-frozen-tag', '助けに来た女も凍りついた', 4,
        '男は凍りついたまま、誰かが助けに来るのをじっと待っていた。ようやく助けに来た女は、男のそばまで来たところで、同じようにその場で凍りついてしまった。どういうこと？',
        '男と女は夫婦で、休みの日に公園で自分の子どもたちと鬼ごっこの一種「氷鬼」で遊んでいた。鬼は子ども。氷鬼では、鬼にタッチされた人は「凍った」ことになってその場から動けなくなり、仲間にタッチしてもらうと「溶けて」また動けるようになる。男は鬼の子どもにタッチされて凍り、仲間が助けに来てくれるのをじっと待っていた。女が助けに走ってきたが、鬼は凍った男のそばで見張っていて、女が男に触れる直前にタッチした。だから女も男のそばで凍ってしまった。凍りついたといっても本当に凍ったわけではなく、二人はこのあと別の子どもに助けてもらって、また走り回った。',
        '["男も女も本当に凍ってはいないし、寒い場所にいるのでもない","男も女も怖がってはいないし、けがや病気でもない","二人がいる場所に危険なものや恐ろしいものはない","男と女は大人で、夫婦である。二人の子どもたちも同じ場所にいて、ほかに大人はいない","男が動けないのは、体のせいでも、誰かに縛られているせいでもなく、守らなければならない決まりのせいである","男と女が何をしていて、なぜ動けないのかは、この問題の答えの核心である（正解宣言のとき以外は補足で言わない）","男が凍りついたのは、ある一人の相手に体をさわられたからで、その相手はまだ男の近くにいる。その相手は大人ではない","女が凍りついたのも、同じ相手に体をさわられたからである","女が来てくれたことは、男にとってうれしいことだった","子どもたちのうち鬼ではない子が二人の体にさわれば、二人はまた動けるようになる","このあと二人は元気に走り回っていて、悲しい出来事は何も起きていない","季節・時刻・二人の名前や職業は問題に関係ない"]',
        '[{"q":"男は本当に凍っていますか？","a":"いいえ"},{"q":"寒い場所での出来事ですか？","a":"いいえ"},{"q":"男は怖くて動けないのですか？","a":"いいえ"},{"q":"男はけがや病気で動けないのですか？","a":"いいえ"},{"q":"男は誰かに縛られていますか？","a":"いいえ"},{"q":"男のそばに危ないものがありますか？","a":"いいえ"},{"q":"男が動けないのは、決まりを守っているからですか？","a":"はい"},{"q":"男と女は遊んでいますか？","a":"はい"},{"q":"鬼ごっこの仲間ですか？","a":"はい"},{"q":"男は誰かに体をさわられて凍りついたのですか？","a":"はい"},{"q":"女も同じ人にさわられたのですか？","a":"はい"},{"q":"女は男を助けられませんでしたか？","a":"はい"},{"q":"別の仲間がさわれば、二人はまた動けるようになりますか？","a":"はい"},{"q":"男と女は知り合いですか？","a":"はい"},{"q":"男と女は子どもですか？","a":"いいえ"},{"q":"季節は重要ですか？","a":"関係ない"},{"q":"二人にさわった相手は大人ですか？","a":"いいえ"},{"q":"二人は子どもたちと氷鬼をしていて、男は鬼にタッチされて動けなくなり、仲間の助けを待っていた。助けに来た女も鬼にタッチされて、男のそばで動けなくなった。","a":"正解"}]',
        '助けに来た女も凍りついた', '「はい / いいえ / 関係ない」で答えられる質問をコメントしてね。出題者が全部返事します',
        '{"problem":"男は凍りついたまま、誰かが助けに来るのをじっと待っていた。ようやく助けに来た女は、男のそばまで来たところで、同じようにその場で凍りついてしまった。どういうこと？","rule":"はい、いいえ、関係ない、で答えられる質問をコメントしてね。全部返事するよ。"}',
        '[{"role":"questioner","text":"男は本当に凍ってる？"},{"role":"master","text":"いいえ。"},{"role":"questioner","text":"怖くて動けないの？"},{"role":"master","text":"いいえ。"},{"role":"questioner","text":"動けないのは決まりのせい？"},{"role":"master","text":"はい！"}]',
        '{"master":{"intro":"質問してみて！","outro":"何度でも答えるよ。コメントで質問！"},"jr":{"outro":"面白かったら、いいね、フォローよろしくね！"}}',
        'A stylized 1990s Japanese OVA anime background painting (hand-painted cel-era background art, poster-color textures, clean shapes, thick brush-like outlines on key objects). Mid-key lighting: moonlight, lamps or candlelight keep the whole scene clearly visible, NOT dark.

Scene: A man standing perfectly still on an open grassy field, arms held slightly out from his sides as if he cannot move, looking hopefully into the distance; a woman running toward him from far away; a few trees and a low fence in the background, bright daytime, no other people.

Vertical 9:16 composition (1024x1536). No text, no letters, no numbers, no logos, no signs. Depict only the scene described in the problem statement; do not depict any clue to the story''s hidden truth. People: only the persons who appear in the problem, plus at most one distant silhouette. Keep the upper 55% of the image calm and simple (sky, wall, ceiling, window) so that text cards can be overlaid there.',
        '【探偵カメロックのウミガメのスープ】

男は凍りついたまま、誰かが助けに来るのをじっと待っていた。ようやく助けに来た女は、男のそばまで来たところで、同じようにその場で凍りついてしまった。どういうこと？

「はい / いいえ / 関係ない」で答えられる質問をコメントしてね。出題者の探偵カメロックが全部返事します。正解が出るまで何度でもどうぞ。

#ウミガメのスープ #水平思考 #推理クイズ #なぞなぞ #謎解き #クイズ #AIart',
        '完全オリジナル（既存問題の転載・改変ではない）。作問法は note 記事 https://note.com/suekai0217/n/n35128e606a9b の4 ステップ（モチーフ → 連想 → 言い方を変える → 不思議にする）と良い問題の 3 条件（コアが明確・動線がある・現実離れしない）に従う。着想の型は research.md（Codex Web リサーチ台帳）を参照。 型: 意味誤誘導型。モチーフ「氷」（作問スキル umigame-problem-writer の抽選 3 語〔氷・花火・くしゃみ〕から選択。花火は「音が光より遅れる」が U15 と同じ遅延構造・「朝の号砲」は地域慣習・煙や型物花火は語の仕掛けなし、くしゃみは語の仕掛けが同音〔こしょう・ほこり〕か大人の迷信で不成立）→ 連想「凍りつく（慣用句）・氷鬼」→ 具体化（凍りついたまま助けを待つ = 氷鬼で鬼にタッチされて仲間を待つ）→ 常識「助けに来た者は凍りつかない」の逆（助けに来た女も凍りつく）。着想元の既存問題なし（台帳に遊びのルールをコアにした行はない。U12〔人形を人と読ませる〕とは慣用句の誤読という点で構造が異なる）。捨てた案: 滑る〔試験に滑る → 氷で滑る。第一義が氷で誤読が強制されない〕/ 真夏に毛布をかけて氷を運ぶ〔常識の逆だけで語の仕掛けなし〕/ 氷を入れても薄くならないジュース〔氷 = 凍らせたジュース。落差が小さい〕/ だるまさんがころんだ〔言葉で全員が凍りつく案は「はいチーズ」でも成立し正解が一つに定まらない〕。2026-09-20 の人間ゲート 1 巡目で「少年・少女は氷鬼を連想させる」の指摘を受け、登場人物を大人の夫婦（鬼は子ども）に差し替えた（登場人物の属性は正体のカテゴリを指す A 型手がかり。スキル 4.5 に反映）。', 1);

-- U18 白紙に戻った約束
INSERT INTO umigame_stock_items (set_id, content_key, title, difficulty, problem_text, truth, fact_sheet,
    expected_questions, hook, rule_text, narration, play_example, character_lines, illustration_prompt,
    caption, source_note, is_active)
VALUES ((SELECT id FROM batch_sets WHERE set_code = 'umigame-soup-1'),
        '007-blank-letter', '白紙に戻った約束', 4,
        '男と女は大切な約束をした。夏のある日、その約束は白紙に戻ってしまった。それなのに、二人は少しも悲しまなかった。そして約束は、後日きちんと果たされた。どういうこと？',
        '二人の約束は、男が女に渡した手紙に、消せるボールペンで書かれていた。夏の夕立で手紙がびしょ濡れになり、女があわててドライヤーで乾かしたところ、消せるボールペンのインクは熱で透明になる性質があるため、文字がすべて消えて、手紙は本当にまっさらな白紙に戻ってしまった。けれど約束の中身は二人とも覚えていたし、気持ちも変わっていなかった。二人は笑って書き直し、約束は後日きちんと果たされた。白紙に戻ったのは約束ではなく、手紙のほうだった。',
        '["約束は取り消されていない。二人の気持ちも変わっていない","二人はけんかをしておらず、仲は良いまま","白紙に戻ったのは、目に見える形のあるもの","約束は口約束ではなく、書かれたものだった","書かれたものは破れても燃えてもおらず、今も手元にある","起きたことは事故のようなもので、誰のいたずらでもない","夏の天気（夕立）が関係している","濡れたものを乾かしたことが関係している","文字を書いた道具に特徴がある（種類は答えの核心。正解宣言のとき以外は補足で言わない）","約束の中身は二人とも覚えていた","二人の職業・年齢・約束の中身は問題に関係ない"]',
        '[{"q":"二人はけんかをしましたか？","a":"いいえ"},{"q":"どちらかの気持ちが変わったのですか？","a":"いいえ"},{"q":"約束は取り消されたのですか？","a":"いいえ"},{"q":"白紙に戻ったのは、形のあるものですか？","a":"はい"},{"q":"約束は紙に書かれていましたか？","a":"はい"},{"q":"その紙は破れたり燃えたりしましたか？","a":"いいえ"},{"q":"紙そのものは今もありますか？","a":"はい"},{"q":"書いてあった文字が消えたのですか？","a":"はい"},{"q":"誰かがわざと消したのですか？","a":"いいえ"},{"q":"消しゴムでこすって消したのですか？","a":"いいえ"},{"q":"夏の天気は関係ありますか？","a":"はい"},{"q":"紙は濡れましたか？","a":"はい"},{"q":"濡れたせいで文字が消えたのですか？","a":"いいえ"},{"q":"乾かしたことが関係ありますか？","a":"はい"},{"q":"特別なペンで書かれていましたか？","a":"はい"},{"q":"二人の職業は関係ありますか？","a":"関係ない"},{"q":"約束は消せるボールペンで手紙に書かれていて、夕立で濡れた手紙をドライヤーで乾かしたら、熱でインクが消えて紙が本当に白紙に戻った。","a":"正解"}]',
        '白紙に戻った約束', '「はい / いいえ / 関係ない」で答えられる質問をコメントしてね。出題者が全部返事します',
        '{"problem":"男と女は大切な約束をした。夏のある日、その約束は白紙に戻ってしまった。それなのに、二人は少しも悲しまなかった。そして約束は、後日きちんと果たされた。どういうこと？","rule":"はい、いいえ、関係ない、で答えられる質問をコメントしてね。全部返事するよ。"}',
        '[{"role":"questioner","text":"二人はけんかした？"},{"role":"master","text":"いいえ。"},{"role":"questioner","text":"白紙に戻ったのは形のあるもの？"},{"role":"master","text":"はい！"},{"role":"questioner","text":"その紙は破れた？"},{"role":"master","text":"いいえ。"}]',
        '{"master":{"intro":"質問してみて！","outro":"何度でも答えるよ。コメントで質問！"},"jr":{"outro":"面白かったら、いいね、フォローよろしくね！"}}',
        'A stylized 1990s Japanese OVA anime background painting (hand-painted cel-era background art, poster-color textures, clean shapes, thick brush-like outlines on key objects). Mid-key lighting: moonlight, lamps or candlelight keep the whole scene clearly visible, NOT dark.

Scene: A man and a woman in summer clothes sitting at a table in a bright Japanese room, both smiling gently while looking together at a single completely blank sheet of paper held between them, warm evening light after summer rain outside the window; no pen, no hair dryer, no text on the paper, nobody sad.

Vertical 9:16 composition (1024x1536). No text, no letters, no numbers, no logos, no signs. Depict only the scene described in the problem statement; do not depict any clue to the story''s hidden truth. People: only the persons who appear in the problem, plus at most one distant silhouette. Keep the upper 55% of the image calm and simple (sky, wall, ceiling, window) so that text cards can be overlaid there.',
        '【探偵カメロックのウミガメのスープ】

男と女は大切な約束をした。夏のある日、その約束は白紙に戻ってしまった。それなのに、二人は少しも悲しまなかった。そして約束は、後日きちんと果たされた。どういうこと？

「はい / いいえ / 関係ない」で答えられる質問をコメントしてね。出題者の探偵カメロックが全部返事します。正解が出るまで何度でもどうぞ。

#ウミガメのスープ #水平思考 #推理クイズ #なぞなぞ #謎解き #クイズ #AIart',
        '完全オリジナル（既存問題の転載・改変ではない）。作問法は note 記事 https://note.com/suekai0217/n/n35128e606a9b の4 ステップ（モチーフ → 連想 → 言い方を変える → 不思議にする）と良い問題の 3 条件（コアが明確・動線がある・現実離れしない）に従う。着想の型は research.md（Codex Web リサーチ台帳）を参照。 型: 意味誤誘導型。21-4a-3 ④ の型別分離（2026-09-22・ユーザー決定）で、人間ゲート通過済みの story 版 U18「濡れた手紙を乾かしたら白紙になった」を、仕組み（消せるボールペンのインクが熱で消える）の面白さを買われて意味誤誘導型に書き換えたもの（U15 と差し替えて存続）。語の仕掛けは定型表現「（約束が）白紙に戻る」の文字どおりへの反転。誤認先の常識「取り消されたら悲しむ・守られない」の逆（悲しまない・果たされた）を 1 つ足した。着想元の既存問題なし（台帳に該当なし。story 版の Web 照合で同じ仕組みの投稿問題なし）。書き換え時の Web 照合をコアゲート前に先行し、「約束が白紙 × 消えるインク」のコアは日英とも該当なし。「白紙に戻る」の文字どおり化という語仕掛けが重なる投稿問題 1 件（反転後は折り紙で別）を提示の上、人間ゲートで採用。詳細は開発記録 21-4a-3 ④。', 1);

-- U20 間違えたのは誰か
INSERT INTO umigame_stock_items (set_id, content_key, title, difficulty, problem_text, truth, fact_sheet,
    expected_questions, hook, rule_text, narration, play_example, character_lines, illustration_prompt,
    caption, source_note, is_active)
VALUES ((SELECT id FROM batch_sets WHERE set_code = 'umigame-soup-1'),
        '008-who-made-the-mistake', '間違えたのは誰か', 4,
        'ピアノの演奏会で、男は途中で「あ、間違えた」と小声で言った。ピアニストの演奏は一音も外さない完璧なものだった。隣で聞いた女は、こらえきれずに吹き出した。どういうこと？',
        '男は音楽に詳しくなく、ピアノも弾けない。男の娘は半年前からピアノを習い始め、毎晩リビングで同じ有名な曲を練習していた。娘は曲の同じ場所で決まってつっかえ、少し違う音で弾いてから先へ進む。男は皿を洗いながら毎晩それを聞くうちに、娘のつっかえ方ごと曲を覚え、鼻歌で歌えるようになっていた。演奏会でピアニストがその曲を弾いたとき、娘がいつも違う音で弾く場所で正しい音が鳴ったので、男は「間違えた」と本気で思った。隣の妻も毎晩娘の練習を聞いていたので、夫がどこで覚えた曲なのかがすぐに分かり、こらえきれずに笑った。間違えていたのはピアニストではなく、男が覚えた曲のほうだった。',
        '["ピアニストは一音も間違えていない。楽譜どおりの正しい演奏だった","男は音楽に詳しくなく、ピアノも弾けない","男の耳や記憶力に問題があるわけではない","男はその曲をよく知っていて、鼻歌で歌えるほどだった","男がその曲を覚えたのは、CD・テレビ・ラジオ・動画からではない","男はその曲を、演奏会の前から毎日のように聞いていた","男が聞き慣れていた曲は、ある一か所がいつも同じように違っていた（なぜ違うのかは答えの核心。正解宣言のとき以外は補足で言わない）","別の編曲・別の版の楽譜の話ではない","隣の女は男の妻で、男がなぜそう言ったのかをすぐに分かった","女は男をばかにしたのではない。おかしくて、ほほえましくて笑った","ピアニストの名前・曲名・会場の場所は問題に関係ない"]',
        '[{"q":"ピアニストは本当に間違えましたか？","a":"いいえ"},{"q":"男は音楽の専門家ですか？","a":"いいえ"},{"q":"男はその曲を知っていましたか？","a":"はい"},{"q":"男は別の編曲を聴き慣れていたのですか？","a":"いいえ"},{"q":"男は耳が悪いのですか？","a":"いいえ"},{"q":"男はその曲をCDやテレビで覚えましたか？","a":"いいえ"},{"q":"男は誰かが弾くのを聞いて曲を覚えましたか？","a":"はい"},{"q":"それは男の家族ですか？","a":"はい"},{"q":"その家族はプロのピアニストですか？","a":"いいえ"},{"q":"その家族はピアノを習っている途中ですか？","a":"はい"},{"q":"家族の弾き方には、いつも違うところがありましたか？","a":"はい"},{"q":"隣の女は男の家族ですか？","a":"はい"},{"q":"女は男をばかにして笑ったのですか？","a":"いいえ"},{"q":"女には男がそう言った理由が分かりましたか？","a":"はい"},{"q":"曲名は関係ありますか？","a":"関係ない"},{"q":"会場の場所は関係ありますか？","a":"関係ない"},{"q":"男は、娘が家で毎晩同じところを間違えて弾く練習を聞いてその曲を覚えていたので、ピアニストの正しい演奏を間違いだと思った。","a":"正解"}]',
        '間違えたのは誰か', '「はい / いいえ / 関係ない」で答えられる質問をコメントしてね。出題者が全部返事します',
        '{"problem":"ピアノの演奏会で、男は途中で、あ、間違えた、と小声で言った。ピアニストの演奏は一音も外さない完璧なものだった。隣で聞いた女は、こらえきれずに吹き出した。どういうこと？","rule":"はい、いいえ、関係ない、で答えられる質問をコメントしてね。全部返事するよ。"}',
        '[{"role":"questioner","text":"ピアニストが間違えた？"},{"role":"master","text":"いいえ。"},{"role":"questioner","text":"男はその曲を知ってた？"},{"role":"master","text":"はい！"},{"role":"questioner","text":"CDで覚えた？"},{"role":"master","text":"いいえ。"}]',
        '{"master":{"intro":"質問してみて！","outro":"何度でも答えるよ。コメントで質問！"},"jr":{"outro":"面白かったら、いいね、フォローよろしくね！"}}',
        'A stylized 1990s Japanese OVA anime background painting (hand-painted cel-era background art, poster-color textures, clean shapes, thick brush-like outlines on key objects). Mid-key lighting: moonlight, lamps or candlelight keep the whole scene clearly visible, NOT dark.

Scene: Inside a small concert hall, a pianist in formal clothes playing a grand piano on the stage under warm stage lights; in the audience seats a man leans toward the woman beside him and whispers with a puzzled, serious face, while the woman covers her mouth, trying hard not to burst out laughing; no child, no sheet music, no text.

Vertical 9:16 composition (1024x1536). No text, no letters, no numbers, no logos, no signs. Depict only the scene described in the problem statement; do not depict any clue to the story''s hidden truth. People: only the persons who appear in the problem, plus at most one distant silhouette. Keep the upper 55% of the image calm and simple (sky, wall, ceiling, window) so that text cards can be overlaid there.',
        '【探偵カメロックのウミガメのスープ】

ピアノの演奏会で、男は途中で「あ、間違えた」と小声で言った。ピアニストの演奏は一音も外さない完璧なものだった。隣で聞いた女は、こらえきれずに吹き出した。どういうこと？

「はい / いいえ / 関係ない」で答えられる質問をコメントしてね。出題者の探偵カメロックが全部返事します。正解が出るまで何度でもどうぞ。

#ウミガメのスープ #水平思考 #推理クイズ #なぞなぞ #謎解き #クイズ #AIart',
        '完全オリジナル（既存問題の転載・改変ではない）。作問法は note 記事 https://note.com/suekai0217/n/n35128e606a9b の4 ステップ（モチーフ → 連想 → 言い方を変える → 不思議にする）と良い問題の 3 条件（コアが明確・動線がある・現実離れしない）に従う。着想の型は research.md（Codex Web リサーチ台帳）を参照。 型: 物語復元型（物語先行方式・21-4a-4 で新方式の初通過）。モチーフ「ピアノ」（抽選: ハンコ / ピアノ / ポスト）→ 連想（発表会・家での練習をいつも聞いている親・同じ箇所で止まる 等 16 件）→ 物語「娘の練習の間違いごと曲を覚えた父」→ 隠した B = 娘が毎晩同じ箇所で間違える練習を聞いて曲を覚えていたこと。着想元の既存問題なし（台帳 #09「音楽が止まって困る曲芸師」は音の実用的役割で構造が別）。Web 照合（ラテシン・らてらて・note・X・英語圏）で同一・近い真相の投稿問題なし。素材化時に場面を発表会の講師演奏から一般の演奏会へ移した（教室・発表会は家族に習う人がいる手がかりになるため）。', 1);

-- U21 一年越しの判定
INSERT INTO umigame_stock_items (set_id, content_key, title, difficulty, problem_text, truth, fact_sheet,
    expected_questions, hook, rule_text, narration, play_example, character_lines, illustration_prompt,
    caption, source_note, is_active)
VALUES ((SELECT id FROM batch_sets WHERE set_code = 'umigame-soup-1'),
        '009-year-late-verdict', '一年越しの判定', 4,
        '夏、男は弟と実家へ帰った。庭のいちばん奥のすみに、小さなすいかが一つ実っていた。男はそれをしばらく黙って眺めてから、笑って弟に「お前の勝ちだ」と言った。どういうこと？',
        '去年の夏、30 代の兄弟は実家の縁側ですいかを食べながら、子どものころのように種飛ばしで勝負した。兄の種は縁側のすぐ先に落ちるのを二人とも見ていた。弟は「庭のいちばん奥の塀ぎわまで飛んだ」と言い張ったが、種は草の中に消えて見つからず、兄は「そこまで飛ぶわけがない」と自分の勝ちを譲らなかった。今年の夏に帰省すると、庭のいちばん奥のすみに、誰も植えていないすいかが実っていた。母はすいかを植えておらず、あの縁側で種を飛ばしたのは去年のあの日だけだった。弟の種は本当に塀ぎわまで飛んでいて、そこで芽を出して育ったのだ。一年越しに証拠が出てきたので、男は笑って負けを認めた。',
        '["すいかは男の母も家族も植えていない。すいかを育てる勝負をしていたのでもない","すいかは誰かが持ってきて置いたものではなく、その場所で自然に育った","男と弟は 30 代の大人で、子どもではない","男と弟は、ちょうど一年前の夏に、この実家である勝負をしていた","その勝負はお金や物を賭けたものではない","勝負のとき、決め手になるものが見つからず、二人とも自分の勝ちを言い張った（何が見つからなかったかは答えの核心。正解宣言のとき以外は補足で言わない）","すいかが実っていた場所が、勝負の結果と関係している","男は負けを認めたが、悔しいというより愉快だった","すいかの大きさ・味・品種は問題に関係ない","母や兄弟の仕事・住まいは問題に関係ない"]',
        '[{"q":"すいかは誰かが植えたものですか？","a":"いいえ"},{"q":"すいかを育てる勝負をしていましたか？","a":"いいえ"},{"q":"すいかの大きさを比べる勝負ですか？","a":"いいえ"},{"q":"お金を賭けていましたか？","a":"いいえ"},{"q":"二人は以前に何かの勝負をしましたか？","a":"はい"},{"q":"その勝負は実家でしましたか？","a":"はい"},{"q":"その勝負は去年のことですか？","a":"はい"},{"q":"その勝負は、その場で決着がつきましたか？","a":"いいえ"},{"q":"すいかが実っていた場所は関係ありますか？","a":"はい"},{"q":"すいかは種から自然に育ちましたか？","a":"はい"},{"q":"勝負はすいかを食べたときにしましたか？","a":"はい"},{"q":"勝負に、すいかの種が関係していますか？","a":"はい"},{"q":"二人は子どもですか？","a":"いいえ"},{"q":"男は悔しがっていますか？","a":"いいえ"},{"q":"すいかの味は関係ありますか？","a":"関係ない"},{"q":"母の仕事は関係ありますか？","a":"関係ない"},{"q":"去年の夏、二人は実家ですいかの種飛ばしをして、弟は庭の奥まで飛んだと言い張ったが種が見つからなかった。その種が育ってすいかが実ったので、弟の勝ちだと分かった。","a":"正解"}]',
        'すいかが下した判定', '「はい / いいえ / 関係ない」で答えられる質問をコメントしてね。出題者が全部返事します',
        '{"problem":"夏、男は弟と実家へ帰った。庭のいちばん奥のすみに、小さなすいかが一つ実っていた。男はそれをしばらく黙って眺めてから、笑って弟に、お前の勝ちだ、と言った。どういうこと？","rule":"はい、いいえ、関係ない、で答えられる質問をコメントしてね。全部返事するよ。"}',
        '[{"role":"questioner","text":"すいかは誰かが植えた？"},{"role":"master","text":"いいえ。"},{"role":"questioner","text":"前に何か勝負をした？"},{"role":"master","text":"はい！"},{"role":"questioner","text":"大きさ比べの勝負？"},{"role":"master","text":"いいえ。"}]',
        '{"master":{"intro":"質問してみて！","outro":"何度でも答えるよ。コメントで質問！"},"jr":{"outro":"面白かったら、いいね、フォローよろしくね！"}}',
        'A stylized 1990s Japanese OVA anime background painting (hand-painted cel-era background art, poster-color textures, clean shapes, thick brush-like outlines on key objects). Mid-key lighting: moonlight, lamps or candlelight keep the whole scene clearly visible, NOT dark.

Scene: A sunny summer afternoon in the garden of a Japanese family house with a wooden veranda; two adult brothers in their thirties stand at the far corner of the garden by the fence, looking down at a single small watermelon growing on a vine in the grass; one man grins and pats his brother on the shoulder, the other smiles proudly; no seeds, no people eating, no text.

Vertical 9:16 composition (1024x1536). No text, no letters, no numbers, no logos, no signs. Depict only the scene described in the problem statement; do not depict any clue to the story''s hidden truth. People: only the persons who appear in the problem, plus at most one distant silhouette. Keep the upper 55% of the image calm and simple (sky, wall, ceiling, window) so that text cards can be overlaid there.',
        '【探偵カメロックのウミガメのスープ】

夏、男は弟と実家へ帰った。庭のいちばん奥のすみに、小さなすいかが一つ実っていた。男はそれをしばらく黙って眺めてから、笑って弟に「お前の勝ちだ」と言った。どういうこと？

「はい / いいえ / 関係ない」で答えられる質問をコメントしてね。出題者の探偵カメロックが全部返事します。正解が出るまで何度でもどうぞ。

#ウミガメのスープ #水平思考 #推理クイズ #なぞなぞ #謎解き #クイズ #AIart',
        '完全オリジナル（既存問題の転載・改変ではない）。作問法は note 記事 https://note.com/suekai0217/n/n35128e606a9b の4 ステップ（モチーフ → 連想 → 言い方を変える → 不思議にする）と良い問題の 3 条件（コアが明確・動線がある・現実離れしない）に従う。着想の型は research.md（Codex Web リサーチ台帳）を参照。 型: 物語復元型（物語先行方式）。モチーフ「すいか」（抽選: 階段 / すいか / コンビニ）→ 連想（縁側・兄弟の種飛ばし競争・勝ち負けの言い争い・草に消える種・捨てた種から翌年芽が出る 等 10 件）→ 物語「種飛ばしの勝負が一年後に庭のすいかで決着した」→ 隠した B = 去年の種飛ばしで弟の種が本当に塀ぎわまで飛んでいたこと。着想元の既存問題なし（台帳に該当なし）。Web 照合（WebSearch 3 クエリ）で同一・近い真相の投稿問題なし。捨てた種から翌年すいかが生える実例の投稿で現実性を確認。', 1);

-- U22 二時間かけて通う歯医者
INSERT INTO umigame_stock_items (set_id, content_key, title, difficulty, problem_text, truth, fact_sheet,
    expected_questions, hook, rule_text, narration, play_example, character_lines, illustration_prompt,
    caption, source_note, is_active)
VALUES ((SELECT id FROM batch_sets WHERE set_code = 'umigame-soup-1'),
        '010-two-hour-dentist', '二時間かけて通う歯医者', 4,
        '虫歯も痛いところもない男が、電車で二時間かけて、ある町の小さな歯医者に半年ごとに通っている。診察が終わっても、男はしばらく待合室の同じ席に座ってから帰る。どういうこと？',
        '男は小学生のころまで、その町の古い木造の家で育った。父の転勤で一家は引っ越し、家は人手に渡った。家を買った人は、1 階を改装して小さな歯医者を開いた。四十年後、男はそのことを知り、中に入る方法として、半年ごとの歯の検診をその歯医者で受けることにした。今の家からは電車で二時間かかるが、男には虫歯も痛みもない。待合室の柱には、子どものころに父が刻んだ男の背丈の傷がそのまま残っている。男は診察のあと、その柱の前の席にしばらく座ってから帰る。男が通っているのは、歯医者になった自分の生家だった。',
        '["男には虫歯も痛いところもなく、特別な治療も受けていない。受けているのは半年ごとのふつうの検診","歯医者の先生・受付の人・ほかの患者は、男の知り合いでも家族でもない","その歯医者の腕や料金・設備が特別に良いわけではない","男は子どものころ、その町に住んでいた。今は電車で二時間かかる別の町に住んでいる","歯医者は古い建物を改装して開かれた小さな医院で、四十年ほど前にはまだ歯医者ではなかった","男が通う理由は、歯医者の建物そのものにある（どういう建物かは答えの核心。正解宣言のとき以外は補足で言わない）","待合室の男がいつも座る席の近くに、男にとって大切なものが残っている（それが何かは答えの核心。正解宣言のとき以外は補足で言わない）","先生は男が通う理由を知らない。男は誰にも迷惑をかけていない","男は悲しんでいるのではなく、懐かしんでいる","男の仕事・家族構成・年齢は問題に関係ない","電車の路線・歯医者の名前は問題に関係ない"]',
        '[{"q":"先生の腕がいいからですか？","a":"いいえ"},{"q":"先生は男の知り合いですか？","a":"いいえ"},{"q":"受付の人に会いに行っていますか？","a":"いいえ"},{"q":"料金が安いからですか？","a":"いいえ"},{"q":"特別な治療を受けていますか？","a":"いいえ"},{"q":"歯医者という場所に理由がありますか？","a":"はい"},{"q":"男はその町に住んでいたことがありますか？","a":"はい"},{"q":"その歯医者は昔から歯医者でしたか？","a":"いいえ"},{"q":"歯医者の建物は昔、別の用途でしたか？","a":"はい"},{"q":"男はその建物に入ったことがありましたか？","a":"はい"},{"q":"待合室に男の思い出の物がありますか？","a":"はい"},{"q":"男は悲しんでいますか？","a":"いいえ"},{"q":"男の仕事は関係ありますか？","a":"関係ない"},{"q":"電車の路線は関係ありますか？","a":"関係ない"},{"q":"男は歯医者が好きなのですか？","a":"いいえ"},{"q":"その歯医者は、男が子どものころに育った家を改装したもので、男は検診を口実に自分の生家に通っている。","a":"正解"}]',
        '虫歯のない男の通院', '「はい / いいえ / 関係ない」で答えられる質問をコメントしてね。出題者が全部返事します',
        '{"problem":"虫歯も痛いところもない男が、電車で二時間かけて、ある町の小さな歯医者に半年ごとに通っている。診察が終わっても、男はしばらく待合室の同じ席に座ってから帰る。どういうこと？","rule":"はい、いいえ、関係ない、で答えられる質問をコメントしてね。全部返事するよ。"}',
        '[{"role":"questioner","text":"先生が知り合い？"},{"role":"master","text":"いいえ。"},{"role":"questioner","text":"場所に理由がある？"},{"role":"master","text":"はい！"},{"role":"questioner","text":"腕のいい先生？"},{"role":"master","text":"いいえ。"}]',
        '{"master":{"intro":"質問してみて！","outro":"何度でも答えるよ。コメントで質問！"},"jr":{"outro":"面白かったら、いいね、フォローよろしくね！"}}',
        'A stylized 1990s Japanese OVA anime background painting (hand-painted cel-era background art, poster-color textures, clean shapes, thick brush-like outlines on key objects). Mid-key lighting: moonlight, lamps or candlelight keep the whole scene clearly visible, NOT dark.

Scene: The small waiting room of a quiet dental clinic set inside an old renovated Japanese wooden house, afternoon light through a window; a man in his fifties sits alone on a bench by a dark wooden pillar, looking around the room with a gentle, nostalgic smile; a reception window in the background; no marks on the pillar, no dentist, no text.

Vertical 9:16 composition (1024x1536). No text, no letters, no numbers, no logos, no signs. Depict only the scene described in the problem statement; do not depict any clue to the story''s hidden truth. People: only the persons who appear in the problem, plus at most one distant silhouette. Keep the upper 55% of the image calm and simple (sky, wall, ceiling, window) so that text cards can be overlaid there.',
        '【探偵カメロックのウミガメのスープ】

虫歯も痛いところもない男が、電車で二時間かけて、ある町の小さな歯医者に半年ごとに通っている。診察が終わっても、男はしばらく待合室の同じ席に座ってから帰る。どういうこと？

「はい / いいえ / 関係ない」で答えられる質問をコメントしてね。出題者の探偵カメロックが全部返事します。正解が出るまで何度でもどうぞ。

#ウミガメのスープ #水平思考 #推理クイズ #なぞなぞ #謎解き #クイズ #AIart',
        '完全オリジナル（既存問題の転載・改変ではない）。作問法は note 記事 https://note.com/suekai0217/n/n35128e606a9b の4 ステップ（モチーフ → 連想 → 言い方を変える → 不思議にする）と良い問題の 3 条件（コアが明確・動線がある・現実離れしない）に従う。着想の型は research.md（Codex Web リサーチ台帳）を参照。 型: 物語復元型（物語先行方式）。モチーフ「歯医者」（抽選: ストロー / くしゃみ / 歯医者。引き直し: 帽子 / 風船 / ヘルメット）→ 連想（待合室・定期検診・先生と患者の関係・開業 / 改装した医院・町の古い医院 等 10 件）→ 物語「育った家が歯医者になり、男が患者として通う」→ 隠した B = その歯医者が男の育った家を改装したものであること。着想元の既存問題なし（台帳に該当なし）。Web 照合（WebSearch 3 クエリ）で同一・近い真相の投稿問題・小話なし。', 1);

-- U23 おじいさんのお釣り
INSERT INTO umigame_stock_items (set_id, content_key, title, difficulty, problem_text, truth, fact_sheet,
    expected_questions, hook, rule_text, narration, play_example, character_lines, illustration_prompt,
    caption, source_note, is_active)
VALUES ((SELECT id FROM batch_sets WHERE set_code = 'umigame-soup-1'),
        '011-grandpas-change', 'おじいさんのお釣り', 4,
        '女の子は見つけて集めたお金で、おじいさんの誕生日に缶コーヒーを買って渡した。お金は元は全部おじいさんのもので、おこづかいではない。おじいさんは大笑いした。どういうこと？',
        'おじいさんは小さな酒屋を営み、店の前に自動販売機を一台置いている。小学生の孫の女の子は、登校の途中に毎朝その自販機のお釣りの取り出し口をのぞくのが好きだった。おじいさんは「おじいちゃんの自販機だから、残っていたお金はもらっていいよ」と言い、毎朝孫が通る前に、取り出し口へこっそり十円玉を一枚入れておいた。女の子は「今日もあった」と喜んで、十円玉を瓶にためていった。おじいさんの誕生日、女の子はためた十円玉を持って店の前の自販機で缶コーヒーを一本買い、おじいさんに渡した。自分が入れた十円玉が、自分の自販機に戻ってきて缶コーヒーになったので、おじいさんは大笑いした。',
        '["お金はおこづかい・お年玉・お手伝いの代金ではない。女の子がおじいさんの財布や家から持ち出したものでもない","女の子は、毎朝同じ場所にあった十円玉を一枚ずつ拾い、数か月かけてためた。道に落ちていたお金ではない","女の子がお金を見つけた場所は、おじいさんの持ち物だった（それが何かは答えの核心。正解宣言のとき以外は補足で言わない）","十円玉がそこにあったのは偶然ではない（どうしてあったかは答えの核心。正解宣言のとき以外は補足で言わない）","おじいさんは前から女の子に「その場所で見つけたお金はもらってよい」と言っていた。女の子は悪いことをしていない","女の子は、そのお金がもともとおじいさんのものだとは知らなかった","おじいさんはお店を営んでいる。女の子は缶コーヒーを、おじいさんのお店のものから買った","缶コーヒーの代金は、結局おじいさんのところへ戻った","おじいさんは怒っていない。うれしくて、おかしくて笑った","女の子の年齢・ほかの家族・缶コーヒーの銘柄は問題に関係ない"]',
        '[{"q":"おこづかいをためたのですか？","a":"いいえ"},{"q":"お年玉ですか？","a":"いいえ"},{"q":"おじいさんの財布から取りましたか？","a":"いいえ"},{"q":"女の子はお金を拾ったのですか？","a":"はい"},{"q":"道に落ちていたお金ですか？","a":"いいえ"},{"q":"毎日同じ場所で見つけましたか？","a":"はい"},{"q":"お金はおじいさんがわざと置いていましたか？","a":"はい"},{"q":"女の子はそれを知っていましたか？","a":"いいえ"},{"q":"おじいさんはお店をしていますか？","a":"はい"},{"q":"缶コーヒーはおじいさんのお店のものですか？","a":"はい"},{"q":"自動販売機に関係がありますか？","a":"はい"},{"q":"女の子は悪いことをしましたか？","a":"いいえ"},{"q":"おじいさんは怒っていますか？","a":"いいえ"},{"q":"缶コーヒーの銘柄は関係ありますか？","a":"関係ない"},{"q":"女の子の年齢は関係ありますか？","a":"関係ない"},{"q":"おじいさんが毎朝、自分の店の自販機のお釣りの出口に十円玉を入れておき、女の子はそれを集めて、そのお金でおじいさんの自販機から缶コーヒーを買った。","a":"正解"}]',
        '代金を出したのは誰？', '「はい / いいえ / 関係ない」で答えられる質問をコメントしてね。出題者が全部返事します',
        '{"problem":"女の子は見つけて集めたお金で、おじいさんの誕生日に缶コーヒーを買って渡した。お金は元は全部おじいさんのもので、おこづかいではない。おじいさんは大笑いした。どういうこと？","rule":"はい、いいえ、関係ない、で答えられる質問をコメントしてね。全部返事するよ。"}',
        '[{"role":"questioner","text":"おこづかい？"},{"role":"master","text":"いいえ。"},{"role":"questioner","text":"拾ったお金？"},{"role":"master","text":"はい！"},{"role":"questioner","text":"道に落ちてた？"},{"role":"master","text":"いいえ。"}]',
        '{"master":{"intro":"質問してみて！","outro":"何度でも答えるよ。コメントで質問！"},"jr":{"outro":"面白かったら、いいね、フォローよろしくね！"}}',
        'A stylized 1990s Japanese OVA anime background painting (hand-painted cel-era background art, poster-color textures, clean shapes, thick brush-like outlines on key objects). Mid-key lighting: moonlight, lamps or candlelight keep the whole scene clearly visible, NOT dark.

Scene: In front of a small old neighborhood shop in a quiet Japanese town, morning light; a young girl with a school backpack happily holds out a can of coffee with both hands to her grandfather, who laughs heartily with his head tilted back; a glass jar is not shown, no vending machine, no coins, no text.

Vertical 9:16 composition (1024x1536). No text, no letters, no numbers, no logos, no signs. Depict only the scene described in the problem statement; do not depict any clue to the story''s hidden truth. People: only the persons who appear in the problem, plus at most one distant silhouette. Keep the upper 55% of the image calm and simple (sky, wall, ceiling, window) so that text cards can be overlaid there.',
        '【探偵カメロックのウミガメのスープ】

女の子は見つけて集めたお金で、おじいさんの誕生日に缶コーヒーを買って渡した。お金は元は全部おじいさんのもので、おこづかいではない。おじいさんは大笑いした。どういうこと？

「はい / いいえ / 関係ない」で答えられる質問をコメントしてね。出題者の探偵カメロックが全部返事します。正解が出るまで何度でもどうぞ。

#ウミガメのスープ #水平思考 #推理クイズ #なぞなぞ #謎解き #クイズ #AIart',
        '完全オリジナル（既存問題の転載・改変ではない）。作問法は note 記事 https://note.com/suekai0217/n/n35128e606a9b の4 ステップ（モチーフ → 連想 → 言い方を変える → 不思議にする）と良い問題の 3 条件（コアが明確・動線がある・現実離れしない）に従う。着想の型は research.md（Codex Web リサーチ台帳）を参照。 型: 物語復元型（物語先行方式）。モチーフ「自動販売機」（抽選: シール / 時計 / 自動販売機。引き直し 2 回: たまご / 毛糸 / 片づけ・くしゃみ / 朝顔 / チャイム）→ 連想（お釣りの取り出し口をのぞく子ども・当たり付き・店先の自販機・売り上げは持ち主に入る 等 9 件）→ 物語「祖父がこっそり置いた十円玉が孫の贈り物になって戻る」→ 隠した B = 祖父が毎朝自分の自販機のお釣り口に十円玉を入れ、孫がそれを集めていたこと。着想元の既存問題なし（台帳に該当なし）。Web 照合（WebSearch 4 クエリ）で同一・近い真相の投稿問題・小話なし。', 1);

-- U24 早く走った朝
INSERT INTO umigame_stock_items (set_id, content_key, title, difficulty, problem_text, truth, fact_sheet,
    expected_questions, hook, rule_text, narration, play_example, character_lines, illustration_prompt,
    caption, source_note, is_active)
VALUES ((SELECT id FROM batch_sets WHERE set_code = 'umigame-soup-1'),
        '012-early-morning-run', '早く走った朝', 4,
        '男がいつもより早くジョギングに出た朝、通学路の家から小学生が次々に飛び出してきて、男を追い抜いて学校へ走っていった。誰も遅刻しそうではなかった。どういうこと？',
        '男は十年ほど、毎朝七時四十分ちょうどに家を出て、小学校の通学路をジョギングしていた。通学路の家の子どもたちは、窓の外を男が走って通るのを見ると「そろそろ出なきゃ」と家を出るようになっていたが、男はそのことを知らなかった。ある朝、男は用事があって、いつもより二十分早く走り出た。男の姿を見た子どもたちは、遅刻すると思い込んで朝ごはんを口にくわえたまま次々に家を飛び出し、男を追い抜いて学校へ駆けていった。実際の時刻はまだ早く、子どもたちは校門が開くより先に門の前に並ぶことになった。',
        '["子どもたちは男を怖がっていない。男は不審者でも、学校の先生でもない","その朝、学校に特別な行事はなかった。鬼ごっこや競走などの遊びでもない","男は子どもたちに何も言っていないし、合図を送ったつもりもない","男は十年ほど、毎朝同じ道を同じように走っている","子どもたちは、家の窓から男の姿を見て、急がなければと思った（なぜそう思ったかは答えの核心。正解宣言のとき以外は補足で言わない）","子どもたちは実際には遅刻しそうではなかった。学校に着いたとき、校門はまだ開いていなかった","家の時計は壊れていない。時計を見ていれば、まだ早いと分かった","男は、子どもたちが走っていった理由をその朝まで知らなかった","男がいつもより早く走ったのは用事があったから。用事の中身は問題に関係ない","子どもたちは男の家族でも知り合いでもない。名前も知らない","男の年齢・服装・走る速さは問題に関係ない"]',
        '[{"q":"子どもたちは男が怖かったのですか？","a":"いいえ"},{"q":"男は学校の先生ですか？","a":"いいえ"},{"q":"学校で行事がありましたか？","a":"いいえ"},{"q":"鬼ごっこをしていたのですか？","a":"いいえ"},{"q":"男が子どもたちに何か言いましたか？","a":"いいえ"},{"q":"子どもたちは男を見て走り出しましたか？","a":"はい"},{"q":"子どもたちは遅刻すると思ったのですか？","a":"はい"},{"q":"本当に遅刻しそうでしたか？","a":"いいえ"},{"q":"家の時計が壊れていましたか？","a":"いいえ"},{"q":"男はいつも同じ時間に走っていますか？","a":"はい"},{"q":"男が走る時間と関係がありますか？","a":"はい"},{"q":"男は子どもたちの様子を知っていましたか？","a":"いいえ"},{"q":"子どもたちは男の知り合いですか？","a":"いいえ"},{"q":"男が早く出た理由は関係ありますか？","a":"関係ない"},{"q":"男の服装は関係ありますか？","a":"関係ない"},{"q":"子どもたちは毎朝同じ時刻に通学路を走る男を見て家を出る時刻を決めていたので、男がいつもより早く通った朝、遅刻すると思って飛び出した。","a":"正解"}]',
        '子どもたちは何を見た？', '「はい / いいえ / 関係ない」で答えられる質問をコメントしてね。出題者が全部返事します',
        '{"problem":"男がいつもより早くジョギングに出た朝、通学路の家から小学生が次々に飛び出してきて、男を追い抜いて学校へ走っていった。誰も遅刻しそうではなかった。どういうこと？","rule":"はい、いいえ、関係ない、で答えられる質問をコメントしてね。全部返事するよ。"}',
        '[{"role":"questioner","text":"男が怖かった？"},{"role":"master","text":"いいえ。"},{"role":"questioner","text":"男を見て走った？"},{"role":"master","text":"はい！"},{"role":"questioner","text":"男は先生？"},{"role":"master","text":"いいえ。"}]',
        '{"master":{"intro":"質問してみて！","outro":"何度でも答えるよ。コメントで質問！"},"jr":{"outro":"面白かったら、いいね、フォローよろしくね！"}}',
        'A stylized 1990s Japanese OVA anime background painting (hand-painted cel-era background art, poster-color textures, clean shapes, thick brush-like outlines on key objects). Mid-key lighting: moonlight, lamps or candlelight keep the whole scene clearly visible, NOT dark.

Scene: A quiet Japanese residential street on a school route in the early morning; a middle-aged man in jogging clothes looks back in surprise as several elementary school children with school backpacks dash past him toward school, one child holding a piece of toast in the mouth; houses with windows along the street, no clocks, no text.

Vertical 9:16 composition (1024x1536). No text, no letters, no numbers, no logos, no signs. Depict only the scene described in the problem statement; do not depict any clue to the story''s hidden truth. People: only the persons who appear in the problem, plus at most one distant silhouette. Keep the upper 55% of the image calm and simple (sky, wall, ceiling, window) so that text cards can be overlaid there.',
        '【探偵カメロックのウミガメのスープ】

男がいつもより早くジョギングに出た朝、通学路の家から小学生が次々に飛び出してきて、男を追い抜いて学校へ走っていった。誰も遅刻しそうではなかった。どういうこと？

「はい / いいえ / 関係ない」で答えられる質問をコメントしてね。出題者の探偵カメロックが全部返事します。正解が出るまで何度でもどうぞ。

#ウミガメのスープ #水平思考 #推理クイズ #なぞなぞ #謎解き #クイズ #AIart',
        '完全オリジナル（既存問題の転載・改変ではない）。作問法は note 記事 https://note.com/suekai0217/n/n35128e606a9b の4 ステップ（モチーフ → 連想 → 言い方を変える → 不思議にする）と良い問題の 3 条件（コアが明確・動線がある・現実離れしない）に従う。着想の型は research.md（Codex Web リサーチ台帳）を参照。 型: 物語復元型（物語先行方式）。モチーフ「マラソン」「足音」（2 巡目の抽選: ろうそく / はしご / マラソン・弁当 / 豆まき / ろうそく・足音 / 日記 / ゴミ出し ほか）→ 連想（毎朝のジョギング・同じ時刻・通学路・すれ違う小学生・「あの人が通ったら家を出る」・遅刻 等 8 件）→ 物語「毎朝同じ時刻に走る男が、知らないうちに通学路の子どもたちの時計になっていた」→ 隠した B = 子どもたちが男を見て家を出る時刻を決めていたこと。着想元の既存問題なし（台帳に該当なし。「カントの散歩」の逸話と構造が近い点は人間ゲートで承認）。Web 照合（WebSearch 2 クエリ）で同一・近い真相の投稿問題・小話なし。', 1);

-- U25 五十五年目の年賀状
INSERT INTO umigame_stock_items (set_id, content_key, title, difficulty, problem_text, truth, fact_sheet,
    expected_questions, hook, rule_text, narration, play_example, character_lines, illustration_prompt,
    caption, source_note, is_active)
VALUES ((SELECT id FROM batch_sets WHERE set_code = 'umigame-soup-1'),
        '013-fifty-five-year-nengajo', '五十五年目の年賀状', 4,
        '七十歳の男は元日、ある友人から届いた年賀状を読むと、家族の前で「勝った！」と万歳した。二人は中学を卒業してから五十五年間、一度も会っていない。どういうこと？',
        '男は中学三年の春、放課後に友人と指していた将棋を終えないまま、友人の転校で離ればなれになった。二人は「続きは年賀状で」と約束し、それから毎年の年賀状に将棋の一手ずつを書いて送り合った。男は元日に届いた相手の一手を一年かけて考え、年末に次の一手を書いて出した。盤は駒を並べたまま、男の家の床の間に五十五年間置かれていた。七十歳の元日、友人の年賀状には次の一手の代わりに「参りました」と書かれていた。男は五十五年かけた一局に勝ち、家族の前で万歳した。二人は卒業以来、一度も会っていない。',
        '["年賀状は友人本人が書いたもの。友人は元気に暮らしている","男はくじに当たったのではない。お金や品物は何ももらっていない","二人は何も賭けていない。お金や物のやりとりはない","長生きや、子ども・孫の数、年賀状の枚数を比べていたのではない","二人は中学の同級生。中学三年の春に友人が転校し、別の町へ引っ越した","二人は卒業してから電話もしていない。毎年の年賀状だけをやりとりしている","年賀状には、新年のあいさつのほかに短い言葉が書かれていた（何が書かれていたかは答えの核心。正解宣言のとき以外は補足で言わない）","二人がしていたのは体を動かす勝負ではなく、頭を使う勝負","勝負は中学のころに始まり、五十五年かけてこの元日に決着した","男は毎年、この友人への年賀状を書くのに長い時間をかけていた","家族は、男がこの友人と勝負を続けていることを知っていた","男の仕事、友人の住む町、年賀状の絵柄は問題に関係ない"]',
        '[{"q":"くじに当たったのですか？","a":"いいえ"},{"q":"何かを賭けていたのですか？","a":"いいえ"},{"q":"友人は亡くなったのですか？","a":"いいえ"},{"q":"長生きを競っていたのですか？","a":"いいえ"},{"q":"二人は何かの勝負をしていたのですか？","a":"はい"},{"q":"体を動かす勝負ですか？","a":"いいえ"},{"q":"年賀状に書かれていた言葉が関係ありますか？","a":"はい"},{"q":"友人が負けを認めたのですか？","a":"はい"},{"q":"盤を使うゲームですか？","a":"はい"},{"q":"年賀状で勝負を進めていたのですか？","a":"はい"},{"q":"勝負は中学のころに始まりましたか？","a":"はい"},{"q":"二人は電話で話していましたか？","a":"いいえ"},{"q":"家族は勝負のことを知っていましたか？","a":"はい"},{"q":"男の仕事は関係ありますか？","a":"関係ない"},{"q":"年賀状の絵柄は関係ありますか？","a":"関係ない"},{"q":"二人は中学のときに終わらなかった将棋の続きを、毎年の年賀状に一手ずつ書いて指していて、この元日の年賀状で友人が負けを認めた。","a":"正解"}]',
        '何に勝ったのか？', '「はい / いいえ / 関係ない」で答えられる質問をコメントしてね。出題者が全部返事します',
        '{"problem":"七十歳の男は元日、ある友人から届いた年賀状を読むと、家族の前で、勝ったと言って万歳した。二人は中学を卒業してから五十五年間、一度も会っていない。どういうこと？","rule":"はい、いいえ、関係ない、で答えられる質問をコメントしてね。全部返事するよ。"}',
        '[{"role":"questioner","text":"くじに当たった？"},{"role":"master","text":"いいえ。"},{"role":"questioner","text":"友人と勝負してた？"},{"role":"master","text":"はい！"},{"role":"questioner","text":"何か賭けてた？"},{"role":"master","text":"いいえ。"}]',
        '{"master":{"intro":"質問してみて！","outro":"何度でも答えるよ。コメントで質問！"},"jr":{"outro":"面白かったら、いいね、フォローよろしくね！"}}',
        'A stylized 1990s Japanese OVA anime background painting (hand-painted cel-era background art, poster-color textures, clean shapes, thick brush-like outlines on key objects). Mid-key lighting: moonlight, lamps or candlelight keep the whole scene clearly visible, NOT dark.

Scene: A Japanese tatami living room on New Year''s morning; an elderly man in his seventies raises both arms in joy while holding a single New Year''s postcard, his wife and grown-up family around a low table with New Year''s dishes look at him with amused smiles; a pile of other postcards on the table, no readable writing, no text.

Vertical 9:16 composition (1024x1536). No text, no letters, no numbers, no logos, no signs. Depict only the scene described in the problem statement; do not depict any clue to the story''s hidden truth. People: only the persons who appear in the problem, plus at most one distant silhouette. Keep the upper 55% of the image calm and simple (sky, wall, ceiling, window) so that text cards can be overlaid there.',
        '【探偵カメロックのウミガメのスープ】

七十歳の男は元日、ある友人から届いた年賀状を読むと、家族の前で「勝った！」と万歳した。二人は中学を卒業してから五十五年間、一度も会っていない。どういうこと？

「はい / いいえ / 関係ない」で答えられる質問をコメントしてね。出題者の探偵カメロックが全部返事します。正解が出るまで何度でもどうぞ。

#ウミガメのスープ #水平思考 #推理クイズ #なぞなぞ #謎解き #クイズ #AIart',
        '完全オリジナル（既存問題の転載・改変ではない）。作問法は note 記事 https://note.com/suekai0217/n/n35128e606a9b の4 ステップ（モチーフ → 連想 → 言い方を変える → 不思議にする）と良い問題の 3 条件（コアが明確・動線がある・現実離れしない）に従う。着想の型は research.md（Codex Web リサーチ台帳）を参照。 型: 物語復元型（物語先行方式）。モチーフ「将棋」「郵便」（抽選 17 回: ネクタイ / 消しゴム / 傘・将棋 / マスク / 傘・バケツ / 畳 / 郵便 ほか）→ 連想（転校で別れた友人・年賀状・一年に一度の便り・手紙で指す将棋・床の間の盤・お年玉くじ 等 11 件）→ 物語「中学の友人と年賀状に一手ずつ書いて指した将棋が、五十五年かけて決着した」→ 隠した B = 二人が毎年の年賀状で将棋を一手ずつ指し続けていたこと。着想元の既存問題なし（台帳に該当なし。U21 と表面の「勝負の決着」が重なる点は人間ゲートで承認）。Web 照合（WebSearch 6 クエリ）で同一・近い真相の投稿問題・小話なし。', 1);

-- U26 日本語を覚えた日から
INSERT INTO umigame_stock_items (set_id, content_key, title, difficulty, problem_text, truth, fact_sheet,
    expected_questions, hook, rule_text, narration, play_example, character_lines, illustration_prompt,
    caption, source_note, is_active)
VALUES ((SELECT id FROM batch_sets WHERE set_code = 'umigame-soup-1'),
        '014-kind-interpreter', '日本語を覚えた日から', 3,
        '外国から嫁いできた女と義母は、同居してから十年間、近所で評判の仲のよさだった。ところが女が日本語を覚えて話せるようになると、二人は毎日けんかを始めた。どういうこと？',
        '女は外国で日本人の夫と結婚し、息子が五歳のとき一家で日本へ移って、夫の母と同居を始めた。女は日本語がほとんど話せず、夫は仕事で帰りが遅かったので、義母との会話は二つの言葉を話す息子が通訳した。息子は二人のけんかを見たくなくて、義母が「味が薄い」と言えば母に「やさしい味だって」と伝え、母が「口を出さないで」と言えば義母に「教えてくれてありがとうだって」と伝えた。二人は十年間、近所で評判の仲のよい嫁と姑だった。息子が高校の寮に入った春、女は辞書を片手に日本語を覚え、義母と通訳なしで話すようになった。すると初めて本当の言葉が聞こえ、二人は毎日言い合いを始めた。やがて十年分の通訳がほとんど作り話だったと気づき、二人そろって息子に電話をかけた。',
        '["義母の性格や考え方は、この十年で変わっていない。義母は前から同じようなことを言っていた","誰かが悪口を吹き込んだのではない。近所の人は何もしていない","女が日本語を覚える前も、二人は毎日たくさん会話をしていた","二人の会話には、いつも間に入って伝える家族がいた（誰がどう伝えていたかは答えの核心。正解宣言のとき以外は補足で言わない）","間に入っていたのは夫ではない。夫は仕事で帰りが遅く、平日はほとんど家にいなかった","同居は十年前、一家が女の国から日本へ移ってきたときに始まった","女が日本語を覚えたのはこの春から。辞書を使って自分で勉強した","けんかの中身は、料理の味つけや家事のやり方など、前から毎日話題にしていたこと","二人は本当は嫌い合ってはいない。今もけんかをしながら同じ家で暮らしている","二人はけんかの理由に気づき、今では笑い話にしている","女の出身の国、義母の年齢、家のある町は問題に関係ない"]',
        '[{"q":"義母の性格が変わったのですか？","a":"いいえ"},{"q":"誰かが悪口を吹き込んだのですか？","a":"いいえ"},{"q":"近所の人が何かしたのですか？","a":"いいえ"},{"q":"日本語が分かるようになって、義母の文句に気づいたのですか？","a":"はい"},{"q":"義母は前から同じようなことを言っていたのですか？","a":"はい"},{"q":"前は二人の言葉が通じていなかったのですか？","a":"はい"},{"q":"二人の間に入って伝える人がいたのですか？","a":"はい"},{"q":"間に入っていたのは家族ですか？","a":"はい"},{"q":"間に入っていたのは夫ですか？","a":"いいえ"},{"q":"伝える人は、言葉をそのまま伝えていましたか？","a":"いいえ"},{"q":"女の言葉も変えて伝えられていましたか？","a":"はい"},{"q":"女が日本語を覚えたのは最近ですか？","a":"はい"},{"q":"二人は本当は嫌い合っているのですか？","a":"いいえ"},{"q":"女の出身の国がどこかは関係ありますか？","a":"関係ない"},{"q":"義母の年齢は関係ありますか？","a":"関係ない"},{"q":"二人の会話は家族が通訳していて、お互いの文句を褒め言葉に言い換えて伝えていたので、女が日本語を覚えて本当の言葉が分かるとけんかになった。","a":"正解"}]',
        '言葉が通じたのに？', '「はい / いいえ / 関係ない」で答えられる質問をコメントしてね。出題者が全部返事します',
        '{"problem":"外国から嫁いできた女と義母は、同居してから十年間、近所で評判の仲のよさだった。ところが女が日本語を覚えて話せるようになると、二人は毎日けんかを始めた。どういうこと？","rule":"はい、いいえ、関係ない、で答えられる質問をコメントしてね。全部返事するよ。"}',
        '[{"role":"questioner","text":"義母の性格が変わった？"},{"role":"master","text":"いいえ。"},{"role":"questioner","text":"前から同じことを言ってた？"},{"role":"master","text":"はい！"},{"role":"questioner","text":"誰かが悪口を吹き込んだ？"},{"role":"master","text":"いいえ。"}]',
        '{"master":{"intro":"質問してみて！","outro":"何度でも答えるよ。コメントで質問！"},"jr":{"outro":"面白かったら、いいね、フォローよろしくね！"}}',
        'A stylized 1990s Japanese OVA anime background painting (hand-painted cel-era background art, poster-color textures, clean shapes, thick brush-like outlines on key objects). Mid-key lighting: moonlight, lamps or candlelight keep the whole scene clearly visible, NOT dark.

Scene: A Japanese home kitchen; a woman in her forties and her elderly mother-in-law stand side by side at the stove, both frowning and arguing with animated hand gestures over a pot of miso soup; an open bilingual dictionary lies on the kitchen table; warm afternoon light, no readable writing, no text.

Vertical 9:16 composition (1024x1536). No text, no letters, no numbers, no logos, no signs. Depict only the scene described in the problem statement; do not depict any clue to the story''s hidden truth. People: only the persons who appear in the problem, plus at most one distant silhouette. Keep the upper 55% of the image calm and simple (sky, wall, ceiling, window) so that text cards can be overlaid there.',
        '【探偵カメロックのウミガメのスープ】

外国から嫁いできた女と義母は、同居してから十年間、近所で評判の仲のよさだった。ところが女が日本語を覚えて話せるようになると、二人は毎日けんかを始めた。どういうこと？

「はい / いいえ / 関係ない」で答えられる質問をコメントしてね。出題者の探偵カメロックが全部返事します。正解が出るまで何度でもどうぞ。

#ウミガメのスープ #水平思考 #推理クイズ #なぞなぞ #謎解き #クイズ #AIart',
        '完全オリジナル（既存問題の転載・改変ではない）。作問法は note 記事 https://note.com/suekai0217/n/n35128e606a9b の4 ステップ（モチーフ → 連想 → 言い方を変える → 不思議にする）と良い問題の 3 条件（コアが明確・動線がある・現実離れしない）に従う。着想の型は research.md（Codex Web リサーチ台帳）を参照。 型: 物語復元型（物語先行方式）。モチーフ「辞書」（抽選 22 回: 毛糸 / お年玉 / バス停・ゴミ出し / 時計 / 辞書・バス停 / 畳 / 辞書 ほか）→ 連想（外国語・国際結婚・同居・嫁と姑・子どもが二つの言葉を話す・通訳・言葉が分かると聞こえ方が変わる 等 11 件）→ 物語「外国から嫁いだ母と義母の会話を、息子が十年間褒め言葉に作り変えて通訳していた」→ 隠した B = 息子が二人の文句を褒め言葉に変えて通訳していたこと。着想元の既存問題なし（台帳に該当なし）。Web 照合（WebSearch 8 クエリ）で同一・近い真相の投稿問題・小話なし。', 1);
