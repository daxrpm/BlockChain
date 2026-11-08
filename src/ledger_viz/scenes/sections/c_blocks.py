"""C1–C2: por qué agrupar transacciones en bloques y la analogía cuaderno/página/línea."""

import itertools

from manim import (
    DOWN,
    LEFT,
    RIGHT,
    UP,
    Create,
    DashedVMobject,
    FadeIn,
    FadeOut,
    Indicate,
    LaggedStart,
    Line,
    SurroundingRectangle,
    Text,
    Transform,
    VGroup,
)
from manim.utils.color import ParsableManimColor

from ledger_viz.domain.transaction import Transaction
from ledger_viz.scenes.sections.common import Stage
from ledger_viz.story import CHAIN, FOCUS_BLOCK, short_tx
from ledger_viz.viz import theme
from ledger_viz.viz.chain_view import build_chain_view
from ledger_viz.viz.components import (
    as_anim,
    box,
    label,
    mono,
    node_icon,
    notebook,
    wire_cube,
)

PENDING = (
    Transaction("Alice", "Bob", 3),
    Transaction("Bob", "Carol", 1),
    Transaction("Dave", "Eve", 2),
    Transaction("Carol", "Dave", 4),
    Transaction("Eve", "Alice", 1),
    Transaction("Bob", "Dave", 2),
    Transaction("Alice", "Carol", 1),
    Transaction("Dave", "Bob", 5),
    Transaction("Carol", "Eve", 2),
    Transaction("Eve", "Bob", 3),
    Transaction("Alice", "Dave", 1),
    Transaction("Bob", "Eve", 2),
)


def _mini_card(tx: Transaction) -> VGroup:
    frame = box(1.15, 0.42, color=theme.MUTED, stroke=2)
    return VGroup(frame, mono(short_tx(tx), 0.32).move_to(frame))


def _counter(value: int, color: ParsableManimColor) -> Text:
    return mono(str(value), 0.9, color=color)


