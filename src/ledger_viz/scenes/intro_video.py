"""Video de Integrante 1 (introducción y fundamentos), sincronizado con su guion.

Una sola escena: el render normal da el video completo y `--save_sections`
da además un clip por diapositiva.
"""

from manim import Scene

from ledger_viz.scenes.intro.narrator import Narrator
from ledger_viz.scenes.intro.part_a import IntroPartA
from ledger_viz.scenes.intro.part_b import IntroPartB
from ledger_viz.scenes.intro.part_c import IntroPartC
from ledger_viz.scenes.sections.common import Stage
from ledger_viz.viz.components import title_bar


class IntroVideo(Scene):
    def construct(self) -> None:
        stage = Stage(
            self, title_bar("El problema de confianza", "¿Por qué necesitamos Blockchain?")
        )
        narrator = Narrator(self)
        IntroPartA(stage, narrator).run()
        IntroPartB(stage, narrator).run()
        IntroPartC(stage, narrator).run()
