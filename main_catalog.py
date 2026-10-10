"""Главное окно приложения с каталогом и разграничением прав (Вариант 22: Автомобили)."""

import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox

from config import DB_PATH, APP_TITLE
from styles import COLOR_MAIN_BG, COLOR_SECONDARY_BG, COLOR_ACCENT, FONT_SIZE_TITLE, FONT_SIZE_NORMAL, font
from models import Product
from catalog import create_product_card
from resources import load_image_proportional, PATH_LOGO, PATH_ICON
from error_handler import safe_call


def set_app_icon(root, icon_path):
    """Устанавливает иконку приложения кроссплатформенно."""
    import os
    try:
        if os.name == "nt":   
            if os.path.exists(icon_path):
                root.iconbitmap(icon_path)
        else:                  
            png_path = icon_path.replace(".ico", ".png")
            icon_img = load_image_proportional(png_path, max_size=(32, 32))
            if icon_img:
                root.iconphoto(True, icon_img)
                root._icon_photo = icon_img   
    except Exception as e:
        print(f"Не удалось установить иконку: {e}")


class CatalogWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title(APP_TITLE)
        self.root.geometry("950x700")
        
        self.current_user = None
        self.user_label = tk.Label()  # Инициализация пустым виджетом во избежание None-ошибок
        self.header_frame = None
        
        self.root.configure(bg=COLOR_MAIN_BG)
        set_app_icon(self.root, PATH_ICON)

        self.build_ui()
        self.load_products()
        self.require_auth()

    def build_ui(self):
        """Строит интерфейс окна."""
        self.header_frame = tk.Frame(self.root, bg=COLOR_SECONDARY_BG, height=80)
        self.header_frame.pack(fill="x")
        self.header_frame.pack_propagate(False)

        logo = load_image_proportional(PATH_LOGO, max_size=(60, 60))
        if logo:
            logo_label = tk.Label(self.header_frame, image=logo, bg=COLOR_SECONDARY_BG)
            logo_label.__dict__['image'] = logo  
            logo_label.pack(side="left", padx=15)
        else:
            tk.Label(self.header_frame, text="[ЛОГОТИП]", bg=COLOR_SECONDARY_BG).pack(side="left", padx=15)

        tk.Label(self.header_frame, text="КАТАЛОГ АВТОМОБИЛЕЙ",
                 font=font(FONT_SIZE_TITLE, bold=True),
                 bg=COLOR_SECONDARY_BG).pack(side="left", padx=(30, 0))

        self.user_label = tk.Label(self.header_frame, text="Не авторизован",
                                   font=font(FONT_SIZE_NORMAL, bold=True),
                                   bg=COLOR_SECONDARY_BG)
        self.user_label.pack(side="right", padx=15)

        self.canvas = tk.Canvas(self.root, bg=COLOR_MAIN_BG, highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.root, orient="vertical", command=self.canvas.yview)
        
        self.catalog_frame = tk.Frame(self.canvas, bg=COLOR_MAIN_BG)
        
        self.catalog_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        
        self.canvas_window = self.canvas.create_window((0, 0), window=self.catalog_frame, anchor="nw")
        self.canvas.bind('<Configure>', lambda e: self.canvas.itemconfig(self.canvas_window, width=e.width))
        
        self.canvas.configure(yscrollcommand=scrollbar.set)
        
        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def require_auth(self):
        """Запрашивает авторизацию при старте."""
        from auth import AuthWindow
        AuthWindow(self.root, self.on_auth_success)

    def on_auth_success(self, user):
        """Обработчик успешного входа."""
        self.current_user = user
        if user and len(user) > 5:
            fio = f"{user[1]} {user[2]} {user[3] or ''}".strip()
            role_name = str(user[5])
            self.user_label.config(text=f"{fio}\n({role_name})")
            self.add_role_buttons(role_name)

    def add_role_buttons(self, role):
        """Выводит кнопки по ролям."""
        if role in ("Менеджер", "Администратор") and self.header_frame:
            btn_orders = tk.Button(
                self.header_frame, text="Заказы", command=self.open_orders,
                bg=COLOR_ACCENT, fg="white", font=font(FONT_SIZE_NORMAL, bold=True),
                relief="flat", cursor="hand2", padx=15, pady=5
            )
            btn_orders.pack(side="right", padx=15, pady=20)

        if role == "Администратор" and self.header_frame:
            btn_admin = tk.Button(
                self.header_frame, text="Админ-панель", command=self.open_admin,
                bg=COLOR_ACCENT, fg="white", font=font(FONT_SIZE_NORMAL, bold=True),
                relief="flat", cursor="hand2", padx=15, pady=5
            )
            btn_admin.pack(side="right", padx=10, pady=20)

    def open_orders(self):
        """Открывает окно списка заказов."""
        from orders_window import OrdersWindow
        OrdersWindow(self.root, self.current_user)

    def open_admin(self):
        """Заглушка для окна админ-панели."""
        messagebox.showinfo("Админ-панель", "Модуль Администратора будет добавлен в следующем задании.")

    def _fetch_products_from_db(self):
        """Извлечение строк из БД."""
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        cur.execute("SELECT * FROM Товар")
        rows = cur.fetchall()
        conn.close()
        return rows

    def refresh_catalog(self):
        """Обновляет содержимое витрины каталога."""
        for widget in self.catalog_frame.winfo_children():
            widget.destroy()
        self.load_products()

    def load_products(self):
        """Загружает товары."""
        rows = safe_call(self._fetch_products_from_db)
        if rows is None:
            rows = []

        for r in rows:
            try:
                product_obj = Product(
                    product_id=int(r[0]) if r[0] is not None else 0,
                    brand=str(r[1]) if r[1] else "[Без марки]",
                    model=str(r[2]) if r[2] else "[Без модели]",
                    year=int(r[3]) if r[3] is not None else 0,
                    price=int(r[4]) if r[4] is not None else 0,
                    quantity=int(r[5]) if r[5] is not None else 0,
                    photo=str(r[6]) if len(r) > 6 and r[6] else ""
                )
                safe_call(create_product_card, self.catalog_frame, product_obj, refresh=self.refresh_catalog)
            except Exception as e:
                print(f"[DEBUG] Ошибка парсинга строки продукта: {e}")

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    CatalogWindow().run()
