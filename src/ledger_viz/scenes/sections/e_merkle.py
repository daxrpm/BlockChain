"""E1–E3: construir el árbol de Merkle, manipular una transacción y probar inclusión."""

import math

import numpy as np
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
from ledger_viz.domain.transaction import Transaction
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
from ledger_viz.viz.chain_view import build_chain_view
from ledger_viz.viz.components import (
    box,
    check,
    cross,
    hash_text,
    label,
    mono,
    phone,
    point,
)
from ledger_viz.viz.merkle_view import TreeView, build_tree, node_mob

STRIP_Y = 2.3


def _header_strip(root_text: str, color: ParsableManimColor) -> VGroup:
    frame = box(6.4, 0.55, color=theme.MUTED, stroke=2)
    name = label("Cabecera · Raíz de Merkle:", 0.36, color=theme.MUTED)
    value = mono(root_text, 0.42, color=color)
    content = VGroup(name, value).arrange(RIGHT, buff=0.25)
    group = VGroup(frame, content).move_to(point(0, STRIP_Y, 0))
    content.move_to(frame)
    return group


def _path_indices(leaf: int, depth: int) -> list[int]:
    return [leaf >> level for level in range(depth)]


class MerkleSection:
    def __init__(self, stage: Stage) -> None:
        self.stage = stage
        self.leaves = [tx.serialize() for tx in BLOCK_TXS]
        self.levels = merkle_levels(self.leaves)

    def run(self) -> None:
        self.e1_build()
        self.e2_tamper()
        self.e3_proof()

    def _reveal_tree(self, tree: TreeView, *, slow: bool) -> None:
        s = self.stage.scene
        speed = 1.0 if slow else 0.45
        s.play(
            LaggedStart(*[FadeIn(t, shift=UP * 0.15) for t in tree.tx_labels], lag_ratio=0.06),
            run_time=speed,
        )
        s.play(
            LaggedStart(*[Create(link) for link in tree.leaf_links], lag_ratio=0.05),
            LaggedStart(*[FadeIn(n) for n in tree.nodes[0]], lag_ratio=0.06),
            run_time=speed * 1.2,
        )
        for depth in range(1, len(tree.nodes)):
            edges = [e for (d, _), e in tree.edges.items() if d == depth - 1]
            s.play(
                LaggedStart(*[Create(e) for e in edges], lag_ratio=0.05),
                LaggedStart(*[FadeIn(n, scale=0.9) for n in tree.nodes[depth]], lag_ratio=0.1),
                run_time=speed,
            )

    def e1_build(self) -> None:
        s = self.stage.scene
        s.next_section("E1_construir_arbol")
        self.stage.swap_title("Árbol de Merkle", "32 bytes que resumen todas las transacciones")
        strip = _header_strip("????????", theme.MUTED)
        s.play(FadeIn(strip), run_time=0.5)

        tree = build_tree(BLOCK_TXS)
        formula = label("cada nodo = SHA-256²(izq ‖ der)", 0.34, color=theme.MUTED)
        formula.move_to(point(-4.6, 1.75))
        self._reveal_tree(tree, slow=True)
        s.play(FadeIn(formula), run_time=0.4)

        root = tree.node(3, 0)
        s.play(Flash(root, color=theme.ACCENT, flash_radius=0.9), run_time=0.7)
        root_copy = hash_text(self.levels[-1][0], 0.42, chars=8).move_to(root)
        target = _header_strip(short_hex(self.levels[-1][0], 8), theme.ACCENT)
        s.play(root_copy.animate.move_to(target[1][1]), run_time=0.9)
        s.remove(root_copy)
        s.play(Transform(strip, target), run_time=0.3)
        self.tree, self.strip, self.formula = tree, strip, formula
        s.wait(1.2)

    def e2_tamper(self) -> None:
        s = self.stage.scene
        s.next_section("E2_manipulacion")
        tree = self.tree
        tampered_txs = list(BLOCK_TXS)
        tampered_txs[TAMPER_INDEX] = TAMPERED_TX
        new_levels = merkle_levels([tx.serialize() for tx in tampered_txs])

        attacker = label("atacante", 0.34, color=theme.DANGER, bold=True)
        old_label = tree.tx_labels[TAMPER_INDEX]
        attacker.next_to(old_label, DOWN, buff=0.08)
        new_label = mono(short_tx(TAMPERED_TX), 0.36, color=theme.DANGER).move_to(old_label)
        s.play(FadeOut(self.formula), FadeIn(attacker, shift=UP * 0.1), run_time=0.5)
        s.play(Transform(old_label, new_label), run_time=0.7)
        self.attacker = attacker

        path = _path_indices(TAMPER_INDEX, len(new_levels))
        for depth, index in enumerate(path):
            node = tree.node(depth, index)
            new_node = node_mob(new_levels[depth][index]).move_to(node)
            new_node[0].set_stroke(theme.DANGER)
            new_node[1].set_color(theme.DANGER)
            anims = [Transform(node, new_node)]
            if depth == 0:
                anims.append(tree.leaf_links[index].animate.set_color(theme.DANGER))
            else:
                child = path[depth - 1]
                anims.append(tree.edges[(depth - 1, child)].animate.set_color(theme.DANGER))
            s.play(*anims, run_time=0.55)
        new_strip = _header_strip(short_hex(new_levels[-1][0], 8), theme.DANGER)
        s.play(Transform(self.strip, new_strip), run_time=0.6)
        s.wait(0.6)

        self._show_broken_chain(tampered_txs)

    def _show_broken_chain(self, tampered_txs: list[Transaction]) -> None:
        s = self.stage.scene
        tampered_block = Block.tamper(
            CHAIN[FOCUS_BLOCK], index=TAMPER_INDEX, new_tx=tampered_txs[TAMPER_INDEX]
        )
        chain = list(CHAIN)
        chain[FOCUS_BLOCK] = tampered_block
        broken = find_broken_links(chain)

        view = build_chain_view(CHAIN)
        s.play(FadeOut(self.tree.group), FadeOut(self.attacker), FadeOut(self.strip), run_time=0.6)
        s.play(FadeIn(view.group), run_time=0.9)

        focus = view.cubes[FOCUS_BLOCK]
        old_hash = view.hashes[FOCUS_BLOCK]
        new_hash = mono(
            f"Hash: {short_hex(tampered_block.hash)}", 0.36, color=theme.DANGER
        ).move_to(old_hash)
        s.play(focus.animate.set_stroke(theme.DANGER), Transform(old_hash, new_hash))
        s.wait(0.4)

        first_broken = broken[0]
        s.play(
            Indicate(view.prevs[first_broken], color=theme.DANGER, scale_factor=1.15),
            view.prevs[first_broken].animate.set_color(theme.DANGER),
        )
        link = view.links[first_broken - 1]
        start_pt, end_pt = link.get_start(), link.get_end()
        mid = (start_pt + end_pt) / 2
        gap = (end_pt - start_pt) / float(np.linalg.norm(end_pt - start_pt)) * 0.25
        halves = VGroup(
            Line(start_pt, mid - gap, color=theme.DANGER, stroke_width=3),
            Line(mid + gap, end_pt, color=theme.DANGER, stroke_width=3),
        )
        spark = cross(0.35).move_to(mid)
        s.play(ReplacementTransform(link, halves), FadeIn(spark, scale=1.6), run_time=0.6)
        later = VGroup(*view.cubes[first_broken:], *view.links[first_broken:])
        s.play(later.animate.set_color(theme.DANGER), run_time=0.7)

        caption = (
            VGroup(
                label("La alteración es ", 0.42),
                label("evidente", 0.42, color=theme.ACCENT, bold=True),
                label(", no imposible → eso lo resuelve el consenso", 0.42),
            )
            .arrange(RIGHT, buff=0.08)
            .to_edge(DOWN, buff=0.5)
        )
        s.play(FadeIn(caption, shift=UP * 0.2))
        s.wait(1.5)

    def e3_proof(self) -> None:
        s = self.stage.scene
        s.next_section("E3_prueba_inclusion")
        self.stage.swap_title("Prueba de inclusión", "¿Está mi pago en el bloque?")
        root = self.levels[-1][0]
        strip = _header_strip(short_hex(root, 8), theme.ACCENT)
        tree = build_tree(BLOCK_TXS)
        device = phone(0.9).move_to(LEFT * 5.9 + UP * 1.55)
        ask = label(f"Dave: ¿«{short_tx(BLOCK_TXS[PROOF_INDEX])}» está?", 0.34)
        ask.next_to(device, RIGHT, buff=0.2).shift(UP * 0.25)
        s.play(FadeIn(strip), FadeIn(tree.group), run_time=0.9)
        s.play(FadeIn(device), FadeIn(ask), run_time=0.6)

        leaf_label = tree.tx_labels[PROOF_INDEX]
        s.play(leaf_label.animate.set_color(theme.ACCENT).scale(1.15), run_time=0.5)

        proof = merkle_proof(self.leaves, PROOF_INDEX)
        path = _path_indices(PROOF_INDEX, len(self.levels))
        badges = VGroup()
        for depth, step in enumerate(proof):
            sibling_index = path[depth] ^ 1
            sibling = tree.node(depth, sibling_index)
            badge = label(str(depth + 1), 0.32, color=theme.BG, bold=True)
            dot = box(0.36, 0.36, color=theme.OK, fill=theme.OK)
            badge_group = (
                VGroup(dot, badge.move_to(dot)).next_to(sibling, UP, buff=0.05).shift(RIGHT * 0.5)
            )
            badges.add(badge_group)
            if short_hex(step.sibling, 8) != short_hex(self.levels[depth][sibling_index], 8):
                msg = "La prueba del dominio no coincide con el árbol dibujado"
                raise RuntimeError(msg)
            s.play(
                sibling[0].animate.set_stroke(theme.OK, width=4), FadeIn(badge_group), run_time=0.55
            )

        for depth, index in enumerate(path):
            node = tree.node(depth, index)
            s.play(node[0].animate.set_stroke(theme.ACCENT, width=4), run_time=0.35)
        ok = verify_proof(self.leaves[PROOF_INDEX], proof, root)
        mark = check(0.45) if ok else cross(0.45)
        mark.next_to(tree.node(3, 0), RIGHT, buff=0.2)
        verdict = label(
            f"{len(proof)} hashes bastan para comprobarlo", 0.4, color=theme.OK, bold=True
        ).next_to(mark, RIGHT, buff=0.2)
        s.play(FadeIn(mark, scale=1.4), FadeIn(verdict), run_time=0.7)
        s.wait(1.2)

        sizes = (len(BLOCK_TXS), 4096, 1_000_000)
        rows = VGroup()
        for n in sizes:
            k = len(proof) if n == len(BLOCK_TXS) else math.ceil(math.log2(n))
            rows.add(
                VGroup(
                    mono(f"{n:,}".replace(",", " "), 0.62, color=theme.TEXT),
                    label("transacciones  →", 0.44, color=theme.MUTED),
                    mono(f"{k}", 0.62, color=theme.ACCENT),
                    label("hashes", 0.44, color=theme.MUTED),
                ).arrange(RIGHT, buff=0.3)
            )
        rows.arrange(DOWN, buff=0.45, aligned_edge=RIGHT).move_to(DOWN * 0.2)
        s.play(
            FadeOut(tree.group),
            FadeOut(badges),
            FadeOut(mark),
            FadeOut(verdict),
            FadeOut(strip),
            run_time=0.6,
        )
        s.play(
            LaggedStart(*[FadeIn(r, shift=RIGHT * 0.3) for r in rows], lag_ratio=0.35), run_time=1.5
        )
        caption = label(
            "Por eso una billetera en el celular solo guarda cabeceras (SPV)", 0.42
        ).to_edge(DOWN, buff=0.45)
        s.play(FadeIn(caption, shift=UP * 0.2))
        s.wait(2)
