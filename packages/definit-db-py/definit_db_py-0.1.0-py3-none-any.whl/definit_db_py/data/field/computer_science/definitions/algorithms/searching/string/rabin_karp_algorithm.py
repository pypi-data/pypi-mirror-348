from definit_db_py.data.field.computer_science.definitions.algorithms.problems.rolling_hash import ROLLING_HASH
from definit_db_py.data.field.computer_science.definitions.data_structure.collection.string.string import STRING
from definit_db_py.data.field.computer_science.definitions.data_structure.collection.string.substring import SUBSTRING
from definit_db_py.data.field.mathematics.definitions.algorithm.algorithm import ALGORITHM
from definit_db_py.data.field.mathematics.definitions.foundamental.hash_function import HASH_FUNCTION
from definit_db_py.definition.definition import Definition
from definit_db_py.definition.definition_key import DefinitionKey
from definit_db_py.definition.field import Field


class _RabinKarpAlgorithm(Definition):
    def _get_content(self) -> str:
        return (
            f"A string searching {ALGORITHM.key.get_reference()} "
            f"that uses a {ROLLING_HASH.key.get_reference(phrase='rolling hash')} "
            f"to find a pattern in a {STRING.key.get_reference()}. "
            f"It computes the {HASH_FUNCTION.key.get_reference(phrase='hash')} of the pattern "
            f"and the hash of each {SUBSTRING.key.get_reference()} "
            f"of the text of the same length as the pattern, and compares them to find matches."
        )


RABIN_KARP_ALGORITHM = _RabinKarpAlgorithm(
    key=DefinitionKey(
        name="rabin_karp_algorithm",
        field=Field.COMPUTER_SCIENCE,
    )
)
