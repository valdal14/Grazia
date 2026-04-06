from abc import ABC, abstractmethod

from grazia.core.exceptions import GraziaError, KeyNotFoundError


class GraziaStore(ABC):
    """
    The abstract interface that all Grazia's Stores must implement.
    """

    @abstractmethod
    def set(self, key: str, value: str) -> None:
        pass

    @abstractmethod
    def get(self, key: str) -> str:
        pass

    @abstractmethod
    def delete(self, key: str) -> None:
        pass


class Store(GraziaStore):
    """
    A concrete implementation of GraziaStore that uses Python's built-in dictionary as our underlying storage mechanism
    """

    def __init__(self):
        self._data = {}

    def set(self, key: str, value: str) -> None:
        if len(key) == 0:
            raise GraziaError("Invalid key: The key cannot be an empty string.")

        if len(value) == 0:
            raise GraziaError("Invalid value: The value cannot be an empty string.")

        self._data[key] = value

    def get(self, key: str) -> str:
        if key not in self._data:
            raise KeyNotFoundError(key)

        return self._data[key]

    def delete(self, key: str) -> None:
        if key not in self._data:
            raise KeyNotFoundError(key)

        self._data.pop(key)
