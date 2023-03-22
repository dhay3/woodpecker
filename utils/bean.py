import json
import random
from typing import Union, Optional

__DESKTOP_USER_AGENT__ = (
    'Mozilla/5.0 (Linux; Android 12; SM-S906N Build/QP1A.190711.020; wv) AppleWebKit/537.36 (KHTML, like Gecko) '
    'Version/4.0 Chrome/80.0.3987.119 Mobile Safari/537.36',
    'Mozilla/5.0 (iPhone12,1; U; CPU iPhone OS 13_0 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) '
    'Version/10.0 Mobile/15E148 Safari/602.1',
    'Mozilla/5.0 (Linux; U; Android 4.0.3; en-us) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.59 Mobile '
    'Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.91 Safari/537.36'
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 '
    'Safari/537.36 Edge/12.246 '
)

import requests


def random_ua():
    return random.choice(__DESKTOP_USER_AGENT__)


class APIBean:

    def __init__(self, phone, desc: str, url: str, method: str, identifier: str,
                 header: Optional[Union[str, dict]] = None,
                 payload: Optional[Union[str, dict]] = None):
        self._desc = desc
        self._url = url.replace('{phone}', phone)
        self._method = method.upper()
        self._identifier = identifier
        if not header:
            header = {}
        header['User-Agent'] = random_ua()
        header['Referer'] = self._url
        self._header = header
        self._payload = json.loads(json.dumps(payload).replace('{phone}', phone)) if payload else None

    def __str__(self):
        return str(self.__dict__)

    def __repr__(self):
        return self.__str__()

    def __copy__(self):
        import copy
        return copy.copy(self)

    @property
    def desc(self):
        return self._desc

    @desc.setter
    def desc(self, value):
        self._desc = value

    @property
    def url(self):
        return self._url

    @url.setter
    def url(self, value):
        self.url = value

    @property
    def header(self):
        return self._header

    @header.setter
    def header(self, value):
        self._header = value

    @property
    def method(self):
        return self._method

    @method.setter
    def method(self, value):
        self._method = value

    @property
    def payload(self):
        return self._payload

    @payload.setter
    def payload(self, value):
        self._payload = value

    @property
    def identifier(self):
        return self._identifier

    @identifier.setter
    def identifier(self, value):
        self._identifier = value


if __name__ == '__main__':
    import utils.api as a

    print(a.load_api('1111'))
    d = {
        "to": "[phone]",
        "sms_type": "sms_registration"
    }
    # b = [1, 2, 3, 4]
    # s = map(lambda x: x.replace('[phone]', '11111'), d.values())

    # for k, v in d.items():
    #     d[k] = v.replace()
    # print(d)

    # json.loads(None)
