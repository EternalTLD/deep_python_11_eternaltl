from io import IOBase


def filter_generator(file_or_file_name: str | IOBase, search_words: list[str]) -> str:
    if not isinstance(search_words, list):
        raise TypeError("Variable 'search_words' must be list of str")

    if isinstance(file_or_file_name, str):
        with open(file_or_file_name, "r", encoding="utf-8") as file_object:
            for line in file_object:
                line_words = line.lower().strip().split()
                for word in search_words:
                    if str(word.lower()) in line_words:
                        yield line.strip()
    elif isinstance(file_or_file_name, IOBase):
        for line in file_or_file_name:
            line_words = line.lower().strip().split()
            for word in search_words:
                if str(word.lower()) in line_words:
                    yield line.strip()
    else:
        raise TypeError("Variable 'file_or_file_name' must be string or file object")
