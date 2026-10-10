"""Окно состава заказа с правами редактирования для Администратора (Вариант 22)."""
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from styles import (
    COLOR_MAIN_BG, COLOR_SECONDARY_BG, COLOR_ACCENT,
    FONT_SIZE_NORMAL, FONT_SIZE_TITLE, font
)
import order_manager as om


class OrderItemsWindow:
    """Окно состава заказа."""

    def __init__(self, parent, order_id, current_user=None):
        """
        Инициализация окна.
        :param parent: родительское окно
        :param order_id: id заказа
        :param current_user: текущий пользователь сессии
        """
        self.order_id = order_id
        self.current_user = current_user

        self.window = tk.Toplevel(parent)
        self.window.title(f"Состав заказа №{order_id}")
        self.window.geometry("900x600")
        self.window.configure(bg=COLOR_MAIN_BG)

        self.build_ui()
        self.load_order_info()
        self.load_items()

    def is_admin(self):
        """Проверяет, является ли пользователь Администратором (Задание 6.2)."""
        return bool(self.current_user and len(self.current_user) > 5 and self.current_user[5] == "Администратор")

    def build_ui(self):
        """Строит интерфейс окна."""
        # Шапка
        header = tk.Frame(self.window, bg=COLOR_SECONDARY_BG, height=60)
        header.pack(fill="x")
        header.pack_propagate(False)

        tk.Label(header, text=f"СОСТАВ ЗАКАЗА №{self.order_id}",
                 font=font(FONT_SIZE_TITLE, bold=True),
                 bg=COLOR_SECONDARY_BG).pack(pady=15)

        # Информация о заказе (Задание 6.2)
        info_frame = tk.Frame(self.window, bg=COLOR_MAIN_BG)
        info_frame.pack(fill="x", padx=20, pady=10)

        tk.Label(info_frame, text="Дата заказа:",
                 font=font(FONT_SIZE_NORMAL, bold=True),
                 bg=COLOR_MAIN_BG).pack(side="left", padx=5)

        self.date_var = tk.StringVar()
        self.date_entry = tk.Entry(info_frame, textvariable=self.date_var,
                                   width=15, font=font(FONT_SIZE_NORMAL),
                                   relief="solid")
        self.date_entry.pack(side="left", padx=5)
        self.date_entry.config(state="readonly")

        # Если зашел Админ — открываем доступ к редактированию даты (Задание 6.4)
        if self.is_admin():
            self.date_entry.config(state="normal")
            tk.Button(info_frame, text="Сохранить дату",
                      command=self.save_date,
                      bg=COLOR_ACCENT, fg="white",
                      font=font(FONT_SIZE_NORMAL, bold=True),
                      relief="flat", cursor="hand2",
                      padx=10, pady=3).pack(side="left", padx=10)

        tk.Label(info_frame, text="Клиент:",
                 font=font(FONT_SIZE_NORMAL, bold=True),
                 bg=COLOR_MAIN_BG).pack(side="left", padx=20)

        self.client_label = tk.Label(info_frame, text="",
                                     font=font(FONT_SIZE_NORMAL),
                                     bg=COLOR_MAIN_BG)
        self.client_label.pack(side="left")

        # Таблица позиций КИМ (Задание 6.2)
        columns = ("id", "name", "size", "quantity", "price", "total")
        self.tree = ttk.Treeview(self.window, columns=columns,
                                 show="headings", height=12)

        self.tree.heading("id", text="№ Позиции")
        self.tree.heading("name", text="Автомобиль")
        self.tree.heading("size", text="Комплектация")
        self.tree.heading("quantity", text="Кол-во")
        self.tree.heading("price", text="Цена")
        self.tree.heading("total", text="Сумма")

        self.tree.column("id", width=80, anchor="center")
        self.tree.column("name", width=250, anchor="w")
        self.tree.column("size", width=120, anchor="center")
        self.tree.column("quantity", width=70, anchor="center")
        self.tree.column("price", width=100, anchor="e")
        self.tree.column("total", width=100, anchor="e")

        self.tree.pack(fill="both", expand=True, padx=20, pady=10)

        # Итоговая сумма
        self.total_label = tk.Label(self.window, text="",
                                    font=font(FONT_SIZE_TITLE, bold=True),
                                    fg=COLOR_ACCENT,
                                    bg=COLOR_MAIN_BG)
        self.total_label.pack(pady=5)

        # Кнопки управления (Задание 6.2)
        btn_frame = tk.Frame(self.window, bg=COLOR_MAIN_BG)
        btn_frame.pack(fill="x", pady=10)

        # Если Админ — выводим кнопку удаления строки состава (Задание 6.4)
        if self.is_admin():
            tk.Button(btn_frame, text="Удалить позицию",
                      command=self.delete_item,
                      bg="#ff8080", fg="white",
                      font=font(FONT_SIZE_NORMAL, bold=True),
                      relief="flat", cursor="hand2",
                      padx=15, pady=5).pack(side="left", padx=20)

        tk.Button(btn_frame, text="Обновить",
                  command=self.refresh_all,
                  bg=COLOR_ACCENT, fg="white",
                  font=font(FONT_SIZE_NORMAL, bold=True),
                  relief="flat", cursor="hand2",
                  padx=15, pady=5).pack(side="left", padx=10)

        tk.Button(btn_frame, text="Назад",
                  command=self.window.destroy,
                  bg=COLOR_ACCENT, fg="white",
                  font=font(FONT_SIZE_NORMAL),
                  relief="flat", cursor="hand2",
                  padx=15, pady=5).pack(side="right", padx=20)

    def load_order_info(self):
        """Загружает информацию о заказе."""
        order = om.get_order_by_id(self.order_id)
        if order:
            self.date_var.set(str(order[1]))
            self.client_label.config(text=str(order[2]))

    def load_items(self):
        """Загружает позиции заказа с адаптацией под Вариант 22."""
        for row in self.tree.get_children():
            self.tree.delete(row)

        try:
            items = om.get_order_items(self.order_id)

            if not items:
                messagebox.showinfo("Информация", "Заказ пуст")
                self.total_label.config(text="ИТОГО: 0.00 руб.")
                return

            for item in items:
                item_id = item[0]
                brand = str(item[1])
                model = str(item[2])
                name = f"{brand} {model}"  # Специфика автомобилей
                
                size = str(item[3])        # Комплектация
                quantity = int(item[4])
                price = float(item[5])
                item_total = quantity * price

                formatted_price = f"{price:,.2f}".replace(",", " ")
                formatted_total = f"{item_total:,.2f}".replace(",", " ")

                self.tree.insert("", tk.END,
                                 values=(item_id, name, size,
                                         quantity, formatted_price, formatted_total))

            total = om.get_order_total(self.order_id)
            formatted_grand_total = f"{total:,.2f}".replace(",", " ")
            self.total_label.config(text=f"ИТОГО ПО ЗАКАЗУ: {formatted_grand_total} руб.")

        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось загрузить состав:\n{e}")

    def save_date(self):
        """Сохраняет изменённую дату (Задание 6.2)."""
        new_date = self.date_var.get().strip()

        # Валидация формата ГГГГ-ММ-ДД
        try:
            datetime.strptime(new_date, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Ошибка формата", "Неверный формат даты! Используйте шаблон: ГГГГ-ММ-ДД")
            return

        if om.update_order_date(self.order_id, new_date):
            messagebox.showinfo("Успех", "Дата заказа успешно обновлена в БД!")
            self.refresh_all()
        else:
            messagebox.showerror("Ошибка", "Не удалось обновить дату заказа")

    def delete_item(self):
        """Удаляет выбранную позицию с возвратом остатков (Задание 6.2)."""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Ошибка выбора", "Пожалуйста, выберите позицию в таблице")
            return

        item_data = self.tree.item(selected[0])
        order_values = item_data.get("values")
        if not order_values:
            return
            
        item_id = order_values[0]

        if not messagebox.askyesno("Подтверждение удаления", f"Вы уверены, что хотите удалить позицию №{item_id}?\nТовар вернется на склад."):
            return

        if om.delete_order_item(item_id):
            messagebox.showinfo("Успех", "Позиция успешно удалена, остатки на складе восстановлены!")
            self.refresh_all()
        else:
            messagebox.showerror("Ошибка", "Не удалось удалить позицию")

    def refresh_all(self):
        """Обновляет всю информацию в окне."""
        self.load_order_info()
        self.load_items()
