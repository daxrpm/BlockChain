"""S6: árbol de Merkle, manipulación que rompe la cadena, prueba de inclusión y escala log₂."""

import math

from manim import (
    DOWN,
    LEFT,
    RIGHT,
    UP,
    Create,
    FadeIn,
    FadeOut,
    Flash,
    Indicate,
    LaggedStart,
    Line,
    ReplacementTransform,
    Transform,
    VGroup,
)
from manim.utils.color import ParsableManimColor

from ledger_viz.domain.block import Block, find_broken_links
from ledger_viz.domain.hashing import short_hex
from ledger_viz.domain.merkle import merkle_levels, merkle_proof, verify_proof
from ledger_viz.scenes.narrator import Narrator
from ledger_viz.scenes.sections.chain import linked_chain_static
from ledger_viz.scenes.sections.common import Stage
from ledger_viz.story import (
    BLOCK_TXS,
    CHAIN,
    FOCUS_BLOCK,
    PROOF_INDEX,
    TAMPER_INDEX,
    TAMPERED_TX,
    short_tx,
)
from ledger_viz.viz import theme
from ledger_viz.viz.components import (
    as_anim,
    box,
    check,
    cross,
    hash_text,
    label,
    mono,
    phone,
    point,
)
from ledger_viz.viz.linked_view import short
from ledger_viz.viz.merkle_view import TreeView, build_tree, node_mob

STRIP_Y = 2.3
LEVEL_CUES = ("las hojas", "de dos en dos", "nivel por nivel", "la raíz")
TAMPER_CUES = ("cambia su hash", "el de su par", "hasta la raíz")


def _header_strip(root_text: str, color: ParsableManimColor) -> VGroup:
    frame = box(6.4, 0.55, color=theme.MUTED, stroke=2)
    name = label("Cabecera · Raíz de Merkle:", 0.36, color=theme.MUTED)
    value = mono(root_text, 0.42, color=color)
    content = VGroup(name, value).arrange(RIGHT, buff=0.25)
    group = VGroup(frame, content).move_to(point(0, STRIP_Y))
    content.move_to(frame)
    return group


def _path_indices(leaf: int, depth: int) -> list[int]:
    return [leaf >> level for level in range(depth)]


