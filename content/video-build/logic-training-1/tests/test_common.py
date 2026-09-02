"""スロット定義と JSON ヘルパーのテスト。"""

import json
from pathlib import Path

import pytest

from common import _parse_slots, dump_json, load_json, resolve_slots


def _slot(**overrides: object) -> dict[str, object]:
    slot: dict[str, object] = {
        "from_jst_hour": 6,
        "quiz_type": "L1",
        "difficulty": "easy",
        "slot_code": "morning",
        "slot_label": "朝の脳みそトレ",
        "slot_hook": "30秒で解けたら天才",
    }
    slot.update(overrides)
    return slot


class FakeCursor:
    """prompt_configs.parameters だけを返す最小カーソル。"""

    def __init__(self, rows: list[tuple[str]]) -> None:
        self.rows = rows

    def __enter__(self) -> "FakeCursor":
        return self

    def __exit__(self, *_args: object) -> None:
        return None

    def execute(self, _sql: str, _parameters: object = None) -> None:
        return None

    def fetchall(self) -> list[tuple[str]]:
        return self.rows


class FakeConnection:
    """毎回同じ prompt_config 行を返す最小 connection。"""

    def __init__(self, payloads: list[dict[str, object]]) -> None:
        self.rows = [(json.dumps(payload),) for payload in payloads]

    def cursor(self) -> FakeCursor:
        return FakeCursor(self.rows)


def test_parse_slots_normalizes_valid_values() -> None:
    parsed = _parse_slots(json.dumps({"slots": [_slot(slot_label="  朝  ")]}))

    assert parsed[0]["from_jst_hour"] == 6
    assert parsed[0]["slot_label"] == "朝"


@pytest.mark.parametrize(
    ("raw", "message"),
    [
        ("not-json", "JSON オブジェクト"),
        (json.dumps({}), "parameters.slots"),
        (json.dumps({"slots": [{}]}), "必須項目"),
        (json.dumps({"slots": [_slot(slot_hook=" ")]}), "slot_hook"),
    ],
)
def test_parse_slots_rejects_invalid_payloads(raw: str, message: str) -> None:
    with pytest.raises(RuntimeError, match=message):
        _parse_slots(raw)


def test_resolve_slots_accepts_duplicate_same_mapping() -> None:
    payload = {"slots": [_slot()]}

    resolved = resolve_slots(FakeConnection([payload, payload]))

    assert resolved[("L1", "easy")] == {
        "slot_code": "morning",
        "slot_label": "朝の脳みそトレ",
        "slot_hook": "30秒で解けたら天才",
    }


def test_resolve_slots_rejects_conflicting_prompt_configs() -> None:
    connection = FakeConnection(
        [
            {"slots": [_slot()]},
            {
                "slots": [
                    _slot(
                        slot_code="night",
                        slot_label="夜の脳みそトレ",
                        slot_hook="寝る前に挑戦",
                    )
                ]
            },
        ]
    )

    with pytest.raises(RuntimeError, match="一意に決まりません"):
        resolve_slots(connection)


def test_load_dump_json_round_trip_and_default(tmp_path: Path) -> None:
    path = tmp_path / "nested" / "value.json"
    value = {"日本語": [1, 2, 3]}

    assert load_json(path, {"default": True}) == {"default": True}
    dump_json(path, value)

    assert load_json(path, None) == value
