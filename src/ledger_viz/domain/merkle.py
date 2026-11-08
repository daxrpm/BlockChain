"""Árbol de Merkle estilo Bitcoin: si un nivel es impar se duplica el último nodo."""

from collections.abc import Sequence
from dataclasses import dataclass
from typing import Literal

from ledger_viz.domain.hashing import sha256d


@dataclass(frozen=True, slots=True)
class ProofStep:
    sibling: bytes
    side: Literal["left", "right"]


def _next_level(level: Sequence[bytes]) -> list[bytes]:
    padded = [*level, level[-1]] if len(level) % 2 else list(level)
    return [sha256d(padded[i] + padded[i + 1]) for i in range(0, len(padded), 2)]


def merkle_levels(leaves: Sequence[bytes]) -> list[list[bytes]]:
    """Todos los niveles, desde los hashes de las hojas hasta la raíz."""
    if not leaves:
        msg = "Se necesita al menos una hoja"
        raise ValueError(msg)
    levels = [[sha256d(leaf) for leaf in leaves]]
    while len(levels[-1]) > 1:
        levels.append(_next_level(levels[-1]))
    return levels


def merkle_root(leaves: Sequence[bytes]) -> bytes:
    return merkle_levels(leaves)[-1][0]


def merkle_proof(leaves: Sequence[bytes], index: int) -> list[ProofStep]:
    """Hermanos necesarios para recalcular la raíz desde la hoja `index`."""
    if not 0 <= index < len(leaves):
        msg = f"Índice {index} fuera de rango"
        raise IndexError(msg)
    proof: list[ProofStep] = []
    for level in merkle_levels(leaves)[:-1]:
        is_right = index % 2 == 1
        sibling_index = index - 1 if is_right else min(index + 1, len(level) - 1)
        proof.append(ProofStep(level[sibling_index], "left" if is_right else "right"))
        index //= 2
    return proof


def verify_proof(leaf: bytes, proof: Sequence[ProofStep], root: bytes) -> bool:
    node = sha256d(leaf)
    for step in proof:
        node = sha256d(step.sibling + node) if step.side == "left" else sha256d(node + step.sibling)
    return node == root
