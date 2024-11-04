from openpyxl import Workbook
from openpyxl.styles import Font
import requests
import json


# Send request, get response
def get_cards():
    response = requests.get("https://api.splinterlands.io/cards/get_details")
    cards = response.json()
    return cards


def get_data():
    cards = get_cards()
    cards_data = []
    for card in cards:
        if card["game_type"] != "splinterlands":
            break
        name = card["name"]
        expansion = card["editions"]
        typ = card["type"]
        color = card["color"]
        second_color = card["secondary_color"]
        if second_color is not None:
            color = f"{color}/{second_color}"
        stats = card["stats"]
        if typ == "Monster":
            levels_num = len(stats["mana"])
            #ability_list = []
            for level in range(levels_num):
                mana = stats["mana"][level]
                lvl = level + 1
                melee = stats["attack"][level]
                ranged = stats["ranged"][level]
                magic = stats["magic"][level]
                armor = stats["armor"][level]
                health = stats["health"][level]
                speed = stats["speed"][level]
                ability = ", ".join(stats["abilities"][level])
                #if len(abilities) != 0:
                #    ability_list.append(abilities)
                cards_data.append([name, expansion, typ, color, mana, lvl, melee, ranged, magic, armor, health, speed, ability])


        else:
            lvl = 1
            mana = stats["mana"]
            attack = stats["attack"]
            ranged = stats["ranged"]
            magic = stats["magic"]
            armor = stats["armor"]
            health = stats["health"]
            speed = stats["speed"]
            ability = ", ".join(stats.get("abilities", []))
            cards_data.append([name, expansion, typ, color, mana, lvl, melee, ranged, magic, armor, health, speed, ability])

        cards_data.append([])

    return cards_data



def main():
    wb = Workbook()
    ws = wb.active
    cards_list = [["Name", "Expansion", "Type", "Color", "Mana", "Level", "Melee", "Ranged", "Magic", "Armor", "Health", "Speed", "Abilities"]]

    cards_data = get_data()

    for card_data in cards_data:
        cards_list.append(card_data)

    for row in cards_list:
        ws.append(row)

    # mate title bold
    ft = Font(bold=True)
    for row in ws["A1:N1"]:
        for cell in row:
            cell.font = ft

    wb.save("Cards_data.xlsx")


if __name__ == "__main__":
    main()
