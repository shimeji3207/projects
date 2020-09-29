from system import display_message
from random import randint

class Character:
    def attack(self, opponent):
        display_message("%sの攻撃!" % (self.stats["name"]))

        if opponent.stats["defence"]/2 > self.stats["attack"]:
            damage = 1
        else:
            damage = int((self.stats["attack"] - (opponent.stats["defence"]/2))/opponent.stats["max_hp"])

        if damage == 0:
            damage = 1

        opponent.stats["hp"] -= int(damage)

        display_message("%sに%sのダメージを与えた。" % (opponent.stats["name"], damage))

class Hero(Character):
    YES = 1
    NO = 0

    def __init__(self):
        self.stats = {
        "name": "",
        "level": 1,
        "exp": 0,
        "next_exp": 15,
        "max_hp": 20,
        "hp": 20,
        "attack": 5,
        "defence": 5,
        "speed": 3
        }
        self.ran = self.NO

    def display_stats(self):
        display_message("""Name: %s
Lvl: %s
EXP: %s
Next level EXP: %s
HP: %s/%s
ATK: %s
DEF: %s
SPD: %s""" % (self.stats["name"], self.stats["level"], self.stats["exp"], self.stats["next_exp"],
        self.stats["hp"], self.stats["max_hp"], self.stats["attack"], self.stats["defence"], self.stats["speed"]))

    def run(self, enemy):

        run_probability = int((2 - (self.stats["speed"]/enemy.stats["speed"])) * 100)

        if (run_probability < 10):
            run_probability = 10

        if (randint(0, 99) < run_probability):
            self.ran = self.YES

class Enemy(Character):
    LEVEL_RANGE = 3

    def __init__(self):
        self.stats = {
        "name": "",
        "level": 1,
        "max_hp": 10,
        "hp": 10,
        "attack": 3,
        "defence": 3,
        "speed": 2
        }

    def define_enemy(self, name):
        self.stats["name"] = name
        self.stats["max_hp"] = 10
        self.stats["hp"] = 10
        self.stats["attack"] = 3
        self.stats["defence"] = 3
        self.stats["speed"] = 2

    def set_level(self, player_level):
        if (player_level - self.LEVEL_RANGE < 1):
            self.stats["level"] = randint(1, player_level + self.LEVEL_RANGE)
        else:
            self.stats["level"] = randint( player_level - self.LEVEL_RANGE, player_level + self.LEVEL_RANGE)

    def set_goblin_stats(self):
        self.stats["level"]

"""
import random, copy
from message import display_message

msg = display_message

class characters:

    def display_stats(self):
        '''Displays the stats of the character'''
        for i in self.statdisplay:
            if i == 'name':
                print('名前: %s' % (self.stats[i]))
            elif i == 'gold':
                print('ゴールド:%s' % (self.gold))
            elif i == 'crit':
                print('クリティカル率:%s' % (self.stats['crit']) + '%')
            elif i == 'killed':
                print('敵を倒した数:%s' % (self.stats[killed]))
            elif i == 'mp':
                print('MP: %s/%s' % (self.stats[i],self.stats['maxmp']))
            elif i == 'day':
                print('%s日目' % (self.stats[i]))
            elif i == 'lvl':
                print('Lvl. %s' % (self.stats[i]))
            elif i == 'lvlupexp':
                print('レベルアップまでのEXP: %s' % (self.stats['lvlupexp'] - self.currentlvlexp))
            elif i == 'hp':
                print('HP: %s/%s' % (self.stats[i],self.stats['maxhp']))
            else:
                print('%s: %s' % (i.upper(), self.stats[i]))

    def set_stats(self, total_points):
        '''Sets the stats of the character.

        arguments:
        [total_points]: Amount of points to be distributetd across
        the player's stats. (int)

        variables:
        [stat_list]: Copy of the statchange list. (list)
        '''
        stat_list = copy.copy(self.statchange)
        random.shuffle(stat_list)

        for i in range(len(stat_list)):
            if i == len(self.statchange) - 1:
                self.stats[stat_list[i]] = total_points
            else:
                self.stats[stat_list[i]] = random.randint(1,total_points-((len(stat_list)-i)))
                total_points -= self.stats[stat_list[i]]

        self.stats['hp'] = self.stats['maxhp']
        self.stats['mp'] = self.stats['maxmp']

    def evade(self, opp):
        '''Evaluates whether the opponent evades the character's attack.

        arguments:
        [opp]: Object of the opponent (obj)

        variables:
        [ratio]: Ratio between the opponent's speed and the character's speed (int)
        [evade_prob]: The percentage probability that the opponent evades the
        character's attack. (int)
        [rng]: A random number between 1 and 100 to indicate whether the
        opponent evades the character's attack or not. (int)

        return:
        [True]: If the opponent evades the player's attack.
        [False]: If the opponent fails to evade the player's attack.
        '''
        ratio = opp.stats['spd']/self.stats['spd']
        evade_prob = round((ratio/4)*100)
        if evade_prob > 100:
            evade_prob = 99
        rng = random.randint(1,100)
        if rng <= evade_prob:
            msg('%sが攻撃を避けた。' % (opp.stats['name']))
            return True
        else:
            return False

    def critical_hit(self):
        '''Evaluates whether the player's attack is a critical hit or not

        returns:
        [1]: If the attack is not a critical hit
        [1.5]: If the attack is a critical hit. The attack becomes 1.5 times
        greater.
        '''
        rng = random.randint(1,100)
        if rng <= self.stats['crit']:
            print('クリティカルヒット！')
            return 1.5
        else:
            return 1

    def attack(self, opp):
        '''Attacks the opponent and applies the
        damage to the opponents hp if the attack hits.

        variables:
        [evade_success]: Indicates whether the opponent evades the
        character's attack. (bool)
            [True]: opponent evades the attack
            [False]: Character's attack hits

        arguments:
        [opp]: Object of the character's opponent. (obj)

        return:
        [dmg]: Damaged inflicted on the opponent.
        [None]: If the opponent evaded the attack.
        '''

        print(self.stats['name'] + "の攻撃!")
        evade_success = self.evade(opp)
        if evade_success is False:
            crit_dmg = self.critical_hit()
            atk_ratio = self.stats['atk']/opp.stats['def']
            dmg = round((opp.stats['maxhp']/4)*atk_ratio*crit_dmg)
            if dmg == 0:
                dmg = 1
            opp.stats['hp'] -= dmg
            return dmg
        else:
            return None"""