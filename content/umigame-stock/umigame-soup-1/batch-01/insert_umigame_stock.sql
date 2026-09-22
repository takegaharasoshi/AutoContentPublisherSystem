-- batch-01 ウミガメストック投入（9 問。人間レビュー + プローブテスト承認後に実行）
-- 生成元: content/umigame-stock/umigame-soup-1/batch-01/stock_items.py（単一ソース）。適用先: ローカル MySQL / Aurora（acps）
-- set_id は set_code から解決するため両環境共通で実行できる。content_key は stock_items.py で採番済み。

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
        '[{"role":"questioner","text":"影は本物の影？"},{"role":"master","text":"いいえ。"},{"role":"questioner","text":"相手は男の友だち？"},{"role":"master","text":"いいえ。"},{"role":"questioner","text":"二人は前にも会った？"},{"role":"master","text":"はい！"}]',
        '{"master":{"intro":"質問してみて！","outro":"何度でも答えるよ。コメントで質問！"},"jr":{"outro":"面白かったら、いいね、フォローよろしくね！"}}',
        'A stylized 1990s Japanese OVA anime background painting (hand-painted cel-era background art, poster-color textures, clean shapes, thick brush-like outlines on key objects). Mid-key lighting: moonlight, lamps or candlelight keep the whole scene clearly visible, NOT dark.

Scene: A middle-aged man in a plain shirt seen from behind, walking alone along a quiet residential street in late afternoon; his long shadow stretches ahead of him on the pavement; low houses, a utility pole and a hedge along the street; soft warm sunlight, no other people.

Vertical 9:16 composition (1024x1536). No text, no letters, no numbers, no logos, no signs. Depict only the scene described in the problem statement; do not depict any clue to the story''s hidden truth. People: only the persons who appear in the problem, plus at most one distant silhouette. Keep the upper 55% of the image calm and simple (sky, wall, ceiling, window) so that text cards can be overlaid there.',
        '【探偵カメロックのウミガメのスープ】
「影が薄くなった」と言われて泣いて喜び、相手に何度も頭を下げた男。相手もにこにこ笑っていました。

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
自分たちの名前をわざと鏡文字で書いている働く男たち。読みにくいのに、このおかげで仕事がやりやすくなっています。

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
階段に並んで楽器を構えているのに、一度も音を出したことがない男たち。それでも見ている人たちは毎日うれしそうです。

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
男の子が書いた手紙を受け取った男。その子に一度も会ったことがないのに、どんな子なのかを誰よりもよく知っています。

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
店の卵をとても大切にしているパン屋の主人。焼くことも割ることもしないのに、パンがおいしいのはこの卵のおかげだといつも自慢しています。

パン屋の主人は、店の卵をとても大切にしている。焼くことも、割ることもしない。それなのに主人は、うちのパンがおいしいのはこの卵のおかげだ、といつも自慢している。なぜ？

「はい / いいえ / 関係ない」で答えられる質問をコメントしてね。出題者の探偵カメロックが全部返事します。正解が出るまで何度でもどうぞ。

#ウミガメのスープ #水平思考 #推理クイズ #なぞなぞ #謎解き #クイズ #AIart',
        '完全オリジナル（既存問題の転載・改変ではない）。作問法は note 記事 https://note.com/suekai0217/n/n35128e606a9b の4 ステップ（モチーフ → 連想 → 言い方を変える → 不思議にする）と良い問題の 3 条件（コアが明確・動線がある・現実離れしない）に従う。着想の型は research.md（Codex Web リサーチ台帳）を参照。 型: 意味誤誘導型。モチーフ「たまご」（作問スキル umigame-problem-writer の抽選 3 語〔ベンチ・たまご・階段〕から。前 3 回の抽選〔自転車・すいか・花火 → 初案取り下げ / 帽子・体重計・お守り → 猫をかぶる案が差し戻し / のど飴・鍵・迷子 → 全滅で引き直し〕も記録）→ 連想「医者の卵・役者の卵 = 見習い」→ 抽象化（店の卵を大切にする → 職人の卵を育てる）→ 常識「卵は焼いて割って使う材料」の逆（焼くことも割ることもしないのに、パンがおいしいのはこの卵のおかげだと自慢する）。初稿の逆「その卵が焼いている」「十年間育てた」は誤認の読みで不可能文となり誤読が自壊するためレビューで言い換え（情報は真相・シートへ）。着想元の既存問題なし（語の多義で場面を反転する構造は台帳 #16〔ホーム = 本塁〕・#23〔撃つ = 撮影〕の型のみ借用。モチーフ・真相・問題文は新規）。捨てた案: タネはありません = 種なしスイカの売り文句〔人間ゲートで「コアが弱い」と取り下げ〕/ 猫をかぶる = かぶりもの〔コア宣言で差し戻し〕/ 白い鍵と黒い鍵 = ピアノ〔英語圏の有名なぞなぞと同構造〕/ 迷子は大人〔決めつけ反転の classic 構造〕/ ベンチを温める〔落差なし・競技用語反転は台帳明示例と同構造〕/ コロンブスの卵・金の卵〔知識クイズ〕。', 1);

