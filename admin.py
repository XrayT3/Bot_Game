import postgresql as pg
import telebot
import time
import texts
from requests import ConnectionError
import requests.exceptions as rExceptions
# import textwrap

token = '383485065:AAGh6gsS8vfYZMEi6ERwUQHdOZOK3jrVLbw'
bot = telebot.TeleBot(token)
db = pg.open(user='postgres', host='localhost', port='5432', password='123456', database='postgres')


link = 'http://telegra.ph/Rukovodstvo-po-redaktirovaniyu-05-11'

keywords = {
    'delete':0,
    'insert':1,
    'get':2,
}

keywords2 = {
    'buttons':0,
    'items':1,
    'texts':2,
    'users':3,
}


@bot.message_handler(commands=['start'])
def handle_start(message):
    bot.send_message(message.chat.id, link)


@bot.message_handler(content_types=['text'])
def handle_text(message):
    query = message.text.split(sep=' ')
    if len(query)>2:
        query[2] = str(query[2]).replace('_', ' ')
    print('Query = ',query)
    data1 = keywords.get(query[0])
    data2 = keywords2.get(query[1])
    print('Data1/2 = ', data1, data2)
    if data1 == 0:
        if data2 == 0:
            delete_button_(int(query[2]))
        elif data2 == 1:
            delete_item_(int(query[2]))
        elif data2 == 2:
            delete_text_(int(query[2]))
        elif data2 == 3:
            delete_user_(int(query[2]))

    elif data1 == 1:
        if data2 == 0:
            add_button(query[2])
        elif data2 == 1:
            add_item(query[2])
        elif data2 == 2:
            add_text(query[2])
        elif data2 == 3:
            add_user(query[2])
    elif data1 == 2:
        if data2 == 0:
            for line in get_buttons_():
                bot.send_message(message.chat.id, str(line))
        elif data2 == 1:
            for line in get_items_():
                bot.send_message(message.chat.id, str(line))
        elif data2 == 2:
            for line in get_texts_():
                bot.send_message(message.chat.id, str(line))
        elif data2 == 3:
            for line in get_users_():
                bot.send_message(message.chat.id, str(line))






insert_button = db.prepare('INSERT INTO buttons(name_rus, name_eng, name_german, name_french, name_spanish,'
                           ' text_rus, text_eng, text_german, text_french, text_spanish,'
                           ' parent_id, calldata)'
                           ' VALUES '
                           '($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12)')

insert_item = db.prepare('INSERT INTO items(name_rus, name_eng, name_german, name_french, name_spanish,'
                          ' type, durability, level ,'
                          ' add_power , add_adroitness , add_armor , add_health ,'
                          ' gold , silver , bronze)'
                          'VALUES '
                          '($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14, $15)')
insert_user = db.prepare("INSERT INTO users(user_id, name, level, fights, wins,"
                           " gold, silver, bronze, small, medium, big,"
                           "commercial, guarantees, invited, power, adroitness, armor, health,"
                           "add_power, add_adroitness, add_armor, add_health,"
                           " inventory, equipped, next_training, language) "
                           "VALUES($1, $2, $3, $4, $5, $6, $7, $8, $9,"
                           "$10, $11, $12, $13, $14, $15, $16, $17, $18, $19, $20, $21, $22, $23, $24, $25, $26)")

insert_text = db.prepare('INSERT INTO texts(text_rus, text_eng, text_german, text_french, text_spanish,'
                         ' eng_description) VALUES ($1, $2, $3, $4, $5, $6) ')

get_buttons = db.prepare('SELECT * FROM buttons')
get_users = db.prepare('SELECT * FROM users')
get_items = db.prepare('SELECT * FROM items')
get_bank = db.prepare('SELECT * FROM bank')
get_text = db.prepare('SELECT * FROM texts')

delete_button = db.prepare('DELETE FROM buttons WHERE id = $1')
delete_user = db.prepare('DELETE FROM users WHERE id = $1')
delete_item = db.prepare('DELETE FROM items WHERE id = $1')
delete_text = db.prepare('DELETE FROM texts WHERE id = $1')


def add_button(str_):
    data = str_.split('/')
    data[10] = int(data[10])
    if len(data) != 11:
        print('ho')
        return 'Not enough arguments'
    else:
        print(*data)
        insert_button(*data, None)
    db.execute('UPDATE buttons SET calldata = id WHERE calldata = NULL')


def add_user(str_):
    data = str_.split(sep='/')
    print('add user data = ',data, len(data))
    for i in {0, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 24}:
        data[i] = 0 if data[i] == 'None' else int(data[i])
    if len(data) != 26:
        return 'Not enough arguments'
    else:
        print('go')
        insert_user(*data)


def add_text(str_):
    data = str_.split(sep='/')
    print('add text data = ', data)
    if len(data) != 6:
        return 'Not enough arguments'
    else:
        texts.insert_text(*data)


def add_item(str_):
    data = str_.split(sep='/')
    if len(data) != 15:
        return 'Not enough arguments'
    else:
        insert_item(*data)


def get_buttons_():
    lines = []
    for but in get_buttons():
        lines.append(str(but))
    if not lines:
        return ['None_']
    return lines


def get_users_():
    lines = []
    for user in get_users():
        lines.append(str(user))
    if not lines:
        return ['None_']
    return lines


def get_items_():
    lines = []
    for item in get_items():
        lines.append(str(item))
    if not lines:
        return ['None_']
    return lines


def get_texts_():
    lines = []
    for text in get_text():
        lines.append(str(text))
    if not lines:
        return ['None_']
    return lines


def delete_user_(deleting_user_id):
    delete_user(deleting_user_id)
    if not get_users():
        db.execute('ALTER SEQUENCE users_id_seq RESTART WITH 1')


def delete_text_(deleting_text_id):
    delete_text(deleting_text_id)


def delete_item_(deleting_item_id):
    delete_item(deleting_item_id)


def delete_button_(deleting_button_id):
    delete_button(deleting_button_id)


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
