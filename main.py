from aiogram import Bot, Dispatcher, executor, types
import os
from dotenv import load_dotenv

from random import choice

from markups import *

load_dotenv()

bot = Bot(os.getenv('API_TOKEN'), parse_mode='HTML')
dp = Dispatcher(bot)


async def on_startup(_):
    print('Бот запущен')


HELP_TEXT = """
<b>/rate</b> - <em>Пооценивать фотки</em>
"""

PHOTOS = ['https://shutniks.com/wp-content/uploads/2020/01/devushka_s_kameroy_14_13035223.jpg',
          'https://www.sostav.ru/blogs/images/feeds/17/32441.jpg',
          'https://klike.net/uploads/posts/2022-09/1663154659_g-9.jpg',
          'https://microsac.es/wp-content/uploads/2019/06/8V1z7D_t20_YX6vKm.jpg',
          'https://www.blackpantera.ru/upload/iblock/b0e/Znachenie-imeni-Aslan.jpg',
          'https://mysekret.ru/wp-content/uploads/2022/01/reinhart-julian-wxm465om4j4-unsplash.jpg',
          'https://myfreesoft.ru/wp-content/uploads/2019/03/prephoto1.jpg',
          'https://api.innogest.ru/sites/default/files/news/images/179246821_1450.jpg',
          'https://mykaleidoscope.ru/x/uploads/posts/2022-09/1663131459_22-mykaleidoscope-ru-p-veselie-druzya-krasivo-24.jpg',
          'https://sun9-60.userapi.com/s/v1/if2/QQOSnilTIj128JGeAEtw1wq2L1bhMadQuSr2pf0Nks8Ov1NzTB-l31FXnOam-CxWOVThUW72mfgKyrCxd8FXdOZ_.jpg?size=1280x853&quality=95&type=album',
          'https://paypress.ru/uploads/2020/08/1598242178-blonde-629726-1920.jpeg',
          'https://android-obzor.com/wp-content/uploads/2022/03/chto-nuzhno-znat-pro-introverta-yesli-on-vash-partner_1-1.jpg',
          'https://cdn.fishki.net/upload/post/201408/25/1297423/20.jpg',
          'https://vsegda-pomnim.com/uploads/posts/2022-04/1649126083_20-vsegda-pomnim-com-p-samie-krasivie-peizazhi-prirodi-foto-23.jpg',
          'https://yobte.ru/uploads/posts/2019-11/avstralijki-61-foto-25.jpg',
          'https://boliviamia.net/Images/ArticlePhotos/Bolivia-experiencias-imperdibles-02.jpg']


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.answer(f'Привет, <b>{message.from_user.first_name}!👋</b>\n\n'
                         f'Этого бота создал - @Solevaaaya - топ 2 БО России на минутучку <em>(да-да, 35 ранг)</em>\n\n'
                         f'Этот бот умеет работать с базой данных\n'
                         f'Чтобы увидеть все команды нажми - /help',
                         reply_markup=markup_start)


@dp.message_handler(commands=['help'])
async def help_comm(message: types.Message):
    await message.answer(HELP_TEXT)


@dp.message_handler(commands=['rate'])
async def rate_photo(message: types.Message):
    await message.answer_photo(choice(PHOTOS), reply_markup=markup_photo)


@dp.callback_query_handler(lambda call: types.CallbackQuery)
async def callback(call):
    if call.data == 'like':
        await rate_photo(call.message)
    elif call.data == 'dislike':
        await rate_photo(call.message)


@dp.message_handler(content_types='text')
async def text(message: types.Message):
    if message.text == 'Все команды':
        await help_comm(message)
    elif message.text == 'Заценить фотки':
        await rate_photo(message)


if __name__ == "__main__":
    executor.start_polling(dp, on_startup=on_startup, skip_updates=True)
