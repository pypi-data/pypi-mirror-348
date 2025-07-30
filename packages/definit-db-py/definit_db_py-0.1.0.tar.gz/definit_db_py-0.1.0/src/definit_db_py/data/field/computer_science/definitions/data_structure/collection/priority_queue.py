from definit_db_py.data.field.computer_science.definitions.data_structure.abstract_data_type import ABSTRACT_DATA_TYPE
from definit_db_py.data.field.computer_science.definitions.data_structure.collection.queue import QUEUE
from definit_db_py.definition.definition import Definition
from definit_db_py.definition.definition_key import DefinitionKey
from definit_db_py.definition.field import Field


class _PriorityQueue(Definition):
    def _get_content(self) -> str:
        return f"A priority queue is an {ABSTRACT_DATA_TYPE.key.get_reference(phrase='abstract data type')} that operates similarly to a regular {QUEUE.key.get_reference(phrase='queue')} but with an added feature: each element in the priority queue has a 'priority' associated with it. Elements with higher priority are served before elements with lower priority. If two elements have the same priority, they are served according to their order in the queue (FIFO - First In, First Out)."


PRIORITY_QUEUE = _PriorityQueue(
    key=DefinitionKey(
        name="priority_queue",
        field=Field.COMPUTER_SCIENCE,
    )
)
