import json
import aiohttp
import asyncio
import os
import random
from enum import Enum
from utils.factory_bak import APIModel
from utils.api_bak import load_api


class METHOD(Enum):
    GET = 1
    POST = 2
    HEAD = 3




async def do(_m: APIModel):
    conn = aiohttp.TCPConnector(ssl=False,
                                use_dns_cache=True,
                                ttl_dns_cache=60,
                                limit=None,
                                limit_per_host=0)
    timeout = aiohttp.ClientTimeout(total=None)
    url = _m.url
    method = _m.method
    payload = _m.payload
    headers = _m.payload
    headers = {
        'User-Agent': random_desktop_ua()
    }
    async with aiohttp.ClientSession(headers=headers) as session:
        rt = await _do(session, url, method, payload)
        print(rt)


async def _do(session: aiohttp.ClientSession, url: str, method: METHOD, payload: dict = None):
    if method.value == 1 and payload:
        r = await session.request(method.name, url, params=json.dumps(payload))
    elif method.value == 2 and payload:
        r = await session.request(method.name, url, data=json.dumps(payload))
    else:
        r = await session.request(method.name, url)
    if isinstance(r, aiohttp.ClientResponse):
        if 200 == r.status:
            rt = await r.text()
            return rt


if __name__ == '__main__':
    tasks = []
    if 'nt' == os.name:
        asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    for idx in range(0, 10):
        tasks.append(do('https://cip.cc', METHOD.GET))
    loop = asyncio.get_event_loop()
    loop.run_until_complete(asyncio.gather(*tasks))
