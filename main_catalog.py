"""Главное окно приложения «Каталог»."""
import tkinter as tk
from tkinter import ttk
import os

from config import APP_TITLE
from styles import COLOR_SECONDARY_BG, FONT_FAMILY, FONT_SIZE_TITLE, font
import database as db
from catalog import create_product_card
from image_utils import load_image_proportional
from resource_paths import PATH_LOGO, PATH_ICON


def set_app_icon(root, icon_path):
    """Устанавливает иконку приложения кроссплатформенно."""
    try:
        if os.name == "nt":
            if os.path.exists(icon_path):
                root.iconbitmap(icon_path)
        else:
            png_path = icon_path.replace(".ico", ".png")
            icon_img = load_image_proportional(png_path, max_size=(32, 32))
            if icon_img:
                root.iconphoto(True, icon_img)
                root._icon_photo = icon_img
    except Exception as e:
        print(f"Не удалось установить иконку: {e}")


class CatalogWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title(APP_TITLE)
        self.root.geometry("900x700")
        set_app_icon(self.root, PATH_ICON)

        self.build_ui()
        self.load_products()

    def build_ui(self):
        """Создаёт интерфейс окна."""
        header = tk.Frame(self.root, bg=COLOR_SECONDARY_BG, height=60)
        header.pack(fill="x")

        try:
            logo_img = load_image_proportional(PATH_LOGO, max_size=(40, 40))
            if logo_img:
                logo_label = tk.Label(header, image=logo_img,
                                      bg=COLOR_SECONDARY_BG)
                logo_label.image = logo_img
                logo_label.pack(side="left", padx=10)
        except Exception as e:
            print(f"Не удалось загрузить логотип: {e}")

        tk.Label(
            header, text="Каталог товаров",
            bg=COLOR_SECONDARY_BG, fg="#000000",
            font=font(FONT_SIZE_TITLE, bold=True)
        ).pack(side="left", padx=10, pady=10)

        container = tk.Frame(self.root)
        container.pack(fill="both", expand=True)

        canvas = tk.Canvas(container, bg="#FFFFFF")
        scrollbar = ttk.Scrollbar(container, orient="vertical",
                                  command=canvas.yview)
        self.scroll_frame = tk.Frame(canvas, bg="#FFFFFF")

        self.scroll_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        canvas.create_window((0, 0), window=self.scroll_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def load_products(self):
        """Загружает товары из БД и создаёт карточки."""
        products = db.get_all_products()
        for product in products:
            create_product_card(self.scroll_frame, product)


if __name__ == "__main__":
    app = CatalogWindow()
    app.root.mainloop()