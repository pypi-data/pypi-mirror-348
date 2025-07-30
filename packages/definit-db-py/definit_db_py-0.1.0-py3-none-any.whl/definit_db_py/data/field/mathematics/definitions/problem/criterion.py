from definit_db_py.definition.definition import Definition
from definit_db_py.definition.definition_key import DefinitionKey
from definit_db_py.definition.field import Field


class _Criterion(Definition):
    def _get_content(self) -> str:
        return "A standard or principle by which something is judged or decided."


CRITERION = _Criterion(
    key=DefinitionKey(
        name="criterion",
        field=Field.MATHEMATICS,
    )
)
