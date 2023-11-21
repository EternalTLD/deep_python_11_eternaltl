import argparse
import logging


class LogFilter(logging.Filter):
    def filter(self, record):
        return len(record.getMessage().split()) % 2 != 0


class LRUCache:
    def __init__(self, limit=42):
        self.logger = logging.getLogger("lru_logger")

        if not isinstance(limit, int):
            self.logger.error("Cache limit must be int")
            if not limit.isdigit():
                self.logger.critical("Cache limit must be digit")

        self.limit = limit
        self.cache_dict = {}

    def get(self, key):
        self.logger.debug("Call get method for key: %s", key)
        if key in self.cache_dict:
            self.cache_dict[key] = self.cache_dict.pop(key)
            self.logger.info("Get existing key: %s", key)
            return self.cache_dict[key]
        self.logger.warning("Get not existing key: %s", key)
        return None

    def set(self, key, value):
        self.logger.debug("Call set method for key: %s", key)
        if key in self.cache_dict:
            self.cache_dict.pop(key)
            self.logger.warning("Reset value of existing key: %s", key)
        elif len(self.cache_dict) == self.limit:
            key_to_delete = next(iter(self.cache_dict))
            self.cache_dict.pop(key_to_delete)
            self.logger.warning(
                "Cache has reached max limit. Key: %s has been reset to key: %s",
                key_to_delete,
                key,
            )
        else:
            self.logger.info("Set not existing key: %s", key)
        self.cache_dict[key] = value


def config_logger(parser_args):
    file_formatter = logging.Formatter(
        "[FILE LOG] %(asctime)s\t%(levelname)s\t%(name)s\t%(message)s"
    )
    file_handler = logging.FileHandler("09/cache.log", mode="w")
    file_handler.setFormatter(file_formatter)

    logger = logging.getLogger("lru_logger")
    logger.propagate = False
    logger.setLevel(logging.DEBUG)
    logger.addHandler(file_handler)

    if parser_args.s:
        stream_formatter = logging.Formatter(
            "[STDOUT LOG] %(asctime)s\t%(levelname)s\t%(name)s\t%(message)s"
        )
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(stream_formatter)
        logger.addHandler(stream_handler)
    if parser_args.f:
        logger.addFilter(LogFilter())


def test(parser_args):
    config_logger(parser_args)

    cache = LRUCache(2)

    cache.set("val1", 1)
    cache.set("val2", 2)

    cache.get("val1")
    cache.get("val3")

    cache.set("val3", 3)
    cache.set("val1", "new_val1")

    LRUCache("2")
    LRUCache("two")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="LRU-cache logger")
    parser.add_argument("-s", help="Stdout logger", action="store_true")
    parser.add_argument("-f", help="Custom filter", action="store_true")
    args = parser.parse_args()
    test(args)
