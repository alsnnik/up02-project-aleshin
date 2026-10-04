"""Проверка класса Product."""
from models import Product


# Тест 1: товар с количеством "мало" 
p1 = Product(
    product_id=1,
    name="Kingston Fury",
    model="DDR4",
    ram=16,
    price=4500,
    quantity=3
)

print(p1.info())
print(f"Со скидкой 25%: {p1.price_with_discount(25):.2f} руб.")
print(f"Индикатор: {p1.indicator()}")
print("-" * 60)


#  Тест 2: товар с количеством "много" 
p2 = Product(
    product_id=2,
    name="Samsung",
    model="DDR5",
    ram=32,
    price=12000,
    quantity=10
)

print(p2.info())
print(f"Со скидкой 10%: {p2.price_with_discount(10):.2f} руб.")
print(f"Индикатор: {p2.indicator()}")
print("-" * 60)


# Тест 3: граничный случай (ровно 5) 
p3 = Product(
    product_id=3,
    name="Crucial",
    model="DDR4",
    ram=8,
    price=2800,
    quantity=5
)

print(p3.info())
print(f"Индикатор: {p3.indicator()}")   # ожидаем "мало" (5 не > 5)
print("-" * 60)


# Тест 4: создание из строки БД 
row_from_db = (4, "Corsair", "DDR5", 64, 25000, 7, "/img/corsair.jpg")
p4 = Product.from_row(row_from_db)
print(p4)
print(f"Общая стоимость: {p4.total()} руб.")

#  Тест 5: проверка is_available() 

print("\n" + "=" * 60)
print("ПРОВЕРКА is_available()")
print("=" * 60)

# Случай 1: товар есть в наличии
p_yes = Product(10, "iPhone 15", "Смартфон", 8, 90000, 5)
print(f"{p_yes.name}: quantity={p_yes.quantity} → is_available()={p_yes.is_available()}")
# Ожидается: True

# Случай 2: последняя штука
p_last = Product(11, "Pixel 8", "Смартфон", 8, 70000, 1)
print(f"{p_last.name}: quantity={p_last.quantity} → is_available()={p_last.is_available()}")
# Ожидается: True

# Случай 3: НЕТ в наличии
p_no = Product(12, "Xiaomi 14", "Смартфон", 12, 85000, 0)
print(f"{p_no.name}: quantity={p_no.quantity} → is_available()={p_no.is_available()}")
# Ожидается: False

# Случай 4: некорректные данные (отрицательное)
p_bad = Product(13, "Тест", "Смартфон", 4, 10000, -3)
print(f"{p_bad.name}: quantity={p_bad.quantity} → is_available()={p_bad.is_available()}")
# Ожидается: False