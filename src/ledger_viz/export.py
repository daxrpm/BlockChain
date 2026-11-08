"""Copia los clips por sección a renders/ con nombre ordenado y genera un PNG de respaldo.

Uso: uv run python -m ledger_viz.export media/videos/part3/1080p30/sections/Part3.json renders
"""

import argparse
import json
import re
import shutil
import subprocess
from dataclasses import dataclass
from pathlib import Path

_SAFE_NAME = re.compile(r"^[A-Za-z0-9_]+$")
_SAFE_VIDEO = re.compile(r"^[A-Za-z0-9_]+\.mp4$")


@dataclass(frozen=True, slots=True)
class ExportPlan:
    source: Path
    video: Path
    poster: Path


def plan_exports(index: Path, out_dir: Path) -> list[ExportPlan]:
    entries = json.loads(index.read_text())
    if not entries:
        msg = f"El índice de secciones está vacío: {index}"
        raise ValueError(msg)
    plans: list[ExportPlan] = []
    for number, entry in enumerate(entries, start=1):
        name, video = str(entry["name"]), str(entry["video"])
        if not _SAFE_NAME.match(name) or not _SAFE_VIDEO.match(video):
            msg = f"Nombre de sección inválido en el índice: {name!r} / {video!r}"
            raise ValueError(msg)
        stem = f"{number:02d}_{name}"
        plans.append(
            ExportPlan(
                source=index.parent / video,
                video=out_dir / f"{stem}.mp4",
                poster=out_dir / f"{stem}.png",
            )
        )
    return plans


def _last_frame(video: Path, poster: Path) -> None:
    ffmpeg = shutil.which("ffmpeg")
    if ffmpeg is None:
        msg = "ffmpeg no está instalado; se necesita para el PNG de respaldo"
        raise RuntimeError(msg)
    subprocess.run(  # noqa: S603 - argumentos fijos, rutas validadas
        [
            ffmpeg,
            "-loglevel",
            "error",
            "-y",
            "-sseof",
            "-0.1",
            "-i",
            str(video),
            "-frames:v",
            "1",
            "-update",
            "1",
            str(poster),
        ],
        check=True,
    )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("index", type=Path)
    parser.add_argument("out_dir", type=Path)
    args = parser.parse_args()
    args.out_dir.mkdir(parents=True, exist_ok=True)
    for plan in plan_exports(args.index, args.out_dir):
        shutil.copyfile(plan.source, plan.video)
        _last_frame(plan.video, plan.poster)
        print(f"✓ {plan.video.name}")  # noqa: T201 - salida de CLI


if __name__ == "__main__":
    main()
