from definit_db_py.data.field.computer_science.definitions.data_structure.primitive.integer import INTEGER
from definit_db_py.data.field.mathematics.definitions.foundamental.notations.label import LABEL
from definit_db_py.data.field.mathematics.definitions.graph.edge import EDGE
from definit_db_py.data.field.mathematics.definitions.graph.graph import GRAPH
from definit_db_py.data.field.mathematics.definitions.graph.node import NODE
from definit_db_py.data.field.mathematics.definitions.problem.problem import PROBLEM
from definit_db_py.definition.definition import Definition
from definit_db_py.definition.definition_key import DefinitionKey
from definit_db_py.definition.field import Field


class _GraphLabeling(Definition):
    def _get_content(self) -> str:
        return f"A {PROBLEM.key.get_reference()} of assigning {LABEL.key.get_reference(phrase='labels')}, traditionally represented by {INTEGER.key.get_reference(phrase='integers')}, to {EDGE.key.get_reference(phrase='edges')} and/or {NODE.key.get_reference(phrase='nodes')} of a {GRAPH.key.get_reference(phrase='graph')}."


GRAPH_LABELING = _GraphLabeling(
    key=DefinitionKey(
        name="graph_labeling",
        field=Field.COMPUTER_SCIENCE,
    )
)
