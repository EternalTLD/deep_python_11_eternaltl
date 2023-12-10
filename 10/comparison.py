from time import time
import json
import ujson
import cjson


def test_dumps_time(library, measurements):
    with open("data.json", "r", encoding="utf-8") as json_file:
        data = json.load(json_file)

    start_time = time()
    for _ in range(measurements):
        for json_data in data:
            library.dumps(json_data)

    print(
        f"[{library.__name__}] Dumps time  - {round((time()-start_time)/measurements, 3)}"
    )


def test_loads_time(library, measurements):
    start_time = time()
    for _ in range(measurements):
        with open("data.json", "r", encoding="utf-8") as json_file:
            for json_data in json_file:
                library.loads(json_data)

    print(
        f"[{library.__name__}] Loads time - {round((time()-start_time)/measurements, 3)}"
    )


if __name__ == "__main__":
    MEASUREMENTS = 5
    libs = [json, ujson, cjson]
    for lib in libs:
        test_dumps_time(lib, MEASUREMENTS)
        test_loads_time(lib, MEASUREMENTS)
