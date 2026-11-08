"""Escena de humo: valida tipografías, paleta y que los hashes provienen del dominio."""

from manim import DOWN, UP, FadeIn, RoundedRectangle, Scene, Text, VGroup, Write

from ledger_viz.domain.hashing import short_hex
from ledger_viz.domain.transaction import Transaction
from ledger_viz.viz import theme


class Smoke(Scene):
    def construct(self) -> None:
        tx = Transaction("Alice", "Bob", 5)
        card = RoundedRectangle(
            width=6, height=2.2, corner_radius=0.2, color=theme.ACCENT, stroke_width=3
        )
        label = Text(tx.label(), font=theme.FONT_SANS, color=theme.TEXT, weight="BOLD")
        txid = Text(
            f"txid: {short_hex(tx.txid, 16)}…", font=theme.FONT_MONO, color=theme.ACCENT
        ).scale(0.6)
        content = VGroup(label, txid).arrange(DOWN, buff=0.3)
        title = Text("ledger-viz OK", font=theme.FONT_SANS, color=theme.MUTED).scale(0.5)
        title.to_edge(UP)
        self.play(FadeIn(title), Write(card))
        self.play(FadeIn(content, shift=UP * 0.2))
        self.wait(0.5)
