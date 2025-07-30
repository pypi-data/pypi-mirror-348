from definit_db_py.data.field.mathematics.definitions.graph.cycle import CYCLE
from definit_db_py.data.field.mathematics.definitions.graph.directed_graph import DIRECTED_GRAPH
from definit_db_py.definition.definition import Definition
from definit_db_py.definition.definition_key import DefinitionKey
from definit_db_py.definition.field import Field


class _DirectedAcyclicGraph(Definition):
    def _get_content(self) -> str:
        return (
            f"A directed acyclic graph is a {DIRECTED_GRAPH.key.get_reference(phrase='directed graph')} with no "
            f"{CYCLE.key.get_reference(phrase='cycles')}."
        )


DIRECTED_ACYCLIC_GRAPH = _DirectedAcyclicGraph(
    key=DefinitionKey(
        name="directed_acyclic_graph",
        field=Field.MATHEMATICS,
    )
)
