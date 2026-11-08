"""S0 y S7: puente desde criptografía (hoja de ruta + tesis) y cierre con relevo al consenso."""

import itertools

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
    Line,
    Text,
    VGroup,
)
from manim.utils.color import ParsableManimColor

from ledger_viz.scenes.intro.narrator import yellow_card
from ledger_viz.scenes.narrator import Narrator
from ledger_viz.scenes.sections.common import Stage
from ledger_viz.viz import icons, theme
from ledger_viz.viz.components import as_anim, box, label, notebook, point, wire_cube

THESIS = "Un blockchain es un cuaderno al que solo se puede agregar: cualquier alteración se nota"


def thesis_text(size: float = 0.42) -> Text:
    accent = theme.ACCENT.to_hex()
    return Text(
        THESIS,
        font=theme.FONT_SANS,
        color=theme.TEXT,
        t2c={"solo se puede agregar": accent, "cualquier alteración se nota": accent},
        t2w={"solo se puede agregar": "BOLD", "cualquier alteración se nota": "BOLD"},
    ).scale(size)


def mini_tree(color: ParsableManimColor = theme.TEXT) -> VGroup:
    """Ícono de árbol binario (3 niveles) para la hoja de ruta y el resumen."""
    dots = VGroup()
    edges = VGroup()
    levels = [[0.0], [-0.4, 0.4], [-0.6, -0.2, 0.2, 0.6]]
    for depth, xs in enumerate(levels):
        for x in xs:
            dots.add(
                box(0.22, 0.16, color=color, stroke=2.5).move_to(point(x, 0.45 - depth * 0.45))
            )
    for depth in range(2):
        parents = [d for d in dots if abs(d.get_y() - (0.45 - depth * 0.45)) < 1e-6]
        children = [d for d in dots if abs(d.get_y() - (0.45 - (depth + 1) * 0.45)) < 1e-6]
        for i, child in enumerate(children):
            edges.add(
                Line(child.get_top(), parents[i // 2].get_bottom(), color=color).set_stroke(
                    width=2.5
                )
            )
    return VGroup(edges, dots)


def framed(mob: VGroup | Text, color: ParsableManimColor = theme.ACCENT) -> VGroup:
    frame = box(mob.width + 0.6, mob.height + 0.4, color=color)
    return VGroup(frame, mob.move_to(frame))


class BridgeSection:
    """S0: arranca justo después de criptografía."""

    def __init__(self, stage: Stage, narrator: Narrator) -> None:
        self.stage, self.n, self.s = stage, narrator, stage.scene

    def run(self) -> None:
        s, n = self.s, self.n
        n.start("S0")
        with n.beat("S0_1_puente"):
            s.play(FadeIn(self.stage.title, shift=DOWN * 0.2), run_time=1.2)
            n.cue("el hash")
            hash_card = yellow_card(icons.fingerprint(), "Hash", caption="huella digital")
            hash_card.scale(0.85).move_to(point(-4.4, -0.3))
            s.play(FadeIn(hash_card, shift=UP * 0.3), run_time=1.0)
            n.cue("la firma digital")
            sign_card = yellow_card(icons.pen(), "Firma", caption="quién autorizó")
            sign_card.scale(0.85).move_to(point(-1.2, -0.3))
            s.play(FadeIn(sign_card, shift=UP * 0.3), run_time=1.0)
            n.cue("dónde se usan")
            cube = wire_cube(1.8).move_to(point(3.9, -0.3))
            mark = label("?", 1.2, color=theme.ACCENT, bold=True).move_to(cube)
            s.play(Create(cube), FadeIn(mark, scale=0.5), run_time=1.2)
            n.cue("qué guarda")
            s.play(
                as_anim(hash_card.animate.scale(0.35).move_to(cube).set_opacity(0)),
                as_anim(sign_card.animate.scale(0.35).move_to(cube).set_opacity(0)),
                run_time=1.4,
            )
            s.play(Indicate(VGroup(cube, mark), color=theme.ACCENT, scale_factor=1.12), run_time=1)
            self.cube, self.mark = cube, mark
            s.remove(hash_card, sign_card)

        with n.beat("S0_2_ruta"):
            steps = VGroup(
                *[
                    VGroup(icon, label(name, 0.42, bold=True)).arrange(DOWN, buff=0.25)
                    for icon, name in (
                        (notebook(1.1, 1.2, title=""), "Ledger"),
                        (icons.document(), "Transacción"),
                        (wire_cube(1.0), "Bloque"),
                        (mini_tree(), "Árbol de Merkle"),
                    )
                ]
            )
            for st in steps:
                st[0].scale_to_fit_height(1.15)
            steps.arrange(RIGHT, buff=1.0).move_to(UP * 0.35)
            numbers = VGroup(
                *[
                    label(str(i), 0.36, color=theme.MUTED, bold=True).next_to(st, UP, buff=0.2)
                    for i, st in enumerate(steps, start=1)
                ]
            )
            arrows = [
                Arrow(a.get_right(), b.get_left(), color=theme.MUTED, buff=0.15, stroke_width=3)
                for a, b in itertools.pairwise(steps)
            ]
            s.play(FadeOut(self.cube), FadeOut(self.mark), run_time=0.6)
            for i, word in enumerate(("ledger", "transacción", "bloque", "árbol de merkle")):
                n.cue(word)
                anims = [FadeIn(steps[i], shift=UP * 0.2), FadeIn(numbers[i])]
                if i:
                    anims.append(GrowArrow(arrows[i - 1]))
                s.play(*anims, run_time=0.8)
            n.cue("quédense con esta idea")
            thesis = framed(thesis_text(0.4)).move_to(DOWN * 2.3)
            s.play(FadeIn(thesis, shift=UP * 0.2), run_time=1.2)
            n.cue("cualquier alteración")
            s.play(Indicate(thesis[1], color=theme.ACCENT, scale_factor=1.04), run_time=1.2)


class ClosingSection:
    """S7: resumen del viaje y relevo hacia consenso."""

    def __init__(self, stage: Stage, narrator: Narrator) -> None:
        self.stage, self.n, self.s = stage, narrator, stage.scene

    def run(self) -> None:
        s, n = self.s, self.n
        n.start("S7")
        with n.beat("S7_1_resumen"):
            self.stage.swap_title("En resumen", "De una línea del cuaderno a la cadena")
            chain_icon = VGroup(
                *[box(0.45, 0.45, color=theme.TEXT, stroke=2.5) for _ in range(3)]
            ).arrange(RIGHT, buff=0.25)
            chain_icon.add(
                *[
                    Arrow(
                        b.get_left(), a.get_right(), buff=0.02, color=theme.ACCENT, stroke_width=3
                    )
                    for a, b in itertools.pairwise(chain_icon)
                ]
            )
            header_icon = VGroup(box(1.2, 0.9, color=theme.TEXT, stroke=2.5))
            header_icon.add(
                *[
                    Line(LEFT * 0.4, RIGHT * 0.4, color=theme.MUTED, stroke_width=3).shift(UP * y)
                    for y in (0.2, 0.0, -0.2)
                ]
            )
            items = [
                (icons.document(), "Transacción", "firmada · ID = hash", "firmadas"),
                (wire_cube(1.0), "Bloque", "lote de transacciones", "bloques"),
                (mini_tree(), "Merkle", "resume el cuerpo", "merkle"),
                (header_icon, "Cabecera", "hash previo + raíz", "la cabecera"),
                (chain_icon, "Cadena", "hash → siguiente bloque", "en el siguiente bloque"),
            ]
            cols = VGroup()
            for icon, name, desc, _ in items:
                icon.scale_to_fit_height(min(1.0, icon.height))
                if icon.width > 1.6:
                    icon.scale_to_fit_width(1.6)
                cols.add(
                    VGroup(
                        icon,
                        label(name, 0.4, color=theme.ACCENT, bold=True),
                        label(desc, 0.28, color=theme.MUTED),
                    ).arrange(DOWN, buff=0.22)
                )
            cols.arrange(RIGHT, buff=0.75, aligned_edge=UP).move_to(UP * 0.1)
            links = [
                Arrow(
                    a[0].get_right(),
                    point(b[0].get_left()[0], a[0].get_y()),
                    color=theme.MUTED,
                    buff=0.12,
                    stroke_width=3,
                )
                for a, b in itertools.pairwise(cols)
            ]
            for i, (_, _, _, word) in enumerate(items):
                n.cue(word)
                anims = [FadeIn(cols[i], shift=UP * 0.2)]
                if i:
                    anims.append(GrowArrow(links[i - 1]))
                s.play(*anims, run_time=0.9)
            self.summary = VGroup(cols, *links)

        with n.beat("S7_2_tesis"):
            n.cue("un blockchain es un cuaderno")
            thesis = framed(thesis_text(0.4)).move_to(DOWN * 1.7)
            s.play(FadeIn(thesis, shift=UP * 0.2), run_time=1.2)
            n.cue("quién decide")
            newcomer = wire_cube(0.7).move_to(point(7.6, -3.0))
            ask = label("?", 0.7, color=theme.ACCENT, bold=True)
            s.play(
                as_anim(self.summary.animate.shift(UP * 0.4)),
                as_anim(newcomer.animate.move_to(point(3.2, -3.0))),
                run_time=1.2,
            )
            ask.next_to(newcomer, RIGHT, buff=0.2)
            handoff = label("¿quién decide?  →  consenso", 0.42, color=theme.ACCENT, bold=True)
            handoff.next_to(newcomer, LEFT, buff=0.5)
            s.play(FadeIn(ask, scale=1.4), FadeIn(handoff, shift=RIGHT * 0.2), run_time=1.0)
