import json
import aiohttp
from enum import Enum

conn = aiohttp.TCPConnector(ssl=False, ttl_dns_cache=30)
timeout = aiohttp.ClientTimeout(total=60)


class METHOD(Enum):
    GET = 1
    POST = 2
    HEAD = 3


async def do(session: aiohttp.ClientSession, url: str, method: METHOD, payload: dict):
    if method.value == 1:
        r = await session.request(method.name, url, params=json.dumps(payload))
    elif method.value == 2:
        r = await session.request(method.name, url, data=json.dumps(payload))
    else:
        r = await session.request(method.name, url)
    if isinstance(r, aiohttp.ClientResponse):
        if 200 == r.status:
            rt = await r.text()
            return rt


if __name__ == '__main__':
    pass
