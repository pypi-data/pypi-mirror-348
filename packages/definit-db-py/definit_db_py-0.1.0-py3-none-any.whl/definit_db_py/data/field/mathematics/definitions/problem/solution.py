from definit_db_py.data.field.mathematics.definitions.foundamental.operation import OPERATION
from definit_db_py.data.field.mathematics.definitions.foundamental.sequence import SEQUENCE
from definit_db_py.data.field.mathematics.definitions.problem.problem import PROBLEM
from definit_db_py.definition.definition import Definition
from definit_db_py.definition.definition_key import DefinitionKey
from definit_db_py.definition.field import Field


class _Solution(Definition):
    def _get_content(self) -> str:
        return (
            f"A method or process for solving a {PROBLEM.key.get_reference(phrase='problem')}, often involving a "
            f"{SEQUENCE.key.get_reference(phrase='sequence')} of steps or {OPERATION.key.get_reference(phrase='operations')}."
        )


SOLUTION = _Solution(
    key=DefinitionKey(
        name="solution",
        field=Field.MATHEMATICS,
    )
)
