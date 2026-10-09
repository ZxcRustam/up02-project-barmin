"""Окно состава заказа."""
import tkinter as tk
from tkinter import ttk, messagebox
from styles import (
    COLOR_MAIN_BG, COLOR_SECONDARY_BG, COLOR_ACCENT,
    FONT_SIZE_NORMAL, FONT_SIZE_TITLE, font
)
import order_manager as om


class OrderItemsWindow:
    """Окно состава заказа."""

    def __init__(self, parent, order_id):
        """
        Инициализация окна.
        :param parent: родительское окно
        :param order_id: id заказа
        """
        self.order_id = order_id
        self.window = tk.Toplevel(parent)
        self.window.title(f"Состав заказа №{order_id}")
        self.window.geometry("750x400")
        self.window.configure(bg=COLOR_MAIN_BG)

        self.build_ui()
        self.load_items()

    def build_ui(self):
        """Строит интерфейс окна."""
        # Шапка
        header = tk.Frame(self.window, bg=COLOR_SECONDARY_BG, height=60)
        header.pack(fill="x")
        header.pack_propagate(False)

        tk.Label(header, text=f"СОСТАВ ЗАКАЗА №{self.order_id}",
                 font=font(FONT_SIZE_TITLE, bold=True),
                 bg=COLOR_SECONDARY_BG).pack(pady=15)

        # Таблица позиций
        columns = ("name", "size", "quantity", "price", "total")
        self.tree = ttk.Treeview(self.window, columns=columns,
                                 show="headings", height=10)

        self.tree.heading("name", text="Автомобиль")
        self.tree.heading("size", text="Комплектация")
        self.tree.heading("quantity", text="Кол-во")
        self.tree.heading("price", text="Цена")
        self.tree.heading("total", text="Сумма")

        self.tree.column("name", width=250, anchor="w")
        self.tree.column("size", width=120, anchor="center")
        self.tree.column("quantity", width=70, anchor="center")
        self.tree.column("price", width=110, anchor="e")
        self.tree.column("total", width=110, anchor="e")

        self.tree.pack(fill="both", expand=True, padx=20, pady=20)

        # Итоговая сумма
        self.total_label = tk.Label(self.window, text="",
                                    font=font(FONT_SIZE_TITLE, bold=True),
                                    bg=COLOR_MAIN_BG)
        self.total_label.pack(pady=5)

        # Кнопки
        btn_frame = tk.Frame(self.window, bg=COLOR_MAIN_BG)
        btn_frame.pack(fill="x", pady=10)

        tk.Button(btn_frame, text="Назад",
                  command=self.window.destroy,
                  bg=COLOR_ACCENT, fg="white",
                  font=font(FONT_SIZE_NORMAL),
                  padx=15, pady=5, relief="flat", cursor="hand2").pack(side="right", padx=20)

    def load_items(self):
        """Загружает позиции заказа из БД."""
        for row in self.tree.get_children():
            self.tree.delete(row)

        try:
            # Извлекаем строки из базы данных по умному SQL-запросу
            items = om.get_order_items(self.order_id)
            total = 0.0

            for item in items:
                # ЧЕТКИЙ ПАРСИНГ ИНДЕКСОВ КОРТЕЖА ИЗ БД:
                # item[0] - id связи / заказа (не выводим)
                # item[1] - Товар.модель (название машины)
                # item[2] - Комплектация / размер
                # item[3] - Количество в заказе
                # item[4] - Цена автомобиля
                name = str(item[1])
                size = str(item[2])
                quantity = int(item[3])
                price = float(item[4])
                
                item_total = quantity * price
                total += item_total

                # Красивое разделение тысяч пробелами
                formatted_price = f"{price:,.2f}".replace(",", " ")
                formatted_total = f"{item_total:,.2f}".replace(",", " ")

                self.tree.insert("", tk.END,
                                 values=(name, size, quantity,
                                         formatted_price, formatted_total))

            formatted_grand_total = f"{total:,.2f}".replace(",", " ")
            self.total_label.config(text=f"Итого: {formatted_grand_total} руб.")

        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось загрузить состав заказа:\n{e}")
