import sqlite3
from config import DB_PATH


class Database:
    def __init__(self):
        self.conn = None
        self.init_db()

    def connect(self):
        self.conn = sqlite3.connect(DB_PATH)
        return self.conn

    def close(self):
        if self.conn:
            self.conn.close()

    def init_db(self):
        conn = self.connect()
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
                           password TEXT
                           NOT NULL,
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
        conn.commit()
        conn.close()


    # registration
    def add_user(self, nickname, password):
        try:
            conn = self.connect()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT OR IGNORE INTO users (nickname, password) VALUES (?, ?)",
                (nickname, password)
            )
            return True
        except Exception:
            return False

    #testing data
    # def seed_test_data():
    #     conn = connect_db()
    #     cursor = conn.cursor()
    #     cursor.execute(""
    #                    "INSERT OR IGNORE INTO users (nickname, password, best_score) VALUES (?, ?, ?)",
    #                    ('best teamlead', '12345', 50))
    #     conn.commit()
    #     conn.close()