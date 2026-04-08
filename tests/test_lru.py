from grazia.core.lru import DLLNode, DoublyLinkedList


def test_init_creates_and_wires_dummy_nodes() -> None:
    """Verifies that a new list is initialized with connected dummy anchors."""
    dll = DoublyLinkedList()

    assert dll.head.key == "DUMMY_HEAD"
    assert dll.tail.key == "DUMMY_TAIL"
    assert dll.head.next == dll.tail
    assert dll.tail.prev == dll.head


def test_add_node_inserts_at_mru_position() -> None:
    """Verifies that new nodes are always wedged directly after the head."""
    dll = DoublyLinkedList()

    node1 = DLLNode(key="k1", value="v1")
    dll.add_node(node1)

    # Check node1 is between head and tail
    assert dll.head.next == node1
    assert node1.prev == dll.head
    assert node1.next == dll.tail
    assert dll.tail.prev == node1

    # Add a second node and verify it pushes node1 down
    node2 = DLLNode(key="k2", value="v2")
    dll.add_node(node2)

    assert dll.head.next == node2
    assert node2.next == node1
    assert node1.prev == node2


def test_remove_node_patches_the_hole() -> None:
    """Verifies that removing a node correctly wires its neighbors to each other."""
    dll = DoublyLinkedList()
    node1 = DLLNode(key="k1", value="v1")
    node2 = DLLNode(key="k2", value="v2")
    node3 = DLLNode(key="k3", value="v3")

    # Order will be HEAD -> node3 -> node2 -> node1 -> TAIL
    dll.add_node(node1)
    dll.add_node(node2)
    dll.add_node(node3)

    # Remove the middle node (node2)
    dll.remove_node(node2)

    # Verify node3 points forward to node1
    assert node3.next == node1
    # Verify node1 points backward to node3
    assert node1.prev == node3


def test_move_to_head_promotes_node_to_mru() -> None:
    """Verifies that a node can be snipped from its position and moved to the front."""
    dll = DoublyLinkedList()
    node1 = DLLNode(key="k1", value="v1")
    node2 = DLLNode(key="k2", value="v2")

    # Order will be HEAD -> node2 -> node1 -> TAIL
    dll.add_node(node1)
    dll.add_node(node2)

    # Promote node1 back to the front
    dll.move_to_head(node1)

    # Verify node1 is now the MRU
    assert dll.head.next == node1
    assert node1.next == node2
    assert node2.prev == node1


def test_pop_tail_removes_and_returns_lru_node() -> None:
    """Verifies that popping the tail correctly evicts the oldest node."""
    dll = DoublyLinkedList()
    node1 = DLLNode(key="k1", value="v1")
    node2 = DLLNode(key="k2", value="v2")

    # Order will be HEAD -> node2 -> node1 -> TAIL
    dll.add_node(node1)
    dll.add_node(node2)

    # node1 is the oldest (LRU), it should be popped
    evicted_node = dll.pop_tail()

    assert evicted_node == node1
    # Verify it is actually gone from the list
    assert dll.tail.prev == node2
    assert node2.next == dll.tail


def test_pop_tail_returns_none_on_empty_list() -> None:
    """Verifies that popping an empty list handles the dummy nodes safely."""
    dll = DoublyLinkedList()

    evicted_node = dll.pop_tail()

    assert evicted_node is None
    # Verify dummies are still intact
    assert dll.head.next == dll.tail
    assert dll.tail.prev == dll.head
