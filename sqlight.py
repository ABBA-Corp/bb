import sqlite3
from sqlite3 import Error


def post_sql_query(sql_query):
    with sqlite3.connect('my.db') as connection:
        cursor = connection.cursor()
        try:
            cursor.execute(sql_query)
        except Error:
            pass
        result = cursor.fetchall()
        return result


def create_tables():
    users_query = '''CREATE TABLE IF NOT EXISTS USERS
                        (user_id INTEGER PRIMARY KEY NOT NULL,
                        lang TEXT,
                        ismi TEXT);'''

    post_sql_query(users_query)


def add_table_requests():
    users_query = '''CREATE TABLE IF NOT EXISTS REQUESTS
                        (req_id INTEGER NOT NULL,
                        user_id INTEGER NOT NULL,
                        ship_id TEXT,
                        cost INTEGER);'''

    post_sql_query(users_query)


add_table_requests()


def register_user(user, lang, ism):
    user_check_query = f'SELECT * FROM USERS WHERE user_id = {user};'
    user_check_data = post_sql_query(user_check_query)
    if not user_check_data:
        insert_to_db_query = f'INSERT INTO USERS (user_id, lang, ismi) VALUES ' \
                             f'({user}, "{lang}", "{ism}");'
        post_sql_query(insert_to_db_query)
    else:
        insert_to_db_query = f'UPDATE USERS set lang = "{lang}", ismi = "{ism}" WHERE user_id={user};'
        post_sql_query(insert_to_db_query)


create_tables()


def gg(user_id):
    con = sqlite3.connect('my.db')
    cur = con.cursor()
    cur.execute(f'SELECT lang FROM USERS where user_id={int(user_id)}')
    us = cur.fetchone()
    return us


def users_id():
    con = sqlite3.connect('my.db')
    cur = con.cursor()
    cur.execute(f'SELECT user_id FROM USERS')
    us = cur.fetchone()
    return us


def get_request(user_id, req_id):
    con = sqlite3.connect('my.db')
    cur = con.cursor()
    cur.execute(f'SELECT * FROM REQUESTS where user_id={int(user_id)} and req_id={req_id}')
    us = cur.fetchone()
    return us


def register_request(user_id, req_id, ship_id, cost):
    user_check_query = f'SELECT * FROM REQUESTS WHERE req_id={int(req_id)} AND user_id={int(user_id)};'
    user_check_data = post_sql_query(user_check_query)
    if not user_check_data:
        insert_to_db_query = f'INSERT INTO REQUESTS (req_id, user_id, ship_id, cost) VALUES ' \
                             f'("{int(req_id)}", {int(user_id)}, "{ship_id}", "{cost}");'
        post_sql_query(insert_to_db_query)


def all_by_user(user_id):
    con = sqlite3.connect('my.db')
    cur = con.cursor()
    cur.execute(f'SELECT * FROM REQUESTS WHERE user_id={int(user_id)} ;')
    us = cur.fetchall()
    return us


def DELETE_requests():
    user_check_query = f'DELETE FROM REQUESTS;'
    post_sql_query(user_check_query)


def delete_request(user_id, req_id):
    delete_query = f'DELETE FROM REQUESTS WHERE req_id={int(req_id)} AND user_id={int(user_id)};'
    post_sql_query(delete_query)


def get_summa(user_id):
    con = sqlite3.connect('my.db')
    cur = con.cursor()
    cur.execute(f'SELECT cost FROM REQUESTS WHERE user_id={int(user_id)} ;')
    us = cur.fetchall()
    summa = 0
    for i in us:
        summa += int(i[0])
    return summa
