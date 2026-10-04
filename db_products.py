"""Загрузка товаров из БД в объекты класса Product с фильтрацией (Вариант 22: Автомобили)."""

import sqlite3
from config import DB_PATH
from models import Product


def get_all_products():
    """Возвращает список всех объектов Product из БД."""
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT * FROM Товар ORDER BY id")
    rows = cur.fetchall()
    conn.close()

    products = []
    for row in rows:
        product = Product(
            product_id=row[0],
            brand=row[1],
            model=row[2],
            year=row[3],
            price=row[4],
            quantity=row[5],
            photo=row[6]
        )
        products.append(product)
    return products


def get_products_by_category(brand):
    """Возвращает список объектов Product по марке (категории)."""
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT * FROM Товар WHERE марка = ?", (brand,))
    rows = cur.fetchall()
    conn.close()

    products = []
    for row in rows:
        product = Product(
            product_id=row[0],
            brand=row[1],
            model=row[2],
            year=row[3],
            price=row[4],
            quantity=row[5],
            photo=row[6]
        )
        products.append(product)
    return products


def get_products_low_stock():
    """Возвращает автомобили с количеством ≤ 3 (низкий остаток)."""
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT * FROM Товар WHERE количество <= 3")
    rows = cur.fetchall()
    conn.close()

    products = []
    for row in rows:
        product = Product(
            product_id=row[0],
            brand=row[1],
            model=row[2],
            year=row[3],
            price=row[4],
            quantity=row[5],
            photo=row[6]
        )
        products.append(product)
    return products


def print_catalog_with_highlight(products):
    """Выводит каталог с подсветкой ⚠️ для автомобилей с количеством ≤ 3."""
    print(f"\n{'=' * 70}")
    print(f"КАТАЛОГ ({len(products)} автомобилей)")
    print("=" * 70)

    for p in products:
        highlight = "⚠️" if p.quantity <= 3 else "  "
        print(f"{highlight} {p.info()}")

    print("=" * 70)


if __name__ == "__main__":
    print("1. Все товары:")
    print_catalog_with_highlight(get_all_products())

    print("\n2. Товары категории «Honda»:")
    print_catalog_with_highlight(get_products_by_category("Honda"))

    print("\n3. Товары с низким остатком (≤3):")
    print_catalog_with_highlight(get_products_low_stock())
