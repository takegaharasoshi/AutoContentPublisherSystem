import { QuizProps } from "./design";

/**
 * Remotion Studio 用のダミー props。実ビルドでは
 * `scripts/build_props.py` が生成した JSON を `--props` で渡す。
 */
export const MOCK_PROPS: QuizProps = {
  slotCode: "morning",
  slotLabel: "朝の脳みそトレ",
  slotHook: "30秒で解けたら天才",
  question:
    "サイとラクダとカメの3匹が、そろって家電量販店にやって来た。さて、何を買いに来た?",
  hint: "並び順の入れ替えがカギだ!",
  illustrationSrc: "illustrations/sample.png",
  illustrationWidth: 1024,
  illustrationHeight: 1024,
};
