import json


def parse_json(json_str: str, keyword_callback, required_fields=None, keywords=None):
    if not isinstance(json_str, str):
        raise TypeError("Variable 'json_str' must be str")
    if keyword_callback is None:
        raise TypeError("Variable 'keyword_callback' should not be None")
    if required_fields is None:
        raise TypeError("Variable 'required_fields' should not be None")
    if keywords is None:
        raise TypeError("Variable 'keywords' should not be None")

    json_doc = json.loads(json_str)
    for field in required_fields:
        if field in json_doc.keys():
            value_str = json_doc[field]
            value_list = value_str.split()
            for keyword in keywords:
                if keyword.lower() in map(lambda value: value.lower(), value_list):
                    keyword_callback(field, keyword)
