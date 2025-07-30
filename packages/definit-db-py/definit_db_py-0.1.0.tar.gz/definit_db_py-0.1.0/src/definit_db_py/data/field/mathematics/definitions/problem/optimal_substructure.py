from definit_db_py.data.field.mathematics.definitions.problem.optimal_solution import OPTIMAL_SOLUTION
from definit_db_py.data.field.mathematics.definitions.problem.problem import PROBLEM
from definit_db_py.data.field.mathematics.definitions.problem.subproblem import SUBPROBLEM
from definit_db_py.definition.definition import Definition
from definit_db_py.definition.definition_key import DefinitionKey
from definit_db_py.definition.field import Field


class _OptimalSubstructure(Definition):
    def _get_content(self) -> str:
        return (
            f"A {PROBLEM.key.get_reference(phrase='problem')} is said to have optimal substructure if an "
            f"{OPTIMAL_SOLUTION.key.get_reference(phrase='optimal solution')} can be constructed from optimal solutions of its "
            f"{SUBPROBLEM.key.get_reference(phrase='subproblems')}."
        )


OPTIMAL_SUBSTRUCTURE = _OptimalSubstructure(
    key=DefinitionKey(
        name="optimal_substructure",
        field=Field.MATHEMATICS,
    )
)
