import itertools

import pytest

from ledger_viz.domain.block import GENESIS_PREV_HASH, Block, build_chain, find_broken_links
from ledger_viz.domain.hashing import sha256d, short_hex
from ledger_viz.domain.ledger import InsufficientFundsError, Ledger
from ledger_viz.domain.transaction import Transaction


def test_short_hex_truncates_uppercase() -> None:
    assert short_hex(bytes.fromhex("abcdef0123"), 4) == "ABCD"


def test_sha256d_is_double_sha256() -> None:
    import hashlib

    once = hashlib.sha256(b"x").digest()
    assert sha256d(b"x") == hashlib.sha256(once).digest()


def test_transaction_rejects_non_positive_amount() -> None:
    with pytest.raises(ValueError, match="positivo"):
        Transaction("Alice", "Bob", 0)


def test_transaction_rejects_self_payment() -> None:
    with pytest.raises(ValueError, match="sí mismo"):
        Transaction("Alice", "Alice", 5)


def test_txid_changes_when_amount_changes() -> None:
    assert Transaction("Alice", "Bob", 5).txid != Transaction("Alice", "Bob", 50).txid


def test_balances_are_derived_from_history() -> None:
    ledger = Ledger(genesis={"Alice": 10})
    ledger.append(Transaction("Alice", "Bob", 5))
    ledger.append(Transaction("Bob", "Carol", 2))
    assert ledger.balances() == {"Alice": 5, "Bob": 3, "Carol": 2}


def test_ledger_rejects_overspend_and_keeps_history() -> None:
    ledger = Ledger(genesis={"Alice": 10})
    with pytest.raises(InsufficientFundsError):
        ledger.append(Transaction("Alice", "Bob", 11))
    assert ledger.entries == ()


def test_entries_are_immutable_view() -> None:
    ledger = Ledger(genesis={"Alice": 10})
    ledger.append(Transaction("Alice", "Bob", 1))
    assert isinstance(ledger.entries, tuple)


def _txs(*amounts: int) -> tuple[Transaction, ...]:
    return tuple(Transaction("Alice", "Bob", a) for a in amounts)


def test_chain_links_prev_hashes() -> None:
    chain = build_chain([_txs(1, 2), _txs(3), _txs(4, 5, 6)], timestamp=1_700_000_000)
    assert chain[0].header.prev_hash == GENESIS_PREV_HASH
    for prev, block in itertools.pairwise(chain):
        assert block.header.prev_hash == prev.hash


def test_valid_chain_has_no_broken_links() -> None:
    chain = build_chain([_txs(1), _txs(2), _txs(3)], timestamp=1_700_000_000)
    assert find_broken_links(chain) == []


def test_tampering_a_transaction_breaks_next_link() -> None:
    chain = build_chain([_txs(1), _txs(5), _txs(3)], timestamp=1_700_000_000)
    tampered = Block.tamper(chain[1], index=0, new_tx=Transaction("Alice", "Bob", 50))
    assert tampered.hash != chain[1].hash
    assert find_broken_links([chain[0], tampered, chain[2]]) == [2]


def test_header_serializes_to_80_bytes_like_bitcoin() -> None:
    (block,) = build_chain([_txs(1)], timestamp=1_700_000_000)
    assert len(block.header.serialize()) == 80
