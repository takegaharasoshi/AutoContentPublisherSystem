-- pref-ranking-1 セット登録 (1/3): prompt_configs + caption_templates
-- 手順の正は docs/app/operation.html セクション 2.1 手順 2、内容の正は
-- docs/app/sets/pref-ranking-1.html セクション 4（parameters）・セクション 5（キャプション）。
-- set_id は環境ごとに異なるため set_code から解決する（ローカル 140 / Aurora 3）。
-- 適用（ローカル）: docker exec -i acps-mysql mysql --default-character-set=utf8mb4 -uroot -proot acps < 01_prompt_caption.sql
-- 適用（Aurora）:   python3 ../common/apply_aurora.py set-registration/01_prompt_caption.sql

-- (1) prompt_configs
--     ストック方式のため prompt_text は未使用（空文言で登録）。実行時に使われるのは parameters のみ。
--     単一スロット evening（20:00 JST 投稿）・duration_seconds=30（2026-08-24 尺確定）。
INSERT INTO prompt_configs (set_id, prompt_text, negative_prompt, parameters, is_active)
SELECT b.id, '', NULL,
       '{"slots": [{"from_jst_hour": 17, "slot_code": "evening", "duration_seconds": 30}]}',
       1
FROM batch_sets b
WHERE b.set_code = 'pref-ranking-1';

-- (2) caption_templates
--     ランキング系プレースホルダ 5 種（hook / title / result_list / trivia / source_display）を
--     SNS 投稿バッチが ranking_items から展開する（services/sns-post-batch/app/captions.py）。
--     常設要素 3 点: VOICEVOX クレジット・出典注記・AI 開示ハッシュタグ #AIart。
INSERT INTO caption_templates (set_id, template_text, is_active)
SELECT b.id,
       '{{hook}}
結果はこの下👇（ネタバレ注意）
・
・
・
・
・
【{{title}} TOP5】
{{result_list}}

{{trivia}}

※出典:{{source_display}}

VOICEVOX:白上虎太郎
#都道府県ランキング #47都道府県 #雑学 #地理 #トリビア #AIart',
       1
FROM batch_sets b
WHERE b.set_code = 'pref-ranking-1';
