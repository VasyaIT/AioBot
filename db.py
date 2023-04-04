import sqlite3
import pandas as pd


conn = sqlite3.connect('db.sqlite3')
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

sql_usernames = """
    SELECT username
    FROM users
"""

usernames = pd.read_sql(sql_usernames, conn)

photos_list = photos['photo'].tolist()
captions_list = captions['description'].tolist()
usernames_list = usernames['username'].tolist()

USERNAMES = list(zip(captions_list, usernames_list))
PHOTOS = dict(zip(photos_list, USERNAMES))

conn.commit()
cur.close()
conn.close()


async def create_user(id_chat, username, first_name):
    conn = sqlite3.connect('db.sqlite3')
    cur = conn.cursor()
    # cur.execute('CREATE TABLE IF NOT EXISTS users'
    #             '(id INTEGER NOT NULL UNIQUE,'
    #             'user_id INTEGER NOT NULL UNIQUE,'
    #             'username DEFAULT "none",'
    #             'name,'
    #             'PRIMARY KEY(id autoincrement)'
    #             'FOREIGN KEY (user_id) REFERENCES profile (form_id) ON DELETE CASCADE)')
    # conn.commit()

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

    us_id = cur.execute(f"SELECT profile.form_id FROM users INNER JOIN profile ON users.user_id == '{user_id}'").fetchone()
    if not us_id:
        cur.execute('INSERT INTO profile (photo, description) '
                    'VALUES ("%s", "%s")' % (photo, description))
    else:
        cur.execute(f"UPDATE profile SET photo = '{photo}', description = '{description}'"
                    f"WHERE form_id == '{int(*us_id)}'")
    conn.commit()
    cur.close()
    conn.close()


async def delete_form(user_id):
    conn = sqlite3.connect('db.sqlite3')
    cur = conn.cursor()
    us_id = cur.execute(
        f"SELECT profile.form_id FROM users INNER JOIN profile ON users.user_id == '{user_id}'").fetchone()
    cur.execute(f"DELETE FROM profile WHERE form_id == '{int(*us_id)}'")
    conn.commit()
    cur.close()
    conn.close()
