from definit_db_py.data.field.mathematics.definitions.problem.criterion import CRITERION
from definit_db_py.data.field.mathematics.definitions.problem.solution import SOLUTION
from definit_db_py.definition.definition import Definition
from definit_db_py.definition.definition_key import DefinitionKey
from definit_db_py.definition.field import Field


class _OptimalSolution(Definition):
    def _get_content(self) -> str:
        return f"A {SOLUTION.key.get_reference(phrase='solution')} that is the best among all possible solutions, often in terms of a specific {CRITERION.key.get_reference(phrase='criterion')}."


OPTIMAL_SOLUTION = _OptimalSolution(
    key=DefinitionKey(
        name="optimal_solution",
        field=Field.MATHEMATICS,
    )
)
