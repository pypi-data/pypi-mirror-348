from definit_db_py.data.field.mathematics.definitions.foundamental.relation import RELATION
from definit_db_py.data.field.mathematics.definitions.graph.node import NODE
from definit_db_py.definition.definition import Definition
from definit_db_py.definition.definition_key import DefinitionKey
from definit_db_py.definition.field import Field


class _Edge(Definition):
    def _get_content(self) -> str:
        return (
            f"An edge is a directed or undirected connection between two {NODE.key.get_reference(phrase='nodes')}. "
            f"It defines a {RELATION.key.get_reference(phrase='relationship')} or link between them."
        )


EDGE = _Edge(
    key=DefinitionKey(
        name="edge",
        field=Field.MATHEMATICS,
    )
)
