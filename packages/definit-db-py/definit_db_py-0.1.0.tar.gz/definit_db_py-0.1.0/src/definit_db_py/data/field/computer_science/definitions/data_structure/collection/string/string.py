from definit_db_py.data.field.computer_science.definitions.data_structure.collection.string.character_encoding import (
    CHARACTER_ENCODING,
)
from definit_db_py.definition.definition import Definition
from definit_db_py.definition.definition_key import DefinitionKey
from definit_db_py.definition.field import Field


class _String(Definition):
    def _get_content(self) -> str:
        return f"A sequence of {CHARACTER_ENCODING.key.get_reference(phrase='decoded characters')}, typically used to represent text. Strings can be of variable length and can contain letters, numbers, symbols, and whitespace."


STRING = _String(
    key=DefinitionKey(
        name="string",
        field=Field.COMPUTER_SCIENCE,
    )
)
