from definit_db_py.data.field.computer_science.definitions.data_structure.bit_field import BIT_FIELD
from definit_db_py.data.field.computer_science.definitions.data_structure.primitive_data_type import PRIMITIVE_DATA_TYPE
from definit_db_py.data.field.computer_science.definitions.foundamental.bit import BIT
from definit_db_py.data.field.mathematics.definitions.foundamental.information import INFORMATION
from definit_db_py.definition.definition import Definition
from definit_db_py.definition.definition_key import DefinitionKey
from definit_db_py.definition.field import Field


class _Boolean(Definition):
    def _get_content(self) -> str:
        return (
            f"Boolean (sometimes shortened to Bool) is a {PRIMITIVE_DATA_TYPE.key.get_reference(phrase='primitive data type')} that has one of two possible values usually denoted true and false. "
            f"Boolean is a {BIT_FIELD.key.get_reference(phrase='bit field')} that stores a single {BIT.key.get_reference(phrase='bit')} of {INFORMATION.key.get_reference(phrase='information')}."
        )


BOOLEAN = _Boolean(
    key=DefinitionKey(
        name="boolean",
        field=Field.COMPUTER_SCIENCE,
    )
)
