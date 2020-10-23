from system import display_message
from random import randint
from item import Item

class Character:
    def attack(self, opponent):
        display_message("%sの攻撃!" % (self.stats["name"]))

        if (self.evade(opponent.stats["speed"])):
            display_message("%sが攻撃をかわした。" % (opponent.stats["name"]))
            return

        damage = self.stats["attack"] - (opponent.stats["defence"]/2)

        if damage <= 0:
            damage = 1

        if (randint(0,99) < self.stats["critical"]):
            display_message("クリティカルヒット！")
            damage = self.return_critical_damage(damage)

        damage = int(damage)

        opponent.stats["hp"] -= damage
        display_message("%sに%sのダメージを与えた。" % (opponent.stats["name"], damage))

    def evade(self, opponent_speed):
        evade_probability = int(((opponent_speed/self.stats["speed"]) - 0.8) * 100)

        if (evade_probability < 10):
            evade_probability = 10

        if (evade_probability > 90):
            evade_probability = 90

        if (randint(0, 99) < evade_probability):
            return True

        return False

    def return_critical_damage(self, damage):
        return damage*1.5

class Hero(Character):
    REGION_NAMES = {
    "head": "頭",
    "chest": "胴体",
    "arms": "腕",
    "right_hand": "右手",
    "left_hand": "左手",
    "legs": "脚",
    "feet": "足"
    }

    def __init__(self):
        self.stats = {
        "name": "",
        "level": 1,
        "exp": 0,
        "next_exp": 15,
        "gold": 0,
        "max_hp": 20,
        "hp": 20,
        "max_mp": 10,
        "mp": 10,
        "critical": 10,
        "attack": 5,
        "defence": 5,
        "speed": 5
        }
        self.equipped_items = {
        "head": "none",
        "chest": "none",
        "arms": "none",
        "left_hand": "none",
        "right_hand": "none",
        "legs": "none",
        "feet": "none"
        }
        self.item_object = Item(self)
        self.equip_initial_items()
        self.items = ["leather_chestplate", "sword", "small_potion", "small_potion"]
        self.event_battle_run_away_line = "ごめんなさい！"
        self.event_run_away_line = "俺が助けなくても大丈夫だろう。多分・・・"
        self.turn_item_used = False
        self.ran = False

    def equip_initial_items(self):
        self.item_object.initial_equip("leather_chestplate")
        self.item_object.initial_equip("sword")

    def display_stats(self):
        print("～ステータス～")
        print("-%s-" % self.stats["name"])
        print(("Lvl: %s" % (self.stats["level"])).ljust(12) + ("Exp: %s" % (self.stats["exp"])))
        print(("Next lvl EXP: %s" % (self.stats["next_exp"])))
        print(("HP:%s/%s" % (self.stats["hp"], self.stats["max_hp"])).ljust(12) + ("ゴールド: %s" % (self.stats["gold"])))
        print(("ATK: %s" % (self.stats["attack"])).ljust(12) + ("DEF: %s" % (self.stats["defence"])))
        display_message(("SPD: %s" % (self.stats["speed"])))
        self.display_equipped_items()

    def display_equipped_items(self):
        print("～装備～")
        counter = 1
        longest_name_length = self.item_object.find_longest_equipment_name()

        for region, equipment in self.equipped_items.items():
            if equipment == "none":
                equipment_name = "無し"
            else:
                equipment_name = self.item_object.return_item_name(equipment)

            if (counter == 7):
                display_message("%s: %s" % (self.REGION_NAMES[region].ljust(2), equipment_name.ljust(longest_name_length)))
            elif (counter % 2 == 0):
                print("%s: %s" % (self.REGION_NAMES[region].ljust(2), equipment_name.ljust(longest_name_length)))
            else:
                print("%s: %s" % (self.REGION_NAMES[region].ljust(2), equipment_name.ljust(longest_name_length)), end = "")
            counter += 1

    def run(self, enemy):
        run_probability = int(((self.stats["speed"]/enemy.stats["speed"]) - 0.5) * 100)

        if (run_probability < 10):
            run_probability = 10

        if (randint(0, 99) < run_probability):
            self.ran = True
        else:
            display_message("逃げられなかった。")

    def gain_exp(self, gained_exp):
        display_message("%sの経験値を獲得しました。" % (gained_exp))
        self.stats["exp"] += gained_exp
        if (self.stats["exp"] >= self.stats["next_exp"]):
            self.level_up()

    def gain_gold(self, dropped_gold):
        display_message("%sゴールドを拾った。" % dropped_gold)
        self.stats["gold"] += dropped_gold

    def level_up(self):
        levels_increased = 0

        while (self.stats["exp"] >= self.stats["next_exp"]):
            self.stats["exp"] -= self.stats["next_exp"]
            self.stats["next_exp"] = int(self.stats["next_exp"] * 1.2)
            self.stats["level"] += 1
            levels_increased += 1
        display_message("レベル%sになりました！" % (self.stats["level"]))

        self.increase_stats(levels_increased)
        self.display_stats()

    def increase_stats(self, levels_increased):
        hp_increase = int(self.stats["max_hp"] * 0.2) * levels_increased

        self.stats["max_hp"] += hp_increase
        self.stats["hp"] += hp_increase
        self.stats["attack"] += 2 * levels_increased
        self.stats["defence"] += 1 * levels_increased
        self.stats["speed"] += 1 * levels_increased

