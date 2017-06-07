import postgresql as pg

db = pg.open(user='postgres', host='localhost', port='4077', password='89/b/3?!MK', database='postgres')

data = db.prepare("SELECT table_name, column_name, column_type FROM information_schema.columns WHERE table_schema='public'")()

for i in range(len(data)):
    if i==0:
        print(data[i][0])
        print('-----',data[i][1])
    elif data[i][0]==data[i-1][0]:
        print('-----',data[i][1])
    else:
        print()
        print(data[i][0])
        print('-----',data[i][1])

# db.execute('DELETE FROM fights')
print(db.prepare('SELECT * FROM users')())
# db.execute("UPDATE texts SET text_rus ='Уклоняйся лучше! Вы получили' WHERE id=52")
exe = db.prepare('INSERT INTO buttons(name_rus, name_eng, name_german, name_french, name_spanish, text_rus, text_eng, text_german, text_french, text_spanish,parent_id,calldata) VALUES ($1, $2, $3,$4, $5,$6, $7,$8,$9,$10,$11, $12)')
# db.execute('UPDATE buttons SET id = id-14 WHERE id>49')
db.execute('UPDATE users SET dinars = 10000')
# db.execute('ALTER TABLE fights ADD COLUMN last_by INTEGER')
# 15 16 17 ban-list
# db.execute('CREATE TABLE news_table(text TEXT, interval INTEGER)')