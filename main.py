import logging
import time
import requests.exceptions as rExceptions
import telebot
from requests import ConnectionError
from telegram.ext import Job, Updater
import actions as ac
import base
import battle
import buttons_reference as br
import markups_former
import player
import texts

logging.basicConfig(format=u'%(filename)s[LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s]  %(message)s',
                    level=logging.DEBUG)

token = '346023811:AAERJkszYOwf1K5Yjnq1F3gtXTLQasvXcjo'
bot = telebot.TeleBot(token)
upd = Updater(token)
queue = upd.job_queue

DAY = 60*60*24


# news_sender_block
def spam(bot_, job):
    for id_ in job.context[0]:
        bot_.send_message(chat_id=id_, text=job.context[1])


for news in base.get_daily_news():
    context_ = [
        base.get_all_user_id(),
        str(news[0])
    ]
    job_sec = Job(spam, DAY * int(news[1]), context=context_)
    queue.put(job_sec, 0.0)


def check(bot_, queue):
    data1 = base.change_turn1(time.time())
    data2 = base.change_turn2(time.time())
    for d in data1:
        bat = battle.Battle(user_id=int(d[2]))
        bat.last_turn_time = time.time()
        bat.last_turn_by = d[2]
        bat.update_base()
        bot.send_message(d[1],'Время ожидания вашего хода кончилось. Ход переходит к другому игроку',reply_markup=None)
        bot.send_message(d[2],'Противник побоялся что-то предпринять, ход переходит к вам',
                         reply_markup=battle.attack_markup(bat,2))
    for d in data2:
        bat = battle.Battle(user_id=int(d[1]))
        bat.last_turn_time = time.time()
        bat.last_turn_by = d[1]
        bat.update_base()
        bot.send_message(int(d[2]), 'Время ожидания вашего хода кончилось. Ход переходит к другому игроку',
                         reply_markup=None)
        bot.send_message(int(d[1]), 'Противник побоялся что-то предпринять, ход переходит к вам',
                         reply_markup=battle.attack_markup(bat, 1))

queue.run_repeating(check, 15)

queue.start()


def loader():
    br.buttons = br.get_buttons()
    ac.load_buttons()
    markups_former.buttons = br.get_buttons()

menus = None


@bot.message_handler(commands=['start'])
def handle_start(message):
    ac.check_start(message)
    loader()
    if player.check_new_user(message.from_user.id, message) == -1:
        markup = markups_former.get_markup(2, 4, 'Русский', 'English', 'Deutsche', 'Français', 'Espanol')
        bot.send_message(message.chat.id, texts.get_text_(2, 1), reply_markup=markup)                                   # languages.get_text_(1, 1)
    else:               # default lang - english. Language text - #1 in base
        player_ = player.authorize(message.from_user.id, message)
        print('player_lang = ',player_.language)
        bot.send_message(message.chat.id, texts.get_text_(1, player_.language), reply_markup=markups_former.main_markup(player_.language))       # languages.get_text_(2, player_.language)
        # welcome text - #2 in base


@bot.message_handler(content_types=['text'], func=lambda message:message.text in list(texts.languages_))
def handle_text(message):
    loader()
    player_ = player.authorize(message.from_user.id, message)
    player_.set_language(texts.languages_.get(message.text))
    print('test:55: ',texts.languages_.get(message.text), message.text)
    bot.send_message(message.chat.id, texts.get_text_(1, player_.language), reply_markup=markups_former.main_markup(player_.language))         # languages.get_text_(2, player_.language)


@bot.message_handler(content_types=['text'], func=lambda message:message.text in (list(markups_former.main_markup_dict(player.authorize(message.from_user.id, message).language).keys())))
def text_handler(message):
    loader()
    print('alive:61:test')
    player_ = player.authorize(message.from_user.id, message)
    id_ = markups_former.main_markup_dict(player_.language).get(message.text)
    markup = markups_former.form_buttons(int(id_), player_.language, player_)
    text = br.get_description(int(id_), player_.language)
    bot.send_message(message.chat.id, text, reply_markup=markup)


