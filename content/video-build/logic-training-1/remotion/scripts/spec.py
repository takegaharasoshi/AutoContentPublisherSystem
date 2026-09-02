"""R-1 の不変条件。

ここは ``remotion/src/timeline.ts`` と一致していなければならない
（``tests/test_timeline_sync.py`` が突き合わせる）。
"""

FPS = 30
DURATION_SECONDS = 16
TOTAL_FRAMES = FPS * DURATION_SECONDS
TICK_SECONDS = 8.0
CHIME_SECONDS = 13.0
BGM_VOLUME = 1.0
TICK_GAIN_DB = -6.0
CHIME_GAIN_DB = -3.0
BGM_FADE_OUT_START = 15
BGM_FADE_OUT_DURATION = 1
COMPOSITION_ID = "Quiz16s"
STILL_FRAMES = {
    "seam_head": 0,
    "cut1": 60,
    "cut2": 300,
    "cut3": 420,
    "seam_tail": 479,
}
STILL_LABELS = {
    "seam_head": "先頭 (0f)",
    "cut1": "導入 (2.0s)",
    "cut2": "カウントダウン (10.0s)",
    "cut3": "誘導 (14.0s)",
    "seam_tail": "末尾 (479f)",
}
