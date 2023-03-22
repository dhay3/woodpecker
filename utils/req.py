import json
import aiohttp
import asyncio
import os
from typing import Union
from utils.api import load_api
from enum import Enum
from utils.bean import APIBean


class METHOD(Enum):
    GET = "GET"
    POST = "POST"


async def sms(m: [APIBean]):
    task = []
    for _m in m:
        print(_m)
        task.append(do(_m))
    await asyncio.gather(*task)


async def do(_m: APIBean):
    conn = aiohttp.TCPConnector(ssl=False,
                                use_dns_cache=True,
                                ttl_dns_cache=60,
                                limit=None,
                                limit_per_host=0)
    timeout = aiohttp.ClientTimeout(total=None)
    url = _m.url
    method = _m.method
    payload = _m.payload
    headers = _m.header
    async with aiohttp.ClientSession(connector=conn,
                                     timeout=timeout,
                                     headers=headers) as session:
        rt = await __do(session, url, method, payload)
        print(rt)
        return rt


async def __do(session: aiohttp.ClientSession, url: str, method: str, payload: Union[dict, str]):
    if method == METHOD.GET.value and payload:
        r = await session.request(method, url, params=payload)
    elif method == METHOD.POST.value and payload:
        if isinstance(payload, dict):
            r = await session.request(method, url, json=payload)
        else:
            r = await session.request(method, url, data=payload)
    else:
        r = await session.request(method, url)
    if isinstance(r, aiohttp.ClientResponse):
        if 200 == r.status:
            rt = await r.text()
            return rt


if __name__ == '__main__':
    if 'nt' == os.name:
        asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    loop = asyncio.get_event_loop()
    loop.run_until_complete(sms(load_api('15988803859')))
