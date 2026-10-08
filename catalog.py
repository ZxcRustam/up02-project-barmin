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
    """
    Создаёт карточку автомобиля по макету Варианта 22.
    
    :param parent: родительский контейнер (tk.Frame)
    :param product_obj: объект класса Product
    """
    # Определяем фон: подсвечиваем, если количество ≤ 3
    qty = product_obj.quantity
    bg_color = COLOR_HIGHLIGHT if qty <= 3 else "white"

    # Карточка — рамка со всех сторон
    card = tk.Frame(parent, bg=bg_color, bd=1, relief="solid")
    card.pack(fill="x", padx=10, pady=5)

    # === 1. Изображение (слева) ===
    img_frame = tk.Frame(card, bg=bg_color)
    img_frame.pack(side="left", padx=10, pady=10)

    # Ищем картинку в папке resources
    image_path = f"resources/{product_obj.photo}" if product_obj.photo else "resources/picture.png"
    if not os.path.exists(image_path):
        image_path = "resources/picture.png"

    try:
        img = Image.open(image_path).resize((100, 100))
        photo = ImageTk.PhotoImage(img)
        img_label = tk.Label(img_frame, image=photo, bg=bg_color)
        img_label.__dict__['image'] = photo  # сохраняем ссылку от сборщика мусора!
        img_label.pack()
    except Exception:
        tk.Label(img_frame, text="[ФОТО]", bg=bg_color, width=10, height=5).pack()

    # === 2. Текстовая часть (справа) ===
    text_frame = tk.Frame(card, bg=bg_color)
    text_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)

    # Год выпуска | Наименование (Модель)
    title = f"{product_obj.year} г. | {product_obj.model}"
    tk.Label(text_frame, text=title, font=(FONT_FAMILY, 14, "bold"),
             bg=bg_color, anchor="w").pack(fill="x")

    # Марка (Бренд) вместо категории
    tk.Label(text_frame, text=f"Марка: {product_obj.brand}",
             font=(FONT_FAMILY, 11), bg=bg_color, anchor="w").pack(fill="x")

    # Количество с использованием автомобильного индикатора (порог 3)
    indicator = product_obj.indicator()  # много / мало
    tk.Label(text_frame, text=f"Количество: {indicator} ({qty} шт.)",
             font=(FONT_FAMILY, 11), bg=bg_color, anchor="w").pack(fill="x")

    # Цена со скидкой (автоматический расчет по алгоритму ДЭ)
    discounted_price = int(product_obj.price_with_discount_auto())
    tk.Label(text_frame, text=f"Цена со скидкой: {discounted_price:,} руб.".replace(",", " "),
             font=(FONT_FAMILY, 13, "bold"), fg="darkgreen",
             bg=bg_color, anchor="w").pack(fill="x")

    # Базовая цена (справа внизу)
    tk.Label(text_frame, text=f"Базовая: {product_obj.price:,} руб.".replace(",", " "),
             font=(FONT_FAMILY, 10, "italic"), fg="gray",
             bg=bg_color, anchor="e").pack(fill="x")

    return card
