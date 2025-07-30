from definit_db_py.data.field.computer_science.definitions.foundamental.bit import BIT
from definit_db_py.data.field.computer_science.definitions.foundamental.data_structure import DATA_STRUCTURE
from definit_db_py.definition.definition import Definition
from definit_db_py.definition.definition_key import DefinitionKey
from definit_db_py.definition.field import Field


class _BitField(Definition):
    def _get_content(self) -> str:
        return f"A bit field is a {DATA_STRUCTURE.key.get_reference(phrase='data structure')} that consist of one or more adjacent {BIT.key.get_reference(phrase='bits')} which have been allocated for specific purposes, so that any single bit or group of bits within the structure can be set or inspected."


BIT_FIELD = _BitField(
    key=DefinitionKey(
        name="bit_field",
        field=Field.COMPUTER_SCIENCE,
    )
)
