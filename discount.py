"""Модуль автоматического расчёта скидки на автомобили (Вариант 22)."""

from datetime import datetime, timedelta
import sqlite3
from config import DB_PATH


def get_previous_month_range(date):
    """
    Возвращает (начало, конец) предыдущего месяца.
    
    :param date: дата расчёта
    :return: (start_date, end_date) в формате YYYY-MM-DD
    """
    first_day = date.replace(day=1)
    last_day_prev = first_day - timedelta(days=1)
    first_day_prev = last_day_prev.replace(day=1)
    return (
        first_day_prev.strftime("%Y-%m-%d"),
        last_day_prev.strftime("%Y-%m-%d")
    )


def has_orders_in_previous_month(car_id, date):
    """
    Проверяет, были ли продажи этого автомобиля в предыдущем месяце.
    
    :param car_id: id автомобиля (товар_id)
    :param date: дата расчёта
    :return: True / False
    """
    start, end = get_previous_month_range(date)

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    # В таблице Заказ поле называется товар_id, связываем его с car_id
    cur.execute(
        "SELECT COUNT(*) FROM Заказ "
        "WHERE товар_id = ? AND дата BETWEEN ? AND ?",
        (car_id, start, end)
    )
    count = cur.fetchone()[0]
    conn.close()
    return count > 0


def calculate_price_with_discount(car_id, price, date):
    """
    Рассчитывает цену автомобиля со скидкой 25% (если не было продаж в прошлом месяце).
    
    :param car_id: id автомобиля
    :param price: базовая цена автомобиля
    :param date: дата расчёта
    :return: цена со скидкой или без
    """
    if has_orders_in_previous_month(car_id, date):
        return price
    return price * 0.75


if __name__ == "__main__":
    # Тестовый запуск для проверки
    # Сегодня по дате в бланке 05.10.2026, значит прошлый месяц — сентябрь 2026
    test_date = datetime(2026, 10, 5)
    
    print("Проверка расчёта скидок для автосалона (за прошлый месяц):")
    print("-" * 50)
    
    # Honda Civic (id=1) покупали в сентябре -> скидки быть не должно
    price_honda = calculate_price_with_discount(1, 1800000, test_date)
    print(f"Honda Civic (были продажи): {price_honda} руб. (Базовая: 1800000)")
    
    # Volkswagen Tiguan (id=4) НЕ покупали в сентябре -> должна быть скидка 25%
    price_vw = calculate_price_with_discount(4, 3500000, test_date)
    print(f"VW Tiguan (не было продаж, скидка 25%): {price_vw} руб. (Базовая: 3500000)")
