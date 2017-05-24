from colorama import init as colorama_init
from colorama import Fore

colorama_init()


def fore(color, msg):
    if color == 'yellow':
        c = Fore.YELLOW
    elif color == 'red':
        c = Fore.RED
    elif color == 'green':
        c = Fore.GREEN
    elif color == 'blue':
        c = Fore.BLUE
    return c + msg + Fore.RESET

# End File politeauthority/politeauthority/color.py
