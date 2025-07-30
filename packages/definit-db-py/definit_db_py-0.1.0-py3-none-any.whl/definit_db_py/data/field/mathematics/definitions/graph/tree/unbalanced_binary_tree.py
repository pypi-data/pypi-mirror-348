from definit_db_py.data.field.mathematics.definitions.graph.node import NODE
from definit_db_py.data.field.mathematics.definitions.graph.tree.balanced_binary_tree import BALANCED_BINARY_TREE
from definit_db_py.data.field.mathematics.definitions.graph.tree.binary_tree import BINARY_TREE
from definit_db_py.data.field.mathematics.definitions.graph.tree.subtree import SUBTREE
from definit_db_py.definition.definition import Definition
from definit_db_py.definition.definition_key import DefinitionKey
from definit_db_py.definition.field import Field


class _UnbalancedBinaryTree(Definition):
    def _get_content(self) -> str:
        return (
            f"A {BINARY_TREE.key.get_reference(phrase='binary tree')} that does not satisfy the {BALANCED_BINARY_TREE.key.get_reference(phrase='balanced binary tree')} property. "
            f"In an unbalanced binary tree, the depth of the two {SUBTREE.key.get_reference(phrase='subtrees')} of at least one {NODE.key.get_reference(phrase='node')} differs by more than one."
        )


UNBALANCED_BINARY_TREE = _UnbalancedBinaryTree(
    key=DefinitionKey(
        name="unbalanced_binary_tree",
        field=Field.MATHEMATICS,
    )
)
