import texts
import base
import buttons_reference as br

class Button:
    id = None
    name_rus = ''
    name_eng = ''
    name_german = ''
    name_french = ''
    name_spanish = ''
    text_rus = ''
    text_eng = ''
    text_german = ''
    text_french = ''
    text_spanish = ''
    parent_id = None
    call = None
    parent = None
    is_buy_but = None
    item = None
    equip = None
    is_desc = None
    to_markup = True

    # todo_me remake

    def __init__(self, args=None, _id=None):
        if args:
            # print(args)
            self.id = (br.buttons[-1].id if br.buttons[-1] else 0) + 1
            self.id = _id if _id else self.id
            self.name_rus = args[0]
            self.name_eng = args[1]
            self.name_german = args[2]
            self.name_french = args[3]
            self.name_spanish = args[4]
            self.text_rus = args[5]
            self.text_eng = args[6]
            self.text_german = args[7]
            self.text_french = args[8]
            self.text_spanish = args[9]
            self.parent_id = args[10]
            self.call = args[11]
            br.buttons.append(self)

    def get_text(self, lang):
        if lang == 0:
            if self.text_rus:
                return self.text_rus
        elif lang == 1:
            if self.text_eng:
                return self.text_eng
        elif lang == 2:
            if self.text_german:
                return self.text_german
        elif lang == 3:
            if self.text_french:
                return self.text_french
        elif lang == 4:
            if self.text_spanish:
                return self.text_spanish
        else:
            return None

    def get_ru_name(self):
        return self.name_rus

    def get_name(self, lang):
        if lang == 0:
            return self.name_rus
        elif lang == 1:
            return self.name_eng
        elif lang == 2:
            return self.name_german
        elif lang == 3:
            return self.name_french
        elif lang == 4:
            return self.name_spanish

    def get_data(self):
        print('id = ' + str(self.id) +
              '\nName = ' + self.get_name(1) +
              '\nText = ' + self.get_text(1) +
              '\nparent_id = ' + str(self.parent_id) +
              '\nCall = ' + str(self.call))


class Item:
    id = None
    name_rus = None
    name_eng = None
    name_german = None
    name_french = None
    name_spanish = None

    durability = None
    type = None
    types = {1: 'weapon',
             2: 'head_armor',
             3: 'body_armor',
             4: 'legs_armor'}
    add_power = None
    add_adroitness = None
    add_armor = None
    add_health = None
    level = None
    dinars = 0

    def __init__(self, args, new_durability=None):
        self.id = args[0]
        self.name_rus = args[1]
        self.name_eng = args[2]
        self.name_german = args[3]
        self.name_french = args[4]
        self.name_spanish = args[5]
        self.type = int(args[6])
        self.durability = args[7]
        self.level = args[8]
        self.add_power = args[9]
        self.add_adroitness = args[10]
        self.add_armor = args[11]
        self.add_health = args[12]
        self.dinars = args[13]
        self.durability = new_durability if new_durability else self.durability

    def get_name(self, lang):
        if lang == 0:
            return self.name_rus
        elif lang == 1:
            return self.name_eng
        elif lang == 2:
            return self.name_german
        elif lang == 3:
            return self.name_french
        elif lang == 4:
            return self.name_spanish

    def get_text(self, lang):
        if lang == 0:
            return self.text_rus
        elif lang == 1:
            return self.text_eng
        elif lang == 2:
            return self.text_german
        elif lang == 3:
            return self.text_french
        elif lang == 4:
            return self.text_spanish

    def get_description(self, lang):
        data = ''
        data += str(self.get_name(lang))
        data += '(' + str(self.durability) + ')\n' + texts.get_text_(3, lang) + ' = ' + str(self.level)
        if self.add_power != 0:
            data += '\n' + texts.get_text_(9, lang) + '+' + str(self.add_power) + ')\n'
        elif self.add_adroitness != 0:
            data += '(' + texts.get_text_(10, lang) + '+' + str(self.add_adroitness) + ')\n'
        elif self.add_armor != 0:
            data += '(' + texts.get_text_(11, lang) + '+' + str(self.add_armor) + ')\n'
        elif self.add_health != 0:
            data += '(' + texts.get_text_(12, lang) + '+' + str(self.add_health) + ')\n'
        data += str(self.dinars) + ' ' + texts.get_text_(15, lang)
        return data


class Inventory:
    weapon = []
    head_armor = []
    body_armor = []
    legs_armor = []
    all_items = [None]
    data = [None, weapon, head_armor, body_armor, legs_armor]

    def __init__(self, items=None):
        self.all_items = []
        self.weapon = []
        self.head_armor = []
        self.body_armor = []
        self.legs_armor = []
        self.data = [None, self.weapon, self.head_armor, self.body_armor, self.legs_armor]
        if items:
            for item in items:
                print(items)
                self.all_items.append(item)
                self.data[item.type].append(item)

    def get_data(self, lang):
        text = ''
        for item in self.all_items:
            text += item.get_description(lang)
            text += '\n'
        return text

    @staticmethod
    def inventory_parser(inv):
        data = inv.split('/')
        inventory = []
        data = [value for value in data if value != '']
        for item_data in data:
            data = item_data.split('#')
            print(data)
            inventory.append(Item(args=base.get_item(int(data[0]))[-1], new_durability=data[1]))
        return inventory


