from system import display_message
from item_info import ITEM_INFO

class Item:
    def __init__(self, player = None, enemy = None):
        self.player = player
        self.enemy = enemy
        self.item_name = None

    def find_longest_equipment_name(self):
        longest_name_length = len("無し")
        for equipment in self.player.equipped_items.values():
            if equipment != "none" and len(ITEM_INFO[equipment]["name"]) > longest_name_length:
                longest_name_length = len(ITEM_INFO[equipment]["name"])
        return longest_name_length

    def return_item_name(self, item_name):
        return ITEM_INFO[item_name]["name"]

    def return_item_price(self, item_name):
        return ITEM_INFO[item_name]["price"]

    def initial_equip(self, item_name):
        self.item_name = item_name
        self.equip_item()

    def equip_status(self):
        #display_message("check status")
        #print(self.player.equipped_items.values())
        if self.item_name in self.player.equipped_items.values():
            return True
        return False

    def use_item(self, item_name):
        self.item_name = item_name

        if (ITEM_INFO[self.item_name]["type"] == "potion"):
            self.use_potion()
        elif (ITEM_INFO[self.item_name]["type"] == "equipment"):
            if (self.equip_status()):
                self.unequip_item()
                return
            self.unequip_overlapping_equipment()
            self.equip_item()
            display_message("%sを装備した。" % (ITEM_INFO[self.item_name]["name"]))

    def display_item_info(self, item):
        print("アイテム: %s" % (ITEM_INFO[item]["name"]))
        print("効果: %s" % (ITEM_INFO[item]["effect"]))

    def display_item_price(self, item):
        print("値段: %sゴールド" % (ITEM_INFO[item]["price"]))

    def use_potion(self):
        display_message("%sを使った。" % (ITEM_INFO[self.item_name]["name"]))
        self.change_stats()
        self.player.turn_item_used = True

    def change_stats(self):
        for stat, stat_change in ITEM_INFO[self.item_name]["stat_change"]:
            if (stat == "hp"):
                self.heal_hp()
            # Continue from here.

    def heal_hp(self):
        if (self.player.stats["hp"] + ITEM_INFO[self.item_name]["stat_change"]["hp"] > self.player.stats["max_hp"]):
            heal = self.player.stats["max_hp"] - self.player.stats["hp"]
        self.player.stats["hp"] += heal

        display_message("体力が%s回復しました。" % (heal))

    def equip_item_on_player(self):
        if ITEM_INFO[self.item_name]["equip_region"] == "both_hands":
            self.player.equipped_items["left_hand"] = self.item_name
            self.player.equipped_items["right_hand"] = self.item_name
        else:
            self.player.equipped_items[ITEM_INFO[self.item_name]["equip_region"]] = self.item_name

    def unequip_item_from_player(self):
        if ITEM_INFO[self.item_name]["equip_region"] == "both_hands":
            self.player.equipped_items["left_hand"] = "none"
            self.player.equipped_items["right_hand"] = "none"
        else:
            self.player.equipped_items[ITEM_INFO[self.item_name]["equip_region"]] = "none"

    def add_equipment_stats(self):
        for stat, stat_change in ITEM_INFO[self.item_name]["stat_change"].items():
            self.player.stats[stat] += stat_change

    def remove_equipment_stats(self):
        for stat, stat_change in ITEM_INFO[self.item_name]["stat_change"].items():
            self.player.stats[stat] -= stat_change

    def unequip_overlapping_equipment(self):
        if ITEM_INFO[self.item_name]["region"] == "both_hands":
            if (self.player.equipped_items["left_hand"] != "none") or (self.player.equipped_items["right_hand"] != "none"):
                for region in ("left_hand", "right_hand"):
                    if self.player.equipped_items[region] != "none":
                        self.unequip_item(self.player.equipped_items[region])
        elif self.player.equipped_items[ITEM_INFO[self.item_name]["region"]] != "none":
            self.unequip_item(self.player.equipped_items[ITEM_INFO[self.item_name]["region"]])

    def equip_item(self):
        self.equip_item_on_player()
        self.add_equipment_stats()

    def unequip_item(self):
        self.remove_equipment_stats()
        self.unequip_item_from_player()
        display_message("%sを外しました。" % (ITEM_INFO[self.item_name]["name"]))
