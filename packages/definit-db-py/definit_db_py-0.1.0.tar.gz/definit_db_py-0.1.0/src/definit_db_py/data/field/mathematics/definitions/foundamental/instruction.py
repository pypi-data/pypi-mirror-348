from definit_db_py.data.field.mathematics.definitions.foundamental.information import INFORMATION
from definit_db_py.definition.definition import Definition
from definit_db_py.definition.definition_key import DefinitionKey
from definit_db_py.definition.field import Field


class _Instruction(Definition):
    def _get_content(self) -> str:
        return f"A detailed {INFORMATION.key.get_reference(phrase='information')} about how something should be done or operated"


INSTRUCTION = _Instruction(
    key=DefinitionKey(
        name="instruction",
        field=Field.MATHEMATICS,
    )
)
