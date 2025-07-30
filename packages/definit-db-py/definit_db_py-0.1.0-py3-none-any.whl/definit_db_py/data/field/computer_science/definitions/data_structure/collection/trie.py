from definit_db_py.data.field.computer_science.definitions.data_structure.collection.string.string import STRING
from definit_db_py.data.field.mathematics.definitions.foundamental.set import SET
from definit_db_py.data.field.mathematics.definitions.graph.node import NODE
from definit_db_py.data.field.mathematics.definitions.graph.tree.tree import TREE
from definit_db_py.definition.definition import Definition
from definit_db_py.definition.definition_key import DefinitionKey
from definit_db_py.definition.field import Field


class _Trie(Definition):
    def _get_content(self) -> str:
        return (
            f"A type of {TREE.key.get_reference(phrase='tree')} data structure that is used to store a dynamic {SET.key.get_reference(phrase='set')} of strings, where the keys are usually strings. "
            f"Each {NODE.key.get_reference(phrase='node')} in the trie represents a single character of a {STRING.key.get_reference(phrase='string')}, and the path from the root to a node represents a prefix of the string. The main advantage of using a trie is that it allows for efficient retrieval of strings with common prefixes."
        )


TRIE = _Trie(
    key=DefinitionKey(
        name="trie",
        field=Field.COMPUTER_SCIENCE,
    )
)
