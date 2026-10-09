"""Работа с заказами."""
import sqlite3
from datetime import datetime
from config import DB_PATH


def get_connection():
    """Соединение с БД."""
    return sqlite3.connect(DB_PATH)


def add_order_to_db(client, product_id, quantity):
    """
    Добавляет новый заказ в БД.
    """
    try:
        conn = get_connection()
        cur = conn.cursor()
        
        current_date = datetime.now().strftime("%Y-%m-%d")
        
        cur.execute(
            "INSERT INTO Заказ (дата, клиент, товар_id, количество) VALUES (?, ?, ?, ?)",
            (current_date, str(client), int(product_id), int(quantity))
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
