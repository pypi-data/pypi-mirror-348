from definit_db_py.data.field.computer_science.definitions.data_structure.collection.string.character_encoding import (
    CHARACTER_ENCODING,
)
from definit_db_py.data.field.computer_science.definitions.foundamental.bit import BIT
from definit_db_py.definition.definition import Definition
from definit_db_py.definition.definition_key import DefinitionKey
from definit_db_py.definition.field import Field


class _Ascii(Definition):
    def _get_content(self) -> str:
        return f"ASCII is a {CHARACTER_ENCODING.key.get_reference(phrase='character encoding')} standard that uses 7 {BIT.key.get_reference(phrase='bits')} to represent 128 characters, including letters, digits, punctuation marks, and control characters."


ASCII = _Ascii(
    key=DefinitionKey(
        name="ascii",
        field=Field.COMPUTER_SCIENCE,
    )
)
