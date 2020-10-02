from character import Hero
from system import display_message
from forest import Forest
from town import Town

class TextRPG:
    def __init__(self):
        self.main_character = Hero()
        self.forest = Forest(self.main_character)
        self.town = Town(self.main_character)

    def display_title(self):
        display_message("""「勇者の冒険」
Enterでゲームスタート""")

    def prompt_heros_name(self):
        while(self.main_character.stats["name"] == ""):
            self.main_character.stats["name"] = input("勇者の名前を入力してください: ").strip()

    def display_intro(self):
        display_message("～大王国の城～")
        display_message("王様：「選ばれし勇者%sよ。この世界に平和をもたらす為に魔王を倒すのだ！」" % (self.main_character.stats["name"]))
        display_message("%s：「お、おう。」" % (self.main_character.stats["name"]))
        display_message("王様：「さあ、行け！」")
        display_message("そして%sは魔王討伐に向けて次の町へ旅立つのであった。" % (self.main_character.stats["name"]))
        display_message("%s：「次の町にたどり着くまで三日はかかる。それまでに死ななければいいが・・・」" % (self.main_character.stats["name"]))

    def main(self):
        self.display_title()
        self.prompt_heros_name()
        self.display_intro()
        self.forest.travel()
        if self.main_character.stats["hp"] <= 0:
            self.game_over()
        self.town.explore()

    def game_over(self):
        display_message("ゲームオーバー")

text_rpg = TextRPG()
text_rpg.main()
