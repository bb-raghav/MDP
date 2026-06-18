from time import time


class TTLCache:
    def __init__(self, ttl_seconds=600):
        self.ttl_seconds = ttl_seconds
        self._values = {}

    def get(self, key):
        item = self._values.get(key)
        if not item:
            return None

        expires_at, value = item
        if expires_at <= time():
            self._values.pop(key, None)
            return None

        return value

    def set(self, key, value):
        self._values[key] = (time() + self.ttl_seconds, value)
        return value
