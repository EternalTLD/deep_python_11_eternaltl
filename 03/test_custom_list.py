import pytest

from custom_list import CustomList


def test_custom_list_add():
    list1 = CustomList([1, 2, 3])
    list2 = CustomList([4, 5, 6])
    assert list1 + list2 == CustomList([5, 7, 9])

    list1 = CustomList([1, 2, 3, 10])
    list2 = CustomList([4, 5, 6])
    assert list1 + list2 == CustomList([5, 7, 9, 10])

    list1 = CustomList([1, 2, 3])
    list2 = CustomList([4, 5, 6, 10])
    assert list1 + list2 == CustomList([5, 7, 9, 10])


def test_custom_list_and_list_add():
    list1 = CustomList([1, 2, 3])
    list2 = [4, 5, 6]
    assert list1 + list2 == CustomList([5, 7, 9])
    assert list2 + list1 == CustomList([5, 7, 9])

    list1 = CustomList([1, 2, 3, 10])
    list2 = [4, 5, 6]
    assert list1 + list2 == CustomList([5, 7, 9, 10])
    assert list2 + list1 == CustomList([5, 7, 9, 10])

    list1 = CustomList([1, 2, 3])
    list2 = [4, 5, 6, 10]
    assert list1 + list2 == CustomList([5, 7, 9, 10])
    assert list2 + list1 == CustomList([5, 7, 9, 10])


def test_custom_list_sub():
    list1 = CustomList([1, 2, 3])
    list2 = CustomList([4, 5, 6])
    assert list1 - list2 == CustomList([-3, -3, -3])
    assert list2 - list1 == CustomList([3, 3, 3])

    list1 = CustomList([1, 2, 3, 10])
    list2 = CustomList([4, 5, 6])
    assert list1 - list2 == CustomList([-3, -3, -3, 10])
    assert list2 - list1 == CustomList([3, 3, 3, -10])

    list1 = CustomList([1, 2, 3])
    list2 = CustomList([4, 5, 6, 10])
    assert list1 - list2 == CustomList([-3, -3, -3, -10])
    assert list2 - list1 == CustomList([3, 3, 3, 10])


def test_custom_list_and_list_sub():
    list1 = CustomList([1, 2, 3])
    list2 = [4, 5, 6]
    assert list1 - list2 == CustomList([-3, -3, -3])
    assert list2 - list1 == CustomList([3, 3, 3])

    list1 = CustomList([1, 2, 3, 10])
    list2 = [4, 5, 6]
    assert list1 - list2 == CustomList([-3, -3, -3, 10])
    assert list2 - list1 == CustomList([3, 3, 3, -10])

    list1 = CustomList([1, 2, 3])
    list2 = [4, 5, 6, 10]
    assert list1 - list2 == CustomList([-3, -3, -3, -10])
    assert list2 - list1 == CustomList([3, 3, 3, 10])


def test_custom_list_immutability():
    list1 = CustomList([1, 2, 3])
    list2 = [4, 5, 6, 10]
    list3 = list1 + list2
    assert list1 == CustomList([1, 2, 3])
    assert list2 == [4, 5, 6, 10]
    assert list3 == CustomList([5, 7, 9, 10])


def test_list_immutability():
    list1 = [1, 2, 3]
    list2 = CustomList([4, 5, 6, 10])
    list3 = list1 - list2
    assert list1 == [1, 2, 3]
    assert list2 == CustomList([4, 5, 6, 10])
    assert list3 == CustomList([-3, -3, -3, -10])


@pytest.mark.parametrize(
    "list1, list2",
    [
        (CustomList([1, 2, 3]), CustomList([4, 5, 6])),
        (CustomList([4, 5]) + CustomList([6]), CustomList([5, 5, 6])),
        (CustomList([9, 9]) - CustomList([7]), CustomList([4]) + CustomList([4, 5])),
    ],
)
def test_comparison_operators_not_equal_lists(list1, list2):
    assert (list1 == list2) is False
    assert (list1 != list2) is True
    assert (list2 > list1) is True
    assert (list1 > list2) is False
    assert (list2 < list1) is False
    assert (list1 < list2) is True
    assert (list2 <= list1) is False
    assert (list1 <= list2) is True
    assert (list2 >= list1) is True
    assert (list1 >= list2) is False


@pytest.mark.parametrize(
    "list1, list2",
    [
        (CustomList([1, 2, 3]), CustomList([1, 2, 3])),
        (CustomList([2, 4, 7]), CustomList([3, 9, 1])),
        (CustomList([2, 4]) + CustomList([7]), CustomList([3, 9, 1])),
        (CustomList([9, 9]) - CustomList([7]), CustomList([3]) + CustomList([4, 4])),
    ],
)
def test_comparison_operators_equal_lists(list1, list2):
    assert (list1 == list2) is True
    assert (list1 != list2) is False
    assert (list2 > list1) is False
    assert (list1 > list2) is False
    assert (list2 < list1) is False
    assert (list1 < list2) is False
    assert (list2 <= list1) is True
    assert (list1 <= list2) is True
    assert (list2 >= list1) is True
    assert (list1 >= list2) is True


def test_list_str(capsys):
    print(CustomList([1, 2, 3]))
    captured = capsys.readouterr()
    assert "CustomList([1, 2, 3]), sum - 6" in captured.out


@pytest.mark.parametrize("other_list", [1, 0.1, "1", (1, 2, 3), {"1": 1}, {1, 2, 3}])
def test_other_list_type(other_list):
    custom_list = CustomList([1, 2, 3])
    with pytest.raises(TypeError) as exception:
        result = custom_list + other_list
        assert result is None
    assert "Addition operation can only be performed on lists" in str(exception.value)

    with pytest.raises(TypeError) as exception:
        result = other_list + custom_list
        assert result is None
    assert "Addition operation can only be performed on lists" in str(exception.value)

    with pytest.raises(TypeError) as exception:
        result = custom_list - other_list
        assert result is None
    assert "Subtraction operation can only be performed on lists" in str(
        exception.value
    )

    with pytest.raises(TypeError) as exception:
        result = other_list - custom_list
        assert result is None
    assert "Subtraction operation can only be performed on lists" in str(
        exception.value
    )
