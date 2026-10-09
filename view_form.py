"""Форма просмотра товара."""
import tkinter as tk
from tkinter import ttk, messagebox

from styles import (
    COLOR_MAIN_BG, COLOR_SECONDARY_BG, COLOR_ACCENT,
    FONT_SIZE_NORMAL, FONT_SIZE_HEADER, FONT_SIZE_TITLE, font
)
from resources import load_image, get_product_image


class ViewForm:
    """
    Форма просмотра выбранного товара.
    
    Открывается при клике на карточку в каталоге.
    """
    
    def __init__(self, parent, product, on_add_to_order=None):
        """
        Инициализация формы.
        
        :param parent: родительское окно
        :param product: объект Product с данными автомобиля
        :param on_add_to_order: callback для добавления в заказ
        """
        self.product = product
        self.on_add_to_order = on_add_to_order
        
        self.window = tk.Toplevel(parent)
        
        # Получаем название модели напрямую из объекта
        model_name = getattr(product, 'model', '[Без модели]')
        self.window.title(f"Просмотр — {model_name}")
        self.window.geometry("700x600")
        self.window.configure(bg=COLOR_MAIN_BG)
        
        self.build_ui()
    
    def build_ui(self):
        """Строит интерфейс формы."""
        # Шапка — ГОТОВО
        header = tk.Frame(self.window, bg=COLOR_SECONDARY_BG, height=60)
        header.pack(fill="x")
        header.pack_propagate(False)
        
        tk.Label(header, text="КАРТОЧКА АВТОМОБИЛЯ",
                 font=font(FONT_SIZE_TITLE, bold=True),
                 bg=COLOR_SECONDARY_BG).pack(pady=15)
        
        # Основная область — ГОТОВО
        main = tk.Frame(self.window, bg=COLOR_MAIN_BG)
        main.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Изображение — ГОТОВО
        img_frame = tk.Frame(main, bg=COLOR_MAIN_BG)
        img_frame.pack(side="left", padx=10)
        
        # Извлекаем имя фото напрямую из объекта автомобиля
        photo_file = getattr(self.product, 'photo', '')
        img_filename = f"resources/{photo_file}" if photo_file else "resources/picture.png"
        
        photo = get_product_image(img_filename, size=(200, 200))
        if photo:
            img_label = tk.Label(img_frame, image=photo, bg=COLOR_MAIN_BG)
            img_label.__dict__['image'] = photo  
            img_label.pack()
        else:
            tk.Label(img_frame, text="[НЕТ ФОТО]", bg=COLOR_MAIN_BG, width=20, height=10, relief="solid").pack()
        
        # Информация — Задание 4.2
        info_frame = tk.Frame(main, bg=COLOR_MAIN_BG)
        info_frame.pack(side="left", fill="both", expand=True, padx=20)
        
        # Берем данные напрямую из полей объекта Product
        brand = getattr(self.product, 'brand', '[Без марки]')
        model = getattr(self.product, 'model', '[Без модели]')
        
        year_val = getattr(self.product, 'year', None)
        year = f"{year_val} г." if year_val else "[Год не указан]"
        
        price_val = getattr(self.product, 'price', None)
        price = f"{price_val:,} руб.".replace(",", " ") if price_val is not None else "0 руб."
        
        qty_val = getattr(self.product, 'quantity', 0)
        qty = f"{qty_val} шт."

        # Добавление полей через метод _add_field
        self._add_field(info_frame, "Марка", brand)
        self._add_field(info_frame, "Модель", model)
        self._add_field(info_frame, "Год выпуска", year)
        self._add_field(info_frame, "Цена", price)
        self._add_field(info_frame, "В наличии", qty)
        
        # Кнопки — Задание 4.3
        btn_frame = tk.Frame(self.window, bg=COLOR_MAIN_BG)
        btn_frame.pack(fill="x", pady=20)
        
        btn_add = tk.Button(
            btn_frame, text="Добавить в заказ", command=self.add_to_order,
            bg=COLOR_ACCENT, fg="white", font=font(FONT_SIZE_NORMAL),
            relief="flat", padx=15, pady=5, cursor="hand2"
        )
        btn_add.pack(side="left", padx=30)
        
        btn_back = tk.Button(
            btn_frame, text="Назад", command=self.window.destroy,
            bg=COLOR_ACCENT, fg="white", font=font(FONT_SIZE_NORMAL),
            relief="flat", padx=15, pady=5, cursor="hand2"
        )
        btn_back.pack(side="right", padx=30)
    
    def _add_field(self, parent, label, value):
        """
        Добавляет поле в форму (Задание 4.1).
        """
        row = tk.Frame(parent, bg=COLOR_MAIN_BG)
        row.pack(fill="x", pady=5)
        
        lbl_title = tk.Label(
            row, text=f"{label}:", font=font(FONT_SIZE_NORMAL, bold=True),
            bg=COLOR_MAIN_BG, anchor="w", width=15
        )
        lbl_title.pack(side="left")
        
        lbl_val = tk.Label(
            row, text=str(value), font=font(FONT_SIZE_NORMAL),
            bg=COLOR_MAIN_BG, anchor="w"
        )
        lbl_val.pack(side="left", fill="x", expand=True)
    
    def add_to_order(self):
        """Обработчик кнопки «Добавить в заказ» (Задание 4.4)."""
        if not self.on_add_to_order:
            messagebox.showinfo("Информация", "Функция в разработке")
            return
            
        if not self.product:
            messagebox.showerror("Ошибка", "Товар не выбран")
            return
            
        try:
            self.on_add_to_order(self.product)
            messagebox.showinfo("Успех", "Товар добавлен в заказ")
        except Exception as e:
            messagebox.showerror("Ошибка заказа", f"Не удалось добавить товар:\n{e}")
