from definit_db_py.data.field.computer_science.definitions.data_structure.abstract_data_type import ABSTRACT_DATA_TYPE
from definit_db_py.data.field.computer_science.definitions.foundamental.data_structure import DATA_STRUCTURE
from definit_db_py.data.field.computer_science.definitions.foundamental.operation import OPERATION
from definit_db_py.definition.definition import Definition
from definit_db_py.definition.definition_key import DefinitionKey
from definit_db_py.definition.field import Field


class _Collection(Definition):
    def _get_content(self) -> str:
        return f"Collection is an {ABSTRACT_DATA_TYPE.key.get_reference(phrase='abstract data type')} that groups some variable number of {DATA_STRUCTURE.key.get_reference(phrase='data structures')} (possibly zero) that have some shared significance to the problem being solved and need to be {OPERATION.key.get_reference(phrase='operated')} upon together in some controlled fashion."


COLLECTION = _Collection(
    key=DefinitionKey(
        name="collection",
        field=Field.COMPUTER_SCIENCE,
    )
)
