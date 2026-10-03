"""Загрузка товаров из БД с расширенным выводом."""

import sqlite3
from config import DB_PATH


def get_all_products():
    """Возвращает список всех товаров."""
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT * FROM Товар ORDER BY id")
    products = cur.fetchall()
    conn.close()
    return products


def get_products_by_category(category):
    """Товары по конкретной категории."""
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT * FROM Товар WHERE категория = ?", (category,))
    products = cur.fetchall()
    conn.close()
    return products


def get_products_low_stock():
    """Товары с количеством <= 3."""
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT * FROM Товар WHERE количество <= 3")
    products = cur.fetchall()
    conn.close()
    return products


def get_categories():
    """Список всех уникальных категорий."""
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT DISTINCT категория FROM Товар ORDER BY категория")
    categories = [row[0] for row in cur.fetchall()]
    conn.close()
    return categories


def print_catalog(products):
    """Каталог с индикатором."""
    print(f"\n{'=' * 60}")
    print(f"КАТАЛОГ ({len(products)} товаров)")
    print("=" * 60)

    for p in products:
        # ИСПРАВЛЕНО под Вариант 1:
        # p[1] - название, p[2] - категория, p[5] - цена, p[6] - количество
        name = p[1]
        category = p[2]
        price = p[5]  # Цена в вашей БД лежит в 5-й колонке!
        qty = p[6]  # Количество лежит в 6-й колонке

        indicator = "много" if qty > 5 else "мало"
        highlight = "⚠️" if qty <= 3 else "  "

        print(f"{highlight} {name} ({category})")
        print(f"   Цена: {price} руб. | Кол-во: {qty} ({indicator})")

    print("=" * 60)


if __name__ == "__main__":
    print("1. Все товары")
    print_catalog(get_all_products())

    print("\n2. Категории:")
    for cat in get_categories():
        print(f"   - {cat}")

    print("\n3. Товары с низким остатком (<=3):")
    print_catalog(get_products_low_stock())
