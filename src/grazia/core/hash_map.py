from dataclasses import dataclass
from typing import Any, Optional

from grazia.core.exceptions import KeyNotFoundError


@dataclass
class _Node:
    """
    A private Linked List node used internally by the HashMap
    to handle index collisions via separate chaining.
    """

    key: str
    value: Any
    next: Optional["_Node"] = None


class HashMap:
    """
    A custom Hash Map implementation using an array of buckets and
    singly linked lists for collision resolution.
    """

    def __init__(self, capacity: int = 16) -> None:
        """
        Initializes the Hash Map with a fixed number of empty buckets.

        Args:
            capacity (int): The total number of buckets in the underlying array.
        """
        self.capacity: int = capacity
        self.buckets: list[Optional[_Node]] = [None] * self.capacity

    def _hash(self, key: str) -> int:
        """
        Generates a deterministic integer index for a given string key
        using the DJB2 hashing algorithm.

        Args:
            key (str): The string to hash.

        Returns:
            int: The calculated bucket index within the array's capacity bounds.
        """
        hash_code = 0
        for char in key:
            hash_code = (hash_code * 31 + ord(char)) % (10**9 + 7)
        return hash_code % self.capacity

    def put(self, key: str, value: Any) -> None:
        """
        Inserts or updates a key-value pair in the Hash Map.

        Args:
            key (str): The unique identifier.
            value (Any): The data to store.
        """
        index = self._hash(key)
        node = self.buckets[index]

        if node is None:
            self.buckets[index] = _Node(key, value)
            return

        prev = None

        while node is not None:
            if node.key == key:
                node.value = value
                return
            prev = node
            node = node.next

        prev.next = _Node(key, value)

    def get(self, key: str) -> Any:
        """
        Retrieves a value by its key.

        Args:
            key (str): The identifier to search for.

        Returns:
            Any: The stored value.

        Raises:
            KeyNotFoundError: If the key does not exist.
        """
        index = self._hash(key)
        node = self.buckets[index]

        while node is not None:
            if node.key == key:
                return node.value
            node = node.next

        raise KeyNotFoundError(key)

    def delete(self, key: str) -> None:
        """
        Removes a key-value pair from the Hash Map, safely unlinking
        the target node to maintain chain integrity.

        Args:
            key (str): The identifier to remove.

        Raises:
            KeyNotFoundError: If the key does not exist.
        """
        index = self._hash(key)

        current = self.buckets[index]
        prev = None

        if current is None:
            raise KeyNotFoundError(key)

        while current is not None:
            if current.key == key:
                if prev is None:
                    self.buckets[index] = current.next
                else:
                    prev.next = current.next
                return

            prev = current
            current = current.next

        raise KeyNotFoundError(key)
