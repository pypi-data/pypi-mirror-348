from definit_db_py.data.field.computer_science.definitions.data_structure.collection.string.character_encoding import (
    CHARACTER_ENCODING,
)
from definit_db_py.data.field.computer_science.definitions.data_structure.collection.string.unicode import UNICODE
from definit_db_py.definition.definition import Definition
from definit_db_py.definition.definition_key import DefinitionKey
from definit_db_py.definition.field import Field


class _Utf(Definition):
    def _get_content(self) -> str:
        return f"UTF (Unicode Transformation Format) is a {CHARACTER_ENCODING.key.get_reference(phrase='character encoding')} standard that represents {UNICODE.key.get_reference(phrase='Unicode')} characters using variable-length sequences of bytes."


UTF = _Utf(
    key=DefinitionKey(
        name="utf",
        field=Field.COMPUTER_SCIENCE,
    )
)
