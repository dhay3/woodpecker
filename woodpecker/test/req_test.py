import unittest
from loguru import logger

import utils.req as req


class ReqTestCase(unittest.TestCase):

    def test_random_user_agent(self):
        print(req.random_user_agent())

    def test_check_internet(self):
        req.check_internet()


if __name__ == '__main__':
    unittest.main()
