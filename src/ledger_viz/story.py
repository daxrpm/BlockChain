"""Datos únicos de la historia: todas las escenas leen de aquí para que los hashes coincidan."""

from typing import Final

from ledger_viz.domain.block import Block, build_chain
from ledger_viz.domain.transaction import Transaction

GENESIS: Final = {"Alice": 10}

LEDGER_TXS: Final = (
    Transaction("Alice", "Bob", 5),
    Transaction("Bob", "Carol", 2),
    Transaction("Carol", "Alice", 1),
)
APPENDED_TX: Final = Transaction("Bob", "Alice", 1)

# Doble gasto: Alice tiene 7 tras A3 e intenta gastarlos dos veces.
DOUBLE_SPEND: Final = (Transaction("Alice", "Bob", 7), Transaction("Alice", "Carol", 7))

DEMO_TX: Final = Transaction("Alice", "Bob", 5)
DEMO_TX_TAMPERED: Final = Transaction("Alice", "Bob", 50)

# Bloque protagonista (índice 1 de la cadena): 8 transacciones para un árbol de 3 niveles.
BLOCK_TXS: Final = (
    *LEDGER_TXS,
    APPENDED_TX,
    Transaction("Alice", "Dave", 2),
    Transaction("Dave", "Carol", 1),
    Transaction("Carol", "Bob", 1),
    Transaction("Alice", "Eve", 1),
)
TAMPER_INDEX: Final = 1
TAMPERED_TX: Final = Transaction("Bob", "Carol", 20)
PROOF_INDEX: Final = 4  # Alice → Dave: Dave verifica su pago desde el celular

TIMESTAMP: Final = 1_794_211_200  # 2026-11-09 08:00 UTC, día de la exposición

CHAIN: Final[list[Block]] = build_chain(
    [
        (Transaction("Red", "Alice", 10),),  # emisión inicial del génesis
        BLOCK_TXS,
        (Transaction("Eve", "Bob", 1), Transaction("Bob", "Dave", 1)),
        (Transaction("Dave", "Alice", 1),),
        (Transaction("Carol", "Eve", 1), Transaction("Eve", "Dave", 1)),
    ],
    timestamp=TIMESTAMP,
)
FOCUS_BLOCK: Final = 1


def short_tx(tx: Transaction) -> str:
    return f"{tx.sender[0]}→{tx.receiver[0]}:{tx.amount}"
