from definit_db_py.data.field.computer_science.definitions.foundamental.data_structure import DATA_STRUCTURE
from definit_db_py.data.field.mathematics.definitions.foundamental.set import SET
from definit_db_py.definition.definition import Definition
from definit_db_py.definition.definition_key import DefinitionKey
from definit_db_py.definition.field import Field


class _PrimitiveDataType(Definition):
    def _get_content(self) -> str:
        return f"Primitive data types are a {SET.key.get_reference(phrase='set')} of basic {DATA_STRUCTURE.key.get_reference(phrase='data structures')} from which all other data types are constructed."


PRIMITIVE_DATA_TYPE = _PrimitiveDataType(
    key=DefinitionKey(
        name="primitive_data_type",
        field=Field.COMPUTER_SCIENCE,
    )
)
