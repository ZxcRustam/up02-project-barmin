"""Каталог товаров (Вариант 22: Автомобили). Полная обработка крайних случаев."""

import tkinter as tk
from models import Product
from resources import get_product_image
from styles import (
    COLOR_MAIN_BG, COLOR_HIGHLIGHT,
    FONT_SIZE_SMALL, FONT_SIZE_NORMAL, FONT_SIZE_HEADER, font
)


def create_product_card(parent, product_obj, refresh=None):
    """Создаёт карточку автомобиля по макету с нижней линией-разделителем."""
    qty = product_obj.quantity
    bg_color = _get_card_color(qty)

    card_container = tk.Frame(parent, bg=COLOR_MAIN_BG)
    card_container.pack(fill="x", padx=10, pady=5)

    card = tk.Frame(card_container, bg=bg_color, bd=1, relief="solid")
    card.pack(fill="x")

    _add_image(card, product_obj, bg_color)
    _add_text_info(card, product_obj, bg_color, qty)

    separator = tk.Frame(card_container, height=2, bg="gray70")
    separator.pack(fill="x", pady=(5, 0))

    # === Задание 5.5 и 5.7. Проброс callback refresh для обновления ===
    def _open_view(event):
        from view_form import ViewForm
        # Передаем refresh как аргумент on_add_to_order формы просмотра
        ViewForm(parent, product_obj, on_add_to_order=refresh)

    # Привязываем клики
    card.bind("<Button-1>", _open_view)
    for child in card.winfo_children():
        child.bind("<Button-1>", _open_view)
        for sub_child in child.winfo_children():
            sub_child.bind("<Button-1>", _open_view)

    return card_container


def _get_card_color(qty):
    """Возвращает цвет фона карточки."""
    try:
        numeric_qty = int(qty) if qty is not None else 0
    except (ValueError, TypeError):
        numeric_qty = 0
    return COLOR_HIGHLIGHT if numeric_qty <= 3 else COLOR_MAIN_BG


def _add_image(card, product_obj, bg_color):
    """Добавляет изображение товара (или заглушку)."""
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


def _add_text_info(card, product_obj, bg_color, qty):
    """Добавляет текстовую информацию об автомобиле с расширенной защитой."""
    text_frame = tk.Frame(card, bg=bg_color)
    text_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)

    # Задание 2. Обработка крайних случаев (NULL, кириллица и длина строки)
    raw_model = str(product_obj.model) if product_obj.model else "[Без модели]"
    
    # Ограничение длины наименования до 100 символов по ТЗ
    if len(raw_model) > 100:
        model = raw_model[:97] + "..."
    else:
        model = raw_model

    year = f"{product_obj.year} г." if product_obj.year else "[Год не указан]"
    brand = str(product_obj.brand) if product_obj.brand else "[Без марки]"
    
    raw_price = product_obj.price if product_obj.price is not None else 0
    discounted_price = int(product_obj.price_with_discount_auto()) if product_obj.price is not None else 0

    # Заголовок: Год выпуска | Наименование (Модель)
    _add_label(text_frame, f"{year} | {model}", bg_color, bold=True, size=FONT_SIZE_HEADER)
    
    # Марка (Бренд)
    _add_label(text_frame, f"Марка: {brand}", bg_color)
    
    # Количество с использованием локальной защищенной функции
    _add_label(text_frame, f"Количество: {_indicator(qty)} ({qty} шт.)", bg_color)
    
    # Цена со скидкой (Красивое форматирование больших цен > 1 000 000)
    _add_label(text_frame, f"Цена со скидкой: {discounted_price:,} руб.".replace(",", " "),
               bg_color, bold=True, size=FONT_SIZE_HEADER, align="w")

    # Базовая цена
    _add_label(text_frame, f"Базовая: {raw_price:,} руб.".replace(",", " "),
               bg_color, bold=False, size=FONT_SIZE_SMALL, align="e")


def _add_label(parent, text, bg_color, bold=False, size=FONT_SIZE_NORMAL, align="w"):
    """Универсальная подфункция добавления текстовых меток."""
    tk_anchor = tk.W if align == "w" else (tk.E if align == "e" else tk.CENTER)
    tk.Label(parent, text=text, font=font(size, bold=bold), bg=bg_color, anchor=tk_anchor).pack(fill="x")


# Задание 4.5 + ДЗ. Новая защищенная функция-индикатор
def _indicator(qty):
    """
    Индикатор «много/мало» (порог 5) с защитой от некорректных типов.
    """
    try:
        numeric_qty = float(qty) if qty is not None else 0
    except (ValueError, TypeError):
        numeric_qty = 0

    return "много" if numeric_qty > 5 else "мало"
