"""Модуль работы с ресурсами."""
import os
from PIL import Image, ImageTk


# Пути к ресурсам
PATH_PICTURE = "resources/picture.png"
PATH_LOGO = "resources/logo.png"
PATH_ICON = "resources/icon.ico"

# Кэш изображений
_image_cache = {}


def load_image(path, size=(100, 100)):
    """
    Загружает изображение с указанным размером.
    
    :param path: путь к файлу
    :param size: (ширина, высота)
    :return: ImageTk.PhotoImage или None
    """
    try:
        if not os.path.exists(path):
            return None
        img = Image.open(path).resize(size)
        return ImageTk.PhotoImage(img)
    except Exception as e:
        print(f"Ошибка загрузки {path}: {e}")
        return None


def load_image_proportional(path, max_size=(100, 100)):
    """
    Загружает изображение с сохранением пропорций.
    Используется для логотипа.
    
    :param path: путь к файлу
    :param max_size: максимальные (ширина, высота)
    :return: ImageTk.PhotoImage или None
    """
    try:
        if not os.path.exists(path):
            return None
        img = Image.open(path)
        img.thumbnail(max_size)   # сохраняет пропорции!
        return ImageTk.PhotoImage(img)
    except Exception as e:
        print(f"Ошибка загрузки {path}: {e}")
        return None


def get_product_image(image_path, size=(100, 100)):
    """
    Возвращает картинку товара или заглушку.
    
    :param image_path: путь к изображению товара
    :param size: (ширина, высота)
    :return: ImageTk.PhotoImage
    """
    if not image_path or not os.path.exists(image_path):
        return load_image(PATH_PICTURE, size)
    return load_image(image_path, size)
