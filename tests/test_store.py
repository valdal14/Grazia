import pytest

from grazia.core.exceptions import GraziaError, KeyNotFoundError
from grazia.core.store import GraziaStore, Store


def test_init_store() -> None:
    store = make_sut()
    assert isinstance(store, GraziaStore)


def test_set_throws_if_the_key_is_empty() -> None:
    store = make_sut()

    with pytest.raises(GraziaError) as exc_info:
        store.set(key="", value="user")

    assert "Invalid key: The key must be a non-empty string." in str(exc_info.value)


def test_set_allows_empty_values() -> None:
    store = make_sut()
    store.set(key="k", value="")

    assert store.get("k") == ""


def test_set_add_new_key_value_to_store_data() -> None:
    store = make_sut()
    store.set(key="k", value="user")

    assert store.get("k") == "user"


def test_get_returns_the_expected_value() -> None:
    store = make_sut()
    expected_key = "k"
    expected_value = "user"
    store.set(key=expected_key, value=expected_value)

    current_value = store.get(key=expected_key)
    assert current_value == expected_value


def test_get_throws_if_the_key_is_not_found() -> None:
    store = make_sut()
    key = "new_key"

    with pytest.raises(KeyNotFoundError) as exc_info:
        store.get(key=key)

    assert f"The given key '{key}' was not found." in str(exc_info.value)


def test_delete_successfully_delete_the_stored_value() -> None:
    store = make_sut()
    expected_key = "k"
    expected_value = "user"
    store.set(key=expected_key, value=expected_value)

    store.delete(key=expected_key)

    # Asserting via the public API that the key is gone
    with pytest.raises(KeyNotFoundError):
        store.get(key=expected_key)


def test_delete_throws_if_the_key_is_not_found() -> None:
    store = make_sut()
    key = "del_key"

    with pytest.raises(KeyNotFoundError) as exc_info:
        store.delete(key=key)

    assert f"The given key '{key}' was not found." in str(exc_info.value)


# NOTE: - Testing the LRU


def test_store_initializes_with_default_capacity():
    """
    Verifies that the GraziaStore initializes correctly with the default
    capacity of 1000 when no arguments are passed to the factory method.
    """
    sut = make_sut()
    assert sut.capacity == 1000


def test_store_initializes_with_custom_capacity():
    """
    Verifies that the GraziaStore initializes correctly when a specific,
    custom capacity is provided to the factory method.
    """
    sut = make_sut(capacity=50)
    assert sut.capacity == 50


def test_store_evicts_lru_item_when_capacity_reached():
    """
    Verifies that the GraziaStore enforces its capacity boundary by silently
    evicting the Least Recently Used (LRU) item when a new key-value pair
    is added that exceeds the maximum capacity.
    """
    sut = make_sut(capacity=1)
    sut.set(key="k1", value="<payload><status>new_user</status></payload>")
    # Add the second item. This should force 'k1' to be evicted.
    sut.set(key="k2", value="<payload><status>active_user</status></payload>")

    # Verify 'k2' exists
    assert sut.get("k2") == "<payload><status>active_user</status></payload>"

    # Verify 'k1' is completely gone by expecting a KeyNotFoundError
    with pytest.raises(KeyNotFoundError):
        sut.get("k1")


def test_store_tracks_internal_size():
    """
    Verifies that the GraziaStore accurately tracks the number of items
    currently held within it using its internal _size attribute, and
    ensures the size does not exceed capacity during eviction.
    """
    sut = make_sut(capacity=2)

    sut.set(key="k1", value="<payload><user_id>1</user_id></payload>")
    assert sut._size == 1

    sut.set(key="k2", value="<payload><user_id>2</user_id></payload>")
    assert sut._size == 2

    # This third addition triggers an eviction.
    # Size should drop to 1 internally, then back to 2, never reaching 3.
    sut.set(key="k3", value="<payload><user_id>3</user_id></payload>")
    assert sut._size == 2


