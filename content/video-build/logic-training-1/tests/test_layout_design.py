"""R-2 の版面導出値の固定テスト（最短・中央・最長の 3 問）。

版面の導出は remotion/src/design.ts にしか無いため、esbuild で
remotion/src/deriveDesignCli.ts を束ねて node で実行し、出力値を突き合わせる。
node_modules が無い環境ではスキップする（ビルド環境の前提は README 参照）。
"""

from __future__ import annotations

import json
from pathlib import Path
import shutil
import subprocess

import pytest


BASE = Path(__file__).resolve().parent.parent
REMOTION = BASE / "remotion"
ESBUILD = REMOTION / "node_modules" / ".bin" / "esbuild"
ENTRY = REMOTION / "src" / "deriveDesignCli.ts"

# 稼働在庫の最短（id=87）・中央（id=169）・最長（id=197）。
# R-2 の採用値は「問題の長さでサイズが変わることを許容する」ため、
# 3 点を固定して配分の入れ替えを検知する。
SHORTEST = "「世界」の真ん中にいる虫は、なんだ?"
MEDIAN = "「りんご」「みかん」「両方」の3箱。ラベルは全部まちがい。1箱から1個だけ見て、全部言い当てるには?"
LONGEST = (
    "金貨の袋が10個。本物は1枚10gだが、1つの袋だけ全部偽物で1枚11gある。"
    "見た目は同じ。重さが数字で出るはかりを1回だけ使い、偽物の袋を当てるには?"
)


def _props(question: str, *, slot: str = "night") -> dict[str, object]:
    return {
        "slotCode": slot,
        "slotLabel": "朝の脳みそトレ" if slot == "morning" else "夜の脳みそトレ",
        "slotHook": "30秒で解けたら天才" if slot == "morning" else "1％の人だけが30秒で解ける",
        "question": question,
        "hint": "よく見ると、答えはもう出ているぞ。",
        "illustrationSrc": "illustrations/87.png",
        "illustrationWidth": 1536,
        "illustrationHeight": 1024,
    }


@pytest.fixture(scope="module")
def bundle(tmp_path_factory: pytest.TempPathFactory) -> Path:
    if not ESBUILD.is_file() or shutil.which("node") is None:
        pytest.skip("remotion/node_modules または node が無いためスキップ")
    out = tmp_path_factory.mktemp("design") / "deriveDesignCli.mjs"
    subprocess.run(
        [
            str(ESBUILD),
            str(ENTRY),
            "--bundle",
            "--platform=node",
            "--format=esm",
            f"--outfile={out}",
            "--log-level=warning",
        ],
        check=True,
        cwd=REMOTION,
    )
    return out


def _derive(bundle: Path, props_list: list[dict[str, object]]) -> list[dict]:
    result = subprocess.run(
        ["node", str(bundle)],
        input=json.dumps(props_list),
        capture_output=True,
        text=True,
        check=True,
    )
    return json.loads(result.stdout)


def test_three_items_match_poc_measurements(bundle: Path) -> None:
    """PoC 実測（2026-09-19 のユーザー決定）と一致すること。"""
    shortest, median, longest = _derive(
        bundle,
        [
            _props(SHORTEST, slot="morning"),
            _props(MEDIAN),
            _props(LONGEST),
        ],
    )

    assert (shortest["question"]["fontSize"], shortest["question"]["lineCount"]) == (68, 2)
    assert (shortest["illustration"]["width"], shortest["illustration"]["height"]) == (797, 531)

    assert (median["question"]["fontSize"], median["question"]["lineCount"]) == (54, 3)
    assert (median["illustration"]["width"], median["illustration"]["height"]) == (797, 531)

    assert (longest["question"]["fontSize"], longest["question"]["lineCount"]) == (50, 4)
    assert (longest["illustration"]["width"], longest["illustration"]["height"]) == (771, 514)


def test_illustration_box_keeps_guaranteed_height(bundle: Path) -> None:
    """どの長さでもイラストの箱は保証高（500px）を下回らないこと。"""
    derived = _derive(
        bundle,
        [_props(SHORTEST, slot="morning"), _props(MEDIAN), _props(LONGEST)],
    )
    for item in derived:
        box = item["illustrationBox"]
        assert box["bottom"] - box["top"] >= 500


def test_illustration_is_aligned_to_top_of_box(bundle: Path) -> None:
    """余りが出る問題でも、イラストは箱の上端（問題文の直下）に寄ること。"""
    (shortest,) = _derive(bundle, [_props(SHORTEST, slot="morning")])
    assert shortest["illustration"]["top"] == shortest["illustrationBox"]["top"]
    assert (
        shortest["illustrationBox"]["bottom"] - shortest["illustrationBox"]["top"]
        > shortest["illustration"]["height"]
    ), "このケースは箱に余りが出る前提（余りが無いと上端寄せを検知できない）"


def test_hook_band_fits_in_one_line_at_adopted_size(bundle: Path) -> None:
    """つかみ帯は採用値 52px で 1 行に収まること。"""
    morning, night = _derive(bundle, [_props(SHORTEST, slot="morning"), _props(MEDIAN)])
    assert morning["hook"] == {"fontSize": 52, "lineCount": 1}
    assert night["hook"] == {"fontSize": 52, "lineCount": 1}


def test_too_long_question_raises(bundle: Path) -> None:
    """下限 44px でも残りに収まらない問題文は例外で落ちること（砦）。"""
    with pytest.raises(subprocess.CalledProcessError) as excinfo:
        _derive(bundle, [_props("あ" * 200)])
    assert "収まらない" in excinfo.value.stderr


def test_char_limit_that_still_fits_is_80(bundle: Path) -> None:
    """R-2 の採用値で収まる問題文の上限は全角 80 字（補充スキルの 90 字より狭い）。

    81 字以上（全角のみ）は下限 44px でも 5 行になり、残りの高さに収まらない。
    在庫の最長は 76 字（id=197）のため現時点の全数は通るが、補充の字数上限
    （quiz-stock-replenish の 90 字）との差はセット計画書のバックログに起票済み。
    """
    (fits,) = _derive(bundle, [_props("あ" * 80)])
    assert fits["question"]["fontSize"] == 44
    assert fits["question"]["lineCount"] == 4

    with pytest.raises(subprocess.CalledProcessError):
        _derive(bundle, [_props("あ" * 81)])
