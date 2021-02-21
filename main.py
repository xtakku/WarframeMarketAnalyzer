from WarframeMarketAnalyzer import *


if __name__ == "__main__":
    app = WarframeMarketAnalyzer()

    relic_list = []
    prefix = "Lith"
    ids = "B7, T4, P4, P5"
    for i in ids.replace(",", "").split(" "):
        relic_list.append(prefix + " " + i)

    # app.print_relic_comparison(relic_list)
    app.print_single_relic("Lith B7")
