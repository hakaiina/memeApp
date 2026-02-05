import sqlite3
from config import DB_PATH


def connect_db():
    return sqlite3.connect(DB_PATH)


def init_db():
    conn = connect_db()
    cursor = conn.cursor()

    #users
    cursor.execute("""
                   CREATE TABLE IF NOT EXISTS users
                   (
                       id
                       INTEGER
                       PRIMARY
                       KEY
                       AUTOINCREMENT,
                       nickname
                       TEXT
                       NOT
                       NULL
                       UNIQUE,
                       best_score
                       INTEGER
                       NOT
                       NULL
                       DEFAULT
                       0,
                       created_at
                       TEXT
                       NOT
                       NULL
                       DEFAULT
                       CURRENT_TIMESTAMP
                   )
                   """)

    # questions
    cursor.execute("""
                   CREATE TABLE IF NOT EXISTS questions
                   (
                       id
                       INTEGER
                       PRIMARY
                       KEY
                       AUTOINCREMENT,
                       question
                       TEXT
                       NOT
                       NULL,
                       image_path
                       TEXT,
                       option_a
                       TEXT
                       NOT
                       NULL,
                       option_b
                       TEXT
                       NOT
                       NULL,
                       option_c
                       TEXT
                       NOT
                       NULL,
                       option_d
                       TEXT
                       NOT
                       NULL,
                       correct_option
                       TEXT
                       NOT
                       NULL
                       CHECK (
                       correct_option
                       IN
                   (
                       'A',
                       'B',
                       'C',
                       'D'
                   )
                       )
                       )
                   """)

    conn.commit()
    conn.close()


def get_or_create_user(nickname):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("INSERT OR IGNORE INTO users (nickname) VALUES (?)", (nickname,))

    cursor.execute("SELECT id, nickname, best_score FROM users WHERE nickname = ?", (nickname,))

    user = cursor.fetchone()
    conn.close()
    return user


#testing data
def seed_test_data():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(""
                   "INSERT OR IGNORE INTO users (nickname, best_score) VALUES (?, ?)",
                   ('best teamlead', 50))
    conn.commit()
    conn.close()