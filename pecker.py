import click
import os
import json
import random
import requests
from json import JSONDecodeError
from colorama import Fore, Style
from utils.req import tk
from utils.bean import APIBean
from utils.log import logger

__VERSION__ = '0.0.2'
__CONTRIBUTORS__ = ['C4z']
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
    contributors = f'Contributor: {" ".join(__CONTRIBUTORS__)}'
    print(f'{random.choice(ALL_COLORS)}{logo}{RESET_ALL}')
    print(version, contributors)


def load_api(path: str = r'apidata.json'):
    try:
        with open(path, 'r', encoding='utf-8') as ct:
            ct = json.loads(ct.read())
            _api_list = [APIBean(**api) for api in ct]
            return _api_list
    except FileNotFoundError:
        logger.warning('apidata.json not found. Fetching data from github.')
        return [APIBean(**api) for api in
                requests.get(
                    url='https://raw.githubusercontent.com/dhay3/woodpecker/master/woodpecker/apidata.json',
                    timeout=10).json()]
    except JSONDecodeError:
        logger.warning('apidata.json read error.')


@click.command()
@click.argument('phone', metavar='<phone number>', type=str)
@click.option('-c', '--count', metavar='[count]', type=int, default=10,
              help='Count of sms to send. Failed\'s will be counted.')
@click.option('-x', '--proxy', metavar='<socket>', type=str,
              help='Use proxy.')
def pecker(phone: str, count: int, proxy: str = None):
    banner()
    _api = load_api()
    logger.success(f'apidata.json has been loaded, {len(_api)} api has been found.')
    tk(_api, phone, count, proxy)


if __name__ == '__main__':
    pecker()
