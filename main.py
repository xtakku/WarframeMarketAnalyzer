from WarframeMarketAnalyzer import *


if __name__ == "__main__":
    app = WarframeMarketAnalyzer()

    # Compare a squad's relics
    prefix = "Lith"
    ids = "B7, T4, P4, P5"
    relic_list = []
    for i in ids.replace(",", "").split(" "):
        relic_list.append(prefix + " " + i)
    app.print_relic_comparison(relic_list)

    # Show details about a relic
    app.print_single_relic("Lith B7")
