from datetime import datetime
import json
import os
import requests
import time


class Cache:
    def __init__(self):
        self.cache_file = "./Cache.db"
        self.requests_cache = {}
        self.session = requests.session()
        self.session.headers.update({
            "platform": "pc",
            "language": "en"
        })
        self.load()

    def get(self, url, key_ttl=(2 * 86400)):
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

    def load(self):
        if os.path.isfile(self.cache_file):
            try:
                with open(self.cache_file, mode="r", encoding="utf-8") as file:
                    loaded_cache = json.load(file)
                print(loaded_cache)
            except json.JSONDecodeError:
                file.close()

    def save(self):
        cache_dump = []
        for cached_request in self.requests_cache.keys():
            cache_dump.append({
                "json": str(self.requests_cache[cached_request].json()),
                "status_code": self.requests_cache[cached_request].status_code,
                "timestamp": str(self.requests_cache[cached_request].timestamp)
            })
        with open(self.cache_file, "w", encoding="utf-8") as file:
            json.dump(cache_dump, file)


class CachedResponse:
    def __init__(self, response):
        self.json = response.json
        self.status_code = response.status_code
        self.timestamp = datetime.now()
