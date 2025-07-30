from definit_db_py.data.field.computer_science.definitions.foundamental.data_structure import DATA_STRUCTURE
from definit_db_py.definition.definition import Definition
from definit_db_py.definition.definition_key import DefinitionKey
from definit_db_py.definition.field import Field


class _Map(Definition):
    def _get_content(self) -> str:
        return f"A {DATA_STRUCTURE.key.get_reference(phrase='data structure')} that maps keys to values. Each key can map to at most one value. It models the mathematical function abstraction."


MAP = _Map(
    key=DefinitionKey(
        name="map",
        field=Field.COMPUTER_SCIENCE,
    )
)
