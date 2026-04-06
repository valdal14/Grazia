import pytest

from grazia.core.exceptions import GraziaError, KeyNotFoundError
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


def test_get_returns_the_expected_value():
    store = make_sut()
    expected_key = "k"
    expected_value = "user"
    store.set(key=expected_key, value=expected_value)

    current_value = store.get(key=expected_key)
    assert current_value == expected_value


def test_get_throws_if_the_key_is_not_found():
    store = make_sut()
    key = "new_key"

    with pytest.raises(KeyNotFoundError) as exc_info:
        store.get(key=key)

    assert f"The given key '{key}' was not found." in str(exc_info.value)


def test_delete_successfully_delete_the_stored_value():
    store = make_sut()
    expected_key = "k"
    expected_value = "user"
    store.set(key=expected_key, value=expected_value)
    store.delete(key="k")
    # using get to prove the value and key were delete
    # by checking that the get raises and error
    with pytest.raises(KeyNotFoundError):
        store.get(key=expected_key)
    # double check that data is empty
    assert len(store._data) == 0


def test_delete_throws_if_the_key_is_not_found():
    store = make_sut()
    key = "del_key"

    with pytest.raises(KeyNotFoundError) as exc_info:
        store.delete(key=key)

    assert f"The given key '{key}' was not found." in str(exc_info.value)


# NOTE: - Helpers methods ########################


def make_sut() -> GraziaStore:
    return Store()
