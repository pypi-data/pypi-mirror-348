from definit_db_py.data.field.computer_science.definitions.data_structure.collection.string.string import STRING
from definit_db_py.definition.definition import Definition
from definit_db_py.definition.definition_key import DefinitionKey
from definit_db_py.definition.field import Field


class _Substring(Definition):
    def _get_content(self) -> str:
        return f"A contiguous sequence of characters within a {STRING.key.get_reference(phrase='string')}. For instance, 'the best of' is a substring of 'It was the best of times'."


SUBSTRING = _Substring(
    key=DefinitionKey(
        name="substring",
        field=Field.COMPUTER_SCIENCE,
    )
)
