import pytest

from custom_meta import CustomMeta


class CustomMetaTest(metaclass=CustomMeta):
    attr = 10

    def __init__(self, value="value"):
        self.value = value

    def test_method(self):
        return "Test method"

    def __str__(self):
        return "__str__"


def test_class_attr():
    test_object = CustomMetaTest()
    assert test_object.custom_attr == 10
    with pytest.raises(AttributeError):
        assert test_object.attr


def test_object_attr():
    test_object = CustomMetaTest()
    assert test_object.custom_value == "value"
    with pytest.raises(AttributeError):
        assert test_object.value


def test_method():
    test_object = CustomMetaTest()
    assert test_object.custom_test_method() == "Test method"
    with pytest.raises(AttributeError):
        assert test_object.test_method()


def test_magic_method():
    test_object = CustomMetaTest()

    assert str(test_object) == "__str__"
    with pytest.raises(AttributeError):
        assert test_object.custom___str__()

    assert hasattr(test_object, "__init__")
    assert not hasattr(test_object, "custom__init__")


def test_dynamic_added_attr():
    test_object = CustomMetaTest()
    test_object.dynamic = "dynamic"
    assert test_object.custom_dynamic == "dynamic"
    with pytest.raises(AttributeError):
        assert test_object.dynamic
