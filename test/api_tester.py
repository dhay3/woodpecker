import unittest
import requests
import pecker as pecker
import utils.req as req
from utils.bean import APIBean


class Tester(unittest.TestCase):

    def test_api_batch(self):
        _api = pecker.load_api(r'D:\code\woodpecker\apidata.json')
        for apiBean in _api:
            r = requests.request(**req.wrapper(apiBean, '15988803859'))
            print(r.text)

    def test_a(self):
        apiBean = APIBean(**{
            "desc": "迪卡侬",
            "url": "https://www.decathlon.com.cn/zh/ajax/rest/model/atg/userprofiling/ProfileActor/send-mobile-verification-code",
            "method": "POST",
            "json": {
                "countryCode": "CN",
                "mobile": "{phone}"
            },
            "identifier": "ok"
        })
        r = requests.request(**req.wrapper(apiBean, '15988803859'), )
        print(r.encoding)
        print(r.text)
        if apiBean.identifier in r.text:
            print(6666)


if __name__ == '__main__':
    unittest.main()
