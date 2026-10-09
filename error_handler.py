"""Модуль безопасного вызова функций и валидации данных."""
from tkinter import messagebox


def safe_call(func, *args, **kwargs):
    """Безопасный вызов функции."""
    try:
        return func(*args, **kwargs)
    except FileNotFoundError as e:
        messagebox.showerror("Ошибка файла", f"Файл не найден:\n{e}")
    except ConnectionError as e:
        messagebox.showerror("Ошибка сети", f"Ошибка подключения к базе данных или серверу:\n{e}")
    except ValueError as e:
        messagebox.showwarning("Предупреждение", f"Некорректное значение данных:\n{e}")
    except Exception as e:
        messagebox.showerror("Критическая ошибка", f"Произошел непредвиденный сбой:\n{e}")
    
    return None


def validate_positive_int(value, field_name="Значение"):
    """Проверяет, что значение — положительное целое число."""
    try:
        number = int(value)
        if number <= 0:
            return (False, f"{field_name} должно быть больше нуля")
        return (True, number)
    except (ValueError, TypeError):
        return (False, f"{field_name} должно быть целым числом")
