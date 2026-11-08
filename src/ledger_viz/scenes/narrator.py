"""Sincroniza la animación con un guion: cada beat dura al menos su tiempo de lectura.

`cue(frase)` espera hasta el instante en que se dice esa frase, para que cada elemento
aparezca cuando se nombra. Si la animación previa ya pasó ese instante, sigue sin esperar.
"""

from collections.abc import Generator, Sequence
from contextlib import contextmanager

from manim import Scene

from ledger_viz.script import WORDS_PER_SECOND, Beat, Section, cue_seconds, find_section


class Narrator:
    def __init__(
        self, scene: Scene, sections: Sequence[Section], *, clip_per_beat: bool = False
    ) -> None:
        self.scene = scene
        self.sections = sections
        self.clip_per_beat = clip_per_beat
        self._section: Section | None = None
        self._beat: Beat | None = None
        self._beat_start = 0.0
        self._cursor = 0  # palabra desde la que buscar la siguiente marca

    def start(self, section_id: str) -> None:
        self._section = find_section(self.sections, section_id)
        if not self.clip_per_beat:
            self.scene.next_section(self._section.id)

    @contextmanager
    def beat(self, beat_id: str) -> Generator[None]:
        if self._section is None:
            msg = "Llama a start() antes de narrar un beat"
            raise RuntimeError(msg)
        beat = self._section.beat(beat_id)
        if self.clip_per_beat:
            self.scene.next_section(beat.id)
        self._beat, self._beat_start, self._cursor = beat, self.scene.time, 0
        yield
        remaining = beat.seconds - (self.scene.time - self._beat_start)
        if remaining > 0:
            self.scene.wait(remaining)
        self._beat = None

    def cue(self, phrase: str) -> None:
        """Espera hasta que el expositor empiece a decir `phrase` dentro del beat actual."""
        if self._beat is None:
            msg = "cue() solo se usa dentro de un beat"
            raise RuntimeError(msg)
        offset = cue_seconds(self._beat.text, phrase, after=self._cursor)
        self._cursor = round(offset * WORDS_PER_SECOND) + 1
        wait = offset - (self.scene.time - self._beat_start)
        if wait > 1 / 30:
            self.scene.wait(wait)

    def left(self) -> float:
        """Segundos que quedan del beat actual (para estirar la última animación)."""
        if self._beat is None:
            return 0.0
        return max(0.0, self._beat.seconds - (self.scene.time - self._beat_start))
