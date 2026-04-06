import pytest

from grazia.core.exceptions import GraziaError
from grazia.core.store import GraziaStore, Store


def test_init_store():
    store = make_sut()
    assert isinstance(store, GraziaStore)
    assert len(store._data) == 0


def test_set_throws_if_the_key_is_empty():
    store = make_sut()

    with pytest.raises(GraziaError) as exc_info:
        store.set(key="", value="user")

    assert "Invalid key: The key cannot be an empty string." in str(exc_info.value)


def test_set_throws_if_the_value_is_empty():
    store = make_sut()

    with pytest.raises(GraziaError) as exc_info:
        store.set(key="k", value="")

    assert "Invalid value: The value cannot be an empty string." in str(exc_info.value)


def test_set_add_new_key_value_to_store_data():
    store = make_sut()
    store.set(key="k", value="user")
    assert len(store._data) == 1
    assert store._data["k"] == "user"


# NOTE: - Helpers methods ########################


def make_sut() -> GraziaStore:
    return Store()
