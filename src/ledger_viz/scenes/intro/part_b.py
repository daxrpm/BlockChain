"""I4–I5: el whitepaper de Bitcoin y qué es Blockchain (cadena en zigzag del Canva)."""

from manim import (
    DOWN,
    LEFT,
    RIGHT,
    UP,
    Arrow,
    Create,
    FadeIn,
    FadeOut,
    GrowArrow,
    Indicate,
    LaggedStart,
    Line,
    VGroup,
    Write,
)

from ledger_viz.scenes.intro.narrator import Narrator, yellow_card
from ledger_viz.scenes.sections.common import Stage
from ledger_viz.story import CHAIN
from ledger_viz.viz import icons, theme
from ledger_viz.viz.chain_view import build_chain_view
from ledger_viz.viz.components import as_anim, box, cross, label, person, wire_cube


class IntroPartB:
    def __init__(self, stage: Stage, narrator: Narrator) -> None:
        self.stage = stage
        self.n = narrator
        self.s = stage.scene

    def run(self) -> None:
        self.i4_bitcoin()
        self.i5_what_is()

    def i4_bitcoin(self) -> None:
        s, n = self.s, self.n
        n.start("I4_aparicion_de_blockchain")
        with n.beat("whitepaper"):
            self.stage.swap_title("La aparición de Blockchain", "Bitcoin, 2008")
            paper = box(4.2, 5.0, color=theme.TEXT, fill=theme.SURFACE).move_to(
                LEFT * 3.3 + DOWN * 0.45
            )
            paper_title = label("Bitcoin: A Peer-to-Peer", 0.4, bold=True)
            paper_title2 = label("Electronic Cash System", 0.4, bold=True)
            author = label("Satoshi Nakamoto", 0.34, color=theme.ACCENT)
            lines = VGroup(
                *[
                    Line(
                        LEFT * 1.5,
                        RIGHT * (1.5 - 0.4 * (i % 3 == 2)),
                        color=theme.MUTED,
                        stroke_width=3,
                    )
                    for i in range(7)
                ]
            ).arrange(DOWN, buff=0.22, aligned_edge=LEFT)
            content = VGroup(paper_title, paper_title2, author, lines).arrange(DOWN, buff=0.22)
            content.move_to(paper)
            s.play(FadeIn(paper, shift=UP * 0.3), run_time=1.2)
            s.play(Write(paper_title), Write(paper_title2), run_time=2)
            s.play(FadeIn(author), Create(lines), run_time=2)
            year = label("2008", 1.6, color=theme.ACCENT, bold=True).move_to(RIGHT * 3.2 + UP * 0.8)
            pseudo = label("una persona o grupo", 0.4, color=theme.MUTED).next_to(
                year, DOWN, buff=0.25
            )
            pseudo2 = label("bajo un seudónimo", 0.4, color=theme.MUTED).next_to(
                pseudo, DOWN, buff=0.1
            )
            s.play(FadeIn(year, scale=0.6), run_time=1.2)
            s.play(FadeIn(pseudo), FadeIn(pseudo2), run_time=1.2)
            p2p = label("efectivo electrónico entre pares", 0.42, color=theme.ACCENT, bold=True)
            p2p.next_to(pseudo2, DOWN, buff=0.5)
            s.play(FadeIn(p2p, shift=UP * 0.2), run_time=1.2)
            self.i4_paper = VGroup(paper, content)
            self.i4_side = VGroup(year, pseudo, pseudo2, p2p)
        with n.beat("directo"):
            s.play(
                FadeOut(self.i4_side),
                self.i4_paper.animate.scale(0.45).to_corner(LEFT + UP, buff=0.4).shift(DOWN * 0.9),
                run_time=1.5,
            )
            alice = person("Alice", 1.0).move_to(LEFT * 3.0 + DOWN * 0.6)
            bob = person("Bob", 1.0).move_to(RIGHT * 4.0 + DOWN * 0.6)
            bank = icons.bank(theme.MUTED).scale(0.5).move_to(RIGHT * 0.5 + UP * 1.5)
            no = cross(0.9).move_to(bank)
            s.play(FadeIn(alice), FadeIn(bob), FadeIn(bank), Create(no), run_time=1.5)
            arrow = Arrow(alice.get_right(), bob.get_left(), color=theme.ACCENT, buff=0.3)
            money = icons.coin("₿", theme.ACCENT).scale(0.6).next_to(alice, RIGHT, buff=0.2)
            s.play(GrowArrow(arrow), FadeIn(money), run_time=1)
            s.play(as_anim(money.animate.next_to(bob, LEFT, buff=0.2)), run_time=2.2)
            tag = label("sin autoridad central", 0.44, color=theme.ACCENT, bold=True).next_to(
                arrow, DOWN, buff=0.4
            )
            s.play(FadeIn(tag), run_time=1)
            self.i4_direct = VGroup(alice, bob, bank, no, arrow, money, tag)
        with n.beat("pilares"):
            s.play(FadeOut(self.i4_direct), FadeOut(self.i4_paper), run_time=1)
            chain_icon = VGroup(*[wire_cube(0.55) for _ in range(3)]).arrange(RIGHT, buff=0.15)
            cards = (
                VGroup(
                    yellow_card(icons.padlock(), "Criptografía", width=3.7, height=3.4),
                    yellow_card(icons.people(), "Consenso", width=3.7, height=3.4),
                    yellow_card(
                        chain_icon,
                        "Estructura de datos",
                        width=3.7,
                        height=3.4,
                        caption="la cadena de bloques",
                    ),
                )
                .arrange(RIGHT, buff=0.45)
                .move_to(DOWN * 0.55)
            )
            for card in cards:
                s.play(FadeIn(card, shift=UP * 0.3), run_time=1.1)
                s.wait(0.6)
            self.i4_cards = cards
        with n.beat("otras"):
            s.play(FadeOut(self.i4_cards), run_time=1)
            axis = Line(LEFT * 5.5, RIGHT * 5.5, color=theme.MUTED, stroke_width=3).move_to(
                DOWN * 0.1
            )
            marks = VGroup()
            for x, year, text in (
                (-4.5, "2008", "whitepaper"),
                (-1.5, "2009", "primer bloque"),
                (2.5, "después", "otras criptomonedas"),
            ):
                dot = box(0.22, 0.22, color=theme.ACCENT, fill=theme.ACCENT).move_to(
                    axis.point_from_proportion((x + 5.5) / 11)
                )
                yl = label(year, 0.5, color=theme.ACCENT, bold=True).next_to(dot, UP, buff=0.25)
                tl = label(text, 0.36, color=theme.MUTED).next_to(dot, DOWN, buff=0.25)
                marks.add(VGroup(dot, yl, tl))
            s.play(Create(axis), run_time=1)
            s.play(
                LaggedStart(*[FadeIn(m, shift=UP * 0.2) for m in marks], lag_ratio=0.5), run_time=3
            )
            coins = VGroup(
                *[icons.coin(sym, theme.MUTED).scale(0.5) for sym in ("Ξ", "◎", "₳")]
            ).arrange(RIGHT, buff=0.2)
            coins.next_to(marks[2], DOWN, buff=0.3)
            s.play(LaggedStart(*[FadeIn(c, scale=0.5) for c in coins], lag_ratio=0.3), run_time=1.2)
            question = icons.question_bubble("¿Cómo funciona exactamente?", theme.ACCENT).move_to(
                DOWN * 2.9
            )
            s.play(FadeIn(question, shift=UP * 0.2), run_time=1.2)
            s.play(Indicate(question, color=theme.ACCENT), run_time=1.5)

    def i5_what_is(self) -> None:
        s, n = self.s, self.n
        n.start("I5_que_es_blockchain")
        with n.beat("definicion"):
            self.stage.swap_title("Blockchain", "¿Qué es y cómo se organiza?")
            definition = label(
                "Estructura de datos distribuida que almacena registros"
                " en bloques enlazados criptográficamente.",
                0.4,
            ).move_to(UP * 2.1)
            s.play(Write(definition), run_time=3)
            view = build_chain_view(CHAIN)
            s.play(Create(view.entry), run_time=0.6)
            for i, cube in enumerate(view.cubes):
                anims = [Create(cube)]
                if i > 0:
                    anims.insert(0, Create(view.links[i - 1]))
                s.play(*anims, run_time=0.7)
            self.view = view
        with n.beat("enlace"):
            for prev in self.view.prevs:
                s.play(FadeIn(prev, shift=UP * 0.15), run_time=0.7)
            s.play(Indicate(self.view.prevs[0], color=theme.ACCENT, scale_factor=1.2), run_time=1.5)
            caption = label("Cada bloque referencia criptográficamente al anterior.", 0.42)
            caption.to_edge(DOWN, buff=0.35)
            s.play(FadeIn(caption, shift=UP * 0.2), run_time=1.2)
