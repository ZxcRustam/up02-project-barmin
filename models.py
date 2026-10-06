"""Модели данных для проекта УП.02 (Вариант 22: Автомобили)."""

from datetime import datetime
from discount import calculate_price_with_discount


class Product:
    """Класс Товар (Автомобиль)."""

    def __init__(self, product_id, brand, model, year, price, quantity, photo):
        """Инициализация автомобиля со всеми полями Варианта 22."""
        self.id = product_id
        self.brand = brand
        self.model = model
        self.year = year
        self.price = price
        self.quantity = quantity
        self.photo = photo

    def is_available(self):
        """Товар доступен для заказа?"""
        return self.quantity > 0

    def total(self):
        """Общая стоимость (цена × количество)."""
        return self.price * self.quantity

    def price_with_discount(self, discount_percent):
        """Цена со старой фиксированной скидкой."""
        return self.price * (1 - discount_percent / 100)

    def price_with_discount_auto(self, date=None):
        """Задание 8. Цена со скидкой по автоматическому алгоритму ДЭ."""
        if date is None:
            date = datetime.now()
        return calculate_price_with_discount(self.id, self.price, date)

    def discounted_price(self):
        """Цена со скидкой 25% (упрощённо для тренировки веток)."""
        return self.price * 0.75   # итоговое значение

    def indicator(self):
        """Индикатор «много/мало» (порог 3)."""
        return "много" if self.quantity > 3 else "мало"

    def info(self):
        """Строка с информацией об автомобиле."""
        status = "В наличии" if self.is_available() else "Нет на складе"
        return (
            f"{self.brand} {self.model} ({self.year} г.) — {status}: "
            f"{self.price} руб. × {self.quantity} шт. = {self.total()} руб. "
            f"({self.indicator()})"
        )


class Order:
    """Класс Заказ."""

    def __init__(self, order_id, date, client, product, quantity):
        self.id = order_id
        self.date = date
        self.client = client
        self.product = product  # Объект класса Product
        self.quantity = quantity

    def total(self):
        """Стоимость заказа."""
        return self.product.price * self.quantity

    def order_info(self):
        """Домашнее задание: краткая информация о заказе."""
        return f"Заказ №{self.id} от {self.date}: {self.client}"

    def info(self):
        """Информация о заказе авто."""
        return (
            f"Заказ №{self.id} от {self.date}: {self.client} — "
            f"{self.product.brand} {self.product.model} × {self.quantity} шт. "
            f"(На сумму: {self.total()} руб.)"
        )
