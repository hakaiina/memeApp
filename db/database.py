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

            conn.commit()

            if cursor.rowcount > 0:
                print(f"Пользователь {nickname} успешно добавлен")
                return True
            else:
                print(f"Пользователь {nickname} уже существует")
                return False
        except Exception as e:
            print(f"Ошибка при добавлении пользователя: {e}")
            if conn:
                conn.rollback()
            return False
        finally:
            if conn:
                conn.close()

    # get user best score for main window
    def get_user_score(self, nickname):
        best_score = 0
        conn = None
        try:
            conn = self.connect()
            cursor = conn.cursor()
            cursor.execute(
                "SELECT best_score FROM users WHERE nickname = ?",
                (nickname,)
            )

            result = cursor.fetchone()

            if result is not None:
                best_score = result[0] if result[0] is not None else 0
            else:
                print(f"Пользователь {nickname} не найден")
                return None

        except Exception as e:
            print(f"Ошибка при запросе данных пользователя: {e}")
            return None

        finally:
            if conn:
                conn.close()

        return best_score

    #testing data
    # def seed_test_data():
    #     conn = connect_db()
    #     cursor = conn.cursor()
    #     cursor.execute(""
    #                    "INSERT OR IGNORE INTO users (nickname, password, best_score) VALUES (?, ?, ?)",
    #                    ('best teamlead', '12345', 50))
    #     conn.commit()
    #     conn.close()