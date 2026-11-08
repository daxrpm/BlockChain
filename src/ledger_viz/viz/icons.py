"""Íconos lineales al estilo de la plantilla Canva (sobre fondo oscuro o tarjeta amarilla)."""

import math

from manim import (
    DOWN,
    LEFT,
    PI,
    RIGHT,
    UP,
    Arc,
    Circle,
    Ellipse,
    Line,
    Polygon,
    Rectangle,
    RoundedRectangle,
    Text,
    VGroup,
    VMobject,
)
from manim.utils.color import ParsableManimColor

from ledger_viz.viz import theme

STROKE = 5


def _c(color: ParsableManimColor | None) -> ParsableManimColor:
    return color if color is not None else theme.TEXT


def bank(color: ParsableManimColor | None = None) -> VGroup:
    c = _c(color)
    roof = Polygon(LEFT * 1.0 + UP * 0.55, RIGHT * 1.0 + UP * 0.55, UP * 1.05, color=c)
    beam = Rectangle(width=2.0, height=0.14, color=c).next_to(roof, DOWN, buff=0)
    cols = VGroup(*[Rectangle(width=0.18, height=0.85, color=c) for _ in range(4)])
    cols.arrange(RIGHT, buff=0.3).next_to(beam, DOWN, buff=0.05)
    base = Rectangle(width=2.1, height=0.16, color=c).next_to(cols, DOWN, buff=0.05)
    icon = VGroup(roof, beam, cols, base)
    icon.set_stroke(c, width=STROKE)
    return icon.move_to((0, 0, 0))


def database(color: ParsableManimColor | None = None, *, disks: int = 3) -> VGroup:
    c = _c(color)
    w, h = 1.4, 0.38
    parts = VGroup()
    top = Ellipse(width=w, height=h, color=c)
    parts.add(top)
    for i in range(1, disks + 1):
        y = -i * 0.42
        arc = Arc(radius=1, start_angle=PI, angle=PI, color=c).stretch(w / 2, 0).stretch(h / 2, 1)
        arc.move_to((0, y - h / 4, 0))
        parts.add(arc)
    side_l = Line(top.get_left(), top.get_left() + DOWN * disks * 0.42, color=c)
    side_r = Line(top.get_right(), top.get_right() + DOWN * disks * 0.42, color=c)
    parts.add(side_l, side_r)
    parts.set_stroke(c, width=STROKE)
    return parts.move_to((0, 0, 0))


def coin(symbol: str = "₿", color: ParsableManimColor | None = None) -> VGroup:
    c = _c(color)
    outer = Circle(radius=0.5, color=c, stroke_width=STROKE)
    inner = Circle(radius=0.38, color=c, stroke_width=2.5)
    mark = Text(symbol, font=theme.FONT_SANS, weight="BOLD", color=c).scale(0.55)
    return VGroup(outer, inner, mark)


def document(title: str = "", lines: int = 4, color: ParsableManimColor | None = None) -> VGroup:
    c = _c(color)
    w, h, fold = 1.3, 1.65, 0.32
    page = Polygon(
        LEFT * w / 2 + UP * h / 2,
        RIGHT * (w / 2 - fold) + UP * h / 2,
        RIGHT * w / 2 + UP * (h / 2 - fold),
        RIGHT * w / 2 + DOWN * h / 2,
        LEFT * w / 2 + DOWN * h / 2,
        color=c,
        stroke_width=STROKE,
    )
    corner = VMobject(color=c, stroke_width=3).set_points_as_corners(
        [
            RIGHT * (w / 2 - fold) + UP * h / 2,
            RIGHT * (w / 2 - fold) + UP * (h / 2 - fold),
            RIGHT * w / 2 + UP * (h / 2 - fold),
        ]
    )
    rows = VGroup(
        *[
            Line(LEFT * 0.42, RIGHT * (0.42 - 0.12 * (i % 2)), color=c, stroke_width=3)
            for i in range(lines)
        ]
    ).arrange(DOWN, buff=0.2, aligned_edge=LEFT)
    rows.move_to(page).shift(DOWN * 0.15)
    group = VGroup(page, corner, rows)
    if title:
        group.add(
            Text(title, font=theme.FONT_SANS, weight="BOLD", color=c)
            .scale(0.22)
            .next_to(page.get_top(), DOWN, buff=0.18)
            .shift(LEFT * 0.12)
        )
    return group


