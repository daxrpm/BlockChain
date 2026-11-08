"""La cadena vista como estructura de datos: cajas con «Hash previo» y «Hash» y punteros de hash."""

from collections.abc import Sequence
from dataclasses import dataclass

from manim import DOWN, LEFT, RIGHT, UP, Arrow, CurvedArrow, RoundedRectangle, Text, VGroup

from ledger_viz.domain.block import Block
from ledger_viz.domain.hashing import short_hex
from ledger_viz.viz import theme
from ledger_viz.viz.components import label, mono, point

SLOTS = 5
BLOCK_W, BLOCK_H = 2.35, 1.75
STEP = 2.85
ROW_Y = -0.2
BLANK = "····"


def slot_x(i: int) -> float:
    return (i - (SLOTS - 1) / 2) * STEP


def short(digest: bytes) -> str:
    return f"{short_hex(digest)}…"


@dataclass
class LinkedBlock:
    frame: RoundedRectangle
    title: Text
    prev_label: Text
    prev_value: Text
    hash_label: Text
    hash_value: Text

    @property
    def group(self) -> VGroup:
        return VGroup(
            self.frame,
            self.title,
            self.prev_label,
            self.prev_value,
            self.hash_label,
            self.hash_value,
        )

    @property
    def details(self) -> VGroup:
        return VGroup(
            self.title, self.prev_label, self.prev_value, self.hash_label, self.hash_value
        )


def prev_text(block: Block, *, known: bool, size: float = 0.38) -> Text:
    if not known:
        return mono(BLANK, size, color=theme.MUTED)
    return mono(short(block.header.prev_hash), size, color=theme.TEXT)


def linked_block(block: Block, index: int, *, prev_known: bool = True) -> LinkedBlock:
    frame = RoundedRectangle(
        width=BLOCK_W,
        height=BLOCK_H,
        corner_radius=0.12,
        stroke_color=theme.ACCENT,
        stroke_width=3,
        fill_color=theme.SURFACE,
        fill_opacity=1,
    ).move_to(point(slot_x(index), ROW_Y))
    title = label(f"Bloque {index}", 0.36, bold=True).next_to(frame.get_top(), DOWN, buff=0.16)
    left = frame.get_left()[0] + 0.2
    prev_label = label("Hash previo", 0.27, color=theme.MUTED)
    prev_label.move_to(point(left, frame.get_y() + 0.2), aligned_edge=LEFT)
    prev_value = prev_text(block, known=prev_known).next_to(prev_label, DOWN, buff=0.1)
    prev_value.align_to(prev_label, LEFT)
    hash_label = label("Hash", 0.27, color=theme.MUTED)
    hash_label.move_to(point(left, frame.get_y() - 0.42), aligned_edge=LEFT)
    hash_value = mono(short(block.hash), 0.38, color=theme.ACCENT).next_to(
        hash_label, RIGHT, buff=0.18
    )
    return LinkedBlock(frame, title, prev_label, prev_value, hash_label, hash_value)


def build_linked_view(chain: Sequence[Block], *, prev_known: bool = True) -> list[LinkedBlock]:
    if len(chain) > SLOTS:
        msg = f"La fila tiene {SLOTS} espacios; se recibieron {len(chain)} bloques"
        raise ValueError(msg)
    return [linked_block(b, i, prev_known=prev_known) for i, b in enumerate(chain)]


def copy_arrow(src: LinkedBlock, dst: LinkedBlock) -> Arrow:
    """Flecha que lleva el hash de un bloque al campo «Hash previo» del siguiente."""
    return Arrow(
        src.hash_value.get_right(),
        dst.prev_value.get_left(),
        color=theme.ACCENT,
        buff=0.08,
        stroke_width=4,
        max_tip_length_to_length_ratio=0.18,
    )


def pointer(src: LinkedBlock, dst: LinkedBlock) -> CurvedArrow:
    """Puntero de hash: del bloque nuevo (dst) hacia su anterior (src), por encima de la fila."""
    return CurvedArrow(
        dst.frame.get_top() + LEFT * 0.35 + UP * 0.05,
        src.frame.get_top() + RIGHT * 0.35 + UP * 0.05,
        angle=0.9,
        color=theme.ACCENT,
        stroke_width=4,
        tip_length=0.18,
    )
