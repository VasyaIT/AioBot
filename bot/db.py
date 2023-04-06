import sqlite3
import pandas as pd

from markups import get_markup_photo


async def get_photos(message, choice, aiogram):
    conn = sqlite3.connect('db.sqlite3')
    cur = conn.cursor()

    sql_photo = """
        SELECT photo, description, username 
        FROM users
    """
    photos = pd.read_sql(sql_photo, conn)

    photos_list = photos['photo'].tolist()
    captions_list = photos['description'].tolist()
    usernames_list = photos['username'].tolist()

    conn.commit()
    cur.close()
    conn.close()

    PHOTOS = list(zip(photos_list, captions_list, usernames_list))
    photos = choice(PHOTOS)
    try:
        await message.answer_photo(photos[0], reply_markup=get_markup_photo(photos), caption=photos[1])
    except aiogram.utils.exceptions.BadRequest:
        return


async def create_user(id_chat, username, first_name):
    conn = sqlite3.connect('db.sqlite3')
    cur = conn.cursor()
    cur.execute('CREATE TABLE IF NOT EXISTS users'
                '(id INTEGER NOT NULL UNIQUE,'
                'user_id INTEGER NOT NULL UNIQUE,'
                'username DEFAULT "none",'
                'name,'
                'photo TEXT DEFAULT "none",'
                'description TEXT DEFAULT "none",'
                'PRIMARY KEY(id autoincrement))')
    conn.commit()

    user_id = cur.execute(f"SELECT 1 FROM users WHERE user_id == '{id_chat}'").fetchone()
    if not user_id:
        cur.execute('INSERT INTO users (user_id, username, name) VALUES ("%s", "%s", "%s")' % (id_chat, username, first_name))
    conn.commit()
    cur.close()
    conn.close()


async def create_update_profile(message, data):
    user_id = message.from_user.id
    photo = data['photo']
    description = data['desc']

    conn = sqlite3.connect('db.sqlite3')
    cur = conn.cursor()
    cur.execute(f"UPDATE users SET photo = '{photo}', description = '{description}'"
                f"WHERE user_id == '{user_id}'")
    conn.commit()
    cur.close()
    conn.close()


async def delete_form(user_id):
    conn = sqlite3.connect('db.sqlite3')
    cur = conn.cursor()
    cur.execute(f"UPDATE users SET photo = 'none', description = 'none'"
                f"WHERE user_id == '{user_id}'")
    conn.commit()
    cur.close()
    conn.close()
