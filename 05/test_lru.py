import pytest

from lru import LRUCache


def test_cache_keys_order():
    cache = LRUCache(3)
    cache.set("k1", "val1")
    cache.set("k2", "val2")
    cache.set("k3", "val3")
    assert list(cache.cache_dict.keys()) == ["k1", "k2", "k3"]

    cache.set("k2", "val2")
    assert list(cache.cache_dict.keys()) == ["k1", "k3", "k2"]

    cache.set("k1", "val1")
    assert list(cache.cache_dict.keys()) == ["k3", "k2", "k1"]

    cache.set("k3", "val1")
    assert list(cache.cache_dict.keys()) == ["k2", "k1", "k3"]


def test_cache_get_and_set():
    cache = LRUCache(2)

    cache.set("k1", "val1")
    cache.set("k2", "val2")

    assert cache.get("k3") is None
    assert cache.get("k2") == "val2"
    assert cache.get("k1") == "val1"

    cache.set("k3", "val3")

    assert cache.get("k3") == "val3"
    assert cache.get("k2") is None
    assert cache.get("k1") == "val1"

    cache.set("k2", 0)

    assert cache.get("k3") is None
    assert cache.get("k2") == 0
    assert cache.get("k1") == "val1"

    cache.set("k4", [])

    assert cache.get("k3") is None
    assert cache.get("k2") is None
    assert cache.get("k1") == "val1"
    assert cache.get("k4") == []


def test_update_existing_key():
    cache = LRUCache(2)

    cache.set("k1", "val1")
    cache.set("k2", "val2")
    assert cache.get("k1") == "val1"
    assert cache.get("k2") == "val2"

    cache.set("k1", "new_val1")
    cache.set("k3", "val3")

    assert cache.get("k1") == "new_val1"
    assert cache.get("k2") is None
    assert cache.get("k3") == "val3"


def test_limit_equal_one():
    cache = LRUCache(1)

    cache.set("k1", "val1")
    assert cache.get("k1") == "val1"
    assert cache.get("k2") is None

    cache.set("k2", 0)
    assert cache.get("k1") is None
    assert cache.get("k2") == 0

    cache.set("k1", [1, 2, 3])
    assert cache.get("k1") == [1, 2, 3]
    assert cache.get("k2") is None


def test_cache_limit_value():
    with pytest.raises(ValueError) as exception:
        assert LRUCache(0)
    assert "Cache limit must be greater then 0" in str(exception.value)

    with pytest.raises(ValueError) as exception:
        assert LRUCache(-999)
    assert "Cache limit must be greater then 0" in str(exception.value)


@pytest.mark.parametrize("limit", ["1", 0.1, [1, 2, 3], (1, 2, 3), {"1": 1}, None])
def test_cache_limit_type(limit):
    with pytest.raises(TypeError) as exception:
        assert LRUCache(limit)
    assert "Cache limit must be int" in str(exception.value)
