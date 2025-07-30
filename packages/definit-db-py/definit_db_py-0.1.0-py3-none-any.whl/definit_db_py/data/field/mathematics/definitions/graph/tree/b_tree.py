from definit_db_py.data.field.mathematics.definitions.graph.node import NODE
from definit_db_py.data.field.mathematics.definitions.graph.tree.subtree import SUBTREE
from definit_db_py.data.field.mathematics.definitions.graph.tree.tree import TREE
from definit_db_py.definition.definition import Definition
from definit_db_py.definition.definition_key import DefinitionKey
from definit_db_py.definition.field import Field


class _BTree(Definition):
    def _get_content(self) -> str:
        return (
            f"A self-balancing {TREE.key.get_reference(phrase='tree')} data structure in which each {NODE.key.get_reference(phrase='node')} has a value, "
            f"and for each node, the values of all nodes in its left {SUBTREE.key.get_reference(phrase='subtree')} are less than its own value, "
            "and the values of all nodes in its right subtree are greater than its own value. This property allows for efficient searching, insertion, and deletion operations."
        )


B_TREE = _BTree(
    key=DefinitionKey(
        name="b_tree",
        field=Field.MATHEMATICS,
    )
)
