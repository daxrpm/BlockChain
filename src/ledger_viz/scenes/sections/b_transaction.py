"""B1: anatomía de una transacción y su ID como huella (efecto avalancha real)."""

from manim import DOWN, LEFT, RIGHT, UP, FadeIn, Indicate, LaggedStart, Transform, VGroup, Write

from ledger_viz.domain.hashing import short_hex
from ledger_viz.scenes.sections.common import Stage
from ledger_viz.story import DEMO_TX, DEMO_TX_TAMPERED
from ledger_viz.viz import theme
from ledger_viz.viz.components import box, hash_chars, label, mono

ID_CHARS = 16


def _field(key: str, value: str) -> VGroup:
    return VGroup(label(key, 0.42, color=theme.MUTED), label(value, 0.5, bold=True))


class TransactionSection:
    def __init__(self, stage: Stage) -> None:
        self.stage = stage

    def run(self) -> None:
        s = self.stage.scene
        s.next_section("B1_transaccion")
        self.stage.swap_title("La transacción", "Una línea del cuaderno, con identidad propia")

        line = mono(DEMO_TX.label(), 0.6).move_to(UP * 0.9)
        s.play(Write(line), run_time=0.8)

        fields = [
            _field("De", DEMO_TX.sender),
            _field("Para", DEMO_TX.receiver),
            _field("Monto", str(DEMO_TX.amount)),
            _field("Firma", "firma digital de Alice"),
        ]
        for f in fields:
            f[1].next_to(f[0], RIGHT, buff=0.4)
        grid = VGroup(*fields).arrange(DOWN, buff=0.28, aligned_edge=LEFT)
        values_x = max(f[0].get_right()[0] for f in fields) + 0.4
        for f in fields:
            f[1].set_x(values_x + f[1].width / 2)
        card = box(7.0, grid.height + 0.8)
        VGroup(card, grid).move_to(UP * 0.75)
        grid.move_to(card)
        s.play(Transform(line, card), LaggedStart(*[FadeIn(f) for f in fields], lag_ratio=0.15))

        id_label = label("ID = SHA-256²(transacción)", 0.42, color=theme.MUTED)
        original = short_hex(DEMO_TX.txid, ID_CHARS)
        chars = hash_chars(original, 0.62)
        id_row = VGroup(id_label, chars).arrange(DOWN, buff=0.22).next_to(card, DOWN, buff=0.45)
        s.play(FadeIn(id_label), Write(chars), run_time=1.0)
        s.wait(0.6)

        amount = fields[2][1]
        new_amount = label(str(DEMO_TX_TAMPERED.amount), 0.5, bold=True).set_color(theme.DANGER)
        new_amount.move_to(amount, aligned_edge=LEFT)
        tampered = short_hex(DEMO_TX_TAMPERED.txid, ID_CHARS)
        new_chars = hash_chars(tampered, 0.62).move_to(chars)
        for new, (a, b) in zip(new_chars, zip(original, tampered, strict=True), strict=True):
            new.set_color(theme.DANGER if a != b else theme.ACCENT)
        s.play(Transform(amount, new_amount), Indicate(fields[2][0], color=theme.DANGER))
        s.play(Transform(chars, new_chars), run_time=1.0)

        caption = label(
            "Cambias un dígito → cambia toda la huella", 0.44, color=theme.TEXT
        ).to_edge(DOWN, buff=0.45)
        s.play(FadeIn(caption, shift=UP * 0.2))
        self.id_row = id_row
        s.wait(1.5)
