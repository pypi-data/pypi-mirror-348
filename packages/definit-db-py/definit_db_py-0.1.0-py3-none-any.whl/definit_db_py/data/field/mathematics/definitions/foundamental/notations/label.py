from definit_db_py.data.field.mathematics.definitions.foundamental.object import OBJECT
from definit_db_py.definition.definition import Definition
from definit_db_py.definition.definition_key import DefinitionKey
from definit_db_py.definition.field import Field


class _Label(Definition):
    def _get_content(self) -> str:
        return f"A label is a name, number, or symbol attached to an {OBJECT.key.get_reference(phrase='object')} to give it meaning or identify it."


LABEL = _Label(
    key=DefinitionKey(
        name="label",
        field=Field.MATHEMATICS,
    )
)
