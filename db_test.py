"""Проверка подключения к БД."""
import sqlite3
from config import DB_PATH


def test_connection():
    """Проверка подключения к БД."""
    try:
        conn = sqlite3.connect(DB_PATH)
        print(f"✅ Подключение к {DB_PATH} установлено")

        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM Товар")
        count = cur.fetchone()[0]
        print(f"📦 Товаров в базе: {count}")

        conn.close()
        print("✅ Соединение закрыто")
    except sqlite3.Error as e:
        print(f"❌ Ошибка БД: {e}")


if __name__ == "__main__":
    test_connection()
