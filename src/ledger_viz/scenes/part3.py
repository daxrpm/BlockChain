"""Escena única de la parte 3. Cada `next_section` es un clip para una diapositiva de Canva.

Renderizar con `--save_sections` garantiza que el último fotograma de un clip
sea el primero del siguiente.
"""

from manim import Scene

from ledger_viz.scenes.sections.a_ledger import LedgerSection
from ledger_viz.scenes.sections.b_transaction import TransactionSection
from ledger_viz.scenes.sections.c_blocks import BlocksSection
from ledger_viz.scenes.sections.common import Stage
from ledger_viz.scenes.sections.d_structure import StructureSection
from ledger_viz.scenes.sections.e_merkle import MerkleSection


class Part3(Scene):
    def construct(self) -> None:
        ledger = LedgerSection(self)
        ledger.run()
        stage = Stage(self, ledger.title)
        TransactionSection(stage).run()
        BlocksSection(stage).run()
        StructureSection(stage).run()
        MerkleSection(stage).run()
