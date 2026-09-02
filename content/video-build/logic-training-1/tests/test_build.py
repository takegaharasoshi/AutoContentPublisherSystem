"""Remotion props とビルド対象選択の純関数テスト。"""

from pathlib import Path
import struct

import pytest

from build import (
    PropsValidationError,
    _container_path,
    _parser,
    _png_size,
    build_props,
    resolve_bgm_source,
    select_items,
    validate_props_input,
)
from common import BASE


def valid_item() -> dict[str, object]:
    """props 検査を通る最小のストック行を返す。"""
    return {
        "id": 85,
        "question_text": "何を買いに来た？",
        "content_fields": {"hint": "並び順がカギ"},
        "video_audio_asset_id": None,
    }


def valid_slot() -> dict[str, str]:
    """props 検査を通るスロットを返す。"""
    return {
        "slot_code": "morning",
        "slot_label": "朝の脳みそトレ",
        "slot_hook": "30秒で解けたら天才",
    }


@pytest.mark.parametrize(
    ("target", "key", "value", "message"),
    [
        ("item", "question_text", " ", "question_text"),
        ("fields", "hint", "", "content_fields.hint"),
        ("slot", "slot_code", "", "slot.slot_code"),
        ("slot", "slot_label", None, "slot.slot_label"),
        ("slot", "slot_hook", " ", "slot.slot_hook"),
    ],
)
def test_validate_props_input_reports_each_required_value(
    target: str, key: str, value: object, message: str
) -> None:
    item = valid_item()
    slot = valid_slot()
    if target == "item":
        item[key] = value
    elif target == "fields":
        item["content_fields"][key] = value
    else:
        slot[key] = value

    errors = validate_props_input(item, slot)

    assert any(message in error for error in errors)


def test_build_props_matches_quiz_props_shape() -> None:
    props = build_props(
        valid_item(),
        valid_slot(),
        illustration_src="illustrations/85.png",
        illustration_width=1536,
        illustration_height=1024,
    )

    assert props == {
        "slotCode": "morning",
        "slotLabel": "朝の脳みそトレ",
        "slotHook": "30秒で解けたら天才",
        "question": "何を買いに来た？",
        "hint": "並び順がカギ",
        "illustrationSrc": "illustrations/85.png",
        "illustrationWidth": 1536,
        "illustrationHeight": 1024,
    }


def test_build_props_raises_validation_error_with_errors() -> None:
    item = valid_item()
    item["question_text"] = ""

    with pytest.raises(PropsValidationError) as captured:
        build_props(
            item,
            valid_slot(),
            illustration_src="illustrations/85.png",
            illustration_width=1,
            illustration_height=1,
        )

    assert captured.value.errors == ["question_text が空です"]


def test_resolve_bgm_source_has_three_branches() -> None:
    assert resolve_bgm_source({"video_audio_asset_id": 7}, rebuild=False) is None
    assert resolve_bgm_source({"video_audio_asset_id": 9}, rebuild=True) == 9
    with pytest.raises(ValueError, match="video_audio_asset_id が NULL"):
        resolve_bgm_source({"video_audio_asset_id": None}, rebuild=True)


def test_select_items_returns_all_or_requested_rows() -> None:
    items = [{"id": 1}, {"id": 2}, {"id": 3}]

    assert select_items(items, None) == items
    assert select_items(items, []) == items
    assert select_items(items, [3, 1]) == [{"id": 1}, {"id": 3}]


def test_select_items_rejects_unknown_id() -> None:
    with pytest.raises(ValueError, match="対象一覧にない.*99"):
        select_items([{"id": 1}], [99])


def test_png_size_reads_ihdr_without_pillow(tmp_path: Path) -> None:
    path = tmp_path / "tiny.png"
    path.write_bytes(
        b"\x89PNG\r\n\x1a\n"
        + struct.pack(">I", 13)
        + b"IHDR"
        + struct.pack(">II", 7, 11)
    )

    assert _png_size(path) == (7, 11)


def test_parser_defaults_and_repeatable_items() -> None:
    defaults = _parser().parse_args([])

    assert defaults.rebuild is False
    assert defaults.item is None
    assert defaults.list is False
    assert defaults.dry_run is False
    assert defaults.skip_assets is False
    assert _parser().parse_args(["--item", "2", "--item", "5"]).item == [2, 5]


def test_container_path_maps_repository_path() -> None:
    assert _container_path(BASE / "work" / "x.json").endswith(
        "/content/video-build/logic-training-1/work/x.json"
    )
