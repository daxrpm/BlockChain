"""Ledger append-only: los saldos no se guardan, se derivan del historial."""

from collections import Counter
from collections.abc import Mapping

from ledger_viz.domain.transaction import Transaction


class InsufficientFundsError(ValueError):
    pass


class Ledger:
    def __init__(self, genesis: Mapping[str, int]) -> None:
        self._genesis = dict(genesis)
        self._entries: list[Transaction] = []

    @property
    def entries(self) -> tuple[Transaction, ...]:
        return tuple(self._entries)

    def balances(self) -> dict[str, int]:
        totals: Counter[str] = Counter(self._genesis)
        for tx in self._entries:
            totals[tx.sender] -= tx.amount
            totals[tx.receiver] += tx.amount
        return dict(totals)

    def append(self, tx: Transaction) -> None:
        available = self.balances().get(tx.sender, 0)
        if tx.amount > available:
            msg = f"{tx.sender} tiene {available} y quiere enviar {tx.amount}"
            raise InsufficientFundsError(msg)
        self._entries.append(tx)
