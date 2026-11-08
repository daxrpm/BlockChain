"""Piezas visuales reutilizables con el lenguaje gráfico del Canva del grupo."""

import numpy as np
import numpy.typing as npt
from manim import (
    DOWN,
    LEFT,
    ORIGIN,
    RIGHT,
    UP,
    Arc,
    Circle,
    Dot,
    Line,
    Polygon,
    Rectangle,
    RoundedRectangle,
    Square,
    Text,
    VGroup,
    VMobject,
)
from manim.animation.animation import Animation
from manim.utils.color import ParsableManimColor

from ledger_viz.domain.hashing import short_hex
from ledger_viz.viz import theme


def label(
    text: str, size: float = 0.5, *, color: ParsableManimColor | None = None, bold: bool = False
) -> Text:
    return Text(
        text,
        font=theme.FONT_SANS,
        color=color or theme.TEXT,
        weight="BOLD" if bold else "NORMAL",
    ).scale(size)


def mono(text: str, size: float = 0.45, *, color: ParsableManimColor | None = None) -> Text:
    return Text(text, font=theme.FONT_MONO, color=color or theme.TEXT).scale(size)


def hash_text(digest: bytes, size: float = 0.45, *, chars: int = theme.HASH_CHARS) -> Text:
    return mono(short_hex(digest, chars), size, color=theme.ACCENT)


def hash_chars(
    hex_str: str, size: float = 0.5, *, color: ParsableManimColor | None = None
) -> VGroup:
    """Hash carácter por carácter con paso fijo, para poder colorear diferencias."""
    step = mono("0", size).width * 1.35
    chars = VGroup(
        *[
            mono(ch, size, color=color or theme.ACCENT).move_to(RIGHT * i * step)
            for i, ch in enumerate(hex_str.upper())
        ]
    )
    return chars.move_to(ORIGIN)


def phone(scale: float = 1.0) -> VGroup:
    body = RoundedRectangle(
        width=0.62, height=1.1, corner_radius=0.1, color=theme.TEXT, stroke_width=3
    )
    screen = Rectangle(width=0.48, height=0.78, color=theme.ACCENT, stroke_width=2)
    button = Dot(radius=0.035, color=theme.TEXT).next_to(screen, DOWN, buff=0.06)
    return VGroup(body, screen, button).scale(scale)


def title_bar(title: str, subtitle: str) -> VGroup:
    """Título superior centrado con el ícono de cuadritos del Canva."""
    squares = VGroup(
        *[Square(0.12, fill_opacity=1, stroke_width=0, color=theme.ACCENT) for _ in range(5)]
    )
    squares[0].shift(LEFT * 0.14 + UP * 0.07)
    squares[1].shift(UP * 0.07 + RIGHT * 0.14)
    squares[2].shift(LEFT * 0.28 + DOWN * 0.07)
    squares[3].shift(DOWN * 0.07)
    squares[4].shift(RIGHT * 0.28 + DOWN * 0.07)
    head = label(title.upper(), 0.62, bold=True)
    row = VGroup(squares, head).arrange(RIGHT, buff=0.3)
    sub = label(subtitle, 0.34, color=theme.MUTED)
    group = VGroup(row, sub).arrange(DOWN, buff=0.15)
    return group.to_edge(UP, buff=0.35)


def person(name: str, scale: float = 1.0) -> VGroup:
    """Silueta lineal como los íconos del Canva."""
    head = Circle(radius=0.28, color=theme.TEXT, stroke_width=4)
    body = Arc(radius=0.48, start_angle=0, angle=3.14159, color=theme.TEXT, stroke_width=4)
    body.next_to(head, DOWN, buff=0.08)
    base = Line(body.get_start(), body.get_end(), color=theme.TEXT, stroke_width=4)
    figure = VGroup(head, body, base)
    name_label = label(name, 0.4, bold=True).next_to(figure, DOWN, buff=0.12)
    return VGroup(figure, name_label).scale(scale)


