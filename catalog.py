"""Каталог товаров (Вариант 22: Автомобили). Рефакторинг и защита данных."""

import tkinter as tk
from models import Product
from resources import get_product_image
from styles import (
    COLOR_MAIN_BG, COLOR_HIGHLIGHT,
    FONT_SIZE_SMALL, FONT_SIZE_NORMAL, FONT_SIZE_HEADER, font
)


def create_product_card(parent, product_obj):
    """Создаёт карточку автомобиля по макету с нижней линией-разделителем."""
    qty = product_obj.quantity
    bg_color = _get_card_color(qty)

    # Контейнер для карточки и разделителя
    card_container = tk.Frame(parent, bg=COLOR_MAIN_BG)
    card_container.pack(fill="x", padx=10, pady=5)

    # Сама карточка — рамка со всех сторон
    card = tk.Frame(card_container, bg=bg_color, bd=1, relief="solid")
    card.pack(fill="x")

    # Вызовы отрефакторенных вспомогательных подфункций
    _add_image(card, product_obj, bg_color)
    _add_text_info(card, product_obj, bg_color, qty)

    # Линия-разделитель снизу карточки
    separator = tk.Frame(card_container, height=2, bg="gray70")
    separator.pack(fill="x", pady=(5, 0))

    return card_container


def _get_card_color(qty):
    """Возвращает цвет фонда карточки (подсветка при ≤3 шт)."""
    return COLOR_HIGHLIGHT if qty <= 3 else COLOR_MAIN_BG


def _add_image(card, product_obj, bg_color):
    """Добавляет изображение товара (или заглушку) через безопасный модуль."""
    img_frame = tk.Frame(card, bg=bg_color)
    img_frame.pack(side="left", padx=10, pady=10)

    img_filename = f"resources/{product_obj.photo}" if product_obj.photo else "resources/picture.png"
    photo = get_product_image(img_filename, size=(100, 100))
    
    if photo:
        img_label = tk.Label(img_frame, image=photo, bg=bg_color)
        img_label.__dict__['image'] = photo  # сохраняем ссылку от сборщика мусора и Pylance
        img_label.pack()
    else:
        tk.Label(img_frame, text="[НЕТ ФОТО]", bg=bg_color, width=10, height=5).pack()


def _add_text_info(card, product_obj, bg_color, qty):
    """Добавляет текстовую информацию об автомобиле с защитой от NULL значений (тернарные операторы)."""
    text_frame = tk.Frame(card, bg=bg_color)
    text_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)

    # Задание 5.4. Проверка крайних случаев (тернарные операторы)
    model = product_obj.model if product_obj.model else "[Без модели]"
    year = f"{product_obj.year} г." if product_obj.year else "[Год не указан]"
    brand = product_obj.brand if product_obj.brand else "[Без марки]"
    
    # Защита базовой цены от None
    raw_price = product_obj.price if product_obj.price is not None else 0
    
    # Расчет цены со скидкой на основе проверенной базовой цены
    discounted_price = int(product_obj.price_with_discount_auto()) if product_obj.price is not None else 0

    # Вывод данных с использованием безопасных переменных
    # Год выпуска | Наименование (Модель)
    _add_label(text_frame, f"{year} | {model}",
               bg_color, bold=True, size=FONT_SIZE_HEADER)
    
    # Марка (Бренд)
    _add_label(text_frame, f"Марка: {brand}", bg_color)
    
    # Количество (с автоматическим индикатором)
    _add_label(text_frame, f"Количество: {product_obj.indicator()} ({qty} шт.)", bg_color)
    
    # Цена со скидкой (выравнивание по левому краю)
    _add_label(text_frame, f"Цена со скидкой: {discounted_price:,} руб.".replace(",", " "),
               bg_color, bold=True, size=FONT_SIZE_HEADER, align="w")

    # Базовая цена (выравнивание по правому краю)
    _add_label(text_frame, f"Базовая: {raw_price:,} руб.".replace(",", " "),
               bg_color, bold=False, size=FONT_SIZE_SMALL, align="e")


def _add_label(parent, text, bg_color, bold=False, size=FONT_SIZE_NORMAL, align="w"):
    """Универсальная подфункция для добавления меток с правильным выравниванием по КИМ."""
    # Безопасный перевод строкового направления в константы Tkinter для Pylance
    tk_anchor = tk.W if align == "w" else (tk.E if align == "e" else tk.CENTER)
    
    tk.Label(parent, text=text, font=font(size, bold=bold),
             bg=bg_color, anchor=tk_anchor).pack(fill="x")
