from abc import ABC, abstractmethod

from grazia.core.exceptions import GraziaError, KeyNotFoundError


class GraziaStore(ABC):
    """
    The abstract interface defining the contract for all Grazia storage engines.
    """

    @abstractmethod
    def set(self, key: str, value: str) -> None:
        """
        Stores a key-value pair in the database.

        Args:
            key (str): The unique identifier for the value.
            value (str): The data to be stored.

        Raises:
            GraziaError: If the provided key or value is an empty string.
        """
        pass

    @abstractmethod
    def get(self, key: str) -> str:
        """
        Retrieves a value from the database using its key.

        Args:
            key (str): The identifier of the value to retrieve.

        Returns:
            str: The stored value associated with the key.

        Raises:
            KeyNotFoundError: If the key does not exist in the store.
        """
        pass

    @abstractmethod
    def delete(self, key: str) -> None:
        """
        Removes a key-value pair from the database.

        Args:
            key (str): The identifier of the key-value pair to remove.

        Raises:
            KeyNotFoundError: If the key does not exist in the store.
        """
        pass


class Store(GraziaStore):
    """
    A concrete implementation of GraziaStore utilizing a native Python
    dictionary as the underlying memory allocation mechanism.
    """

    def __init__(self) -> None:
        """Initializes an empty storage dictionary."""
        self._data: dict[str, str] = {}

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

        del self._data[key]
