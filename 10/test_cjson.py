from time import time
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
    assert type(json_doc) == type(cjson_doc) == type(ujson_doc)


def test_dumps():
    json_doc = {"hello": 10, "world": "value"}

    json_str = json.dumps(json_doc)
    cjson_str = json.dumps(json_doc)
    ujson_str = json.dumps(json_doc)

    assert json_str == cjson_str == ujson_str
    assert type(json_str) == type(cjson_str) == type(ujson_str)


def test_empty_dumps_and_loads():
    json_doc = {}

    json_str = json.dumps(json_doc)
    cjson_str = json.dumps(json_doc)
    ujson_str = json.dumps(json_doc)

    assert json_str == cjson_str == ujson_str
    assert type(json_str) == type(cjson_str) == type(ujson_str)

    json_str = "{}"

    json_doc = json.loads(json_str)
    cjson_doc = cjson.loads(json_str)
    ujson_doc = ujson.loads(json_str)

    assert json_doc == cjson_doc == ujson_doc
    assert type(json_doc) == type(cjson_doc) == type(ujson_doc)


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


def measure_dumps_time(lib, data, measurements):
    start_time = time()
    for _ in range(5):
        for json in data:
            lib.dumps(json)
    print(
        f"[{lib.__name__}] Dumps time of {measurements} measurements - {(time()-start_time)/5}"
    )


def measure_loads_time(lib, data, measurements):
    start_time = time()
    for _ in range(measurements):
        for json in data:
            lib.loads(json)
    print(
        f"[{lib.__name__}] Loads time of {measurements} measurements - {(time()-start_time)/5}"
    )


if __name__ == "__main__":
    MEASUREMENTS = 10

    with open("data.json", "r") as json_file:
        data_doc = json.load(json_file)

    json_str = []
    for data in data_doc:
        json_str.append(json.dumps(data))

    measure_dumps_time(json, data_doc, MEASUREMENTS)
    measure_dumps_time(ujson, data_doc, MEASUREMENTS)
    measure_dumps_time(cjson, data_doc, MEASUREMENTS)

    measure_loads_time(json, json_str, MEASUREMENTS)
    measure_loads_time(ujson, json_str, MEASUREMENTS)
    measure_loads_time(cjson, json_str, MEASUREMENTS)
