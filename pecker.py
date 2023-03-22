# -*- coding: utf-8 -*-
"""
@author fdsaz
"""
import click
import multiprocessing
import utils.checker
import req
import api
from concurrent.futures import ThreadPoolExecutor
from utils.log import logger

__nproc__ = multiprocessing.cpu_count()


@click.command()
@click.argument('phone', type=str)
@click.option('-t', '--thread', metavar='ThreadingNum', type=int,
              help='Threading number to send sms.')
@click.option('-c', '--count', metavar='Count', type=int,
              help='Count of sms to send. Failed\'s will be counted.')
@click.option('-i', '--interval', metavar='Interval', type=int,
              help='Delay time of sending sms.')
@click.option('--max-tried', metavar='MaxLimit', type=int,
              help='Max tried count.')
@click.option('-x', '--proxy', is_flag=True, type=bool,
              help='Use proxy.')
# TODO add proxy function as curl
@click.option('-f', '--flooding', is_flag=True, type=bool,
              help='Flooding api mode. Skipping check request status. Thread 64 interval 0')
@click.option('--only', is_flag=True, type=bool,
              help='Only succeed counts.')
@click.option('--check', is_flag=True, type=bool,
              help='Check api is available or not.')
@click.option('--debug', is_flag=True, type=bool,
              help='Enable debug mode.')
def pecker(phone: str, thread: int, count: int, interval: int, max_tried: int,
           proxy: bool = False, only: bool = False, flooding: bool = False, check: bool = False, debug: bool = False):
    """
    SMS bomber
    """
    utils.banner()
    utils.checker.chk_internet()
    utils.checker.chk_args_conflict(phone, thread, count, interval, max_tried, proxy, only, flooding, check)
    thread = thread if thread else __nproc__
    count = count if count else 1
    interval = interval if interval else 0
    max_tried = max_tried if max_tried else 100
    utils.checker.chk_args_validation(phone, thread, count, interval, max_tried)
    logger.info(f'phone:{phone}, thread:{thread}, count:{count}, max_tried:{max_tried} '
                f'interval:{interval}, proxy:{proxy}, flooding:{flooding}, only:{only}, check:{check}, debug:{debug}')
    _api = api.load_api_json()
    logger.success(f'apidata.json has been loaded, {len(_api)} api has been found.')
    try:
        if check:
            req.do_sms_check(phone, _api)
        elif flooding:
            with ThreadPoolExecutor(max_workers=64, thread_name_prefix='Pecker') as executor:
                while True:
                    executor.submit(req.do_sms_flooding,
                                    phone, _api)
        else:
            with ThreadPoolExecutor(max_workers=thread, thread_name_prefix='Pecker') as executor:
                if only:
                    max_tried = max_tried if max_tried else req.max_tried
                    for i in range(max_tried):
                        executor.submit(req.do_sms_succeeds,
                                        phone, count, interval, max_tried, _api)
                else:
                    for i in range(count):
                        executor.submit(req.do_sms,
                                        phone, count, interval, _api)
                        # TODO add statistics
    except KeyboardInterrupt as e:
        executor.shutdown()
        exit(-1)


if __name__ == '__main__':
    pecker()
