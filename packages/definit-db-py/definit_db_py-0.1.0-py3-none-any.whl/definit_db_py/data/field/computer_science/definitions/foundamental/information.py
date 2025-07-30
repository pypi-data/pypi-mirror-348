from definit_db_py.definition.definition import Definition
from definit_db_py.definition.definition_key import DefinitionKey
from definit_db_py.definition.field import Field


class _Information(Definition):
    def _get_content(self) -> str:
        return "Information is data that has been processed, organized, or structured in a way that is meaningful or useful."


INFORMATION = _Information(
    key=DefinitionKey(
        name="information",
        field=Field.COMPUTER_SCIENCE,
    )
)
