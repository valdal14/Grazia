from abc import ABC, abstractmethod
from typing import Any

from grazia.core.exceptions import GraziaError
from grazia.core.hash_map import HashMap


class GraziaStore(ABC):
    """The abstract interface defining the contract for all Grazia storage engines."""

    @abstractmethod
    def set(self, key: str, value: Any) -> None:
        """Stores a key-value pair in the database."""
        pass

    @abstractmethod
    def get(self, key: str) -> Any:
        """Retrieves a value from the database using its key."""
        pass

    @abstractmethod
    def delete(self, key: str) -> None:
        """Removes a key-value pair from the database."""
        pass


class Store(GraziaStore):
    """
    A concrete implementation of GraziaStore utilizing the custom
    HashMap as the underlying memory allocation mechanism.
    """

    def __init__(self) -> None:
        """Initializes the underlying custom HashMap engine."""
        self._data = HashMap()

    def set(self, key: str, value: Any) -> None:
        self._validate_key(key)
        self._data.put(key, value)

    def get(self, key: str) -> Any:
        self._validate_key(key)
        return self._data.get(key)

    def delete(self, key: str) -> None:
        self._validate_key(key)
        self._data.delete(key)

    # NOTE: - Internal Helper ######################################################
    def _validate_key(self, key: Any) -> bool:
        """
        Validates that the provided key is a non-empty string.

        Args:
            key (Any): The key to validate.

        Returns:
            bool: True if the key is valid.

        Raises:
            GraziaError: If the key is not a string or is an empty string.
        """
        if not isinstance(key, str) or len(key) == 0:
            raise GraziaError("Invalid key: The key must be a non-empty string.")
        return True
