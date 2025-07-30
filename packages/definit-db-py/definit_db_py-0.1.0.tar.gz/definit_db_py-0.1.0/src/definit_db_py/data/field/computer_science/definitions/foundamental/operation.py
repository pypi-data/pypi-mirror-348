from definit_db_py.data.field.computer_science.definitions.foundamental.object import OBJECT
from definit_db_py.definition.definition import Definition
from definit_db_py.definition.definition_key import DefinitionKey
from definit_db_py.definition.field import Field


class _Operation(Definition):
    def _get_content(self) -> str:
        return f"Operation is an action that is carried out to accomplish a given task. In the most simple scenario, it is an action performed on at least one {OBJECT.key.get_reference(phrase='object')}."


OPERATION = _Operation(
    key=DefinitionKey(
        name="operation",
        field=Field.COMPUTER_SCIENCE,
    )
)
