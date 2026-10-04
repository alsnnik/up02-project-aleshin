from datetime import datetime
from models import Product

p = Product(2, "Ботинки Timberland", "Ботинки", 15000, 3)
date = datetime(2026, 10, 15)

print(f"Базовая цена: {p.price}")
print(f"Со скидкой:   {p.price_with_discount_auto(date)}")