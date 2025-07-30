from definit_db_py.data.field.mathematics.definitions.foundamental.set import SET
from definit_db_py.data.field.mathematics.definitions.graph.edge import EDGE
from definit_db_py.data.field.mathematics.definitions.graph.graph import GRAPH
from definit_db_py.data.field.mathematics.definitions.graph.node import NODE
from definit_db_py.definition.definition import Definition
from definit_db_py.definition.definition_key import DefinitionKey
from definit_db_py.definition.field import Field


class _BipartiteGraph(Definition):
    def _get_content(self) -> str:
        return (
            f"A {GRAPH.key.get_reference(phrase='graph')} whose {NODE.key.get_reference(phrase='nodes')} can be divided into two disjoint "
            f"{SET.key.get_reference(phrase='sets')} such that every {EDGE.key.get_reference(phrase='edge')} connects a node in one set to a node in the other set. "
            "In other words, there are no edges connecting nodes within the same set."
        )


BIPARTITE_GRAPH = _BipartiteGraph(
    key=DefinitionKey(
        name="bipartite_graph",
        field=Field.MATHEMATICS,
    )
)
