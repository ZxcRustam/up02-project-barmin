"""Модуль работы с ресурсами. Полная защита от ошибок кодирования текста и путей."""
import os
import io
from pathlib import Path
from PIL import Image, ImageTk

# Базовая директория проекта
BASE_DIR = Path(__file__).resolve().parent
PATH_PICTURE = BASE_DIR / "resources" / "picture.png"
PATH_LOGO = BASE_DIR / "resources" / "logo.png"
PATH_ICON = BASE_DIR / "resources" / "icon.ico"


def load_image(path_obj, size=(100, 100)):
    """Загружает изображение в виде байтов, обходя любые проблемы с кириллицей в путях."""
    try:
        p = Path(path_obj)
        sys_path = os.fsencode(str(p.resolve()))
        
        if not os.path.exists(sys_path):
            return None
            
        with open(sys_path, "rb") as f:
            img_bytes = io.BytesIO(f.read())
            img = Image.open(img_bytes).resize(size)
            
        return ImageTk.PhotoImage(img)
    except Exception as e:
        print(f"Ошибка загрузки {path_obj}: {e}")
        return None


def load_image_proportional(path_obj, max_size=(100, 100)):
    """Загружает изображение с сохранением пропорций (для логотипа)."""
    try:
        p = Path(path_obj)
        sys_path = os.fsencode(str(p.resolve()))
        
        if not os.path.exists(sys_path):
            return None
            
        with open(sys_path, "rb") as f:
            img_bytes = io.BytesIO(f.read())
            img = Image.open(img_bytes)
            img.thumbnail(max_size)
            
        return ImageTk.PhotoImage(img)
    except Exception as e:
        print(f"Ошибка загрузки {path_obj}: {e}")
        return None


def get_product_image(image_path, size=(100, 100)):
    """Возвращает картинку товара или заглушку."""
    if not image_path:
        return load_image(PATH_PICTURE, size)
        
    p = Path(image_path)
    if not p.is_absolute():
        p = BASE_DIR / image_path
        
    sys_path = os.fsencode(str(p.resolve()))
    if not os.path.exists(sys_path):
        return load_image(PATH_PICTURE, size)
        
    return load_image(p, size)
