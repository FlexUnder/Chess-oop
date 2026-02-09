import os
import platform


def clear_console():
    system = platform.system().lower()
    if system == "windows":
        os.system('cls')
    else:
        os.system('clear')