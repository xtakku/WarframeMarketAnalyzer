from datetime import datetime
import requests


class Cache:
    def __init__(self):
        self.requests_cache = {}

    def get(self, url):
        if url.startswith("https://api.warframe.market"):
            key_ttl = 3600
            key_name = url.split("/")[-2]
        else:
            key_ttl = 86400
            key_name = url.split("/")[-1]

        is_cached = False
        if key_name in self.requests_cache.keys():
            is_cached = True
        if is_cached and (self.requests_cache[key_name].timestamp - datetime.now()).total_seconds() > key_ttl:
            is_cached = False
        
        if is_cached:
            return self.requests_cache[key_name]
        else:
            response = CachedResponse(requests.get(url))
            if response.status_code == 200:
                self.requests_cache[key_name] = response
            return response


class CachedResponse:
    def __init__(self, response):
        self.json = response.json
        self.status_code = response.status_code
        self.timestamp = datetime.now()
