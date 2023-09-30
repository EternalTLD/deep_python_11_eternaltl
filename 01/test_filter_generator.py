from io import StringIO
import os
import pytest

from filter_generator import filter_generator


def setup_test_file(test_data):
    with open("test.txt", "w", encoding="utf-8") as file_object:
        file_object.writelines(test_data)


def test_with_file_object():
    test_data = "word1 test1\n word2 test2\n word3 test3 word2\n"
    file_object = StringIO(test_data)
    search_words = ["word2"]
    result = list(filter_generator(file_object, search_words))
    assert result == ["word2 test2", "word3 test3 word2"]


def test_with_file_name():
    test_data = ["word1 test1\n", "word2 test2\n", "word3 test3 word2\n"]
    setup_test_file(test_data)
    search_words = ["word2"]
    result = list(filter_generator("test.txt", search_words))
    assert result == ["word2 test2", "word3 test3 word2"]
    os.remove("test.txt")


def test_data_case_insensitive():
    test_data = ["worD1 test1\n", "WoRd2 tEst2\n", "wOrd3 tesT3 wOrD2\n"]
    setup_test_file(test_data)
    search_words = ["word2"]
    result = list(filter_generator("test.txt", search_words))
    assert result == ["WoRd2 tEst2", "wOrd3 tesT3 wOrD2"]
    os.remove("test.txt")


def test_words_case_insensitive():
    test_data = ["worD1 test1\n", "WoRd2 tEst2\n", "wOrd3 tesT3 wOrD2\n"]
    setup_test_file(test_data)
    search_words = ["WorD2"]
    result = list(filter_generator("test.txt", search_words))
    assert result == ["WoRd2 tEst2", "wOrd3 tesT3 wOrD2"]
    os.remove("test.txt")


def test_two_words():
    test_data = ["test word1\n", "word2 test\n", "test word2 test\n"]
    setup_test_file(test_data)
    search_words = ["word1", "word2"]
    result = list(filter_generator("test.txt", search_words))
    assert result == ["test word1", "word2 test", "test word2 test"]
    os.remove("test.txt")


def test_word_match():
    test_data = ["testing word1\n", "test word2\n", "tester word3\n"]
    setup_test_file(test_data)
    search_words = ["test", "testinggg"]
    result = list(filter_generator("test.txt", search_words))
    assert result == ["test word2"]

    search_words = ["tester"]
    result = list(filter_generator("test.txt", search_words))
    assert result == ["tester word3"]

    search_words = ["tes", "testinggg"]
    result = list(filter_generator("test.txt", search_words))
    assert not result
    os.remove("test.txt")


@pytest.mark.parametrize("search_words", [1, 0.1, (1, 2, 3), {"1": 1}, "test"])
def test_search_words_type(search_words):
    with pytest.raises(TypeError) as exception:
        next(filter_generator("test.txt", search_words))
    assert "Variable 'search_words' must be list of str" in str(exception.value)


@pytest.mark.parametrize("file_or_file_name", [1, 0.1, (1, 2, 3), {"1": 1}, [1, 2, 3]])
def test_file_or_file_name_type(file_or_file_name):
    search_words = ["test"]
    with pytest.raises(TypeError) as exception:
        next(filter_generator(file_or_file_name, search_words))
    assert "Variable 'file_or_file_name' must be string or file object" in str(
        exception.value
    )
