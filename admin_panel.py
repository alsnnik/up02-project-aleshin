"""Админ-панель: управление товарами."""
import tkinter as tk
from tkinter import ttk, messagebox

from styles import (
    COLOR_MAIN_BG, COLOR_SECONDARY_BG, COLOR_ACCENT,
    FONT_SIZE_NORMAL, FONT_SIZE_TITLE, font
)
import database as db
from error_handler import safe_call


class AdminPanel:
    """Окно администратора для управления товарами."""

    def __init__(self, parent, current_user=None):
        self.current_user = current_user
        self.window = tk.Toplevel(parent)
        self.window.title("Админ-панель")
        self.window.geometry("900x500")
        self.window.configure(bg=COLOR_MAIN_BG)
        self.build_ui()
        self.load_products()

    def build_ui(self):
        header = tk.Frame(self.window, bg=COLOR_SECONDARY_BG, height=60)
        header.pack(fill="x")
        header.pack_propagate(False)
        tk.Label(header, text="АДМИН-ПАНЕЛЬ: ТОВАРЫ",
                 font=font(FONT_SIZE_TITLE, bold=True),
                 bg=COLOR_SECONDARY_BG).pack(pady=15)

        columns = ("id", "brand", "model", "ram", "price", "quantity")
        self.tree = ttk.Treeview(self.window, columns=columns,
                                 show="headings", height=15)
        for col, title in zip(columns,
                              ["ID", "Бренд", "Модель", "ОЗУ", "Цена", "Кол-во"]):
            self.tree.heading(col, text=title)
            self.tree.column(col, width=130)
        self.tree.pack(fill="both", expand=True, padx=20, pady=20)

        self.tree.bind("<Double-1>", self.on_edit)

        btn_frame = tk.Frame(self.window, bg=COLOR_MAIN_BG)
        btn_frame.pack(fill="x", pady=10)
        tk.Button(btn_frame, text="Редактировать",
                  command=self.on_edit,
                  bg=COLOR_ACCENT, fg="white",
                  font=font(FONT_SIZE_NORMAL),
                  padx=15, pady=5).pack(side="left", padx=20)
        tk.Button(btn_frame, text="Обновить",
                  command=self.load_products,
                  bg=COLOR_ACCENT, fg="white",
                  font=font(FONT_SIZE_NORMAL),
                  padx=15, pady=5).pack(side="left", padx=10)
        tk.Button(btn_frame, text="Назад",
                  command=self.window.destroy,
                  bg=COLOR_ACCENT, fg="white",
                  font=font(FONT_SIZE_NORMAL),
                  padx=15, pady=5).pack(side="right", padx=20)

    def load_products(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        products = safe_call(db.get_all_products) or []
        for p in products:
            self.tree.insert("", tk.END,
                             values=(p[0], p[1], p[2], p[3], p[4], p[5]))

    def on_edit(self, event=None):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Ошибка", "Выберите товар")
            return
        item = self.tree.item(selected[0])
        product_id = item["values"][0]
        from edit_product_window import EditProductWindow
        EditProductWindow(self.window, product_id, on_save=self.load_products)
