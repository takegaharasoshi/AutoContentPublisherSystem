-- umigame-soup-1 セット登録 (1/4): prompt_configs + caption_templates
-- 手順の正は docs/app/operation.html セクション 2.1 手順 2、内容の正は
-- docs/app/sets/umigame-soup-1.html セクション 6（キャプション）・10.7.2（スナップショット）と
-- docs/app/generators/umigame-prebuilt.html セクション 3（parameters）。
-- set_id は環境ごとに異なるため set_code から解決する。再適用しても重複しないよう NOT EXISTS で守る。
-- 適用（ローカル）: docker exec -i acps-mysql mysql --default-character-set=utf8mb4 -uroot -proot acps < set-registration/01_prompt_caption.sql
-- 適用（Aurora）:   python3 ../../ranking-stock/pref-ranking-1/common/apply_aurora.py set-registration/01_prompt_caption.sql

-- (1) prompt_configs
--     parameters は duration_seconds の 1 キーだけ（24 のみ許容。slots を持たない単一スロット）。
--     prompt_text は生成には使わず、SNS 投稿バッチが問題スナップショットの master_rules に写すだけ。
--     判定・返信のプロンプトは comment-reply Lambda に同梱しているため、ここには転記せず
--     その旨の記録文を入れる（空だとスナップショット出力が異常扱いになる。21-7 で決定）。
INSERT INTO prompt_configs (set_id, prompt_text, negative_prompt, parameters, is_active)
SELECT b.id,
       '判定・返信のプロンプトは comment-reply Lambda に同梱（services/comment-reply/app/）。この列は記録用で判定には使わない。',
       NULL,
       '{"duration_seconds": 24}',
       1
FROM batch_sets b
WHERE b.set_code = 'umigame-soup-1'
  AND NOT EXISTS (SELECT 1 FROM prompt_configs p WHERE p.set_id = b.id AND p.is_active = 1);

-- (2) caption_templates
--     本文・ハッシュタグ（#AIart 含む）はストックの caption に問題ごとに持つ。
--     {{prev_truth_block}} は前回の問題の真相ブロック（21-6h。先頭の改行はブロック側が持つため間に改行を入れない）。
INSERT INTO caption_templates (set_id, template_text, is_active)
SELECT b.id, '{{caption}}{{prev_truth_block}}', 1
FROM batch_sets b
WHERE b.set_code = 'umigame-soup-1'
  AND NOT EXISTS (SELECT 1 FROM caption_templates c WHERE c.set_id = b.id AND c.is_active = 1);
