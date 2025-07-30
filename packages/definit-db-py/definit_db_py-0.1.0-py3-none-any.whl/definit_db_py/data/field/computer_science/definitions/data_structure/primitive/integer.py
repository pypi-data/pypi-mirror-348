from definit_db_py.data.field.computer_science.definitions.data_structure.primitive_data_type import PRIMITIVE_DATA_TYPE
from definit_db_py.definition.definition import Definition
from definit_db_py.definition.definition_key import DefinitionKey
from definit_db_py.definition.field import Field


class _Integer(Definition):
    def _get_content(self) -> str:
        return f"A {PRIMITIVE_DATA_TYPE.key.get_reference(phrase='primitive data type')} that represents whole numbers. Integers can be positive, negative, or zero."


INTEGER = _Integer(
    key=DefinitionKey(
        name="integer",
        field=Field.COMPUTER_SCIENCE,
    )
)
