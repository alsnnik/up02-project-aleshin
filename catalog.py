"""Каталог товаров."""
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import os

from config import COLOR_HIGHLIGHT, FONT_FAMILY
import database as db


def create_product_card(parent, product):
    """
    Создаёт карточку товара по макету.
    Вариант 13: Смартфоны.
    Поля БД: id, бренд, модель, озу, цена, количество, изображение
    """
    # Индексы для варианта 13
    brand      = product[1]   # бренд
    model      = product[2]   # модель
    ram        = product[3]   # озу
    price      = product[4]   # цена
    qty        = product[5]   # количество
    image_path = product[6]   # изображение

    # Фон: подсветка, если количество ≤3
    bg_color = COLOR_HIGHLIGHT if qty <= 3 else "white"

    # Карточка — рамка со всех сторон
    card = tk.Frame(parent, bg=bg_color, bd=1, relief="solid")
    card.pack(fill="x", padx=10, pady=5)

    # Изображение (слева) 
    img_frame = tk.Frame(card, bg=bg_color)
    img_frame.pack(side="left", padx=10, pady=10)

    if not image_path or not os.path.exists(image_path):
        image_path = "resources/picture.png"

    try:
        img = Image.open(image_path).resize((100, 100))
        photo = ImageTk.PhotoImage(img)
        img_label = tk.Label(img_frame, image=photo, bg=bg_color)
        img_label.image = photo   # type: ignore  # сохраняем ссылку!
        img_label.pack()
    except Exception:
        tk.Label(img_frame, text="[ФОТО]", bg=bg_color,
                 width=10, height=5).pack()

    # Текстовая часть (справа)
    text_frame = tk.Frame(card, bg=bg_color)
    text_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)

    # Производство | Наименование  →  бренд | модель
    title = f"{brand} | {model}"
    tk.Label(text_frame, text=title, font=(FONT_FAMILY, 14, "bold"),
             bg=bg_color, anchor="w").pack(fill="x")

    # Категория
    tk.Label(text_frame, text="Категория: Смартфоны",
             font=(FONT_FAMILY, 11), bg=bg_color, anchor="w").pack(fill="x")

    # Количество
    indicator = "много" if qty > 5 else "мало"
    tk.Label(text_frame, text=f"Количество: {indicator} ({qty})",
             font=(FONT_FAMILY, 11), bg=bg_color, anchor="w").pack(fill="x")

    # Состав  →  озу (характеристика смартфона)
    tk.Label(text_frame, text=f"ОЗУ: {ram} ГБ",
             font=(FONT_FAMILY, 11), bg=bg_color, anchor="w").pack(fill="x")

    # Цена (справа, внизу) 
    price_label = tk.Label(text_frame, text=f"{price} руб.",
                           font=(FONT_FAMILY, 14, "bold"),
                           bg=bg_color)
    price_label.pack(side="bottom", anchor="e", fill="x")

    return card