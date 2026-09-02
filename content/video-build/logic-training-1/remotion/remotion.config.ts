import { Config } from "@remotion/cli/config";

Config.setVideoImageFormat("jpeg");
Config.setOverwriteOutput(true);
// 現行レンダラー（gpt_quiz_multicut.OUTPUT_CRF）と同じ画質設定にそろえる
Config.setCrf(20);
