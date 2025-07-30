from definit_db_py.data.field.mathematics.definitions.foundamental.information import INFORMATION
from definit_db_py.definition.definition import Definition
from definit_db_py.definition.definition_key import DefinitionKey
from definit_db_py.definition.field import Field


class _Data(Definition):
    def _get_content(self) -> str:
        return f"A collection of discrete or continuous values that convey {INFORMATION.key.get_reference(phrase='information')}, describing the quantity, quality, fact, statistics, other basic units of meaning, or simply sequences of symbols that may be further interpreted formally."


DATA = _Data(
    key=DefinitionKey(
        name="data",
        field=Field.COMPUTER_SCIENCE,
    )
)
