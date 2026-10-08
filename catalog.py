"""Каталог товаров (Вариант 22: Автомобили)."""

import os
import tkinter as tk
from PIL import Image, ImageTk

# Безопасный импорт конфигурации
try:
    import config
    DB_PATH = getattr(config, "DB_PATH", "databases/db_variant_22.db")
    COLOR_HIGHLIGHT = getattr(config, "COLOR_HIGHLIGHT", "#ff8080")
    FONT_FAMILY = getattr(config, "FONT_FAMILY", "Arial")
except ImportError:
    DB_PATH = "databases/db_variant_22.db"
    COLOR_HIGHLIGHT = "#ff8080"
    FONT_FAMILY = "Arial"

from models import Product


def create_product_card(parent, product_obj):
    """Создаёт карточку автомобиля по макету Варианта 22 с нижней линией-разделителем."""
    qty = product_obj.quantity
    # Убеждаемся, что при количестве ≤ 3 фон строго светло-красный (#ff8080)
    bg_color = COLOR_HIGHLIGHT if qty <= 3 else "white"

    # Контейнер для карточки и разделителя
    card_container = tk.Frame(parent, bg="white")
    card_container.pack(fill="x", padx=10, pady=5)

    # Сама карточка — рамка со всех сторон
    card = tk.Frame(card_container, bg=bg_color, bd=1, relief="solid")
    card.pack(fill="x")

    # === 1. Изображение (слева) ===
    img_frame = tk.Frame(card, bg=bg_color)
    img_frame.pack(side="left", padx=10, pady=10)

    image_path = f"resources/{product_obj.photo}" if product_obj.photo else "resources/picture.png"
    if not os.path.exists(image_path):
        image_path = "resources/picture.png"

    try:
        img = Image.open(image_path).resize((100, 100))
        photo = ImageTk.PhotoImage(img)
        img_label = tk.Label(img_frame, image=photo, bg=bg_color)
        img_label.__dict__['image'] = photo  
        img_label.pack()
    except Exception:
        tk.Label(img_frame, text="[ФОТО]", bg=bg_color, width=10, height=5).pack()

    # === 2. Текстовая часть (справа) ===
    text_frame = tk.Frame(card, bg=bg_color)
    text_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)

    title = f"{product_obj.year} г. | {product_obj.model}"
    tk.Label(text_frame, text=title, font=(FONT_FAMILY, 14, "bold"),
             bg=bg_color, anchor="w").pack(fill="x")

    tk.Label(text_frame, text=f"Марка: {product_obj.brand}",
             font=(FONT_FAMILY, 11), bg=bg_color, anchor="w").pack(fill="x")

    indicator = product_obj.indicator()  
    tk.Label(text_frame, text=f"Количество: {indicator} ({qty} шт.)",
             font=(FONT_FAMILY, 11), bg=bg_color, anchor="w").pack(fill="x")

    discounted_price = int(product_obj.price_with_discount_auto())
    tk.Label(text_frame, text=f"Цена со скидкой: {discounted_price:,} руб.".replace(",", " "),
             font=(FONT_FAMILY, 13, "bold"), fg="darkgreen",
             bg=bg_color, anchor="w").pack(fill="x")

    tk.Label(text_frame, text=f"Базовая: {product_obj.price:,} руб.".replace(",", " "),
             font=(FONT_FAMILY, 10, "italic"), fg="gray",
             bg=bg_color, anchor="e").pack(fill="x")

    # ЗАДАНИЕ 1. Линия-разделитель снизу карточки
    separator = tk.Frame(card_container, height=2, bg="gray70")
    separator.pack(fill="x", pady=(5, 0))

    return card_container
