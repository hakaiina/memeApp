import pytest
import sqlite3
import os
import tempfile
from db.database import Database


@pytest.fixture
def temp_db_path(tmp_path):
    """Использует pytest tmp_path для создания временной директории"""
    db_path = str(tmp_path / "test.db")

    # Убеждаемся, что файл не существует
    if os.path.exists(db_path):
        os.unlink(db_path)

    yield db_path


@pytest.fixture
def db_with_test_path(monkeypatch, temp_db_path):
    """Создает экземпляр Database с тестовым путем к БД"""
    import db.database as database

    # Патчим константу DB_PATH
    monkeypatch.setattr(database, 'DB_PATH', temp_db_path)

    # Создаем экземпляр БД
    db = Database()

    # Убеждаемся, что таблицы созданы
    db.init_db()

    # Возвращаем db
    yield db

    # Явно закрываем соединение после теста
    if hasattr(db, 'conn') and db.conn:
        db.conn.close()


@pytest.fixture
def db_with_test_user(db_with_test_path):
    """Создает БД с тестовым пользователем"""
    db = db_with_test_path

    # Добавляем тестового пользователя
    db.add_user("test_user", "test_pass")

    return db