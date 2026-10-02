price = float(input("Введите цену: "))
discount = float(input("Введите скидку (%): "))

final_price = price * (1 - discount / 100)

print(f"Цена со скидкой: {final_price:.2f} руб.")