"""Модуль для работы с изображениями."""
import os
from PIL import Image, ImageTk

# Пути к ресурсам
PATH_LOGO = "resources/logo.png"
PATH_ICON = "resources/icon.ico"
PATH_PICTURE = "resources/picture.png"


def load_image_proportional(image_path, max_size=(100, 100)):
    """Загружает изображение с сохранением пропорций."""
    if not image_path or not os.path.exists(image_path):
        return None
    try:
        img = Image.open(image_path)
        img.thumbnail(max_size, Image.LANCZOS)
        return ImageTk.PhotoImage(img)
    except Exception as e:
        print(f"Ошибка загрузки {image_path}: {e}")
        return None


def get_product_image(image_path, size=(100, 100)):
    """Возвращает картинку товара или None."""
    if not image_path or not os.path.exists(image_path):
        return None
    try:
        img = Image.open(image_path).resize(size)
        return ImageTk.PhotoImage(img)
    except Exception:
        return None