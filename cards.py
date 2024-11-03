import requests
import json
from tabulate import tabulate


# Send request, get response
def get_cards():
    response = requests.get("https://api.splinterlands.io/cards/get_details")
    cards = response.json()
    return cards


def main():
    cards = get_cards()
    for card in cards:
        if card["game_type"] != "splinterlands":
            break
        stats_list = []
        name = card["name"]
        type = card["type"]
        color = card["color"]
        second_color = card["secondary_color"]
        if second_color is not None:
            color = f"{color}/{second_color}"
        stats = card["stats"]
        if type == "Monster":
            levels_num = len(stats["mana"])
            ability_list = []
            for level in range(levels_num):
                mana = stats["mana"][level]
                attack = stats["attack"][level]
                ranged = stats["ranged"][level]
                magic = stats["magic"][level]
                armor = stats["armor"][level]
                health = stats["health"][level]
                speed = stats["speed"][level]
                abilities = stats["abilities"][level]
                if len(abilities) != 0:
                    ability_list.append(abilities)
                stats_list.append(
                    [attack, ranged, magic, armor, health, speed, list(ability_list)]
                )
            with open("table.md", "a", encoding="utf-8") as f:
                title = f"{name} - {type} - {mana} mana - {color}"
                headers = [
                    "Melee",
                    "Ranged",
                    "Magic",
                    "Armor",
                    "Health",
                    "Speed",
                    "Abilities",
                ]

                markdown_table = tabulate(stats_list, headers, tablefmt="github")
                f.write(title + "\n" + markdown_table + "\n\n")

        else:
            mana = stats["mana"]
            attack = stats["attack"]
            ranged = stats["ranged"]
            magic = stats["magic"]
            armor = stats["armor"]
            health = stats["health"]
            speed = stats["speed"]
            abilities = stats.get("abilities", [])
            stats_list.append(
                [attack, ranged, magic, armor, health, speed, ability_list]
            )
            with open("table.md", "a", encoding="utf-8") as f:
                title = f"{name} - {type} - {mana} mana - {color}"
                headers = [
                    "Melee",
                    "Ranged",
                    "Magic",
                    "Armor",
                    "Health",
                    "Speed",
                    "Abilities",
                ]

                markdown_table = tabulate(stats_list, headers, tablefmt="github")
                f.write(title + "\n" + markdown_table + "\n\n")


if __name__ == "__main__":
    main()