def shield_check(color: ParsableManimColor | None = None) -> VGroup:
    c = _c(color)
    shield = VMobject(color=c, stroke_width=STROKE)
    shield.set_points_smoothly(
        [UP * 0.75, RIGHT * 0.6 + UP * 0.55, RIGHT * 0.55 + DOWN * 0.15, DOWN * 0.8]
    )
    left = shield.copy().flip(UP).align_to(shield, RIGHT).shift(LEFT * shield.width)
    left.move_to(shield.get_center() + LEFT * shield.width)
    outline = VGroup(shield, left)
    outline.move_to((0, 0, 0))
    tick = VMobject(color=c, stroke_width=STROKE).set_points_as_corners(
        [LEFT * 0.28 + UP * 0.02, LEFT * 0.06 + DOWN * 0.22, RIGHT * 0.3 + UP * 0.25]
    )
    return VGroup(outline, tick)


def padlock(color: ParsableManimColor | None = None) -> VGroup:
    c = _c(color)
    body = RoundedRectangle(width=1.1, height=0.85, corner_radius=0.1, color=c)
    shackle = Arc(radius=0.36, start_angle=0, angle=PI, color=c).next_to(body, UP, buff=-0.02)
    legs = VGroup(
        Line(shackle.get_start(), shackle.get_start() + DOWN * 0.18, color=c),
        Line(shackle.get_end(), shackle.get_end() + DOWN * 0.18, color=c),
    )
    hole = (
        VGroup(Circle(radius=0.09, color=c), Line(DOWN * 0.08, DOWN * 0.25, color=c))
        .move_to(body)
        .shift(UP * 0.05)
    )
    icon = VGroup(body, shackle, legs, hole)
    icon.set_stroke(c, width=STROKE)
    return icon.move_to((0, 0, 0))


def key(color: ParsableManimColor | None = None) -> VGroup:
    c = _c(color)
    ring = Circle(radius=0.28, color=c)
    shaft = Line(ring.get_right(), ring.get_right() + RIGHT * 0.9, color=c)
    teeth = VGroup(
        Line(shaft.get_end(), shaft.get_end() + DOWN * 0.22, color=c),
        Line(shaft.get_end() + LEFT * 0.22, shaft.get_end() + LEFT * 0.22 + DOWN * 0.16, color=c),
    )
    icon = VGroup(ring, shaft, teeth)
    icon.set_stroke(c, width=STROKE)
    return icon.move_to((0, 0, 0))


def fingerprint(color: ParsableManimColor | None = None) -> VGroup:
    c = _c(color)
    arcs = VGroup(
        *[
            Arc(
                radius=0.12 + 0.11 * i, start_angle=PI * 0.15, angle=PI * (1.25 - 0.05 * i), color=c
            )
            for i in range(5)
        ]
    )
    arcs.set_stroke(c, width=3.5)
    return arcs.move_to((0, 0, 0))


def gear(color: ParsableManimColor | None = None) -> VGroup:
    c = _c(color)
    ring = Circle(radius=0.42, color=c)
    hub = Circle(radius=0.16, color=c)
    teeth = VGroup()
    for k in range(8):
        a = k * PI / 4
        direction = RIGHT * math.cos(a) + UP * math.sin(a)
        teeth.add(Line(direction * 0.42, direction * 0.6, color=c))
    icon = VGroup(ring, hub, teeth)
    icon.set_stroke(c, width=STROKE)
    return icon


def chip(color: ParsableManimColor | None = None) -> VGroup:
    c = _c(color)
    core = RoundedRectangle(width=0.9, height=0.9, corner_radius=0.08, color=c)
    inner = RoundedRectangle(width=0.45, height=0.45, corner_radius=0.04, color=c)
    pins = VGroup()
    for i in range(4):
        off = -0.33 + i * 0.22
        pins.add(
            Line(UP * 0.45 + RIGHT * off, UP * 0.65 + RIGHT * off, color=c),
            Line(DOWN * 0.45 + RIGHT * off, DOWN * 0.65 + RIGHT * off, color=c),
            Line(LEFT * 0.45 + UP * off, LEFT * 0.65 + UP * off, color=c),
            Line(RIGHT * 0.45 + UP * off, RIGHT * 0.65 + UP * off, color=c),
        )
    icon = VGroup(core, inner, pins)
    icon.set_stroke(c, width=4)
    return icon


def people(color: ParsableManimColor | None = None) -> VGroup:
    """Grupo de tres personas (participantes / consenso)."""
    c = _c(color)

    def one(scale: float) -> VGroup:
        head = Circle(radius=0.2, color=c)
        body = Arc(radius=0.34, start_angle=0, angle=PI, color=c).next_to(head, DOWN, buff=0.05)
        return VGroup(head, body).scale(scale)

    back_l, back_r, front = one(0.85), one(0.85), one(1.0)
    back_l.shift(LEFT * 0.45 + UP * 0.15)
    back_r.shift(RIGHT * 0.45 + UP * 0.15)
    group = VGroup(back_l, back_r, front)
    group.set_stroke(c, width=STROKE)
    return group.move_to((0, 0, 0))


