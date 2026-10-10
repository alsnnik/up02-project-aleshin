"""Форма просмотра товара."""
import tkinter as tk
from tkinter import messagebox

from styles import (
    COLOR_MAIN_BG, COLOR_SECONDARY_BG, COLOR_ACCENT,
    FONT_SIZE_NORMAL, FONT_SIZE_TITLE, font
)
from image_utils import get_product_image
from error_handler import safe_call, validate_positive_int
from order_manager import (
    add_order_to_db,
    update_product_quantity,
    get_product_quantity
)


class ViewForm:
    def __init__(self, parent, product, on_add_to_order=None):
        self.product = product
        self.on_add_to_order = on_add_to_order
        self.window = tk.Toplevel(parent)
        self.window.title(f"Просмотр — {product[1]} {product[2]}")
        self.window.geometry("700x600")
        self.window.configure(bg=COLOR_MAIN_BG)
        self.build_ui()

    def build_ui(self):
        header = tk.Frame(self.window, bg=COLOR_SECONDARY_BG, height=60)
        header.pack(fill="x")
        header.pack_propagate(False)
        tk.Label(header, text="КАРТОЧКА ТОВАРА",
                 font=font(FONT_SIZE_TITLE, bold=True),
                 bg=COLOR_SECONDARY_BG).pack(pady=15)

        main = tk.Frame(self.window, bg=COLOR_MAIN_BG)
        main.pack(fill="both", expand=True, padx=20, pady=20)

        img_frame = tk.Frame(main, bg=COLOR_MAIN_BG)
        img_frame.pack(side="left", padx=10)
        photo = safe_call(get_product_image, self.product[6], size=(200, 200))
        if photo:
            lbl = tk.Label(img_frame, image=photo, bg=COLOR_MAIN_BG)
            lbl.image = photo  # type: ignore[attr-defined]
            lbl.pack()

        info_frame = tk.Frame(main, bg=COLOR_MAIN_BG)
        info_frame.pack(side="left", fill="both", expand=True, padx=20)
        self._add_field(info_frame, "Производство", self.product[1])
        self._add_field(info_frame, "Наименование", self.product[2])
        self._add_field(info_frame, "ОЗУ", f"{self.product[3]} ГБ")
        self._add_field(info_frame, "Цена", f"{self.product[4]} руб.")
        self._add_field(info_frame, "Количество", self.product[5])

        qty_frame = tk.Frame(self.window, bg=COLOR_MAIN_BG)
        qty_frame.pack(fill="x", padx=20, pady=5)
        tk.Label(qty_frame, text="Количество для заказа:",
                 font=font(FONT_SIZE_NORMAL, bold=True),
                 bg=COLOR_MAIN_BG).pack(side="left")
        self.qty_entry = tk.Entry(qty_frame, font=font(FONT_SIZE_NORMAL), width=6)
        self.qty_entry.insert(0, "1")
        self.qty_entry.pack(side="left", padx=5)

        btn_frame = tk.Frame(self.window, bg=COLOR_MAIN_BG)
        btn_frame.pack(fill="x", pady=10)
        tk.Button(btn_frame, text="Добавить в заказ",
                  command=self.add_to_order,
                  bg=COLOR_ACCENT, fg="white",
                  font=font(FONT_SIZE_NORMAL),
                  padx=15, pady=5).pack(side="left", padx=20)
        tk.Button(btn_frame, text="Назад",
                  command=self.window.destroy,
                  bg=COLOR_ACCENT, fg="white",
                  font=font(FONT_SIZE_NORMAL),
                  padx=15, pady=5).pack(side="right", padx=20)

    def _add_field(self, parent, label, value):
        row = tk.Frame(parent, bg=COLOR_MAIN_BG)
        row.pack(fill="x", pady=2)
        tk.Label(row, text=f"{label}:",
                 font=font(FONT_SIZE_NORMAL, bold=True),
                 bg=COLOR_MAIN_BG, width=15, anchor="w").pack(side="left")
        tk.Label(row, text=str(value),
                 font=font(FONT_SIZE_NORMAL),
                 bg=COLOR_MAIN_BG, anchor="w").pack(side="left")

    def add_to_order(self):
        if not self.product:
            messagebox.showerror("Ошибка", "Товар не выбран")
            return

        ok, result = validate_positive_int(self.qty_entry.get(), "Количество")
        if not ok:
            messagebox.showwarning("Ошибка ввода", str(result))
            return

        qty = int(result)  # type: ignore[arg-type]

        try:
            product_id = self.product[0]
            current_qty = int(get_product_quantity(product_id))

            if current_qty < qty:
                messagebox.showwarning("Ошибка", "Недостаточно товара на складе")
                return

            new_qty = current_qty - qty
            add_order_to_db("Иванов Иван Иванович", product_id, qty)
            update_product_quantity(product_id, new_qty)

            messagebox.showinfo("Успех", f"Заказ оформлен ({qty} шт.)")

            if self.on_add_to_order:
                self.on_add_to_order()

        except Exception as e:
            messagebox.showerror("Ошибка заказа",
                                 f"Не удалось оформить заказ:\n{e}")