class BlocksSection:
    def __init__(self, stage: Stage) -> None:
        self.stage = stage

    def run(self) -> None:
        self.c1_batching()
        self.c2_analogy()

    def c1_batching(self) -> None:
        s = self.stage.scene
        s.next_section("C1_por_que_bloques")
        self.stage.swap_title("De transacciones a bloques", "¿Por qué agrupar?")

        nodes = VGroup(*[node_icon(0.7) for _ in range(3)]).arrange(DOWN, buff=0.7)
        nodes.move_to(LEFT * 6.0 + DOWN * 0.4)
        pool_frame = DashedVMobject(box(4.8, 3.4, color=theme.MUTED, stroke=2), num_dashes=60)
        pool_frame.move_to(LEFT * 1.9 + DOWN * 0.4)
        pool_label = label("Pendientes (mempool)", 0.36, color=theme.MUTED)
        pool_label.next_to(pool_frame, UP, buff=0.12)
        s.play(FadeIn(nodes), Create(pool_frame), FadeIn(pool_label), run_time=1)

        cards = VGroup(*[_mini_card(tx) for tx in PENDING])
        cards.arrange_in_grid(rows=4, cols=3, buff=(0.25, 0.3)).move_to(pool_frame)
        targets = [c.get_center() for c in cards]
        for card, node in zip(cards, itertools.cycle(nodes), strict=False):
            card.move_to(node)
        s.play(
            LaggedStart(
                *[as_anim(c.animate.move_to(t)) for c, t in zip(cards, targets, strict=True)],
                lag_ratio=0.08,
            ),
            run_time=2.0,
        )

        counter_label = label("Rondas de acuerdo", 0.38, color=theme.MUTED)
        counter = _counter(0, theme.TEXT)
        counter_group = VGroup(counter_label, counter).arrange(DOWN, buff=0.2)
        counter_group.move_to(RIGHT * 4.3 + UP * 1.3)
        s.play(FadeIn(counter_group), run_time=0.5)
        cursor = SurroundingRectangle(cards[0], color=theme.ACCENT, buff=0.05)
        s.add(cursor)
        for i, card in enumerate(cards, start=1):
            color = theme.DANGER if i > len(cards) // 2 else theme.TEXT
            s.play(
                cursor.animate.move_to(card),
                Transform(counter, _counter(i, color).move_to(counter)),
                run_time=0.16,
            )
        slow = label("una por una = lentísimo", 0.36, color=theme.DANGER, bold=True)
        slow.next_to(counter, DOWN, buff=0.15)
        s.play(FadeOut(cursor), FadeIn(slow), run_time=0.5)
        s.wait(0.5)

        cube = wire_cube(1.5).move_to(RIGHT * 4.3 + DOWN * 1.4)
        s.play(Create(cube), run_time=0.7)
        s.play(
            LaggedStart(
                *[as_anim(c.animate.scale(0.15).move_to(cube).set_opacity(0)) for c in cards],
                lag_ratio=0.05,
            ),
            run_time=1.4,
        )
        block_label = label("Bloque = lote de transacciones", 0.4, bold=True)
        block_label.next_to(cube, DOWN, buff=0.2)
        s.play(
            Transform(counter, _counter(1, theme.OK).move_to(counter)),
            Transform(
                slow, label("1 bloque = 1 acuerdo", 0.36, color=theme.OK, bold=True).move_to(slow)
            ),
            FadeIn(block_label),
            run_time=0.8,
        )
        caption = label(
            "Bitcoin: ~1 bloque cada 10 minutos, con miles de transacciones",
            0.4,
            color=theme.MUTED,
        ).to_edge(DOWN, buff=0.35)
        s.play(FadeIn(caption, shift=UP * 0.2))
        s.wait(1.5)

    def c2_analogy(self) -> None:
        s = self.stage.scene
        s.next_section("C2_cuaderno_pagina_linea")
        self.stage.swap_title("Cuaderno, página, línea", "Ledger vs. bloque")

        page = box(1.5, 2.0, color=theme.TEXT, stroke=3)
        page_lines = (
            VGroup(
                *[
                    Line(LEFT * 0.5, RIGHT * 0.5, color=theme.MUTED, stroke_width=3)
                    for _ in range(5)
                ]
            )
            .arrange(DOWN, buff=0.22)
            .move_to(page)
        )
        line_frame = box(1.7, 0.55, color=theme.TEXT, stroke=3)
        icons = [
            notebook(1.7, 2.1, title=""),
            VGroup(page, page_lines),
            VGroup(line_frame, mono("A→B:5", 0.4).move_to(line_frame)),
        ]
        texts = [
            ("LEDGER", "= el cuaderno", "Toda la historia"),
            ("BLOQUE", "= una página", "Lote sellado de transacciones"),
            ("TRANSACCIÓN", "= una línea", "Un movimiento firmado"),
        ]
        columns = VGroup()
        for icon, (name, eq, desc) in zip(icons, texts, strict=True):
            icon_slot = VGroup(icon).set_height(min(icon.height, 2.1))
            col = VGroup(
                icon_slot,
                label(name, 0.5, color=theme.ACCENT, bold=True),
                label(eq, 0.42),
                label(desc, 0.34, color=theme.MUTED),
            ).arrange(DOWN, buff=0.22)
            columns.add(col)
        columns.arrange(RIGHT, buff=1.4, aligned_edge=UP).move_to(DOWN * 0.3)
        s.play(LaggedStart(*[FadeIn(c, shift=UP * 0.3) for c in columns], lag_ratio=0.35))
        s.wait(1.5)

        chain = build_chain_view(CHAIN)
        s.play(FadeOut(columns), run_time=0.6)
        s.play(Create(chain.entry), run_time=0.5)
        for i, cube in enumerate(chain.cubes):
            anims = [Create(cube), FadeIn(chain.prevs[i], shift=UP * 0.1)]
            if i > 0:
                anims.insert(0, Create(chain.links[i - 1]))
            s.play(*anims, run_time=0.55)
        s.play(LaggedStart(*[FadeIn(h) for h in chain.hashes], lag_ratio=0.15), run_time=1)
        caption = label("Cada bloque referencia criptográficamente al anterior.", 0.42).to_edge(
            DOWN, buff=0.4
        )
        s.play(FadeIn(caption, shift=UP * 0.2))
        focus = chain.cubes[FOCUS_BLOCK]
        s.play(Indicate(focus, color=theme.ACCENT, scale_factor=1.15))
        self.stage.focus = focus
        s.wait(1.2)
