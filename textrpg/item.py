from system import display_message

class Item:
    ITEM_INFO = {
    "small_potion": {
        "name": "小回復薬",
        "price": 20,
        "effect": "体力を20回復"
        }
    }

    def __init__(self, player, enemy = None):
        self.player = player
        self.enemy = enemy

    def use_item(self, item):
        items = {
        "small_potion": self.use_potion
        }

        items[item]()

    def display_item_info(self, item):
        print("アイテム: %s" % (self.ITEM_INFO[item]["name"]))
        print("効果: %s" % (self.ITEM_INFO[item]["effect"]))

    def use_potion(self):
        display_message("%sを使った。" % (self.ITEM_INFO["small_potion"]["name"]))
        self.heal_hp(20)
        self.player.turn_item_used = True

    def heal_hp(self, heal):
        if (self.player.stats["hp"] + heal > self.player.stats["max_hp"]):
            heal = self.player.stats["max_hp"] - self.player.stats["hp"]
        self.player.stats["hp"] += heal

        display_message("体力が%s回復しました。" % (heal))
