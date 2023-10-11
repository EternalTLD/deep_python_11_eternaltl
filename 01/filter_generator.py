from io import IOBase


def filter_generator(file_or_file_name: str | IOBase, search_words: list[str]) -> str:
    if not isinstance(search_words, list):
        raise TypeError("Variable 'search_words' must be list of str")

    if isinstance(file_or_file_name, str):
        with open(file_or_file_name, "r", encoding="utf-8") as file_object:
            yield from process_file_object(file_object, search_words)
    elif isinstance(file_or_file_name, IOBase):
        yield from process_file_object(file_or_file_name, search_words)
    else:
        raise TypeError("Variable 'file_or_file_name' must be string or file object")


def process_file_object(file_object, search_words):
    for line in file_object:
        current_line = ""
        line_words = line.lower().strip().split()
        for word in search_words:
            if line == current_line:
                continue
            if word.lower() in line_words:
                current_line = line
                yield line.strip()
