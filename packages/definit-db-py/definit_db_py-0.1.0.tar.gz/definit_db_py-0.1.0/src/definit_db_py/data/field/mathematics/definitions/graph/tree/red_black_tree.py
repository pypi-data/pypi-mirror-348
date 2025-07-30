from definit_db_py.data.field.mathematics.definitions.graph.node import NODE
from definit_db_py.data.field.mathematics.definitions.graph.tree.b_tree import B_TREE
from definit_db_py.data.field.mathematics.definitions.graph.tree.binary_search_tree import BINARY_SEARCH_TREE
from definit_db_py.data.field.mathematics.definitions.graph.tree.leaf import LEAF
from definit_db_py.definition.definition import Definition
from definit_db_py.definition.definition_key import DefinitionKey
from definit_db_py.definition.field import Field


class _RedBlackTree(Definition):
    def _get_content(self) -> str:
        return (
            f"A type of {B_TREE.key.get_reference(phrase='self-balancing')} {BINARY_SEARCH_TREE.key.get_reference(phrase='binary search tree')}. "
            f"The red-black tree is named after the colors used to represent the {NODE.key.get_reference(phrase='nodes')}. "
            "The tree maintains certain properties to ensure that it remains approximately balanced, allowing for efficient search, insertion, and deletion operations. "
            "The properties include: 1. Each node is either red or black. 2. The root node is always black. 3. All "
            f"{LEAF.key.get_reference(phrase='leaves')} are black. 4. If a red node has children, then both children are black. "
            "5. Every path from a node to its descendant leaves has the same number of black nodes. "
            "These properties ensure that the tree remains approximately balanced, allowing for efficient search, insertion, and deletion operations."
        )


RED_BLACK_TREE = _RedBlackTree(
    key=DefinitionKey(
        name="red_black_tree",
        field=Field.MATHEMATICS,
    )
)
