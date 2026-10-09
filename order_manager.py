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
        cur.execute(
            "UPDATE Товар SET количество = ? WHERE id = ?",
            (int(new_quantity), int(product_id))
        )
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"[DEBUG] Ошибка обновления количества товара: {e}")


def decrease_product_quantity(product_id, quantity):
    """
    Уменьшает количество товара на складе (Задание 4.4).
    :param product_id: id товара
    :param quantity: на сколько уменьшить
    :return: True при успехе, False при ошибке
    """
    conn = get_connection()
    cur = conn.cursor()

    try:
        # Проверяем, что товара достаточно
        cur.execute("SELECT количество FROM Товар WHERE id = ?", (int(product_id),))
        row = cur.fetchone()
        if not row:
            return False

        current = row[0]
        if current < quantity:
            return False

        # Уменьшаем (Вариант 2 — атомарное вычитание)
        cur.execute(
            "UPDATE Товар SET количество = количество - ? WHERE id = ?",
            (int(quantity), int(product_id))
        )
        conn.commit()
        return True

    except Exception as e:
        conn.rollback()
        print(f"Ошибка обновления: {e}")
        return False

    finally:
        conn.close()


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
    """
    try:
        conn = get_connection()
        cur = conn.cursor()
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


def get_all_orders():
    """
    Возвращает список всех заказов (Задание 4.3).
    :return: список кортежей (id, дата, клиент)
    """
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT id, дата, клиент FROM Заказ ORDER BY id DESC")
        rows = cur.fetchall()
        conn.close()
        return rows
    except Exception as e:
        print(f"[DEBUG] Ошибка получения всех заказов: {e}")
        return []


def create_order(client, items):
    """
    Создаёт заказ с несколькими позициями (Задание 5.3).
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

        # 2. Добавляем позиции И уменьшаем остатки
        for product_id, size, quantity, price in items:
            # Проверяем наличие
            cur.execute("SELECT количество FROM Товар WHERE id = ?", (int(product_id),))
            row = cur.fetchone()
            if not row or row[0] < quantity:
                raise ValueError(f"Недостаточно товара id={product_id}")

            # Добавляем позицию в Состав_заказа (комплектация вместо размера для Варианта 22)
            cur.execute(
                "INSERT INTO Состав_заказа "
                "(заказ_id, товар_id, комплектация, количество, цена) "
                "VALUES (?, ?, ?, ?, ?)",
                (order_id, int(product_id), str(size), int(quantity), float(price))
            )

            # Уменьшаем остаток атомарно
            cur.execute(
                "UPDATE Товар SET количество = количество - ? WHERE id = ?",
                (int(quantity), int(product_id))
            )

        # 3. Фиксируем ВСЁ, только если все шаги прошли успешно
        conn.commit()
        return order_id

    except Exception as e:
        # Откатываем ВСЁ назад, база остается нетронутой
        conn.rollback()
        print(f"Ошибка создания заказа: {e}")
        return None

    finally:
        conn.close()
        
def get_order_items(order_id):
    """
    Возвращает состав заказа (Универсальная версия для Варианта 22).
    """
    try:
        conn = get_connection()
        cur = conn.cursor()
        
        # 1. Сначала пробуем найти позиции в таблице Состав_заказа
        cur.execute("""
            SELECT Состав_заказа.id, Товар.модель,
                   Состав_заказа.комплектация, Состав_заказа.количество,
                   Состав_заказа.цена
            FROM Состав_заказа
            JOIN Товар ON Состав_заказа.товар_id = Товар.id
            WHERE Состав_заказа.заказ_id = ?
        """, (int(order_id),))
        rows = cur.fetchall()
        
        # 2. Если в Состав_заказа пусто (как для заказов 7, 8, 9), берем данные напрямую из таблицы Заказ!
        if not rows:
            cur.execute("""
                SELECT Заказ.id, Товар.модель,
                       'Базовая' AS комплектация, Заказ.количество,
                       Товар.цена
                FROM Заказ
                JOIN Товар ON Заказ.товар_id = Товар.id
                WHERE Заказ.id = ? AND Заказ.товар_id IS NOT NULL
            """, (int(order_id),))
            rows = cur.fetchall()
            
        conn.close()
        return rows
    except Exception as e:
        print(f"[DEBUG] Ошибка получения состава заказа: {e}")
        return []

