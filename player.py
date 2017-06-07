import postgresql as pg
import classes, base
db = pg.open(user='postgres', host='localhost', port='5432', password='123456', database='postgres')



def get_item(id):
    exe = db.prepare("SELECT * FROM items WHERE id = $1")
    data = exe(id)
    data = data[-1]
    return data


def default_set():
    return '/////'


def form_default_player(message):
    base.insert_player(message.from_user.id, message.from_user.first_name, 1, 0, 0, 1000, 1000, 1000, 0, 0, 0, 0, 0, 0, 10, 10,
                  10, 10, 0, 0, 0, 0, default_set(), default_set(), None, None)
    base.set_bank_account(message.from_user.id, 0)


def check_new_user(user_id, message):
    exe = db.prepare('SELECT * FROM users WHERE user_id = $1')
    if not exe(int(user_id)):
            form_default_player(message)
            return -1
    else:
        return 0


def authorize(user_id, message=None):
    check_new_user(user_id, message if message else None)
    data = db.prepare("SELECT * FROM users WHERE user_id = $1")
    if not base.get_bank_account(user_id):
        base.set_bank_account(user_id, 0)

    return classes.Player(*data(user_id))


