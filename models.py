"""Модели данных для проекта УП.02 (Вариант 22: Автомобили)."""


class Product:
    """Класс Товар (Автомобиль)."""

    def __init__(self, product_id, brand, model, year, price, quantity, photo):
        """
        Инициализация автомобиля.

        :param product_id: идентификатор (id)
        :param brand: марка автомобиля
        :param model: модель автомобиля
        :param year: год выпуска
        :param price: цена
        :param quantity: количество на складе
        :param photo: имя файла изображения
        """
        self.id = product_id
        self.brand = brand
        self.model = model
        self.year = year
        self.price = price
        self.quantity = quantity
        self.photo = photo

    def total(self):
        """Общая стоимость (цена × количество)."""
        return self.price * self.quantity

    def price_with_discount(self, discount_percent):
        """Цена со скидкой."""
        return self.price * (1 - discount_percent / 100)

    def indicator(self):
        """Индикатор «много/мало» (порог 3 для автосалона)."""
        return "много" if self.quantity > 3 else "мало"

    def info(self):
        """Строка с информацией об автомобиле."""
        return (
            f"{self.brand} {self.model} ({self.year} г.): "
            f"{self.price} руб. × {self.quantity} шт. = {self.total()} руб. "
            f"({self.indicator()})"
        )
