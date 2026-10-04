"""Модели данных для проекта УП.02."""


class Product:
    """Класс Товар — соответствует таблице «Товар» в БД."""

    def __init__(self, product_id, name, model, ram, price, quantity, image=None):
        """
        Инициализация товара.

        :param product_id: идентификатор (id)
        :param name: название (брешь)
        :param model: модель (модель)
        :param ram: объём ОЗУ (озу)
        :param price: цена (цена)
        :param quantity: количество (количество)
        :param image: путь к изображению (изображение)
        """
        self.id = product_id
        self.name = name
        self.model = model
        self.ram = ram
        self.price = price
        self.quantity = quantity
        self.image = image

    #  Бизнес-логика 

    def total(self):
        """Общая стоимость (цена × количество)."""
        return self.price * self.quantity

    def price_with_discount(self, discount_percent):
        """Цена со скидкой (округление до 2 знаков)."""
        return round(self.price * (1 - discount_percent / 100), 2)

    def indicator(self):
        """Индикатор остатка: много / мало / критично."""
        if self.quantity > 5:
            return "много"
        elif self.quantity > 3:
            return "мало"
        return "критично"

    def info(self):
        """Строка с информацией о товаре."""
        return (
            f"[{self.id}] {self.name} {self.model} "
            f"(ОЗУ {self.ram} ГБ) — {self.price} руб. | "
            f"Остаток: {self.quantity} ({self.indicator()})"
        )

    # Служебные методы 

    @classmethod
    def from_row(cls, row):
        """
        Создаёт объект Product из строки БД (кортеж).
        Удобно использовать при SELECT * FROM Товар.
        """
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
        return f"Product(id={self.id}, name='{self.name}', model='{self.model}')"