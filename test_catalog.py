"""Проверка вывода полей (Вариант 22: Автомобили)."""

import sqlite3

# Безопасный импорт пути к БД
try:
    import config
    DB_PATH = getattr(config, "DB_PATH", "databases/db_variant_22.db")
except ImportError:
    DB_PATH = "databases/db_variant_22.db"


def test_fields():
    """Проверяет, что все поля на месте."""
    try:
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        cur.execute("SELECT * FROM Товар")
        products = cur.fetchall()
        conn.close()
    except Exception as e:
        print(f"❌ Ошибка подключения к БД: {e}")
        return

    print(f"Всего товаров: {len(products)}")

    required_count = 6   # минимум полей для макета
    errors = 0

    for p in products:
        if len(p) < required_count:
            print(f"❌ Товар id={p[0]}: мало полей ({len(p)})")
            errors += 1

    if errors == 0:
        print("✅ Все товары содержат нужные поля")
    else:
        print(f"❌ Найдено ошибок: {errors}")


if __name__ == "__main__":
    test_fields()
