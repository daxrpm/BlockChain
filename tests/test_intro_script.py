import pytest

from ledger_viz.intro_script import MIN_SECONDS, SECTIONS, Beat, render_markdown, section


def test_section_ids_are_unique() -> None:
    ids = [s.id for s in SECTIONS]
    assert len(ids) == len(set(ids))


def test_beat_ids_unique_within_section() -> None:
    for s in SECTIONS:
        ids = [b.id for b in s.beats]
        assert len(ids) == len(set(ids)), s.id


def test_beat_duration_grows_with_words() -> None:
    short = Beat("a", "hola")
    long = Beat("b", " ".join(["palabra"] * 100))
    assert short.seconds == MIN_SECONDS
    assert long.seconds > short.seconds


def test_lookup_errors_are_explicit() -> None:
    with pytest.raises(KeyError, match="sección"):
        section("nope")
    with pytest.raises(KeyError, match="beat"):
        SECTIONS[0].beat("nope")


def test_markdown_contains_every_beat() -> None:
    md = render_markdown()
    for s in SECTIONS:
        for b in s.beats:
            assert b.text in md
