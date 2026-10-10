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
    Вариант 13 «Смартфоны»: id, бренд, модель, озу, цена, количество, изображение.
    """
    qty = product[5]
    bg_color = _get_card_color(qty)

    card = tk.Frame(parent, bg=bg_color, bd=1, relief="solid")
    card.pack(fill="x", padx=10, pady=5)

    _add_image(card, product, bg_color)
    _add_text_info(card, product, bg_color, qty)

    # Привязка клика ко всем вложенным элементам карточки
    _bind_recursive(card, parent, product)

    return card


def _bind_recursive(widget, parent, product):
    """Рекурсивно привязывает клик ко всем дочерним виджетам."""
    widget.bind("<Button-1>", lambda e, p=product: _open_view(parent, p))
    for child in widget.winfo_children():
        _bind_recursive(child, parent, product)


def _open_view(parent, product):
    """Открывает форму просмотра товара."""
    from view_form import ViewForm
    ViewForm(parent, product)

def _get_card_color(qty):
    """Возвращает цвет фона карточки (подсветка при qty <= 3)."""
    return COLOR_HIGHLIGHT if qty <= 3 else COLOR_MAIN_BG


def _add_image(card, product, bg_color):
    """Добавляет изображение товара (или заглушку)."""
    img_frame = tk.Frame(card, bg=bg_color)      # ✅ bg_color
    img_frame.pack(side="left", padx=10, pady=10)

    image_path = product[6]                       # изображение (ваш индекс!)
    photo = get_product_image(image_path, size=(100, 100))
    if photo:
        img_label = tk.Label(img_frame, image=photo, bg=bg_color)   
        img_label.image = photo
        img_label.pack()
    else:
        tk.Label(img_frame, text="Нет фото", bg=bg_color,           
                 width=10, height=5).pack()


def _add_text_info(card, product, bg_color, qty):
    """Добавляет текстовую информацию о товаре."""
    text_frame = tk.Frame(card, bg=bg_color)
    text_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)

    # --- Крайние случаи ---
    brand = product[1] if product[1] else "[Без бренда]"
    model = product[2] if product[2] else "[Без названия]"
    ram = product[3] if product[3] else "—"
    price = product[4] if product[4] is not None else 0
    qty = qty if qty is not None else 0

    # Обрезаем слишком длинное название
    full_name = f"{brand} | {model}"
    if len(full_name) > 100:
        full_name = full_name[:97] + "..."

    # --- Вывод ---
    _add_label(text_frame, full_name,
               bg_color, bold=True, size=FONT_SIZE_HEADER)
    _add_label(text_frame, f"ОЗУ: {ram} ГБ", bg_color)

    # Количество с индикатором
    indicator = _indicator(qty)
    _add_label(text_frame, f"Количество: {indicator} ({qty})", bg_color)

    _add_label(text_frame, f"{price} руб.",
               bg_color, bold=True, size=FONT_SIZE_HEADER, align="e")


def _add_label(parent, text, bg_color, bold=False,
               size=FONT_SIZE_NORMAL, align="w"):
    """Добавляет метку с текстом."""
    tk.Label(parent, text=text, font=font(size, bold=bold),
             bg=bg_color, anchor=align).pack(fill="x")   


def _indicator(qty):
    """
    Индикатор «много/мало» (порог 5 по КИМ).

    :param qty: количество товара (число, строка или None)
    :return: «много» или «мало»
    """
    try:
        qty = float(qty)   # приводим к числу (работает и для "10", и для 0.5)
    except (TypeError, ValueError):
        return "мало"      # при None или мусоре — «мало»
    return "много" if qty > 5 else "мало"