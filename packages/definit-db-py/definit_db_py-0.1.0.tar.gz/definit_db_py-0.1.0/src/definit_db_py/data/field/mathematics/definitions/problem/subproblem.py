from definit_db_py.data.field.mathematics.definitions.problem.problem import PROBLEM
from definit_db_py.definition.definition import Definition
from definit_db_py.definition.definition_key import DefinitionKey
from definit_db_py.definition.field import Field


class _Subproblem(Definition):
    def _get_content(self) -> str:
        return f"A smaller, more manageable {PROBLEM.key.get_reference(phrase='problem')} derived from a larger problem, often used in the context of problem-solving and algorithm design."


SUBPROBLEM = _Subproblem(
    key=DefinitionKey(
        name="subproblem",
        field=Field.MATHEMATICS,
    )
)
