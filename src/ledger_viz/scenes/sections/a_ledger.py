"""S1: del cuaderno de Alice, Bob y Carol a la definición de ledger y el doble gasto."""

import numpy as np
from manim import (
    DOWN,
    LEFT,
    RIGHT,
    UP,
    Create,
    FadeIn,
    FadeOut,
    Indicate,
    LaggedStart,
    SurroundingRectangle,
    Text,
    Transform,
    TransformFromCopy,
    VGroup,
    Wiggle,
    Write,
)
from manim.utils.color import ParsableManimColor

from ledger_viz.domain.ledger import Ledger
from ledger_viz.scenes.narrator import Narrator
from ledger_viz.scenes.sections.common import Stage
from ledger_viz.story import APPENDED_TX, DOUBLE_SPEND, GENESIS, LEDGER_TXS
from ledger_viz.viz import theme
from ledger_viz.viz.components import (
    as_anim,
    box,
    check,
    cross,
    label,
    mono,
    node_icon,
    notebook,
    person,
    point,
)

PEOPLE = ("Alice", "Bob", "Carol")
LINE_STEP = 0.55
TX_CUES = ("alice le paga 5", "bob le paga 2", "carol le devuelve")
WALK_CUES = ("recorremos", "recibió 5", "pagó 2", "le quedan 3")


def _line_position(book: VGroup, index: int) -> np.ndarray:
    rule = book[3]
    x = book[0].get_left()[0] + 0.6
    y = rule.get_center()[1] - 0.45 - index * LINE_STEP
    return np.array([x, y, 0.0])


def _write_line(book: VGroup, index: int, text: str, *, muted: bool = False) -> Text:
    line = mono(text, 0.5, color=theme.MUTED if muted else theme.TEXT)
    line.move_to(_line_position(book, index), aligned_edge=LEFT)
    return line


def _balance_rows(balances: dict[str, int]) -> VGroup:
    rows = VGroup()
    for name in PEOPLE:
        rows.add(
            VGroup(
                label(name, 0.42),
                mono(str(balances.get(name, 0)), 0.55, color=theme.ACCENT),
            ).arrange(RIGHT, buff=0.6)
        )
    rows.arrange(DOWN, buff=0.35, aligned_edge=LEFT)
    values_x = max(row[0].get_right()[0] for row in rows) + 0.5
    for row in rows:
        row[1].set_x(values_x, direction=LEFT)
    return rows


def _framed_text(text: str, color: ParsableManimColor, size: float = 0.5) -> VGroup:
    content = label(text, size, color=color, bold=True)
    frame = box(content.width + 0.6, content.height + 0.4, color=color, fill=theme.BG)
    return VGroup(frame, content.move_to(frame))


