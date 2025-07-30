from definit_db_py.data.field.mathematics.definitions.foundamental.set import SET
from definit_db_py.definition.definition import Definition
from definit_db_py.definition.definition_key import DefinitionKey
from definit_db_py.definition.field import Field


class _Multiset(Definition):
    def _get_content(self) -> str:
        return (
            f"A multiset is a {SET.key.get_reference(phrase='set')} that allows for multiple occurrences of the same element. "
            "Unlike a traditional set, which only allows unique elements, a multi-set can contain duplicates. This means that the same element can appear more than once."
        )


MULTISET = _Multiset(
    key=DefinitionKey(
        name="multiset",
        field=Field.MATHEMATICS,
    )
)
