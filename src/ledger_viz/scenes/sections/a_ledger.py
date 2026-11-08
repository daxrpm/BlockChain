"""A1–A4: del cuaderno de Alice y Bob a la definición de ledger y el problema del doble gasto."""

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
    Scene,
    SurroundingRectangle,
    Text,
    Transform,
    TransformFromCopy,
    VGroup,
    Wiggle,
    Write,
)

from ledger_viz.domain.ledger import Ledger
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
    title_bar,
)

PEOPLE = ("Alice", "Bob", "Carol")
LINE_STEP = 0.55


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


class LedgerSection:
    def __init__(self, scene: Scene) -> None:
        self.scene = scene

    def run(self) -> None:
        self.a1_notebook()
        self.a2_balances()
        self.a3_append_only()
        self.a4_replicated()

    def a1_notebook(self) -> None:
        s = self.scene
        s.next_section("A1_cuaderno")
        self.title = title_bar("El ledger", "¿Dónde anotamos quién le paga a quién?")
        self.people = (
            VGroup(*[person(n) for n in PEOPLE]).arrange(DOWN, buff=0.3).scale(0.72)
        ).move_to(LEFT * 5.6 + DOWN * 0.3)
        self.book = notebook(6.0, 4.3).move_to(LEFT * 0.9 + DOWN * 0.3)
        s.play(FadeIn(self.title, shift=DOWN * 0.2))
        s.play(
            LaggedStart(*[FadeIn(p, shift=RIGHT * 0.3) for p in self.people], lag_ratio=0.2),
            Create(self.book),
            run_time=1.4,
        )
        self.lines = VGroup(_write_line(self.book, 0, "Inicio: Alice tiene 10", muted=True))
        s.play(Write(self.lines[0]), run_time=0.9)
        for i, tx in enumerate(LEDGER_TXS, start=1):
            line = _write_line(self.book, i, tx.label())
            sender = self.people[PEOPLE.index(tx.sender)]
            s.play(Indicate(sender, color=theme.ACCENT, scale_factor=1.08), Write(line), run_time=1)
            self.lines.add(line)
        s.wait(1)

    def a2_balances(self) -> None:
        s = self.scene
        s.next_section("A2_saldos_derivados")
        ledger = Ledger(GENESIS)
        head = label("SALDOS", 0.42, color=theme.ACCENT, bold=True)
        rows = _balance_rows({})
        panel_content = VGroup(head, rows).arrange(DOWN, buff=0.35, aligned_edge=LEFT)
        panel = box(3.0, 3.2, color=theme.MUTED, stroke=2)
        panel.move_to(RIGHT * 4.9 + DOWN * 0.3)
        panel_content.move_to(panel)
        self.balances = VGroup(panel, head, rows)
        s.play(FadeIn(panel), FadeIn(head), FadeIn(rows), run_time=0.8)

        cursor = SurroundingRectangle(self.lines[0], color=theme.ACCENT, buff=0.08)
        s.play(Create(cursor), run_time=0.5)
        steps: list[dict[str, int]] = [ledger.balances()]
        for tx in LEDGER_TXS:
            ledger.append(tx)
            steps.append(ledger.balances())
        for i, balances in enumerate(steps):
            new_rows = _balance_rows(balances).move_to(rows, aligned_edge=LEFT)
            target = SurroundingRectangle(self.lines[i], color=theme.ACCENT, buff=0.08)
            s.play(Transform(cursor, target), Transform(rows, new_rows), run_time=0.8)
            s.wait(0.25)
        self.ledger = ledger
        self.rows = rows
        self.caption = label(
            "El saldo no se guarda: se calcula leyendo la historia", 0.42, color=theme.MUTED
        ).to_edge(DOWN, buff=0.45)
        s.play(FadeOut(cursor), FadeIn(self.caption, shift=UP * 0.2))
        s.wait(1)

    def a3_append_only(self) -> None:
        s = self.scene
        s.next_section("A3_solo_agregar")
        target = self.lines[1]
        eraser = box(1.3, 0.5, color=theme.DANGER, fill=theme.BG)
        eraser_text = label("borrar", 0.32, color=theme.DANGER, bold=True).move_to(eraser)
        eraser_group = VGroup(eraser, eraser_text).next_to(target, RIGHT, buff=2.4)
        s.play(FadeIn(eraser_group, shift=LEFT * 0.3), run_time=0.6)
        s.play(eraser_group.animate.move_to(target.get_center()), run_time=0.8)
        mark = cross(0.5).next_to(self.book[0], RIGHT, buff=-0.6).match_y(target)
        s.play(Wiggle(target, scale_value=1.05), FadeIn(mark, scale=1.4), run_time=0.9)
        s.play(FadeOut(eraser_group, shift=RIGHT * 0.4), FadeOut(mark), run_time=0.6)

        new_line = _write_line(self.book, len(self.lines), APPENDED_TX.label())
        new_line.set_color(theme.ACCENT)
        self.ledger.append(APPENDED_TX)
        new_rows = _balance_rows(self.ledger.balances()).move_to(self.rows, aligned_edge=LEFT)
        plus = label("+", 0.7, color=theme.OK, bold=True).next_to(new_line, LEFT, buff=0.15)
        s.play(Write(new_line), FadeIn(plus), Transform(self.rows, new_rows), run_time=1.1)
        s.play(new_line.animate.set_color(theme.TEXT), FadeOut(plus), run_time=0.6)
        self.lines.add(new_line)

        definition = Text(
            "Ledger = registro ordenado de transacciones al que solo se puede agregar",
            font=theme.FONT_SANS,
            color=theme.TEXT,
            t2c={"Ledger": theme.ACCENT.to_hex(), "solo se puede agregar": theme.ACCENT.to_hex()},
            t2w={"Ledger": "BOLD", "solo se puede agregar": "BOLD"},
        ).scale(0.44)
        frame = box(definition.width + 0.6, definition.height + 0.45, color=theme.ACCENT)
        definition_group = VGroup(frame, definition).to_edge(DOWN, buff=0.35)
        definition.move_to(frame)
        s.play(FadeOut(self.caption), FadeIn(definition_group, shift=UP * 0.2), run_time=0.9)
        self.definition = definition_group
        s.wait(1.2)

    def a4_replicated(self) -> None:
        s = self.scene
        s.next_section("A4_replicado_doble_gasto")
        new_title = title_bar("Un ledger replicado", "Cada nodo guarda su propia copia")
        book_group = VGroup(self.book, self.lines)
        s.play(
            FadeOut(self.people),
            FadeOut(self.balances),
            FadeOut(self.definition),
            Transform(self.title, new_title),
            book_group.animate.scale(0.3).move_to(UP * 0.4),
            run_time=1.1,
        )

        xs = (-5.2, -2.6, 0.0, 2.6, 5.2)
        nodes = VGroup(*[node_icon(0.8).move_to(point(x, 1.3, 0)) for x in xs])
        copies = VGroup(*[book_group.copy().scale(0.75).next_to(n, DOWN, buff=0.15) for n in nodes])
        s.play(
            LaggedStart(*[FadeIn(n, scale=0.8) for n in nodes], lag_ratio=0.12),
            book_group.animate.move_to(DOWN * 1.6),
            run_time=1,
        )
        s.play(
            LaggedStart(*[TransformFromCopy(book_group, c) for c in copies], lag_ratio=0.12),
            run_time=1.4,
        )
        s.play(FadeOut(book_group), run_time=0.4)

        origin = DOWN * 2.0
        alice = person("Alice", 0.6).move_to(origin)
        wallet = label("saldo: 7", 0.32, color=theme.ACCENT).next_to(alice, RIGHT, buff=0.2)
        s.play(FadeIn(alice), FadeIn(wallet), run_time=0.6)

        to_bob, to_carol = DOUBLE_SPEND
        msgs = VGroup()
        anims = []
        for indices, tx in (((0, 1), to_bob), ((3, 4), to_carol)):
            for idx in indices:
                card = mono(tx.label(), 0.32, color=theme.ACCENT).move_to(origin)
                msgs.add(card)
                anims.append(as_anim(card.animate.next_to(copies[idx], DOWN, buff=0.15)))
        s.play(LaggedStart(*anims, lag_ratio=0.08), run_time=1.6)
        marks = VGroup(*[check(0.28).next_to(m, RIGHT, buff=0.08) for m in msgs])
        doubt = label("?", 0.8, color=theme.DANGER, bold=True).next_to(copies[2], DOWN, buff=0.1)
        s.play(FadeIn(marks), FadeIn(doubt, scale=1.4), run_time=0.6)

        warning_box = box(4.4, 0.8, color=theme.DANGER, fill=theme.BG)
        warning = label("⚠ DOBLE GASTO", 0.55, color=theme.DANGER, bold=True)
        warning_group = VGroup(warning_box, warning).move_to(origin)
        warning.move_to(warning_box)
        s.play(FadeOut(alice), FadeOut(wallet), FadeIn(warning_group, scale=1.2), run_time=0.8)
        caption = label(
            "¿Cuál vale? Todos deben acordar un único orden", 0.42, color=theme.TEXT
        ).to_edge(DOWN, buff=0.3)
        s.play(FadeIn(caption, shift=UP * 0.2))
        s.wait(1.5)
