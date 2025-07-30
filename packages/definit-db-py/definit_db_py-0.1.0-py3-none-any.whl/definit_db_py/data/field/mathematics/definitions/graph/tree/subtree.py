from definit_db_py.data.field.mathematics.definitions.graph.node import NODE
from definit_db_py.data.field.mathematics.definitions.graph.tree.tree import TREE
from definit_db_py.definition.definition import Definition
from definit_db_py.definition.definition_key import DefinitionKey
from definit_db_py.definition.field import Field


class _Subtree(Definition):
    def _get_content(self) -> str:
        return f"A {TREE.key.get_reference(phrase='tree')} formed from a {NODE.key.get_reference(phrase='node')} and all its descendants in a tree."


SUBTREE = _Subtree(
    key=DefinitionKey(
        name="subtree",
        field=Field.MATHEMATICS,
    )
)
