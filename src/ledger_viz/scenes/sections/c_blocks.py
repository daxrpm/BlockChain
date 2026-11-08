"""S3: mempool, por qué agrupar en bloques y la diferencia ledger / bloque / transacción."""

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
from ledger_viz.scenes.narrator import Narrator
from ledger_viz.scenes.sections.common import Stage
from ledger_viz.story import short_tx
from ledger_viz.viz import theme
from ledger_viz.viz.components import as_anim, box, label, mono, node_icon, notebook, wire_cube

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
COLUMN_CUES = ("ledger es el cuaderno", "bloque es una página", "transacción una línea")


def _mini_card(tx: Transaction) -> VGroup:
    frame = box(1.15, 0.42, color=theme.MUTED, stroke=2)
    return VGroup(frame, mono(short_tx(tx), 0.32).move_to(frame))


def _counter(value: int, color: ParsableManimColor) -> Text:
    return mono(str(value), 0.9, color=color)


class BlocksSection:
    def __init__(self, stage: Stage, narrator: Narrator) -> None:
        self.stage, self.n, self.s = stage, narrator, stage.scene

    def run(self) -> None:
        self.n.start("S3")
        self.mempool()
        self.batching()
        self.analogy()

    def mempool(self) -> None:
        s, n = self.s, self.n
        with n.beat("S3_1_mempool"):
            self.stage.swap_title("De transacciones a bloques", "¿Por qué agrupar?")
            nodes = VGroup(*[node_icon(0.7) for _ in range(3)]).arrange(DOWN, buff=0.7)
            nodes.move_to(LEFT * 6.0 + DOWN * 0.4)
            frame = DashedVMobject(box(4.8, 3.4, color=theme.MUTED, stroke=2), num_dashes=60)
            frame.move_to(LEFT * 1.9 + DOWN * 0.4)
            pool_label = label("mempool (sala de espera)", 0.36, color=theme.MUTED)
            pool_label.next_to(frame, UP, buff=0.12)
            s.play(FadeIn(nodes), run_time=0.8)
            n.cue("transacciones nuevas")
            cards = VGroup(*[_mini_card(tx) for tx in PENDING])
            cards.arrange_in_grid(rows=4, cols=3, buff=(0.25, 0.3)).move_to(frame)
            targets = [c.get_center() for c in cards]
            for card, node in zip(cards, itertools.cycle(nodes), strict=False):
                card.move_to(node)
            s.play(
                LaggedStart(
                    *[as_anim(c.animate.move_to(t)) for c, t in zip(cards, targets, strict=True)],
                    lag_ratio=0.1,
                ),
                run_time=2.4,
            )
            n.cue("mempool")
            s.play(Create(frame), FadeIn(pool_label), run_time=1.0)
            n.cue("una por una")
            counter_label = label("Rondas de acuerdo", 0.38, color=theme.MUTED)
            counter = _counter(0, theme.TEXT)
            VGroup(counter_label, counter).arrange(DOWN, buff=0.2).move_to(RIGHT * 4.3 + UP * 1.3)
            s.play(FadeIn(counter_label), FadeIn(counter), run_time=0.4)
            cursor = SurroundingRectangle(cards[0], color=theme.ACCENT, buff=0.05)
            s.add(cursor)
            for i, card in enumerate(cards, start=1):
                color = theme.DANGER if i > len(cards) // 2 else theme.TEXT
                s.play(
                    as_anim(cursor.animate.move_to(card)),
                    Transform(counter, _counter(i, color).move_to(counter)),
                    run_time=0.2,
                )
            n.cue("lentísimo")
            slow = label("una por una = lentísimo", 0.36, color=theme.DANGER, bold=True)
            slow.next_to(counter, DOWN, buff=0.15)
            s.play(FadeOut(cursor), FadeIn(slow), run_time=0.8)
            self.cards, self.counter, self.slow = cards, counter, slow
            self.pool = VGroup(frame, pool_label)

    def batching(self) -> None:
        s, n = self.s, self.n
        with n.beat("S3_2_agrupar"):
            n.cue("agrupar")
            cube = wire_cube(1.5).move_to(RIGHT * 4.3 + DOWN * 1.2)
            s.play(Create(cube), run_time=0.8)
            s.play(
                LaggedStart(
                    *[
                        as_anim(c.animate.scale(0.15).move_to(cube).set_opacity(0))
                        for c in self.cards
                    ],
                    lag_ratio=0.06,
                ),
                run_time=1.8,
            )
            n.cue("ese paquete es un bloque")
            block_label = label("Bloque = lote de transacciones", 0.4, bold=True)
            block_label.next_to(cube, DOWN, buff=0.2)
            s.play(
                Transform(self.counter, _counter(1, theme.OK).move_to(self.counter)),
                Transform(
                    self.slow,
                    label("1 bloque = 1 acuerdo", 0.36, color=theme.OK, bold=True).move_to(
                        self.slow
                    ),
                ),
                FadeIn(block_label),
                run_time=1.0,
            )
            n.cue("cada cuánto")
            rules = VGroup(
                label("Cada red define:", 0.4, color=theme.ACCENT, bold=True),
                label("• intervalo: de segundos a minutos", 0.38),
                label("• tamaño máximo del bloque", 0.38),
            ).arrange(DOWN, buff=0.25, aligned_edge=LEFT)
            rules.move_to(LEFT * 1.9 + DOWN * 0.4)
            s.play(FadeOut(self.pool), run_time=0.5)
            s.play(FadeIn(rules[0]), FadeIn(rules[1], shift=RIGHT * 0.2), run_time=1.0)
            n.cue("tamaño máximo")
            s.play(FadeIn(rules[2], shift=RIGHT * 0.2), run_time=0.8)
            n.cue("de decenas a miles")
            span = label("decenas … miles de transacciones por bloque", 0.36, color=theme.MUTED)
            span.next_to(rules, DOWN, buff=0.45).align_to(rules, LEFT)
            s.play(FadeIn(span, shift=UP * 0.1), run_time=0.8)

    def analogy(self) -> None:
        s, n = self.s, self.n
        with n.beat("S3_3_diferencia"):
            self.stage.swap_title("Ledger vs. bloque", "Cuaderno, página, línea")
            page = box(1.5, 2.0, color=theme.TEXT, stroke=3)
            page_lines = VGroup(
                *[
                    Line(LEFT * 0.5, RIGHT * 0.5, color=theme.MUTED, stroke_width=3)
                    for _ in range(5)
                ]
            ).arrange(DOWN, buff=0.22)
            page_lines.move_to(page)
            line_frame = box(1.7, 0.55, color=theme.TEXT, stroke=3)
            pictures = [
                notebook(1.7, 2.1, title=""),
                VGroup(page, page_lines),
                VGroup(line_frame, mono("A→B:5", 0.4).move_to(line_frame)),
            ]
            texts = [
                ("LEDGER", "= el cuaderno", "el registro completo"),
                ("BLOQUE", "= una página", "la unidad con la que crece"),
                ("TRANSACCIÓN", "= una línea", "un movimiento firmado"),
            ]
            columns = VGroup()
            for picture, (name, eq, desc) in zip(pictures, texts, strict=True):
                slot = VGroup(picture).set_height(min(picture.height, 2.1))
                columns.add(
                    VGroup(
                        slot,
                        label(name, 0.5, color=theme.ACCENT, bold=True),
                        label(eq, 0.42),
                        label(desc, 0.34, color=theme.MUTED),
                    ).arrange(DOWN, buff=0.22)
                )
            columns.arrange(RIGHT, buff=1.4, aligned_edge=UP).move_to(DOWN * 0.3)
            for col, cue in zip(columns, COLUMN_CUES, strict=True):
                n.cue(cue)
                s.play(FadeIn(col, shift=UP * 0.3), run_time=0.9)
            n.cue("el ledger es el registro")
            s.play(Indicate(columns[0][3], color=theme.ACCENT), run_time=1.0)
            n.cue("la unidad con la que crece")
            s.play(Indicate(columns[1][3], color=theme.ACCENT), run_time=1.0)
