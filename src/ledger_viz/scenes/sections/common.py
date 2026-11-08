"""Estado compartido entre secciones y transición estándar de título."""

from collections.abc import Iterable
from dataclasses import dataclass

from manim import FadeOut, Mobject, Scene, Transform, VGroup, VMobject

from ledger_viz.viz.components import title_bar


@dataclass
class Stage:
    scene: Scene
    title: VGroup
    focus: VMobject | None = None  # mobjeto que una sección entrega a la siguiente

    def swap_title(
        self, title: str, subtitle: str, *, keep: Iterable[Mobject] = (), run_time: float = 1.0
    ) -> None:
        """Desvanece todo salvo `keep` y transforma el título actual en el nuevo."""
        kept = {id(m) for m in keep} | {id(self.title)}
        fades = [FadeOut(m) for m in self.scene.mobjects if id(m) not in kept]
        self.scene.play(
            *fades, Transform(self.title, title_bar(title, subtitle)), run_time=run_time
        )
