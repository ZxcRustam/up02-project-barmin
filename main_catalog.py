"""Главное окно приложения с каталогом (Вариант 22: Автомобили)."""

import sqlite3
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

# Безопасный импорт конфигурации
try:
    import config
    DB_PATH = getattr(config, "DB_PATH", "databases/db_variant_22.db")
    APP_TITLE = getattr(config, "APP_TITLE", "Автосалон — Вариант 22")
    FONT_FAMILY = getattr(config, "FONT_FAMILY", "Arial")
except ImportError:
    DB_PATH = "databases/db_variant_22.db"
    APP_TITLE = "Автосалон — Вариант 22"
    FONT_FAMILY = "Arial"

from models import Product
from catalog import create_product_card


class CatalogWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title(APP_TITLE)
        self.root.geometry("900x700")

        self.build_ui()
        self.load_products()

    def build_ui(self):
        # Заголовок (Нежно-зелёный фон по ТЗ ДЭ)
        header = tk.Frame(self.root, bg="#D2F6E7")
        header.pack(fill="x")

        # ЗАДАНИЕ 2. Добавление логотипы компании в шапку каталога
        try:
            logo = Image.open("resources/logo.png").resize((50, 50))
            logo_photo = ImageTk.PhotoImage(logo)
            logo_label = tk.Label(header, image=logo_photo, bg="#D2F6E7")
            logo_label.__dict__['image'] = logo_photo  # защищаем ссылку от сборщика мусора
            logo_label.pack(side="left", padx=20, pady=10)
        except Exception:
            # Если файла нет — создаем пустой отступ, чтобы верстка не поехала
            tk.Frame(header, bg="#D2F6E7", width=50).pack(side="left")

        tk.Label(header, text="КАТАЛОГ АВТОМОБИЛЕЙ",
                 font=(FONT_FAMILY, 16, "bold"),
                 bg="#D2F6E7").pack(side="left", pady=15, expand=True, anchor="center")
        
        # Дополнительный невидимый элемент справа для идеального центрирования текста из-за логотипа
        tk.Frame(header, bg="#D2F6E7", width=70).pack(side="right")

        # Область с прокруткой (Canvas + Scrollbar)
        self.canvas = tk.Canvas(self.root, bg="white", highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.root, orient="vertical", command=self.canvas.yview)
        
        self.catalog_frame = tk.Frame(self.canvas, bg="white")
        
        # Настройка области прокрутки
        self.catalog_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        
        # Растягиваем контейнер карточек по ширине окна
        self.canvas_window = self.canvas.create_window((0, 0), window=self.catalog_frame, anchor="nw")
        self.canvas.bind('<Configure>', lambda e: self.canvas.itemconfig(self.canvas_window, width=e.width))
        
        self.canvas.configure(yscrollcommand=scrollbar.set)
        
        # Размещение на экране
        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def load_products(self):
        """Прямая загрузка автомобилей из базы Варианта 22 и создание объектов класса Product."""
        try:
            conn = sqlite3.connect(DB_PATH)
            cur = conn.cursor()
            cur.execute("SELECT * FROM Товар")
            rows = cur.fetchall()
            conn.close()

            for r in rows:
                product_obj = Product(r[0], r[1], r[2], r[3], r[4], r[5], r[6])
                create_product_card(self.catalog_frame, product_obj)
        except Exception as e:
            tk.Label(self.catalog_frame, text=f"Ошибка загрузки БД: {e}", 
                     fg="red", bg="white", font=(FONT_FAMILY, 12)).pack(pady=20)

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    CatalogWindow().run()
