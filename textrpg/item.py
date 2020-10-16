from system import display_message

class Item:
    ITEM_INFO = {
    "small_potion": {
        "name": "小回復薬",
        "price": 20,
        "effect": "体力を20回復",
        "type": "potion",
        "stat_change": {
            "hp": 20
            }
        },
    "leather_chestplate": {
        "name": "革のチェストプレート",
        "price": 20,
        "effect": "DEF+1",
        "type": "equipment",
        "equip_region": "chest",
        "stat_change": {
            "defence": 1
            }
        },
    "sword": {
        "name": "普通の剣",
        "price": 20,
        "effect": "ATK+1",
        "type": "equipment",
        "equip_region": "right_hand",
        "stat_change": {
            "attack": 1
            }
        }
    }

    def __init__(self, player = None, enemy = None):
        self.player = player
        self.enemy = enemy
        self.item_name = None

    def return_item_price(self, item_name):
        return self.ITEM_INFO[item_name]["price"]
        
    def initial_equip(self, item_name):
        self.item_name = item_name
        self.equip_item()

    def use_item(self, item_name):
        self.item_name = item_name

        if (self.ITEM_INFO[self.item_name]["type"] == "potion"):
            self.use_potion()
        elif (self.ITEM_INFO[self.item_name]["type"] == "equipment"):
            self.equip_item()
            display_message("%sを装備した。" % (self.ITEM_INFO[self.item_name]["name"]))

    def display_item_info(self, item):
        print("アイテム: %s" % (self.ITEM_INFO[item]["name"]))
        print("効果: %s" % (self.ITEM_INFO[item]["effect"]))

    def display_item_price(self, item):
        print("値段: %sゴールド" % (self.ITEM_INFO[item]["price"]))

    def use_potion(self):
        display_message("%sを使った。" % (self.ITEM_INFO[self.item_name]["name"]))
        self.change_stats()
        self.player.turn_item_used = True

    def change_stats(self):
        for stat, stat_change in self.ITEM_INFO[self.item_name]["stat_change"]:
            if (stat == "hp"):
                self.heal_hp()
            # Continue from here.

    def heal_hp(self):
        if (self.player.stats["hp"] + self.ITEM_INFO[self.item_name]["stat_change"]["hp"] > self.player.stats["max_hp"]):
            heal = self.player.stats["max_hp"] - self.player.stats["hp"]
        self.player.stats["hp"] += heal

        display_message("体力が%s回復しました。" % (heal))

    def equip_item_on_player(self):
        self.player.equipped_items[self.ITEM_INFO[self.item_name]["equip_region"]] = self.item_name

    def add_equipment_stats(self):
        for stat, stat_change in self.ITEM_INFO[self.item_name]["stat_change"].items():
            self.player.stats[stat] += stat_change

    def equip_item(self):
        self.equip_item_on_player()

        self.add_equipment_stats()

    def unequip_item(self):
        pass
