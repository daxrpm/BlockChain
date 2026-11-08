"""S5: el bloque se abre en cabecera y cuerpo; el hash del bloque cubre solo la cabecera."""

from datetime import UTC, datetime

from manim import (
    DOWN,
    LEFT,
    RIGHT,
    UP,
    Arrow,
    Circumscribe,
    FadeIn,
    LaggedStart,
    ReplacementTransform,
    SurroundingRectangle,
    VGroup,
    Write,
)

from ledger_viz.domain.hashing import short_hex
from ledger_viz.scenes.narrator import Narrator
from ledger_viz.scenes.sections.common import Stage
from ledger_viz.story import CHAIN, FOCUS_BLOCK, short_tx
from ledger_viz.viz import theme
from ledger_viz.viz.components import as_anim, box, hash_chars, label, mono

HEADER_W = 10.4
VALUE_CHARS = 12
ROW_CUES = ("versión", "hash previo", "raíz de merkle", "marca de tiempo")
NOTES = {1: "← el enlace", 2: "← resume el cuerpo"}


class StructureSection:
    def __init__(self, stage: Stage, narrator: Narrator) -> None:
        self.stage, self.n, self.s = stage, narrator, stage.scene
        self.block = CHAIN[FOCUS_BLOCK]

    def run(self) -> None:
        self.n.start("S5")
        self.open_block()
        self.fields()
        self.block_hash()

    def _header_rows(self) -> VGroup:
        h = self.block.header
        when = datetime.fromtimestamp(h.timestamp, tz=UTC).strftime("%Y-%m-%d %H:%M UTC")
        spec = [
            ("Versión", str(h.version)),
            ("Hash previo", short_hex(h.prev_hash, VALUE_CHARS) + "…"),
            ("Raíz de Merkle", short_hex(h.merkle_root, VALUE_CHARS) + "…"),
            ("Marca de tiempo", when),
            ("Dificultad", f"{h.bits:08x}"),
            ("Nonce", str(h.nonce)),
        ]
        rows = VGroup(
            *[
                VGroup(label(name, 0.4), mono(value, 0.38, color=theme.ACCENT))
                for name, value in spec
            ]
        )
        rows.arrange(DOWN, buff=0.17, aligned_edge=LEFT)
        for row in rows:
            row[0].set_x(-4.6, direction=LEFT)
            row[1].set_x(-0.9, direction=LEFT)
        return rows

    def open_block(self) -> None:
        s, n = self.s, self.n
        with n.beat("S5_1_abrir"):
            focus = self.stage.focus
            if focus is None:
                msg = "La sección de la cadena debe entregar el bloque en stage.focus"
                raise RuntimeError(msg)
            self.stage.swap_title("Anatomía de un bloque", "Cabecera + cuerpo", keep=[focus])
            header_frame = box(HEADER_W, 3.25)
            header_title = label("CABECERA", 0.42, color=theme.ACCENT, bold=True)
            rows = self._header_rows()
            header_content = VGroup(header_title, rows).arrange(DOWN, buff=0.22, aligned_edge=LEFT)
            header = VGroup(header_frame, header_content).move_to(UP * 0.85)
            header_content.move_to(header_frame).shift(LEFT * 0.1)

            body_frame = box(HEADER_W, 1.45, color=theme.MUTED)
            body_title = label(
                f"CUERPO · {len(self.block.transactions)} transacciones", 0.42, bold=True
            )
            txs = VGroup(*[mono(short_tx(tx), 0.36) for tx in self.block.transactions])
            txs.arrange(RIGHT, buff=0.32)
            body_content = VGroup(body_title, txs).arrange(DOWN, buff=0.22)
            body = VGroup(body_frame, body_content).next_to(header, DOWN, buff=0.3)
            body_content.move_to(body_frame)

            n.cue("abramos un bloque")
            s.play(as_anim(focus.animate.scale(1.5).move_to(DOWN * 0.3)), run_time=0.8)
            s.play(ReplacementTransform(focus, VGroup(header_frame, body_frame)), run_time=1.1)
            n.cue("cabecera")
            s.play(FadeIn(header_title, shift=RIGHT * 0.2), run_time=0.7)
            small = label("resumen pequeño, tamaño fijo", 0.32, color=theme.MUTED)
            small.next_to(header_title, RIGHT, buff=0.4)
            s.play(FadeIn(small), run_time=0.6)
            n.cue("cuerpo")
            s.play(FadeIn(body_title), run_time=0.6)
            s.play(LaggedStart(*[FadeIn(t) for t in txs], lag_ratio=0.1), run_time=1.2)
            self.header, self.body, self.rows, self.header_frame = header, body, rows, header_frame
            self.small = small

    def fields(self) -> None:
        s, n, rows = self.s, self.n, self.rows
        with n.beat("S5_2_campos"):
            notes = VGroup()
            for i, cue in enumerate(ROW_CUES):
                n.cue(cue)
                s.play(FadeIn(rows[i], shift=RIGHT * 0.2), run_time=0.7)
                if i in NOTES:
                    note = label(NOTES[i], 0.32, color=theme.ACCENT)
                    note.set_x(self.header_frame.get_right()[0] - 0.25, direction=RIGHT)
                    note.match_y(rows[i])
                    frame = SurroundingRectangle(rows[i], color=theme.ACCENT, buff=0.06)
                    s.play(FadeIn(note), FadeIn(frame), run_time=0.6)
                    s.play(as_anim(frame.animate.set_opacity(0)), run_time=0.4)
                    notes.add(note)
            n.cue("dificultad")
            mining = VGroup(rows[4], rows[5])
            s.play(FadeIn(mining, shift=RIGHT * 0.2), run_time=0.8)
            consensus = label("→ consenso", 0.32, color=theme.MUTED)
            consensus.set_x(self.header_frame.get_right()[0] - 0.25, direction=RIGHT)
            consensus.match_y(mining)
            s.play(as_anim(mining.animate.set_opacity(0.5)), FadeIn(consensus), run_time=0.8)
            self.notes = VGroup(notes, consensus)

    def block_hash(self) -> None:
        s, n = self.s, self.n
        with n.beat("S5_3_hash_cabecera"):
            n.cue("solo con la cabecera")
            s.play(
                as_anim(
                    VGroup(self.header, self.body)
                    .animate.scale(0.72)
                    .to_edge(LEFT, buff=0.4)
                    .shift(DOWN * 0.15)
                ),
                as_anim(self.notes.animate.set_opacity(0)),
                as_anim(self.small.animate.set_opacity(0)),
                run_time=1.0,
            )
            hasher = box(2.3, 0.8, color=theme.ACCENT)
            hasher_text = label("hash", 0.5, color=theme.ACCENT, bold=True).move_to(hasher)
            engine = VGroup(hasher, hasher_text).move_to(RIGHT * 4.6 + UP * 1.0)
            arrow_in = Arrow(
                self.header.get_right(), engine.get_left(), color=theme.ACCENT, buff=0.15
            )
            s.play(FadeIn(engine), Write(arrow_in), run_time=0.9)
            result_label = label("Hash del bloque", 0.4, color=theme.MUTED)
            digest = hash_chars(short_hex(self.block.hash, 12), 0.5)
            result = VGroup(result_label, digest).arrange(DOWN, buff=0.18)
            result.next_to(engine, DOWN, buff=0.9)
            arrow_out = Arrow(engine.get_bottom(), result.get_top(), color=theme.ACCENT, buff=0.1)
            s.play(Write(arrow_out), FadeIn(result_label), Write(digest), run_time=1.1)
            n.cue("no entran directamente")
            s.play(as_anim(self.body.animate.set_opacity(0.25)), run_time=0.8)
            n.cue("qué protege")
            question = label("¿Y las transacciones?", 0.5, color=theme.DANGER, bold=True)
            question.next_to(result, DOWN, buff=0.8)
            s.play(FadeIn(question, shift=UP * 0.2), run_time=0.8)
            s.play(Circumscribe(self.rows[2], color=theme.ACCENT, time_width=0.6), run_time=1.4)