class MerkleSection:
    def __init__(self, stage: Stage, narrator: Narrator) -> None:
        self.stage, self.n, self.s = stage, narrator, stage.scene
        self.leaves = [tx.serialize() for tx in BLOCK_TXS]
        self.levels = merkle_levels(self.leaves)
        tampered = list(BLOCK_TXS)
        tampered[TAMPER_INDEX] = TAMPERED_TX
        self.tampered_levels = merkle_levels([tx.serialize() for tx in tampered])

    def run(self) -> None:
        self.n.start("S6")
        self.build()
        self.root()
        self.attack()
        self.broken_chain()
        self.proof()
        self.scale()

    def _level_anims(self, tree: TreeView, depth: int) -> list:
        if depth == 0:
            return [
                LaggedStart(*[Create(link) for link in tree.leaf_links], lag_ratio=0.05),
                LaggedStart(*[FadeIn(nd) for nd in tree.nodes[0]], lag_ratio=0.08),
            ]
        edges = [e for (d, _), e in tree.edges.items() if d == depth - 1]
        return [
            LaggedStart(*[Create(e) for e in edges], lag_ratio=0.05),
            LaggedStart(*[FadeIn(nd, scale=0.9) for nd in tree.nodes[depth]], lag_ratio=0.12),
        ]

    def build(self) -> None:
        s, n = self.s, self.n
        with n.beat("S6_1_construir"):
            self.stage.swap_title("Árbol de Merkle", "Un resumen de todas las transacciones")
            strip = _header_strip("????????", theme.MUTED)
            tree = build_tree(BLOCK_TXS)
            s.play(FadeIn(strip), run_time=0.6)
            n.cue("calculamos el hash de cada transacción")
            s.play(
                LaggedStart(*[FadeIn(t, shift=UP * 0.15) for t in tree.tx_labels], lag_ratio=0.08),
                run_time=1.2,
            )
            formula = label("cada nodo = H(izq ‖ der)", 0.36, color=theme.MUTED)
            formula.move_to(point(-4.6, 1.75))
            for depth, cue in enumerate(LEVEL_CUES):
                n.cue(cue)
                anims = self._level_anims(tree, depth)
                if depth == 1:
                    anims.append(FadeIn(formula))
                s.play(*anims, run_time=1.2)
            s.play(Flash(tree.node(3, 0), color=theme.ACCENT, flash_radius=0.9), run_time=0.8)
            self.tree, self.strip, self.formula = tree, strip, formula

    def root(self) -> None:
        s, n = self.s, self.n
        with n.beat("S6_2_raiz"):
            n.cue("impar")
            odd = label("nivel impar → se duplica el último", 0.36, color=theme.ACCENT)
            odd.move_to(self.formula, aligned_edge=LEFT)
            s.play(Transform(self.formula, odd), run_time=0.9)
            n.cue("esa raíz")
            root = self.tree.node(3, 0)
            flying = hash_text(self.levels[-1][0], 0.42, chars=8).move_to(root)
            target = _header_strip(short_hex(self.levels[-1][0], 8), theme.ACCENT)
            s.play(as_anim(flying.animate.move_to(target[1][1])), run_time=1.2)
            s.remove(flying)
            s.play(Transform(self.strip, target), run_time=0.4)
            n.cue("32 bytes")
            size = label("32 bytes", 0.34, color=theme.ACCENT, bold=True)
            size.next_to(self.strip, RIGHT, buff=0.25)
            s.play(FadeIn(size), run_time=0.6)
            n.cue("resume todas")
            s.play(Indicate(self.strip, color=theme.ACCENT, scale_factor=1.05), run_time=1.0)
            self.size = size

    def attack(self) -> None:
        s, n, tree = self.s, self.n, self.tree
        with n.beat("S6_3_atacante"):
            n.cue("seamos el atacante")
            attacker = label("atacante", 0.34, color=theme.DANGER, bold=True)
            old_label = tree.tx_labels[TAMPER_INDEX]
            attacker.next_to(old_label, DOWN, buff=0.08)
            s.play(FadeOut(self.formula), FadeOut(self.size), FadeIn(attacker, shift=UP * 0.1))
            n.cue("de 2 a 20")
            new_label = mono(short_tx(TAMPERED_TX), 0.36, color=theme.DANGER).move_to(old_label)
            s.play(Transform(old_label, new_label), run_time=0.8)
            path = _path_indices(TAMPER_INDEX, len(self.tampered_levels))
            groups = [[0], [1], [2, 3]]
            for cue, depths in zip(TAMPER_CUES, groups, strict=True):
                n.cue(cue)
                for depth in depths:
                    s.play(*self._redden(depth, path), run_time=0.6)
            n.cue("cambia la cabecera")
            new_strip = _header_strip(short_hex(self.tampered_levels[-1][0], 8), theme.DANGER)
            s.play(Transform(self.strip, new_strip), run_time=0.8)
            n.cue("el hash del bloque")
            tampered_block = self._tampered_block()
            block_hash = label(
                f"Hash del bloque: {short(tampered_block.hash)}",
                0.36,
                color=theme.DANGER,
                bold=True,
            ).next_to(self.strip, DOWN, buff=0.15)
            s.play(FadeIn(block_hash, shift=DOWN * 0.1), run_time=0.8)
            self.attacker, self.block_hash = attacker, block_hash

    def _redden(self, depth: int, path: list[int]) -> list:
        tree = self.tree
        index = path[depth]
        node = tree.node(depth, index)
        new_node = node_mob(self.tampered_levels[depth][index]).move_to(node)
        new_node[0].set_stroke(theme.DANGER)
        new_node[1].set_color(theme.DANGER)
        anims = [Transform(node, new_node)]
        if depth == 0:
            anims.append(as_anim(tree.leaf_links[index].animate.set_color(theme.DANGER)))
        else:
            edge = tree.edges[(depth - 1, path[depth - 1])]
            anims.append(as_anim(edge.animate.set_color(theme.DANGER)))
        return anims

    def _tampered_block(self) -> Block:
        return Block.tamper(CHAIN[FOCUS_BLOCK], index=TAMPER_INDEX, new_tx=TAMPERED_TX)

    def broken_chain(self) -> None:
        s, n = self.s, self.n
        with n.beat("S6_4_rotura"):
            n.cue("el bloque siguiente")
            tampered = self._tampered_block()
            chain = list(CHAIN)
            chain[FOCUS_BLOCK] = tampered
            first_broken = find_broken_links(chain)[0]
            blocks, pointers = linked_chain_static(CHAIN, colors=True)
            row = VGroup(*[b.group for b in blocks], *pointers)
            s.play(
                FadeOut(VGroup(self.tree.group, self.attacker, self.strip, self.block_hash)),
                run_time=0.7,
            )
            self.stage.swap_title("La cadena se rompe", "Un solo valor deja de coincidir")
            s.play(FadeIn(row), run_time=1.0)
            focus = blocks[FOCUS_BLOCK]
            new_hash = mono(short(tampered.hash), 0.38, color=theme.DANGER).move_to(
                focus.hash_value, aligned_edge=LEFT
            )
            s.play(
                as_anim(focus.frame.animate.set_stroke(theme.DANGER)),
                Transform(focus.hash_value, new_hash),
                run_time=1.0,
            )
            n.cue("ya no coincide")
            nxt = blocks[first_broken]
            neq = label("≠", 0.6, color=theme.DANGER, bold=True)
            neq.next_to(nxt.prev_value, RIGHT, buff=0.12)
            s.play(
                as_anim(nxt.prev_value.animate.set_color(theme.DANGER)),
                Indicate(nxt.prev_value, color=theme.DANGER, scale_factor=1.2),
                FadeIn(neq, scale=1.4),
                run_time=1.0,
            )
            n.cue("la cadena se rompe")
            link = pointers[first_broken - 1]
            points = link.get_points()
            start_pt, end_pt = points[0], points[-1]
            mid = link.point_from_proportion(0.5)
            spark = cross(0.4).move_to(mid)
            halves = VGroup(
                Line(start_pt, mid + (start_pt - mid) * 0.15, color=theme.DANGER, stroke_width=4),
                Line(mid + (end_pt - mid) * 0.15, end_pt, color=theme.DANGER, stroke_width=4),
            )
            s.play(ReplacementTransform(link, halves), FadeIn(spark, scale=1.6), run_time=0.9)
            n.cue("todos los siguientes")
            later = VGroup(*[b.frame for b in blocks[first_broken:]], *pointers[first_broken:])
            s.play(as_anim(later.animate.set_stroke(theme.DANGER)), run_time=1.0)
            n.cue("evidente")
            caption = VGroup(
                label("La alteración es ", 0.42),
                label("evidente", 0.42, color=theme.ACCENT, bold=True),
                label(", no imposible → lo impracticable lo pone el consenso", 0.42),
            ).arrange(RIGHT, buff=0.08)
            caption.to_edge(DOWN, buff=0.6)
            s.play(FadeIn(caption, shift=UP * 0.2), run_time=1.0)

    def proof(self) -> None:
        s, n = self.s, self.n
        with n.beat("S6_5_prueba"):
            self.stage.swap_title("Prueba de inclusión", "¿Está mi pago en el bloque?")
            root = self.levels[-1][0]
            strip = _header_strip(short_hex(root, 8), theme.ACCENT)
            tree = build_tree(BLOCK_TXS)
            s.play(FadeIn(strip), FadeIn(tree.group), run_time=1.0)
            n.cue("dave desde su celular")
            device = phone(0.9).move_to(LEFT * 5.9 + UP * 1.55)
            ask = label(f"Dave: ¿«{short_tx(BLOCK_TXS[PROOF_INDEX])}» está?", 0.34)
            ask.next_to(device, RIGHT, buff=0.2).shift(UP * 0.25)
            s.play(FadeIn(device), FadeIn(ask), run_time=0.8)
            leaf_label = tree.tx_labels[PROOF_INDEX]
            s.play(as_anim(leaf_label.animate.set_color(theme.ACCENT).scale(1.15)), run_time=0.6)

            n.cue("tres hashes")
            proof = merkle_proof(self.leaves, PROOF_INDEX)
            path = _path_indices(PROOF_INDEX, len(self.levels))
            badges = VGroup()
            for depth, step in enumerate(proof):
                sibling_index = path[depth] ^ 1
                if short_hex(step.sibling, 8) != short_hex(self.levels[depth][sibling_index], 8):
                    msg = "La prueba del dominio no coincide con el árbol dibujado"
                    raise RuntimeError(msg)
                sibling = tree.node(depth, sibling_index)
                dot = box(0.36, 0.36, color=theme.OK, fill=theme.OK)
                number = label(str(depth + 1), 0.32, color=theme.BG, bold=True).move_to(dot)
                badge = VGroup(dot, number).next_to(sibling, UP, buff=0.05).shift(RIGHT * 0.5)
                badges.add(badge)
                s.play(
                    as_anim(sibling[0].animate.set_stroke(theme.OK, width=4)),
                    FadeIn(badge),
                    run_time=0.7,
                )
            n.cue("recalcula la raíz")
            for depth, index in enumerate(path):
                node = tree.node(depth, index)
                s.play(as_anim(node[0].animate.set_stroke(theme.ACCENT, width=4)), run_time=0.4)
            n.cue("la compara con la cabecera")
            ok = verify_proof(self.leaves[PROOF_INDEX], proof, root)
            mark = check(0.45) if ok else cross(0.45)
            mark.next_to(tree.node(3, 0), RIGHT, buff=0.2)
            verdict = label(
                f"coincide: {len(proof)} hashes bastan", 0.4, color=theme.OK, bold=True
            ).next_to(mark, RIGHT, buff=0.2)
            s.play(FadeIn(mark, scale=1.4), FadeIn(verdict), Indicate(strip, color=theme.OK))
            self.proof_len = len(proof)
            self.proof_view = VGroup(tree.group, badges, mark, verdict, strip, device, ask)

    def scale(self) -> None:
        s, n = self.s, self.n
        with n.beat("S6_6_escala"):
            sizes = (len(BLOCK_TXS), 4096, 1_000_000)
            rows = VGroup()
            for size in sizes:
                k = self.proof_len if size == len(BLOCK_TXS) else math.ceil(math.log2(size))
                rows.add(
                    VGroup(
                        mono(f"{size:,}".replace(",", " "), 0.62, color=theme.TEXT),
                        label("transacciones  →", 0.44, color=theme.MUTED),
                        mono(f"{k}", 0.62, color=theme.ACCENT),
                        label("hashes", 0.44, color=theme.MUTED),
                    ).arrange(RIGHT, buff=0.3)
                )
            rows.arrange(DOWN, buff=0.45, aligned_edge=RIGHT).move_to(UP * 0.2)
            s.play(FadeOut(self.proof_view), run_time=0.7)
            n.cue("con ocho transacciones")
            s.play(FadeIn(rows[0], shift=RIGHT * 0.3), run_time=0.8)
            n.cue("con un millón")
            s.play(
                LaggedStart(*[FadeIn(r, shift=RIGHT * 0.3) for r in rows[1:]], lag_ratio=0.5),
                run_time=1.4,
            )
            law = label("log₂ n", 0.5, color=theme.ACCENT, bold=True).next_to(rows, RIGHT, buff=0.6)
            s.play(FadeIn(law), run_time=0.6)
            n.cue("verificación simplificada de pagos")
            caption = label("SPV: billeteras ligeras que solo guardan las cabeceras", 0.42).to_edge(
                DOWN, buff=0.7
            )
            s.play(FadeIn(caption, shift=UP * 0.2), run_time=1.0)
