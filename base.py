import postgresql as sql
import classes

db = pg.open(user='postgres', host='localhost', port='5432', password='123456', database='postgres')


get_button = db.prepare('SELECT * FROM buttons WHERE id = $1')

insert_player = db.prepare("INSERT INTO users(user_id, name, level, fights, wins,"
                           " small, medium, big, commercial, guarantees, invited, power, adroitness, armor, health,"
                           "add_power, add_adroitness, add_armor, add_health,"
                           " inventory, equipped, next_training, language, dinars) "
                           "VALUES($1, $2, $3, $4, $5, $6, $7, $8, $9,"
                           "$10, $11, $12, $13, $14, $15, $16, $17, $18, $19, $20, $21, $22, $23, $24)")

get_item = db.prepare('SELECT * FROM items WHERE id = $1')

update_inventory = db.prepare("UPDATE users SET inventory = $1 WHERE user_id = $2")

update_equipped = db.prepare("UPDATE users SET equipped = $1 WHERE user_id = $2")

update_dinars = db.prepare("UPDATE users SET dinars = $1 WHERE user_id = $2")

set_bank_account = db.prepare('INSERT INTO bank(user_id, dinars) VALUES ($1, $2)')

update_bank_dinars = db.prepare('UPDATE bank SET dinars = $1 WHERE user_id = $2')

change_turn1 = db.prepare('SELECT * FROM fights WHERE last_by = fighter1_id AND $1 - last_turn >15')

change_turn2= db.prepare('SELECT * FROM fights WHERE last_by = fighter2_id AND $1 - last_turn >15')

delete_bank_account = db.prepare('DELETE FROM bank WHERE user_id = $1')

update_language = db.prepare('UPDATE users SET language = $1 WHERE id = $2')

update_plus_scores = db.prepare('UPDATE users SET scores = scores + $1 WHERE user_id = $2')

update_level = db.prepare('UPDATE users SET level = $1 WHERE user_id = $2')

get_user_data = db.prepare("SELECT * FROM users WHERE user_id = $1")

get_bank_account = db.prepare('SELECT * FROM bank WHERE user_id = $1')

update_add_power = db.prepare('UPDATE users SET add_power = $1 WHERE user_id = $2')
update_add_armor = db.prepare('UPDATE users SET add_armor = $1 WHERE user_id = $2')
update_add_health = db.prepare('UPDATE users SET add_health = $1 WHERE user_id = $2')
update_add_adroitness = db.prepare('UPDATE users SET add_adroitness = $1 WHERE user_id = $2')
update_plus_coins = db.prepare('UPDATE users SET dinars = $1 WHERE user_id = $2')
increment_invited = db.prepare('UPDATE users SET invited = invited + 1 WHERE user_id = $1')
get_inventory = db.prepare("SELECT inventory FROM users WHERE user_id = $1")

update_dinars = db.prepare("UPDATE users SET dinars = $1 WHERE id = $2")

get_user_id = db.prepare('SELECT * FROM news_table')

get_daily_news = db.prapare('SELECT * FROM news_table')


def get_all_user_id():
    data = get_user_id()
    # print(data)
    return [i[0] for i in data]


def replace(erase, insert, args):
    try:
        i = args.index(erase)
        args.remove(erase)
        args.insert(i,insert)
        return 0
    except KeyError:
        return -1


def get_data(table_name):
    data = None
    try:
        get_lines = db.prepare('SELECT * FROM {table_name}'.format(table_name=table_name))
        data = get_lines()
    except Exception as e:
        print(e)
    data.sort(key=lambda tup: tup[0])
    return data












