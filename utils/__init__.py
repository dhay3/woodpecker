import os
import random
from colorama import Fore, Style


def get_version():
    try:
        return open(".version", "r").read().strip()
    except Exception:
        return '1.0'


__VERSION__ = get_version()
__CONTRIBUTORS__ = ['kl_z3']
ALL_COLORS = [Fore.GREEN, Fore.RED, Fore.YELLOW, Fore.BLUE,
              Fore.MAGENTA, Fore.CYAN, Fore.WHITE]
RESET_ALL = Style.RESET_ALL


def clr():
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")


def banner():
    clr()
    logo = """                           
 ██▓███  ▓█████  ▄████▄   ██ ▄█▀▓█████  ██▀███  
▓██░  ██▒▓█   ▀ ▒██▀ ▀█   ██▄█▒ ▓█   ▀ ▓██ ▒ ██▒
▓██░ ██▓▒▒███   ▒▓█    ▄ ▓███▄░ ▒███   ▓██ ░▄█ ▒
▒██▄█▓▒ ▒▒▓█  ▄ ▒▓▓▄ ▄██▒▓██ █▄ ▒▓█  ▄ ▒██▀▀█▄  
▒██▒ ░  ░░▒████▒▒ ▓███▀ ░▒██▒ █▄░▒████▒░██▓ ▒██▒
▒▓▒░ ░  ░░░ ▒░ ░░ ░▒ ▒  ░▒ ▒▒ ▓▒░░ ▒░ ░░ ▒▓ ░▒▓░
░▒ ░      ░ ░  ░  ░  ▒   ░ ░▒ ▒░ ░ ░  ░  ░▒ ░ ▒░
░░          ░   ░        ░ ░░ ░    ░     ░░   ░ 
            ░  ░░ ░      ░  ░      ░  ░   ░     
                ░                                                        
"""
    version = f'Version: {__VERSION__}'
    # contributors = f'Contributor: {" ".join(__CONTRIBUTORS__)}'
    print(random.choice(ALL_COLORS) + logo + RESET_ALL)
    print(version)
    # print(contributors)
