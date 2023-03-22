import string
import requests
from typing import Union
from loguru import logger


def chk_internet():
    try:
        # logger.info('Checking Internet connection.')
        requests.head('https://motherfuckingwebsite.com')
        # logger.success('Connection available.')
    except Exception as e:
        logger.error('Poor Internet connection.')
        exit(-1)


def chk_args_conflict(phone: str, thread: int, count: int, interval: int, max_tried: int,
                      proxy: bool = False, only: bool = False, flooding: bool = False, check: bool = False):
    try:
        # redundancy
        if check:
            if flooding or only or thread or count or interval or max_tried:
                raise Exception('1')
        elif flooding:
            if check or only or thread or count or interval or max_tried:
                raise Exception('2')
        elif only:
            if check or flooding:
                raise Exception('3')
            if not max_tried:
                raise Exception('3')
        elif max_tried:
            if check or flooding:
                raise Exception('4')
            if not only:
                raise Exception('4')
        elif count:
            if check or flooding:
                raise Exception(5)
        elif thread:
            if check or flooding:
                raise Exception(5)
        elif interval:
            if check or flooding:
                raise Exception(5)
    except Exception as e:
        logger.error(e.__str__())
        exit(-1)


def chk_args_validation(phone: Union[str, None], thread: int, count: int, interval: int, max_tried: int):
    try:
        if phone:
            if 6 <= len(phone) <= 12:
                for n in phone:
                    if n not in string.digits:
                        raise Exception('Invalid Phone number.')
            else:
                raise Exception('Invalid Phone number.')
        else:
            raise Exception('Phone number cannot be null.')
        if count < 0 or interval < 0 or thread < 0 or max_tried < 0:
            raise Exception('Either count/interval/thread/max_tried must be positive.')
    except Exception as e:
        logger.error(e.__str__())
        exit(-1)
