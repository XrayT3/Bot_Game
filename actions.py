import player
import postgresql as pg
import buttons_reference as br
import classes
import battle as bt
import trainig as tr
import bank
import texts

db = pg.open(user='postgres', host='localhost', port='5432', password='123456', database='postgres')


get_items = db.prepare("SELECT * FROM items")
data = get_items()
data.sort(key=lambda tup: tup[0])
i_market = []
actions_ = [None for i in range(10000)]


class Action:
    id = None
    func = None
    text = None
    final = None

    def __init__(self, func, id=None, text=None, final=None):
        self.func = func
        self.id = id if id else None
        self.text = text if text else None
        self.final = final

    def execute(self, language, player_):
        self.text = self.func(language, player_)
        print('Self.text = ', self.text)
        if self.final:
            return 1
        elif self.text:
            return 0
        else:
            return -1


def check_start(msg):
    if len(msg.text) < 7:
        return
    user_id = int(msg.text[7:])
    if player.check_new_user(msg.from_user.id, msg) != 0:
        updater = db.prepare('UPDATE users SET invited = invited + 1 WHERE user_id = $1')
        updater(user_id)


def add_action(func, id, final=None):
    actions_[id] = Action(func, id=id if id else None, final=final)


def form_link(player_):
    return texts.get_text_(13, player_.language) + "\n\nhttps://t.me/quotationer_bot?start=" + str(player_.user_id)


def f_1(language, player_):
    return player_.get_profile(language)


def f_3(language, player_):
    print('63:actions:Language = ', language)
    text = ''
    text += texts.get_text_(14, language) + '\n' + texts.get_text_(15, language)+ ': '+str(player_.dinars)
    try:
        text += '\n' + texts.get_text_(7, language) + ' ' + str(int(player_.guarantees))
    except Exception as e:
        print(e)
    return text


def f_12(language, player_):
    data = bank.get_bank_money(player_)
    text = ''
    text += texts.get_text_(18, language) + '\n' + texts.get_text_(15, language) + ' ' + str(data[-1][0]) + \
            '\n' + texts.get_text_(7, language) + ' ' + str(player_.guarantees if player_.guarantees else 0)
    return text


def f_8(language, player_):
    text = 'Top 10:\n'
    exe = db.prepare('SELECT * FROM users WHERE level = (SELECT max(level) FROM users)')
    users = exe()
    for user in users[:(len(users) - 1 if len(users) < 10 else 10)]:
        if user:
            text += '\t\t\t' + str(user[2])
            text += '(' + str(user[3]) + ')\n'
    return text


def f_2(language, player_):
    text = '' + texts.get_text_(19, language) + '\n'
    text += player_.equipped.get_data(1) if player_.equipped else + texts.get_text_(20, language)
    return text


def f_10(language, player_):  # make_fight
    if not player_:
        print('Error occurred')
    res = bt.find_battle(0, 1, player_.user_id)
    if res == 0:
        return '' + texts.get_text_(21, language) + ''
    elif res == -1:
        return '' + texts.get_text_(22, language) + ''


def f_31(language, player_):
    bank.close_account(player_)


def f_7(language, player_):
    return form_link(player_)


def f_27(language, player_):
    if tr.training(player_, time_selected=2, power=1) == 0:
        return '' + texts.get_text_(9, language) + ' ' + texts.get_text_(23, language) + ''
    else:
        return '' + texts.get_text_(24, language) + ''


def f_28(language, player_):
    if tr.training(player_, time_selected=2, adroitness=1) == 0:
        return texts.get_text_(10, language) + ' ' + texts.get_text_(23, language)
    else:
        return texts.get_text_(24, language)


def f_29(language, player_):
    if tr.training(player_, time_selected=2, health=1) == 0:
        return texts.get_text_(12, language) + ' ' + texts.get_text_(23, language)
    else:
        return texts.get_text_(24, language)


def f_30(language, player_):
    if tr.training(player_, time_selected=2, armor=1) == 0:
        return texts.get_text_(11, language) + ' ' + texts.get_text_(23, language)
    else:
        return texts.get_text_(24, language)


def f_36(language, player_):
    return bank.add_money_by_percent(player_, 0.25)


def f_37(language, player_):
    return bank.add_money_by_percent(player_, 0.50)


def f_38(language, player_):
    return bank.add_money_by_percent(player_, 0.75)


def f_39(language, player_):
    return bank.add_money_by_percent(player_, 1.00)


'''
def find_battle_random(language, player_):
    type = 0
    level = player_.level
'''


def wardrobe(lang, player_):
    type_former = {1: 19, 2: 20, 3: 21, 4: 22}  # разделение типов предметов по своим кнопкам
    # если у человека есть инвентарий, то запускаем его перевод в кнопки
    if player_.inventory:
        inv = player_.inventory
        for item in inv.all_items:
            but = classes.Button(args=[str(item.get_name(0)) + ' (' + str(item.level) + ' lvl)',
                                       item.get_name(1), None, None, None,
                                       item.get_description(0),
                                       item.get_description(1),
                                       None, None, None,
                                       type_former.get(int(item.type)), br.buttons[-1].id + 1])
            but.item = item.id
            but1 = classes.Button(
                args=[texts.get_text_(30, 0), texts.get_text_(30, 1), None, None, None, texts.get_text_(29, 0),
                      texts.get_text_(29, 1), None, None, None,
                      but.id, 'w' + str(item.id)])

    else:
        return texts.get_text_(31, lang)


def equip():
    print()


def load_buttons():
    global data, i_market, actions_
    actions_ = [None for i in range(10000)]
    add_action(f_1, 1, final=False)
    add_action(f_2, 2, final=False)
    add_action(f_3, 3, final=False)
    add_action(f_31, 31, final=True)
    add_action(f_12, 12, final=False)
    add_action(f_27, 27, final=True)
    add_action(f_28, 28, final=True)
    add_action(f_29, 29, final=True)
    add_action(f_30, 30, final=True)
    add_action(f_36, 36, final=True)
    add_action(f_39, 39, final=True)
    add_action(f_37, 37, final=True)
    add_action(f_38, 38, final=True)
    add_action(f_8, 8, final=True)
    add_action(f_10, 10, final=True)
    add_action(f_7, 7, final=True)
    i_market = [None]
    for item in data:
        i_market.append(classes.Item(item))
    inv = classes.Inventory(i_market[1:])
    type_former = {1: 23, 2: 24, 3: 25, 4: 26}
    for item in inv.all_items:
        # print(len(br) - 1)
        but = classes.Button(args=[str(item.get_name(0)) + ' (' + str(item.level) + ')',
                                   item.get_name(1) + ' (' + str(item.level) + ')',
                                   None, None, None,
                                   item.get_description(0),
                                   item.get_description(1),
                                   item.get_description(2),
                                   item.get_description(3),
                                   item.get_description(4),
                                   type_former.get(int(item.type)),
                                   br.buttons[-1].id + 1
                                   ])
        # print(len(br)-1)
        # print('but.id = ', but.id)
        br.buttons[but.id].is_desc = True
        br.buttons[but.id].is_buy_but = True
        br.buttons[but.id].item = item.id
        but2 = classes.Button(
            args=[texts.get_text_(31, 0), texts.get_text_(31, 1), None, None, None, item.get_description(1),
                  item.get_description(2), None, None, None, but.id, br.buttons[-1].id + 1])
