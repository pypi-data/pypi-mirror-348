from definit_db_py.data.field.computer_science.definitions.data_structure.abstract_data_type import ABSTRACT_DATA_TYPE
from definit_db_py.data.field.computer_science.definitions.data_structure.collection import COLLECTION
from definit_db_py.data.field.computer_science.definitions.data_structure.map import MAP
from definit_db_py.data.field.computer_science.definitions.foundamental.operation import OPERATION
from definit_db_py.definition.definition import Definition
from definit_db_py.definition.definition_key import DefinitionKey
from definit_db_py.definition.field import Field


class _AssociativeArray(Definition):
    def _get_content(self) -> str:
        return f"An {ABSTRACT_DATA_TYPE.key.get_reference(phrase='abstract data type')} that {MAP.key.get_reference(phrase='maps')} keys to values. It is a {COLLECTION.key.get_reference(phrase='collection')} of key-value pairs, where each key is unique and is used to access the corresponding value. Associative arrays allow for efficient {OPERATION.key.get_reference(phrase='operations')}: retrieval, insertion, and deletion of values based on their keys."


ASSOCIATIVE_ARRAY = _AssociativeArray(
    key=DefinitionKey(
        name="associative_array",
        field=Field.COMPUTER_SCIENCE,
    )
)
