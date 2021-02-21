from bs4 import BeautifulSoup


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
        response = self.cache.get("https://api.warframe.market/v1/items/" + search_string + "/orders")
        if response.status_code != 200:
            return "N/A"
        item_data = response.json()
        # Filter listed orders
        order_prices = []
        for order in item_data["payload"]["orders"]:
            if order["region"] != "en" or order["platform"] != "pc" or order["user"]["status"] != "ingame":
                continue
            if order["order_type"] == "sell":
                order_prices.append(order["platinum"])
        # Sort filtered orders
        order_prices.sort()
        if len(order_prices) >= 4:
            return round(sum(order_prices[:4]) / 4, 1)
        elif len(order_prices) in range(1, 4):
            return round(sum(order_prices[:len(order_prices)]) / len(order_prices), 1)
        else:
            return "N/A"
