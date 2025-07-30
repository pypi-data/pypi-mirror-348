from definit_db_py.data.field.mathematics.definitions.foundamental.object import OBJECT
from definit_db_py.definition.definition import Definition
from definit_db_py.definition.definition_key import DefinitionKey
from definit_db_py.definition.field import Field


class _Sequence(Definition):
    def _get_content(self) -> str:
        return f"A collection of {OBJECT.key.get_reference(phrase='objects')} in which repetitions are allowed and order matters."


SEQUENCE = _Sequence(
    key=DefinitionKey(
        name="sequence",
        field=Field.MATHEMATICS,
    )
)
