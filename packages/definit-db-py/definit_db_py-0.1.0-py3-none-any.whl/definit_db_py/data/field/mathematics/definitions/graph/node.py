from definit_db_py.data.field.mathematics.definitions.foundamental.object import OBJECT
from definit_db_py.definition.definition import Definition
from definit_db_py.definition.definition_key import DefinitionKey
from definit_db_py.definition.field import Field


class _Node(Definition):
    def _get_content(self) -> str:
        return f"A node (also called vertex) is an abstract entity that can represent an {OBJECT.key.get_reference(phrase='object')} or position in a structure. It does not imply any connections or context on its own."


NODE = _Node(
    key=DefinitionKey(
        name="node",
        field=Field.MATHEMATICS,
    )
)
