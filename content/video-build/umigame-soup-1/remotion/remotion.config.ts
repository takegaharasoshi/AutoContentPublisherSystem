/**
 * Remotion CLI 設定（Node.js API からは参照されない）。
 * 既存 2 セット（quiz-prebuilt / ranking-prebuilt）と同じ JPEG フレーム + CRF 20。
 * create-video の雛形にあった Tailwind は本セットでは使わないため外している。
 */
import { Config } from "@remotion/cli/config";

Config.setRspack(true);
Config.setVideoImageFormat("jpeg");
Config.setOverwriteOutput(true);
Config.setCrf(20);
