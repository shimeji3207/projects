from character import Enemy
from battle import Battle
from system import display_message

class LastCastle:
    def __init__(self, player):
        self.player = player
        self.enemy = Enemy()
        self.enemy.define_enemy("last_boss", self.player.stats["level"])
        self.battle = Battle(self.player, self.enemy)

    def boss_lines(self):
        display_message('魔王:「良くぞここまでたどり着いた、勇者よ。誉めてやろう。」')
        display_message('%s:「だろ？そして、俺はお前を倒す！」' % (self.player.stats['name']))
        display_message('魔王:「ほう。面白い。出来るものならやってみせよ！」')

    def encounter(self):
        display_message("%sが現れた！" % (self.enemy.stats["name"]))
        self.battle.start_battle()

    def travel(self):
        display_message("～魔王城～")

        self.boss_lines()

        self.encounter()



