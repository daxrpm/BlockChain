"""Vista Manim de un árbol de Merkle construido con los hashes reales del dominio."""

from collections.abc import Sequence
from dataclasses import dataclass

import numpy as np
from manim import DOWN, UP, Line, Text, VGroup

from ledger_viz.domain.merkle import merkle_levels
from ledger_viz.domain.transaction import Transaction
from ledger_viz.story import short_tx
from ledger_viz.viz import theme
from ledger_viz.viz.components import box, hash_text, mono, point

LEVEL_Y = (-2.35, -1.25, -0.15, 0.95)
TX_Y = -3.3
X_SPAN = 6.1


@dataclass
class TreeView:
    tx_labels: list[Text]
    nodes: list[list[VGroup]]
    edges: dict[tuple[int, int], Line]
    leaf_links: list[Line]

    @property
    def group(self) -> VGroup:
        return VGroup(
            *self.tx_labels,
            *self.leaf_links,
            *self.edges.values(),
            *[n for level in self.nodes for n in level],
        )

    def node(self, level: int, index: int) -> VGroup:
        return self.nodes[level][index]


def node_mob(digest: bytes, *, root: bool = False) -> VGroup:
    frame = box(1.3, 0.5, color=theme.ACCENT if root else theme.MUTED, stroke=2.5)
    return VGroup(frame, hash_text(digest, 0.42).move_to(frame))


def build_tree(txs: Sequence[Transaction]) -> TreeView:
    levels = merkle_levels([tx.serialize() for tx in txs])
    if len(levels) != len(LEVEL_Y):
        msg = f"La vista asume {len(LEVEL_Y)} niveles (8 hojas); hay {len(levels)}"
        raise ValueError(msg)
    xs = [float(x) for x in np.linspace(-X_SPAN, X_SPAN, len(levels[0]))]
    nodes: list[list[VGroup]] = []
    for depth, level in enumerate(levels):
        is_root = depth == len(levels) - 1
        row = [
            node_mob(d, root=is_root).move_to(point(xs[i], LEVEL_Y[depth]))
            for i, d in enumerate(level)
        ]
        nodes.append(row)
        xs = [(xs[i] + xs[i + 1]) / 2 for i in range(0, len(xs) - 1, 2)]

    edges: dict[tuple[int, int], Line] = {}
    for depth in range(len(nodes) - 1):
        for i, child in enumerate(nodes[depth]):
            parent = nodes[depth + 1][i // 2]
            edges[(depth, i)] = Line(
                child.get_top(), parent.get_bottom(), color=theme.MUTED, stroke_width=2
            )

    tx_labels = [
        mono(short_tx(tx), 0.36).move_to(point(nodes[0][i].get_x(), TX_Y))
        for i, tx in enumerate(txs)
    ]
    leaf_links = [
        Line(
            lbl.get_top() + UP * 0.05, leaf.get_bottom() + DOWN * 0.03, color=theme.MUTED
        ).set_stroke(width=2)
        for lbl, leaf in zip(tx_labels, nodes[0], strict=True)
    ]
    return TreeView(tx_labels, nodes, edges, leaf_links)
