import json


def parse_json(json_str: str, keyword_callback, required_fields=None, keywords=None):
    json_doc = json.loads(json_str)
    for field in required_fields:
        if field in json_doc.keys():
            value_str = json_doc[field]
            value_list = value_str.split()
            for value in value_list:
                if value.lower() in map(lambda keyword: keyword.lower(), keywords):
                    keyword_callback(value)
