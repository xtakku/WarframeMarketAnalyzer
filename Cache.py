from datetime import datetime
import requests
import time


class Cache:
    def __init__(self):
        self.requests_cache = {}
        self.session = requests.session()
        self.session.headers.update({
            "platform": "pc",
            "language": "en"
        })

    def get(self, url, key_ttl=86400):
        if url.startswith("https://api.warframe.market"):
            key_name = url.split("/")[-2]
        else:
            key_name = url.split("/")[-1]

        is_cached = False
        if key_name in self.requests_cache.keys():
            is_cached = True
        if is_cached and (self.requests_cache[key_name].timestamp - datetime.now()).total_seconds() > key_ttl:
            is_cached = False
        
        if is_cached:
            return self.requests_cache[key_name]
        else:
            response = CachedResponse(self.session.get(url))
            time.sleep(1/3)
            if response.status_code == 200:
                self.requests_cache[key_name] = response
            return response


class CachedResponse:
    def __init__(self, response):
        self.json = response.json
        self.status_code = response.status_code
        self.timestamp = datetime.now()
