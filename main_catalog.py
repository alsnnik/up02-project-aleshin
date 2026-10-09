"""Главное окно приложения с каталогом."""
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import os

from config import APP_TITLE, FONT_FAMILY
import database as db
from catalog import create_product_card
from image_utils import load_image_proportional
from resource_paths import PATH_LOGO, PATH_ICON


def set_app_icon(root, icon_path):
    """Устанавливает иконку приложения кроссплатформенно."""
    try:
        if os.name == "nt":   # Windows
            if os.path.exists(icon_path):
                root.iconbitmap(icon_path)
        else:                  # Linux/Mac
            png_path = icon_path.replace(".ico", ".png")
            icon_img = load_image_proportional(png_path, max_size=(32, 32))
            if icon_img:
                root.iconphoto(True, icon_img)
                root._icon_photo = icon_img   # сохраняем ссылку
    except Exception as e:
        print(f"Не удалось установить иконку: {e}")


class CatalogWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title(APP_TITLE)
        self.root.geometry("900x700")
        set_app_icon(self.root, PATH_ICON) 

        # Иконка приложения
        set_app_icon(self.root, PATH_ICON)

        self.build_ui()
        self.load_products()

    def build_ui(self):
        # Заголовок с логотипом
        header = tk.Frame(self.root, bg="#D2F6E7")
        header.pack(fill="x")

        # Логотип слева (с сохранением пропорций)
        logo = load_image_proportional(PATH_LOGO, max_size=(60, 60))
        if logo:
            logo_label = tk.Label(header, image=logo, bg="#D2F6E7")
            logo_label.image = logo  # сохраняем ссылку!
            logo_label.pack(side="left", padx=10, pady=5)
        else:
            tk.Label(header, text="[ЛОГОТИП]", bg="#D2F6E7").pack(
                side="left", padx=10)

        # Текст заголовка (по центру)
        tk.Label(header, text="КАТАЛОГ ТОВАРОВ",
                 font=(FONT_FAMILY, 16, "bold"),
                 bg="#D2F6E7").pack(side="left", expand=True, pady=15)

        # Область с прокруткой
        self.canvas = tk.Canvas(self.root, bg="#FFFFFF", highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.root, orient="vertical",
                                   command=self.canvas.yview)
        self.catalog_frame = tk.Frame(self.canvas, bg="#FFFFFF")
        self.catalog_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        self.canvas.create_window((0, 0), window=self.catalog_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)
        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def load_products(self):
        products = db.get_all_products()
        for p in products:
            create_product_card(self.catalog_frame, p)

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    CatalogWindow().run()