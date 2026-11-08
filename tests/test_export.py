import json
from pathlib import Path

import pytest

from ledger_viz.export import plan_exports


def _index(tmp_path: Path, entries: list[dict[str, str]]) -> Path:
    path = tmp_path / "Part3.json"
    path.write_text(json.dumps(entries))
    return path


def test_plans_numbered_mp4_and_png(tmp_path: Path) -> None:
    index = _index(
        tmp_path,
        [
            {"name": "A1_cuaderno", "video": "Part3_0000_A1_cuaderno.mp4"},
            {"name": "B1_transaccion", "video": "Part3_0004_B1_transaccion.mp4"},
        ],
    )
    plans = plan_exports(index, tmp_path / "renders")
    assert [p.video.name for p in plans] == ["01_A1_cuaderno.mp4", "02_B1_transaccion.mp4"]
    assert [p.poster.name for p in plans] == ["01_A1_cuaderno.png", "02_B1_transaccion.png"]
    assert plans[0].source == tmp_path / "Part3_0000_A1_cuaderno.mp4"


def test_rejects_path_traversal_in_index(tmp_path: Path) -> None:
    index = _index(tmp_path, [{"name": "../evil", "video": "../../etc/passwd"}])
    with pytest.raises(ValueError, match="inválido"):
        plan_exports(index, tmp_path / "renders")


def test_rejects_empty_index(tmp_path: Path) -> None:
    index = _index(tmp_path, [])
    with pytest.raises(ValueError, match="vacío"):
        plan_exports(index, tmp_path / "renders")