-- U15 画面より先に聞こえたホームラン
INSERT INTO umigame_stock_items (set_id, content_key, title, difficulty, problem_text, truth, fact_sheet,
    expected_questions, hook, rule_text, narration, play_example, character_lines, illustration_prompt,
    caption, source_note, is_active)
VALUES ((SELECT id FROM batch_sets WHERE set_code = 'umigame-soup-1'),
        '006-cheer-before-screen', '画面より先に聞こえたホームラン', 4,
        '野球の生中継を見ていた少年の耳に、隣の家から「ホームランだ！」という歓声が聞こえてきた。それなのに画面の中では、ピッチャーがまだボールを投げてもいない。どういうこと？',
        '隣の家の人は、同じ試合をラジオで聞いていた。ラジオの放送は電波ですぐ届くが、少年がテレビの画面で見ていたのはインターネットで届くネット配信の中継で、映像を届ける仕組みの都合で球場より数十秒遅れて届く。だから隣の家の人が歓声を上げたとき、球場ではとっくにホームランが出ていて、少年の画面にはまだ届いていなかった。生中継といっても、少年が見ていたのは少しだけ過去の球場だった。数十秒後、少年の画面にも同じホームランがちゃんと映った。',
        '["隣の家の人は、少年が見ているのと同じ試合の、同じホームランのことを叫んだ","隣の家の人は予言者や占い師ではない。でたらめやまぐれで叫んだのでもない","隣の家の人は自分の家にいて、球場には行っていない","隣の家の人はテレビを見ていない。少年の画面をのぞいたのでもない","誰かが電話やメッセージで隣の家の人に結果を知らせたのではない","隣の家の人がどうやってホームランを知ったのかと、少年の画面がどういう状態だったのかは、この問題の答えの核心である（正解宣言のとき以外は補足で言わない）","少年のテレビは壊れていない。少年は録画や一時停止、巻き戻しをしていない","少年はごく普通の方法で中継を見ていて、少年に落ち度はない","このあと、少年の画面にも同じホームランがちゃんと映った","ホームランを打った選手・チーム・点数は問題に関係ない","少年と隣の家の人の関係や、隣の家の人の年齢は問題に関係ない"]',
        '[{"q":"隣の家の人は、少年と同じ試合のことを言っていますか？","a":"はい"},{"q":"隣の家の人は予言者ですか？","a":"いいえ"},{"q":"隣の家の人はでたらめに叫んだのですか？","a":"いいえ"},{"q":"隣の家の人は球場にいますか？","a":"いいえ"},{"q":"隣の家の人はテレビで試合を見ていますか？","a":"いいえ"},{"q":"誰かが電話やメッセージで隣の家の人に結果を知らせたのですか？","a":"いいえ"},{"q":"隣の家の人はラジオで試合を聞いていますか？","a":"はい"},{"q":"少年のテレビは壊れていますか？","a":"いいえ"},{"q":"少年は録画や一時停止した映像を見ていたのですか？","a":"いいえ"},{"q":"少年が見ていたのはインターネットで届く配信の中継ですか？","a":"はい"},{"q":"ラジオとネット配信では、届く速さが違いますか？","a":"はい"},{"q":"少年の見ていた中継は、球場で起きたことがすぐに映るものですか？","a":"いいえ"},{"q":"隣の家の人が叫んだとき、球場ではもうホームランが出ていましたか？","a":"はい"},{"q":"このあと、少年の画面にも同じホームランが映りましたか？","a":"はい"},{"q":"ホームランを打った選手が誰かは重要ですか？","a":"関係ない"},{"q":"少年と隣の家の人が知り合いかどうかは重要ですか？","a":"関係ない"},{"q":"試合の点数は重要ですか？","a":"関係ない"},{"q":"隣の家の人は同じ試合をラジオで聞いていた。少年のネット配信の中継は球場より数十秒遅れて届くから、球場ではもうホームランが出ていて、画面より先に歓声が聞こえた。","a":"正解"}]',
        '画面より先に聞こえた歓声', '「はい / いいえ / 関係ない」で答えられる質問をコメントしてね。出題者が全部返事します',
        '{"problem":"野球の生中継を見ていた少年の耳に、隣の家から、ホームランだ、という歓声が聞こえてきた。それなのに画面の中では、ピッチャーがまだボールを投げてもいない。どういうこと？","rule":"はい、いいえ、関係ない、で答えられる質問をコメントしてね。全部返事するよ。"}',
        '[{"role":"questioner","text":"隣の人は予言者？"},{"role":"master","text":"いいえ。"},{"role":"questioner","text":"隣の人はテレビで見てる？"},{"role":"master","text":"いいえ。"},{"role":"questioner","text":"同じ試合のこと？"},{"role":"master","text":"はい！"}]',
        '{"master":{"intro":"質問してみて！","outro":"何度でも答えるよ。コメントで質問！"},"jr":{"outro":"面白かったら、いいね、フォローよろしくね！"}}',
        'A stylized 1990s Japanese OVA anime background painting (hand-painted cel-era background art, poster-color textures, clean shapes, thick brush-like outlines on key objects). Mid-key lighting: moonlight, lamps or candlelight keep the whole scene clearly visible, NOT dark.

Scene: A boy in pajamas sitting on the living room floor at night, watching a glowing television that shows a distant green baseball stadium; he looks back over his shoulder toward a curtained window as if hearing a sound from outside; warm lamp light, cozy simple room, no other people.

Vertical 9:16 composition (1024x1536). No text, no letters, no numbers, no logos, no signs. Depict only the scene described in the problem statement; do not depict any clue to the story''s hidden truth. People: only the persons who appear in the problem, plus at most one distant silhouette. Keep the upper 55% of the image calm and simple (sky, wall, ceiling, window) so that text cards can be overlaid there.',
        '【探偵カメロックのウミガメのスープ】
野球の生中継を見ていた少年の耳に、隣の家から「ホームランだ！」と歓声が届きました。画面の中では、ピッチャーはまだ投げてもいません。

野球の生中継を見ていた少年の耳に、隣の家から「ホームランだ！」という歓声が聞こえてきた。それなのに画面の中では、ピッチャーがまだボールを投げてもいない。どういうこと？

「はい / いいえ / 関係ない」で答えられる質問をコメントしてね。出題者の探偵カメロックが全部返事します。正解が出るまで何度でもどうぞ。

#ウミガメのスープ #水平思考 #推理クイズ #なぞなぞ #謎解き #クイズ #AIart',
        '完全オリジナル（既存問題の転載・改変ではない）。作問法は note 記事 https://note.com/suekai0217/n/n35128e606a9b の4 ステップ（モチーフ → 連想 → 言い方を変える → 不思議にする）と良い問題の 3 条件（コアが明確・動線がある・現実離れしない）に従う。着想の型は research.md（Codex Web リサーチ台帳）を参照。 型: 意味誤誘導型。モチーフ「ラジオ」（作問スキル umigame-problem-writer の抽選 3 語〔ラジオ・なわとび・将棋〕から。前 3 回の抽選〔手相・はしご・カーテン → カーテンの留守宅防犯案がコア NG / 砂時計・鉛筆・落とし物 → 砂時計の故郷の砂案がコア NG / はしご・ポスト・ホームラン → コア検査を通る案なしで引き直し〕も記録）→ 連想「ネット配信は数十秒遅れる・ラジオの実況は速い」→ 具体化（隣の歓声が画面より先に届く）→ 常識「生中継は今この瞬間の姿」の逆（画面より先に歓声が聞こえる）。着想元の既存問題なし（台帳 #09〔BGM が実は位置の合図〕とは構造が異なる。ワールドカップや甲子園で「隣の歓声が先に上がる」実体験は広く知られるが、ウミガメとしての出題は台帳・記憶になし）。捨てた案: カーテン〔留守宅の防犯の開け閉め。人間ゲートでコア NG〕/ 砂時計〔故郷の砂浜の砂。人間ゲートでコア NG〕/ はしご〔はしご酒は大人の読みで子ども向けに不成立〕/ ポスト〔役職・ゴールポストの多義も大人の読み〕/ ホームラン〔ホーム = 本塁は台帳の既知構造〕/ なわとび〔回し係・縄の長さ調整は即答され難易度 1〜2 止まり〕/ 将棋〔駒を人と読ませる案は U12 とコア構造が同じ〕。', 1);

