"""Генератор заглушки 'Нет фото'."""
from PIL import Image, ImageDraw, ImageFont

# Создаём пустое изображение 100x100 (серый фон)
img = Image.new("RGB", (100, 100), color="#DDDDDD")
draw = ImageDraw.Draw(img)

# Пробуем загрузить шрифт Calibri, если нет — стандартный
try:
    font = ImageFont.truetype("calibri.ttf", 16)
except OSError:
    font = ImageFont.load_default()

# Рисуем текст по центру
text = "Нет фото"
# Получаем размеры текста
bbox = draw.textbbox((0, 0), text, font=font)
text_w = bbox[2] - bbox[0]
text_h = bbox[3] - bbox[1]
x = (100 - text_w) // 2
y = (100 - text_h) // 2
draw.text((x, y), text, fill="#666666", font=font)

# Сохраняем
img.save("resources/picture.png")
print("Заглушка resources/picture.png обновлена.")