import json
import os

from parse_json import parse_json


class TestCallback:
    def callback(self, keyword):
        return "Called for " + keyword


def setup_json_file(data):
    with open("test_json.json", "w", encoding="utf-8") as file_object:
        file_object.write(json.dumps(data))


def test_callback_return(mocker):
    json_data = {"key1": "word1 word2", "key2": "word2 word3"}
    setup_json_file(json_data)
    with open("test_json.json", "r", encoding="utf-8") as file_object:
        json_str = file_object.read()
    callback = mocker.spy(TestCallback(), "callback")
    required_fields = ["key1"]
    keywords = ["word2"]
    parse_json(json_str, callback, required_fields, keywords)
    assert callback.spy_return == "Called for word2"
    os.remove("test_json.json")


def test_one_keyword(mocker):
    json_data = {"key1": "word2 word1", "key2": "word1 word3"}
    setup_json_file(json_data)
    with open("test_json.json", "r", encoding="utf-8") as file_object:
        json_str = file_object.read()
    callback = mocker.spy(TestCallback(), "callback")
    required_fields = ["key1", "key2"]
    keywords = ["word1"]
    parse_json(json_str, callback, required_fields, keywords)
    assert callback.call_count == 2
    os.remove("test_json.json")


def test_many_keywords(mocker):
    json_data = {"key1": "word2 word1", "key2": "word1 word3"}
    setup_json_file(json_data)
    with open("test_json.json", "r", encoding="utf-8") as file_object:
        json_str = file_object.read()
    callback = mocker.spy(TestCallback(), "callback")
    required_fields = ["key1", "key2"]
    keywords = ["word1", "word3", "word4"]
    parse_json(json_str, callback, required_fields, keywords)
    assert callback.call_count == 3
    os.remove("test_json.json")


def test_empty_keywords(mocker):
    json_data = {"key1": "word2 word1", "key2": "word1 word3"}
    setup_json_file(json_data)
    with open("test_json.json", "r", encoding="utf-8") as file_object:
        json_str = file_object.read()
    callback = mocker.spy(TestCallback(), "callback")
    required_fields = ["Key1", "key2"]
    keywords = []
    parse_json(json_str, callback, required_fields, keywords)
    assert callback.call_count == 0
    os.remove("test_json.json")


def test_keywords_case_insensitive(mocker):
    json_data = {"key1": "Word2 word1", "key2": "wORd1 word3 word1", "key3": "woRD2"}
    setup_json_file(json_data)
    with open("test_json.json", "r", encoding="utf-8") as file_object:
        json_str = file_object.read()
    callback = mocker.spy(TestCallback(), "callback")
    required_fields = ["key1", "key2"]
    keywords = ["wOrD1", "word2", "WORD3"]
    parse_json(json_str, callback, required_fields, keywords)
    assert callback.call_count == 5
    os.remove("test_json.json")


def test_keywords_match(mocker):
    json_data = {"key1": "tester testing", "key2": "beta-test test"}
    setup_json_file(json_data)
    with open("test_json.json", "r", encoding="utf-8") as file_object:
        json_str = file_object.read()
    required_fields = ["key1", "key2"]
    callback = mocker.spy(TestCallback(), "callback")

    keywords = ["testinggg"]
    parse_json(json_str, callback, required_fields, keywords)
    assert callback.call_count == 0

    keywords = ["tes"]
    parse_json(json_str, callback, required_fields, keywords)
    assert callback.call_count == 0

    keywords = ["test"]
    parse_json(json_str, callback, required_fields, keywords)
    assert callback.call_count == 1
    os.remove("test_json.json")


def test_one_required_field(mocker):
    json_data = {"key1": "Word2 word1", "key2": "wORd1 word3 word1", "key3": "woRD2"}
    setup_json_file(json_data)
    with open("test_json.json", "r", encoding="utf-8") as file_object:
        json_str = file_object.read()
    callback = mocker.spy(TestCallback(), "callback")
    required_fields = ["key1"]
    keywords = ["wOrD1", "word2", "WORD3"]
    parse_json(json_str, callback, required_fields, keywords)
    assert callback.call_count == 2
    os.remove("test_json.json")


def test_empty_required_fields(mocker):
    json_data = {"key1": "word2 word1", "key2": "word1 word3"}
    setup_json_file(json_data)
    with open("test_json.json", "r", encoding="utf-8") as file_object:
        json_str = file_object.read()
    callback = mocker.spy(TestCallback(), "callback")
    required_fields = []
    keywords = ["wOrD1", "WORD3"]
    parse_json(json_str, callback, required_fields, keywords)
    assert callback.call_count == 0
    os.remove("test_json.json")


def test_required_fields_case_sensitive(mocker):
    json_data = {"key1": "word2 word1 word3", "key2": "word1 word3"}
    setup_json_file(json_data)
    with open("test_json.json", "r", encoding="utf-8") as file_object:
        json_str = file_object.read()
    callback = mocker.spy(TestCallback(), "callback")
    required_fields = ["KEY1"]
    keywords = ["WORD3"]
    parse_json(json_str, callback, required_fields, keywords)
    assert callback.call_count == 0
    os.remove("test_json.json")
