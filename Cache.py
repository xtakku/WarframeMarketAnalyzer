from datetime import datetime
import requests


class Cache:
    def __init__(self):
        self.requests_cache = {}

    def get(self, url):
        key_name = url.split("/")[-1]
        key_ttl = 3600
        if "market" not in url:
            key_ttl = 86400

        is_cached = False
        if key_name in self.requests_cache.keys():
            is_cached = True
        if is_cached and (self.requests_cache[key_name].timestamp - datetime.now()).total_seconds() > key_ttl:
            is_cached = False
        
        if is_cached:
            return self.requests_cache[key_name].response
        else:
            response = CachedResponse(requests.get(url))
            if response.response.status_code == 200:
                self.requests_cache[key_name] = response
            return response.response


class CachedResponse(requests.Response):
    def __init__(self, response):
        super().__init__()
        self.response = response
        self.timestamp = datetime.now()
