from abc import ABC, abstractmethod

from grazia.core.exceptions import GraziaError


class GraziaStore(ABC):
    """
    The abstract interface that all Grazia's Stores must implement.
    """

    @abstractmethod
    def set(self, key: str, value: str) -> None:
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
