"""Primitivas de hash usadas por Bitcoin (doble SHA-256)."""

import hashlib


def sha256d(data: bytes) -> bytes:
    """SHA-256 aplicado dos veces, como en Bitcoin."""
    return hashlib.sha256(hashlib.sha256(data).digest()).digest()


def short_hex(digest: bytes, length: int = 4) -> str:
    """Prefijo legible de un hash para mostrarlo en pantalla."""
    return digest.hex()[:length].upper()
