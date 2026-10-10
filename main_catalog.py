"""Главное окно каталога."""
import tkinter as tk
from tkinter import ttk, messagebox

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

        self.current_user = None
        self.user_label = None

        self.build_ui()
        self.load_products()
        self.require_auth()

    def build_ui(self):
        """Строит интерфейс главного окна."""
        # Шапка
        header = tk.Frame(self.root, bg=COLOR_SECONDARY_BG, height=70)
        header.pack(fill="x")
        header.pack_propagate(False)

        tk.Label(header, text="Каталог товаров",
                 font=font(FONT_SIZE_TITLE, bold=True),
                 bg=COLOR_SECONDARY_BG).pack(side="left", padx=20, pady=20)

        # ФИО пользователя
        self.user_label = tk.Label(header, text="Не авторизован",
                                   font=font(FONT_SIZE_NORMAL),
                                   bg=COLOR_SECONDARY_BG)
        self.user_label.pack(side="right", padx=15)

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

    def require_auth(self):
        """Запрашивает авторизацию."""
        from auth import AuthWindow
        AuthWindow(self.root, self.on_auth_success)

    def on_auth_success(self, user):
        """Обработчик успешной авторизации."""
        self.current_user = user
        fio = f"{user[1]} {user[2]} {user[3] or ''}".strip()
        if self.user_label:
            self.user_label.config(text=f"{fio} ({user[5]})")
        self.add_role_buttons(user[5])

    def add_role_buttons(self, role):
        """Добавляет кнопки в зависимости от роли."""
        header = self.user_label.master if self.user_label else None
        if not header:
            return

        if role in ("Менеджер", "Администратор"):
            tk.Button(header, text="Заказы",
                      command=self.open_orders,
                      bg=COLOR_ACCENT, fg="white",
                      font=font(FONT_SIZE_NORMAL),
                      padx=10, pady=5).pack(side="right", padx=10)

    def open_orders(self):
        """Открывает окно списка заказов."""
        from orders_window import OrdersWindow
        OrdersWindow(self.root, self.current_user)

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

    def run(self):
        """Запускает главный цикл."""
        self.root.mainloop()


if __name__ == "__main__":
    app = CatalogWindow()
    app.run()
