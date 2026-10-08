"""Каталог товаров (Вариант 22: Автомобили)."""

import tkinter as tk
from models import Product
from resources import get_product_image
# Задание 7.4. Официальный импорт стилей КИМ
from styles import (
    COLOR_MAIN_BG, COLOR_HIGHLIGHT,
    FONT_SIZE_SMALL, FONT_SIZE_NORMAL, FONT_SIZE_HEADER, FONT_SIZE_TITLE,
    font
)


def create_product_card(parent, product_obj):
    """Создаёт карточку автомобиля по макету Варианта 22 с нижней линией-разделителем."""
    qty = product_obj.quantity
    # Задание 7.6. Убеждаемся, что при количестве ≤ 3 фон строго COLOR_HIGHLIGHT (#ff8080)
    bg_color = COLOR_HIGHLIGHT if qty <= 3 else COLOR_MAIN_BG

    # Контейнер для карточки и разделителя
    card_container = tk.Frame(parent, bg=COLOR_MAIN_BG)
    card_container.pack(fill="x", padx=10, pady=5)

    # Сама карточка — рамка со всех сторон
    card = tk.Frame(card_container, bg=bg_color, bd=1, relief="solid")
    card.pack(fill="x")

    # === 1. Изображение (слева) ===
    img_frame = tk.Frame(card, bg=bg_color)
    img_frame.pack(side="left", padx=10, pady=10)

    img_filename = f"resources/{product_obj.photo}" if product_obj.photo else "resources/picture.png"

    photo = get_product_image(img_filename, size=(100, 100))
    if photo:
        img_label = tk.Label(img_frame, image=photo, bg=bg_color)
        img_label.__dict__['image'] = photo  
        img_label.pack()
    else:
        tk.Label(img_frame, text="[НЕТ ФОТО]", bg=bg_color, width=10, height=5).pack()

    # === 2. Текстовая часть (справа) ===
    text_frame = tk.Frame(card, bg=bg_color)
    text_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)

    # Задание 7.5. Применяем Calibri с правильными размерами через функцию font()
    title = f"{product_obj.year} г. | {product_obj.model}"
    tk.Label(text_frame, text=title, font=font(FONT_SIZE_HEADER, bold=True),
             bg=bg_color, anchor="w").pack(fill="x")

    tk.Label(text_frame, text=f"Марка: {product_obj.brand}",
             font=font(FONT_SIZE_NORMAL), bg=bg_color, anchor="w").pack(fill="x")

    indicator = product_obj.indicator()  
    tk.Label(text_frame, text=f"Количество: {indicator} ({qty} шт.)",
             font=font(FONT_SIZE_NORMAL), bg=bg_color, anchor="w").pack(fill="x")

    discounted_price = int(product_obj.price_with_discount_auto())
    tk.Label(text_frame, text=f"Цена со скидкой: {discounted_price:,} руб.".replace(",", " "),
             font=font(FONT_SIZE_HEADER, bold=True), fg="darkgreen",
             bg=bg_color, anchor="w").pack(fill="x")

    tk.Label(text_frame, text=f"Базовая: {product_obj.price:,} руб.".replace(",", " "),
             font=font(FONT_SIZE_SMALL, bold=False), fg="gray",
             bg=bg_color, anchor="e").pack(fill="x")

    # Линия-разделитель снизу карточки
    separator = tk.Frame(card_container, height=2, bg="gray70")
    separator.pack(fill="x", pady=(5, 0))

    return card_container
