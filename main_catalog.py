"""Главное окно каталога."""
import tkinter as tk

import database as db
from styles import (
    COLOR_MAIN_BG, COLOR_SECONDARY_BG, COLOR_ACCENT,
    FONT_SIZE_NORMAL, FONT_SIZE_TITLE, font
)
from catalog import create_product_card
from error_handler import safe_call


class CatalogWindow:
    """Главное окно приложения."""

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Электроника — Каталог товаров")
        self.root.geometry("900x700")
        self.root.configure(bg=COLOR_MAIN_BG)

        self.build_ui()
        self.load_products()

    def build_ui(self):
        """Строит интерфейс главного окна."""
        # Шапка
        header = tk.Frame(self.root, bg=COLOR_SECONDARY_BG, height=70)
        header.pack(fill="x")
        header.pack_propagate(False)

        tk.Label(header, text="Каталог товаров",
                 font=font(FONT_SIZE_TITLE, bold=True),
                 bg=COLOR_SECONDARY_BG).pack(side="left", padx=20, pady=20)

        # Кнопка «Список заказов»
        tk.Button(header, text="Список заказов",
                  command=self.open_orders,
                  bg=COLOR_ACCENT, fg="white",
                  font=font(FONT_SIZE_NORMAL),
                  padx=10, pady=5).pack(side="right", padx=20)

        # Область с прокруткой
        container = tk.Frame(self.root, bg=COLOR_MAIN_BG)
        container.pack(fill="both", expand=True)

        canvas = tk.Canvas(container, bg=COLOR_MAIN_BG, highlightthickness=0)
        scrollbar = tk.Scrollbar(container, orient="vertical", command=canvas.yview)
        self.catalog_frame = tk.Frame(canvas, bg=COLOR_MAIN_BG)

        self.catalog_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=self.catalog_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def load_products(self):
        """Загружает товары с обработкой ошибок."""
        products = safe_call(db.get_all_products) or []
        for product in products:
            safe_call(create_product_card, self.catalog_frame, product,
                      refresh=self.refresh_catalog)

    def refresh_catalog(self):
        """Обновляет каталог."""
        for widget in self.catalog_frame.winfo_children():
            widget.destroy()
        self.load_products()

    def open_orders(self):
        """Открывает окно списка заказов."""
        from orders_window import OrdersWindow
        OrdersWindow(self.root)

    def run(self):
        """Запускает главный цикл."""
        self.root.mainloop()


if __name__ == "__main__":
    app = CatalogWindow()
    app.run()