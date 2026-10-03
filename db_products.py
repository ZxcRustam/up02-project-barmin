"""Загрузка товаров из БД с расширенным выводом (Вариант 22: Автомобили)."""

import sqlite3
from config import DB_PATH


def get_all_products():
    """Возвращает список всех автомобилей."""
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT * FROM Товар ORDER BY id")
    products = cur.fetchall()
    conn.close()
    return products


def get_products_by_category(category):
    """Товары по категории (марке)."""
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT * FROM Товар WHERE марка = ?", (category,))
    products = cur.fetchall()
    conn.close()
    return products


def get_products_low_stock():
    """Товары с количеством <= 3 (низкий остаток)."""
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT * FROM Товар WHERE количество <= 3")
    products = cur.fetchall()
    conn.close()
    return products


def get_categories():
    """Список всех уникальных марок авто."""
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT DISTINCT марка FROM Товар ORDER BY марка")
    categories = [row[0] for row in cur.fetchall()]
    conn.close()
    return categories


def print_catalog(products):
    """Каталог с индикатором остатка."""
    print(f"\n{'=' * 60}")
    print(f"КАТАЛОГ ({len(products)} автомобилей)")
    print("=" * 60)

    for p in products:
        # Распаковка строго по колонкам твоей базы данных Варианта 22:
        # 0: id, 1: марка, 2: модель, 3: год, 4: цена, 5: количество
        brand = p[1]
        model = p[2]
        year = p[3]
        price = p[4]
        qty = p[5]  # Теперь берем реальное количество из базы (у Honda будет 4!)

        indicator = "много" if qty > 3 else "мало"
        highlight = "⚠️" if qty <= 3 else "  "

        print(f"{highlight} {brand} {model} ({year} г.)")
        print(f"   Цена: {price} руб. | Кол-во: {qty} шт. ({indicator})")
        print("-" * 40)

    print("=" * 60)


if __name__ == "__main__":
    print("1. Все товары")
    print_catalog(get_all_products())

    print("\n2. Категории:")
    for cat in get_categories():
        print(f"   - {cat}")

    print("\n3. Товары с низким остатком (<=3):")
    print_catalog(get_products_low_stock())