class Enemy(Character):
    LEVEL_RANGE = 3

    def __init__(self):
        self.stats = {
        "name": "",
        "level": 1,
        "max_hp": 0,
        "hp": 0,
        "critical": 0,
        "attack": 0,
        "defence": 0,
        "speed": 0
        }
        self.obtainable_exp = 0
        self.dropped_gold = 0

    def define_enemy(self, name, player_level):
        enemy_stats = {
        "goblin": self.set_goblin_stats,
        "slime": self.set_slime_stats,
        "bandit": self.set_bandit_stats,
        "skeleton": self.set_skeleton_stats,
        "werewolf": self.set_werewolf_stats,
        "large_spider": self.set_large_spider_stats,
        "last_boss": self.set_last_boss_stats
        }

        self.set_level(player_level)
        enemy_stats[name]()

    def set_level(self, player_level):
        if (player_level - self.LEVEL_RANGE < 1):
            self.stats["level"] = randint(1, player_level + self.LEVEL_RANGE)
        else:
            self.stats["level"] = randint( player_level - self.LEVEL_RANGE, player_level + self.LEVEL_RANGE)

    def set_slime_stats(self):
        self.stats["name"] = "スライム"
        self.stats["max_hp"] = 5 + (self.stats["level"] - 1)
        self.stats["hp"] = self.stats["max_hp"]
        self.stats["attack"] = 1 + (self.stats["level"] - 1)
        self.stats["defence"] = 1 + (self.stats["level"] - 1)
        self.stats["speed"] = 1 + (self.stats["level"] - 1)
        self.stats["critical"] = 2

        self.obtainable_exp = 3 + self.stats["level"]
        self.dropped_gold = randint(1,3)

    def set_goblin_stats(self):
        self.stats["name"] = "ゴブリン"
        self.stats["max_hp"] = 5 + (self.stats["level"] + 1)
        self.stats["hp"] = self.stats["max_hp"]
        self.stats["attack"] = 2 + (self.stats["level"])
        self.stats["defence"] = 1 + (self.stats["level"])
        self.stats["speed"] = 2 + (self.stats["level"])
        self.stats["critical"] = 4

        self.obtainable_exp = 3 + (2 * self.stats["level"])
        self.dropped_gold = randint(1,5)

    def set_bandit_stats(self):
        self.stats["name"] = "盗賊"
        self.stats["max_hp"] = 8 + (self.stats["level"] + 1)
        self.stats["hp"] = self.stats["max_hp"]
        self.stats["attack"] = 2 + (self.stats["level"])
        self.stats["defence"] = 2 + (self.stats["level"])
        self.stats["speed"] = 1 + (self.stats["level"])
        self.stats["critical"] = 5

        self.obtainable_exp = 5 + (2 * self.stats["level"])
        self.dropped_gold = randint(5,15)

    def set_skeleton_stats(self):
        self.stats["name"] = "スケルトン"
        self.stats["max_hp"] = 15 + (self.stats["level"] + 1)
        self.stats["hp"] = self.stats["max_hp"]
        self.stats["attack"] = 4 + (self.stats["level"])
        self.stats["defence"] = 4 + (self.stats["level"])
        self.stats["speed"] = 3 + (self.stats["level"])
        self.stats["critical"] = 5

        self.obtainable_exp = 8 + (2 * self.stats["level"])
        self.dropped_gold = randint(5, 15)

    def set_werewolf_stats(self):
        self.stats["name"] = "狼男"
        self.stats["max_hp"] = 20 + (self.stats["level"] + 1)
        self.stats["hp"] = self.stats["max_hp"]
        self.stats["attack"] = 6 + (self.stats["level"])
        self.stats["defence"] = 4 + (self.stats["level"])
        self.stats["speed"] = 6 + (self.stats["level"])
        self.stats["critical"] = 10

        self.obtainable_exp = 12 + (2 * self.stats["level"])
        self.dropped_gold = randint(5, 15)

    def set_large_spider_stats(self):
        self.stats["name"] = "でかい蜘蛛"
        self.stats["max_hp"] = 15 + (self.stats["level"] + 1)
        self.stats["hp"] = self.stats["max_hp"]
        self.stats["attack"] = 5 + (self.stats["level"])
        self.stats["defence"] = 3 + (self.stats["level"])
        self.stats["speed"] = 5 + (self.stats["level"])
        self.stats["critical"] = 5

        self.obtainable_exp = 10 + (2 * self.stats["level"])
        self.dropped_gold = randint(5, 15)

    def set_last_boss_stats(self):
        self.stats["name"] = "魔王"
        self.stats["max_hp"] = 30 + (self.stats["level"] + 1)
        self.stats["hp"] = self.stats["max_hp"]
        self.stats["attack"] = 7 + (2 * self.stats["level"])
        self.stats["defence"] = 7 + (self.stats["level"])
        self.stats["speed"] = 7 + (self.stats["level"])
        self.stats["critical"] = 10

        self.obtainable_exp = 20 + (2 * self.stats["level"])
        self.dropped_gold = randint(15, 30)
