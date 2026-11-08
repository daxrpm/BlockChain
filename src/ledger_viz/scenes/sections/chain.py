"""S4: la cadena del Canva se convierte en lo que es, una lista enlazada por punteros de hash."""

from collections.abc import Sequence

from manim import (
    DOWN,
    LEFT,
    RIGHT,
    UP,
    Arrow,
    Create,
    CurvedArrow,
    FadeIn,
    FadeOut,
    GrowArrow,
    Indicate,
    LaggedStart,
    ReplacementTransform,
    Transform,
    VGroup,
)

from ledger_viz.domain.block import Block
from ledger_viz.scenes.narrator import Narrator
from ledger_viz.scenes.sections.common import Stage
from ledger_viz.story import CHAIN, FOCUS_BLOCK
from ledger_viz.viz import theme
from ledger_viz.viz.chain_view import build_chain_view
from ledger_viz.viz.components import as_anim, label, point
from ledger_viz.viz.linked_view import (
    LinkedBlock,
    build_linked_view,
    copy_arrow,
    pointer,
    prev_text,
)

SHOWN = 4  # bloques visibles al transformar; el 5.º entra en «génesis y crecimiento»
PAIR_COLORS = (theme.OK, "#5AB0FF", "#C792EA", "#FF9F43")


class ChainSection:
    def __init__(self, stage: Stage, narrator: Narrator) -> None:
        self.stage, self.n, self.s = stage, narrator, stage.scene
        self.blocks = build_linked_view(CHAIN, prev_known=False)
        self.pointers: list[CurvedArrow] = []

    def run(self) -> None:
        self.n.start("S4")
        self.drawing()
        self.structure()
        self.hash_pointer()
        self.genesis()

    def drawing(self) -> None:
        s, n = self.s, self.n
        with n.beat("S4_1_dibujo"):
            self.stage.swap_title("Blockchain", "¿Qué es y cómo se organiza?")
            n.cue("esta imagen")
            zig = build_chain_view(CHAIN)
            s.play(Create(zig.entry), run_time=0.5)
            for i, cube in enumerate(zig.cubes):
                anims = [Create(cube), FadeIn(zig.prevs[i], shift=UP * 0.1)]
                if i:
                    anims.insert(0, Create(zig.links[i - 1]))
                s.play(*anims, run_time=0.5)
            caption = label("Cada bloque referencia criptográficamente al anterior.", 0.42)
            caption.to_edge(DOWN, buff=0.4)
            s.play(FadeIn(caption, shift=UP * 0.2), run_time=0.8)
            n.cue("esa línea")
            question = label("?", 1.0, color=theme.ACCENT, bold=True)
            question.move_to(zig.links[1].get_center() + UP * 0.6 + RIGHT * 0.3)
            s.play(
                LaggedStart(
                    *[Indicate(lk, color=theme.TEXT, scale_factor=1.1) for lk in zig.links]
                ),
                FadeIn(question, scale=1.5),
                run_time=1.6,
            )
            self.zig, self.zig_extra = zig, VGroup(caption, question)

    def structure(self) -> None:
        s, n, blocks = self.s, self.n, self.blocks
        with n.beat("S4_2_estructura"):
            n.cue("estructura de datos")
            new_title_sub = "La línea, vista como estructura de datos"
            zig = self.zig
            s.play(
                FadeOut(self.zig_extra),
                FadeOut(VGroup(zig.entry, *zig.links, *zig.hashes, *zig.prevs, *zig.cubes[SHOWN:])),
                run_time=0.8,
            )
            self.stage.swap_title("Blockchain", new_title_sub, keep=zig.cubes[:SHOWN])
            s.play(
                *[ReplacementTransform(zig.cubes[i], blocks[i].frame) for i in range(SHOWN)],
                run_time=1.4,
            )
            s.play(
                LaggedStart(*[FadeIn(b.title) for b in blocks[:SHOWN]], lag_ratio=0.15),
                run_time=0.8,
            )
            n.cue("su propio hash")
            s.play(
                *[FadeIn(VGroup(b.hash_label, b.hash_value)) for b in blocks[:SHOWN]], run_time=1.0
            )
            n.cue("hash previo")
            s.play(
                *[FadeIn(VGroup(b.prev_label, b.prev_value)) for b in blocks[:SHOWN]], run_time=1.0
            )
            n.cue("se copia")
            self.copies: list[Arrow] = []
            self._copy_hashes([(i, i + 1) for i in range(SHOWN - 1)])

    def _copy_hashes(self, pairs: list[tuple[int, int]]) -> None:
        """El hash de cada bloque viaja al «Hash previo» del siguiente (en paralelo)."""
        s = self.s
        arrows, flying, knowns, dsts = [], [], [], []
        for src_i, dst_i in pairs:
            src, dst = self.blocks[src_i], self.blocks[dst_i]
            arrows.append(copy_arrow(src, dst))
            flying.append(src.hash_value.copy())
            knowns.append(
                prev_text(CHAIN[dst_i], known=True).move_to(dst.prev_value, aligned_edge=LEFT)
            )
            dsts.append(dst)
        s.play(*[GrowArrow(a) for a in arrows], run_time=0.6)
        s.play(
            *[as_anim(f.animate.move_to(k)) for f, k in zip(flying, knowns, strict=True)],
            run_time=1.0,
        )
        s.remove(*flying)
        s.play(
            *[Transform(d.prev_value, k) for d, k in zip(dsts, knowns, strict=True)], run_time=0.4
        )
        self.copies.extend(arrows)

    def hash_pointer(self) -> None:
        s, n, blocks = self.s, self.n, self.blocks
        with n.beat("S4_3_puntero"):
            n.cue("no es un cable")
            s.play(*[FadeOut(a) for a in self.copies], run_time=0.6)
            n.cue("puntero de hash")
            self.pointers = [pointer(blocks[i], blocks[i + 1]) for i in range(SHOWN - 1)]
            tags = VGroup(
                *[
                    label("apunta a", 0.26, color=theme.MUTED).next_to(p, UP, buff=0.04)
                    for p in self.pointers
                ]
            )
            s.play(LaggedStart(*[Create(p) for p in self.pointers], lag_ratio=0.25), run_time=1.6)
            s.play(FadeIn(tags), run_time=0.6)
            self.tags = tags
            n.cue("dónde")
            parts = [
                label("puntero de hash =", 0.44, bold=True),
                label("dónde está", 0.44, color=theme.ACCENT, bold=True),
                label("+", 0.44),
                label("cómo era", 0.44, color=theme.ACCENT, bold=True),
            ]
            eq = VGroup(*parts).arrange(RIGHT, buff=0.2).move_to(DOWN * 2.6)
            s.play(FadeIn(VGroup(*parts[:2]), shift=UP * 0.2), run_time=0.8)
            n.cue("cómo era exactamente")
            s.play(FadeIn(VGroup(*parts[2:]), shift=UP * 0.2), run_time=0.8)
            n.cue("ya no coincide")
            for i in range(SHOWN - 1):
                color = PAIR_COLORS[i]
                s.play(
                    as_anim(blocks[i].hash_value.animate.set_color(color)),
                    as_anim(blocks[i + 1].prev_value.animate.set_color(color)),
                    run_time=0.5,
                )
            self.equation = eq

    def genesis(self) -> None:
        s, n, blocks = self.s, self.n, self.blocks
        with n.beat("S4_4_genesis"):
            n.cue("todo ceros")
            zeros = prev_text(CHAIN[0], known=True).move_to(blocks[0].prev_value, aligned_edge=LEFT)
            zeros.set_color(theme.ACCENT)
            s.play(
                FadeOut(self.equation),
                Transform(blocks[0].prev_value, zeros),
                Indicate(blocks[0].prev_label, color=theme.ACCENT),
                run_time=1.0,
            )
            n.cue("bloque génesis")
            genesis_title = label("Génesis", 0.36, color=theme.ACCENT, bold=True).move_to(
                blocks[0].title
            )
            fixed = label("fijado en el software", 0.28, color=theme.MUTED)
            fixed.next_to(blocks[0].frame, DOWN, buff=0.15)
            s.play(Transform(blocks[0].title, genesis_title), FadeIn(fixed), run_time=1.0)
            n.cue("solo crece")
            new = blocks[SHOWN]
            s.play(FadeIn(VGroup(new.frame, new.title), shift=LEFT * 0.6), run_time=0.9)
            s.play(FadeIn(VGroup(new.prev_label, new.prev_value, new.hash_label, new.hash_value)))
            self.copies = []
            self._copy_hashes([(SHOWN - 1, SHOWN)])
            last = pointer(blocks[SHOWN - 1], new)
            color = PAIR_COLORS[SHOWN - 1]
            s.play(
                FadeOut(self.copies[-1]),
                Create(last),
                as_anim(blocks[SHOWN - 1].hash_value.animate.set_color(color)),
                as_anim(new.prev_value.animate.set_color(color)),
                run_time=0.8,
            )
            self.pointers.append(last)
            grow = label("la cadena solo crece  →", 0.42, color=theme.ACCENT, bold=True)
            grow.move_to(point(2.0, -2.6))
            s.play(FadeIn(grow, shift=RIGHT * 0.3), run_time=0.8)
            focus = blocks[FOCUS_BLOCK].group
            self.stage.focus = focus
            self.fixed, self.grow = fixed, grow


def linked_chain_static(
    chain: Sequence[Block], *, colors: bool = False
) -> tuple[list[LinkedBlock], list[CurvedArrow]]:
    """Fila completa (para reutilizar en la manipulación de S6)."""
    blocks = build_linked_view(chain)
    pointers = [pointer(blocks[i], blocks[i + 1]) for i in range(len(blocks) - 1)]
    if colors:
        for i in range(len(blocks) - 1):
            blocks[i].hash_value.set_color(PAIR_COLORS[i % len(PAIR_COLORS)])
            blocks[i + 1].prev_value.set_color(PAIR_COLORS[i % len(PAIR_COLORS)])
    return blocks, pointers
