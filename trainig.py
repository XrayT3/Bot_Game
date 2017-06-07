import postgresql as pg
import time

db = pg.open(user='postgres', host='localhost', port='5432', password='123456', database='postgres')



def training(pl, time_selected=None, power=None, adroitness=None, health=None, armor=None):
    print('smth')
    if not pl:
        return False
    if time.time() < (pl.next_training if pl.next_training else 0):
        return -1
    if power:
        set = 'power'
        num = power + pl.power
    elif adroitness:
        set = 'adroitness'
        num = adroitness + pl.adroitness
    elif health:
        set = 'health'
        num = health + pl.health
    else:
        set = 'armor'
        num = armor + pl.armor

    exe = db.prepare('UPDATE users SET {param} = $1 WHERE user_id = $2'.format(param=str(set)))
    exe(num, pl.user_id)
    exe = db.prepare('UPDATE users SET next_training = $1 WHERE user_id = $2')
    exe(int(time.time()+time_selected*3600), pl.user_id)
    return 0
