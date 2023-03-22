import requests
import os
import json
from utils.log import logger
from utils.factory_bak import APIModel


def load_api(path: str = r'D:\code\woodpecker\apidata_test.json'):
    if os.path.isfile(path):
        with open(path, 'r', encoding='utf-8') as ct:
            # try:
            ct = json.loads(ct.read())
            _api = [APIModel(**api) for api in ct]
            return _api
        # except Exception as e:
        #     logger.error(e.__str__())
    else:
        logger.warning('apidata.json not found. Fetching data from github.')
        return [APIModel(**api) for api in
                requests.get('https://raw.githubusercontent.com/dhay3/woodpecker/master/woodpecker/apidata_test.json',
                             timeout=10).json()]


if __name__ == '__main__':
    print(load_api())
