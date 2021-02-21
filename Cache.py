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
            with open(self.cache_file, "r", encoding="utf-8") as file:
                for line in file:
                    temp = line.split(";")
                    response = TempResponse()
                    response.timestamp = datetime.strptime(temp[1], "%Y-%m-%d %H:%M:%S.%f")
                    response.status_code = int(temp[2])
                    response.json_data = json.loads(temp[3])
                    self.requests_cache[temp[0]] = response

    def save(self):
        with open(self.cache_file, "w", encoding="utf-8") as file:
            for key in self.requests_cache.keys():
                file.write(key + ";")
                file.write(str(self.requests_cache[key].timestamp) + ";")
                file.write(str(self.requests_cache[key].status_code) + ";")
                file.write(str(json.dumps(self.requests_cache[key].json_data, indent=4, sort_keys=True)) + "\n")


class CachedResponse:
    def __init__(self, response):
        self.json_data = response.json()
        self.status_code = response.status_code
        self.timestamp = datetime.now()


class TempResponse:
    def __init(self):
        self.json_data = {}
        self.status_code = 0
        self.timestamp = 0
