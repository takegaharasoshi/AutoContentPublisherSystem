-- 2026-10-w1 A59(候補 m08)の完成稿 NG による差し替え A61(候補 m20)の 1 問だけを投入(他の 13 問は 2026-10-05 に投入済み)
-- 生成元: content/quiz-stock/logic-training-1/2026-10-w1/stock_items.py(単一ソース)。適用先: ローカル MySQL / Aurora(acps)
-- set_id は set_code から解決するため両環境共通で実行できる。
-- content_key はスロット内の既存最大連番 + 1 を適用時に解決する(V007。両環境で同一値になる)。

-- A61
INSERT INTO quiz_stock_items (set_id, content_key, quiz_type, difficulty, question_text, answer_text, content_fields, source_note, is_active)
VALUES ((SELECT id FROM batch_sets WHERE set_code = 'logic-training-1'),
        (SELECT CONCAT('morning-', LPAD(COALESCE(MAX(CAST(SUBSTRING_INDEX(t.content_key, '-', -1) AS UNSIGNED)), 0) + 1, 3, '0')) FROM (SELECT q.content_key FROM quiz_stock_items q JOIN batch_sets b ON b.id = q.set_id WHERE b.set_code = 'logic-training-1' AND q.content_key LIKE 'morning-%') t),
        'L1', 'light',
        'アルファベットが2組に分かれている。上の組と下の組には、それぞれ共通点がある。では、Rはどっちの組に入る?',
        '下の組(上は直線だけ、下は曲線のある文字)',
        '{"hook":"英語が苦手でも解けるぞ","hint":"ペンの動きを思い出せ!","question":"アルファベットが2組に分かれている。上の組と下の組には、それぞれ共通点がある。では、Rはどっちの組に入る?","answer":"下の組(上は直線だけ、下は曲線のある文字)","explanation":"上の組は直線だけで書ける文字、下の組は曲線がまじる文字。Rは右上が丸くふくらんでいるので下の組。ABC順や母音を探すと迷子になる。","coach_comment":"形で分けたら一目瞭然だ!","tags":["なぞなぞ","朝の一問","法則発見"],"summary":"上の組A E F H I K L・下の組B C D J O P Qの分け方からRの組を当てる法則発見。上は直線だけ、下は曲線を含む文字で、Rは下。ABC順を探すと詰まる。文字は積み木の絵で提示。","illustration_scene":"朝日の差す子ども部屋の床に、アルファベットの積み木が上下2列に並ぶ。上の列は「A E F H I K L」、下の列は「B C D J O P Q」。2列から少し離れて「R」の積み木が1つ置かれ、その上に大きな「?」。積み木の文字は太く単純な書体にする。他の文字・数字・人物は描かない。"}',
        '類型: アルファベットを直線だけの文字と曲線を含む文字に分ける定番(AEFHIKLMNTVWXYZ / BCDGJOPQRSU。作者不詳・英語圏に流布)。流布例: https://www.braingle.com/brainteasers/112/aefhiklmntvwxyz.html , https://puzzleaday.wordpress.com/2025/04/03/three-alphabet-puzzles/ 。文字は問題文に書かず積み木の絵で提示。文面はオリジナルに書き下ろし(表現は書き直し済み)。', 1);
