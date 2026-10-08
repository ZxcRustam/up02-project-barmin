"""Стили приложения по руководству КИМ (Прил_3)."""
import tkinter as tk


# =========================================
# Цвета из руководства по стилю
# =========================================
COLOR_MAIN_BG = "#FFFFFF"       # основной фон
COLOR_SECONDARY_BG = "#D2F6E7"  # дополнительный фон
COLOR_ACCENT = "#70B2AF"        # акцент
COLOR_HIGHLIGHT = "#ff8080"     # подсветка ≤3

# =========================================
# Шрифт
# =========================================
FONT_FAMILY = "Calibri"
FONT_SIZE_SMALL = 10
FONT_SIZE_NORMAL = 12
FONT_SIZE_HEADER = 14
FONT_SIZE_TITLE = 18


def font(size=FONT_SIZE_NORMAL, bold=False):
    """Возвращает кортеж шрифта."""
    return (FONT_FAMILY, size, "bold" if bold else "normal")


def make_button(parent, text, command):
    """Кнопка в стиле КИМ."""
    return tk.Button(
        parent, text=text, command=command,
        bg=COLOR_ACCENT, fg="white",
        font=font(FONT_SIZE_NORMAL),
        relief="flat", padx=15, pady=5,
        activebackground=COLOR_ACCENT,
        cursor="hand2"
    )
