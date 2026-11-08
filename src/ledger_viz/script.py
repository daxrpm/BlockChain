"""Guion como datos: beats con tiempo de lectura y marcas de sincronía por palabra.

La escena dura al menos lo que tarda en leerse cada beat (a `WORDS_PER_SECOND`) y puede
disparar cada animación en el instante en que se dice una frase (`cue_seconds`).
"""

import re
from collections.abc import Sequence
from dataclasses import dataclass
from typing import Final

WORDS_PER_SECOND: Final = 2.4  # ritmo pausado de exposición (~144 palabras/min)
MIN_SECONDS: Final = 2.5

_MARKUP = re.compile(r"[*_]")
_NON_WORD = re.compile(r"[^\w]+")


def plain(text: str) -> str:
    """Texto sin marcas de énfasis Markdown."""
    return _MARKUP.sub("", text)


def _tokens(text: str) -> list[str]:
    return [t for t in (_NON_WORD.sub("", w).lower() for w in plain(text).split()) if t]


def word_count(text: str) -> int:
    return len(plain(text).split())


def cue_seconds(text: str, phrase: str, *, after: int = 0) -> float:
    """Segundo (desde el inicio del beat) en que se empieza a decir `phrase`."""
    words, target = _tokens(text), _tokens(phrase)
    for i in range(after, len(words) - len(target) + 1):
        if words[i : i + len(target)] == target:
            return i / WORDS_PER_SECOND
    msg = f"La frase {phrase!r} no aparece en el beat (desde la palabra {after})"
    raise KeyError(msg)


@dataclass(frozen=True, slots=True)
class Beat:
    id: str
    text: str
    changed: bool = False  # True si difiere del guion original (para revisarlo)
    title: str = ""
    visual: str = ""

    @property
    def seconds(self) -> float:
        return max(MIN_SECONDS, word_count(self.text) / WORDS_PER_SECOND)


@dataclass(frozen=True, slots=True)
class Section:
    id: str
    slide: str
    beats: tuple[Beat, ...]

    def beat(self, beat_id: str) -> Beat:
        for b in self.beats:
            if b.id == beat_id:
                return b
        msg = f"No existe el beat {beat_id!r} en la sección {self.id}"
        raise KeyError(msg)


def find_section(sections: Sequence[Section], section_id: str) -> Section:
    for s in sections:
        if s.id == section_id:
            return s
    msg = f"No existe la sección {section_id!r}"
    raise KeyError(msg)