def test_store_get_promotes_key_to_mru():
    """
    Verifies that accessing an existing key via get() promotes it to the
    Most Recently Used (MRU) position in the cache. This protects the key
    from being the next item evicted when the store reaches maximum capacity.
    """
    sut = make_sut(capacity=2)

    # Fill the store to capacity
    sut.set(key="user_1", value="<payload><status>active</status></payload>")
    sut.set(key="user_2", value="<payload><status>idle</status></payload>")

    # Access "user_1". It was the LRU, but this get() should promote it to MRU.
    # This makes "user_2" the new LRU.
    sut.get("user_1")

    # Add a 3rd item, forcing an eviction. "user_2" should be evicted, not "user_1".
    sut.set(key="user_3", value="<payload><status>new</status></payload>")

    # Verify "user_1" survived
    assert sut.get("user_1") == "<payload><status>active</status></payload>"
    # Verify "user_3" was added successfully
    assert sut.get("user_3") == "<payload><status>new</status></payload>"

    # Verify "user_2" was the one evicted
    with pytest.raises(KeyNotFoundError):
        sut.get("user_2")


def test_store_set_existing_key_promotes_to_mru():
    """
    Verifies that updating an existing key via set() promotes it to the
    Most Recently Used (MRU) position. This protects the updated key
    from being the next item evicted when the store reaches maximum capacity.
    """
    sut = make_sut(capacity=2)

    # Fill the store to capacity
    sut.set(key="config_a", value="<payload><theme>dark</theme></payload>")
    sut.set(key="config_b", value="<payload><theme>light</theme></payload>")

    # Update "config_a". It was the LRU, but this set() should promote it to MRU.
    # This makes "config_b" the new LRU.
    sut.set(key="config_a", value="<payload><theme>blue</theme></payload>")

    # Add a 3rd item, forcing an eviction. "config_b" should be evicted.
    sut.set(key="config_c", value="<payload><theme>system</theme></payload>")

    # Verify "config_a" survived and has the updated value
    assert sut.get("config_a") == "<payload><theme>blue</theme></payload>"
    # Verify "config_c" was added successfully
    assert sut.get("config_c") == "<payload><theme>system</theme></payload>"

    # Verify "config_b" was the one evicted
    with pytest.raises(KeyNotFoundError):
        sut.get("config_b")


def test_abstract_methods_can_be_called_via_super():
    """
    Verifies that the abstract methods in GraziaStore can be called.
    This exists purely to satisfy test coverage for the interface's `pass` statements.
    """

    class DummyStore(GraziaStore):
        def set(self, key: str, value: any) -> None:
            super().set(key, value)

        def get(self, key: str) -> any:
            super().get(key)

        def delete(self, key: str) -> None:
            super().delete(key)

    dummy = DummyStore()
    assert dummy.set("k", "v") is None
    assert dummy.get("k") is None
    assert dummy.delete("k") is None


def test_store_eviction_successfully_deletes_from_hashmap():
    """
    Verifies that when an item is evicted, it is successfully removed
    from the underlying HashMap engine and the size is strictly decremented.
    If this test fails, pop_tail() may be returning a dummy node.
    """
    sut = Store(capacity=1)

    # Fill to capacity
    sut.set(key="k1", value="<payload><data>first</data></payload>")

    # Force eviction of k1
    sut.set(key="k2", value="<payload><data>second</data></payload>")

    # Ensure size is strictly 1
    assert sut._size == 1

    # Ensure k1 is entirely gone from the underlying HashMap
    # (Bypassing the public get() to check internal state directly)
    with pytest.raises(KeyNotFoundError):
        sut._data.get("k1")


# NOTE: - Helpers methods ########################


def make_sut(capacity: int = 1000) -> GraziaStore:
    """Factory method to create the System Under Test."""
    return Store(capacity=capacity)
