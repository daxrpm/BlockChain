"""I6 e I8: propiedades fundamentales y entrada a la criptografía.

La arquitectura (I7) se omitió: es el tema del Integrante 4.
"""

import itertools

from manim import (
    DOWN,
    LEFT,
    RIGHT,
    UP,
    Animation,
    Create,
    DashedLine,
    FadeIn,
    FadeOut,
    Indicate,
    LaggedStart,
    Line,
    Rectangle,
    Transform,
    VGroup,
    Write,
)

from ledger_viz.scenes.intro.narrator import Narrator, yellow_card
from ledger_viz.scenes.sections.common import Stage
from ledger_viz.viz import icons, theme
from ledger_viz.viz.components import (
    as_anim,
    box,
    check,
    cross,
    label,
    mono,
    node_icon,
    person,
    wire_cube,
)


def _mini_chain(count: int, size: float = 0.6) -> tuple[VGroup, VGroup]:
    cubes = VGroup(*[wire_cube(size) for _ in range(count)]).arrange(RIGHT, buff=0.55)
    links = VGroup(
        *[
            DashedLine(a.get_right(), b.get_left(), color=theme.ACCENT, dash_length=0.1)
            for a, b in itertools.pairwise(cubes)
        ]
    )
    return cubes, links


class IntroPartC:
    def __init__(self, stage: Stage, narrator: Narrator) -> None:
        self.stage = stage
        self.n = narrator
        self.s = stage.scene

    def _focus(self, index: int) -> list[Animation]:
        """Resalta una tarjeta oscureciendo las demás con una capa encima."""
        return [
            as_anim(d.animate.set_fill(theme.BG, opacity=0 if i == index else 0.72))
            for i, d in enumerate(self.dimmers)
        ]

    def run(self) -> None:
        self.i6_properties()
        self.i8_protection()

    # ------------------------------------------------------------------ I6
    def i6_properties(self) -> None:
        s, n = self.s, self.n
        n.start("I6_propiedades")
        with n.beat("intro"):
            self.stage.swap_title("Propiedades fundamentales", "¿Qué garantías debe proporcionar?")
            cards = (
                VGroup(
                    yellow_card(
                        icons.database(),
                        "Persistencia",
                        width=3.8,
                        height=3.6,
                        caption="lo confirmado permanece",
                    ),
                    yellow_card(
                        icons.shield_check(),
                        "Seguridad",
                        width=3.8,
                        height=3.6,
                        caption="los honestos no discrepan",
                    ),
                    yellow_card(
                        icons.chart_up(),
                        "Progreso",
                        width=3.8,
                        height=3.6,
                        caption="lo válido se incorpora",
                    ),
                )
                .arrange(RIGHT, buff=0.45)
                .move_to(DOWN * 0.5)
            )
            s.play(
                LaggedStart(*[FadeIn(c, shift=UP * 0.3) for c in cards], lag_ratio=0.5), run_time=3
            )
            self.prop_cards = cards
        small = self.prop_cards.copy().scale(0.42).to_edge(UP, buff=1.3)
        stage_area = DOWN * 1.2

        with n.beat("persistencia"):
            s.play(Transform(self.prop_cards, small), run_time=1.2)
            self.dimmers = VGroup(
                *[
                    Rectangle(width=c.width + 0.04, height=c.height + 0.04, stroke_width=0)
                    .set_fill(theme.BG, opacity=0)
                    .move_to(c)
                    for c in self.prop_cards
                ]
            )
            s.add(self.dimmers)
            s.play(*self._focus(0), run_time=0.6)
            cubes, links = _mini_chain(4, 0.75)
            group = VGroup(cubes, links).move_to(stage_area)
            s.play(
                LaggedStart(*[Create(c) for c in cubes], lag_ratio=0.25),
                Create(links),
                run_time=2.5,
            )
            confirmed = label("confirmado ✓", 0.36, color=theme.OK).next_to(
                cubes[0], DOWN, buff=0.2
            )
            s.play(FadeIn(confirmed), run_time=1)
            s.wait(3)
            attacker = icons.hacker().scale(0.6).next_to(cubes[1], UP, buff=0.3)
            s.play(FadeIn(attacker, shift=DOWN * 0.2), run_time=1)
            s.play(cubes[1].animate.set_stroke(theme.DANGER), run_time=1)
            spark = cross(0.4).move_to(links[1])
            s.play(links[1].animate.set_color(theme.DANGER), FadeIn(spark, scale=1.5), run_time=1)
            s.play(VGroup(*cubes[2:], links[2]).animate.set_stroke(theme.DANGER), run_time=1.2)
            hard = label("modificar el historial: extremadamente difícil", 0.42, bold=True)
            hard.to_edge(DOWN, buff=0.35)
            s.play(FadeIn(hard, shift=UP * 0.2), run_time=1.2)
            self.demo = VGroup(group, confirmed, attacker, spark, hard)

        with n.beat("seguridad"):
            s.play(
                FadeOut(self.demo),
                *self._focus(1),
                run_time=1.2,
            )
            nodes = (
                VGroup(*[node_icon(0.7) for _ in range(5)])
                .arrange(RIGHT, buff=1.2)
                .move_to(stage_area + UP * 0.4)
            )
            s.play(LaggedStart(*[FadeIn(nd) for nd in nodes], lag_ratio=0.15), run_time=1.5)
            hashes = VGroup(
                *[
                    mono("historia #A3F2", 0.3, color=theme.ACCENT).next_to(nd, DOWN, buff=0.2)
                    for nd in nodes
                ]
            )
            s.play(LaggedStart(*[FadeIn(h) for h in hashes], lag_ratio=0.2), run_time=2)
            agree = label(
                "todos los nodos honestos ven la misma historia", 0.42, color=theme.OK, bold=True
            )
            agree.to_edge(DOWN, buff=0.35)
            s.play(FadeIn(agree, shift=UP * 0.2), run_time=1.2)
            rules = VGroup(
                *[
                    icons.shield_check(theme.ACCENT).scale(0.3).next_to(nd, UP, buff=0.15)
                    for nd in nodes
                ]
            )
            s.play(
                LaggedStart(*[FadeIn(r, scale=0.5) for r in rules], lag_ratio=0.15), run_time=1.5
            )
            self.sec_nodes, self.sec_extra = nodes, VGroup(hashes, agree, rules)

        with n.beat("seguridad_ejemplo"):
            s.play(FadeOut(self.sec_extra), run_time=0.8)
            alice = person("Alice", 0.6).move_to(LEFT * 6.0 + DOWN * 0.5)
            bad_tx = mono("Alice → Carol: 7  (ya gastado)", 0.34, color=theme.DANGER)
            bad_tx.next_to(alice, UP, buff=0.2).shift(RIGHT * 1.6)
            s.play(FadeIn(alice), FadeIn(bad_tx), run_time=1.2)
            packets = VGroup(
                *[
                    box(0.35, 0.25, color=theme.DANGER, fill=theme.DANGER).move_to(alice)
                    for _ in self.sec_nodes
                ]
            )
            s.play(
                LaggedStart(
                    *[
                        as_anim(p.animate.next_to(nd, DOWN, buff=0.25))
                        for p, nd in zip(packets, self.sec_nodes, strict=True)
                    ],
                    lag_ratio=0.15,
                ),
                run_time=2.2,
            )
            xs = VGroup(*[cross(0.35).move_to(p) for p in packets])
            s.play(
                FadeOut(packets),
                LaggedStart(*[FadeIn(x, scale=1.5) for x in xs], lag_ratio=0.15),
                run_time=1.5,
            )
            reject = label(
                "rechazada por los nodos → registro consistente",
                0.42,
                color=theme.DANGER,
                bold=True,
            )
            reject.to_edge(DOWN, buff=0.35)
            s.play(FadeIn(reject, shift=UP * 0.2), run_time=1.2)
            self.demo = VGroup(self.sec_nodes, alice, bad_tx, xs, reject)

        with n.beat("progreso"):
            s.play(
                FadeOut(self.demo),
                *self._focus(2),
                run_time=1.2,
            )
            cubes, links = _mini_chain(2, 0.75)
            chain = VGroup(cubes, links).move_to(stage_area + LEFT * 3.5)
            s.play(Create(cubes), Create(links), run_time=1.5)
            for _ in range(3):
                new = wire_cube(0.75).next_to(cubes[-1], RIGHT, buff=0.55)
                link = DashedLine(
                    cubes[-1].get_right(), new.get_left(), color=theme.ACCENT, dash_length=0.1
                )
                plus = label("+", 0.8, color=theme.OK, bold=True).next_to(new, UP, buff=0.15)
                s.play(Create(link), FadeIn(new, shift=LEFT * 0.4), FadeIn(plus), run_time=1.2)
                s.play(FadeOut(plus), run_time=0.4)
                s.wait(1.6)
                cubes.add(new)
                links.add(link)
            grows = label("la cadena sigue creciendo con transacciones válidas", 0.42, bold=True)
            grows.to_edge(DOWN, buff=0.35)
            s.play(FadeIn(grows, shift=UP * 0.2), run_time=1.2)
            self.demo = VGroup(chain, grows)

        with n.beat("conjunto"):
            s.play(FadeOut(self.demo), FadeOut(self.dimmers), run_time=1)
            big = (
                VGroup(
                    yellow_card(
                        icons.database(),
                        "Persistencia",
                        width=3.8,
                        height=3.6,
                        caption="registro persistente",
                    ),
                    yellow_card(
                        icons.shield_check(),
                        "Seguridad",
                        width=3.8,
                        height=3.6,
                        caption="operaciones válidas",
                    ),
                    yellow_card(
                        icons.chart_up(),
                        "Progreso",
                        width=3.8,
                        height=3.6,
                        caption="sigue incorporando",
                    ),
                )
                .arrange(RIGHT, buff=0.45)
                .move_to(DOWN * 0.5)
            )
            s.play(Transform(self.prop_cards, big), run_time=1.5)
            together = label(
                "…sin depender de una autoridad central", 0.46, color=theme.ACCENT, bold=True
            )
            together.to_edge(DOWN, buff=0.4)
            s.play(FadeIn(together, shift=UP * 0.2), run_time=1.2)

    # ------------------------------------------------------------------ I8
    def i8_protection(self) -> None:
        s, n = self.s, self.n
        n.start("I8_como_protegemos")
        with n.beat("repaso"):
            self.stage.swap_title(
                "¿Cómo protegemos la información?",
                "La criptografía como fundamento de la seguridad",
            )
            recap = (
                VGroup(
                    VGroup(
                        icons.database(theme.ACCENT).scale(0.6),
                        label("persistencia", 0.4, bold=True),
                    ).arrange(DOWN, buff=0.2),
                    VGroup(
                        icons.shield_check(theme.ACCENT).scale(0.7),
                        label("seguridad", 0.4, bold=True),
                    ).arrange(DOWN, buff=0.2),
                    VGroup(
                        icons.chart_up(theme.ACCENT).scale(0.7), label("progreso", 0.4, bold=True)
                    ).arrange(DOWN, buff=0.2),
                )
                .arrange(RIGHT, buff=1.8)
                .move_to(UP * 0.2)
            )
            ticks = VGroup(*[check(0.45).next_to(r, RIGHT, buff=0.3) for r in recap])
            s.play(
                LaggedStart(*[FadeIn(r, shift=UP * 0.2) for r in recap], lag_ratio=0.4),
                run_time=1.5,
            )
            s.play(FadeIn(ticks, scale=1.4), run_time=1)
            still = label(
                "…pero todavía hay preguntas", 0.5, color=theme.ACCENT, bold=True
            ).move_to(DOWN * 2.0)
            s.play(FadeIn(still, shift=UP * 0.2), run_time=1.2)
            self.recap = VGroup(recap, ticks, still)

        with n.beat("preguntas"):
            s.play(FadeOut(self.recap), run_time=0.8)
            alice = person("Alice", 0.75).move_to(LEFT * 5.8 + UP * 0.6)
            bob = person("Bob", 0.75).move_to(RIGHT * 5.8 + UP * 0.6)
            msg = icons.document("TX", lines=3).scale(0.5).next_to(alice, RIGHT, buff=0.3)
            sig = icons.signature(theme.ACCENT).scale(0.4).move_to(msg).shift(DOWN * 0.25)
            path = Line(alice.get_right(), bob.get_left(), color=theme.MUTED, stroke_width=2)
            path.set_stroke(opacity=0.6)
            s.play(FadeIn(alice), FadeIn(bob), Create(path), FadeIn(msg), run_time=1.5)
            s.play(Create(sig), run_time=1.0)
            letter = VGroup(msg, sig)
            questions = VGroup(
                VGroup(
                    icons.pen(theme.ACCENT).scale(0.5),
                    label("¿Alice lo autorizó?", 0.38, bold=True),
                ),
                VGroup(
                    icons.hacker().scale(0.5),
                    label("¿Alguien lo modificó en el camino?", 0.38, bold=True),
                ),
                VGroup(
                    wire_cube(0.5), label("¿Alguien alteró el bloque después?", 0.38, bold=True)
                ),
            )
            for q in questions:
                q.arrange(RIGHT, buff=0.3)
            questions.arrange(DOWN, buff=0.35, aligned_edge=LEFT).move_to(DOWN * 2.0)
            s.play(
                FadeIn(questions[0], shift=UP * 0.2), Indicate(sig, color=theme.ACCENT), run_time=2
            )
            s.wait(1.5)
            spy = icons.hacker().scale(0.55).next_to(path, UP, buff=0.4)
            s.play(
                as_anim(letter.animate.move_to(path.get_center())),
                FadeIn(spy, shift=DOWN * 0.2),
                run_time=1.8,
            )
            s.play(
                FadeIn(questions[1], shift=UP * 0.2), Indicate(spy, color=theme.DANGER), run_time=2
            )
            s.wait(1.5)
            s.play(as_anim(letter.animate.next_to(bob, LEFT, buff=0.3)), FadeOut(spy), run_time=1.5)
            s.play(FadeIn(questions[2], shift=UP * 0.2), run_time=1.5)
            self.i8 = VGroup(alice, bob, path, letter, questions)

        with n.beat("sin_autoridad"):
            s.play(FadeOut(self.i8), run_time=1)
            bank = icons.bank(theme.MUTED).scale(0.7).move_to(LEFT * 3.2 + DOWN * 0.2)
            no = cross(1.4).move_to(bank)
            words = (
                VGroup(
                    label("autenticidad", 0.6, color=theme.ACCENT, bold=True),
                    label("+", 0.6, bold=True),
                    label("integridad", 0.6, color=theme.ACCENT, bold=True),
                )
                .arrange(RIGHT, buff=0.3)
                .move_to(RIGHT * 2.6 + DOWN * 0.2)
            )
            q = label("¿cómo las garantizamos?", 0.42, color=theme.MUTED).next_to(
                words, DOWN, buff=0.35
            )
            s.play(FadeIn(bank), Create(no), run_time=1.5)
            s.play(FadeIn(words, shift=LEFT * 0.2), run_time=1.5)
            s.play(FadeIn(q), run_time=1)
            self.i8 = VGroup(bank, no, words, q)

        with n.beat("criptografia"):
            s.play(FadeOut(self.i8), run_time=1)
            lock = icons.padlock(theme.ACCENT).scale(1.6).move_to(UP * 0.4)
            word = label("CRIPTOGRAFÍA", 1.0, color=theme.ACCENT, bold=True).next_to(
                lock, DOWN, buff=0.4
            )
            s.play(FadeIn(lock, scale=0.5), run_time=1.5)
            s.play(Write(word), run_time=1.5)
            uses = VGroup(
                VGroup(icons.padlock().scale(0.4), label("proteger la información", 0.34)),
                VGroup(icons.key().scale(0.45), label("identidad y autorización", 0.34)),
                VGroup(icons.fingerprint().scale(0.6), label("detectar modificaciones", 0.34)),
            )
            for u in uses:
                u.arrange(RIGHT, buff=0.25)
            uses.arrange(RIGHT, buff=0.7).to_edge(DOWN, buff=1.1)
            s.play(VGroup(lock, word).animate.shift(UP * 0.5), run_time=0.8)
            s.play(
                LaggedStart(*[FadeIn(u, shift=UP * 0.2) for u in uses], lag_ratio=0.5), run_time=3
            )
            handoff = label(
                "A continuación: Integrante 2 · Criptografía aplicada", 0.38, color=theme.MUTED
            )
            handoff.to_edge(DOWN, buff=0.4)
            s.play(FadeIn(handoff, shift=UP * 0.2), run_time=1.2)
