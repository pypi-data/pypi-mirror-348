from definit_db_py.data.field.computer_science.definitions.foundamental.data import DATA
from definit_db_py.definition.definition import Definition
from definit_db_py.definition.definition_key import DefinitionKey
from definit_db_py.definition.field import Field


class _DataStructure(Definition):
    def _get_content(self) -> str:
        return (
            f"A data structure is a way of organizing and storing {DATA.key.get_reference(phrase='data')} so it can be accessed and modified efficiently. "
            "A data structure contains a value or group of values and the functions or operations that can be applied to the data."
        )


DATA_STRUCTURE = _DataStructure(
    key=DefinitionKey(
        name="data_structure",
        field=Field.COMPUTER_SCIENCE,
    )
)
