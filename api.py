import requests
import os
import json
from utils.log import logger
from factory import AIPModel


def load_api_json(file_path: str = r'D:\workspace_for_pycharm\woodpecker\apidata_test.json'):
    if os.path.isfile(file_path):
        with open(file_path, 'r', encoding='utf-8') as api_json:
            try:
                apis = json.loads(api_json.read())
                _apis = [AIPModel(**api).copy() for api in apis]
                return _apis
            except Exception as e:
                logger.error(e.__str__())
    else:
        logger.warning('apidata.json not found. Fetching data from github.')
        return [AIPModel(**api) for api in
                requests.get('https://raw.githubusercontent.com/dhay3/woodpecker/master/woodpecker/apidata_test.json',
                             timeout=10).json()]


if __name__ == '__main__':
    print(load_api_json())
