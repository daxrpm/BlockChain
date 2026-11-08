"""Transacción mínima: quién paga, a quién y cuánto."""

from dataclasses import dataclass

from ledger_viz.domain.hashing import sha256d


@dataclass(frozen=True, slots=True)
class Transaction:
    sender: str
    receiver: str
    amount: int

    def __post_init__(self) -> None:
        if self.amount <= 0:
            msg = f"El monto debe ser positivo, se recibió {self.amount}"
            raise ValueError(msg)
        if self.sender == self.receiver:
            msg = "Nadie puede pagarse a sí mismo"
            raise ValueError(msg)

    def serialize(self) -> bytes:
        return f"{self.sender}->{self.receiver}:{self.amount}".encode()

    @property
    def txid(self) -> bytes:
        return sha256d(self.serialize())

    def label(self) -> str:
        return f"{self.sender} → {self.receiver}: {self.amount}"
