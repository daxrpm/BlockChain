"""Cada `n.cue(...)` de las escenas existe, en orden, dentro del texto de su beat.

Falla en milisegundos lo que si no fallaría tras minutos de render.
"""

import ast
from pathlib import Path

import pytest

from ledger_viz.part3_script import SECTIONS
from ledger_viz.script import WORDS_PER_SECOND, cue_seconds

SECTIONS_DIR = Path(__file__).parents[1] / "src" / "ledger_viz" / "scenes" / "sections"
FILES = ("bridge", "a_ledger", "b_transaction", "c_blocks", "chain", "d_structure", "e_merkle")
BEATS = {b.id: b for s in SECTIONS for b in s.beats}


def _calls(path: Path) -> list[tuple[str, str]]:
    """(método, argumento literal) de cada n.beat / n.cue en orden de aparición."""
    found = [
        (node.lineno, node.col_offset, node.func.attr, node.args[0].value)
        for node in ast.walk(ast.parse(path.read_text()))
        if isinstance(node, ast.Call)
        and isinstance(node.func, ast.Attribute)
        and node.func.attr in {"beat", "cue"}
        and node.args
        and isinstance(node.args[0], ast.Constant)
        and isinstance(node.args[0].value, str)
    ]
    return [(kind, arg) for *_, kind, arg in sorted(found)]


def _literal_cues_by_beat() -> dict[str, list[str]]:
    by_beat: dict[str, list[str]] = {}
    for name in FILES:
        current: str | None = None
        for kind, arg in _calls(SECTIONS_DIR / f"{name}.py"):
            if kind == "beat":
                current = arg
                by_beat[arg] = []
            elif current is not None:
                by_beat[current].append(arg)
    return by_beat


def test_every_scripted_beat_is_animated() -> None:
    animated = set(_literal_cues_by_beat())
    assert animated == set(BEATS)


@pytest.mark.parametrize(("beat_id", "cues"), sorted(_literal_cues_by_beat().items()))
def test_literal_cues_appear_in_order(beat_id: str, cues: list[str]) -> None:
    cursor = 0
    for phrase in cues:
        offset = cue_seconds(BEATS[beat_id].text, phrase, after=cursor)
        cursor = round(offset * WORDS_PER_SECOND) + 1
