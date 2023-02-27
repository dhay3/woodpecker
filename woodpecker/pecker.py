import click
import multiprocessing
import utils
import utils.req
from concurrent.futures import ThreadPoolExecutor
from utils.log import logger

__nproc__ = multiprocessing.cpu_count()
__version__ = 0.1


@click.group()
def cli():
    pass


@cli.command()
def call():
    pass


@cli.command()
@click.option('-p', '--phone', metavar='Phone', prompt=True, required=True, type=str,
              help='Target phone number to send sms.')
@click.option('-t', '--thread', metavar='ThreadingNum', default=__nproc__, show_default=True, type=int,
              help='Threading number to send sms.')
@click.option('-c', '--count', metavar='Count', default=1, show_default=True, type=int,
              help='Count of sms to send. Failed\'s will be counted.')
@click.option('-i', '--interval', metavar='Interval', default=1, show_default=True, type=int,
              help='Delay time of sending sms.')
@click.option('-x', '--proxy', is_flag=True, type=bool,
              help='Use proxy.')
@click.option('-f', '--flooding', is_flag=True, type=bool,
              help='Flooding api mode.')
@click.option('--only', is_flag=True, type=bool,
              help='Only succeed counts.')
def sms(phone: str, thread: int, count: int, interval: int, proxy: bool = False, only: bool = False,
        flooding: bool = False):
    """
    SMS bomber
    """
    try:
        if phone:
            utils.phone_checker(phone)
            # redundancy
        else:
            raise Exception('Phone number cannot be null.')
        if count < 1 or interval < 1 or thread < 1:
            raise Exception('Either count or interval or thread must be positive.')
    except Exception as e:
        logger.error(e.__str__())
        exit(-1)
    with ThreadPoolExecutor(max_workers=thread, thread_name_prefix='Pecker') as executor:
        if proxy:
            pass
        else:
            if only:
                executor.submit(utils.req.do_sms_succeeds, phone, count)
            else:
                executor.submit(utils.req.do_sms, phone, count)


if __name__ == '__main__':
    cli()
