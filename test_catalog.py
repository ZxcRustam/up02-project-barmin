"""Расширенная автоматизированная проверка (Вариант 22: Автомобили)."""

import sqlite3

try:
    import config
    DB_PATH = getattr(config, "DB_PATH", "databases/db_variant_22.db")
except ImportError:
    DB_PATH = "databases/db_variant_22.db"


def get_products():
    """Безопасное извлечение строк из базы данных."""
    try:
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        cur.execute("SELECT * FROM Товар")
        rows = cur.fetchall()
        conn.close()
        return rows
    except Exception as e:
        print(f"❌ Ошибка подключения к БД: {e}")
        return []


def test_fields():
    """Проверяет минимальное количество полей."""
    products = get_products()
    print(f"Всего товаров в базе: {len(products)}")
    required_count = 6
    errors = 0
    for p in products:
        if len(p) < required_count:
            print(f"❌ Автомобиль id={p[0]}: мало полей ({len(p)})")
            errors += 1
    if errors == 0:
        print("✅ Все автомобили содержат нужные поля")


def test_prices_and_qty():
    """Проверяет наличие цен и неотрицательное количество."""
    products = get_products()
    price_ok = True
    qty_ok = True
    has_photo = False

    for p in products:
        # Индекс 4: цена, Индекс 5: количество, Индекс 6: фото
        price = p[4]
        qty = p[5]
        photo = p[6]

        if price is None:
            print(f"❌ Автомобиль id={p[0]}: отсутствует цена")
            price_ok = False
        if qty is None or qty < 0:
            print(f"❌ Автомобиль id={p[0]}: некорректное количество ({qty})")
            qty_ok = False
        if photo and photo.strip() != "":
            has_photo = True

    if price_ok:
        print("✅ У всех автомобилей заполнена стоимость")
    if qty_ok:
        print("✅ У всех автомобилей количество на складе корректно (>= 0)")
    if has_photo:
        print("✅ В базе присутствует как минимум одно изображение автомобиля")
    else:
        print("❌ Ошибка: В базе нет ни одного изображения")


if __name__ == "__main__":
    print("--- ЗАПУСК РАСШИРЕННЫХ ТЕСТОВ ---")
    test_fields()
    test_prices_and_qty()
