from definit_db_py.data.field.mathematics.definitions.graph.node import NODE
from definit_db_py.data.field.mathematics.definitions.graph.tree.tree import TREE
from definit_db_py.definition.definition import Definition
from definit_db_py.definition.definition_key import DefinitionKey
from definit_db_py.definition.field import Field


class _HeapTree(Definition):
    def _get_content(self) -> str:
        return f"A type of {TREE.key.get_reference(phrase='tree')} data structure that satisfies the heap property: the value of each {NODE.key.get_reference(phrase='node')} is greater than or equal to (or less than or equal to) the values of its children. This property allows for efficient retrieval of the minimum (or maximum) element in the tree."


HEAP_TREE = _HeapTree(
    key=DefinitionKey(
        name="heap_tree",
        field=Field.COMPUTER_SCIENCE,
    )
)
