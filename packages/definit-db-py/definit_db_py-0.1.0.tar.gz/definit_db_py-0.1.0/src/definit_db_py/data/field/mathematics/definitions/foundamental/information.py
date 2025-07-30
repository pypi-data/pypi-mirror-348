from definit_db_py.definition.definition import Definition
from definit_db_py.definition.definition_key import DefinitionKey
from definit_db_py.definition.field import Field


class _Information(Definition):
    def _get_content(self) -> str:
        return (
            "An abstract concept that refers to something which has the power to inform. "
            "At the most fundamental level, it pertains to the interpretation (perhaps formally) of that which may be sensed, or their abstractions. "
            "Any natural process that is not completely random and any observable pattern in any medium can be said to convey some amount of information."
        )


INFORMATION = _Information(
    key=DefinitionKey(
        name="information",
        field=Field.MATHEMATICS,
    )
)
