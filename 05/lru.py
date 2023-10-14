class LRUCache:
    def __init__(self, limit=42):
        self.limit = limit
        self.cache = dict()
        
    def get(self, key):
        if not self.cache.get(key):
            raise ValueError(f"There is no {key}")
        self.cache[key] = self.cache.pop(key)
        return self.cache[key]

    def set(self, key, value):
        if len(self.cache) == self.limit:
            lru_key = list(self.cache.keys())[0]
            self.cache.pop(lru_key)
            self.cache[key] = value
            return True
        self.cache[key] = value
        return True
