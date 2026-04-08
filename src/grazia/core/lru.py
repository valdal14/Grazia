from typing import Any, Optional


class DLLNode:
    """
    A Node for a Doubly Linked List that stores a key, a value, and
    bidirectional pointers to its neighbors.

    Attributes:
        key (Optional[str]): The string key associated with the data.
        value (Any): The payload or data stored in the node.
        prev (Optional[DLLNode]): Pointer to the previous node in the list.
        next (Optional[DLLNode]): Pointer to the next node in the list.
    """

    def __init__(self, key: Optional[str] = None, value: Any = None) -> None:
        """
        Initializes a DLLNode with optional key and value.

        Args:
            key (Optional[str]): The identifier for the node. Defaults to None.
            value (Any): The data to be stored. Defaults to None.
        """
        self.key = key
        self.value = value
        self.prev: Optional["DLLNode"] = None
        self.next: Optional["DLLNode"] = None


class DoublyLinkedList:
    """
    A Doubly Linked List implementation optimized for O(1) insertions and
    removals, utilizing permanent dummy nodes at the head and tail.

    Attributes:
        head (DLLNode): The permanent sentinel node at the front of the list.
        tail (DLLNode): The permanent sentinel node at the end of the list.
    """

    def __init__(self) -> None:
        """
        Initializes an empty Doubly Linked List by creating and wiring
        permanent dummy head and tail nodes.
        """
        self.head = DLLNode("DUMMY_HEAD", None)
        self.tail = DLLNode("DUMMY_TAIL", None)

        # Connect the anchors to represent an empty list
        self.head.next = self.tail
        self.tail.prev = self.head

    def add_node(self, new_node: DLLNode) -> None:
        """
        Inserts a new node at the beginning of the list, immediately
        following the dummy head. This position represents the
        'Most Recently Used' (MRU) item.

        Args:
            new_node (DLLNode): The node to be inserted into the list.
        """
        # Identify the current first real node
        first_real_node = self.head.next

        # Wire the new node to its neighbors
        new_node.prev = self.head
        new_node.next = first_real_node

        # Update neighbors to point to the new node
        self.head.next = new_node
        if first_real_node:
            first_real_node.prev = new_node

    def remove_node(self, node: DLLNode) -> None:
        """
        Removes an existing node from the list by wiring its neighbors
        to each other, effectively bypassing the target node.

        Args:
            node (DLLNode): The node to be removed from the chain.
        """
        prev_node = node.prev
        next_node = node.next

        # Patch the hole by connecting the neighbors
        if prev_node:
            prev_node.next = next_node
        if next_node:
            next_node.prev = prev_node

    def move_to_head(self, node: DLLNode) -> None:
        """
        Updates a node's position by removing it from its current
        location and re-inserting it at the head.

        Args:
            node (DLLNode): The node to be promoted to the MRU position.
        """
        self.remove_node(node)
        self.add_node(node)

    def pop_tail(self) -> Optional[DLLNode]:
        """
        Removes and returns the node immediately preceding the dummy tail.
        This represents the 'Least Recently Used' (LRU) item.

        Returns:
            Optional[DLLNode]: The evicted node, or None if the list is empty
            (i.e., contains only dummy nodes).
        """
        target = self.tail.prev

        # If the target is the head, the list is empty
        if target == self.head:
            return None

        if target:
            self.remove_node(target)

        return target