-- U16 助けに来た女も凍りついた
INSERT INTO umigame_stock_items (set_id, content_key, title, difficulty, problem_text, truth, fact_sheet,
    expected_questions, hook, rule_text, narration, play_example, character_lines, illustration_prompt,
    caption, source_note, is_active)
VALUES ((SELECT id FROM batch_sets WHERE set_code = 'umigame-soup-1'),
        '007-frozen-tag', '助けに来た女も凍りついた', 4,
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
凍りついたまま助けを待っていた男。ようやく助けに来た女も、男のそばで同じように凍りついてしまいました。

男は凍りついたまま、誰かが助けに来るのをじっと待っていた。ようやく助けに来た女は、男のそばまで来たところで、同じようにその場で凍りついてしまった。どういうこと？

「はい / いいえ / 関係ない」で答えられる質問をコメントしてね。出題者の探偵カメロックが全部返事します。正解が出るまで何度でもどうぞ。

#ウミガメのスープ #水平思考 #推理クイズ #なぞなぞ #謎解き #クイズ #AIart',
        '完全オリジナル（既存問題の転載・改変ではない）。作問法は note 記事 https://note.com/suekai0217/n/n35128e606a9b の4 ステップ（モチーフ → 連想 → 言い方を変える → 不思議にする）と良い問題の 3 条件（コアが明確・動線がある・現実離れしない）に従う。着想の型は research.md（Codex Web リサーチ台帳）を参照。 型: 意味誤誘導型。モチーフ「氷」（作問スキル umigame-problem-writer の抽選 3 語〔氷・花火・くしゃみ〕から選択。花火は「音が光より遅れる」が U15 と同じ遅延構造・「朝の号砲」は地域慣習・煙や型物花火は語の仕掛けなし、くしゃみは語の仕掛けが同音〔こしょう・ほこり〕か大人の迷信で不成立）→ 連想「凍りつく（慣用句）・氷鬼」→ 具体化（凍りついたまま助けを待つ = 氷鬼で鬼にタッチされて仲間を待つ）→ 常識「助けに来た者は凍りつかない」の逆（助けに来た女も凍りつく）。着想元の既存問題なし（台帳に遊びのルールをコアにした行はない。U12〔人形を人と読ませる〕とは慣用句の誤読という点で構造が異なる）。捨てた案: 滑る〔試験に滑る → 氷で滑る。第一義が氷で誤読が強制されない〕/ 真夏に毛布をかけて氷を運ぶ〔常識の逆だけで語の仕掛けなし〕/ 氷を入れても薄くならないジュース〔氷 = 凍らせたジュース。落差が小さい〕/ だるまさんがころんだ〔言葉で全員が凍りつく案は「はいチーズ」でも成立し正解が一つに定まらない〕。2026-09-20 の人間ゲート 1 巡目で「少年・少女は氷鬼を連想させる」の指摘を受け、登場人物を大人の夫婦（鬼は子ども）に差し替えた（登場人物の属性は正体のカテゴリを指す A 型手がかり。スキル 4.5 に反映）。', 1);

