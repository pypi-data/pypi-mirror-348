from abc import abstractmethod

from definit_db_py.definition.definition_key import DefinitionKey


class Definition:
    def __init__(self, key: DefinitionKey) -> None:
        self._key = key
        self._content = self._get_content()

    @property
    def key(self) -> DefinitionKey:
        return self._key

    @property
    def content(self) -> str:
        return self._content

    @abstractmethod
    def _get_content(self) -> str: ...
