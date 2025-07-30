from definit_db_py.data.field.computer_science.definitions.algorithms.problems.graph_labeling.graph_coloring import (
    GRAPH_COLORING,
)
from definit_db_py.data.field.mathematics.definitions.graph.node import NODE
from definit_db_py.definition.definition import Definition
from definit_db_py.definition.definition_key import DefinitionKey
from definit_db_py.definition.field import Field


class _VertexColoring(Definition):
    def _get_content(self) -> str:
        return f"A specific type of {GRAPH_COLORING.key.get_reference(phrase='graph coloring')} where the goal is to ensure that no two connected {NODE.key.get_reference(phrase='nodes')} share the same color."


VERTEX_COLORING = _VertexColoring(
    key=DefinitionKey(
        name="vertex_coloring",
        field=Field.COMPUTER_SCIENCE,
    )
)
