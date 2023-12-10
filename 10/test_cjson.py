import json
import ujson
import cjson
import pytest


def test_loads():
    json_str = '{"hello": 10, "world": "value"}'

    json_doc = json.loads(json_str)
    cjson_doc = cjson.loads(json_str)
    ujson_doc = ujson.loads(json_str)

    assert json_doc == cjson_doc == ujson_doc
    assert isinstance(json_doc, dict)
    assert isinstance(cjson_doc, dict)
    assert isinstance(ujson_doc, dict)


def test_dumps():
    json_doc = {"hello": 10, "world": "value"}

    json_str = json.dumps(json_doc)
    cjson_str = json.dumps(json_doc)
    ujson_str = json.dumps(json_doc)

    assert json_str == cjson_str == ujson_str
    assert isinstance(json_str, str)
    assert isinstance(cjson_str, str)
    assert isinstance(ujson_str, str)


def test_empty_dumps_and_loads():
    json_doc = {}

    json_str = json.dumps(json_doc)
    cjson_str = json.dumps(json_doc)
    ujson_str = json.dumps(json_doc)

    assert json_str == cjson_str == ujson_str
    assert isinstance(json_str, str)
    assert isinstance(cjson_str, str)
    assert isinstance(ujson_str, str)

    json_str = "{}"

    json_doc = json.loads(json_str)
    cjson_doc = cjson.loads(json_str)
    ujson_doc = ujson.loads(json_str)

    assert json_doc == cjson_doc == ujson_doc
    assert isinstance(json_doc, dict)
    assert isinstance(cjson_doc, dict)
    assert isinstance(ujson_doc, dict)


@pytest.mark.parametrize(
    "arg", [1, 1.5, [1, 2, 3], (1, 2, "3"), {"k": "v", "k2": 2}, None]
)
def test_cjson_loads_args(arg):
    with pytest.raises(TypeError) as exception:
        cjson.loads(arg)

    assert "Invalid argument. Expected string." in str(exception.value)


@pytest.mark.parametrize(
    "arg", [1, 1.5, [1, 2, 3], (1, 2, "3"), '{"k": "v", "k2": 2}', None]
)
def test_cjson_dumps_args(arg):
    with pytest.raises(TypeError) as exception:
        cjson.dumps(arg)

    assert "Invalid argument. Expected dictionary." in str(exception.value)