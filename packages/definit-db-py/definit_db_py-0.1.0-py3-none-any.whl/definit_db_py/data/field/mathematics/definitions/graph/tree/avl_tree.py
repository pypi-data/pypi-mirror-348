from definit_db_py.data.field.mathematics.definitions.graph.node import NODE
from definit_db_py.data.field.mathematics.definitions.graph.tree.b_tree import B_TREE
from definit_db_py.data.field.mathematics.definitions.graph.tree.binary_search_tree import BINARY_SEARCH_TREE
from definit_db_py.data.field.mathematics.definitions.graph.tree.subtree import SUBTREE
from definit_db_py.definition.definition import Definition
from definit_db_py.definition.definition_key import DefinitionKey
from definit_db_py.definition.field import Field


class _AVLTree(Definition):
    def _get_content(self) -> str:
        return (
            f"A type of {B_TREE.key.get_reference(phrase='self-balancing')} {BINARY_SEARCH_TREE.key.get_reference(phrase='binary search tree')} where the difference in heights between the left and right "
            f"{SUBTREE.key.get_reference(phrase='subtrees')} of any {NODE.key.get_reference(phrase='node')} is at most one. "
            "This property ensures that the tree remains approximately balanced, allowing for efficient search, insertion, and deletion operations. "
            "The AVL tree is named after its inventors, Georgy Adelson-Velsky and Evgenii Landis."
        )


AVL_TREE = _AVLTree(
    key=DefinitionKey(
        name="avl_tree",
        field=Field.MATHEMATICS,
    )
)
