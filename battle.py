from player import authorize
import postgresql as pg
import telebot
import markups_former, base
import texts
import time
import random
db = pg.open(user='postgres', host='localhost', port='5432', password='123456', database='postgres')

but1 = [[None, None, None, None, None], [None, None, None, None, None]]
but2 = [[None, None, None, None, None], [None, None, None, None, None]]
but3 = [[None, None, None, None, None], [None, None, None, None, None]]
but1[0] = [texts.get_text_(37, i) for i in range(5)]
but2[0] = [texts.get_text_(38, i) for i in range(5)]
but3[0] = [texts.get_text_(39, i) for i in range(5)]
but1[1] = [texts.get_text_(40, i) for i in range(5)]
but2[1] = [texts.get_text_(41, i) for i in range(5)]
but3[1] = [texts.get_text_(42, i) for i in range(5)]


def get_queues():
    data = base.get_data('queue')
    mas = []
    for d in data:
        mas.append(dict(id=d[0], level=d[1], type_=d[2], player1_id=d[3], player2_id=d[4]))
    return mas


def get_battles():
    data = base.get_data('fights')
    mas = []
    for d in data:
        mas.append(dict(id=d[0], fighter1_id=d[1], fighter2_id=d[2], f1_health=d[3], f2_health=d[4],
                        f1_exp=d[5], f2_exp=d[6]))
    return mas


def attack_markup(battle, player_num):
    battle.get_data()
    # player_num - его номер, номер атакующего,он же передается дальше
    mas = []
    player_ = battle.fighter1 if player_num == 1 else battle.fighter2
    print('42:battle.py:Attack : ', player_.name)
    mas.append(but1[0][0])
    mas.append(str('f/a/' + str(battle.fighter1.user_id) + '/' + str(player_num) + '/l/' + str(
        int(player_.power + player_.add_power))))
    mas.append((but2[0][0]))
    mas.append(str('f/a/' + str(battle.fighter1.user_id) + '/' + str(player_num) + '/r/' + str(
        int(player_.power + player_.add_power))))
    mas.append((but3[0][0]))
    mas.append(str('f/a/' + str(battle.fighter1.user_id) + '/' + str(player_num) + '/c/' + str(
        int(player_.power + player_.add_power))))
    return markups_former.get_inline_markup(2, 3, *mas)


# f/a/fighter1_id/playernum/dir/power
# f/d/fighter1_id/opp_dir/opp_damage/playernum/dir/armor

# fight, player_num, dir, power

def defence_markup(battle, player_num, dir, damage):
    player_ = battle.fighter2 if player_num == 1 else battle.fighter1   # если атаковал 1, то защищается 2
    print('61:battle.py:Defend : ',player_.name)
    mas = [but1[1][0], str(
        'f/d/' + str(battle.fighter1.user_id) + '/' + dir + '/' + damage + '/' + player_num + '/l/' + str(
            int(player_.armor + player_.add_armor))), (but2[1][0]), str(
        'f/d/' + str(battle.fighter1.user_id) + '/' + dir + '/' + damage + '/' + player_num + '/r/' + str(
            int(player_.armor + player_.add_armor))), (but3[1][0]), str(
        'f/d/' + str(battle.fighter1.user_id) + '/' + dir + '/' + damage + '/' + player_num + '/c/' + str(int(player_.armor + player_.add_armor)))]
    return markups_former.get_inline_markup(2, 3, *mas)


