"""Окно списка заказов для Менеджера."""
import tkinter as tk
from tkinter import ttk, messagebox
from styles import (
    COLOR_MAIN_BG, COLOR_SECONDARY_BG, COLOR_ACCENT,
    FONT_SIZE_NORMAL, FONT_SIZE_HEADER, FONT_SIZE_TITLE, font
)
import order_manager as om


class OrdersWindow:
    """Окно списка заказов."""

    def __init__(self, parent, current_user=None):
        """
        Инициализация окна списка заказов (Задание 6.3).
        :param parent: родительское окно
        :param current_user: кортеж текущего авторизованного пользователя
        """
        self.current_user = current_user
        self.window = tk.Toplevel(parent)
        self.window.title("Список заказов")
        self.window.geometry("800x500")
        self.window.configure(bg=COLOR_MAIN_BG)

        self.build_ui()
        self.load_orders()

    def build_ui(self):
        """Строит интерфейс окна."""
        # Шапка
        header = tk.Frame(self.window, bg=COLOR_SECONDARY_BG, height=60)
        header.pack(fill="x")
        header.pack_propagate(False)

        tk.Label(header, text="СПИСОК ЗАКАЗОВ",
                 font=font(FONT_SIZE_TITLE, bold=True),
                 bg=COLOR_SECONDARY_BG).pack(pady=15)

        # Таблица заказов
        columns = ("id", "date", "client")
        self.tree = ttk.Treeview(self.window, columns=columns,
                                 show="headings", height=15)

        self.tree.heading("id", text="№")
        self.tree.heading("date", text="Дата")
        self.tree.heading("client", text="Клиент")

        self.tree.column("id", width=50, anchor="center")
        self.tree.column("date", width=120, anchor="center")
        self.tree.column("client", width=400, anchor="w")

        self.tree.pack(fill="both", expand=True, padx=20, pady=20)

        # Привязка двойного клика
        self.tree.bind("<Double-1>", self.on_order_select)

        # Кнопки
        btn_frame = tk.Frame(self.window, bg=COLOR_MAIN_BG)
        btn_frame.pack(fill="x", pady=10)

        tk.Button(btn_frame, text="Просмотр состава",
                  command=self.on_order_select,
                  bg=COLOR_ACCENT, fg="white",
                  font=font(FONT_SIZE_NORMAL),
                  padx=15, pady=5, relief="flat", cursor="hand2").pack(side="left", padx=20)

        tk.Button(btn_frame, text="Обновить",
                  command=self.load_orders,
                  bg=COLOR_ACCENT, fg="white",
                  font=font(FONT_SIZE_NORMAL),
                  padx=15, pady=5, relief="flat", cursor="hand2").pack(side="left", padx=10)

        tk.Button(btn_frame, text="Назад",
                  command=self.window.destroy,
                  bg=COLOR_ACCENT, fg="white",
                  font=font(FONT_SIZE_NORMAL),
                  padx=15, pady=5, relief="flat", cursor="hand2").pack(side="right", padx=20)

    def load_orders(self):
        """Загружает заказы из БД."""
        for row in self.tree.get_children():
            self.tree.delete(row)

        try:
            orders = om.get_all_orders()
            for order in orders:
                self.tree.insert("", tk.END, values=order)
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось загрузить заказы:\n{e}")

    def on_order_select(self, event=None):
        """Обработчик выбора заказа."""
        selected = self.tree.selection()
        if not selected:
            if event is not None:
                return
            messagebox.showwarning("Ошибка", "Выберите заказ")
            return

        item = self.tree.item(selected[0])
        order_values = item.get("values")
        
        if not order_values:
            return
            
        order_id = order_values[0]

        # ИСПРАВЛЕНО: Передаем сессию текущего пользователя current_user
        from order_items_window import OrderItemsWindow
        OrderItemsWindow(self.window, order_id, current_user=self.current_user)

