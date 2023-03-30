from aiogram.types import \
    ReplyKeyboardMarkup, \
    ReplyKeyboardRemove, \
    KeyboardButton, \
    InlineKeyboardMarkup, \
    InlineKeyboardButton


markup_start = ReplyKeyboardMarkup(resize_keyboard=True)
but_help = KeyboardButton("Все команды")
but_photo = KeyboardButton("Заценить фотки")
markup_start.add(but_photo, but_help, )


markup_photo = InlineKeyboardMarkup(row_width=2)
bt1 = InlineKeyboardButton('👍', callback_data='like')
bt2 = InlineKeyboardButton('👎', callback_data='dislike')
bt3 = InlineKeyboardButton('💌', url='t.me/iBekZzZ')
markup_photo.row(bt1, bt3, bt2)
