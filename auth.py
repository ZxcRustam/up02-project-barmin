"""Авторизация пользователей."""
import tkinter as tk
from tkinter import messagebox
from styles import (
    COLOR_MAIN_BG, COLOR_SECONDARY_BG, COLOR_ACCENT,
    FONT_SIZE_NORMAL, FONT_SIZE_TITLE, font
)
from database import get_user_by_login


class AuthWindow:
    """Окно авторизации."""

    def __init__(self, root, on_success):
        """
        Инициализация окна.
        :param root: главное окно
        :param on_success: callback при успешной авторизации
        """
        self.root = root
        self.on_success = on_success
        self.current_user = None

        self.window = tk.Toplevel(root)
        self.window.title("Авторизация")
        self.window.geometry("400x300")
        self.window.configure(bg=COLOR_MAIN_BG)
        self.window.grab_set()

        self.build_ui()

    def build_ui(self):
        """Строит интерфейс окна."""
        # Шапка
        header = tk.Frame(self.window, bg=COLOR_SECONDARY_BG, height=60)
        header.pack(fill="x")
        header.pack_propagate(False)

        tk.Label(header, text="ВХОД В СИСТЕМУ",
                 font=font(FONT_SIZE_TITLE, bold=True),
                 bg=COLOR_SECONDARY_BG).pack(pady=15)

        # Логин
        form = tk.Frame(self.window, bg=COLOR_MAIN_BG)
        form.pack(pady=30)

        tk.Label(form, text="Логин:", font=font(FONT_SIZE_NORMAL),
                 bg=COLOR_MAIN_BG).pack(anchor="w")

        self.login_var = tk.StringVar()
        tk.Entry(form, textvariable=self.login_var, width=30,
                 font=font(FONT_SIZE_NORMAL)).pack(pady=5)

        # Кнопка
        tk.Button(form, text="Войти", command=self.login,
                  bg=COLOR_ACCENT, fg="white",
                  font=font(FONT_SIZE_NORMAL),
                  padx=20, pady=5).pack(pady=15)

        # Подсказка
        tk.Label(form, text="Пример: manager1, admin1, client1",
                 font=font(FONT_SIZE_NORMAL),
                 fg="gray", bg=COLOR_MAIN_BG).pack()

    def login(self):
        """Обработчик входа."""
        login = self.login_var.get().strip()

        if not login:
            messagebox.showwarning("Ошибка", "Введите логин")
            return

        user = get_user_by_login(login)

        if not user:
            messagebox.showerror("Ошибка", "Пользователь не найден")
            return

        self.current_user = user
        messagebox.showinfo("Успех", f"Добро пожаловать, {user[1]}!")
        self.window.destroy()
        self.on_success(user)
