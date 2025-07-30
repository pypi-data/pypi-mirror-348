from definit_db_py.data.field.computer_science.definitions.foundamental.data import DATA
from definit_db_py.data.field.computer_science.definitions.foundamental.data_type import DATA_TYPE
from definit_db_py.data.field.computer_science.definitions.foundamental.operation import OPERATION
from definit_db_py.definition.definition import Definition
from definit_db_py.definition.definition_key import DefinitionKey
from definit_db_py.definition.field import Field


class _AbstractDataType(Definition):
    def _get_content(self) -> str:
        return f"Abstract data type (ADT) is a mathematical model for {DATA_TYPE.key.get_reference(phrase='data type')}, defined by its behavior from the point of view of a user of the {DATA.key.get_reference(phrase='data')}, specifically in terms of possible values, possible {OPERATION.key.get_reference(phrase='operations')} on data of this {DATA_TYPE.key.get_reference(phrase='data type')}, and the behavior of these {OPERATION.key.get_reference(phrase='operations')}."


ABSTRACT_DATA_TYPE = _AbstractDataType(
    key=DefinitionKey(
        name="abstract_data_type",
        field=Field.COMPUTER_SCIENCE,
    )
)
