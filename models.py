"""Модели данных для проекта УП.02."""
from datetime import datetime


class Product:
    """Класс Товар — соответствует таблице «Товар» в БД."""

    def __init__(self, product_id, name, model, ram, price, quantity, image=None):
        self.id = product_id
        self.name = name
        self.model = model
        self.ram = ram
        self.price = price
        self.quantity = quantity
        self.image = image

    def total(self):
        return self.price * self.quantity

    def price_with_discount(self, discount_percent):
        return round(self.price * (1 - discount_percent / 100), 2)

    def indicator(self):
        if self.quantity > 5:
            return "много"
        elif self.quantity > 3:
            return "мало"
        return "критично"

    def is_available(self):
        return self.quantity > 0

    def info(self):
        return (
            f"[{self.id}] {self.name} {self.model} "
            f"(ОЗУ {self.ram} ГБ) — {self.price} руб. | "
            f"Остаток: {self.quantity} ({self.indicator()})"
        )

    @classmethod
    def from_row(cls, row):
        return cls(
            product_id=row[0],
            name=row[1],
            model=row[2],
            ram=row[3],
            price=row[4],
            quantity=row[5],
            image=row[6] if len(row) > 6 else None,
        )

    def __str__(self):
        return self.info()

    def __repr__(self):
        return f"Product(id={self.id}, name='{self.name}')"


# ЗАДАНИЕ 2: Класс Order 

class Order:
    """Класс Заказ."""

    def __init__(self, order_id, date, client, product, quantity):
        """
        :param order_id: номер заказа
        :param date: дата заказа (строка или datetime)
        :param client: имя клиента
        :param product: объект Product (или его id)
        :param quantity: количество единиц товара
        """
        self.id = order_id
        self.date = date
        self.client = client
        self.product = product          # объект Product
        self.quantity = quantity

    def total(self):
        """Стоимость заказа (цена товара × количество)."""
        return round(self.product.price * self.quantity, 2)

    def total_with_discount(self, discount_percent):
        """Стоимость заказа со скидкой."""
        return round(self.product.price_with_discount(discount_percent) * self.quantity, 2)

    def info(self):
        """Строка с информацией о заказе."""
        return (
            f"Заказ №{self.id} от {self.date}: "
            f"{self.client} — {self.product.name} × {self.quantity} = "
            f"{self.total()} руб."
        )

    @classmethod
    def from_row(cls, row, product=None):
        """
        Создаёт объект Order из строки БД.
        :param row: кортеж из БД (id, дата, клиент, product_id, quantity)
        :param product: объект Product, найденный по product_id (если None — id)
        """
        return cls(
            order_id=row[0],
            date=row[1],
            client=row[2],
            product=product if product is not None else row[3],  # объект или id
            quantity=row[4],
        )

    def __str__(self):
        return self.info()

    def __repr__(self):
        return f"Order(id={self.id}, client='{self.client}', qty={self.quantity})"