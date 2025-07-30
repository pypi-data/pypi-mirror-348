from definit_db_py.data.field.mathematics.definitions.graph.tree.k_ary_tree import K_ARY_TREE
from definit_db_py.data.field.mathematics.definitions.graph.tree.tree import TREE
from definit_db_py.definition.definition import Definition
from definit_db_py.definition.definition_key import DefinitionKey
from definit_db_py.definition.field import Field


class _BinaryTree(Definition):
    def _get_content(self) -> str:
        return (
            f"A {TREE.key.get_reference(phrase='tree')} in which each node has at most two children, referred to as the left child and the right child. "
            f"A binary tree is a special case of a {K_ARY_TREE.key.get_reference(phrase='k-ary tree')} where k = 2."
        )


BINARY_TREE = _BinaryTree(
    key=DefinitionKey(
        name="binary_tree",
        field=Field.MATHEMATICS,
    )
)
