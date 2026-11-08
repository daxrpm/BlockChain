"""Parte 3 (estructura de datos y ledger): una escena, un clip por beat del guion.

`--save_sections` produce un clip por beat; el último fotograma de cada clip es el primero
del siguiente, así en Canva se ve como una sola animación que espera al expositor.
"""

from manim import Scene

from ledger_viz.part3_script import SECTIONS
from ledger_viz.scenes.narrator import Narrator
from ledger_viz.scenes.sections.a_ledger import LedgerSection
from ledger_viz.scenes.sections.b_transaction import TransactionSection
from ledger_viz.scenes.sections.bridge import BridgeSection, ClosingSection
from ledger_viz.scenes.sections.c_blocks import BlocksSection
from ledger_viz.scenes.sections.chain import ChainSection
from ledger_viz.scenes.sections.common import Stage
from ledger_viz.scenes.sections.d_structure import StructureSection
from ledger_viz.scenes.sections.e_merkle import MerkleSection
from ledger_viz.viz.components import title_bar


class Part3(Scene):
    def construct(self) -> None:
        stage = Stage(
            self,
            title_bar(
                "Estructura de datos y Ledger", "¿Qué guarda un blockchain y cómo lo organiza?"
            ),
        )
        narrator = Narrator(self, SECTIONS, clip_per_beat=True)
        for section in (
            BridgeSection,
            LedgerSection,
            TransactionSection,
            BlocksSection,
            ChainSection,
            StructureSection,
            MerkleSection,
            ClosingSection,
        ):
            section(stage, narrator).run()
