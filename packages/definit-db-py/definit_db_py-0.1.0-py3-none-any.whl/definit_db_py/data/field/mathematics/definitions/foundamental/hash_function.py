from definit_db_py.data.field.mathematics.definitions.foundamental.object import OBJECT
from definit_db_py.definition.definition import Definition
from definit_db_py.definition.definition_key import DefinitionKey
from definit_db_py.definition.field import Field


class _HashFunction(Definition):
    def _get_content(self) -> str:
        return (
            f"A function that for an input {OBJECT.key.get_reference(phrase='object')} assigns a fixed-size text. "
            "The text is typically a 'digest' that is unique to each unique input."
        )


HASH_FUNCTION = _HashFunction(
    key=DefinitionKey(
        name="hash_function",
        field=Field.MATHEMATICS,
    )
)
