class LRUCache:
    def __init__(self, limit=42):
        self.limit = limit
        self.cache_dict = {}

    @property
    def limit(self):
        return self._limit

    @limit.setter
    def limit(self, value):
        if not isinstance(value, int):
            raise TypeError("Cache limit must be int")
        if value <= 0:
            raise ValueError("Cache limit must be greater then 0")
        self._limit = value

    def get(self, key):
        if self.cache_dict.get(key):
            self.cache_dict[key] = self.cache_dict.pop(key)
            return self.cache_dict[key]
        return None

    def set(self, key, value):
        if key in self.cache_dict:
            self.cache_dict.pop(key)
            self.cache_dict[key] = value
            return True
        if len(self.cache_dict) == self.limit and key not in self.cache_dict:
            key_to_delete = next(iter(self.cache_dict))
            self.cache_dict.pop(key_to_delete)
        self.cache_dict[key] = value
        return True
