"""I0–I3: Blockchain vs Bitcoin, sistema centralizado, problema de confianza, descentralizado."""

import math

from manim import (
    DOWN,
    LEFT,
    RIGHT,
    UP,
    Arrow,
    Circumscribe,
    Create,
    DashedLine,
    FadeIn,
    FadeOut,
    GrowArrow,
    Indicate,
    LaggedStart,
    Line,
    Transform,
    VGroup,
    Write,
)

from ledger_viz.scenes.intro.narrator import Narrator, yellow_card
from ledger_viz.scenes.sections.common import Stage
from ledger_viz.story import CHAIN
from ledger_viz.viz import icons, theme
from ledger_viz.viz.chain_view import build_chain_view
from ledger_viz.viz.components import as_anim, box, check, cross, label, mono, person, point


def _cubes_only() -> VGroup:
    view = build_chain_view(CHAIN)
    return VGroup(view.entry, *view.links, *view.cubes)


class IntroPartA:
    def __init__(self, stage: Stage, narrator: Narrator) -> None:
        self.stage = stage
        self.n = narrator
        self.s = stage.scene

    def run(self) -> None:
        self.i0_blockchain_vs_bitcoin()
        self.i1_centralized()
        self.i2_trust_problem()
        self.i3_decentralized()

    # ------------------------------------------------------------------ I0
    def i0_blockchain_vs_bitcoin(self) -> None:
        s, n = self.s, self.n
        n.start("I0_blockchain_vs_bitcoin")
        with n.beat("portada"):
            heading = label("BLOCKCHAIN", 1.8, color=theme.ACCENT, bold=True).move_to(UP * 0.5)
            cubes = _cubes_only().scale(0.55).to_edge(DOWN, buff=0.5)
            s.play(FadeIn(self.stage.title, shift=DOWN * 0.2), run_time=1.2)
            s.play(FadeIn(heading, shift=DOWN * 0.3), run_time=1.5)
            s.play(Create(cubes), run_time=3)
        with n.beat("confusion"):
            s.play(
                FadeOut(heading),
                cubes.animate.scale_to_fit_width(4.6).move_to(LEFT * 4.2),
                run_time=1.5,
            )
            btc = icons.coin("₿", theme.ACCENT).scale(1.9).move_to(RIGHT * 3.8)
            same = label("=", 2.0, bold=True)
            doubt = label("?", 1.2, color=theme.DANGER, bold=True).next_to(same, UP, buff=0.05)
            names = VGroup(
                label("Blockchain", 0.6, bold=True).next_to(cubes, DOWN, buff=0.5),
                label("Bitcoin", 0.6, bold=True).next_to(btc, DOWN, buff=0.5),
            )
            s.play(FadeIn(btc, scale=0.7), FadeIn(names), run_time=1.2)
            s.play(Write(same), FadeIn(doubt, scale=1.5), run_time=1)
            s.play(Indicate(doubt, color=theme.DANGER), run_time=1.2)
        with n.beat("diferencia"):
            s.play(FadeOut(VGroup(same, doubt, names, cubes)), btc.animate.scale(0.5), run_time=1)
            tech = box(9.5, 4.6, color=theme.ACCENT, fill=theme.SURFACE).move_to(DOWN * 0.3)
            tech_title = label("BLOCKCHAIN  ·  la tecnología", 0.55, color=theme.ACCENT, bold=True)
            gear = icons.gear(theme.ACCENT).scale(0.6)
            VGroup(gear, tech_title).arrange(RIGHT, buff=0.3).next_to(
                tech.get_top(), DOWN, buff=0.3
            )
            tech.set_z_index(-1)
            s.play(Create(tech), FadeIn(tech_title), FadeIn(gear), run_time=1.5)
            s.play(btc.animate.move_to(tech.get_center() + LEFT * 2.3 + DOWN * 0.3), run_time=1.2)
            btc_label = label("Bitcoin", 0.5, bold=True).next_to(btc, DOWN, buff=0.2)
            btc_note = label("una criptomoneda que la usa", 0.36, color=theme.MUTED)
            btc_note.next_to(btc_label, DOWN, buff=0.1)
            s.play(FadeIn(btc_label), FadeIn(btc_note), run_time=1)
            others = VGroup(
                *[icons.coin(sym, theme.MUTED).scale(0.75) for sym in ("Ξ", "◎", "₳")]
            ).arrange(RIGHT, buff=0.4)
            others.move_to(tech.get_center() + RIGHT * 2.2 + DOWN * 0.3)
            others_label = label("otras criptomonedas", 0.36, color=theme.MUTED)
            others_label.next_to(others, DOWN, buff=0.3)
            s.play(
                LaggedStart(*[FadeIn(o, scale=0.6) for o in others], lag_ratio=0.3), run_time=1.5
            )
            s.play(FadeIn(others_label), run_time=0.8)
            self.i0_parts = VGroup(
                tech, tech_title, gear, btc, btc_label, btc_note, others, others_label
            )
        with n.beat("pregunta"):
            q1 = icons.question_bubble("¿Por qué surgió?", theme.ACCENT)
            q2 = icons.question_bubble("¿Qué problema resuelve?", theme.ACCENT)
            VGroup(q1, q2).arrange(RIGHT, buff=1.2).move_to(DOWN * 0.3)
            s.play(FadeOut(self.i0_parts), run_time=1)
            s.play(
                LaggedStart(FadeIn(q1, shift=UP * 0.3), FadeIn(q2, shift=UP * 0.3), lag_ratio=0.5),
                run_time=1.6,
            )

    # ------------------------------------------------------------------ I1
    def i1_centralized(self) -> None:
        s, n = self.s, self.n
        n.start("I1_sistema_centralizado")
        with n.beat("definicion"):
            self.stage.swap_title("Sistema centralizado", "Una autoridad central controla todo")
            panel = box(13.0, 5.0, color=theme.ACCENT, fill=theme.ACCENT).move_to(DOWN * 0.55)
            self.bank = icons.bank(theme.BG).scale(0.85).move_to(UP * 0.55)
            bank_label = label("Banco · autoridad central", 0.4, color=theme.BG, bold=True)
            bank_label.next_to(self.bank, DOWN, buff=0.15)
            self.db = icons.database(theme.BG).scale(0.65).move_to(DOWN * 2.0 + LEFT * 0.8)
            db_label = label("Ledger central", 0.36, color=theme.BG, bold=True)
            db_label.next_to(self.db, DOWN, buff=0.12)
            link = Arrow(bank_label.get_bottom(), self.db.get_top(), color=theme.BG, buff=0.1)
            s.play(FadeIn(panel), run_time=1.2)
            s.play(FadeIn(self.bank, scale=0.8), FadeIn(bank_label), run_time=1.5)
            s.play(GrowArrow(link), FadeIn(self.db, shift=UP * 0.2), FadeIn(db_label), run_time=1.5)
            keywords = (
                VGroup(
                    label("controla", 0.4, color=theme.BG, bold=True),
                    label("los datos", 0.36, color=theme.BG),
                    label("y las operaciones", 0.36, color=theme.BG),
                )
                .arrange(DOWN, buff=0.08)
                .next_to(self.bank, RIGHT, buff=0.9)
            )
            s.play(FadeIn(keywords, shift=LEFT * 0.2), run_time=1.2)
            self.panel, self.bank_label, self.db_label, self.db_link = (
                panel,
                bank_label,
                db_label,
                link,
            )
            self.keywords = keywords
        with n.beat("participantes"):
            self.alice = person("Alice", 0.9, color=theme.BG).move_to(LEFT * 5.0 + DOWN * 0.3)
            self.bob = person("Bob", 0.9, color=theme.BG).move_to(RIGHT * 5.0 + DOWN * 0.3)
            s.play(
                FadeOut(self.keywords),
                FadeIn(self.alice, shift=RIGHT * 0.3),
                FadeIn(self.bob, shift=LEFT * 0.3),
                run_time=1.5,
            )
            wish = icons.question_bubble("Quiero enviar 5 a Bob", theme.BG).scale(0.8)
            wish.next_to(self.alice, UP, buff=0.2).shift(RIGHT * 0.6)
            s.play(FadeIn(wish, shift=UP * 0.2), run_time=1)
            self.wish = wish
        with n.beat("solicitud"):
            request = icons.document("TRANSFERIR", lines=3, color=theme.BG).scale(0.45)
            request.move_to(self.alice.get_right() + RIGHT * 0.5)
            arrow = Arrow(self.alice.get_right(), self.bank.get_left(), color=theme.BG, buff=0.3)
            s.play(FadeOut(self.wish), GrowArrow(arrow), FadeIn(request), run_time=1.2)
            s.play(request.animate.move_to(self.bank.get_left() + LEFT * 0.4), run_time=1.6)
            self.request, self.req_arrow = request, arrow
        with n.beat("verifica"):
            stamp = check(0.6, color=theme.BG).next_to(self.bank, UP, buff=0.1).shift(RIGHT * 1.2)
            checks = (
                VGroup(
                    label("¿tiene fondos?  ✓", 0.34, color=theme.BG),
                    label("operación autorizada  ✓", 0.34, color=theme.BG),
                )
                .arrange(DOWN, buff=0.1, aligned_edge=LEFT)
                .next_to(self.bank, RIGHT, buff=0.5)
                .shift(UP * 0.3)
            )
            s.play(Circumscribe(self.bank, color=theme.BG), run_time=1.5)
            s.play(FadeIn(stamp, scale=1.6), FadeIn(checks[0]), run_time=1)
            s.play(FadeIn(checks[1]), run_time=0.8)
            self.checks, self.stamp = checks, stamp
        with n.beat("registra"):
            row = mono("Alice → Bob: 5", 0.36, color=theme.BG).next_to(self.db, RIGHT, buff=0.35)
            s.play(FadeOut(self.request), Indicate(self.db, color=theme.BG), run_time=1)
            s.play(Write(row), run_time=1.2)
            money = (
                icons.coin("$", theme.BG).scale(0.55).move_to(self.bank.get_right() + RIGHT * 0.3)
            )
            pay = Arrow(self.bank.get_right(), self.bob.get_left(), color=theme.BG, buff=0.3)
            s.play(FadeIn(money), GrowArrow(pay), run_time=0.8)
            s.play(money.animate.next_to(self.bob, UP, buff=0.15), run_time=1.6)
            self.row, self.money, self.pay = row, money, pay
        with n.beat("conclusion"):
            depends = VGroup(
                DashedLine(self.alice.get_top(), self.bank.get_corner(UP + LEFT), color=theme.BG),
                DashedLine(self.bob.get_top(), self.bank.get_corner(UP + RIGHT), color=theme.BG),
            )
            dep_label = label("ambos dependen del banco", 0.36, color=theme.BG, bold=True)
            dep_label.next_to(self.bank, UP, buff=0.35)
            s.play(
                FadeOut(self.checks),
                FadeOut(self.stamp),
                Create(depends),
                FadeIn(dep_label),
                run_time=1.8,
            )
            conclusion_box = box(11.2, 0.75, color=theme.BG, fill=theme.BG)
            conclusion = label(
                "Una autoridad de confianza gestiona y valida las transacciones",
                0.42,
                color=theme.ACCENT,
                bold=True,
            )
            concl = VGroup(conclusion_box, conclusion).move_to(DOWN * 3.55)
            conclusion.move_to(conclusion_box)
            s.play(FadeIn(concl, shift=UP * 0.2), run_time=1.2)

    # ------------------------------------------------------------------ I2
    def i2_trust_problem(self) -> None:
        s, n = self.s, self.n
        n.start("I2_problema_de_confianza")
        with n.beat("sin_banco"):
            self.stage.swap_title("El problema de confianza", "¿Y si quitamos al intermediario?")
            alice = person("Alice", 1.0).move_to(LEFT * 4.2 + DOWN * 0.4)
            bob = person("Bob", 1.0).move_to(RIGHT * 4.2 + DOWN * 0.4)
            bank = icons.bank().scale(0.75).move_to(UP * 0.3)
            s.play(FadeIn(alice), FadeIn(bob), FadeIn(bank), run_time=1.5)
            x = cross(1.6).move_to(bank)
            s.play(Create(x), run_time=1)
            s.play(FadeOut(VGroup(bank, x), scale=0.6), run_time=1.2)
            direct = Arrow(alice.get_right(), bob.get_left(), color=theme.ACCENT, buff=0.3)
            direct_label = label("directamente entre ellos", 0.42, color=theme.ACCENT, bold=True)
            direct_label.next_to(direct, UP, buff=0.2)
            s.play(GrowArrow(direct), FadeIn(direct_label), run_time=1.5)
            self.i2 = VGroup(alice, bob, direct, direct_label)
        with n.beat("preguntas"):
            s.play(self.i2.animate.scale(0.6).to_edge(UP, buff=1.5), run_time=1.2)
            cards = (
                VGroup(
                    yellow_card(icons.shield_check(), "¿Quién valida?", width=3.6, height=2.8),
                    yellow_card(
                        icons.database(), "¿Dónde está el registro?", width=4.3, height=2.8
                    ),
                    yellow_card(icons.people(), "¿Cómo confiamos?", width=3.6, height=2.8),
                )
                .arrange(RIGHT, buff=0.4)
                .move_to(DOWN * 1.5)
            )
            for card in cards:
                s.play(FadeIn(card, shift=UP * 0.3), run_time=1.0)
                s.wait(1.6)
            self.i2_cards = cards
        with n.beat("confianza"):
            s.play(FadeOut(self.i2_cards), FadeOut(self.i2), run_time=1)
            left = VGroup(icons.bank().scale(0.6), label("Banco", 0.42, bold=True))
            left.arrange(DOWN, buff=0.2)
            left_ok = label("confianza en una entidad", 0.36, color=theme.OK)
            left_group = (
                VGroup(left, left_ok).arrange(DOWN, buff=0.3).move_to(LEFT * 3.6 + DOWN * 0.3)
            )
            right = VGroup(icons.people().scale(0.9), label("Red sin banco", 0.42, bold=True))
            right.arrange(DOWN, buff=0.2)
            right_q = label("¿confianza en...?", 0.36, color=theme.DANGER)
            right_group = (
                VGroup(right, right_q).arrange(DOWN, buff=0.3).move_to(RIGHT * 3.6 + DOWN * 0.3)
            )
            arrow = Arrow(
                left_group.get_right(), right_group.get_left(), color=theme.ACCENT, buff=0.4
            )
            s.play(FadeIn(left_group, shift=RIGHT * 0.2), run_time=1.5)
            s.play(GrowArrow(arrow), FadeIn(right_group, shift=LEFT * 0.2), run_time=1.5)
            s.play(Indicate(right_q, color=theme.DANGER, scale_factor=1.2), run_time=1.5)

    # ------------------------------------------------------------------ I3
    def i3_decentralized(self) -> None:
        s, n = self.s, self.n
        n.start("I3_sistema_descentralizado")
        with n.beat("red"):
            self.stage.swap_title(
                "Sistema descentralizado", "El control se reparte entre muchos nodos"
            )
            names = ("Alice", "Nodo", "Nodo", "Bob", "Nodo", "Nodo", "Nodo")
            center = DOWN * 0.45
            nodes = VGroup()
            for k, name in enumerate(names[:-1]):
                angle = math.pi / 2 + k * 2 * math.pi / 6
                pos = center + point(math.cos(angle) * 4.2, math.sin(angle) * 2.3)
                nodes.add(person(name, 0.62).move_to(pos))
            nodes.add(person("Nodo", 0.62).move_to(center))
            ring = len(nodes) - 1
            pairs = [(k, (k + 1) % ring) for k in range(ring)]  # anillo exterior
            pairs += [(k, ring) for k in range(ring)]  # radios al nodo central
            pairs += [(0, 2), (3, 5)]  # algunas cuerdas: malla parcial, como una red P2P
            edges = VGroup(
                *[
                    Line(
                        nodes[a].get_center(),
                        nodes[b].get_center(),
                        buff=0.6,
                        color=theme.MUTED,
                        stroke_width=2,
                    )
                    for a, b in pairs
                ]
            )
            edges.set_z_index(-1)
            s.play(
                LaggedStart(*[FadeIn(nd, scale=0.7) for nd in nodes], lag_ratio=0.15), run_time=2.5
            )
            s.play(Create(edges), run_time=2.5)
            for nd in (nodes[0], nodes[3]):
                nd[0].set_color(theme.ACCENT)
                nd[1].set_color(theme.ACCENT)
            s.play(
                Indicate(nodes[0], color=theme.ACCENT),
                Indicate(nodes[3], color=theme.ACCENT),
                run_time=1.5,
            )
            self.net_nodes, self.net_edges = nodes, edges
        with n.beat("replicas"):
            ledgers = VGroup(
                *[
                    icons.database(theme.ACCENT).scale(0.28).next_to(nd, RIGHT, buff=0.08)
                    for nd in self.net_nodes
                ]
            )
            s.play(
                LaggedStart(*[FadeIn(lg, scale=0.5) for lg in ledgers], lag_ratio=0.15), run_time=3
            )
            tag = label(
                "Replicated ledger: cada nodo guarda una copia", 0.42, color=theme.ACCENT, bold=True
            )
            tag.to_edge(DOWN, buff=0.35)
            s.play(FadeIn(tag, shift=UP * 0.2), run_time=1.2)
            self.net_ledgers, self.net_tag = ledgers, tag
        with n.beat("reglas"):
            shield = icons.shield_check(theme.ACCENT).scale(0.8)
            shield_bg = box(1.6, 1.8, color=theme.ACCENT, fill=theme.BG).move_to(self.net_nodes[-1])
            shield.move_to(shield_bg)
            rules = label("Reglas del protocolo", 0.38, color=theme.ACCENT, bold=True)
            rules.next_to(shield_bg, DOWN, buff=0.1)
            s.play(
                FadeOut(self.net_nodes[-1]),
                FadeOut(self.net_ledgers[-1]),
                FadeIn(shield_bg),
                FadeIn(shield, scale=0.6),
                FadeIn(rules),
                run_time=1.5,
            )
            ticks = VGroup(
                *[check(0.25).next_to(lg, UP, buff=0.04) for lg in self.net_ledgers[:-1]]
            )
            s.play(LaggedStart(*[FadeIn(t, scale=1.5) for t in ticks], lag_ratio=0.2), run_time=2.5)
            same = label("todos verifican el mismo registro", 0.42, bold=True).to_edge(
                DOWN, buff=0.35
            )
            s.play(Transform(self.net_tag, same), run_time=1)
            self.net_rules = VGroup(shield_bg, shield, rules, ticks)
        with n.beat("preguntas"):
            s.play(
                FadeOut(VGroup(self.net_edges, self.net_ledgers, self.net_rules, self.net_tag)),
                *[
                    FadeOut(nd)
                    for nd in self.net_nodes
                    if nd not in (self.net_nodes[0], self.net_nodes[3])
                ],
                run_time=1.2,
            )
            alice, bob = self.net_nodes[0], self.net_nodes[3]
            s.play(
                alice.animate.scale(1.4).move_to(LEFT * 4.5 + DOWN * 0.3),
                bob.animate.scale(1.4).move_to(RIGHT * 4.5 + DOWN * 0.3),
                run_time=1.2,
            )
            bank_ghost = icons.bank(theme.MUTED).scale(0.6).move_to(UP * 0.4)
            no = cross(1.2).move_to(bank_ghost)
            s.play(FadeIn(bank_ghost), Create(no), run_time=1.2)
            q_funds = icons.question_bubble("¿Alice tiene los fondos?", theme.ACCENT).scale(0.9)
            q_funds.next_to(alice, UP, buff=0.3).shift(RIGHT * 1.0)
            s.play(FadeOut(VGroup(bank_ghost, no)), FadeIn(q_funds, shift=UP * 0.2), run_time=1.2)
            s.wait(1.5)
            coin_a = icons.coin("$", theme.ACCENT).scale(0.6).next_to(alice, RIGHT, buff=0.3)
            coin_b = coin_a.copy()
            carol = person("Carol", 0.85).move_to(RIGHT * 4.5 + DOWN * 2.6)
            s.play(FadeIn(coin_a), FadeIn(carol), run_time=1)
            s.play(
                as_anim(coin_a.animate.next_to(bob, LEFT, buff=0.3)),
                as_anim(coin_b.animate.next_to(carol, LEFT, buff=0.3)),
                run_time=2,
            )
            q_double = icons.question_bubble("¿Gasta dos veces?", theme.DANGER).scale(0.9)
            q_double.move_to(DOWN * 1.6)
            s.play(FadeIn(q_double, scale=1.2), run_time=1)
            s.play(Indicate(q_double, color=theme.DANGER), run_time=1.2)
