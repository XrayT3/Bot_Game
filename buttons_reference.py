import classes, base

buttons = [None]


def get_but(id_):
    exe = base.get_button
    but = classes.Button(args=list(exe(id_)[0]))
    return but


def get_description(id_, lang):
    print('lang = ', lang)
    try:
        but = buttons[id_]
        if but.get_text(lang):
            return but.get_text(lang)
        if not but.parent:
            return None
        while not but.parent.get_text(lang):
            but = but.parent
        return but.parent.get_text(lang)
    except Exception as e:
        print("Exception = ", e)


def get_buttons():
    print('Loading buttons...')
    global buttons
    buttons = [None]
    data = base.get_data('buttons')
    # print('data = ',data)
    for but in data:
        # print(but)
        new_button = classes.Button()
        new_button.id = but[0]
        new_button.name_rus = but[1]
        new_button.name_eng = but[2]
        new_button.name_german = but[3]
        new_button.name_french = but[4]
        new_button.name_spanish = but[5]
        new_button.text_rus = but[6]
        new_button.text_eng = but[7]
        new_button.text_german = but[8]
        new_button.text_french = but[9]
        new_button.text_spanish = but[10]
        new_button.parent_id = int(but[11])
        new_button.call = but[12]
        buttons.append(new_button)
    for but in buttons[1:]:
        if but.parent_id != 0:
            but.parent = buttons[int(but.parent_id)]
    # print('len buttons = l', len(buttons)-1)
    return buttons