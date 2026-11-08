"""S2: anatomía de una transacción, campos que agrega cada red y su ID como hash."""

from manim import (
    DOWN,
    LEFT,
    RIGHT,
    UP,
    FadeIn,
    FadeOut,
    Indicate,
    SurroundingRectangle,
    Transform,
    VGroup,
    Write,
)

from ledger_viz.domain.hashing import short_hex
from ledger_viz.scenes.narrator import Narrator
from ledger_viz.scenes.sections.common import Stage
from ledger_viz.story import DEMO_TX, DEMO_TX_TAMPERED
from ledger_viz.viz import icons, theme
from ledger_viz.viz.components import as_anim, box, hash_chars, label, mono, point

ID_CHARS = 16
CARD_W = 7.6
CARD_TOP = 2.35
FIELD_CUES = ("de quién", "para quién", "cuánto", "firma digital")


def _field(key: str, value: str) -> VGroup:
    return VGroup(label(key, 0.38, color=theme.MUTED), label(value, 0.44, bold=True))


class TransactionSection:
    def __init__(self, stage: Stage, narrator: Narrator) -> None:
        self.stage, self.n, self.s = stage, narrator, stage.scene

    def run(self) -> None:
        self.n.start("S2")
        self._layout()
        self.fields_beat()
        self.extras_beat()
        self.id_beat()

    def _layout(self) -> None:
        self.fields = [
            _field("De", DEMO_TX.sender),
            _field("Para", DEMO_TX.receiver),
            _field("Monto", str(DEMO_TX.amount)),
            _field("Firma", "firma digital de Alice"),
            _field("Comisión", "0,1"),
            _field("Contador", "nº 7  (no se repite)"),
        ]
        keys = VGroup(*[f[0] for f in self.fields]).arrange(DOWN, buff=0.28, aligned_edge=LEFT)
        key_x = -CARD_W / 2 + 0.5
        values_x = key_x + max(k.width for k in keys) + 0.5
        for key, value in self.fields:
            key.set_x(key_x, direction=LEFT)
            value.set_x(values_x, direction=LEFT).match_y(key)
        grid = VGroup(*self.fields)
        grid.shift(UP * (CARD_TOP - 0.35 - grid.get_top()[1]))
        bottom_small = self.fields[3].get_bottom()[1] - 0.35
        bottom_big = self.fields[5].get_bottom()[1] - 0.35
        self.small_frame = box(CARD_W, CARD_TOP - bottom_small).move_to(
            point(0, (CARD_TOP + bottom_small) / 2)
        )
        self.big_frame = box(CARD_W, CARD_TOP - bottom_big).move_to(
            point(0, (CARD_TOP + bottom_big) / 2)
        )

    def fields_beat(self) -> None:
        s, n = self.s, self.n
        with n.beat("S2_1_campos"):
            self.stage.swap_title("La transacción", "Un mensaje con formato fijo")
            n.cue("una transacción")
            line = mono(DEMO_TX.label(), 0.6).move_to(self.small_frame)
            s.play(Write(line), run_time=1.0)
            self.card = line
            s.play(Transform(self.card, self.small_frame), run_time=1.0)
            for field, cue in zip(self.fields[:4], FIELD_CUES, strict=True):
                n.cue(cue)
                s.play(FadeIn(field, shift=RIGHT * 0.2), run_time=0.7)
            n.cue("la firma prueba")
            key = icons.key(theme.ACCENT).scale(0.45).next_to(self.fields[3], RIGHT, buff=0.3)
            note = label("solo Alice puede generarla", 0.32, color=theme.ACCENT)
            note.next_to(self.small_frame, DOWN, buff=0.25)
            s.play(FadeIn(key, scale=0.6), Indicate(self.fields[3][1], color=theme.ACCENT))
            s.play(FadeIn(note, shift=UP * 0.1), run_time=0.8)
            self.key, self.note = key, note

    def extras_beat(self) -> None:
        s, n = self.s, self.n
        with n.beat("S2_2_extras"):
            n.cue("lleva más datos")
            s.play(FadeOut(self.note), Transform(self.card, self.big_frame), run_time=1.0)
            n.cue("comisión")
            s.play(FadeIn(self.fields[4], shift=RIGHT * 0.2), run_time=0.8)
            n.cue("contador")
            s.play(FadeIn(self.fields[5], shift=RIGHT * 0.2), run_time=0.8)
            n.cue("ejecutarla dos veces")
            s.play(Indicate(self.fields[5][1], color=theme.ACCENT), run_time=1.0)
            n.cue("las reglas de cada red")
            rule = label("válida = cumple las reglas de la red", 0.42, color=theme.OK, bold=True)
            rule.next_to(self.big_frame, DOWN, buff=0.35)
            s.play(FadeIn(rule, shift=UP * 0.2), run_time=1.0)
            self.rule = rule

    def id_beat(self) -> None:
        s, n = self.s, self.n
        with n.beat("S2_3_id"):
            n.cue("con su hash")
            id_label = label("ID = hash(transacción)", 0.4, color=theme.MUTED)
            original = short_hex(DEMO_TX.txid, ID_CHARS)
            chars = hash_chars(original, 0.6)
            id_row = VGroup(id_label, chars).arrange(DOWN, buff=0.2)
            id_row.next_to(self.big_frame, DOWN, buff=0.3)
            s.play(FadeOut(self.rule), FadeIn(id_label), Write(chars), run_time=1.4)

            n.cue("cambia el monto")
            amount = self.fields[2][1]
            new_amount = label(str(DEMO_TX_TAMPERED.amount), 0.44, bold=True)
            new_amount.set_color(theme.DANGER).move_to(amount, aligned_edge=LEFT)
            s.play(
                Transform(amount, new_amount),
                Indicate(self.fields[2][0], color=theme.DANGER),
                run_time=1.0,
            )
            n.cue("por completo")
            tampered = short_hex(DEMO_TX_TAMPERED.txid, ID_CHARS)
            new_chars = hash_chars(tampered, 0.6).move_to(chars)
            for new, (a, b) in zip(new_chars, zip(original, tampered, strict=True), strict=True):
                new.set_color(theme.DANGER if a != b else theme.ACCENT)
            s.play(Transform(chars, new_chars), run_time=1.2)
            n.cue("ya es otra transacción")
            frame = SurroundingRectangle(chars, color=theme.DANGER, buff=0.12)
            s.play(FadeIn(frame), as_anim(id_label.animate.set_color(theme.DANGER)), run_time=0.8)