class LedgerSection:
    def __init__(self, stage: Stage, narrator: Narrator) -> None:
        self.stage, self.n, self.s = stage, narrator, stage.scene

    def run(self) -> None:
        self.n.start("S1")
        self.notebook()
        self.balances()
        self.append_only()
        self.replicated()
        self.single_order()

    def notebook(self) -> None:
        s, n = self.s, self.n
        with n.beat("S1_1_cuaderno"):
            self.stage.swap_title("El ledger", "¿Dónde anotamos quién le paga a quién?")
            n.cue("alice bob y carol")
            self.people = (
                VGroup(*[person(p) for p in PEOPLE]).arrange(DOWN, buff=0.3).scale(0.72)
            ).move_to(LEFT * 5.6 + DOWN * 0.3)
            s.play(
                LaggedStart(*[FadeIn(p, shift=RIGHT * 0.3) for p in self.people], lag_ratio=0.25),
                run_time=1.4,
            )
            n.cue("cuaderno compartido")
            self.book = notebook(6.0, 4.3).move_to(LEFT * 0.9 + DOWN * 0.3)
            s.play(Create(self.book), run_time=1.2)
            n.cue("alice empieza con 10")
            self.lines = VGroup(_write_line(self.book, 0, "Inicio: Alice tiene 10", muted=True))
            s.play(Write(self.lines[0]), run_time=1.2)
            for i, (tx, cue) in enumerate(zip(LEDGER_TXS, TX_CUES, strict=True), start=1):
                n.cue(cue)
                line = _write_line(self.book, i, tx.label())
                sender = self.people[PEOPLE.index(tx.sender)]
                s.play(
                    Indicate(sender, color=theme.ACCENT, scale_factor=1.08),
                    Write(line),
                    run_time=1.2,
                )
                self.lines.add(line)

    def balances(self) -> None:
        s, n = self.s, self.n
        with n.beat("S1_2_saldos"):
            ledger = Ledger(GENESIS)
            head = label("SALDOS", 0.42, color=theme.ACCENT, bold=True)
            rows = _balance_rows({})
            content = VGroup(head, rows).arrange(DOWN, buff=0.35, aligned_edge=LEFT)
            panel = box(3.0, 3.2, color=theme.MUTED, stroke=2).move_to(RIGHT * 4.9 + DOWN * 0.3)
            content.move_to(panel)
            missing = label("?", 1.4, color=theme.DANGER, bold=True).move_to(panel)
            n.cue("no hay columna de saldos")
            s.play(FadeIn(panel), FadeIn(missing, scale=0.6), run_time=1.0)
            n.cue("cuánto tiene bob")
            s.play(FadeOut(missing), FadeIn(head), FadeIn(rows), run_time=0.8)
            steps: list[dict[str, int]] = [ledger.balances()]
            for tx in LEDGER_TXS:
                ledger.append(tx)
                steps.append(ledger.balances())
            cursor = SurroundingRectangle(self.lines[0], color=theme.ACCENT, buff=0.08)
            for i, (balances, cue) in enumerate(zip(steps, WALK_CUES, strict=True)):
                n.cue(cue)
                new_rows = _balance_rows(balances).move_to(rows, aligned_edge=LEFT)
                target = SurroundingRectangle(self.lines[i], color=theme.ACCENT, buff=0.08)
                first = Create(cursor) if i == 0 else Transform(cursor, target)
                s.play(first, Transform(rows, new_rows), run_time=0.9)
            bob = SurroundingRectangle(rows[1], color=theme.ACCENT, buff=0.1)
            s.play(Create(bob), run_time=0.6)
            n.cue("se calcula")
            caption = label(
                "El saldo no se guarda: se calcula leyendo la historia", 0.42, color=theme.MUTED
            ).to_edge(DOWN, buff=0.45)
            s.play(FadeOut(cursor), FadeOut(bob), FadeIn(caption, shift=UP * 0.2), run_time=1.0)
            self.ledger, self.rows, self.caption = ledger, rows, caption
            self.panel = VGroup(panel, head, rows)

    def append_only(self) -> None:
        s, n = self.s, self.n
        with n.beat("S1_3_definicion"):
            n.cue("no se borra")
            target = self.lines[1]
            eraser = box(1.3, 0.5, color=theme.DANGER, fill=theme.BG)
            eraser_text = label("borrar", 0.32, color=theme.DANGER, bold=True).move_to(eraser)
            eraser_group = VGroup(eraser, eraser_text).next_to(target, RIGHT, buff=2.4)
            s.play(FadeIn(eraser_group, shift=LEFT * 0.3), run_time=0.6)
            s.play(as_anim(eraser_group.animate.move_to(target.get_center())), run_time=0.8)
            mark = cross(0.5).next_to(self.book[0], RIGHT, buff=-0.6).match_y(target)
            s.play(Wiggle(target, scale_value=1.05), FadeIn(mark, scale=1.4), run_time=1.0)
            s.play(FadeOut(eraser_group, shift=RIGHT * 0.4), FadeOut(mark), run_time=0.6)

            n.cue("se agrega una línea")
            new_line = _write_line(self.book, len(self.lines), APPENDED_TX.label())
            new_line.set_color(theme.ACCENT)
            self.ledger.append(APPENDED_TX)
            new_rows = _balance_rows(self.ledger.balances()).move_to(self.rows, aligned_edge=LEFT)
            plus = label("+", 0.7, color=theme.OK, bold=True).next_to(new_line, LEFT, buff=0.15)
            s.play(Write(new_line), FadeIn(plus), Transform(self.rows, new_rows), run_time=1.2)
            s.play(as_anim(new_line.animate.set_color(theme.TEXT)), FadeOut(plus), run_time=0.6)
            self.lines.add(new_line)

            n.cue("eso es un ledger")
            accent = theme.ACCENT.to_hex()
            definition = Text(
                "Ledger = registro ordenado de transacciones al que solo se puede agregar",
                font=theme.FONT_SANS,
                color=theme.TEXT,
                t2c={"Ledger": accent, "solo se puede agregar": accent},
                t2w={"Ledger": "BOLD", "solo se puede agregar": "BOLD"},
            ).scale(0.44)
            frame = box(definition.width + 0.6, definition.height + 0.45, color=theme.ACCENT)
            self.definition = VGroup(frame, definition).to_edge(DOWN, buff=0.35)
            definition.move_to(frame)
            s.play(FadeOut(self.caption), FadeIn(self.definition, shift=UP * 0.2), run_time=1.0)
            n.cue("append-only")
            tag = label("append-only", 0.4, color=theme.ACCENT, bold=True)
            tag.next_to(self.definition, UP, buff=0.15).align_to(self.definition, RIGHT)
            s.play(FadeIn(tag, shift=UP * 0.1), run_time=0.8)
            self.tag = tag

    def replicated(self) -> None:
        s, n = self.s, self.n
        with n.beat("S1_4_replicado"):
            n.cue("cada nodo guarda")
            book_group = VGroup(self.book, self.lines)
            s.play(
                FadeOut(self.people),
                FadeOut(self.panel),
                FadeOut(self.definition),
                FadeOut(self.tag),
                as_anim(book_group.animate.scale(0.3).move_to(DOWN * 1.6)),
                run_time=1.1,
            )
            xs = (-5.2, -2.6, 0.0, 2.6, 5.2)
            nodes = VGroup(*[node_icon(0.8).move_to(point(x, 1.3)) for x in xs])
            copies = VGroup(
                *[book_group.copy().scale(0.75).next_to(nd, DOWN, buff=0.15) for nd in nodes]
            )
            s.play(
                LaggedStart(*[FadeIn(nd, scale=0.8) for nd in nodes], lag_ratio=0.12), run_time=1
            )
            s.play(
                LaggedStart(*[TransformFromCopy(book_group, c) for c in copies], lag_ratio=0.12),
                run_time=1.6,
            )
            s.play(FadeOut(book_group), run_time=0.4)

            n.cue("alice que ahora tiene 7")
            origin = DOWN * 2.0
            alice = person("Alice", 0.6).move_to(origin)
            wallet = label("saldo: 7", 0.32, color=theme.ACCENT).next_to(alice, RIGHT, buff=0.2)
            s.play(FadeIn(alice), FadeIn(wallet), run_time=0.8)

            n.cue("envía a la vez")
            to_bob, to_carol = DOUBLE_SPEND
            msgs = VGroup()
            anims = []
            for indices, tx in (((0, 1), to_bob), ((3, 4), to_carol)):
                for idx in indices:
                    card = mono(tx.label(), 0.32, color=theme.ACCENT).move_to(origin)
                    msgs.add(card)
                    anims.append(as_anim(card.animate.next_to(copies[idx], DOWN, buff=0.15)))
            s.play(LaggedStart(*anims, lag_ratio=0.1), run_time=2.0)
            n.cue("cada mensaje parece válido")
            marks = VGroup(*[check(0.28).next_to(m, RIGHT, buff=0.08) for m in msgs])
            s.play(FadeIn(marks), run_time=0.8)
            n.cue("cuál cuenta")
            doubt = label("?", 0.8, color=theme.DANGER, bold=True).next_to(
                copies[2], DOWN, buff=0.1
            )
            s.play(FadeIn(doubt, scale=1.4), run_time=0.8)
            self.nodes, self.copies = nodes, copies
            self.transient = VGroup(alice, wallet, msgs, marks, doubt)

    def single_order(self) -> None:
        s, n = self.s, self.n
        with n.beat("S1_5_orden"):
            n.cue("doble gasto")
            warning = _framed_text("⚠ DOBLE GASTO", theme.DANGER, 0.55).move_to(DOWN * 1.15)
            s.play(FadeOut(self.transient), FadeIn(warning, scale=1.2), run_time=1.0)

            n.cue("en el mismo orden")
            first, second = DOUBLE_SPEND
            queue = (
                VGroup(
                    *[
                        VGroup(
                            label(f"{i}.", 0.42, color=theme.MUTED, bold=True),
                            mono(tx.label(), 0.42),
                        ).arrange(RIGHT, buff=0.2)
                        for i, tx in enumerate((first, second), start=1)
                    ]
                )
                .arrange(RIGHT, buff=1.6)
                .move_to(DOWN * 2.35)
            )
            s.play(
                LaggedStart(*[FadeIn(q, shift=UP * 0.2) for q in queue], lag_ratio=0.4),
                run_time=1.4,
            )
            ok = VGroup(check(0.32), label("saldo 7 → 0", 0.32, color=theme.OK))
            ok.arrange(RIGHT, buff=0.12).next_to(queue[0], DOWN, buff=0.18)
            s.play(FadeIn(ok), run_time=0.8)

            n.cue("la segunda llega tarde")
            rejected = VGroup(cross(0.3), label("fondos insuficientes", 0.32, color=theme.DANGER))
            rejected.arrange(RIGHT, buff=0.12).next_to(queue[1], DOWN, buff=0.18)
            s.play(FadeIn(rejected), as_anim(queue[1].animate.set_opacity(0.45)), run_time=1.0)

            n.cue("orden único")
            unique = _framed_text("ORDEN ÚNICO", theme.OK, 0.55).move_to(warning)
            s.play(Transform(warning, unique), run_time=1.0)
