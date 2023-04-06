import asyncio
import random
import sqlite3
import time
import hashlib

import aiogram.utils.exceptions
import aioschedule
import schedule as schedule

from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from random import choice

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.types import InputMedia, InputMediaPhoto

# from middlewares import ThrottlingMiddleware
from config import API_TOKEN
from markups import *
from db import create_update_profile, create_user, delete_form, get_photos

storage = MemoryStorage()
bot = Bot(API_TOKEN, parse_mode='HTML')
dp = Dispatcher(bot, storage=storage)


async def on_startup(_):
    print('Бот запущен')


HELP_TEXT = """
<b>/rate</b> - <em>Пооценивать фотки</em>
<b>/test</b> - <em>Пройти тест на IQ</em>
"""


# 305605867	Anton
@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    id_chat = message.from_user.id
    username = message.from_user.username
    first_name = message.from_user.first_name
    await message.answer(f'Привет, <b>{message.from_user.first_name}!👋</b>\n\n'
                         # f'Этого бота создал - @Solevaaaya - топ 2 БО России на минутучку <em>(да-да, 
                         # 35 ранг)</em>\n\n # f'Этот бот умеет работать с базой данных\n'
                         f'Чтобы увидеть все команды нажми - /help',
                         reply_markup=markup_start)

    await create_user(id_chat, username, first_name)


@dp.message_handler(Text(equals=['Все команды 💬', '/help']))
async def help_comm(message: types.Message):
    await message.answer(HELP_TEXT)


@dp.message_handler(Text(equals=['Заценить фотки 👀', '/rate']))
async def rate_photo(message: types.Message):
    await get_photos(message, choice, aiogram)



# Тест
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
    await message.answer(
        f'<b>Твой IQ => {random.randint(-10, 10)}</b>\n\nПоздравлю! Отличный результат! Ты этого заслуживаешь!💪')
    time.sleep(2)
    await message.answer_sticker('CAACAgIAAxkBAAEIaAdkJ4CLyfWswB9y8O7G4QfQs8LwagACcgEAAiI3jgTwHKSRbRIvOi8E')
    time.sleep(2)
    await message.answer_sticker('CAACAgIAAxkBAAEIaAtkJ4DJLAGDPvZQvGxI272XdLruRAACsgEAAhZCawqceQABhqhR6VIvBA')
    return


# Добалвение анкеты
class ClientStatesGroup(StatesGroup):
    photo = State()
    desc = State()


