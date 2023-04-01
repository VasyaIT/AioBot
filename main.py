import asyncio
import random
import sqlite3
import time
import hashlib
import aioschedule
import schedule as schedule

from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from random import choice

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup

from config import API_TOKEN, CAPTION
from markups import *


storage = MemoryStorage()
bot = Bot(API_TOKEN, parse_mode='HTML')
dp = Dispatcher(bot, storage=storage)


async def on_startup(_):
    print('Бот запущен')


HELP_TEXT = """
<b>/rate</b> - <em>Пооценивать фотки</em>
<b>/test</b> - <em>Пройти тест на IQ</em>
"""




@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    # conn = sqlite3.connect('db.sqlite3')
    # cur = conn.cursor()
    # cur.execute('CREATE TABLE IF NOT EXISTS users '
    #             '(id integer not null unique, '
    #             'user_id integer not null unique,'
    #             'name varchar(50) not null,'
    #             'PRIMARY KEY(id autoincrement))')
    # conn.commit()
    # cur.close()
    # conn.close()

    id_chat = message.chat.id
    first_name = message.from_user.first_name
    await message.answer(f'Привет, <b>{message.from_user.first_name}!👋</b>\n\n'
                         f'Этого бота создал - @Solevaaaya - топ 2 БО России на минутучку <em>(да-да, 35 ранг)</em>\n\n'
                         f'Этот бот умеет работать с базой данных\n'
                         f'Чтобы увидеть все команды нажми - /help',
                         reply_markup=markup_start)

    conn = sqlite3.connect('db.sqlite3')
    cur = conn.cursor()
    cur.execute('INSERT OR IGNORE INTO users (user_id, name) VALUES ("%s", "%s")' % (id_chat, first_name))
    conn.commit()
    cur.close()
    conn.close()


@dp.message_handler(commands=['help'])
async def help_comm(message: types.Message):
    await message.answer(HELP_TEXT)


@dp.message_handler(commands=['rate'])
async def rate_photo(message: types.Message):
    photo = choice(list(CAPTION.keys()))
    await message.answer_photo(photo, reply_markup=markup_photo, caption=CAPTION[photo])


# class ClientStatesGroup(StatesGroup):
#     question = State()
#     question2 = State()


@dp.message_handler(commands=['test'])
async def test_cmd(message: types.Message):
    await message.answer('Тест на IQ🧐', reply_markup=markup_test)


async def test_done(message: types.Message):
    time.sleep(2)
    await message.answer('Итак, подводим итоги...')
    time.sleep(4)
    await message.answer('<em>Сбор данных...</em>')
    time.sleep(3)
    await message.answer('<em>Загрузка...</em>')
    time.sleep(3)
    await message.answer(f'<b>Твой IQ => {random.randint(-10, 10)}</b>\n\nПоздравлю! Отличный результат! Ты этого заслуживаешь!💪')
    time.sleep(2)
    await message.answer_sticker('CAACAgIAAxkBAAEIaAdkJ4CLyfWswB9y8O7G4QfQs8LwagACcgEAAiI3jgTwHKSRbRIvOi8E')
    time.sleep(2)
    await message.answer_sticker('CAACAgIAAxkBAAEIaAtkJ4DJLAGDPvZQvGxI272XdLruRAACsgEAAhZCawqceQABhqhR6VIvBA')
    return


@dp.callback_query_handler(lambda call: call.data == 'holdik' or call.data == 'vasyadasher' or call.data == 'mma' or call.data == 'antinub' or call.data == 'cancel')
async def callback_q1(call: types.CallbackQuery, state: FSMContext):
    if call.data == 'vasyadasher':
        await call.message.edit_text('Красава, бро! Конечно же VasyaDasher, тут без сомнений😎\n\n'
                                     '<b>Второй вопрос:</b><em>Сколько мне лет?</em>',
                                     reply_markup=markup_test_question2)
        await call.answer()
    if call.data == 'holdik' or call.data == 'mma' or call.data == 'antinub':
        await call.message.edit_text('НЕВЕРНО!😡 Как можно не знать это!???\n\n'
                                     '<b>Второй вопрос:</b><em>Сколько мне лет?</em>',
                                     reply_markup=markup_test_question2)
        await call.answer()
    if call.data == 'cancel':
        await call.message.delete()
        await bot.delete_message(call.message.chat.id, call.message.message_id - 1)
    await call.answer('Отменено')


@dp.callback_query_handler(lambda call: call.data == '20' or call.data == '87' or call.data == '148' or call.data == '16')
async def callback_q2(call: types.CallbackQuery):
    if call.data == '16':
        await call.message.edit_text('Уоу Уоу! Это верно!🥳 Хотя ты почти ошибся')
        await call.answer()
        await test_done(call.message)
    else:
        await call.message.edit_text('Эхх, к сожалению, это не правильно\nНо ты был близок😉')
        await call.answer()
        await test_done(call.message)


@dp.callback_query_handler(lambda call: call.data == 'dislike' or call.data == 'like')
async def callback_rate(call: types.CallbackQuery):
    if call.data == 'like':
        await rate_photo(call.message)
        await call.answer()
    if call.data == 'dislike':
        await rate_photo(call.message)
        await call.answer()


@dp.callback_query_handler(lambda call: call.data == 'go')
async def callback_test_start(call: types.CallbackQuery):
    await call.message.edit_text('<b>Первый вопрос:</b>\n\n<em>Кто лучший БО мира в 2022 году?</em>',
                                 reply_markup=markup_test_question)


@dp.message_handler(content_types='text')
async def text_cmd(message: types.Message):
    if message.text == 'Все команды':
        await help_comm(message)
    elif message.text == 'Заценить фотки':
        await rate_photo(message)


@dp.inline_handler()
async def inline_answer(inline: types.InlineQuery) -> None:
    text = inline.query or 'echo'
    input_content = types.InputTextMessageContent(text)
    result_id: str = hashlib.md5(text.encode()).hexdigest()
    item = types.InlineQueryResultArticle(
        input_message_content=input_content,
        id=result_id,
        title=text
    )

    await bot.answer_inline_query(inline_query_id=inline.id, results=[item], cache_time=1)

if __name__ == "__main__":
    executor.start_polling(dp, on_startup=on_startup, skip_updates=True)
