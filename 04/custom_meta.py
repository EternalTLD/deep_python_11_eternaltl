import re


class CustomMeta(type):
    def __new__(mcs, name, bases, classdict, **kwargs):
        magic_method_pattern = r"__\w+__"
        for attr in classdict.copy():
            if not re.match(magic_method_pattern, attr):
                classdict[f"custom_{attr}"] = classdict.pop(attr)

        def __setattr__(obj, name, value):
            obj.__dict__[f"custom_{name}"] = value

        classdict["__setattr__"] = __setattr__

        return super().__new__(mcs, name, bases, classdict, **kwargs)
