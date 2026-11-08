"""Cadena en zigzag idéntica a la diapositiva "Blockchain" del Canva (continuidad visual)."""

import itertools
from collections.abc import Sequence
from dataclasses import dataclass

from manim import DOWN, UP, DashedLine, Text, VGroup
from manim.typing import Point3DLike

from ledger_viz.domain.block import Block
from ledger_viz.domain.hashing import short_hex
from ledger_viz.viz import theme
from ledger_viz.viz.components import label, mono, point, wire_cube

XS = (-5.6, -2.8, 0.0, 2.8, 5.6)
Y_UP, Y_DOWN = 0.75, -0.85
CUBE_SIZE = 0.85


@dataclass
class ChainView:
    cubes: list[VGroup]
    links: list[DashedLine]
    entry: DashedLine
    hashes: list[Text]
    prevs: list[VGroup]

    @property
    def group(self) -> VGroup:
        return VGroup(self.entry, *self.links, *self.cubes, *self.hashes, *self.prevs)


def _dashed(start: Point3DLike, end: Point3DLike) -> DashedLine:
    return DashedLine(start, end, color=theme.ACCENT, dash_length=0.12, stroke_width=3)


def build_chain_view(chain: Sequence[Block]) -> ChainView:
    if len(chain) != len(XS):
        msg = f"El zigzag del Canva tiene {len(XS)} bloques; se recibieron {len(chain)}"
        raise ValueError(msg)
    cubes = [
        wire_cube(CUBE_SIZE, filled=False).move_to(point(x, Y_UP if i % 2 == 0 else Y_DOWN))
        for i, x in enumerate(XS)
    ]
    links = [_dashed(a.get_center(), b.get_center()) for a, b in itertools.pairwise(cubes)]
    entry = _dashed(point(-7.4, cubes[0].get_y()), cubes[0].get_left())
    hashes = [
        mono(f"Hash: {short_hex(block.hash)}", 0.36, color=theme.ACCENT).next_to(
            cube, UP, buff=0.15
        )
        for cube, block in zip(cubes, chain, strict=True)
    ]
    prevs = [
        VGroup(
            label("Hash Previo:", 0.36, bold=True),
            label(short_hex(block.header.prev_hash), 0.4, bold=True),
        )
        .arrange(DOWN, buff=0.08)
        .next_to(cube, DOWN, buff=0.2)
        for cube, block in zip(cubes, chain, strict=True)
    ]
    return ChainView(cubes, links, entry, hashes, prevs)
