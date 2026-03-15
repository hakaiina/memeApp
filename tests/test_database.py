import pytest
import sqlite3
import os
from db.database import Database


class TestDatabase:

    def test_db_creation_on_first_start(self, monkeypatch, temp_db_path):
        """TC-DB-01: Тестирование БД при первом запуске"""
        import db.database as database

        # Убеждаемся, что файл БД действительно не существует
        assert not os.path.exists(temp_db_path), f"Файл {temp_db_path} не должен существовать до теста"

        # Патчим путь к БД
        monkeypatch.setattr(database, 'DB_PATH', temp_db_path)

        # Создаем экземпляр Database - должен создать БД и таблицы
        db = Database()

        # Проверяем, что БД создалась
        assert os.path.exists(temp_db_path), "БД не была создана"

        # Подключаемся напрямую для проверки структуры
        conn = sqlite3.connect(temp_db_path)
        cursor = conn.cursor()

        # Проверяем наличие таблицы users
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users'")
        assert cursor.fetchone() is not None, "Таблица users не создана"

        conn.close()

        # Закрываем соединение в db
        if hasattr(db, 'conn') and db.conn:
            db.conn.close()

    def test_db_creation_with_existing_file(self, monkeypatch, temp_db_path):
        """Дополнительный тест: создание БД когда файл уже существует"""
        import db.database as database

        # Создаем пустой файл БД
        with open(temp_db_path, 'w') as f:
            f.write("")

        assert os.path.exists(temp_db_path)

        # Патчим путь к БД
        monkeypatch.setattr(database, 'DB_PATH', temp_db_path)

        # Создаем экземпляр Database
        db = Database()

        # Проверяем, что таблицы создались (должно работать с существующим файлом)
        conn = sqlite3.connect(temp_db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users'")
        assert cursor.fetchone() is not None

        conn.close()

        if hasattr(db, 'conn') and db.conn:
            db.conn.close()

    def test_repeated_app_start_no_db_recreation(self, monkeypatch, temp_db_path):
        """TC-DB-02: Повторный запуск приложения"""
        import db.database as database
        monkeypatch.setattr(database, 'DB_PATH', temp_db_path)

        # Первый запуск
        db1 = Database()

        # Добавляем тестовые данные
        conn = sqlite3.connect(temp_db_path)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (nickname, password) VALUES (?, ?)",
                       ("user1", "pass1"))
        cursor.execute("INSERT INTO users (nickname, password) VALUES (?, ?)",
                       ("user2", "pass2"))
        conn.commit()
        cursor.execute("SELECT COUNT(*) FROM users")
        users_before = cursor.fetchone()[0]
        conn.close()

        # Закрываем первое соединение
        if hasattr(db1, 'conn') and db1.conn:
            db1.conn.close()

        # Второй запуск
        db2 = Database()

        # Проверяем, что данные не продублировались
        conn = sqlite3.connect(temp_db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM users")
        users_after = cursor.fetchone()[0]
        conn.close()

        assert users_before == users_after

        if hasattr(db2, 'conn') and db2.conn:
            db2.conn.close()

    def test_add_user(self, monkeypatch, temp_db_path):
        """TC-USER-01: Добавление тестового пользователя"""
        import db.database as database
        monkeypatch.setattr(database, 'DB_PATH', temp_db_path)

        db = Database()

        # Добавляем нового пользователя
        result = db.add_user("new_user", "new_pass")

        # Проверяем результат операции
        assert result is True

        # Проверяем через отдельное соединение
        conn = sqlite3.connect(temp_db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE nickname='new_user'")
        user = cursor.fetchone()
        conn.close()

        assert user is not None
        assert user[1] == "new_user"
        assert user[2] == "new_pass"
        assert user[3] == 0

        if hasattr(db, 'conn') and db.conn:
            db.conn.close()