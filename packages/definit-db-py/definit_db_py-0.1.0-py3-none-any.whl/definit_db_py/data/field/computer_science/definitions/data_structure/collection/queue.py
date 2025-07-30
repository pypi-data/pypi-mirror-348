from definit_db_py.data.field.computer_science.definitions.data_structure.collection import COLLECTION
from definit_db_py.data.field.computer_science.definitions.foundamental.data_structure import DATA_STRUCTURE
from definit_db_py.data.field.computer_science.definitions.foundamental.operation import OPERATION
from definit_db_py.definition.definition import Definition
from definit_db_py.definition.definition_key import DefinitionKey
from definit_db_py.definition.field import Field


class _Queue(Definition):
    def _get_content(self) -> str:
        return (
            f"Queue is a {DATA_STRUCTURE.key.get_reference(phrase='data structure')} providing first-in-first-out (FIFO) semantics.\n\n"
            f"Serves as a {COLLECTION.key.get_reference(phrase='collection')} of elements with two main {OPERATION.key.get_reference(phrase='operations')}:\n\n"
            "- Enqueue, which adds an element to the rear of the queue, and\n"
            "- Dequeue, which removes an element from the front.\n\n"
            f"Additionally, a peek {OPERATION.key.get_reference(phrase='operation')} can, without modifying the queue, return the value of the next element to be dequeued without dequeuing it."
        )


QUEUE = _Queue(
    key=DefinitionKey(
        name="queue",
        field=Field.COMPUTER_SCIENCE,
    )
)
