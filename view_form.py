"""Форма просмотра товара с выбором количества и комплектации (Размера) из КИМ."""
import tkinter as tk
from tkinter import ttk, messagebox

from styles import (
    COLOR_MAIN_BG, COLOR_SECONDARY_BG, COLOR_ACCENT,
    FONT_SIZE_NORMAL, FONT_SIZE_HEADER, FONT_SIZE_TITLE, font
)
from resources import load_image, get_product_image
from error_handler import validate_positive_int

# Импортируем только менеджер заказов
from order_manager import (
    add_order_to_db, 
    update_product_quantity, 
    get_product_quantity
)


class ViewForm:
    """Форма просмотра выбранного товара."""
    
    def __init__(self, parent, product, on_add_to_order=None):
        """
        Инициализация формы.
        """
        self.product = product
        self.on_add_to_order = on_add_to_order
        
        self.window = tk.Toplevel(parent)
        
        model_name = getattr(product, 'model', '[Без модели]')
        self.window.title(f"Просмотр — {model_name}")
        self.window.geometry("700x700")  # Увеличили высоту под новые фреймы КИМ
        self.window.configure(bg=COLOR_MAIN_BG)
        
        self.build_ui()
    
    def build_ui(self):
        """Строит интерфейс формы."""
        # Шапка
        header = tk.Frame(self.window, bg=COLOR_SECONDARY_BG, height=60)
        header.pack(fill="x")
        header.pack_propagate(False)
        
        tk.Label(header, text="КАРТОЧКА АВТОМОБИЛЯ",
                 font=font(FONT_SIZE_TITLE, bold=True),
                 bg=COLOR_SECONDARY_BG).pack(pady=15)
        
        # Основная область
        main = tk.Frame(self.window, bg=COLOR_MAIN_BG)
        main.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Изображение
        img_frame = tk.Frame(main, bg=COLOR_MAIN_BG)
        img_frame.pack(side="left", padx=10)
        
        photo_file = getattr(self.product, 'photo', '')
        img_filename = f"resources/{photo_file}" if photo_file else "resources/picture.png"
        
        photo = get_product_image(img_filename, size=(200, 200))
        if photo:
            img_label = tk.Label(img_frame, image=photo, bg=COLOR_MAIN_BG)
            img_label.__dict__['image'] = photo  
            img_label.pack()
        else:
            tk.Label(img_frame, text="[НЕТ ФОТО]", bg=COLOR_MAIN_BG, width=20, height=10, relief="solid").pack()
        
        # Информация
        info_frame = tk.Frame(main, bg=COLOR_MAIN_BG)
        info_frame.pack(side="left", fill="both", expand=True, padx=20)
        
        brand = getattr(self.product, 'brand', '[Без марки]')
        model = getattr(self.product, 'model', '[Без модели]')
        
        year_val = getattr(self.product, 'year', None)
        year = f"{year_val} г." if year_val else "[Год не указан]"
        
        price_val = getattr(self.product, 'price', None)
        price = f"{price_val:,} руб.".replace(",", " ") if price_val is not None else "0 руб."
        
        qty_val = getattr(self.product, 'quantity', 0)
        qty = f"{qty_val} шт."

        self._add_field(info_frame, "Марка", brand)
        self._add_field(info_frame, "Модель", model)
        self._add_field(info_frame, "Год выпуска", year)
        self._add_field(info_frame, "Цена", price)
        self._add_field(info_frame, "В наличии", qty)
        
        description = getattr(self.product, 'description', "Официальный дилерский автомобиль. Комплектация базовая.")
        self._add_field(info_frame, "Описание", description)

        # === Задание 4.2. Поле ввода количества через StringVar ===
        qty_frame = tk.Frame(info_frame, bg=COLOR_MAIN_BG)
        qty_frame.pack(fill="x", pady=10)

        tk.Label(qty_frame, text="Количество:", font=font(FONT_SIZE_NORMAL),
                 bg=COLOR_MAIN_BG).pack(side="left", padx=5)

        self.qty_var = tk.StringVar(value="1")
        qty_entry = tk.Entry(qty_frame, textvariable=self.qty_var, width=5,
                             font=font(FONT_SIZE_NORMAL), relief="solid")
        qty_entry.pack(side="left", padx=5)

        # === Задание 4.2. Выбор размера (комплектации автомобиля для Варианта 22) ===
        size_frame = tk.Frame(info_frame, bg=COLOR_MAIN_BG)
        size_frame.pack(fill="x", pady=10)

        tk.Label(size_frame, text="Комплектация:", font=font(FONT_SIZE_NORMAL),
                 bg=COLOR_MAIN_BG).pack(side="left", padx=5)

        # Передаем фиксированный список опций комплектации вместо обращения к БД
        sizes = ["Базовая", "Комфорт", "Люкс"]

        self.size_var = tk.StringVar(value=sizes[0])
        size_combo = ttk.Combobox(size_frame, textvariable=self.size_var,
                                  values=sizes, state="readonly", width=12,
                                  font=font(FONT_SIZE_NORMAL))
        size_combo.pack(side="left", padx=5)
        
        # Кнопки
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
        """Добавляет поле в форму."""
        row = tk.Frame(parent, bg=COLOR_MAIN_BG)
        row.pack(fill="x", pady=5)
        
        lbl_title = tk.Label(
            row, text=f"{label}:", font=font(FONT_SIZE_NORMAL, bold=True),
            bg=COLOR_MAIN_BG, anchor="w", width=15
        )
        lbl_title.pack(side="left")
        
        lbl_val = tk.Label(
            row, text=str(value), font=font(FONT_SIZE_NORMAL),
            bg=COLOR_MAIN_BG, anchor="w", wraplength=300, justify="left"
        )
        lbl_val.pack(side="left", fill="x", expand=True)
    
    def add_to_order(self):
        """Обработчик кнопки «Добавить в заказ» с использованием StringVar."""
        if not self.product:
            messagebox.showerror("Ошибка", "Товар не выбран")
            return

        try:
            # Читаем значение из переменной StringVar
            user_input = self.qty_var.get().strip()
            is_valid, result_value = validate_positive_int(user_input, "Количество для заказа")
            
            if not is_valid:
                messagebox.showerror("Ошибка валидации", str(result_value))
                return

            order_qty = int(result_value)
            
            product_id = getattr(self.product, 'id', None)
            if product_id is None:
                product_id = getattr(self.product, 'product_id', 0)
            
            current_qty = get_product_quantity(product_id)
            
            if current_qty < 1:
                messagebox.showwarning("Предупреждение", "Товар закончился")
                return
                
            if order_qty > current_qty:
                messagebox.showerror("Ошибка остатка", f"Недостаточно товара. В наличии: {current_qty} шт.")
                return
            
            new_qty = current_qty - order_qty
            
            # Считываем выбранную из выпадающего списка комплектацию
            chosen_size = self.size_var.get()
            client_name = f"Иванов Иван ({chosen_size})"
            
            add_order_to_db(client_name, product_id, order_qty)
            update_product_quantity(product_id, new_qty)
            
            messagebox.showinfo("Успех", f"Заказ оформлен! Выбрана комплектация: {chosen_size}")
            
            if self.on_add_to_order:
                self.on_add_to_order()
                
            self.window.destroy()
            
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось оформить заказ:\n{e}")
