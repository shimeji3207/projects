import random, sys
from system import display_message

class Battle:
    ATTACK = 1
    DISPLAY_STATS = 2
    RUN = 3

    def __init__(self, player, enemy):
        self.player_battle_command = None
        self.player = player
        self.enemy = enemy

    def obtain_battle_command(self):
        while (True):
            command = input().strip()

            if command in ("1", "2", "3"):
                return int(command)
            else:
                print("Invalid command")

    def battle_menu(self):
        print("1. 攻撃\n2. ステータス\n3. 逃げる")
        self.player_battle_command = self.obtain_battle_command()

    def start_battle(self):
        player_commands = {
        self.ATTACK: self.player.attack,
        self.DISPLAY_STATS: self.player.display_stats,
        self.RUN: self.player.run
        }

        while(self.player.stats["hp"] > 0 and self.enemy.stats["hp"] > 0):

            self.battle_menu()

            if (self.player_battle_command == self.DISPLAY_STATS):
               player_commands[self.player_battle_command]()
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

    def player_defeated(self):
        display_message("力が尽きた。")

    def player_ran(self):
        display_message("戦闘から逃げた。")

"""
msg = display_message

def gain_exp(hero, monster):
    '''Player gains exp according to the level of the monster
    that was defeated.

    arguments:
    [hero]: Object of the hero gaining exp. (obj)
    [monster]: Object of the monster which the hero defeated. (obj)
    '''
    gained_exp = round(6 + monster.stats['lvl']**1.5)
    hero.stats['exp'] += gained_exp
    hero.currentlvlexp += gained_exp
    msg('%sのEXPを得た。' % (gained_exp))

def money_drop(hero,monster):
    gold_drop = 3 + 3*(monster.stats['lvl']-1)
    hero.gold += gold_drop
    print('%sゴールドを手に入れた。' % (gold_drop), end ='')
    input()

def battle(hero, monster):
    '''Conducts the battle between the hero and the monster

    arguments:
    [her]: Hero object
    [monster]: Monster object
    '''

    # Indicate that the player is in battle
    hero.inbattle = True

    # Outputs that a monster has appeared
    print("%sがあらわれた！" % (monster.stats['name']), end = '')
    input()

    # Initiate battle
    while hero.stats['hp'] > 0 and monster.stats['hp'] > 0:
        # Player's turn
        effect = hero.move(monster) # 0: Nothing, 1: Ran

        if effect == 1:
            break

        if monster.stats['hp'] < 1:
            break

        # Monster's turn
        monster.monster_atk(hero)

    if monster.stats['hp'] < 1 and effect != 1:
        print("戦闘に勝った！")
        gain_exp(hero,monster)
        hero.level_up()
        hero.stats['killed'] += 1
        money_drop(hero,monster)
        hero.inbattle = False
    elif hero.stats['hp'] < 1:
        msg("ゲームオーバー")
        sys.exit()
"""
