"""Работа с заказами."""
import sqlite3
from datetime import datetime
from config import DB_PATH


def get_connection():
    """Соединение с БД."""
    return sqlite3.connect(DB_PATH)


def add_order_to_db(client, date=None):
    """
    Добавляет новый заказ в БД (Задание 5.2).
    :param client: ФИО клиента
    :param date: дата заказа (по умолчанию — сегодня)
    :return: id заказа или None при ошибке
    """
    if date is None:
        date = datetime.now().strftime("%Y-%m-%d")

    try:
        conn = get_connection()
        cur = conn.cursor()

        # В новой структуре пишем только дату и ФИО клиента
        cur.execute(
            "INSERT INTO Заказ (дата, клиент) VALUES (?, ?)",
            (date, str(client))
        )
        conn.commit()
        order_id = cur.lastrowid
        conn.close()

        return order_id
    except Exception as e:
        print(f"[DEBUG] Ошибка добавления заказа в БД: {e}")
        return None



def update_product_quantity(product_id, new_quantity):
    """
    Обновляет количество товара в БД.
    """
    try:
        conn = get_connection()
        cur = conn.cursor()
        
        # Исправлено: возвращаем имя колонки id для таблицы Товар
        cur.execute(
            "UPDATE Товар SET количество = ? WHERE id = ?",
            (int(new_quantity), int(product_id))
        )
        
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"[DEBUG] Ошибка обновления количества товара: {e}")


def get_last_order_id():
    """
    Возвращает id последнего заказа.
    """
    try:
        conn = get_connection()
        cur = conn.cursor()
        
        cur.execute("SELECT MAX(id) FROM Заказ")
        row = cur.fetchone()
        
        conn.close()
        return row[0] if row and row[0] is not None else None
    except Exception as e:
        print(f"[DEBUG] Ошибка получения ID последнего заказа: {e}")
        return None


def get_product_quantity(product_id):
    """
    Возвращает количество товара по id.
    """
    try:
        conn = get_connection()
        cur = conn.cursor()
        # Исправлено: возвращаем имя колонки id для таблицы Товар
        cur.execute("SELECT количество FROM Товар WHERE id = ?", (product_id,))
        row = cur.fetchone()
        conn.close()
        return row[0] if row else 0
    except Exception as e:
        print(f"[DEBUG] Ошибка получения количества товара: {e}")
        return 0
def add_order_item(order_id, product_id, size, quantity, price):
    """
    Добавляет позицию в состав заказа (Задание 6.2).
    :param order_id: id заказа
    :param product_id: id товара
    :param size: комплектация (размер) автомобиля
    :param quantity: количество
    :param price: цена за единицу на момент заказа
    :return: id позиции или None
    """
    try:
        conn = get_connection()
        cur = conn.cursor()

        # Адаптировано под Вариант 22 (комплектация вместо размера)
        cur.execute(
            "INSERT INTO Состав_заказа "
            "(заказ_id, товар_id, комплектация, количество, цена) "
            "VALUES (?, ?, ?, ?, ?)",
            (int(order_id), int(product_id), str(size), int(quantity), float(price))
        )
        conn.commit()
        item_id = cur.lastrowid
        conn.close()

        return item_id
    except Exception as e:
        print(f"[DEBUG] Ошибка добавления позиции в Состав_заказа: {e}")
        return None


def create_order(client, items):
    """
    Создаёт заказ с несколькими позициями (Задание 6.4).
    :param client: ФИО клиента
    :param items: список кортежей (product_id, size, quantity, price)
    :return: id заказа или None
    """
    conn = get_connection()
    cur = conn.cursor()

    try:
        # 1. Создаём заказ
        date = datetime.now().strftime("%Y-%m-%d")
        cur.execute(
            "INSERT INTO Заказ (дата, клиент) VALUES (?, ?)",
            (date, str(client))
        )
        order_id = cur.lastrowid

        # 2. Добавляем позиции
        for product_id, size, quantity, price in items:
            # Адаптировано под Вариант 22 (комплектация вместо размера)
            cur.execute(
                "INSERT INTO Состав_заказа "
                "(заказ_id, товар_id, комплектация, количество, price) "
                "VALUES (?, ?, ?, ?, ?)" if "price" in [col[1] for col in cur.execute("PRAGMA table_info(Состав_заказа)").fetchall()] else
                "INSERT INTO Состав_заказа (заказ_id, товар_id, комплектация, количество, цена) VALUES (?, ?, ?, ?, ?)",
                (order_id, int(product_id), str(size), int(quantity), float(price))
            )

        # 3. Фиксируем изменения, если всё прошло без ошибок
        conn.commit()
        return order_id

    except Exception as e:
        # Откат транзакции при любой ошибке
        conn.rollback()
        print(f"Ошибка создания заказа: {e}")
        return None

    finally:
        conn.close()
