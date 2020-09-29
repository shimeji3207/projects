from system import display_message
from random import randint
from character import Enemy
from battle import Battle

class Forest:
    ENEMIES = ["goblin", "slime", "bandit"]

    def __init__(self, player):
        self.times_visited = 0
        self.days_passed = 0
        self.encounter_rate = 10
        self.enemy = Enemy()
        self.player = player
        self.battle = Battle(player, self.enemy)

    def travel(self):
        while(self.days_passed < 3 + self.times_visited):
            display_message("～%s日目～" % (self.days_passed + 1))

            self.event()

            if self.player.stats["hp"] <= 0:
                return

            self.days_passed += 1
            # Heal by resting for the night
            self.player.stats["hp"] += 2

        display_message("街についた。")
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
        self.enemy.define_enemy(self.ENEMIES[randint(0,len(self.ENEMIES) - 1)])