-- U17 誰も入っていないのに焦げた畳
INSERT INTO umigame_stock_items (set_id, content_key, title, difficulty, problem_text, truth, fact_sheet,
    expected_questions, hook, rule_text, narration, play_example, character_lines, illustration_prompt,
    caption, source_note, is_active)
VALUES ((SELECT id FROM batch_sets WHERE set_code = 'umigame-soup-1'),
        '008-scorched-tatami', '誰も入っていないのに焦げた畳', 4,
        'よく晴れた日、女は家に鍵をかけて朝から夕方まで出かけた。帰ってきても鍵はかかったままだったのに、火の気のない和室の畳に小さな焦げ跡ができていた。どういうこと？',
        '女は和室の窓辺に、水を入れた丸いガラスの金魚鉢を置いていた。季節は冬で、低い太陽の光が窓から部屋の奥まで差し込む。よく晴れたその日、水の入った丸いガラス鉢が虫めがねのように日光を一点に集め、光が当たり続けた畳の表面をじわじわと焦がした。留守の間に人は誰も入っていないし、火も電気も使っていない。焦げ跡は畳のごく一部で火事にはならず、金魚も無事だった。女は驚いて、金魚鉢を窓辺から離れた棚に移した。',
        '["留守の間、家の中に人は誰も入っていない（女の家族も含む）","焦げ跡ができたとき、家の中で火も電気製品も使われていない（コンセントにつないだ物はない）","焦げ跡は畳のごく一部で、火事にはならず、けがをした人も生き物もいない","焦げ跡は和室の窓に近い場所にできた","その日は朝から夕方までよく晴れていて、季節は冬で、日の光が窓から部屋の奥まで差し込んでいた","もしその日が曇りや雨だったら、焦げ跡はできなかった","窓辺には、女が前から置いていた物がひとつあり、それは火も電気も使わない","窓辺の物は虫めがねやレンズではないが、光を通す","窓辺の物を別の場所へ移せば、同じことは二度と起きない","焦げ跡が何によってできたのかは、この問題の答えの核心である（正解宣言のとき以外は補足で言わない）","女の職業・家の場所・鍵の種類は問題に関係ない"]',
        '[{"q":"留守の間に誰かが家に入りましたか？","a":"いいえ"},{"q":"女の家族が火を使いましたか？","a":"いいえ"},{"q":"電気製品が熱くなって焦げたのですか？","a":"いいえ"},{"q":"女が出かける前に何かを燃やしましたか？","a":"いいえ"},{"q":"タバコや線香が原因ですか？","a":"いいえ"},{"q":"誰かのいたずらですか？","a":"いいえ"},{"q":"生き物のしわざですか？","a":"いいえ"},{"q":"天気は関係ありますか？","a":"はい"},{"q":"曇りの日だったら焦げ跡はできませんでしたか？","a":"はい"},{"q":"焦げ跡は窓の近くにできましたか？","a":"はい"},{"q":"日の光が焦げ跡の原因に関係していますか？","a":"はい"},{"q":"窓辺に何か置いてありましたか？","a":"はい"},{"q":"窓辺の物は虫めがねですか？","a":"いいえ"},{"q":"窓辺の物は光を通しますか？","a":"はい"},{"q":"窓辺の物の中に水が入っていますか？","a":"はい"},{"q":"窓辺の物を動かせば、同じことは起きませんか？","a":"はい"},{"q":"鍵の種類は関係ありますか？","a":"関係ない"},{"q":"女の職業は関係ありますか？","a":"関係ない"},{"q":"窓辺に置いてあった水の入ったガラスの鉢がレンズのように日光を集めて、畳を焦がした。","a":"正解"}]',
        '誰もいない和室に焦げ跡', '「はい / いいえ / 関係ない」で答えられる質問をコメントしてね。出題者が全部返事します',
        '{"problem":"よく晴れた日、女は家に鍵をかけて朝から夕方まで出かけた。帰ってきても鍵はかかったままだったのに、火の気のない和室の畳に小さな焦げ跡ができていた。どういうこと？","rule":"はい、いいえ、関係ない、で答えられる質問をコメントしてね。全部返事するよ。"}',
        '[{"role":"questioner","text":"留守中に誰か入った？"},{"role":"master","text":"いいえ。"},{"role":"questioner","text":"電気製品が熱くなった？"},{"role":"master","text":"いいえ。"},{"role":"questioner","text":"天気は関係ある？"},{"role":"master","text":"はい！"}]',
        '{"master":{"intro":"質問してみて！","outro":"何度でも答えるよ。コメントで質問！"},"jr":{"outro":"面白かったら、いいね、フォローよろしくね！"}}',
        'A stylized 1990s Japanese OVA anime background painting (hand-painted cel-era background art, poster-color textures, clean shapes, thick brush-like outlines on key objects). Mid-key lighting: moonlight, lamps or candlelight keep the whole scene clearly visible, NOT dark.

Scene: A quiet Japanese tatami room filled with bright winter sunlight from a window, a small dark scorch mark on the tatami near the window, a woman in a coat standing in the doorway holding house keys and looking at the mark in surprise; no fire, no smoke, no other people, nothing placed on the windowsill.

Vertical 9:16 composition (1024x1536). No text, no letters, no numbers, no logos, no signs. Depict only the scene described in the problem statement; do not depict any clue to the story''s hidden truth. People: only the persons who appear in the problem, plus at most one distant silhouette. Keep the upper 55% of the image calm and simple (sky, wall, ceiling, window) so that text cards can be overlaid there.',
        '【探偵カメロックのウミガメのスープ】
鍵をかけて出かけた女。帰ってきても鍵はかかったままなのに、火の気のない和室の畳には小さな焦げ跡ができていました。

よく晴れた日、女は家に鍵をかけて朝から夕方まで出かけた。帰ってきても鍵はかかったままだったのに、火の気のない和室の畳に小さな焦げ跡ができていた。どういうこと？

「はい / いいえ / 関係ない」で答えられる質問をコメントしてね。出題者の探偵カメロックが全部返事します。正解が出るまで何度でもどうぞ。

#ウミガメのスープ #水平思考 #推理クイズ #なぞなぞ #謎解き #クイズ #AIart',
        '完全オリジナル（既存問題の転載・改変ではない）。作問法は note 記事 https://note.com/suekai0217/n/n35128e606a9b の4 ステップ（モチーフ → 連想 → 言い方を変える → 不思議にする）と良い問題の 3 条件（コアが明確・動線がある・現実離れしない）に従う。着想の型は research.md（Codex Web リサーチ台帳）を参照。 型: 物語復元型。モチーフ「畳」（作問スキル umigame-problem-writer の抽選 3 語〔お守り・たまご・畳〕から選択。たまごは U14 とモチーフが重複、お守りは連想が返納・願掛けの動機に寄り B が出来事にならない）→ 連想「和室に日が差す・窓辺の金魚鉢・留守にする」→ 物語 A→B→C（A = 晴れた日に鍵をかけて一日留守 / B = 窓辺の水入りガラス鉢が日光を集めて畳を焦がす / C = 誰も入っていない和室の畳に焦げ跡）→ B を隠し、読者に「誰かが入って火を使った・電気の過熱」と補わせる。着想元の既存問題なし（台帳の story 15 件に「日光と水の収れん」の構造はなく、#02〔溶けた雪だるまの痕跡から直前の姿を復元〕とも異なる）。工程 7 の Web 検索で、同じ仕組み〔水入り容器の収れん〕を真相の背景に使うラテシンの投稿問題「火事だ！水を捨てよう」〔コアは「なぜ水を捨てたか」〕が 1 件見つかったが、着想元ではなく問題文・場面・コアとも重ならない（採否は人間ゲートで判断。詳細は開発記録 21-4a-3 U17）。捨てた案: 畳の日焼け跡で前の住人の家具の位置を当てる〔#02 と痕跡復元の構造が近く、誰もが知る現象で難易度 2〕。', 1);