def find_battle(type, level, player2_id):  # ищет второй , первый просто оставлял заявку, первый и начинает
    mas = []
    # print('queues! =',get_queues())
    for queue in get_queues():
        mas.append(Queue(**queue))  # составление массива заявок
    # print('mas = ',mas)
    for queue in mas:
        if queue.level == level and queue.type == type and queue.player1_id != player2_id:  # проверка заявок
            player2_ = authorize(player2_id)
            queue.player2 = player2_
            queue.player2_id = player2_id
            queue.get_data()
            battle = Battle(queue=queue)
            queue.delete()
            token = '346023811:AAERJkszYOwf1K5Yjnq1F3gtXTLQasvXcjo'
            bot = telebot.TeleBot(token)
            bot.send_message(battle.fighter2.user_id, texts.get_text_(43, battle.fighter2.language))
            # Отправление сообщения искавшему пользователю о том, что его противник найден и инициализация
            #                                                                           боевого интерфейса
            bot.send_message(battle.fighter1.user_id, texts.get_text_(43, battle.fighter1.language),
                             reply_markup=attack_markup(battle, 1))
            return 0
            # Аналогично для второго
    # print('smth#############')
    my_queue = Queue(type_=type, level=level, player1_id=player2_id)
    my_queue.add_to_queue()
    return -1


class Queue:
    id = None
    level = None
    type = None
    player1_id = None
    player1 = None
    player2_id = None
    player2 = None

    def update_player2(self, player2_id=None):
        if player2_id:
            self.player2_id = player2_id
            self.player2 = authorize(player2_id)
            exe = db.prepare('UPDATE queue SET player2_id = $1 WHERE id = $2')
            exe(player2_id, self.id)

    def __init__(self, id=None, level=None, type_=None, player1_id=None, player2_id=None):
        flag = None
        if player1_id not in [queue.get('player1_id') for queue in get_queues()]:
            flag = True
        # print(type_, self.type)
        self.id = (get_queues()[-1].get('id') + 1) if get_queues() else 1
        self.id = id if id else self.id
        self.level = level if level else self.level
        self.type = int(type_) if type_ != None else int(self.type)
        self.player1_id = player1_id if player1_id else self.player1_id
        self.player2_id = player2_id if player2_id else self.player2_id
        self.player1 = authorize(self.player1_id) if self.player1_id else self.player1
        self.player1 = authorize(self.player1_id) if self.player1_id else self.player1
        if flag:
            self.add_to_queue()

    def get_data(self):
        print(
            'Queue #' + str(self.id) + '\nLevel = ' + str(self.level) + '\nType = ' + str(self.type) + '\nPlayer1 = ' +
            str(self.player1_id) + '\nPlayer2 = ' + str(self.player2_id) + '\nplayer1: ' +
            str(type(self.player1)) + '\nplayer2: ' + str(type(self.player2)))

    def add_to_queue(self):
        adder = db.prepare('INSERT INTO queue (level, type, player1_id) VALUES ($1, $2, $3)')
        adder(self.level, self.type, self.player1_id)

    def delete(self):
        deleter = db.prepare('DELETE FROM queue WHERE id = $1')
        deleter(self.id)
        if not base.get_data('queue'):
            db.execute('ALTER SEQUENCE queue_id_seq RESTART WITH 1')


