"""Bloque = cabecera (80 bytes) + cuerpo (transacciones). El hash cubre solo la cabecera."""

import struct
from collections.abc import Sequence
from dataclasses import dataclass, replace

from ledger_viz.domain.hashing import sha256d
from ledger_viz.domain.merkle import merkle_root
from ledger_viz.domain.transaction import Transaction

GENESIS_PREV_HASH = bytes(32)
DEFAULT_BITS = 0x1D00FFFF
_HEADER_FORMAT = "<I32s32sIII"


@dataclass(frozen=True, slots=True)
class BlockHeader:
    version: int
    prev_hash: bytes
    merkle_root: bytes
    timestamp: int
    bits: int = DEFAULT_BITS
    nonce: int = 0

    def serialize(self) -> bytes:
        return struct.pack(
            _HEADER_FORMAT,
            self.version,
            self.prev_hash,
            self.merkle_root,
            self.timestamp,
            self.bits,
            self.nonce,
        )


@dataclass(frozen=True, slots=True)
class Block:
    header: BlockHeader
    transactions: tuple[Transaction, ...]

    @property
    def hash(self) -> bytes:
        return sha256d(self.header.serialize())

    @classmethod
    def create(
        cls, prev_hash: bytes, transactions: Sequence[Transaction], timestamp: int
    ) -> "Block":
        txs = tuple(transactions)
        root = merkle_root([tx.serialize() for tx in txs])
        header = BlockHeader(version=1, prev_hash=prev_hash, merkle_root=root, timestamp=timestamp)
        return cls(header, txs)

    @classmethod
    def tamper(cls, block: "Block", index: int, new_tx: Transaction) -> "Block":
        """Simula a un atacante que reescribe una transacción y recalcula su bloque."""
        txs = list(block.transactions)
        txs[index] = new_tx
        root = merkle_root([tx.serialize() for tx in txs])
        return cls(replace(block.header, merkle_root=root), tuple(txs))


def build_chain(batches: Sequence[Sequence[Transaction]], timestamp: int) -> list[Block]:
    chain: list[Block] = []
    prev = GENESIS_PREV_HASH
    for offset, batch in enumerate(batches):
        block = Block.create(prev, batch, timestamp + offset * 600)
        chain.append(block)
        prev = block.hash
    return chain


def find_broken_links(chain: Sequence[Block]) -> list[int]:
    """Índices de bloques cuyo `prev_hash` ya no coincide con el bloque anterior."""
    return [i for i in range(1, len(chain)) if chain[i].header.prev_hash != chain[i - 1].hash]
