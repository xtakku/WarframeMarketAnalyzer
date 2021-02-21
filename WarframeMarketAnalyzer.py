from Cache import Cache
from Relic import Relic


class WarframeMarketAnalyzer:
    def __init__(self):
        self.cache = Cache()

    def print_relic_comparison(self, relics):
        drops, sorted_drops = {}, {}
        for relic_name in relics:
            relic = Relic(self.cache, relic_name)
            for drop in relic.drops:
                if drop.name in drops.keys():
                    continue
                drops[drop.name] = drop.platinum
        for v in sorted(drops.values(), reverse=True):
            for k in drops.keys():
                if drops[k] == v:
                    sorted_drops[k] = drops[k]
                    break
        for drop in sorted_drops.keys():
            print(drop + ": " + str(sorted_drops[drop]))
        self.cache.save()

    def print_single_relic(self, relic_name):
        relic = Relic(self.cache, relic_name)
        if relic.vaulted == "Baro":
            is_vaulted = " (Baro Ki'Teer exclusive)"
        else:
            is_vaulted = " (Vaulted: Yes)" if relic.vaulted else " (Vaulted: No)"
        print(relic.name + is_vaulted)
        total = 0
        for drop in relic.drops:
            print(drop.name + ": " + str(drop.platinum) + " (" + str(drop.chance) + "%)")
            try:
                total += drop.platinum * drop.chance
            except TypeError:
                total = -1
                break
        if total == -1:
            print("Average Drop Value: N/A")
        else:
            print("Average Drop Value: " + str(round(total / 100, 1)))
        print("Relic Market Value: " + str(relic.platinum))
        self.cache.save()
