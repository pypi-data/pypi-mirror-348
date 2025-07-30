from definit_db_py.data.field.mathematics.definitions.foundamental.finite_sequence import FINITE_SEQUENCE
from definit_db_py.data.field.mathematics.definitions.foundamental.instruction import INSTRUCTION
from definit_db_py.data.field.mathematics.definitions.problem.problem import PROBLEM
from definit_db_py.definition.definition import Definition
from definit_db_py.definition.definition_key import DefinitionKey
from definit_db_py.definition.field import Field


class _Algorithm(Definition):
    def _get_content(self) -> str:
        return (
            f"A {FINITE_SEQUENCE.key.get_reference(phrase='finite sequence')} of mathematically rigorous "
            f"{INSTRUCTION.key.get_reference(phrase='instructions')}, typically used to solve a "
            f"{PROBLEM.key.get_reference(phrase='problem')}."
        )


ALGORITHM = _Algorithm(
    key=DefinitionKey(
        name="algorithm",
        field=Field.MATHEMATICS,
    )
)
