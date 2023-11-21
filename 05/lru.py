class LRUCache:
    def __init__(self, limit=42):
        if not isinstance(limit, int):
            raise TypeError("Cache limit must be int")
        if limit <= 0:
            raise ValueError("Cache limit must be greater then 0")
        self.limit = limit
        self.cache_dict = {}

    def get(self, key):
        if key in self.cache_dict:
            self.cache_dict[key] = self.cache_dict.pop(key)
            return self.cache_dict[key]
        return None

    def set(self, key, value):
        if key in self.cache_dict:
            self.cache_dict.pop(key)
        elif len(self.cache_dict) == self.limit:
            key_to_delete = next(iter(self.cache_dict))
            self.cache_dict.pop(key_to_delete)
        self.cache_dict[key] = value
