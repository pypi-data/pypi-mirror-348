from definit_db_py.data.field.mathematics.definitions.graph.graph import GRAPH
from definit_db_py.data.field.mathematics.definitions.graph.node import NODE
from definit_db_py.data.field.mathematics.definitions.graph.path import PATH
from definit_db_py.definition.definition import Definition
from definit_db_py.definition.definition_key import DefinitionKey
from definit_db_py.definition.field import Field


class _Cycle(Definition):
    def _get_content(self) -> str:
        return (
            f"A cycle in a {GRAPH.key.get_reference(phrase='graph')} is a non-empty {PATH.key.get_reference(phrase='path')} "
            f"in which only the first and last {NODE.key.get_reference(phrase='nodes')} are equal."
        )


CYCLE = _Cycle(
    key=DefinitionKey(
        name="cycle",
        field=Field.MATHEMATICS,
    )
)
