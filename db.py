import sqlite3
import pandas as pd


conn = sqlite3.connect('db_profile.sqlite3')
cur = conn.cursor()

sql_photo = """
    SELECT photo
    FROM profile
"""
photos = pd.read_sql(sql_photo, conn)

sql_captions = """
    SELECT description
    FROM profile
"""
captions = pd.read_sql(sql_captions, conn)

photos_list = photos['photo'].tolist()
captions_list = captions['description'].tolist()

PHOTOS = dict(zip(photos_list, captions_list))

conn.commit()
cur.close()
conn.close()


async def create_user(id_chat, username, first_name):
    conn = sqlite3.connect('db.sqlite3')
    cur = conn.cursor()
    # cursor.execute('CREATE TABLE IF NOT EXISTS users '
    #             '(id INTEGER NOT NULL UNIQUE, '
    #             'user_id INTEGER NOT NULL UNIQUE,'
    #             'username,'
    #             'name,'
    #             'PRIMARY KEY(id autoincrement))')
    # connect.commit()

    user_id = cur.execute(f"SELECT 1 FROM users WHERE user_id == '{id_chat}'").fetchone()
    if not user_id:
        cur.execute('INSERT INTO users (user_id, username, name) VALUES ("%s", "%s", "%s")' % (id_chat, username, first_name))
    conn.commit()
    cur.close()
    conn.close()


async def create_update_profile(message, data):
    user_id = message.from_user.id
    username = message.from_user.username
    photo = data['photo']
    description = data['desc']

    conn = sqlite3.connect('db_profile.sqlite3')
    cur = conn.cursor()
    # cur.execute('CREATE TABLE IF NOT EXISTS profile'
    #             '(id INTEGER NOT NULL UNIQUE, '
    #             'user_id INTEGER NOT NULL UNIQUE,'
    #             'username, '
    #             'photo TEXT,'
    #             'description TEXT,'
    #             'PRIMARY KEY(id autoincrement))')
    # conn.commit()

    us_id = cur.execute(f"SELECT 1 FROM profile WHERE user_id == '{user_id}'").fetchone()
    if not us_id:
        cur.execute('INSERT INTO profile (user_id, username, photo, description) '
                    'VALUES ("%s", "%s", "%s", "%s")' % (user_id, username, photo, description))
    else:
        cur.execute("UPDATE profile SET photo = '{}', description = '{}'"
                    "WHERE user_id == '{}'".format(photo, description, user_id))
    conn.commit()
    cur.close()
    conn.close()


async def delete_form(user_id):
    conn = sqlite3.connect('db_profile.sqlite3')
    cur = conn.cursor()
    cur.execute(f"DELETE FROM profile WHERE user_id == '{user_id}'")
    conn.commit()
    cur.close()
    conn.close()
