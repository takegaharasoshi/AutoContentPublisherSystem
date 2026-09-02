/**
 * スロット別パレット。現行レンダラー（gpt_quiz_multicut.SLOT_PALETTES）と同値。
 * 色は R-1 の対象外（変えるのはレンダラー・動き・上部の余白だけ）。
 */

export type SlotCode = "morning" | "noon" | "night";

export type Palette = {
  background: string;
  card: string;
  text: string;
  mutedText: string;
  accent: string;
  decoration: string;
};

export const SLOT_PALETTES: Record<SlotCode, Palette> = {
  morning: {
    background: "#F3EEE3",
    card: "#FBF8F1",
    text: "#1B2A4A",
    mutedText: "#56688A",
    accent: "#F4B942",
    decoration: "#E4DCC9",
  },
  noon: {
    background: "#E9F1F8",
    card: "#FBFDFF",
    text: "#1B2A4A",
    mutedText: "#56688A",
    accent: "#E39B0C",
    decoration: "#D3E2EF",
  },
  night: {
    background: "#0A1226",
    card: "#111E3C",
    text: "#F7F7F2",
    mutedText: "#9FB0CC",
    accent: "#F4B942",
    decoration: "#1B2C50",
  },
};
