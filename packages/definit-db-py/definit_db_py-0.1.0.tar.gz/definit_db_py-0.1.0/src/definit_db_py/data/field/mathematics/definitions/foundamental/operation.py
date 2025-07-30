from definit_db_py.data.field.mathematics.definitions.foundamental.object import OBJECT
from definit_db_py.definition.definition import Definition
from definit_db_py.definition.definition_key import DefinitionKey
from definit_db_py.definition.field import Field


class _Operation(Definition):
    def _get_content(self) -> str:
        return (
            "A mathematical action performed on one or more "
            f"{OBJECT.key.get_reference(phrase='objects')} to produce a result."
        )


OPERATION = _Operation(
    key=DefinitionKey(
        name="operation",
        field=Field.MATHEMATICS,
    )
)
