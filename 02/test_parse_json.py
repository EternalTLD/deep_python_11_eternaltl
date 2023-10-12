from unittest.mock import call
import pytest

from parse_json import parse_json


def test_one_keyword(mocker):
    json_str = '{"key1": "word2 word1", "key2": "word1 word3"}'
    callback = mocker.Mock()
    required_fields = ["key1", "key2"]
    keywords = ["word1"]
    parse_json(json_str, callback, required_fields, keywords)
    expected_calls = [call("key1", "word1"), call("key2", "word1")]
    assert callback.call_args_list == expected_calls
    assert callback.call_count == 2


def test_many_keywords(mocker):
    json_str = '{"key1": "word2 word1", "key2": "word1 word3"}'
    callback = mocker.Mock()
    required_fields = ["key1", "key2"]
    keywords = ["word1", "word3", "word4"]
    parse_json(json_str, callback, required_fields, keywords)
    expected_calls = [
        call("key1", "word1"),
        call("key2", "word1"),
        call("key2", "word3"),
    ]
    assert callback.call_args_list == expected_calls
    assert callback.call_count == 3


def test_many_same_keywords_in_one_field(mocker):
    json_str = '{"key1": "word2 word1 word2", "key2": "word3 word3 word3"}'
    callback = mocker.Mock()
    required_fields = ["key1", "key2"]
    keywords = ["word2", "word3"]
    parse_json(json_str, callback, required_fields, keywords)
    expected_calls = [call("key1", "word2"), call("key2", "word3")]
    assert callback.call_args_list == expected_calls
    assert callback.call_count == 2


def test_no_keywords_in_fields(mocker):
    json_str = '{"key1": "word2 word1 word2", "key2": "word3 word3 word3"}'
    callback = mocker.Mock()
    required_fields = ["key1", "key2"]
    keywords = ["word4", "word5"]
    parse_json(json_str, callback, required_fields, keywords)
    assert not callback.called


def test_empty_keywords(mocker):
    json_str = '{"key1": "word2 word1", "key2": "word1 word3"}'
    callback = mocker.Mock()
    required_fields = ["Key1", "key2"]
    keywords = []
    parse_json(json_str, callback, required_fields, keywords)
    assert not callback.called


def test_keywords_case_insensitive(mocker):
    json_str = '{"key1": "Word2 word1", "key2": "wORd1 word3 word1", "key3": "woRD2"}'
    callback = mocker.Mock()
    required_fields = ["key1", "key2"]
    keywords = ["wOrD1", "word2", "WORD3"]
    parse_json(json_str, callback, required_fields, keywords)
    expected_calls = [
        call("key1", "wOrD1"),
        call("key1", "word2"),
        call("key2", "wOrD1"),
        call("key2", "WORD3"),
    ]
    assert callback.call_args_list == expected_calls
    assert callback.call_count == 4


def test_keywords_match(mocker):
    json_str = '{"key1": "tester testing", "key2": "beta-test test"}'
    required_fields = ["key1", "key2"]
    callback = mocker.Mock()

    keywords = ["testinggg"]
    parse_json(json_str, callback, required_fields, keywords)
    assert not callback.called

    keywords = ["tes"]
    parse_json(json_str, callback, required_fields, keywords)
    assert not callback.called

    keywords = ["test"]
    parse_json(json_str, callback, required_fields, keywords)
    assert callback.call_args_list == [call("key2", "test")]
    assert callback.call_count == 1


def test_one_required_field(mocker):
    json_str = '{"key1": "Word2 word1", "key2": "wORd1 word3 word1", "key3": "woRD2"}'
    callback = mocker.Mock()
    required_fields = ["key1"]
    keywords = ["wOrD1", "word2", "WORD3"]
    parse_json(json_str, callback, required_fields, keywords)
    assert callback.call_count == 2
    assert callback.call_args_list == [call("key1", "wOrD1"), call("key1", "word2")]


def test_empty_required_fields(mocker):
    json_str = '{"key1": "word2 word1", "key2": "word1 word3"}'
    callback = mocker.Mock()
    required_fields = []
    keywords = ["wOrD1", "WORD3"]
    parse_json(json_str, callback, required_fields, keywords)
    assert not callback.called


def test_required_fields_case_sensitive(mocker):
    json_str = '{"key1": "word2 word1 word3", "key2": "word1 word3"}'
    callback = mocker.Mock()
    required_fields = ["KEY1"]
    keywords = ["WORD3"]
    parse_json(json_str, callback, required_fields, keywords)
    assert not callback.called


@pytest.mark.parametrize("json_str", [1, 0.1, (1, 2, 3), [1, 2, 3], {"1": 1}, None])
def test_json_str_type(mocker, json_str):
    callback = mocker.Mock()
    required_fields = ["key1"]
    keywords = ["word1"]
    with pytest.raises(TypeError) as exception:
        assert parse_json(json_str, callback, required_fields, keywords)
    assert "Variable 'json_str' must be str" in str(exception.value)


def test_keyword_callback_is_none():
    json_str = '{"key1": "Word2 word1", "key2": "wORd1 word3 word1", "key3": "woRD2"}'
    callback = None
    required_fields = ["key1"]
    keywords = ["word1"]
    with pytest.raises(TypeError) as exception:
        assert parse_json(json_str, callback, required_fields, keywords)
    assert "Variable 'keyword_callback' should not be None" in str(exception.value)


def test_required_fields_is_none(mocker):
    json_str = '{"key1": "Word2 word1", "key2": "wORd1 word3 word1", "key3": "woRD2"}'
    callback = mocker.Mock()
    required_fields = None
    keywords = ["word1"]
    with pytest.raises(TypeError) as exception:
        assert parse_json(json_str, callback, required_fields, keywords)
    assert "Variable 'required_fields' should not be None" in str(exception.value)


def test_keywords_is_none(mocker):
    json_str = '{"key1": "Word2 word1", "key2": "wORd1 word3 word1", "key3": "woRD2"}'
    callback = mocker.Mock()
    required_fields = ["key1"]
    keywords = None
    with pytest.raises(TypeError) as exception:
        assert parse_json(json_str, callback, required_fields, keywords)
    assert "Variable 'keywords' should not be None" in str(exception.value)
