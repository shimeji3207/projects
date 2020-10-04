from system import display_message

class Item:
    ITEM_INFO = {
    "small_potion": {
        "name": "小回復薬",
        "price": 20,
        "effect": "体力を20回復"
        }
    }

    def __init__(self, player, enemy = None):
        self.player = player
        self.enemy = enemy

    def use_item(self, item):
        items = {
        "small_potion": self.use_potion
        }

        items[item]()

    def display_item_info(self, item):
        print("アイテム: %s" % (self.ITEM_INFO[item]["name"]))
        print("効果: %s" % (self.ITEM_INFO[item]["effect"]))

    def use_potion(self):
        display_message("%sを使った。" % (self.ITEM_INFO["small_potion"]["name"]))
        self.heal_hp(20)
        self.player.turn_item_used = True

    def heal_hp(self, heal):
        if (self.player.stats["hp"] + heal > self.player.stats["max_hp"]):
            heal = self.player.stats["max_hp"] - self.player.stats["hp"]
        self.player.stats["hp"] += heal

        display_message("体力が%s回復しました。" % (heal))

"""
msg = display_message

# Healing item name and description
# list[0]: description, list[1]:effect, list[2]:price
# Potion
potion = '回復薬'
potion_des = '体力を20回復'
potion_effect = 20
potion_price = 20
potion_deslist = [potion_des, potion_effect,potion_price]
# High potion
high_potion = '回復薬（良）'
high_potion_des = '体力を40回復'
high_potion_effect = 40
high_potion_price = 40
high_potion_deslist = [high_potion_des, high_potion_effect, high_potion_price]
# Ultimate high potion
uhigh_potion = '回復薬（超）'
uhigh_potion_des = '体力を100回復'
uhigh_potion_effect = 100
uhigh_potion_price = 80
uhigh_potion_deslist = [uhigh_potion_des, uhigh_potion_effect, uhigh_potion_price]
# MP potion
mppotion = 'エネルギー草'
mppotion_des = 'MPを20回復'
mppotion_effect = 20
mppotion_price = 20
mppotion_list = [mppotion_des, mppotion_effect, mppotion_price]
# Tuple of healing items
healing_items = (potion,high_potion,uhigh_potion)

# Escape items
# Smoke bomb
smoke_name = '煙玉'
smoke_des = '戦闘から逃げられる。'
smoke_price = 10
smoke_effect = ''
smoke_list = [smoke_des, smoke_effect, smoke_price]
# Tuple of escape items
escape_items = (smoke_name,)

# Skill items and descriptions
# Magic book 1
magicbook1 = '魔導書（初級）'
magicbook1_des = '初級の魔導書。技「ファイアボール」を習得できる。'
magicbook1_price = 50
magicbook1_effect = 'ファイアボール'
magicbook1_list = [magicbook1_des, magicbook1_effect, magicbook1_price]
# Magic book 2
magicbook2 = '魔導書（中級）'
magicbook2_des = '中級の魔導書。技「サンダーボルト」を習得できる。'
magicbook2_price = 100
magicbook2_effect = 'サンダーボルト'
magicbook2_list = [magicbook2_des, magicbook2_effect, magicbook2_price]
# Magic book 3
magicbook3 = '魔導書（上級）'
magicbook3_des = '上級の魔導書。技「ハリケーン」を習得できる。'
magicbook3_effect = 'ハリケーン'
magicbook3_price = 200
magicbook3_list = [magicbook3_des, magicbook3_effect, magicbook3_price]
# Tuple of skill items
skill_items = (magicbook1, magicbook2, magicbook3)

# Mapping of the item names with the description and effect
item_desc = {potion: potion_deslist, high_potion: high_potion_deslist,
             uhigh_potion: uhigh_potion_deslist,
             magicbook1:magicbook1_list, magicbook2:magicbook2_list,
             magicbook3:magicbook3_list, smoke_name: smoke_list}

class items:
    def hp_heal(self, item_name, effect):
        '''Heals the player that used the item

        arguments:
        [item_name]: Name of the item (str)
        [effect]: Effect of the item on health (int)
        '''
        initial_hp = self.stats['hp']
        self.stats['hp'] += effect
        if self.stats['hp'] > self.stats['maxhp']:
            self.stats['hp'] = self.stats['maxhp']
        dif = self.stats['hp'] - initial_hp
        msg('体力が%s回復した。' % (dif))

    def learn_skill(self, effect):
        self.specials.append(effect)
        msg('「%s」を習得した!' % (effect))

    def use_item(self, item, index):
        '''Uses item within the inventory

        arguments:
        [item]: Name of the item. (str)
        [index]: Index of the item within the self's inventory. (int)

        returns:
        [0]: Item was not used
        [1]: Item was used
        [2]: An escape item was used
        '''
        des = item_desc[item]
        print('アイテム： %s' % (item))
        print('説明:' + des[0])
        cmd = ''
        while cmd not in ('y','n'):
            print('このアイテムを使いますか？(y/n)')
            cmd = input()
        if cmd == 'y':
            if item in healing_items: # If item is a healing item
                self.hp_heal(item, des[1])
                del self.items[index]
                return 1
            if item in escape_items: # If item is an escape item
                if self.lastbattle is True: # If an escape item is used during the boss battle
                    msg('ここで逃げるわけにはいかない！')
                    return 0
                elif self.inbattle is True: # If used during a normal battle
                    msg('上手く逃げられた。')
                    del self.items[index]
                    return 2
                else: # If used when not in battle
                    msg('今使っても意味がない。')
                    return 0
            if item in skill_items:
                if self.inbattle is True:
                    msg('今は使えないな。')
                    return 0
                else:
                    self.learn_skill(des[1])
                    del self.items[index]"""