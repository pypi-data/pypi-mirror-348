from definit_db_py.data.field.computer_science.definitions.data_structure.collection.list.list import LIST
from definit_db_py.data.field.computer_science.definitions.foundamental.data_type import DATA_TYPE
from definit_db_py.definition.definition import Definition
from definit_db_py.definition.definition_key import DefinitionKey
from definit_db_py.definition.field import Field


class _Array(Definition):
    def _get_content(self) -> str:
        return f"Array is a {LIST.key.get_reference(phrase='list')} of elements of the same {DATA_TYPE.key.get_reference(phrase='type')}."


ARRAY = _Array(
    key=DefinitionKey(
        name="array",
        field=Field.COMPUTER_SCIENCE,
    )
)
