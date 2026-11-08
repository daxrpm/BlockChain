"""Sincroniza la animación con el guion: cada beat dura al menos su tiempo de lectura."""

from manim import DOWN, RoundedRectangle, VGroup, VMobject

from ledger_viz.scenes.narrator import Narrator
from ledger_viz.viz import theme
from ledger_viz.viz.components import label

__all__ = ["Narrator", "yellow_card"]


def yellow_card(
    icon: VMobject, title: str, *, width: float = 3.4, height: float = 3.0, caption: str = ""
) -> VGroup:
    """Tarjeta amarilla con ícono oscuro, como las diapositivas del Canva."""
    card = RoundedRectangle(
        width=width,
        height=height,
        corner_radius=0.18,
        fill_color=theme.ACCENT,
        fill_opacity=1,
        stroke_width=0,
    )
    icon.set_color(theme.BG)
    icon.scale_to_fit_height(min(icon.height, height * 0.42))
    head = label(title, 0.5, color=theme.BG, bold=True)
    if head.width > width - 0.4:
        head.scale_to_fit_width(width - 0.4)
    parts = VGroup(icon, head)
    if caption:
        parts.add(label(caption, 0.32, color=theme.BG))
    parts.arrange(DOWN, buff=0.22).move_to(card)
    return VGroup(card, *parts)
