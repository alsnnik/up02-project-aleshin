# resource.py - Заглушка для модуля resource (только для Windows)
import sys
PATH_LOGO = "resources/logo.png"
PATH_ICON = "resources/icon.ico"

from resources import load_image_proportional, PATH_LOGO, PATH_ICON, get_product_image

if sys.platform == "win32":
    # Определяем фиктивные функции и константы, которые может использовать ваш скрипт
    def getrlimit(*args, **kwargs):
        return (None, None)

    def setrlimit(*args, **kwargs):
        pass

    RLIMIT_NOFILE = 0
    # При необходимости добавьте другие константы
    
    print("ВНИМАНИЕ: Используется заглушка модуля 'resource' на Windows. Лимиты ресурсов не будут применены.")
else:
    # На Unix-системах импортируем настоящий модуль
    from builtins import *
    from resource import *