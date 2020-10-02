from system import display_message

class Town:
    INN = "1"
    LEAVE = "2"

    def __init__(self, player):
        self.player = player
        self.destination = None
        self.shop = Shop(self.player)

    def explore(self):
        destinations = {
        self.INN: self.shop.inn
        }

        while(True):
            display_message('～広場～')
            display_message('%s:「さて、これからどうした物か。」' % (self.player.stats['name']))

            self.town_menu()
            if (self.destination == self.LEAVE):
                print("町を去った")
                break
            destinations[self.destination]()

    def town_menu(self):
        print('行動を選択してください:')
        print("1. 宿屋")
        print("2. 町を出る")
        self.get_destination()

    def get_destination(self):
        while (True):
            self.destination = input().strip()

            if self.destination not in ("1", "2"):
                print("Invalid input")
            else:
                break

class Shop:
    def __init__(self, player):
        self.player = player
        self.keeper_name = ""
        self.shop_name = ""
        self.greeting = ""
        self.farewell = ""
        self.service_price = 0

    def inn(self):
        self.define_inn()

        self.enter_shop()
        self.inn_service()
        self.leave_shop()

    def enter_shop(self):
        display_message('～%s～' % (self.shop_name))
        display_message('%s:「%s」' % (self.keeper_name, self.greeting))

    def leave_shop(self):
        display_message('%s:「%s」' % (self.keeper_name, self.farewell))

    def define_inn(self):
        self.shop_name = "宿屋"
        self.keeper_name = "ヤドルミ"
        self.greeting = "いらっしゃいませ。"
        self.farewell = "またのご来店をお待ちしております。"
        self.service_price = 25

    def inn_service(self):
        display_message('%s:「一泊%sゴールドになります。」' % (self.keeper_name, self.service_price))
        print('HP：%s/%s ゴールド: %s' %(self.player.stats['hp'], self.player.stats['max_hp'], self.player.stats["gold"]))
        print('一晩泊まりますか？(y/n)')

        if (self.get_yes_no_input() == "y"):
            if self.player.stats["gold"] >= self.service_price:
                self.inn_rest()
            else:
                display_message('ゴールドが足りない・・・')

    def get_yes_no_input(self):
        while (True):
            command = input().strip().lower()

            if command in ("y", "n"):
                return command
            else:
                print("Invalid input")

    def inn_rest(self):
        display_message('%s:「ごゆっくりどうぞ。」' % (self.keeper_name))
        display_message('宿屋に一泊した')
        self.player.stats['hp'] = self.player.stats['max_hp']
        #hero.stats['mp'] = hero.stats['maxmp']
        #player.stats['day'] += 1
        self.player.stats["gold"] -= self.service_price
        display_message('HPが全回復した。')
