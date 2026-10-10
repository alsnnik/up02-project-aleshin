"""Окно списка заказов (для Менеджера)."""
import tkinter as tk
from tkinter import ttk

from styles import (
    COLOR_MAIN_BG, COLOR_SECONDARY_BG, FONT_SIZE_TITLE, font
)
from order_manager import get_all_orders
from error_handler import safe_call


class OrdersWindow:
    """Окно списка заказов."""

    def __init__(self, parent):
        self.window = tk.Toplevel(parent)
        self.window.title("Список заказов")
        self.window.geometry("800x500")
        self.window.configure(bg=COLOR_MAIN_BG)
        self.build_ui()

    def build_ui(self):
        header = tk.Frame(self.window, bg=COLOR_SECONDARY_BG, height=60)
        header.pack(fill="x")
        header.pack_propagate(False)
        tk.Label(header, text="СПИСОК ЗАКАЗОВ",
                 font=font(FONT_SIZE_TITLE, bold=True),
                 bg=COLOR_SECONDARY_BG).pack(pady=15)

        columns = ("id", "дата", "клиент", "товар", "количество")
        tree = ttk.Treeview(self.window, columns=columns, show="headings")
        for col, title in zip(columns,
                              ["ID", "Дата", "Клиент", "Товар", "Кол-во"]):
            tree.heading(col, text=title)
            tree.column(col, width=140)
        tree.pack(fill="both", expand=True, padx=20, pady=20)

        orders = safe_call(get_all_orders) or []
        for row in orders:
            tree.insert("", "end", values=row)
