// コンポジションが決めるのは**ナレーションと BGM の相対バランスだけ**で、配信レベル
// （絶対的なラウドネス）はレンダリング後の ffmpeg loudnorm が揃える
// （scripts/normalize_loudness.py。方式設計書 ranking-prebuilt.html セクション 8.3 の decision 17-4d）。

/** ナレーション（VOICEVOX 出力）の再生ゲイン。基準なので 1 のまま動かさない */
export const NARRATION_GAIN = 1;
/**
 * BGM の定常ゲイン。17-4d の実測校正値。
 * ナレーションのみの 20 秒版が -23.9 LUFS、BGM 音源（audio_assets の既存曲で計測）が
 * -13.8 LUFS。BGM がナレーションの 18 LU 下に座るゲインを机上で出したうえで、
 * 実際にミックスした動画のナレーション無音区間を計測して詰めた値
 * （無音区間の BGM ≒ -42 LUFS = ナレーションの 18 LU 下）。ダッキングはしない
 * （ナレーションがほぼ全編を占め、常時作動して定常減衰と変わらないため）。
 */
export const BGM_GAIN = 0.056;
export const BGM_FADE_IN_FRAMES = 15;
export const BGM_FADE_OUT_FRAMES = 45;

/** 全編定常 + 頭のフェードイン + 尻のフェードアウト。ダッキングはしない */
export const bgmVolumeAt = (frame: number, total: number): number => {
  if (total <= 0) return 0;
  const fadeIn = frame / BGM_FADE_IN_FRAMES;
  const fadeOut = (total - frame) / BGM_FADE_OUT_FRAMES;
  return Math.max(0, Math.min(BGM_GAIN, BGM_GAIN * fadeIn, BGM_GAIN * fadeOut));
};
