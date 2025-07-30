from definit_db_py.data.field.computer_science.definitions.data_structure.collection import COLLECTION
from definit_db_py.data.field.computer_science.definitions.data_structure.collection.queue import QUEUE
from definit_db_py.data.field.computer_science.definitions.foundamental.data_structure import DATA_STRUCTURE
from definit_db_py.data.field.computer_science.definitions.foundamental.operation import OPERATION
from definit_db_py.data.field.mathematics.definitions.foundamental.set import SET
from definit_db_py.definition.definition import Definition
from definit_db_py.definition.definition_key import DefinitionKey
from definit_db_py.definition.field import Field


class _Stack(Definition):
    def _get_content(self) -> str:
        return (
            f"Stack is a {DATA_STRUCTURE.key.get_reference(phrase='data structure')} providing last-in-first-out semantics; also called a LIFO {QUEUE.key.get_reference(phrase='queue')}.\n\n"
            f"Serves as a {COLLECTION.key.get_reference(phrase='collection')} of elements with two main {OPERATION.key.get_reference(phrase='operations')}:\n\n"
            "- Push, which adds an element to the collection, and\n"
            "- Pop, which removes the most recently added element.\n\n"
            f"Additionally, a peek {OPERATION.key.get_reference(phrase='operation')} can, without modifying the stack, return the value of the last element added. The name stack is an analogy to a {SET.key.get_reference(phrase='set')} of physical items stacked one atop another, such as a stack of plates."
        )


STACK = _Stack(
    key=DefinitionKey(
        name="stack",
        field=Field.COMPUTER_SCIENCE,
    )
)
