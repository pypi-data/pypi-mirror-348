from definit_db_py.data.field.computer_science.definitions.data_structure.collection.associative_array import (
    ASSOCIATIVE_ARRAY,
)
from definit_db_py.data.field.mathematics.definitions.foundamental.hash_function import HASH_FUNCTION
from definit_db_py.definition.definition import Definition
from definit_db_py.definition.definition_key import DefinitionKey
from definit_db_py.definition.field import Field


class _HashTable(Definition):
    def _get_content(self) -> str:
        return f"Data structure that implements {ASSOCIATIVE_ARRAY.key.get_reference(phrase='associative array')} using a {HASH_FUNCTION.key.get_reference(phrase='hash function')} to compute an index into an array of buckets or slots, from which the desired value can be found. Hash tables are designed to provide fast access to data by using a hash function to map keys to indices in an array."


HASH_TABLE = _HashTable(
    key=DefinitionKey(
        name="hash_table",
        field=Field.COMPUTER_SCIENCE,
    )
)
