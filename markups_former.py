import actions
import telebot
import buttons_reference, classes
import texts

buttons = buttons_reference.get_buttons()
main_but = classes.Button()
main_but.parent_id = None
main_but.id = 0

# me_todo fill documentation


def main_markup_dict(lang):
    return {
        texts.get_text_(58, lang):1, texts.get_text_(59, lang):2, texts.get_text_(60, lang):3,
        texts.get_text_(61, lang):4, texts.get_text_(62, lang):5, texts.get_text_(63, lang):6,
    }


def get_action(id_):
    but_ = buttons[id_]
    if but_.action_id:
        return but_.action_id
    if not but_.parent:
        return None
    while not but_.parent.action_id:
        but_ = but_.parent
    return but_.parent.action_id


def get_inline_markup(width, length, *args):
    markup = telebot.types.InlineKeyboardMarkup(row_width=width)
    args_iterator = 0
    buts = []
    for i in range(length):
        buts.append(telebot.types.InlineKeyboardButton(args[args_iterator], callback_data=args[args_iterator+1]))
        args_iterator += 2
    markup.add(*buts)
    return markup


def get_markup(width, length, *args):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True,row_width=width)
    buts = []
    for i in range(length):
        buts.append(telebot.types.KeyboardButton(args[i]))
    markup.add(*buts)
    return markup


# initialize Button.parents by its id
for but in buttons[1:]:
    if but.parent_id == 0:
        but.parent = main_but


def main_markup(lang):
    print('lang = ',lang)
    return get_markup(2, 6, texts.get_text_(58, lang), texts.get_text_(59, lang),texts.get_text_(60, lang),
                      texts.get_text_(61, lang), texts.get_text_(62, lang), texts.get_text_(63, lang))


def form_buttons_data(id_, language, player_):
    print('id_ = ', id_)
    global buttons
    # making an array of daughter buttons
    mas = []
    # print(id_, [but_.parent_id for but_ in buttons[1:]])
    for button in buttons[1:]:
        if button.parent_id == id_:
            mas.append(button.get_name(language))
            mas.append(str(button.call))
    if buttons[id_].is_buy_but:
        return get_inline_markup(1, 2, texts.get_text_(32, language), 'b' + str(buttons[id_].item),
                                 texts.get_text_(57, language), str(buttons[id_].parent_id))
    # Error catchers
    if len(mas) == 0:
        # something
        return get_inline_markup(1, 1, texts.get_text_(57, language), str(buttons[id_].parent_id))
    if id_ == -1:
        # something
        return None
    print('-----', mas)
    return mas

'''Получаем на вход id нажатой кнопки и объект игрока, делаем загрузку всех временных кнопок,
 если к кнопке\отцовской кнопке приписано действие и оно есть в массиве действий,
  то выполняем его ловим и обрабатываем выходной сигнал, если он 0 - изменился текст, меняем текст в parent_but,
  если 1, то кнопка финальная,(и поиск по родительским кнопкам не проводится,
  если присутствует action, и срабатывает вылет на form_b_data) выводим только back

'''


def form_buttons(id_, language, player_):
    global buttons
    print('id- = ', id_, language)
    buttons_reference.buttons = buttons_reference.get_buttons()
    actions.load_buttons()
    actions.wardrobe(language, player_)
    buttons = buttons_reference.buttons
    mas = []
    if actions.actions_[id_]:
        res = actions.actions_[id_].execute(language, player_)
        # update buttons after executing of action
        buttons = buttons_reference.buttons
        # handle output signals
        if res == 1:
            mas = form_buttons_data(id_, language, player_)
            if actions.actions_[id_].text:
                buttons_reference.buttons[id_].text_rus = actions.actions_[id_].text
                buttons[id_].text_rus = actions.actions_[id_].text
                if type(mas) == telebot.types.InlineKeyboardMarkup:
                    return mas
                return get_inline_markup(2, int(len(mas) / 2), *mas)
        elif res == 0:
            buttons_reference.buttons[id_].text_rus = actions.actions_[id_].text
            buttons[id_].text_rus = actions.actions_[id_].text
            mas = form_buttons_data(id_, language,player_)
        elif res == -1:
            mas = form_buttons_data(id_, language,player_)
    else:
        mas = form_buttons_data(id_, language,player_)
    if type(mas) == telebot.types.InlineKeyboardMarkup:
        return mas

    # default markup builder
    if len(mas) != 0:
        if buttons[id_].parent_id == 0 or not buttons[id_].parent_id:
            return get_inline_markup(2, int(len(mas) / 2), *mas)
        else:
            return get_inline_markup(2, int(len(mas) / 2), *mas).row(telebot.types.InlineKeyboardButton(text=texts.get_text_(57, language), callback_data=str(buttons[id_].parent_id)))
    else:
        return get_inline_markup(1, 1, texts.get_text_(57, language), str(buttons[id_].parent_id))