@bot.callback_query_handler(func=lambda call:call.data[0] == 'f')
def fight_query_handler(call):
    loader()
    player_ = player.authorize(call.message.chat.id, call.message)
    if not player_:
        raise Exception('Player authorizing error')
    call.data = call.data[2:]

    if call.data[0] == 'a':
        mas = call.data.split(sep='/')
        print('80:main.py:Income data :', mas)
        fight = battle.Battle(user_id=int(mas[1]))
        player_num = mas[2]
        dir = mas[3]
        print('83:main.py:Attack by :',fight.fighter1.user_id if int(player_num) == 1 else fight.fighter2.user_id, fight.fighter1.name if int(player_num) == 1 else fight.fighter2.name )
        power = mas[4]
        print('86:main.py:With power = ', power)
        opponent_id = fight.fighter2.user_id if int(player_num) == 1 else fight.fighter1.user_id
        markup = battle.defence_markup(fight, player_num, dir, power)
        bot.edit_message_text(call.message.text, call.message.chat.id, call.message.message_id, reply_markup=None)
        print('90:main.py:Next turn by : ',fight.fighter2.name if int(player_num) == 1 else fight.fighter1.name, fight.fighter2.user_id if int(player_num) == 1 else fight.fighter1.user_id)
        bot.send_message(opponent_id,'Выберите направление уклонения.', reply_markup=markup)
    elif call.data[0] == 'd':
        mas = call.data.split(sep='/')
        print('masD =',mas)
        fight = battle.Battle(user_id=int(mas[1]))
        opponent_dir = mas[2]
        opponent_damage = mas[3]
        player_num = mas[4]
        dir = mas[5]
        armor = mas[6]
        defender = fight.fighter2 if int(player_num) == 1 else fight.fighter1
        bot.edit_message_text(call.message.text, call.message.chat.id, call.message.message_id, reply_markup=None)
        fight.make_turn(player_num, opponent_dir, dir, opponent_damage, armor)


@bot.callback_query_handler(func=lambda call:call.data[0] == 'w')
def wear_query_handler(call):
    loader()
    player_ = player.authorize(call.message.chat.id, call.message)
    if not player_:
        print('ERROR_PLAYER_AUTHORIZING')
        return
    item = ac.i_market[int(call.data[1:])]
    player_.update_equipped(item)
    bot.edit_message_text(text='Предмет успешно одет',
                          chat_id=call.message.chat.id,
                          message_id=call.message.message_id)


@bot.callback_query_handler(func=lambda call:call.data[0] == 'b')
def buy_query_handler(call):
    print('BUYING ITEMS', str(call.data[1:]))
    loader()
    player_ = player.authorize(call.message.chat.id, call.message)
    if not player_:
        print('ERROR_PLAYER_AUTHORIZING')
        return
    item = ac.i_market[int(call.data[1:])]
    operation_code = player_.buy_item(item)
    if operation_code == 0:
        bot.edit_message_text('Товар успешно куплен!',call.message.chat.id, call.message.message_id)
    elif operation_code == -1:
        bot.edit_message_text('Такой товар уже есть в инвентаре!', call.message.chat.id, call.message.message_id)
    elif operation_code == -2:
        bot.send_message(call.message.chat.id, 'У вас недостаточно средств на счёте.'
                                               ' \nУ вас на счету:\n ' +
                                               str(player_.gold) + ' золота\n' +
                                               str(player_.silver) + ' серебра\n' +
                                               str(player_.bronze) + 'бронзы')


@bot.callback_query_handler(func=lambda call:call.data == None or call.data == 'new')
def handle_errors(call):
    print('Error occured at '+str(time.ctime(time.time())))


@bot.callback_query_handler(func=lambda call:int(call.data) in range(-5, 10000))
def handler(call):
    print('call.data = ', call.data)
    player_ = player.authorize(call.message.chat.id, call.message)
    loader()
    if call.data == 0:
        markup = markups_former.main_markup(player_.language)
        bot.send_message(call.message.chat.id,texts.get_text_(1, player_.language), reply_markup=markup)

    markup = markups_former.form_buttons(int(call.data), player_.language, player_)
    text = br.get_description(int(call.data), 0)
    if not markup:
        markup = None
        text = texts.get_text_(1, player_.language)
    elif br.buttons[int(call.data)].is_desc:
        text = br.buttons[int(call.data)].text_rus

    bot.edit_message_text(text=text,
                          chat_id=call.message.chat.id,
                          message_id=call.message.message_id,
                          reply_markup=markup)


while True:
    try:
        bot.polling(none_stop=True, interval=0)
    except ConnectionError as exptn:
        # log(Exception='HTTP_CONNECTION_ERROR', text=exptn)
        print('Connection lost..')
        time.sleep(30)
        continue
    except rExceptions.Timeout as exptn:
        # log(Exception='HTTP_REQUEST_TIMEOUT_ERROR', text=exptn)
        time.sleep(5)
        continue
