import unittest
import utils.req
import utils.api
from utils.log import logger


class UtilsTestCase(unittest.TestCase):
    def test_logger(self):
        logger.debug("That's it, beautiful and simple logging!")
        logger.info("That's it, beautiful and simple logging!")
        logger.error("That's it, beautiful and simple logging!")
        logger.success("That's it, beautiful and simple logging!")

    def test_api_load_json(self):
        utils.api.load_api_json('D:\\code\\woodpecker\\apidata_test.json')

    def test_req_do_sms(self):
        utils.req.do_sms('15988803859', 5, 1, utils.api.load_api_json())

    def test_req_do_sms_succeeds(self):
        utils.req.do_sms_succeeds('15988803859', 5, 1, 10, utils.api.load_api_json())

    def test_req_check_internet(self):
        utils.req.check_internet()

    def test_random_user_agent(self):
        utils.req.random_user_agent('D:\\code\\woodpecker\\headers.json')


class peckerTestCase(unittest.TestCase):
    def test_pecker(self):
        pass


if __name__ == '__main__':
    unittest.main()
