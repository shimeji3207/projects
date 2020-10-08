from random import randint
from system import display_message
from character import Enemy
from battle import Battle

class TravelArea:
    def __init__(self, area_name, player):
        self.area_name = area_name
        self.times_visited = 0
        self.days_passed = 0
        self.days_till_destination = 3
        self.encounter_rate = 0
        self.enemies = []
        self.enemy = Enemy()
        self.player = player
        self.battle = Battle(player, self.enemy)

    def travel(self):
        self.days_passed = 0
        display_message("～%s～" % (self.area_name))

        while(self.days_passed < 3 + self.times_visited):
            display_message("<%s日目>" % (self.days_passed + 1))

            self.event()

            if self.player.stats["hp"] <= 0:
                return

            if (self.days_passed < self.days_till_destination - 1):
                self.rest_heal()

            self.days_passed += 1

        display_message("町についた。")
        self.times_visited += 1

    def event(self):
        if(randint(0,9) < self.encounter_rate):
            self.encounter()
        else:
            display_message("平和な一日でした。")

    def encounter(self):
        self.choose_enemy()
        display_message("%sが現れた！" % (self.enemy.stats["name"]))
        self.battle.start_battle()

    def choose_enemy(self):
        self.enemy.define_enemy(self.enemies[randint(0,len(self.enemies) - 1)], self.player.stats["level"])

    def rest_heal(self):
        heal =  int(self.player.stats["max_hp"]*0.1)
        if (self.player.stats["hp"] + heal > self.player.stats["max_hp"]):
            heal = self.player.stats["max_hp"] - self.player.stats["hp"]
            self.player.stats["hp"] += heal

        display_message("夜休んで体力が%s回復しました。" % (heal))

class Forest(TravelArea):
    def __init__(self, player):
        self.area_name = "森"
        self.times_visited = 0
        self.days_passed = 0
        self.days_till_destination = 3
        self.encounter_rate = 7
        self.enemies = ["goblin", "slime", "bandit"]
        self.enemy = Enemy()
        self.player = player
        self.battle = Battle(player, self.enemy)

class HauntedForest(TravelArea):
    def __init__(self, player):
        self.area_name = "呪われた森"
        self.times_visited = 0
        self.days_passed = 0
        self.days_till_destination = 3
        self.encounter_rate = 10
        self.enemies = ["skeleton", "werewolves", "large_spider"]
        self.enemy = Enemy()
        self.player = player
        self.battle = Battle(player, self.enemy)

