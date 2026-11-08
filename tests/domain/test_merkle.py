from hypothesis import given
from hypothesis import strategies as st

from ledger_viz.domain.hashing import sha256d
from ledger_viz.domain.merkle import merkle_levels, merkle_proof, merkle_root, verify_proof

leaves_st = st.lists(st.binary(min_size=1, max_size=16), min_size=1, max_size=33)


def test_single_leaf_root_is_its_hash() -> None:
    assert merkle_root([b"tx"]) == sha256d(b"tx")


def test_two_leaves_root_hashes_concatenation() -> None:
    a, b = sha256d(b"a"), sha256d(b"b")
    assert merkle_root([b"a", b"b"]) == sha256d(a + b)


def test_odd_level_duplicates_last_node_like_bitcoin() -> None:
    a, b, c = (sha256d(x) for x in (b"a", b"b", b"c"))
    expected = sha256d(sha256d(a + b) + sha256d(c + c))
    assert merkle_root([b"a", b"b", b"c"]) == expected


def test_levels_end_in_root() -> None:
    levels = merkle_levels([b"a", b"b", b"c", b"d"])
    assert [len(level) for level in levels] == [4, 2, 1]
    assert levels[-1][0] == merkle_root([b"a", b"b", b"c", b"d"])


def test_empty_leaves_rejected() -> None:
    import pytest

    with pytest.raises(ValueError, match="al menos una"):
        merkle_root([])


@given(leaves_st, st.data())
def test_every_leaf_has_valid_proof(leaves: list[bytes], data: st.DataObject) -> None:
    index = data.draw(st.integers(min_value=0, max_value=len(leaves) - 1))
    root = merkle_root(leaves)
    proof = merkle_proof(leaves, index)
    assert verify_proof(leaves[index], proof, root)


@given(leaves_st, st.data())
def test_tampered_leaf_fails_proof(leaves: list[bytes], data: st.DataObject) -> None:
    index = data.draw(st.integers(min_value=0, max_value=len(leaves) - 1))
    root = merkle_root(leaves)
    proof = merkle_proof(leaves, index)
    assert not verify_proof(leaves[index] + b"!", proof, root)


def test_proof_size_is_logarithmic() -> None:
    leaves = [bytes([i % 256, i // 256]) for i in range(4096)]
    assert len(merkle_proof(leaves, 1234)) == 12
