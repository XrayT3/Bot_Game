import postgresql as pg
db = pg.open(user='postgres', host='localhost', port='5432', password='123456', database='postgres')

db.execute('CREATE TABLE users (id SERIAL PRIMARY KEY, user_id INTEGER, name TEXT, level INTEGER, fights INTEGER, wins INTEGER, small INTEGER, medium INTEGER, big INTEGER, commercial INTEGER, guarantees INTEGER, invited INTEGER, power INTEGER, adroitness INTEGER, armor INTEGER, health INTEGER, add_power INTEGER, add_adroitness INTEGER, add_armor INTEGER, add_health INTEGER, inventory TEXT, equipped TEXT, next_training INTEGER, language INTEGER, scores INTEGER, dinars INTEGER)')
db.execute('CREATE TABLE items ( id SERIAL PRIMARY KEY, name_rus TEXT, name_eng TEXT, name_german TEXT, name_french TEXT, name_spanish TEXT, type INTEGER, durability INTEGER, level INTEGER, add_power INTEGER, add_adroitness INTEGER, add_armor INTEGER, add_health INTEGER, dinars INTEGER)')
db.execute('CREATE TABLE bank (user_id INTEGER, dinars INTEGER)')
db.execute('CREATE TABLE texts ( id SERIAL PRIMARY KEY, text_rus TEXT, text_eng TEXT, text_german TEXT, text_french TEXT, text_spanish TEXT, eng_description TEXT)')
db.execute('CREATE TABLE buttons(id SERIAL PRIMARY KEY, name_rus TEXT, name_eng TEXT, name_german TEXT, name_french TEXT, name_spanish TEXT, text_rus TEXT, text_eng TEXT, text_german TEXT, text_french TEXT, text_spanish TEXT, parent_id INTEGER, calldata INTEGER)')
db.execute('CREATE TABLE queue(id SERIAL PRIMARY KEY, level INTEGER, type INTEGER, player1_id INTEGER, player2_id INTEGER)')
db.execute('CREATE TABLE fights(id SERIAL PRIMARY KEY,fighter1_id INTEGER, fighter2_id INTEGER ,f1_health INTEGER ,f2_health INTEGER, f1_exp INTEGER ,f2_exp INTEGER ,last_turn INTEGER ,last_by INTEGER)')