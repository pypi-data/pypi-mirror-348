from definit_db_py.data.field.computer_science.definitions.data_structure.collection.string.ascii import ASCII
from definit_db_py.data.field.computer_science.definitions.data_structure.collection.string.character_encoding import (
    CHARACTER_ENCODING,
)
from definit_db_py.definition.definition import Definition
from definit_db_py.definition.definition_key import DefinitionKey
from definit_db_py.definition.field import Field


class _ExtendedAscii(Definition):
    def _get_content(self) -> str:
        return f"An extension of the {ASCII.key.get_reference(phrase='ASCII')} {CHARACTER_ENCODING.key.get_reference(phrase='character encoding')} standard that uses 8 bits to represent 256 characters, including additional symbols and characters from various languages."


EXTENDED_ASCII = _ExtendedAscii(
    key=DefinitionKey(
        name="extended_ascii",
        field=Field.COMPUTER_SCIENCE,
    )
)