@dp.message_handler(Text(equals='Отменить ↩️'), state='*')
async def cancel_form(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return None
    await message.answer('Добавление анкеты отменено', reply_markup=markup_start)
    await state.finish()


@dp.message_handler(Text(equals='Моя анкета 🦸‍♂️'), state=None)
async def my_form(message: types.Message):
    user_id = message.from_user.id
    conn = sqlite3.connect('db.sqlite3')
    cur = conn.cursor()

    form = cur.execute(f"SELECT photo, description FROM users WHERE user_id == '{user_id}'").fetchone()
    if form[0] == 'none':
        await ClientStatesGroup.photo.set()
        await message.answer('<b>На данный момент, у тебя нет анкеты</b>\n\nДавай же создадим её 🤑')
        time.sleep(1)
        await add_form(message)
        return
    else:
        await message.answer_photo(photo=form[0], caption=form[1], reply_markup=markup_ud_form)
    conn.commit()
    cur.close()
    conn.close()


async def add_form(message: types.Message):
    await message.answer('<b>Отправь фотографию</b>\n<i>Её будут видеть другие пользователи</i>\n\n<em>'
                         'Нажми "Отменить ↩️" если хочешь выйти</em>',
                         reply_markup=markup_cancel_form)


@dp.message_handler(lambda message: not message.photo, state=ClientStatesGroup.photo)
async def check_photo(message: types.Message):
    return await message.answer('Я же вроде ясно сказал, что нужно фото🤦‍♂️')


@dp.message_handler(lambda message: message.photo, content_types=['photo'], state=ClientStatesGroup.photo)
async def load_photo(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['photo'] = message.photo[0].file_id
    await ClientStatesGroup.next()
    await message.answer('<b>Фотография сохранена!✅</b>\n\nТеперь добавь небольшое описание. Оно будет отображаться'
                         'под фоткой в твоей анкете')


@dp.message_handler(lambda message: message.text, content_types=['text'], state=ClientStatesGroup.desc)
async def load_desc(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['desc'] = message.text
        await message.answer(
            '<b>Твоя анкета сохранена!✅</b>\n\nТеперь её будут видеть другие пользователи и оценивать её!',
            reply_markup=markup_start)
        await message.answer_photo(data['photo'], caption=data['desc'])

    await create_update_profile(message, data)

    await state.finish()


@dp.message_handler(Text(equals='qwerty'))
async def text(message: types.Message):
    conn = sqlite3.connect('db.sqlite3')
    cur = conn.cursor()
    users = cur.execute('SELECT user_id FROM users').fetchall()
    us = str(*users)
    for i in list(*us):
        await bot.send_message(i, 'Реклама!')
    conn.commit()
    cur.close()
    conn.close()


# Callback_handlers
@dp.callback_query_handler(lambda call: call.data == 'holdik' or call.data == 'vasyadasher' or call.data == 'mma'
                           or call.data == 'antinub'
                           or call.data == 'cancel_test')
async def callback_q1(call: types.CallbackQuery):
    if call.data == 'mma':
        await call.message.edit_text('Красава, бро! Конечно же шкаф, тут без сомнений😎\n\n'
                                     '<b>Второй вопрос:</b><em>Сколько мне лет?</em>',
                                     reply_markup=markup_test_question2)
        await call.answer()
    if call.data == 'holdik' or call.data == 'vasyadasher' or call.data == 'antinub':
        await call.message.edit_text('НЕВЕРНО!😡 Как можно не знать это!???\n\n'
                                     '<b>Второй вопрос:</b><em>Сколько мне лет?</em>',
                                     reply_markup=markup_test_question2)
        await call.answer()
    if call.data == 'cancel_test':
        await call.message.delete()
        await bot.delete_message(call.message.chat.id, call.message.message_id - 1)
    await call.answer('Отменено')


# @dp.callback_query_handler(lambda call: call.data == 'holdik' or call.data == 'vasyadasher' or call.data == 'mma' or call.data == 'antinub' or call.data == 'cancel_test')
# async def callback_q1(call: types.CallbackQuery):
#     if call.data == 'vasyadasher':
#         await call.message.edit_text('Красава, бро! Конечно же VasyaDasher, тут без сомнений😎\n\n'
#                                      '<b>Второй вопрос:</b><em>Сколько мне лет?</em>',
#                                      reply_markup=markup_test_question2)
#         await call.answer()
#     if call.data == 'holdik' or call.data == 'mma' or call.data == 'antinub':
#         await call.message.edit_text('НЕВЕРНО!😡 Как можно не знать это!???\n\n'
#                                      '<b>Второй вопрос:</b><em>Сколько мне лет?</em>',
#                                      reply_markup=markup_test_question2)
#         await call.answer()
#     if call.data == 'cancel_test':
#         await call.message.delete()
#         await bot.delete_message(call.message.chat.id, call.message.message_id - 1)
#     await call.answer('Отменено')


@dp.callback_query_handler(
    lambda call: call.data == '20' or call.data == '87' or call.data == '148' or call.data == '16')
async def callback_q2(call: types.CallbackQuery):
    if call.data == '16':
        await call.message.edit_text('Уоу Уоу! Это верно!🥳 Ты не такой безмозглый, как я думал')
        await call.answer()
        await test_done(call.message)
    else:
        await call.message.edit_text('Я же написал: не тебе, а мне! Ответ неверный!')
        await call.answer()
        await test_done(call.message)


@dp.callback_query_handler(lambda call: call.data == 'dislike' or call.data == 'like' or call.data == 'go'
                           or call.data == 'update_form' or call.data == 'delete_form'
                           or call.data == 'delete_form_done' or call.data == 'back'
                           or call.data == 'url'
                           )
async def callback_rate(call: types.CallbackQuery):
    if call.data == 'like':
        await rate_photo(call.message)
        await call.answer()
    if call.data == 'dislike':
        await rate_photo(call.message)
        await call.answer()
    if call.data == 'url':
        await call.answer('У этого пользователя нет @Имени 😢')
    if call.data == 'go':
        await call.message.edit_text('<b>Первый вопрос:</b>\n\n<em>Сколько весит калл слона?</em>',
                                     reply_markup=markup_test_question)
    if call.data == 'update_form':
        await ClientStatesGroup.photo.set()
        await add_form(call.message)
        await call.answer()
    if call.data == 'delete_form':
        await call.message.edit_caption('Ты точно хочешь удалить свою анкету?\n\n'
                                        '<em>Анкета будет удалена безвозвратно</em>',
                                        reply_markup=markup_delete_form)
        await call.answer()
    if call.data == 'delete_form_done':
        user_id = call.from_user.id
        await delete_form(user_id)
        await call.message.delete()
        await call.bot.delete_message(call.message.chat.id, call.message.message_id - 1)
        await call.answer('Анкета удалена')
    if call.data == 'back':
        conn = sqlite3.connect('db.sqlite3')
        cur = conn.cursor()

        id_user = call.from_user.id
        form = cur.execute(f"SELECT photo, description FROM users WHERE user_id == '{id_user}'").fetchone()
        if form[0] == 'none':
            await ClientStatesGroup.photo.set()
            await call.message.answer('<b>На данный момент, у тебя нет анкеты</b>\n\nДавай же создадим её 🤑')
            time.sleep(1)
            await add_form(call.message)
            return
        else:
            await call.message.edit_caption(caption=form[1], reply_markup=markup_ud_form)
        conn.commit()
        cur.close()
        conn.close()
        await call.answer()


# @dp.callback_query_handler(lambda call: call.data == 'dislike' or call.data == 'like' or call.data == 'go')
# async def callback_rate(call: types.CallbackQuery):
#     if call.data == 'like':
#         await rate_photo(call.message)
#         await call.answer()
#     if call.data == 'dislike':
#         await rate_photo(call.message)
#         await call.answer()
#     if call.data == 'go':
#         await call.message.edit_text('<b>Первый вопрос:</b>\n\n<em>Кто лучший БО мира в 2022 году?</em>',
#                                      reply_markup=markup_test_question)


# Inline mod
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
    # dp.middleware.setup(ThrottlingMiddleware())
    executor.start_polling(dp, on_startup=on_startup, skip_updates=True)
