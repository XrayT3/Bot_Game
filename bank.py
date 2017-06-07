import postgresql as pg
import texts

db = pg.open(user='postgres', host='localhost', port='5432', password='123456', database='postgres')


# db.execute('CREATE TABLE bank (id SERIAL PRIMARY KEY, user_id INTEGER, dinars INTEGER, silver INTEGER, bronze INTEGER)')


def update_money():
    db.execute('UPDATE bank SET dinars = dinars + dinars * 0.02')


def get_bank_money(player_):
    exe = db.prepare('SELECT dinars FROM bank WHERE user_id = $1')
    return exe(player_.user_id)


def withdraw(player_):
        exe = db.prepare('SELECT dinars FROM bank WHERE user_id = $1')
        exe1 = db.prepare('UPDATE bank SET dinars = 0 WHERE user_id = $1')
        exe2 = db.prepare('UPDATE users SET dinars = dinars + $1 WHERE user_id = $2')
        dinars = exe(player_.user_id)
        exe1(player_.user_id)
        exe2(dinars, player_.user_id)


def close_account(player_):
    exe = db.prepare('DELETE FROM bank WHERE user_id = $1')
    exe(player_.user_id)


def add_money(player_, money):
        exe = db.prepare('SELECT dinars FROM users WHERE user_id = $1')
        exe1 = db.prepare('UPDATE users SET dinars = dinars - $1 WHERE user_id = $2')
        exe2 = db.prepare('UPDATE bank SET dinars = dinars + $1 WHERE user_id = $2')
        if exe(player_.user_id) > money:
            exe1(player_.user_id, money)
            exe2(money, player_.user_id)
            return texts.get_text_(25, player_.language)
        else:
            return 'Not enough money'


def add_money_by_percent(player_, percent):
        print(' HERE ')
        exe = db.prepare('SELECT dinars FROM users WHERE user_id = $1')
        exe1 = db.prepare('UPDATE users SET dinars = dinars - $1 WHERE user_id = $2')
        exe2 = db.prepare('UPDATE bank SET dinars = dinars + $1 WHERE user_id = $2')
        money = exe(player_.user_id)[-1][0] * percent
        if money == 0:
            return texts.get_text_(26, player_.language)
        exe1(money, player_.user_id)
        exe2(money, player_.user_id)
        return texts.get_text_(25, player_.language) + '  ' + texts.get_text_(27, player_.language) + ' ' + str(money) + ' ' + texts.get_text_(15, player_.language)
