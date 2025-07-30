from definit_db_py.data.field.mathematics.definitions.graph.node import NODE
from definit_db_py.data.field.mathematics.definitions.graph.tree.b_tree import B_TREE
from definit_db_py.definition.definition import Definition
from definit_db_py.definition.definition_key import DefinitionKey
from definit_db_py.definition.field import Field


class _BinarySearchTree(Definition):
    def _get_content(self) -> str:
        return f"A special case of a {B_TREE.key.get_reference(phrase='b_tree')} in that a {NODE.key.get_reference(phrase='node')} can only have maximum two children."


BINARY_SEARCH_TREE = _BinarySearchTree(
    key=DefinitionKey(
        name="binary_search_tree",
        field=Field.MATHEMATICS,
    )
)
