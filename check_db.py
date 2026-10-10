"""Проверка содержимого БД."""
import sqlite3
from config import DB_PATH

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

# Список таблиц
cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
print("Таблицы:", [r[0] for r in cur.fetchall()])

# Заказы
print("\n[Заказ]")
for r in cur.execute("SELECT * FROM Заказ"):
    print(" ", r)

# Позиции
print("\n[Состав_заказа]")
for r in cur.execute("SELECT * FROM Состав_заказа"):
    print(" ", r)

# Остатки
print("\n[Товар]")
for r in cur.execute("SELECT id, модель, количество FROM Товар"):
    print(" ", r)

conn.close()
