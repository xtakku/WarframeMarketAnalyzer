class Drop:
    def __init__(self, c, name):
        self.name = name.strip()
        self.cache = c
        self.chance = 0
        # Replace "P." with "Prime"
        if "P." in self.name:
            self.name = self.name.split(" ")
            self.name.remove("P.")
            temp = self.name[0] + " Prime " + self.name[1]
            for i in range(2, len(self.name)):
                temp += " " + self.name[i]
            self.name = temp
        # Replace "BP" with "Blueprint"
        if "BP" in self.name:
            self.name = self.name.split(" ")
            self.name.pop()
            self.name = " ".join(self.name)
            if len(self.name.split(" ")) == 2:
                self.name += " Blueprint"
        # Get Price
        self.platinum = self.get_price()

    def get_price(self):
        search_string = "_".join(self.name.lower().split(" "))
        if self.name.split(" ")[-1][-1] in [str(x) for x in range(10)]:
            search_string += "_intact"
        response = self.cache.get("https://api.warframe.market/v1/items/" + search_string + "/statistics")
        if response.status_code != 200:
            return "N/A"
        item_data = response.json_data["payload"]["statistics_closed"]
        if len(item_data["48hours"]) > 0:
            return item_data["48hours"][0]["wa_price"]
        elif len(item_data["48hours"]) == 0 and len(item_data["90days"]) > 0:
            return item_data["90days"][0]["wa_price"]
        else:
            return "N/A"