from definit_db_py.data.field.mathematics.definitions.foundamental.hash_function import HASH_FUNCTION
from definit_db_py.data.field.mathematics.definitions.foundamental.sequence import SEQUENCE
from definit_db_py.definition.definition import Definition
from definit_db_py.definition.definition_key import DefinitionKey
from definit_db_py.definition.field import Field


class _RollingHash(Definition):
    def _get_content(self) -> str:
        return (
            "A rolling hash is an approach designed to enable efficient execution of the "
            f"{HASH_FUNCTION.key.get_reference(phrase='hash function')} when the input is modified incrementally, "
            f"such as when a window of fixed size moves over a {SEQUENCE.key.get_reference()}."
        )


ROLLING_HASH = _RollingHash(
    key=DefinitionKey(
        name="rolling_hash",
        field=Field.COMPUTER_SCIENCE,
    )
)
