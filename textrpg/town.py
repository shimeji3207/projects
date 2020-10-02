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

"""
# Name of options in the town
shop_select = '雑貨屋に行く'
weaponry_select = '武器屋に行く'
inn_select = '宿屋に行く'
status_select = 'ステータスを見る'
inventory_select = '持ち物を見る'
nexttown_select = '次の町に行く'
boss_stage_select = '魔王城に行く'
magic_shop_select = '魔法道具屋に行く'
dojo_select = '道場に行く'

# Importing of the description of the items
import items as i
item_desc = i.item_desc
#list[0]: item description, list[1]: item effect, list[2]: item price

# Importing of the message display function
import message as m
msg = m.display_message

# Listing of the things to do in the town
town_options = [shop_select, magic_shop_select, inn_select, dojo_select, status_select, inventory_select, nexttown_select]

# Common functions
def buy(hero, keeper_info, item):
    '''Function for when the player selects an
    item to purchase

    arguments:
    [hero]: The player object. (obj)
    [keeper_name]: Name of the shop keeper. (str)
    [item]: Name of the item of purchase. (str)
    '''
    print('アイテム: %s' % (item))
    print('値段:%sゴールド' % (item_desc[item][2]))
    print('説明: %s' % (item_desc[item][0]))
    cmd = ''
    while cmd not in ('y','n'):
        print('このアイテムを買いますか？(y/n)')
        cmd = input()
    if cmd == 'y':
        if hero.gold >= item_desc[item][2]:
            hero.items.append(item)
            hero.items.sort()
            hero.gold -= item_desc[item][2]
            msg('%s:「%s」' % (keeper_info[0],keeper_info[2]))
            return True
        else:
            msg('お金が足りない・・・')
            return False
    return False

def browsing(hero, keeper_info, items):
    '''Displays the items for browsing

    arguments:
    [hero]: Object of the player character. (obj)
    [keeper_info]: Information on the shop keeper. (list)
    [items]: Items for sale. (list)
    '''
    options = tuple((range(1,len(items)+2)))
    while True:
        cmd = ''
        while cmd not in options:
            print('ゴールド:%s' %(hero.gold))
            display_options(items)
            print('%s.戻る' % (len(items)+1))
            try:
                cmd = int(input())
                assert cmd in options
            except:
                print("表示されている数字を入力してください")

        if cmd == len(items) + 1:
            msg('%s:「%s」' % (keeper_info[0],keeper_info[3]))
            break
        else:
            bought = buy(hero,keeper_info, items[cmd-1])
            if bought is True:
                del items[cmd-1]

def display_options(listing):
    '''Displays the options avaliable to the player.

    arguments:
    [listing]: List to display. (list)
    '''
    for i in range(len(listing)):
        print('%s.%s' % (i+1,listing[i]))

# Functions of the things to do
def shop(hero, shop_items):
    '''Player enters the store

    arguments:
    [hero]: Object of the player character (obj)
    [shop_items]: List of the items sold in the shop. (list)
    '''
    # Keeper info
    # list[0]: name, list[1]: Entering line, list[2]: Purchase line
    # list[3]: Leaving line
    keeper_info = ['ミセリーナ', 'いらっしゃいませ!',
    'お買い上げありがとうございます!', 'ありがとうございました！']
    # Title of the place
    print('～雑貨屋～')
    msg('%s:「%s」' % (keeper_info[0], keeper_info[1]))
    browsing(hero, keeper_info, shop_items)

# Define the inventory of the magic shop
mshop_items = ['魔導書（初級）','魔導書（中級）','魔導書（上級）']

def magic_shop(hero):
    '''Player enters the magic shops

    arguments:
    [hero]: Object of the character. (obj)
    '''
    # Keeper info
    # list[0]: name, list[1]: Entering line, list[2]: Purchase line
    # list[3]: Leaving line
    keeper_info = ['マジリーヌ', 'いらっしゃいませ。',
    'お買い上げありがとうございます。', 'またのお越しをお待ちしております。']
    # Title of the place
    print('～魔法道具屋～')
    msg('%s:「%s」' % (keeper_info[0], keeper_info[1]))
    browsing(hero, keeper_info, mshop_items)

def dojo(hero):
    '''Player enters the dojo

    arguments:
    [hero]: Object of the character. (obj)
    '''
    # Keeper info
    # list[0]: name, list[1]: Entering line, list[2]: Purchase line
    # list[3]: Leaving line
    keeper_info = ['トレン', 'おう、よく来たな。',
    'うん。このぐらいでいいだろ。', 'また来いよ。']
    # Price of training
    price = 10
    # Title of the place
    print('～道場～')
    msg('%s:「%s」' % (keeper_info[0], keeper_info[1]))
    cmd = ''
    msg('説明：ここでステータスをもう一度ランダムに割り振る事ができます。')
    msg('必要ゴールド:%s' % (price))
    while cmd not in ('y', 'n'):
        print('鍛えますか？　ゴールド:%s (y/n)' % (hero.gold))
        cmd = input()
    if cmd == 'y' and hero.gold >= price:
        while hero.gold >= price:
            hero.set_stats(50+len(hero.statchange)*5 + 2*len(hero.statchange)*(hero.stats['lvl']-1))
            hero.hero_stats()
            hero.gold -= price
            msg('%s:「%s」' % (keeper_info[0],keeper_info[2]))
            cmd = ''
            while cmd not in ('y', 'n'):
                print('鍛えますか？　ゴールド:%s (y/n)' % (hero.gold))
                cmd = input()
            if cmd == 'y' and hero.gold < price:
                msg('ゴールドが足りない・・・')
            if cmd == 'n':
                break
    elif hero.gold < price:
        msg('ゴールドが足りない・・・')

    msg('%s:「%s」' % (keeper_info[0],keeper_info[3]))

def inn(hero):
    '''Player enters the inn

    hero: Object of the player. (obj)
    '''
    # Keeper info
    # list[0]: name, list[1]: Entering line, list[2]: stay line
    # list[3]: Leaving line
    keeper_name = 'ヤドルミ'
    # Price to stay
    price = 25

    # Title of the place
    print('～宿屋～')
    msg('%s:「いらっしゃいませ。」' % (keeper_name))
    msg('%s:「一泊%sゴールドになります。」' % (keeper_name, price))
    cmd = ''
    while cmd not in ('y','n'):
        print('HP：%s/%s MP:%s/%s ゴールド:%s' %(hero.stats['hp'], hero.stats['maxhp'],
        hero.stats['mp'], hero.stats['maxmp'], hero.gold))
        print('一晩泊まりますか？(y/n)')
        cmd = input()
    if cmd == 'y':
        if hero.gold >= price:
            msg('%s:「ごゆっくりどうぞ。」' % (keeper_name))
            msg('宿屋に一泊した')
            hero.stats['hp'] = hero.stats['maxhp']
            hero.stats['mp'] = hero.stats['maxmp']
            hero.stats['day'] += 1
            hero.gold -= price
            msg('HPとMPが全回復した。')
        else:
            msg('ゴールドが足りない・・・')
    else:
        msg('%s:「またのご来店をお待ちしております。」' % (keeper_name))

def status(hero):
    '''Display status of the hero'''
    hero.hero_stats()

def inventory(hero):
    hero.inventory('持ち物')

def next_town(hero):
    msg('%s:「そろそろ出発するか。」' % (hero.stats['name']))
    msg('%s:「次の町まで%s日かかる。」' %(hero.stats['name'],(3 + round(hero.trips*0.5))))

def boss_stage(hero):
    msg('%s:「次でやっと魔王城だ。」' % (hero.stats['name']))
    msg('%s:「これが最後の旅になるだろう。」' % (hero.stats['name']))
    cmd = ''
    while cmd not in ('y','n'):
        print('%s：「他に準備する事はないか？」(y/n)' % (hero.stats['name']))
        cmd = input()
    if cmd == 'n':
        msg('%s:「うん、ないな。それじゃ出発だ。」' % (hero.stats['name']))
        msg('%s:「魔王城まで%s日はかかる。」' % (hero.stats['name'],(3 + round(hero.trips*0.5))))
        return True
    else:
        msg('まだあるな。一端戻ろう。')
        return False

# Mapping of the name of the option to their respective functions
town_map = {shop_select: shop, inn_select:inn, status_select:status, inventory_select:inventory,
nexttown_select:next_town, boss_stage_select:boss_stage, magic_shop_select:magic_shop,
dojo_select:dojo}

def town(hero):
    # Sets the shops inventory
    shop_items = ['回復薬','回復薬','回復薬', '回復薬（良）','回復薬（良）','回復薬（超）',
    '煙玉','煙玉','煙玉',]

    if hero.trips == hero.req_trips:
        for i in range(len(town_options)):
            if town_options[i] == nexttown_select:
                del town_options[i]
                break
        town_options.append(boss_stage_select)

    msg('町に着いた')
    while True:
        print('～広場～')
        msg('%s:「さて、これからどうした物か。」' % (hero.stats['name']))
        cmd = ''
        while cmd not in town_options:
            print('行動を選択してください')
            display_options(town_options)
            try:
                cmd = int(input())
                cmd = town_options[cmd-1]
            except:
                print("表示されている数字を入力してください")

        if cmd == nexttown_select:
            town_map[cmd](hero)
            break
        elif cmd == boss_stage_select:
            leave = town_map[cmd](hero)
            if leave is True:
                break
        elif cmd == shop_select:
            town_map[cmd](hero,shop_items)
        else:
            town_map[cmd](hero)"""