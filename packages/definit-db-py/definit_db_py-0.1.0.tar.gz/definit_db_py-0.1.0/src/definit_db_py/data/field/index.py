from definit_db_py.data.field.computer_science import computer_science_index
from definit_db_py.data.field.mathematics import mathematics_index
from definit_db_py.definition.definition import Definition
from definit_db_py.definition.definition_key import DefinitionKey
from definit_db_py.definition.field import Field

_field_to_index: dict[Field, dict[DefinitionKey, Definition]] = {
    Field.COMPUTER_SCIENCE: {definition.key: definition for definition in computer_science_index},
    Field.MATHEMATICS: {definition.key: definition for definition in mathematics_index},
}


def get_index(field: Field) -> dict[DefinitionKey, Definition]:
    return _field_to_index[field]
