from openpyxl import Workbook
from openpyxl.styles import Font
import requests
import json
import sys


# Send request, get response
def get_cards():
    response = requests.get("https://api.splinterlands.io/cards/get_details")
    cards = response.json()
    return cards


# Get expansion's name from its corresponding num
def get_expansion(num):
    match num:
        case "0,1":
            return "Alpha/Beta"

        case "1":
            return "Beta"

        case "2":
            return "Promo"

        case "3":
            return "Reward"

        case "4":
            return "Untamed"

        case "5":
            return "Dice"

        case "6":
            return "Gladius"

        case "7":
            return "Chaos Legion"

        case "8":
            return "Riftwatchers"

        case "9":
            return ""

        case "10":
            return "Soulbound Reward Chaos Legion"

        case "11":
            return ""

        case "12":
            return "Rebellion"

        case "13":
            return "Soulbound Reward Chaos Rebellion"

        case _:
            return ""


# Get and collect data of all Splinterlands cards
def get_data():
    cards = get_cards()
    cards_data = []
    for card in cards:
        if card["game_type"] != "splinterlands":
            break  # No assets from other games
        name = card["name"]
        expansion_num = card["editions"]
        expansion_name = get_expansion(expansion_num)
        typ = card["type"]
        color = card["color"]
        second_color = card["secondary_color"]
        if second_color is not None:  # For multicolor cards
            color = f"{color}/{second_color}"
        stats = card["stats"]
        if typ == "Monster":
            levels_num = len(stats["mana"])
            abilities_list = []
            for level in range(levels_num):
                mana = stats["mana"][level]
                lvl = level + 1
                melee = stats["attack"][level]
                ranged = stats["ranged"][level]
                magic = stats["magic"][level]
                armor = stats["armor"][level]
                health = stats["health"][level]
                speed = stats["speed"][level]

                # Show at each level all available abilities
                ability = ", ".join(stats["abilities"][level])
                if ability != "":
                    abilities_list.append(ability)
                abilities = ", ".join(abilities_list)

                cards_data.append(
                    [
                        name,
                        expansion_name,
                        typ,
                        color,
                        mana,
                        lvl,
                        melee,
                        ranged,
                        magic,
                        armor,
                        health,
                        speed,
                        abilities,
                    ]
                )

        else:
            lvl = "all"
            mana = stats["mana"]
            melee = stats["attack"]
            ranged = stats["ranged"]
            magic = stats["magic"]
            armor = stats["armor"]
            health = stats["health"]
            speed = stats["speed"]
            abilities = ", ".join(stats.get("abilities", []))
            choose_abilities = stats.get("ptrOptions", [])
            if choose_abilities:
                choose_1_ability = choose_abilities[0]["name"]
                choose_1_target = choose_abilities[0]["max"]
                choose_2_ability = choose_abilities[1]["name"]
                choose_2_target = choose_abilities[1]["max"]
                choose_abilities_formatted = f"Choose {choose_1_ability} x{choose_1_target} or {choose_2_ability} x{choose_2_target}"
                if abilities:
                    abilities = f"{abilities} + {choose_abilities_formatted}"
                else:
                    abilities = choose_abilities_formatted
            cards_data.append(
                [
                    name,
                    expansion_name,
                    typ,
                    color,
                    mana,
                    lvl,
                    melee,
                    ranged,
                    magic,
                    armor,
                    health,
                    speed,
                    abilities,
                ]
            )

        cards_data.append([])

    return cards_data


# Create excel file with all the collected data
def main():
    wb = Workbook()
    ws = wb.active
    cards_list = [
        [
            "Name",
            "Expansion",
            "Type",
            "Color",
            "Mana",
            "Level",
            "Melee",
            "Ranged",
            "Magic",
            "Armor",
            "Health",
            "Speed",
            "Abilities",
        ]
    ]

    cards_data = get_data()

    for card_data in cards_data:
        cards_list.append(card_data)

    for row in cards_list:
        ws.append(row)

    # make title bold
    ft = Font(bold=True)
    for row in ws["A1:N1"]:
        for cell in row:
            cell.font = ft

    wb.save("Cards_data.xlsx")


if __name__ == "__main__":
    main()
