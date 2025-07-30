from definit_db_py.data.field.computer_science.definitions.data_structure.collection.string.character_encoding import (
    CHARACTER_ENCODING,
)
from definit_db_py.data.field.computer_science.definitions.data_structure.collection.string.unicode import UNICODE
from definit_db_py.data.field.computer_science.definitions.data_structure.collection.string.utf import UTF
from definit_db_py.definition.definition import Definition
from definit_db_py.definition.definition_key import DefinitionKey
from definit_db_py.definition.field import Field


class _Utf8(Definition):
    def _get_content(self) -> str:
        return f"A {UTF.key.get_reference(phrase='UTF')} {CHARACTER_ENCODING.key.get_reference(phrase='character encoding')} scheme that uses 1 to 4 bytes to represent {UNICODE.key.get_reference(phrase='Unicode')} characters. It is backward compatible with ASCII and can represent any character in the Unicode standard."


UTF_8 = _Utf8(
    key=DefinitionKey(
        name="utf_8",
        field=Field.COMPUTER_SCIENCE,
    )
)
