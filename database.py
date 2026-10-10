"""Модуль работы с пользователями и авторизацией."""
import sqlite3
from config import DB_PATH


def get_user_by_login(login):
    """
    Ищет пользователя по логину (Задание 5.2).
    :param login: логин
    :return: кортеж (id, фамилия, имя, отчество, логин, роль) или None
    """
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
        SELECT Пользователь.id, Пользователь.фамилия,
               Пользователь.имя, Пользователь.отчество,
               Пользователь.логин, Роль.название
        FROM Пользователь
        JOIN Роль ON Пользователь.роль_id = Роль.id
        WHERE Пользователь.логин = ?
    """, (login,))
    row = cur.fetchone()
    conn.close()
    return row
