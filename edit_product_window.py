"""Форма редактирования товара."""
import tkinter as tk
from tkinter import messagebox

from styles import (
    COLOR_MAIN_BG, COLOR_SECONDARY_BG, COLOR_ACCENT,
    FONT_SIZE_NORMAL, FONT_SIZE_TITLE, font
)
from order_manager import update_product, get_connection
from error_handler import safe_call


def get_product(product_id):
    """Возвращает товар по id."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, бренд, модель, озу, цена, количество FROM Товар WHERE id = ?",
                (product_id,))
    row = cur.fetchone()
    conn.close()
    return row


class EditProductWindow:
    """Окно редактирования товара."""

    def __init__(self, parent, product_id, on_save=None):
        self.product_id = product_id
        self.on_save = on_save

        product = safe_call(get_product, product_id)
        if not product:
            messagebox.showerror("Ошибка", "Товар не найден")
            return

        self.product = product
        self.window = tk.Toplevel(parent)
        self.window.title(f"Редактирование товара №{product_id}")
        self.window.geometry("400x400")
        self.window.configure(bg=COLOR_MAIN_BG)
        self.build_ui()

    def build_ui(self):
        header = tk.Frame(self.window, bg=COLOR_SECONDARY_BG, height=60)
        header.pack(fill="x")
        header.pack_propagate(False)
        tk.Label(header, text=f"ТОВАР №{self.product_id}",
                 font=font(FONT_SIZE_TITLE, bold=True),
                 bg=COLOR_SECONDARY_BG).pack(pady=15)

        form = tk.Frame(self.window, bg=COLOR_MAIN_BG)
        form.pack(pady=20, padx=20, fill="x")

        # Модель
        tk.Label(form, text="Модель:", font=font(FONT_SIZE_NORMAL),
                 bg=COLOR_MAIN_BG).pack(anchor="w")
        self.model_var = tk.StringVar(value=self.product[2])
        tk.Entry(form, textvariable=self.model_var, width=30,
                 font=font(FONT_SIZE_NORMAL)).pack(pady=5)

        # Цена
        tk.Label(form, text="Цена:", font=font(FONT_SIZE_NORMAL),
                 bg=COLOR_MAIN_BG).pack(anchor="w")
        self.price_var = tk.StringVar(value=str(self.product[4]))
        tk.Entry(form, textvariable=self.price_var, width=30,
                 font=font(FONT_SIZE_NORMAL)).pack(pady=5)

        # Количество
        tk.Label(form, text="Количество:", font=font(FONT_SIZE_NORMAL),
                 bg=COLOR_MAIN_BG).pack(anchor="w")
        self.qty_var = tk.StringVar(value=str(self.product[5]))
        tk.Entry(form, textvariable=self.qty_var, width=30,
                 font=font(FONT_SIZE_NORMAL)).pack(pady=5)

        btn_frame = tk.Frame(self.window, bg=COLOR_MAIN_BG)
        btn_frame.pack(pady=20)
        tk.Button(btn_frame, text="Сохранить", command=self.save,
                  bg=COLOR_ACCENT, fg="white",
                  font=font(FONT_SIZE_NORMAL),
                  padx=15, pady=5).pack(side="left", padx=10)
        tk.Button(btn_frame, text="Отмена",
                  command=self.window.destroy,
                  bg=COLOR_ACCENT, fg="white",
                  font=font(FONT_SIZE_NORMAL),
                  padx=15, pady=5).pack(side="left", padx=10)

    def save(self):
        name = self.model_var.get().strip()
        try:
            price = float(self.price_var.get())
            quantity = int(self.qty_var.get())
        except ValueError:
            messagebox.showwarning("Ошибка", "Цена и количество — числа")
            return

        if not name:
            messagebox.showwarning("Ошибка", "Введите модель")
            return

        if update_product(self.product_id, name, price, quantity):
            messagebox.showinfo("Успех", "Товар обновлён")
            if self.on_save:
                self.on_save()
            self.window.destroy()
        else:
            messagebox.showerror("Ошибка", "Не удалось обновить товар")
