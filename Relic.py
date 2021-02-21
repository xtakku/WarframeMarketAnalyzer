from Drop import Drop


class Relic(Drop):
    def __init__(self, c, name):
        super().__init__(c, name)
        self.vaulted = False
        self.drops = []
        for k, v in self.get_drops().items():
            if k == "Forma BP":
                continue
            temp = Drop(c, k)
            temp.chance = v
            self.drops.append(temp)

    def get_drops(self):
        # Modify search string
        suffixes = ["Exceptional", "Flawless", "Radiant"]
        temp = self.name.split(" ")
        if temp[-1] in suffixes:
            search_string = " ".join([temp[0], temp[1], "Relic"]) + " (" + temp[2] + ")"
        elif temp[-1] == "Intact":
            search_string = " ".join([temp[0], temp[1], "Relic"])
        else:
            search_string = self.name + " Relic"
        response = self.cache.get("https://api.warframestat.us/drops/search/" + search_string.lower())
        if response.status_code != 200:
            return "N/A"
        drops = response.json()
        # Check if relic is vaulted
        intact_search_string = " ".join([temp[0], temp[1], "Relic"])
        intact_response = self.cache.get("https://api.warframestat.us/drops/search/" + intact_search_string.lower())
        intact_drops = intact_response.json()
        if len(intact_drops) == 24:
            self.vaulted = True
        if intact_search_string[0:6] in ["Neo O1", "Axi A2", "Axi A5", "Axi V8"]:
            self.vaulted = "Baro"
        # Aggregate possible drops
        loot_table = {}
        for drop in drops:
            if drop["place"] == search_string:
                loot_table[drop["item"]] = drop["chance"]
        return loot_table