def notebook(width: float, height: float, title: str = "LEDGER") -> VGroup:
    page = RoundedRectangle(
        width=width,
        height=height,
        corner_radius=0.15,
        stroke_color=theme.ACCENT,
        stroke_width=3,
        fill_color=theme.SURFACE,
        fill_opacity=1,
    )
    rings = VGroup(
        *[
            Circle(0.07, color=theme.ACCENT, stroke_width=3)
            for _ in range(max(3, int(height / 0.55)))
        ]
    ).arrange(DOWN, buff=(height - 0.6) / max(3, int(height / 0.55)) - 0.14)
    rings.move_to(page.get_left() + RIGHT * 0.25)
    head = label(title, 0.36, color=theme.ACCENT, bold=True)
    head.next_to(page.get_top(), DOWN, buff=0.22)
    rule = Line(
        page.get_left() + RIGHT * 0.5, page.get_right() + LEFT * 0.3, color=theme.MUTED
    ).next_to(head, DOWN, buff=0.15)
    rule.set_stroke(width=1.5)
    return VGroup(page, rings, head, rule)


def wire_cube(
    size: float = 1.0,
    color: ParsableManimColor | None = None,
    stroke: float = 4,
    *,
    filled: bool = True,
) -> VGroup:
    """Cubo isométrico de alambre, igual al de la portada."""
    c = color or theme.ACCENT
    w, d = size * 0.866, size * 0.5
    top = [UP * 2 * d, RIGHT * w + UP * d, ORIGIN, LEFT * w + UP * d]
    top_face = Polygon(*top, color=c, stroke_width=stroke)
    left_face = Polygon(
        top[3], top[2], top[2] + DOWN * size, top[3] + DOWN * size, color=c, stroke_width=stroke
    )
    right_face = Polygon(
        top[2], top[1], top[1] + DOWN * size, top[2] + DOWN * size, color=c, stroke_width=stroke
    )
    cube = VGroup(top_face, left_face, right_face)
    for face in cube:
        face.set_fill(theme.BG, opacity=1 if filled else 0)
    return cube.move_to(ORIGIN)


def box(
    width: float,
    height: float,
    *,
    color: ParsableManimColor | None = None,
    fill: ParsableManimColor | None = None,
    fill_opacity: float = 1.0,
    stroke: float = 3,
) -> RoundedRectangle:
    return RoundedRectangle(
        width=width,
        height=height,
        corner_radius=0.12,
        stroke_color=color or theme.ACCENT,
        stroke_width=stroke,
        fill_color=fill or theme.SURFACE,
        fill_opacity=fill_opacity,
    )


def node_icon(scale: float = 1.0) -> VGroup:
    """Servidor estilizado (nodo de la red)."""
    slabs = VGroup(
        *[Rectangle(width=0.9, height=0.26, color=theme.TEXT, stroke_width=3) for _ in range(3)]
    ).arrange(DOWN, buff=0.05)
    leds = VGroup(
        *[Dot(radius=0.035, color=theme.ACCENT).move_to(s.get_right() + LEFT * 0.14) for s in slabs]
    )
    return VGroup(slabs, leds).scale(scale)


def cross(size: float = 0.6, color: ParsableManimColor | None = None) -> VGroup:
    c = color or theme.DANGER
    a = Line(
        UP * size / 2 + LEFT * size / 2, DOWN * size / 2 + RIGHT * size / 2, color=c, stroke_width=8
    )
    b = Line(
        UP * size / 2 + RIGHT * size / 2, DOWN * size / 2 + LEFT * size / 2, color=c, stroke_width=8
    )
    return VGroup(a, b)


def check(size: float = 0.6, color: ParsableManimColor | None = None) -> VMobject:
    c = color or theme.OK
    mark = VMobject(color=c, stroke_width=8)
    mark.set_points_as_corners(
        [LEFT * size / 2, DOWN * size / 3 + LEFT * size / 10, UP * size / 2 + RIGHT * size / 2]
    )
    return mark


def point(x: float, y: float, z: float = 0.0) -> npt.NDArray[np.float64]:
    return np.array([x, y, z], dtype=np.float64)


def as_anim(builder: object) -> Animation:
    """`mob.animate` está tipado en manim como `Self`; en tiempo de ejecución es un builder."""
    if isinstance(builder, Animation):
        return builder
    build = getattr(builder, "build", None)
    if build is None:
        msg = f"Se esperaba una animación o `.animate`, se recibió {type(builder).__name__}"
        raise TypeError(msg)
    return build()
