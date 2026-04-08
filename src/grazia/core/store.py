from abc import ABC, abstractmethod
from typing import Any

from grazia.core.exceptions import GraziaError, KeyNotFoundError
from grazia.core.hash_map import HashMap
from grazia.core.lru import DLLNode, DoublyLinkedList


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

    def __init__(self, capacity: int = 1000) -> None:
        """Initializes the underlying custom HashMap engine."""
        self.capacity = capacity
        self._data = HashMap()
        self._lru = DoublyLinkedList()
        # Track current items without counting the entire HashMap
        self._size = 0

    def set(self, key: str, value: Any) -> None:
        """
        Stores a key-value pair in the database.

        If the cache is at maximum capacity, the Least Recently Used (LRU)
        item is evicted before insertion. If the key already exists, its
        value is updated and it is promoted to the Most Recently Used position.

        Args:
            key (str): The unique identifier for the value.
            value (Any): The data to be stored.

        Raises:
            GraziaError: If the provided key is an empty string or not a string.
        """
        self._validate_key(key)

        try:
            # Fetch the actual DLLNode directly from the internal engine
            node = self._data.get(key)

            # Update the payload and promote to MRU
            node.value = value
            self._lru.move_to_head(node)
            return

        except KeyNotFoundError:
            # Key does not exist. Check capacity for eviction.
            if self._size >= self.capacity:
                evicted_node = self._lru.pop_tail()

                # Safety check to ensure the dummy tail's key is not deleted
                if evicted_node and evicted_node.key is not None:
                    self._data.delete(evicted_node.key)
                    self._size -= 1

            # Create the new node and insert it into both engines
            new_node = DLLNode(key, value)
            self._lru.add_node(new_node)

            # The HashMap stores the key pointing directly to the DLLNode
            self._data.put(key, new_node)
            self._size += 1

    def get(self, key: str) -> Any:
        """
        Retrieves a value from the database using its key.

        Successfully accessing a key will promote it to the Most Recently Used
        (MRU) position within the underlying LRU cache.

        Args:
            key (str): The identifier of the value to retrieve.

        Returns:
            Any: The stored value associated with the key.

        Raises:
            GraziaError: If the provided key is an empty string or not a string.
            KeyNotFoundError: If the key does not exist in the store.
        """
        self._validate_key(key)
        node = self._data.get(key)
        self._lru.move_to_head(node)
        return node.value

    def delete(self, key: str) -> None:
        """
        Removes a key-value pair from the database.

        This method ensures that the data is safely unlinked from both the
        internal HashMap and the LRU Doubly Linked List, maintaining strict
        memory constraints and size tracking.

        Args:
            key (str): The identifier of the key-value pair to remove.

        Raises:
            GraziaError: If the provided key is an empty string or not a string.
            KeyNotFoundError: If the key does not exist in the store.
        """
        self._validate_key(key)
        # Retrieve the node (will raise KeyNotFoundError if missing)
        node = self._data.get(key)
        # Remove from the underlying engine
        self._data.delete(key)
        # Remove from the LRU chain
        self._lru.remove_node(node)
        self._size -= 1

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
