import random, sys
from system import display_message

class Battle:
    ATTACK = 1
    DISPLAY_STATS = 2
    ITEM_MENU = 3
    RUN = 4

    def __init__(self, player, enemy):
        self.player_battle_command = None
        self.player = player
        self.enemy = enemy

    def obtain_battle_command(self):
        while (True):
            command = input().strip()

            if command in ("1", "2", "3", "4"):
                return int(command)
            else:
                print("Invalid command")

    def battle_menu(self):
        print("行動を選択してください。")
        print("1. 攻撃\n2. ステータス\n3. アイテム\n4. 逃げる")
        self.player_battle_command = self.obtain_battle_command()

    def start_battle(self):
        player_commands = {
        self.ATTACK: self.player.attack,
        self.DISPLAY_STATS: self.player.display_stats,
        self.ITEM_MENU: self.player.item_menu,
        self.RUN: self.player.run
        }

        while(self.player.stats["hp"] > 0 and self.enemy.stats["hp"] > 0):

            self.battle_menu()

            if (self.player_battle_command == self.DISPLAY_STATS):
                player_commands[self.player_battle_command]()
                continue
            elif (self.player_battle_command == self.ITEM_MENU):
                player_commands[self.player_battle_command]()

                if (self.player.turn_item_used):
                    self.enemy.attack(self.player)
                    self.player.turn_item_used = False

                continue

            # Determines who attacks first depending on speed
            if (self.player.stats["speed"] > self.enemy.stats["speed"] or self.player_battle_command == self.RUN):
                player_commands[self.player_battle_command](self.enemy)
                #print("Enemy hp: %s" % (self.enemy.stats["hp"]))

                if (self.battle_ended()):
                    return

                self.enemy.attack(self.player)
                #print("Player hp: %s" % (self.player.stats["hp"]))
            else:
                self.enemy.attack(self.player)

                if (self.battle_ended()):
                    return

                player_commands[self.player_battle_command](self.enemy)

            if (self.battle_ended()):
                return

    def battle_ended(self):
        self.player.turn_item_used = False

        if(self.enemy.stats["hp"] <= 0):
            self.player_victory()
            return True

        if(self.player.stats["hp"] <= 0):
            self.player_defeated()
            return True

        if(self.player.ran):
            self.player_ran()
            self.player.ran = False
            return True

        return False

    def player_victory(self):
        display_message("%sを倒した!" % (self.enemy.stats["name"]))
        self.player.gain_exp(self.enemy.obtainable_exp)
        self.player.gain_gold(self.enemy.dropped_gold)

    def player_defeated(self):
        display_message("力が尽きた。")

    def player_ran(self):
        display_message("戦闘から逃げた。")
