"""Работа с изображениями."""
import os
from typing import Optional

from PIL import Image, ImageTk


def load_image_proportional(image_path, max_size=(100, 100)):
    if not image_path or not os.path.exists(image_path):
        return None
    try:
        img = Image.open(image_path)
        img.thumbnail(max_size, Image.Resampling.LANCZOS)
        return ImageTk.PhotoImage(img)
    except Exception as e:
        print(f"Ошибка загрузки {image_path}: {e}")
        return None


def get_product_image(path: str, size: tuple = (100, 100)) -> Optional[ImageTk.PhotoImage]:
    try:
        img = Image.open(path)
        img = img.resize(size, Image.Resampling.LANCZOS)
        return ImageTk.PhotoImage(img)
    except Exception:
        return None
