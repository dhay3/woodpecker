import os
import json
import random
from utils.log import logger
from utils.factory import APIFactory


def load_api_json():
    if os.path.isfile('D:\\code\\woodpecker\\apidata_test.json'):
        with open('D:\\code\\woodpecker\\apidata_test.json', 'r', encoding='utf-8') as api_json:
            try:
                apis = json.loads(api_json.read())
                _apis = [APIFactory(**api) for api in apis]
                return _apis
            except Exception as e:
                logger.error(e.__str__())
    else:
        logger.warning('apidata.json not found. Downloading from github')
        # TODO download from github
        return load_api_json()


def random_api():
    return [random.choice(load_api_json())]


if __name__ == '__main__':
    print(random_api())
