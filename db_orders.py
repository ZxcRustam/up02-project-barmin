"""Задание 3. Загрузка заказов из БД и связывание с объектами Product."""

import sqlite3
from config import DB_PATH
from models import Product, Order


def get_all_orders():
    """Загружает заказы из БД и связывает их с автомобилями."""
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    
    # Загружаем сначала все автомобили, чтобы делать привязку по id
    cur.execute("SELECT * FROM Товар")
    cars_rows = cur.fetchall()
    cars_dict = {}
    for r in cars_rows:
        cars_dict[r[0]] = Product(r[0], r[1], r[2], r[3], r[4], r[5], r[6])

    # Теперь загружаем все заказы
    # Структура таблицы Заказ: 0-id, 1-дата, 2-клиент, 3-товар_id, 4-количество
    cur.execute("SELECT * FROM Заказ ORDER BY id")
    orders_rows = cur.fetchall()
    conn.close()

    orders = []
    for row in orders_rows:
        order_id = row[0]
        date = row[1]
        client = row[2]
        product_id = row[3]
        quantity = row[4]

        # Находим объект автомобиля по его id
        associated_product = cars_dict.get(product_id)

        if associated_product:
            # Создаем объект заказа и передаем внутрь объект автомобиля!
            order = Order(order_id, date, client, associated_product, quantity)
            orders.append(order)
            
    return orders


if __name__ == "__main__":
    print("=" * 70)
    print("СПИСОК ОФОРМЛЕННЫХ ЗАКАЗОВ В АВТОСАЛОНЕ:")
    print("=" * 70)
    
    orders = get_all_orders()
    for o in orders:
        print(o.info())
        print("-" * 70)
