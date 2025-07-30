from definit_db_py.data.field.computer_science.definitions.foundamental.data_structure import DATA_STRUCTURE
from definit_db_py.definition.definition import Definition
from definit_db_py.definition.definition_key import DefinitionKey
from definit_db_py.definition.field import Field


class _Object(Definition):
    def _get_content(self) -> str:
        return f"An object is an instance of a {DATA_STRUCTURE.key.get_reference(phrase='data structure')}."


OBJECT = _Object(
    key=DefinitionKey(
        name="object",
        field=Field.COMPUTER_SCIENCE,
    )
)
