from definit_db_py.data.field.mathematics.definitions.foundamental.finite_set import FINITE_SET
from definit_db_py.data.field.mathematics.definitions.graph.edge import EDGE
from definit_db_py.data.field.mathematics.definitions.graph.graph import GRAPH
from definit_db_py.data.field.mathematics.definitions.graph.node import NODE
from definit_db_py.definition.definition import Definition
from definit_db_py.definition.definition_key import DefinitionKey
from definit_db_py.definition.field import Field


class _Path(Definition):
    def _get_content(self) -> str:
        return (
            f"A path in a {GRAPH.key.get_reference(phrase='graph')} is a {FINITE_SET.key.get_reference(phrase='finite')} or infinite sequence of "
            f"{EDGE.key.get_reference(phrase='edges')} which joins a sequence of {NODE.key.get_reference(phrase='nodes')} which, by most definitions, are all distinct (and since the nodes are distinct, so are the edges)."
        )


PATH = _Path(
    key=DefinitionKey(
        name="path",
        field=Field.MATHEMATICS,
    )
)
