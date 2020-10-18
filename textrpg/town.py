from system import display_message
from item import Item
from menu import Menu

class Town:
    INN = "1"
    ITEM_SHOP = "2"
    WEAPON_SHOP = "3"
    LEAVE = "4"

    def __init__(self, player):
        self.player = player
        self.destination = None
        self.inn = Inn(self.player)
        self.item_shop = ItemShop(self.player)
        self.weapon_shop = WeaponShop(self.player)

    def explore(self):
        destinations = {
        self.INN: self.inn.main,
        self.ITEM_SHOP: self.item_shop.main,
        self.WEAPON_SHOP: self.weapon_shop.main
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
        print("2. アイテムショップ")
        print("3. 武器屋")
        print("4. 町を出る")
        self.get_destination()

    def get_destination(self):
        while (True):
            self.destination = input().strip()

            if self.destination not in ("1", "2", "3", "4"):
                print("Invalid input")
            else:
                break

class Shop:
    def enter_shop(self):
        display_message('～%s～' % (self.shop_name))
        display_message('%s:「%s」' % (self.keeper_name, self.greeting))

    def leave_shop(self):
        display_message('%s:「%s」' % (self.keeper_name, self.farewell))

    def get_yes_no_input(self):
        while (True):
            command = input().strip().lower()

            if command in ("y", "n"):
                return command
            else:
                print("Invalid input")
                
class Inn(Shop):
    def __init__(self, player):
        self.player = player
        self.shop_name = "宿屋"
        self.keeper_name = "ヤドルミ"
        self.greeting = "いらっしゃいませ。"
        self.farewell = "またのご来店をお待ちしております。"
        self.service_price = 25

    def main(self):
        self.enter_shop()
        self.inn_service()
        self.leave_shop()

    def inn_service(self):
        display_message('%s:「一泊%sゴールドになります。」' % (self.keeper_name, self.service_price))
        print('HP：%s/%s ゴールド: %s' %(self.player.stats['hp'], self.player.stats['max_hp'], self.player.stats["gold"]))
        print('一晩泊まりますか？(y/n)')

        if (self.get_yes_no_input() == "y"):
            if self.player.stats["gold"] >= self.service_price:
                self.inn_rest()
            else:
                display_message('ゴールドが足りない・・・')

    def inn_rest(self):
        display_message('%s:「ごゆっくりどうぞ。」' % (self.keeper_name))
        display_message('宿屋に一泊した')
        self.player.stats['hp'] = self.player.stats['max_hp']
        #hero.stats['mp'] = hero.stats['maxmp']
        #player.stats['day'] += 1
        self.player.stats["gold"] -= self.service_price
        display_message('HPが全回復した。')

class ItemShop(Shop):
    def __init__(self, player):
        self.player = player
        self.shop_name = "アイテムショップ"
        self.keeper_name = "ミセリーナ"
        self.greeting = "いらっしゃいませ!"
        self.browsing_line = "何をお買い上げになりますか?"
        self.farewell = "ありがとうございました！"
        self.inventory = ["small_potion", "small_potion", "small_potion"]
        self.purchase_index = None
        self.shop_visited = True
        self.item = Item()
        self.menu = Menu(self.inventory, "広場に戻る")

    def main(self):
        self.enter_shop()
        self.browse_shop()
        self.leave_shop()

    def browse_shop(self):
        display_message("%s　（ゴールド: %s)" % (self.browsing_line, self.player.stats["gold"]))
        while (True):
            self.purchase_index = self.menu.return_selected_option()
            if(self.purchase_index is not None):
                self.purchase_item()
            else:
                break

    def purchase_item(self):
        if (self.purchase_confirmed()):
            if (self.item.return_item_price(self.inventory[self.purchase_index]) > self.player.stats["gold"]):
                display_message('ゴールドが足りない・・・')
            else:
                self.make_purchase()

    def purchase_confirmed(self):
        self.item.display_item_info(self.inventory[self.purchase_index])
        self.item.display_item_price(self.inventory[self.purchase_index])
        print("このアイテムを買いますか？(y/n):")
        command = self.get_yes_no_input()

        if (command == "y"):
            return True

        return False

    def make_purchase(self):
        self.player.stats["gold"] -= self.item.return_item_price(self.inventory[self.purchase_index])
        self.player.items.append(self.inventory[self.purchase_index])
        self.inventory.pop(self.purchase_index)
        
class WeaponShop(ItemShop):
    def __init__(self, player):
        self.player = player
        self.shop_name = "武器屋"
        self.keeper_name = "ブキーロ"
        self.greeting = "へい、いらっしゃい!"
        self.browsing_line = "何を買うんだ？"
        self.farewell = "また来いよ！"
        self.inventory = ["claymore", "shield"]
        self.purchase_index = None
        self.shop_visited = True
        self.item = Item()
        self.menu = Menu(self.inventory, "広場に戻る")
