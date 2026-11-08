import pytest
from hypothesis import given
from hypothesis import strategies as st

from ledger_viz.script import WORDS_PER_SECOND, Beat, Section, cue_seconds, find_section


def test_cue_is_word_offset_over_reading_speed() -> None:
    text = "uno dos tres cuatro"
    assert cue_seconds(text, "tres") == pytest.approx(2 / WORDS_PER_SECOND)


def test_cue_ignores_markdown_case_and_punctuation() -> None:
    text = "Primero, el **Hash previo**: se copia."
    assert cue_seconds(text, "hash previo") == pytest.approx(2 / WORDS_PER_SECOND)


def test_cue_searches_after_given_word() -> None:
    text = "bloque a bloque b"
    assert cue_seconds(text, "bloque", after=1) == pytest.approx(2 / WORDS_PER_SECOND)


def test_cue_missing_phrase_fails_loudly() -> None:
    with pytest.raises(KeyError, match="no aparece"):
        cue_seconds("hola mundo", "adiós")


@given(st.lists(st.sampled_from(["a", "b", "c"]), min_size=1, max_size=30))
def test_cue_never_exceeds_beat_duration(words: list[str]) -> None:
    beat = Beat("x", " ".join(words))
    assert cue_seconds(beat.text, words[-1]) <= beat.seconds


def test_beat_seconds_ignore_markdown() -> None:
    assert Beat("a", "**uno** dos").seconds == Beat("b", "uno dos").seconds


def test_find_section_and_beat_errors_are_explicit() -> None:
    sections = (Section("s", "Slide", (Beat("b", "texto"),)),)
    assert find_section(sections, "s").beat("b").text == "texto"
    with pytest.raises(KeyError, match="sección"):
        find_section(sections, "nope")
    with pytest.raises(KeyError, match="beat"):
        sections[0].beat("nope")
