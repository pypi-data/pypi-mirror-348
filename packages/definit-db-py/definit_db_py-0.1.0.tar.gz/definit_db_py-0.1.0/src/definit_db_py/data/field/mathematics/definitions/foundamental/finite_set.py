from definit_db_py.data.field.mathematics.definitions.foundamental.set import SET
from definit_db_py.definition.definition import Definition
from definit_db_py.definition.definition_key import DefinitionKey
from definit_db_py.definition.field import Field


class _FiniteSet(Definition):
    def _get_content(self) -> str:
        return (
            f"Finite set is a {SET.key.get_reference(phrase='set')} that has a finite number of elements. "
            "Informally, a finite set is a set which one could in principle count and finish counting. "
            "For example, {2,4,6,8,10} is a finite set with five elements."
        )


FINITE_SET = _FiniteSet(
    key=DefinitionKey(
        name="finite_set",
        field=Field.MATHEMATICS,
    )
)
