"""Модели данных для проекта УП.02."""
from datetime import datetime
from discount import calculate_price_with_discount


class Product:
    """Класс Товар."""

    def __init__(
        self,
        product_id,
        name,
        category="Без категории",
        price=0,
        quantity=0,
        ram=None,
        model=None,
    ):
        """
        :param product_id: id товара
        :param name: название
        :param category: категория
        :param price: цена
        :param quantity: количество на складе
        :param ram: объём ОЗУ (для смартфонов), ГБ
        :param model: модель устройства
        """
        self.id = product_id
        self.name = name
        self.category = category
        self.price = price
        self.quantity = quantity
        self.ram = ram
        self.model = model

    # ========== Фабричный метод для БД ==========
    @classmethod
    def from_row(cls, row):
        """
        Создать объект Product из строки БД.

        Порядок колонок: id, name, category, price, quantity
        """
        return cls(
            product_id=row[0],
            name=row[1],
            category=row[2],
            price=row[3],
            quantity=row[4],
        )

    # ========== Базовые методы ==========
    def total(self):
        """Общая стоимость позиции (цена × количество)."""
        return self.price * self.quantity

    def indicator(self):
        """Текстовый индикатор остатка."""
        return "много" if self.quantity > 5 else "мало"

    def is_available(self):
        """
        Есть ли товар в наличии.

        :return: True, если quantity > 0
        """
        return self.quantity > 0

    # ========== Методы расчёта скидки ==========
    def price_with_discount_auto(self, date=None):
        """
        Цена со скидкой по алгоритму ДЭ (из discount.py).
        Скидка 25% на товары без заказов в предыдущем месяце.
        """
        if date is None:
            date = datetime.now()
        return calculate_price_with_discount(self.id, self.price, date)

    def price_with_discount(self, percent=10):
        """
        Простой расчёт цены со скидкой в процентах.

        :param percent: размер скидки в процентах (по умолчанию 10)
        :return: цена со скидкой
        """
        return self.price * (1 - percent / 100)

    # ========== Информация о товаре ==========
    def info(self):
        """Строка с полной информацией о товаре."""
        extra = ""
        if self.ram:
            extra += f", RAM: {self.ram} ГБ"
        if self.model:
            extra += f", модель: {self.model}"

        return (
            f"{self.name} ({self.category}){extra}: "
            f"{self.price} руб. × {self.quantity} = {self.total()} руб. "
            f"({self.indicator()})"
        )