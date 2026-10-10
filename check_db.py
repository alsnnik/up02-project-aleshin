"""Проверка содержимого БД: какие таблицы и данные есть."""
import sqlite3
from config import DB_PATH

print("Путь к БД:", DB_PATH)

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

# Все таблицы в БД
tables = cur.execute(
    "SELECT name FROM sqlite_master WHERE type='table'"
).fetchall()
print("\nТаблицы:", tables)

# Данные из таблицы Товар
try:
    rows = cur.execute("SELECT * FROM Товар").fetchall()
    print(f"\n[Товар] Всего записей: {len(rows)}")
    for row in rows:
        print("  ", row)
    if not rows:
        print("  (пусто)")
except sqlite3.OperationalError as e:
    print(f"[Товар] Ошибка: {e}")

# Данные из таблицы Заказ
try:
    rows = cur.execute("SELECT * FROM Заказ").fetchall()
    print(f"\n[Заказ] Всего записей: {len(rows)}")
    for row in rows:
        print("  ", row)
    if not rows:
        print("  (пусто)")
except sqlite3.OperationalError as e:
    print(f"[Заказ] Ошибка: {e}")

conn.close()