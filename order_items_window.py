"""Окно состава заказа."""
import tkinter as tk
from tkinter import ttk, messagebox

from styles import (
    COLOR_MAIN_BG, COLOR_SECONDARY_BG, COLOR_ACCENT,
    FONT_SIZE_NORMAL, FONT_SIZE_TITLE, font
)
from order_manager import get_order_items
from error_handler import safe_call


class OrderItemsWindow:
    """Окно состава заказа."""

    def __init__(self, parent, order_id):
        self.order_id = order_id
        self.window = tk.Toplevel(parent)
        self.window.title(f"Состав заказа №{order_id}")
        self.window.geometry("700x400")
        self.window.configure(bg=COLOR_MAIN_BG)
        self.build_ui()
        self.load_items()

    def build_ui(self):
        header = tk.Frame(self.window, bg=COLOR_SECONDARY_BG, height=60)
        header.pack(fill="x")
        header.pack_propagate(False)
        tk.Label(header, text=f"СОСТАВ ЗАКАЗА №{self.order_id}",
                 font=font(FONT_SIZE_TITLE, bold=True),
                 bg=COLOR_SECONDARY_BG).pack(pady=15)

        columns = ("name", "size", "quantity", "price", "total")
        self.tree = ttk.Treeview(self.window, columns=columns,
                                 show="headings", height=10)
        self.tree.heading("name", text="Товар")
        self.tree.heading("size", text="Размер")
        self.tree.heading("quantity", text="Кол-во")
        self.tree.heading("price", text="Цена")
        self.tree.heading("total", text="Сумма")
        self.tree.column("name", width=250, anchor="w")
        self.tree.column("size", width=70, anchor="center")
        self.tree.column("quantity", width=70, anchor="center")
        self.tree.column("price", width=100, anchor="e")
        self.tree.column("total", width=100, anchor="e")
        self.tree.pack(fill="both", expand=True, padx=20, pady=20)

        self.total_label = tk.Label(self.window, text="",
                                    font=font(FONT_SIZE_NORMAL, bold=True),
                                    bg=COLOR_MAIN_BG)
        self.total_label.pack(pady=5)

        btn_frame = tk.Frame(self.window, bg=COLOR_MAIN_BG)
        btn_frame.pack(fill="x", pady=10)
        tk.Button(btn_frame, text="Назад",
                  command=self.window.destroy,
                  bg=COLOR_ACCENT, fg="white",
                  font=font(FONT_SIZE_NORMAL),
                  padx=15, pady=5).pack(side="right", padx=20)

    def load_items(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        items = safe_call(get_order_items, self.order_id) or []
        total = 0.0

        for item in items:
            # item = (id, name, size, quantity, price)
            _, name, size, quantity, price = item
            item_total = quantity * price
            total += item_total
            self.tree.insert("", tk.END,
                             values=(name, size, quantity,
                                     f"{price:.2f}", f"{item_total:.2f}"))

        self.total_label.config(text=f"Итого: {total:.2f} руб.")
