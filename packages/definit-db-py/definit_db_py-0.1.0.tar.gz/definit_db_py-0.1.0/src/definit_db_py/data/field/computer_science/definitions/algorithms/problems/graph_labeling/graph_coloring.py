from definit_db_py.data.field.computer_science.definitions.algorithms.problems.graph_labeling.graph_labeling import (
    GRAPH_LABELING,
)
from definit_db_py.data.field.mathematics.definitions.foundamental.notations.label import LABEL
from definit_db_py.definition.definition import Definition
from definit_db_py.definition.definition_key import DefinitionKey
from definit_db_py.definition.field import Field


class _GraphColoring(Definition):
    def _get_content(self) -> str:
        return (
            f"A special case of {GRAPH_LABELING.key.get_reference(phrase='graph labeling')} where the "
            f"{LABEL.key.get_reference(phrase='labels')} are colors."
        )


GRAPH_COLORING = _GraphColoring(
    key=DefinitionKey(
        name="graph_coloring",
        field=Field.COMPUTER_SCIENCE,
    )
)
