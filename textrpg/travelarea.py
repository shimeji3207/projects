from random import randint
from system import display_message, get_yes_no_input
from character import Enemy
from battle import Battle

class TravelArea:
    def __init__(self, area_name, player):
        self.area_name = area_name
        self.times_visited = 0
        self.days_passed = 0
        self.days_till_destination = 3
        self.encounter_rate = 0
        self.happening_rate = 0
        self.happenings = []
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
        if (randint(0,9) < self.happening_rate):
            self.happening()
        elif(randint(0,9) < self.encounter_rate):
            self.encounter()
        else:
            display_message("平和な一日でした。")

    def happening(self):
        self.happenings[randint(0, len(self.happenings) - 1)]()

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
        self.happening_rate = 3
        self.happenings = [self.caravan_attack]
        self.enemies = ["goblin", "slime", "bandit"]
        self.enemy = Enemy()
        self.player = player
        self.battle = Battle(player, self.enemy)

    def caravan_attack(self):
        monster_type = self.enemies[randint(0, len(self.enemies) - 1)]
        self.enemy.define_enemy(monster_type, self.player.stats["level"])

        if monster_type == "bandit":
            display_message("商人が%sの集団に襲われている。" % (self.enemy.stats["name"]))
        else:
            display_message("商人が%sの群れに襲われている。" % (self.enemy.stats["name"]))

        print("商人を助けますか？　**連戦になります** (y/n)")

        if (get_yes_no_input() == "y"):
            self.consecutive_battles(monster_type)
            if (self.player.ran):
                display_message("%s:「%s」" % (self.player.stats["name"], self.player.event_battle_run_away_line))
                display_message("俺は振り返らずにその場から逃げ出した。")
            else:
                display_message("商人:「助けてくれてありがとうございます！」")
                display_message("商人:「ほんの気持ちですが、どうかお受け取りください。」")
                gained_gold = randint(10, 25)
                self.player.stats["gold"] += gained_gold
                display_message("商人から%sゴールドを貰った。" % (gained_gold))
        else:
            display_message("%s:「%s」" % (self.player.stats["name"], self.player.event_run_away_line))
            display_message("そっとその場が去った。")

class HauntedForest(TravelArea):
    def __init__(self, player):
        self.area_name = "呪われた森"
        self.times_visited = 0
        self.days_passed = 0
        self.days_till_destination = 3
        self.encounter_rate = 10
        self.enemies = ["skeleton", "werewolf", "large_spider"]
        self.enemy = Enemy()
        self.player = player
        self.battle = Battle(player, self.enemy)