def chart_up(color: ParsableManimColor | None = None) -> VGroup:
    c = _c(color)
    bars = VGroup(*[Rectangle(width=0.2, height=0.2 + 0.18 * i, color=c) for i in range(5)])
    bars.arrange(RIGHT, buff=0.08, aligned_edge=DOWN)
    arrow = VMobject(color=c).set_points_as_corners(
        [bars.get_corner(DOWN + LEFT) + UP * 0.5, bars.get_corner(UP + RIGHT) + UP * 0.25]
    )
    head = VMobject(color=c).set_points_as_corners(
        [
            arrow.get_end() + LEFT * 0.18,
            arrow.get_end(),
            arrow.get_end() + DOWN * 0.18,
        ]
    )
    icon = VGroup(bars, arrow, head)
    icon.set_stroke(c, width=STROKE - 1)
    return icon.move_to((0, 0, 0))


def scroll_contract(color: ParsableManimColor | None = None) -> VGroup:
    c = _c(color)
    doc = document(lines=3, color=c)
    code = Text("SI → ENTONCES", font=theme.FONT_MONO, color=c).scale(0.2)
    code.move_to(doc[0]).shift(UP * 0.48)
    return VGroup(doc, code)


def question_bubble(text: str, color: ParsableManimColor | None = None) -> VGroup:
    c = _c(color)
    label = Text(text, font=theme.FONT_SANS, weight="BOLD", color=c).scale(0.4)
    frame = RoundedRectangle(
        width=label.width + 0.5, height=label.height + 0.4, corner_radius=0.2, color=c
    )
    tail = Polygon(
        frame.get_bottom() + LEFT * 0.25,
        frame.get_bottom() + LEFT * 0.05,
        frame.get_bottom() + LEFT * 0.35 + DOWN * 0.25,
        color=c,
    )
    frame.set_stroke(c, width=3)
    tail.set_stroke(c, width=3)
    return VGroup(frame, tail, label.move_to(frame))


def pen(color: ParsableManimColor | None = None) -> VGroup:
    c = _c(color)
    body = Rectangle(width=0.22, height=1.0, color=c)
    tip = Polygon(
        body.get_corner(DOWN + LEFT),
        body.get_corner(DOWN + RIGHT),
        body.get_bottom() + DOWN * 0.3,
        color=c,
    )
    icon = VGroup(body, tip).rotate(-PI / 4)
    icon.set_stroke(c, width=4)
    return icon


def signature(color: ParsableManimColor | None = None) -> VMobject:
    c = _c(color)
    curve = VMobject(color=c, stroke_width=3.5)
    pts = [LEFT * 0.6 + RIGHT * 0.1 * i + UP * 0.12 * math.sin(i * 1.3) for i in range(13)]
    curve.set_points_smoothly(pts)
    return curve


def magnifier(color: ParsableManimColor | None = None) -> VGroup:
    c = _c(color)
    lens = Circle(radius=0.32, color=c)
    handle = Line(
        lens.point_at_angle(-PI / 4), lens.point_at_angle(-PI / 4) + (RIGHT + DOWN) * 0.3, color=c
    )
    icon = VGroup(lens, handle)
    icon.set_stroke(c, width=STROKE)
    return icon


def layers_icon(color: ParsableManimColor | None = None) -> VGroup:
    c = _c(color)
    slabs = VGroup(
        *[
            Polygon(LEFT * 0.6, UP * 0.25, RIGHT * 0.6, DOWN * 0.25, color=c).shift(UP * 0.22 * i)
            for i in range(3)
        ]
    )
    slabs.set_stroke(c, width=4)
    return slabs.move_to((0, 0, 0))


def hacker(color: ParsableManimColor | None = None) -> VGroup:
    """Silueta con capucha (atacante)."""
    c = _c(color or theme.DANGER)
    hood = Arc(radius=0.42, start_angle=0, angle=PI, color=c)
    face = Circle(radius=0.22, color=c).move_to(hood.get_center() + DOWN * 0.02)
    shoulders = Arc(radius=0.55, start_angle=0, angle=PI, color=c).next_to(face, DOWN, buff=0.18)
    icon = VGroup(hood, face, shoulders)
    icon.set_stroke(c, width=STROKE)
    return icon.move_to((0, 0, 0))
