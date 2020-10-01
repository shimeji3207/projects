from system import display_message
from random import randint

class Character:
    def attack(self, opponent):
        display_message("%sの攻撃!" % (self.stats["name"]))

        damage = int(self.stats["attack"] - (opponent.stats["defence"]/2))

        if damage <= 0:
            damage = 1

        opponent.stats["hp"] -= int(damage)

        display_message("%sに%sのダメージを与えた。" % (opponent.stats["name"], damage))

class Hero(Character):
    def __init__(self):
        self.stats = {
        "name": "",
        "level": 1,
        "exp": 0,
        "next_exp": 15,
        "gold": 0,
        "max_hp": 20,
        "hp": 20,
        "attack": 5,
        "defence": 5,
        "speed": 5
        }
        self.ran = False

    def display_stats(self):
        print("-%s-" % self.stats["name"])
        print(("Lvl: %s" % (self.stats["level"])).ljust(12) + ("Exp: %s" % (self.stats["exp"])))
        print(("Next lvl EXP: %s" % (self.stats["next_exp"])))
        print(("HP:%s/%s" % (self.stats["hp"], self.stats["max_hp"])).ljust(12) + ("ゴールド: %s" % (self.stats["gold"])))
        print(("ATK: %s" % (self.stats["attack"])).ljust(12) + ("DEF: %s" % (self.stats["defence"])))
        display_message(("SPD: %s" % (self.stats["speed"])))

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
        "bandit": self.set_bandit_stats
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

        self.obtainable_exp = 3 + self.stats["level"]
        self.dropped_gold = randint(1,3)

    def set_goblin_stats(self):
        self.stats["name"] = "ゴブリン"
        self.stats["max_hp"] = 5 + (self.stats["level"] + 1)
        self.stats["hp"] = self.stats["max_hp"]
        self.stats["attack"] = 2 + (self.stats["level"])
        self.stats["defence"] = 1 + (self.stats["level"])
        self.stats["speed"] = 2 + (self.stats["level"])

        self.obtainable_exp = 3 + (2 * self.stats["level"])
        self.dropped_gold = randint(1,5)

    def set_bandit_stats(self):
        self.stats["name"] = "盗賊"
        self.stats["max_hp"] = 8 + (self.stats["level"] + 1)
        self.stats["hp"] = self.stats["max_hp"]
        self.stats["attack"] = 2 + (self.stats["level"])
        self.stats["defence"] = 2 + (self.stats["level"])
        self.stats["speed"] = 1 + (self.stats["level"])

        self.obtainable_exp = 5 + (2 * self.stats["level"])
        self.dropped_gold = randint(5,15)

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
