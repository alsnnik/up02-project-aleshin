"""Каталог товаров."""
import tkinter as tk

from styles import (
    COLOR_MAIN_BG, COLOR_HIGHLIGHT,
    FONT_FAMILY, FONT_SIZE_NORMAL, FONT_SIZE_HEADER, font
)
from image_utils import get_product_image, load_image_proportional
from resource_paths import PATH_LOGO, PATH_ICON
import database as db


def create_product_card(parent, product):
    """Создаёт карточку товара по макету.
    Вариант 13: Смартфоны.
    Поля БД: id, бренд, модель, озу, цена, количество, изображение.
    """
    qty = product[5]                       # количество
    bg_color = _get_card_color(qty)

    card = tk.Frame(parent, bg=bg_color, bd=1, relief="solid")
    card.pack(fill="x", padx=10, pady=5)

    _add_image(card, product, bg_color)
    _add_text_info(card, product, bg_color, qty)

    return card


def _get_card_color(qty):
    """Возвращает цвет фона карточки (подсветка при qty <= 3)."""
    return COLOR_HIGHLIGHT if qty <= 3 else COLOR_MAIN_BG


def _add_image(card, product, bg_color):
    """Добавляет изображение товара (или заглушку)."""
    img_frame = tk.Frame(card, bg=bg_color)
    img_frame.pack(side="left", padx=10, pady=10)

    image_path = product[6] if product[6] else None
    photo = get_product_image(image_path, size=(100, 100)) if image_path else None

    if photo:
        img_label = tk.Label(img_frame, image=photo, bg=bg_color)
        img_label.image = photo
        img_label.pack()
    else:
        # Заглушка, если картинки нет
        tk.Label(img_frame, text="Нет фото", bg=bg_color,
                 width=10, height=5, relief="solid", bd=1).pack()


def _add_text_info(card, product, bg_color, qty):
    """Добавляет текстовую информацию о товаре (с обработкой крайних случаев)."""
    text_frame = tk.Frame(card, bg=bg_color)
    text_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)

    # --- Крайние случаи ---
    brand = product[1] if product[1] else "[Без бренда]"
    model = product[2] if product[2] else "[Без названия]"
    ram = product[3] if product[3] else "—"
    price = product[4] if product[4] is not None else 0
    qty = qty if qty is not None else 0

    # 1. Очень длинное название (> 100 символов) — обрезаем
    full_name = f"{brand} | {model}"
    if len(full_name) > 100:
        full_name = full_name[:97] + "..."

    # 2. Цена больше 1 000 000 — выводим с предупреждением
    if price > 1_000_000:
        price_text = f"{price} руб. ⚠️"
    else:
        price_text = f"{price} руб."

    # 3. Кириллица — tkinter с Calibri её поддерживает,
    #    ничего дополнительно делать не нужно.
    #    Проверка нужна только если шрифт не поддерживает Unicode.

    # --- Вывод ---
    _add_label(text_frame, full_name,
               bg_color, bold=True, size=FONT_SIZE_HEADER)
    _add_label(text_frame, f"ОЗУ: {ram} ГБ", bg_color)
    _add_label(text_frame, f"Количество: {_indicator(qty)} ({qty})", bg_color)
    _add_label(text_frame, price_text,
               bg_color, bold=True, size=FONT_SIZE_HEADER, align="e")


def _add_label(parent, text, bg_color, bold=False,
               size=FONT_SIZE_NORMAL, align="w"):
    """Добавляет метку с текстом."""
    tk.Label(parent, text=text, font=font(size, bold=bold),
             bg=bg_color, anchor=align).pack(fill="x")


def _indicator(qty):
    """
    Индикатор «много/мало» (порог 5 по КИМ).

    :param qty: количество товара
    :return: «много» или «мало»
    """
    return "много" if qty > 5 else "мало"