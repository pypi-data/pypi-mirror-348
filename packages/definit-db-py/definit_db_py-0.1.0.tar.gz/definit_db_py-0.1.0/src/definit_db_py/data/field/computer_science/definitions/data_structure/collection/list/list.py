from definit_db_py.data.field.computer_science.definitions.data_structure.collection import COLLECTION
from definit_db_py.data.field.computer_science.definitions.foundamental.data_type import DATA_TYPE
from definit_db_py.definition.definition import Definition
from definit_db_py.definition.definition_key import DefinitionKey
from definit_db_py.definition.field import Field


class _List(Definition):
    def _get_content(self) -> str:
        return f"An ordered {COLLECTION.key.get_reference(phrase='collection')}. Also known as a sequence. One can add, remove, and pop any element from the list. List can store elements of different {DATA_TYPE.key.get_reference(phrase='types')}."


LIST = _List(
    key=DefinitionKey(
        name="list",
        field=Field.COMPUTER_SCIENCE,
    )
)
