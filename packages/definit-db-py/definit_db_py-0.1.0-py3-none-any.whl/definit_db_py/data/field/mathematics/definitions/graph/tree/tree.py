from definit_db_py.data.field.mathematics.definitions.graph.directed_acyclic_graph import DIRECTED_ACYCLIC_GRAPH
from definit_db_py.data.field.mathematics.definitions.graph.node import NODE
from definit_db_py.definition.definition import Definition
from definit_db_py.definition.definition_key import DefinitionKey
from definit_db_py.definition.field import Field


class _Tree(Definition):
    def _get_content(self) -> str:
        return (
            f"A tree is a {DIRECTED_ACYCLIC_GRAPH.key.get_reference(phrase='directed acyclic graph')} with the restriction that a child can only have one parent. "
            f"Each tree has a root {NODE.key.get_reference(phrase='node')}, which is the topmost node in the hierarchy, and each node can have zero or more child nodes. "
            "Each node has only one parent node, except for the root node, which has no parent."
        )


TREE = _Tree(
    key=DefinitionKey(
        name="tree",
        field=Field.MATHEMATICS,
    )
)
