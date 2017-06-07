import postgresql as pg

db = pg.open(user='postgres', host='localhost', port='5432', password='123456', database='postgres')


''''id, text_rus, text_eng, text_german, text_french, text_spanish, eng_description'''''

insert_text = db.prepare('INSERT INTO texts(text_rus, text_eng, text_german, text_french, text_spanish,'
                         ' eng_description) VALUES ($1, $2, $3, $4, $5, $6)')
get_text = db.prepare('SELECT * FROM texts WHERE id = $1')

languages_ = {
    'Русский':0,
    'English':1,
    'Deutsche':2,
    'Français':3,
    'Espanol':4,
}



def get_text_(id_, lang):
    if int(lang) > 5:
        raise Exception('Value Error')
    # print('text = ', get_text(id_)[0][lang+1])
    data = get_text(id_)
    return data[0][lang+1]


