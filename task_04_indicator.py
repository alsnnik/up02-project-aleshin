# task_04_indicator.py
catalog = [
    {"name": "Кроссовки", "price": 8500, "qty": 3},
    {"name": "Ботинки",   "price": 15000, "qty": 1},
    {"name": "Туфли",     "price": 12000, "qty": 5},
    {"name": "Сандалии",  "price": 4500, "qty": 8},
    {"name": "Кеды",      "price": 6000, "qty": 2},
]

# Добавляем поле "indicator": "много" если qty > 5, иначе "мало"
for item in catalog:
    item["indicator"] = "много" if item["qty"] > 5 else "мало"

# Сортируем: сначала "много", затем "мало"
# key: 0 для "много", 1 для "мало"
catalog.sort(key=lambda x: 0 if x["indicator"] == "много" else 1)

print("Каталог с индикатором:")
for i, item in enumerate(catalog, start=1):
    print(f"{i}. {item['name']:<10} — {item['qty']} шт. → {item['indicator']}")