-- U18 濡れた手紙を乾かしたら白紙になった
INSERT INTO umigame_stock_items (set_id, content_key, title, difficulty, problem_text, truth, fact_sheet,
    expected_questions, hook, rule_text, narration, play_example, character_lines, illustration_prompt,
    caption, source_note, is_active)
VALUES ((SELECT id FROM batch_sets WHERE set_code = 'umigame-soup-1'),
        '009-blank-letter', '濡れた手紙を乾かしたら白紙になった', 4,
        '女は男への手紙を書き終えたが、封をする前に机のお茶をこぼして手紙を濡らしてしまった。急いで乾かすと、紙はきれいに乾いたのに、字は一文字も残っていなかった。どういうこと？',
        '女が手紙を書いたのは、ペンの後ろのゴムでこすると字が消える「消せるボールペン」だった。このインクはこすったときの摩擦の熱で透明になる仕組みで、ドライヤーの熱風でも同じように消える。女は冷めたお茶をこぼしたあと、濡れた手紙をドライヤーで急いで乾かした。字はお茶で流れたのではなく、乾かすときの熱で一文字残らず透明になったのだった。紙もインクもそのまま残っている。女があとで調べると、このインクは冷やすと色が戻ると分かり、手紙を冷凍庫に入れておくと字はすっかり元どおりになった。',
        '["手紙は女が市販のボールペンで白い紙に書いた（鉛筆・筆・万年筆ではない）","こぼしたお茶は冷めていて、こぼした直後の濡れた手紙でも字ははっきり読めた","濡れた紙に、字がにじんだり流れたりした跡は残っていない","字が消えたのは、女が手紙を乾かしている間である","女は手紙を、髪を乾かすときに使う道具で乾かした（日なた・アイロン・火は使っていない）","乾かし方は、字が消えたことに直接関係している","手紙の紙は最初から最後まで同じ 1 枚で、すり替えられていない","女以外の人は誰も手紙に触れておらず、女がわざと字を消したのでもない","消えた字は、あとで女が元に戻すことができた","手紙を書いたペンの種類と、字が消えた仕組みは、この問題の答えの核心である（正解宣言のとき以外は補足で言わない）","手紙の内容・相手の男・お茶の種類は問題に関係ない"]',
        '[{"q":"お茶で字が流れて消えたのですか？","a":"いいえ"},{"q":"濡れたことが、字が消えた原因ですか？","a":"いいえ"},{"q":"誰かが手紙をすり替えましたか？","a":"いいえ"},{"q":"女以外の誰かが字を消しましたか？","a":"いいえ"},{"q":"女がわざと字を消したのですか？","a":"いいえ"},{"q":"濡れた直後は字が読めましたか？","a":"はい"},{"q":"字はにじんでいましたか？","a":"いいえ"},{"q":"手紙は鉛筆で書かれていましたか？","a":"いいえ"},{"q":"ボールペンで書きましたか？","a":"はい"},{"q":"乾かし方は、字が消えたことに関係ありますか？","a":"はい"},{"q":"日なたに置いて乾かしましたか？","a":"いいえ"},{"q":"ドライヤーで乾かしましたか？","a":"はい"},{"q":"熱が関係していますか？","a":"はい"},{"q":"そのペンは、書いた字を消すことができますか？","a":"はい"},{"q":"消えた字は、あとで元に戻りましたか？","a":"はい"},{"q":"お茶の種類は関係ありますか？","a":"関係ない"},{"q":"手紙の内容は関係ありますか？","a":"関係ない"},{"q":"相手の男は関係ありますか？","a":"関係ない"},{"q":"手紙は消せるボールペンで書かれていて、ドライヤーの熱でインクが透明になって字が消えた。","a":"正解"}]',
        '乾かしたら白紙になった手紙', '「はい / いいえ / 関係ない」で答えられる質問をコメントしてね。出題者が全部返事します',
        '{"problem":"女は男への手紙を書き終えたが、封をする前に机のお茶をこぼして手紙を濡らしてしまった。急いで乾かすと、紙はきれいに乾いたのに、字は一文字も残っていなかった。どういうこと？","rule":"はい、いいえ、関係ない、で答えられる質問をコメントしてね。全部返事するよ。"}',
        '[{"role":"questioner","text":"お茶で字が流れた？"},{"role":"master","text":"いいえ。"},{"role":"questioner","text":"誰かが字を消した？"},{"role":"master","text":"いいえ。"},{"role":"questioner","text":"乾かし方が関係ある？"},{"role":"master","text":"はい！"}]',
        '{"master":{"intro":"質問してみて！","outro":"何度でも答えるよ。コメントで質問！"},"jr":{"outro":"面白かったら、いいね、フォローよろしくね！"}}',
        'A stylized 1990s Japanese OVA anime background painting (hand-painted cel-era background art, poster-color textures, clean shapes, thick brush-like outlines on key objects). Mid-key lighting: moonlight, lamps or candlelight keep the whole scene clearly visible, NOT dark.

Scene: A woman sitting at a wooden desk in a bright room, holding up a sheet of letter paper that is completely blank except for a faint dried tea stain, an overturned teacup beside her, her eyes wide in surprise; an envelope on the desk; no hair dryer, no pen visible, no other people.

Vertical 9:16 composition (1024x1536). No text, no letters, no numbers, no logos, no signs. Depict only the scene described in the problem statement; do not depict any clue to the story''s hidden truth. People: only the persons who appear in the problem, plus at most one distant silhouette. Keep the upper 55% of the image calm and simple (sky, wall, ceiling, window) so that text cards can be overlaid there.',
        '【探偵カメロックのウミガメのスープ】
手紙を書き終えた女。お茶をこぼして濡らした手紙を急いで乾かすと、紙はきれいに乾いたのに、字は一文字も残っていませんでした。

女は男への手紙を書き終えたが、封をする前に机のお茶をこぼして手紙を濡らしてしまった。急いで乾かすと、紙はきれいに乾いたのに、字は一文字も残っていなかった。どういうこと？

「はい / いいえ / 関係ない」で答えられる質問をコメントしてね。出題者の探偵カメロックが全部返事します。正解が出るまで何度でもどうぞ。

#ウミガメのスープ #水平思考 #推理クイズ #なぞなぞ #謎解き #クイズ #AIart',
        '完全オリジナル（既存問題の転載・改変ではない）。作問法は note 記事 https://note.com/suekai0217/n/n35128e606a9b の4 ステップ（モチーフ → 連想 → 言い方を変える → 不思議にする）と良い問題の 3 条件（コアが明確・動線がある・現実離れしない）に従う。着想の型は research.md（Codex Web リサーチ台帳）を参照。 型: 物語復元型。モチーフ「消しゴム」（作問スキル umigame-problem-writer の抽選。1 回目〔ポスト・ヘルメット・眼鏡〕はB が制度説明・動機・知識クイズに寄り引き直し、2 回目「マラソン」〔同じ号砲なのに記録が逆転〕は人間ゲートで「一般読者にイメージが湧かない」と NG、3 回目〔時計・包丁・そろばん〕は既出・語感・出来事の薄さで引き直し、4 回目「自転車」〔同じ型の自転車に鍵が合って乗って帰った〕は人間ゲートで「ひねりが足りない」と NG、5 回目〔消しゴム・花束・おにぎり〕から選択）→ 連想「消しゴムを使わずに消える字 → 消せるボールペン → 熱で消える・濡れた紙をドライヤーで乾かす」→ 物語 A→B→C（A = 手紙を書き終えて冷めたお茶をこぼす / B = ドライヤーの熱で消せるボールペンのインクが透明になる / C = 乾いた手紙に字が一文字も残っていない）→ B を隠し、読者に「濡れてインクが流れた」と補わせる。因果の反転（濡れたからではなく乾かしたから消えた）がコア。着想元の既存問題なし（台帳の story 15 件に「熱で字が消える」構造はなく、あぶり出し〔熱で字が浮かぶ〕とは逆向き）。工程 7 の Web 照合の結果は開発記録 21-4a-3 U18 に記載。捨てた案: 夏の車内に置いた手紙が白紙になる〔留守中に熱で変化する形で U17 と骨格が同じ〕。', 1);
