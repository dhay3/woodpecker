import requests
import os
import json
from utils.log import logger
<<<<<<< HEAD
from utils.bean import APIBean


def load_api(phone, path: str = r'D:\workspace_for_pycharm\woodpecker\apidata_test.json'):
    if os.path.isfile(path):
        with open(path, 'r', encoding='utf-8') as ct:
            try:
                ct = json.loads(ct.read())
                _api_list = [APIBean(phone, **api) for api in ct]
                return _api_list
=======
from utils.factory import APIFactory


def load_api_json(file_path: str = 'apidata_test.json'):
    if os.path.isfile(file_path):
        with open(file_path, 'r', encoding='utf-8') as api_json:
            try:
                apis = json.loads(api_json.read())
                _apis = [APIFactory(**api) for api in apis]
                return _apis
>>>>>>> e5838f1 (init)
            except Exception as e:
                logger.error(e.__str__())
    else:
        logger.warning('apidata.json not found. Fetching data from github.')
<<<<<<< HEAD
        return [APIBean(**api) for api in
                requests.get(
                    url='https://raw.githubusercontent.com/dhay3/woodpecker/master/woodpecker/apidata_test.json',
                    timeout=10).json()]


if __name__ == '__main__':
    print(load_api('22222'))
=======
        return [APIFactory(**api) for api in
                requests.get('https://raw.githubusercontent.com/dhay3/woodpecker/master/woodpecker/apidata_test.json',
                             timeout=10).json()]
>>>>>>> e5838f1 (init)
