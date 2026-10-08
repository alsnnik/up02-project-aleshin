import sqlite3
from config import DB_PATH


def get_all_products():
    """Возвращает все товары из таблицы Товар."""
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT * FROM Товар")
    rows = cur.fetchall()
    conn.close()
    return rows