class Player:
    name = None
    id = None
    user_id = None
    level = None
    fights = None
    wins = None
    power = None
    adroitness = None
    armor = None
    health = None
    add_power = None
    add_adroitness = None
    add_armor = None
    add_health = None
    bank = None
    small = None
    medium = None
    big = None
    commercial = None
    guarantees = None
    invited = None
    inventory = Inventory()
    equipped = None
    next_training = None
    language = 0
    scores = None
    dinars = 0

    def __init__(self, args):
        # print()
        if not args:
            return
        self.id = args[0]
        self.user_id = args[1]
        self.name = args[2]
        self.level = args[3]
        self.fights = args[4]
        self.wins = args[5]
        self.small = args[6]
        self.medium = args[7]
        self.big = args[8]
        self.commercial = args[9]
        self.guarantees = args[10]
        self.invited = args[11]
        self.power = args[12]
        self.adroitness = args[13]
        self.armor = args[14]
        self.health = args[15]
        self.add_power = args[16]
        self.add_adroitness = args[17]
        self.add_armor = args[18]
        self.add_health = args[19]
        self.inventory = Inventory(self.inventory.inventory_parser(args[20]))
        self.equipped = Inventory(self.inventory.inventory_parser(args[21])) if args[21] else None
        self.next_training = args[22]
        self.language = args[23] if args[23] else 0
        self.scores = args[24] if args[24] else 0
        self.dinars = args[25]

    def set_language(self, lang):
        # print(lang)
        self.language = lang

        base.update_language(str(lang), self.user_id)

    def update_plus_scores(self, plus_scores):
        self.scores = self.scores + plus_scores
        if self.scores > self.level * 500:
            self.level += 1
            self.update_level()
        exe = base.update_plus_scores
        exe(plus_scores, self.user_id)

    '''
    def update_scores(self):
        exe = db.prepare('UPDATE users SET scores = $1 WHERE user_id = $2')
        exe(self.scores, self.user_id)
    '''

    def update_level(self):
        exe = base.update_level
        exe(self.level, self.user_id)

    def update_inventory(self, item_id, durability=None):
        get_data = base.get_user_data
        inv = get_data(self.user_id)[-1][-2]
        # ('inv =', inv)
        if inv.find(str(item_id)) == -1:
            inv += str(item_id) + '#' + str(durability) if durability else '' + '/'
            base.update_inventory(inv, self.user_id)
            self.inventory = Inventory(self.inventory.inventory_parser(inv))
            return 0
        elif not durability:
            return -1

    def update_adders(self):
        base.update_add_power(self.add_power, self.user_id)
        base.update_add_armor(self.add_armor, self.user_id)
        base.update_add_health(self.add_health, self.user_id)
        base.update_add_adroitness(self.add_adroitness, self.user_id)

    def update_plus_coins(self, dinars):
        self.dinars += dinars
        base.update_plus_coins(self.dinars, self.user_id)

    def update_invited(self):
        self.invited += 1
        base.increment_invited(self.user_id)

    def update_equipped(self, item):
        self.add_armor = item.add_armor
        self.add_health = item.add_health
        self.add_power = item.add_power
        self.add_adroitness = item.add_adroitness
        if not self.equipped:
            inv = Inventory()
            inv.data[item.type] = [item]
            base.update_equipped('/' + str(item.id) + '#' + str(item.durability) + '/', self.user_id)
        else:
            print('equipped data = ', self.equipped.data[1:])
            self.equipped.data[item.type] = [item]
            str_ = ''
            for d in self.equipped.data[1:]:
                if d:
                    str_ += '/' + str(d[-1].id) + '#' + str(d[-1].durability) + '/'
            base.update_equipped(str_, self.user_id)

            for item in self.equipped.data:
                if item:
                    self.add_armor += item[-1].add_armor
                    self.add_health += item[-1].add_health
                    self.add_power += item[-1].add_power
                    self.add_adroitness += item[-1].add_adroitness
        self.update_adders()

    def buy_item(self, item):
        inv = base.get_inventory(self.user_id)[-1][0]
        if not inv:
            inv += '/'
        if inv.find(str(item.id)) == -1:
            if self.dinars >= item.dinars:
                inv += str(item.id) + '#' + str(item.durability) + '/'
                self.dinars -= item.dinars
                self.inventory = Inventory(self.inventory.inventory_parser(inv))
                base.update_inventory(inv, self.user_id)
                base.update_dinars(self.dinars, self.user_id)
                return 0
            else:
                return -2
        else:
            return -1

    def get_profile(self, language):
        str_ = ''
        str_ += texts.get_text_(3, language) + ' = ' + str(self.name) + \
            '\n' + texts.get_text_(4, language) + ' = ' + str(self.level) + \
            '\n' + texts.get_text_(5, language) + ' = ' + str(self.fights) + \
            '\n' + texts.get_text_(6, language) + ' = ' + str(self.wins) + \
            '\n' + texts.get_text_(7, language) + ' = ' + str(self.guarantees) + \
            '\n' + texts.get_text_(8, language) + ' = ' + str(self.invited) + \
            '\n' + texts.get_text_(9, language) + ' = ' + str(self.power) + ' (+' + str(self.add_power) + ')' + \
            '\n' + texts.get_text_(10, language) + ' = ' + str(self.adroitness) + ' (+' + str(self.add_adroitness) + ')' + \
            '\n' + texts.get_text_(11, language) + ' = ' + str(self.armor) + ' (+' + str(self.add_adroitness) + ')' + \
            '\n' + texts.get_text_(12, language) + ' = ' + str(self.health) + ' (+' + str(self.add_health) + ')'
        return str_

        # todo_me дописать условие else для update_durability

    def update_money(self, dinars):
        if dinars > self.dinars:
            return -1
        base.update_dinars(self.dinars-dinars, self.id)


