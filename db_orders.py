"""Загрузка заказов из БД в объекты класса Order."""
import sqlite3
from config import DB_PATH
from models import Product, Order


#Вспомогательные 

def get_product_by_id(product_id):
    """Находит объект Product по его id."""
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT * FROM Товар WHERE id = ?", (product_id,))
    row = cur.fetchone()
    conn.close()
    return Product.from_row(row) if row else None


#  Загрузка заказов 

def get_all_orders():
    """Возвращает список объектов Order с привязанными Product."""
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("SELECT * FROM Заказ ORDER BY id")
    rows = cur.fetchall()
    conn.close()

    orders = []
    for row in rows:
        # Предполагаемая структура Заказа:
        # 0 id | 1 дата | 2 клиент | 3 товар_id | 4 количество
        product = get_product_by_id(row[3])
        order = Order(
            order_id=row[0],
            date=row[1],
            client=row[2],
            product=product if product else row[3],
            quantity=row[4],
        )
        orders.append(order)
    return orders


#  Вывод 

def print_orders(orders, title="ЗАКАЗЫ"):
    """Выводит список заказов."""
    print(f"\n{'=' * 70}")
    print(f"{title} ({len(orders)} шт.)")
    print("=" * 70)

    if not orders:
        print("   Заказы не найдены.")
    else:
        for o in orders:
            print(o.info())
            # Дополнительно — общая стоимость со скидкой
            # print(f"    Со скидкой 10%: {o.total_with_discount(10)} руб.")

    print("=" * 70)


def print_orders_summary(orders):
    """Сводка: количество заказов и общая выручка."""
    if not orders:
        print("\nНет заказов для подсчёта.")
        return

    total_revenue = sum(o.total() for o in orders)
    print(f"\n ИТОГО:")
    print(f"   Заказов: {len(orders)}")
    print(f"   Общая выручка: {total_revenue} руб.")
    print(f"   Средний чек: {round(total_revenue / len(orders), 2)} руб.")


# Демонстрация

if __name__ == "__main__":
    # Отладка: показать структуру таблицы Заказ
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("PRAGMA table_info(Заказ)")
    print("Структура таблицы «Заказ»:")
    for col in cur.fetchall():
        print(f"  {col[0]}: {col[1]} ({col[2]})")
    conn.close()

    orders = get_all_orders()
    print_orders(orders, title="ВСЕ ЗАКАЗЫ")
    print_orders_summary(orders)