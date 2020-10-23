from random import randint
from system import display_message, get_yes_no_input
from character import Enemy
from battle import Battle
from item_info import ITEM_INFO

class TravelArea:
    AMBUSH_DROP_RATE = 5

    def __init__(self, area_name, player):
        self.area_name = area_name
        self.times_visited = 0
        self.days_passed = 0
        self.days_till_destination = 3
        self.encounter_rate = 0
        self.happening_rate = 0
        self.happenings = []
        self.ambush_rate = 0
        self.enemies = []
        self.enemy = Enemy()
        self.player = player
        self.battle = Battle(player, self.enemy)

    def travel(self):
        self.days_passed = 0
        display_message("～%s～" % (self.area_name))

        while(self.days_passed < self.days_till_destination):
            display_message("<%s日目>" % (self.days_passed + 1))

            self.day_event()

            if self.player.stats["hp"] <= 0:
                return

            if (self.days_passed < self.days_till_destination - 1):
                self.night_event()

            self.days_passed += 1

        display_message("町についた。")
        self.times_visited += 1

    def night_event(self):
        display_message("-夜-")

        if (self.ambush()):
            self.ambush_battle()
        else:
            self.rest_heal()

    def ambush(self):
        if randint(0,10) <= self.ambush_rate:
            return True
        return False

    def ambush_battle(self):
        monster_type = self.enemies[randint(0, len(self.enemies) - 1)]
        self.enemy.define_enemy(monster_type, self.player.stats["level"])

        display_message("寝ている間に%sが襲い掛かってきた!" % (self.enemy.stats["name"]))
        self.battle.start_battle()

        if self.player.ran:
            self.ambush_ran_event()

    def ambush_ran_event(self):
        if randint(0,10) <= self.AMBUSH_DROP_RATE:
            self.drop_random_item_from_player()

    def drop_random_item_from_player(self):
        inventory_item_index = [index for index in range(len(self.player.items))
        if self.player.items[index] not in self.player.equipped_items.values()]

        if len(inventory_item_index) == 0:
            return

        dropped_item_index = inventory_item_index[randint(0,len(inventory_item_index) - 1)]

        display_message("逃げている途中に%sを落としてしまった!" % (ITEM_INFO[self.player.items[dropped_item_index]]["name"]))
        self.player.items.pop(dropped_item_index)

    def day_event(self):
        if (randint(0,9) < self.happening_rate):
            self.happening()
        elif(randint(0,9) < self.encounter_rate):
            self.encounter()
        else:
            display_message("平和な一日でした。")

    def event_attack_message(self, character_name, transport_name, monster_type):
        if transport_name is None:
            if monster_type == "bandit":
                display_message("%sが%sの集団に襲われている。" % (character_name, self.enemy.stats["name"]))
            else:
                display_message("%sが%sの群れに襲われている。" % (character_name, self.enemy.stats["name"]))
        else:
            if monster_type == "bandit":
                display_message("%sが%sの集団に襲われている。" % (transport_name, self.enemy.stats["name"]))
            else:
                display_message("%sが%sの群れに襲われている。" % (transport_name, self.enemy.stats["name"]))

    def event_question(self, character_name, transport_name):
        if transport_name is None:
            print("%sを助けますか？　**連戦になります** (y/n)" % (character_name))
        else:
            print("助けに行きますか？　**連戦になります** (y/n)")

    def attack_event(self, character_name, thank_you_lines, gained_gold, transport_name = None):
        monster_type = self.enemies[randint(0, len(self.enemies) - 1)]
        self.enemy.define_enemy(monster_type, self.player.stats["level"])

        self.event_attack_message(character_name, transport_name, monster_type)

        self.event_question(character_name, transport_name)

        if (get_yes_no_input() == "y"):
            self.consecutive_battles(monster_type)
            if (self.player.ran):
                self.event_battle_run_away()
            else:
                self.event_battle_victory(character_name, thank_you_lines, gained_gold)
        else:
            self.event_run_away()

    def event_run_away(self):
        display_message("%s:「%s」" % (self.player.stats["name"], self.player.event_run_away_line))
        display_message("そっとその場が去った。")

    def event_battle_run_away(self):
        display_message("%s:「%s」" % (self.player.stats["name"], self.player.event_battle_run_away_line))
        display_message("俺は振り返らずにその場から逃げ出した。")

    def event_battle_victory(self, character_name, thank_you_lines, gained_gold):
        for line in thank_you_lines:
            display_message(line)
        self.player.stats["gold"] += gained_gold
        display_message("%sから%sゴールドを貰った。" % (character_name, gained_gold))

    def happening(self):
        self.choose_happening()

    def consecutive_battles(self, monster_type):
        number_of_battles = randint(3,5)

        for battle_number in range(1, number_of_battles + 1):
            self.choose_enemy(monster_type)
            display_message("%sが現れた！" % (self.enemy.stats["name"]))
            self.battle.start_battle()
            if (self.player.ran):
                break
            if (number_of_battles - battle_number == 0):
                display_message("敵を全員倒した！")
            else:
                display_message("=敵は後%s体=" % (number_of_battles - battle_number))

    def encounter(self):
        self.randomly_choose_enemy()
        display_message("%sが現れた！" % (self.enemy.stats["name"]))
        self.battle.start_battle()

    def choose_enemy(self, monster_type):
        self.enemy.define_enemy(monster_type, self.player.stats["level"])

    def randomly_choose_enemy(self):
        self.enemy.define_enemy(self.enemies[randint(0,len(self.enemies) - 1)], self.player.stats["level"])

    def rest_heal(self):
        heal =  self.player.stats["max_hp"]*0.1
        if (self.player.stats["hp"] + heal > self.player.stats["max_hp"]):
            heal = self.player.stats["max_hp"] - self.player.stats["hp"]
            self.player.stats["hp"] += int(heal)

        display_message("夜休んで体力が%s回復しました。" % (heal))

class Forest(TravelArea):
    CARAVAN_ATTACK_PERCENTAGE = 8
    NOBLES_ATTACK_PERCENTAGE = 2

    def __init__(self, player):
        self.area_name = "森"
        self.times_visited = 0
        self.days_passed = 0
        self.days_till_destination = 3
        self.encounter_rate = 7
        self.happening_rate = 3
        self.ambush_rate = 3
        self.enemies = ["goblin", "slime", "bandit"]
        self.enemy = Enemy()
        self.player = player
        self.battle = Battle(player, self.enemy)

    def choose_happening(self):
        if randint(0, 10) <= self.CARAVAN_ATTACK_PERCENTAGE:
            self.caravan_attack()
        else:
            self.nobles_attack()

    def caravan_attack(self):
        thank_you_lines = ["商人:「助けてくれてありがとうございます！」"]

        self.attack_event("商人", thank_you_lines, randint(10,25))

    def nobles_attack(self):
        thank_you_lines = ["貴族:「助けてくれた事を感謝します。」"]

        self.attack_event("貴族", thank_you_lines, randint(100,200), "馬車")

class HauntedForest(TravelArea):
    def __init__(self, player):
        self.area_name = "呪われた森"
        self.times_visited = 0
        self.days_passed = 0
        self.days_till_destination = 3
        self.encounter_rate = 9
        self.ambush_rate = 7
        self.enemies = ["skeleton", "werewolf", "large_spider"]
        self.enemy = Enemy()
        self.player = player
        self.battle = Battle(player, self.enemy)
