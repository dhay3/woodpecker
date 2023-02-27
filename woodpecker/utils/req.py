import requests
import json
import random
import os
import threading
import utils.api
from utils.log import logger
from utils.factory import APIFactory

succeed_cnt = 0
max_limit_cnt = 5
tried_cnt = 0
lock = threading.Lock()


def check_internet():
    try:
        requests.head('https://motherfuckingwebsite.com')
    except Exception as e:
        logger.error('Poor Internet connection.')
        exit(-1)


def random_user_agent():
    if os.path.isfile('/home/cpl/PycharmProjects/woodpecker/headers.json'):
        with open('/home/cpl/PycharmProjects/woodpecker/headers.json', 'r') as headers_json:
            headers = json.loads(headers_json.read())
            return random.choice(headers)
    else:
        logger.warning('headers.json not found. Downloading form github.')
        # TODO download from github
        return random_user_agent()


def check_request(api: APIFactory, resp: str):
    return True if api.identifier in resp else False


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
            raise Exception('Method not supported, check aipdata.json.')
        if check_request(api, resp):
            logger.success(f'{api.desc} succeed.')
            return True
        else:
            logger.warning(f'{api.desc} failed.')
            return False
    except Exception as e:
        logger.error(e.__str__())


def do_sms_onerun(phone: str):
    _api = utils.api.load_api_json()
    for api in _api:
        if isinstance(api, APIFactory):
            api.api_bean(phone)
            do_request(api)


def do_sms(phone: str, count: int):
    global tried_cnt
    _api = utils.api.load_api_json()
    logger.success(f'apidata.json has been loaded, {len(_api)} api has been found.')
    # lock.acquire()
    while tried_cnt < count:
        for api in _api:
            if isinstance(api, APIFactory):
                if tried_cnt == count:
                    break
                api = api.copy()
                api.api_bean(phone)
                do_request(api)
            lock.acquire()
            tried_cnt += 1
            lock.release()
    # lock.release()


def do_sms_succeeds(phone: str, count: int):
    global succeed_cnt
    global tried_cnt
    _api = utils.api.load_api_json()
    logger.success(f'apidata.json has been loaded, {len(_api)} api has been found.')
    # lock.acquire()
    while succeed_cnt < count and tried_cnt < max_limit_cnt:
        for api in _api:
            if isinstance(api, APIFactory):
                if succeed_cnt == count:
                    break
                if tried_cnt == max_limit_cnt:
                    break
                api = api.copy()
                api.api_bean(phone)
                if do_request(api):
                    lock.acquire()
                    succeed_cnt += 1
                    lock.release()
            lock.acquire()
            tried_cnt += 1
            lock.release()
    # lock.release()


if __name__ == '__main__':
    # do_sms('15988803859', 5)
    # do_sms_succeeds('15988803859', 5)
    do_sms_onerun('15988803859')