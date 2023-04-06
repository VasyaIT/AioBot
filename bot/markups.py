from aiogram.types import \
    ReplyKeyboardMarkup, \
    ReplyKeyboardRemove, \
    KeyboardButton, \
    InlineKeyboardMarkup, \
    InlineKeyboardButton


markup_start = ReplyKeyboardMarkup(resize_keyboard=True)
but_help = KeyboardButton("Все команды 💬")
but_photo = KeyboardButton("Заценить фотки 👀")
but_form = KeyboardButton("Моя анкета 🦸‍♂️")
markup_start.row(but_photo, but_help)
markup_start.add(but_form)


def get_markup_photo(photos):
    markup_photo = InlineKeyboardMarkup(row_width=2)
    bt1 = InlineKeyboardButton('👍', callback_data='like')
    bt2 = InlineKeyboardButton('👎', callback_data='dislike')
    if photos[2] == 'none':
        bt3 = InlineKeyboardButton('💌', callback_data='url')
    else:
        bt3 = InlineKeyboardButton('💌', url=f't.me/{photos[2]}')
    markup_photo.row(bt1, bt3, bt2)
    return markup_photo


markup_test = InlineKeyboardMarkup()
b_test = InlineKeyboardButton('Пройти', callback_data='go')
markup_test.row(b_test)


markup_test_question = InlineKeyboardMarkup(row_width=2)
bq1 = InlineKeyboardButton('3', callback_data='holdik')
bq2 = InlineKeyboardButton('123', callback_data='vasyadasher')
bq3 = InlineKeyboardButton('Шкаф', callback_data='mma')
bq4 = InlineKeyboardButton('40°C', callback_data='antinub')
b_test_cancel = InlineKeyboardButton('Отмена', callback_data='cancel_test')
markup_test_question.row(bq1, bq2)
markup_test_question.row(bq3, bq4)
markup_test_question.row(b_test_cancel)


# markup_test_question = InlineKeyboardMarkup(row_width=2)
# bq1 = InlineKeyboardButton('Holdik', callback_data='holdik')
# bq2 = InlineKeyboardButton('VasyaDasher', callback_data='vasyadasher')
# bq3 = InlineKeyboardButton('MMA', callback_data='mma')
# bq4 = InlineKeyboardButton('Antinub', callback_data='antinub')
# b_test_cancel = InlineKeyboardButton('Отмена', callback_data='cancel_test')
# markup_test_question.row(bq1, bq2)
# markup_test_question.row(bq3, bq4)
# markup_test_question.row(b_test_cancel)


markup_test_question2 = InlineKeyboardMarkup(row_width=2)
bq5 = InlineKeyboardButton('20', callback_data='20')
bq6 = InlineKeyboardButton('87', callback_data='87')
bq7 = InlineKeyboardButton('16', callback_data='16')
bq8 = InlineKeyboardButton('148', callback_data='148')
markup_test_question2.row(bq5, bq6)
markup_test_question2.row(bq7, bq8)
markup_test_question2.row(b_test_cancel)


markup_cancel_form = ReplyKeyboardMarkup(resize_keyboard=True)
bcf = KeyboardButton('Отменить ↩️')
markup_cancel_form.row(bcf)


markup_ud_form = InlineKeyboardMarkup(row_width=2)
bup = InlineKeyboardButton('Изменить анкету 🔁', callback_data='update_form')
bdel = InlineKeyboardButton('Удалить анкету 🚫', callback_data='delete_form')
markup_ud_form.row(bup, bdel)


markup_delete_form = InlineKeyboardMarkup(row_width=2)
ad = InlineKeyboardButton('Удалить ❌', callback_data='delete_form_done')
back = InlineKeyboardButton('Назад', callback_data='back')
markup_delete_form.add(ad, back)
