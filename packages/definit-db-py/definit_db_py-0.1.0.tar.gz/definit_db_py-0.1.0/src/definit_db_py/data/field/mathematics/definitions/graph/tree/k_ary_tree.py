from definit_db_py.data.field.mathematics.definitions.graph.node import NODE
from definit_db_py.data.field.mathematics.definitions.graph.tree.tree import TREE
from definit_db_py.definition.definition import Definition
from definit_db_py.definition.definition_key import DefinitionKey
from definit_db_py.definition.field import Field


class _KAryTree(Definition):
    def _get_content(self) -> str:
        return (
            f"A {TREE.key.get_reference(phrase='tree')} in which each {NODE.key.get_reference(phrase='node')} has at most k children. "
            "The maximum number of nodes at level h of a k-ary tree is k^h, and the maximum number of nodes in a k-ary tree of height h is (k^(h+1) - 1) / (k - 1)."
        )


K_ARY_TREE = _KAryTree(
    key=DefinitionKey(
        name="k_ary_tree",
        field=Field.MATHEMATICS,
    )
)
