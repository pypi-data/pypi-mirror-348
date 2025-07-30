from definit_db_py.data.field.computer_science.definitions.data_structure.collection.hash_table import HASH_TABLE
from definit_db_py.data.field.computer_science.definitions.foundamental.data import DATA
from definit_db_py.data.field.mathematics.definitions.foundamental.hash_function import HASH_FUNCTION
from definit_db_py.definition.definition import Definition
from definit_db_py.definition.definition_key import DefinitionKey
from definit_db_py.definition.field import Field


class _HashCollision(Definition):
    def _get_content(self) -> str:
        return (
            "A situation in which two different inputs produce the same hash value when processed by a "
            f"{HASH_FUNCTION.key.get_reference(phrase='hash function')}. This can lead to "
            f"{DATA.key.get_reference()} integrity issues and is a key consideration "
            f"in the design of hash functions and {HASH_TABLE.key.get_reference(phrase='hash tables')}."
        )


HASH_COLLISION = _HashCollision(
    key=DefinitionKey(
        name="hash_collision",
        field=Field.COMPUTER_SCIENCE,
    )
)
