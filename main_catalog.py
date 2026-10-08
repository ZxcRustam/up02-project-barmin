"""Главное окно приложения с каталогом (Вариант 22: Автомобили)."""

import sqlite3
import tkinter as tk
from tkinter import ttk

# Официальный импорт настроек из config
from config import DB_PATH, APP_TITLE

# Задание 7.4. Официальный импорт стилей КИМ
from styles import COLOR_MAIN_BG, COLOR_SECONDARY_BG, FONT_SIZE_TITLE, font
from models import Product
from catalog import create_product_card
from resources import load_image_proportional, PATH_LOGO, PATH_ICON


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
        self.root.geometry("900x700")
        
        # Задание 7.6. Устанавливаем основной фон окна из КИМ
        self.root.configure(bg=COLOR_MAIN_BG)

        set_app_icon(self.root, PATH_ICON)

        self.build_ui()
        self.load_products()

    def build_ui(self):
        # Шапка с логотипом и заголовком (Задание 7.6. Цвет COLOR_SECONDARY_BG)
        header = tk.Frame(self.root, bg=COLOR_SECONDARY_BG, height=80)
        header.pack(fill="x")
        header.pack_propagate(False)

        logo = load_image_proportional(PATH_LOGO, max_size=(60, 60))
        if logo:
            logo_label = tk.Label(header, image=logo, bg=COLOR_SECONDARY_BG)
            logo_label.__dict__['image'] = logo  
            logo_label.pack(side="left", padx=15)
        else:
            tk.Label(header, text="[ЛОГОТИП]", bg=COLOR_SECONDARY_BG).pack(side="left", padx=15)

        # Заголовок по центру (Задание 7.5. Шрифт Calibri TITLE через font())
        tk.Label(header, text="КАТАЛОГ АВТОМОБИЛЕЙ",
                 font=font(FONT_SIZE_TITLE, bold=True),
                 bg=COLOR_SECONDARY_BG).pack(expand=True)

        # Область с прокруткой (Canvas + Scrollbar)
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

    def load_products(self):
        """Прямая загрузка автомобилей из базы Варианта 22 и создание объектов Product."""
        try:
            conn = sqlite3.connect(DB_PATH)
            cur = conn.cursor()
            cur.execute("SELECT * FROM Товар")
            rows = cur.fetchall()
            conn.close()

            for r in rows:
                product_obj = Product(
                    product_id=int(r[0]),
                    brand=str(r[1]),
                    model=str(r[2]),
                    year=int(r[3]),
                    price=int(r[4]),
                    quantity=int(r[5]),
                    photo=str(r[6]) if r[6] else ""
                )
                create_product_card(self.catalog_frame, product_obj)
        except Exception as e:
            tk.Label(self.catalog_frame, text=f"Ошибка загрузки БД: {e}", 
                     fg="red", bg=COLOR_MAIN_BG, font=font(FONT_SIZE_TITLE)).pack(pady=20)

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    CatalogWindow().run()