class Battle:
    id = None
    fighter1 = None
    fighter2 = None
    f1_health = None
    f2_health = None
    f1_exp = None
    f2_exp = None
    last_turn_time = None
    last_turn_by = None

    def __init__(self, fighter1_id=None, fighter2_id=None, f1_health=None,
                 f2_health=None, f1_exp=None, f2_exp=None, last_turn_time = None, last_turn_by = None, queue=None, user_id=None):

        exe = db.prepare('INSERT INTO fights '
                         '(fighter1_id, fighter2_id '
                         ', f1_health, f2_health,'
                         ' f1_exp, f2_exp, last_turn, last_by) '
                         'VALUES ($1, $2, $3, $4, $5, $6, $7, $8) ')

        exe1 = db.prepare('UPDATE fights SET f1_health = $1, f2_health = $2,'
                          ' f1_exp = $3, f2_exp = $4, last_turn = $5, last_by = $6 WHERE fighter1_id = $5')

        if queue:
            self.fighter1 = queue.player1
            self.fighter2 = queue.player2
            self.f1_health = self.fighter1.health + self.fighter1.add_health
            self.f2_health = self.fighter1.health + self.fighter1.add_health
            exe(self.fighter1.user_id, self.fighter2.user_id, self.fighter1.health + self.fighter1.add_health,
                self.fighter2.health + self.fighter2.add_health, 0, 0, None, None)
        elif user_id:
            get_by_user_id = db.prepare('SELECT * FROM fights WHERE fighter1_id = $1')
            fight = get_by_user_id(user_id)
            fight = fight[-1] if fight else None
            if not fight:
                return
            self.fighter1 = authorize(fight[1])
            self.fighter2 = authorize(fight[2])
            self.f1_health = fight[3]
            self.f2_health = fight[4]
            self.f1_exp = fight[5]
            self.f2_exp = fight[6]
            self.last_turn_time = fight[7]
            self.last_turn_by = fight[8]
        else:
            self.f1_health = f1_health
            self.f2_health = f2_health
            self.f1_exp = f1_exp
            self.f2_exp = f2_exp
            self.last_turn_time = last_turn_time
            self.last_turn_by = last_turn_by
            self.fighter1 = authorize(fighter1_id)
            self.fighter2 = authorize(fighter2_id)
            self.type = type
            if not (fighter1_id in [battle.get('fighter1_id') for battle in get_battles()] or fighter1_id in [
                battle.get('fighter2_id') for battle in get_battles()]):
                exe(fighter1_id, fighter2_id, self.f1_health + self.fighter1.add_health,
                    self.f2_health + self.fighter2.add_health, 0, 0, None, None)
            else:
                exe1(f1_health, f2_health, f1_exp, f2_exp, fighter1_id, last_turn_time, last_turn_by)

        data = base.get_data('fights')
        # print(data)

    def update_base(self):
        exe1 = db.prepare(
            'UPDATE fights SET f1_health = $1, f2_health = $2, f1_exp = $3, f2_exp = $4,last_turn = $5, last_by = $6 WHERE fighter1_id = $7')
        exe1(self.f1_health, self.f2_health, self.f1_exp, self.f2_exp,self.last_turn_time, self.last_turn_by, (self.fighter1.user_id if self.fighter1 else None))

    def delete(self):
        exe = db.prepare('DELETE from fights WHERE fighter1_id = $1')
        exe(self.fighter1.id)

    def get_data(self):
        print('Battle #' + str(self.id) + '\nFighter1 = ' +
              str(self.fighter1.user_id) + '\nFighter2 = ' + str(self.fighter2.user_id) + '\nHealth1: ' +
              str(self.f1_health) + '\nHealth2: ' + str((self.f2_health)))

    def make_turn(self, player_num, dir1, dir2, damage, armor):
        token = '346023811:AAERJkszYOwf1K5Yjnq1F3gtXTLQasvXcjo'
        bot = telebot.TeleBot(token)
        print('224:battle.py: Data = ', player_num, dir1, dir2, damage, armor)
        self.last_turn_time = time.time()
        if int(player_num)==1:
            self.last_turn_by = self.fighter1.user_id
        else:
            self.last_turn_by = self.fighter2.user_id
            self.update_base()
        if dir1 == dir2:
            dmg = (int(damage) - int(armor)) if (int(damage) - int(armor) > 1) else 1
            if int(player_num) == 1:
                self.last_turn_time = time.time()
                self.last_turn_by = self.fighter1.user_id
                self.f2_health -= dmg
                self.f1_exp += int(dmg / 10)
                self.update_base()
                if self.f2_health <= 0:
                    bot.send_message(self.fighter2.user_id, '' + texts.get_text_(56, self.fighter2.language) + ' ' + texts.get_text_(52, self.fighter2.language) + ' ' + str(self.f2_exp) + ' ' + texts.get_text_(45, self.fighter2.language) + '')
                    bot.send_message(self.fighter1.user_id, '' + texts.get_text_(55, self.fighter1.language) + ' ' + texts.get_text_(52, self.fighter1.language) + ' ' + str(self.f1_exp) + ' ' + texts.get_text_(47, self.fighter1.language) + ' ' + str(self.fighter2.level * 10 + 10) + ' ' + texts.get_text_(17, self.fighter1.language) + '.\n' + texts.get_text_(48, self.fighter1.language) + '')
                    self.fighter1.update_plus_scores(
                        (self.fighter1.level-self.fighter2.level if self.fighter1.level-self.fighter2.level >0 else 0)\
                        + (int(0.3*self.fighter1.level) if int(0.3*self.fighter1.level) > 1 else 1))
                    self.fighter1.update_plus_coins(random.randrange(0,self.fighter1.level))
                    self.fighter2.update_plus_scores(self.fighter1.scores*0.2)
                    self.fighter2.update_plus_coins(0)
                    self.delete()
                else:
                    self.update_base()
                    bot.send_message(self.fighter2.user_id, '' + texts.get_text_(52, self.fighter2.language) + ' ' + str(dmg) + ' ' + texts.get_text_(53, self.fighter1.language) + '.\n' + str(self.f2_health) + ' ' + texts.get_text_(54, self.fighter1.language) + '.\n ' + texts.get_text_(50, self.fighter1.language) + '', reply_markup=attack_markup(self, 2))
            else:
                self.f1_health -= dmg
                self.f2_exp += int(dmg / 10)
                self.last_turn_time = time.time()
                self.last_turn_by = self.fighter2.user_id
                self.update_base()
                if self.f1_health <= 0:
                    token = '346023811:AAERJkszYOwf1K5Yjnq1F3gtXTLQasvXcjo'
                    bot = telebot.TeleBot(token)
                    bot.send_message(self.fighter1.user_id, '' + texts.get_text_(56, self.fighter1.language) + ' ' + texts.get_text_(52, self.fighter1.language) + ' ' + str(self.f1_exp) + ' ' + texts.get_text_(45, self.fighter1.language) + ''+texts.get_text_(46, self.fighter1.language))
                    bot.send_message(self.fighter2.user_id, '' + texts.get_text_(55, self.fighter2.language) + ' ' + texts.get_text_(52, self.fighter2.language) + ' '+ str(self.f2_exp) + ' ' + texts.get_text_(47, self.fighter2.language) + ' ' + str(self.fighter2.level * 10 + 10) + ' ' + texts.get_text_(17, self.fighter1.language) + '.\n' + texts.get_text_(48, self.fighter2.language) + '')
                    self.fighter2.update_plus_scores(
                        (self.fighter2.level - self.fighter1.level if self.fighter2.level - self.fighter1.level > 0 else 0) \
                        + (int(0.3 * self.fighter2.level) if int(0.3 * self.fighter2.level) > 1 else 1))
                    self.fighter1.update_plus_coins(random.randrange(0, self.fighter2.level))
                    self.fighter1.update_plus_scores(int(self.fighter2.scores * 0.2))
                    self.fighter1.update_plus_coins(0)
                    self.delete()
                else:
                    self.update_base()
                    bot.send_message(self.fighter1.user_id, 'You got '+ str(dmg) + ' points of damage.\n'+str(self.f1_health) +' points left.\n Your turn.', reply_markup=attack_markup(self, 1))
            # расписать ф-ю перехода хода & по возможности db_update реализовать в сеттерах полей
        else:
            at = self.fighter2 if player_num == 1 else self.fighter1
            df = self.fighter1 if player_num == 1 else self.fighter2
            num = 1 if player_num == 1 else 2
            bot.send_message(at.user_id, '' + texts.get_text_(49, self.fighter1.language) + ' ')
            bot.send_message(df.user_id, '' + texts.get_text_(50, self.fighter1.language) + ' ' + texts.get_text_(51, self.fighter1.language) + '', reply_markup=attack_markup(self, num))
