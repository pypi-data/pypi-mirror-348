from definit_db_py.data.field.mathematics.definitions.foundamental.set import SET
from definit_db_py.definition.definition import Definition
from definit_db_py.definition.definition_key import DefinitionKey
from definit_db_py.definition.field import Field


class _Relation(Definition):
    def _get_content(self) -> str:
        return f"A relation (also called relationship) describes a connection or association between elements of a {SET.key.get_reference(phrase='set(s)')}."


RELATION = _Relation(
    key=DefinitionKey(
        name="relation",
        field=Field.MATHEMATICS,
    )
)
