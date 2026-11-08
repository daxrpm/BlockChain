import re

from ledger_viz.part3_script import MAX_SECONDS, SECTIONS, render_markdown

CLIP_NAME = re.compile(r"^[A-Za-z0-9_]+$")


def test_fits_in_seven_minutes_with_margin() -> None:
    total = sum(b.seconds for s in SECTIONS for b in s.beats)
    assert total <= MAX_SECONDS


def test_beat_ids_are_globally_unique_and_valid_clip_names() -> None:
    ids = [b.id for s in SECTIONS for b in s.beats]
    assert len(ids) == len(set(ids))
    assert all(CLIP_NAME.match(i) for i in ids)


def test_every_beat_has_title_and_visual() -> None:
    for s in SECTIONS:
        for b in s.beats:
            assert b.title, b.id
            assert b.visual, b.id


def test_script_is_about_blockchain_in_general() -> None:
    spoken = " ".join(b.text for s in SECTIONS for b in s.beats)
    assert "Bitcoin" not in spoken
    assert "SHA-256" not in spoken


def test_markdown_contains_every_beat() -> None:
    md = render_markdown()
    for s in SECTIONS:
        for b in s.beats:
            assert b.text in md
            assert b.visual in md
