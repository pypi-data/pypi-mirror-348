from definit_db_py.data.field.computer_science.definitions.data_structure.collection.string.character_encoding import (
    CHARACTER_ENCODING,
)
from definit_db_py.definition.definition import Definition
from definit_db_py.definition.definition_key import DefinitionKey
from definit_db_py.definition.field import Field


class _Unicode(Definition):
    def _get_content(self) -> str:
        return f"A {CHARACTER_ENCODING.key.get_reference(phrase='character encoding')} standard that aims to provide a unique number for every character, regardless of the system."


UNICODE = _Unicode(
    key=DefinitionKey(
        name="unicode",
        field=Field.COMPUTER_SCIENCE,
    )
)
