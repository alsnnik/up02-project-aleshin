"""Каталог товаров."""
import tkinter as tk

from styles import (
    COLOR_MAIN_BG, COLOR_SECONDARY_BG, COLOR_ACCENT, COLOR_HIGHLIGHT,
    FONT_SIZE_NORMAL, FONT_SIZE_HEADER, font
)
from image_utils import get_product_image
from error_handler import safe_call


def create_product_card(parent, product, refresh=None):
    card = tk.Frame(parent, bg=COLOR_MAIN_BG, relief="ridge", bd=1)
    card.pack(fill="x", padx=10, pady=5)

    img_frame = tk.Frame(card, bg=COLOR_MAIN_BG)
    img_frame.pack(side="left", padx=10, pady=10)
    photo = safe_call(get_product_image, product[6], size=(100, 100))
    if photo:
        img_label = tk.Label(img_frame, image=photo, bg=COLOR_MAIN_BG)
        img_label.image = photo
        img_label.pack()

    info_frame = tk.Frame(card, bg=COLOR_MAIN_BG)
    info_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)

    tk.Label(info_frame, text=f"{product[1]} | {product[2]}",
             font=font(FONT_SIZE_HEADER, bold=True),
             bg=COLOR_MAIN_BG, anchor="w").pack(fill="x")
    tk.Label(info_frame, text=f"ОЗУ: {product[3]} ГБ",
             font=font(FONT_SIZE_NORMAL),
             bg=COLOR_MAIN_BG, anchor="w").pack(fill="x")
    tk.Label(info_frame, text=f"Количество: {product[5]}",
             font=font(FONT_SIZE_NORMAL),
             bg=COLOR_MAIN_BG, anchor="w").pack(fill="x")
    tk.Label(info_frame, text=f"{product[4]} руб.",
             font=font(FONT_SIZE_HEADER, bold=True),
             bg=COLOR_MAIN_BG, anchor="e").pack(fill="x")

    card.bind("<Button-1>", lambda e: _open_view(parent, product, refresh))
    for child in card.winfo_children():
        child.bind("<Button-1>", lambda e: _open_view(parent, product, refresh))
        for sub in child.winfo_children():
            sub.bind("<Button-1>", lambda e: _open_view(parent, product, refresh))

    return card


def _open_view(parent, product, refresh=None):
    from view_form import ViewForm
    ViewForm(parent, product, on_add_to_order=refresh)
