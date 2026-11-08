"""D1–D2: el bloque se abre en cabecera (80 B) y cuerpo; el hash cubre solo la cabecera."""

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
from ledger_viz.scenes.sections.common import Stage
from ledger_viz.story import CHAIN, FOCUS_BLOCK, short_tx
from ledger_viz.viz import theme
from ledger_viz.viz.components import box, hash_chars, label, mono

HEADER_W = 10.4
VALUE_CHARS = 12


class StructureSection:
    def __init__(self, stage: Stage) -> None:
        self.stage = stage
        self.block = CHAIN[FOCUS_BLOCK]

    def run(self) -> None:
        self.d1_open_block()
        self.d2_block_hash()

    def _header_rows(self) -> VGroup:
        h = self.block.header
        when = datetime.fromtimestamp(h.timestamp, tz=UTC).strftime("%Y-%m-%d %H:%M UTC")
        spec = [
            ("Versión", "4 B", str(h.version)),
            ("Hash anterior", "32 B", short_hex(h.prev_hash, VALUE_CHARS) + "…"),
            ("Raíz de Merkle", "32 B", short_hex(h.merkle_root, VALUE_CHARS) + "…"),
            ("Timestamp", "4 B", when),
            ("Dificultad", "4 B", f"{h.bits:08x}"),
            ("Nonce", "4 B", str(h.nonce)),
        ]
        rows = VGroup()
        for name, size, value in spec:
            rows.add(
                VGroup(
                    label(name, 0.4),
                    mono(size, 0.36, color=theme.MUTED),
                    mono(value, 0.38, color=theme.ACCENT),
                )
            )
        rows.arrange(DOWN, buff=0.17, aligned_edge=LEFT)
        for row in rows:
            row[1].set_x(-1.2, direction=LEFT)
            row[2].set_x(0.2, direction=LEFT)
            row[0].set_x(-4.6, direction=LEFT)
        return rows

    def d1_open_block(self) -> None:
        s = self.stage.scene
        s.next_section("D1_abrir_bloque")
        cube = self.stage.focus
        if cube is None:
            msg = "La sección C debe entregar el cubo del bloque en stage.focus"
            raise RuntimeError(msg)
        self.stage.swap_title("Anatomía de un bloque", "Cabecera + cuerpo", keep=[cube])

        header_frame = box(HEADER_W, 3.25)
        header_title = label("CABECERA · 80 bytes", 0.42, color=theme.ACCENT, bold=True)
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

        s.play(cube.animate.scale(1.6).move_to(DOWN * 0.3), run_time=0.7)
        s.play(
            ReplacementTransform(cube, VGroup(header_frame, body_frame)),
            run_time=1.0,
        )
        s.play(FadeIn(header_title), FadeIn(body_title), run_time=0.5)
        s.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.2) for r in rows], lag_ratio=0.15))
        s.play(LaggedStart(*[FadeIn(t) for t in txs], lag_ratio=0.08), run_time=1)

        prev_box = SurroundingRectangle(rows[1], color=theme.ACCENT, buff=0.06)
        prev_note = label("← bloque anterior", 0.32, color=theme.ACCENT)
        prev_note.set_x(header_frame.get_right()[0] - 0.25, direction=RIGHT).match_y(rows[1])
        s.play(FadeIn(prev_box), FadeIn(prev_note), run_time=0.7)
        s.wait(0.6)
        root_box = SurroundingRectangle(rows[2], color=theme.ACCENT, buff=0.06)
        root_note = label("← resume el cuerpo", 0.32, color=theme.ACCENT)
        root_note.set_x(header_frame.get_right()[0] - 0.25, direction=RIGHT).match_y(rows[2])
        s.play(
            ReplacementTransform(prev_box, root_box),
            ReplacementTransform(prev_note, root_note),
            run_time=0.7,
        )
        s.wait(0.6)
        mining = VGroup(rows[4], rows[5])
        mining_note = label("minería → Int. 6", 0.3, color=theme.MUTED)
        mining_note.set_x(header_frame.get_right()[0] - 0.25, direction=RIGHT).match_y(mining)
        s.play(
            mining.animate.set_opacity(0.45),
            FadeIn(mining_note),
            root_box.animate.set_opacity(0),
            root_note.animate.set_opacity(0),
            run_time=0.7,
        )
        self.header, self.body, self.rows = header, body, rows
        self.notes = VGroup(root_box, root_note, mining_note)
        s.wait(1.2)

    def d2_block_hash(self) -> None:
        s = self.stage.scene
        s.next_section("D2_hash_de_cabecera")
        s.play(
            VGroup(self.header, self.body)
            .animate.scale(0.72)
            .to_edge(LEFT, buff=0.4)
            .shift(DOWN * 0.15),
            self.notes.animate.set_opacity(0),
            run_time=0.9,
        )
        hasher = box(2.3, 0.8, color=theme.ACCENT)
        hasher_text = label("SHA-256²", 0.48, color=theme.ACCENT, bold=True).move_to(hasher)
        engine = VGroup(hasher, hasher_text).move_to(RIGHT * 4.6 + UP * 1.0)
        arrow_in = Arrow(self.header.get_right(), engine.get_left(), color=theme.ACCENT, buff=0.15)
        s.play(FadeIn(engine), Write(arrow_in), run_time=0.8)

        result_label = label("Hash del bloque", 0.4, color=theme.MUTED)
        digest = hash_chars(short_hex(self.block.hash, 12), 0.5)
        result = VGroup(result_label, digest).arrange(DOWN, buff=0.18)
        result.next_to(engine, DOWN, buff=0.9)
        arrow_out = Arrow(engine.get_bottom(), result.get_top(), color=theme.ACCENT, buff=0.1)
        s.play(Write(arrow_out), FadeIn(result_label), Write(digest), run_time=1.0)
        s.wait(0.5)

        question = label("¿Y las transacciones?", 0.5, color=theme.DANGER, bold=True)
        question.next_to(result, DOWN, buff=0.8)
        s.play(self.body.animate.set_opacity(0.25), FadeIn(question, shift=UP * 0.2))
        s.play(
            Circumscribe(self.rows[2], color=theme.ACCENT, time_width=0.6),
            run_time=1.4,
        )
        s.play(Circumscribe(self.rows[2], color=theme.ACCENT, time_width=0.6), run_time=1.2)
        s.wait(1.2)
