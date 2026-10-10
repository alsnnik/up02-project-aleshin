"""Пути к ресурсам проекта."""
import sys

PATH_LOGO = "resources/logo.png"
PATH_ICON = "resources/icon.ico"
PATH_PICTURE = "resources/picture.png"


# Заглушка для системного модуля 'resource' (только для Windows)
if sys.platform == "win32":
    def getrlimit(*args, **kwargs):
        return (None, None)

    def setrlimit(*args, **kwargs):
        pass

    RLIMIT_NOFILE = 0
    print("ВНИМАНИЕ: Используется заглушка модуля 'resource' на Windows.")
else:
    from resource import *