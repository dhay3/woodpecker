import datetime
import json
from pydantic import BaseModel
from typing import Union, Optional


class APIFactory(BaseModel):
    desc: str
    url: str
    method: str
    header: Optional[Union[str, dict]]
    data: Optional[Union[str, dict]]
    identifier: Optional[Union[str, dict]]

    def data2str(self, data: Union[str, dict], phone: str):
        return str(data).replace('[phone]', phone).replace('[timestamp]', str(datetime.datetime.now().timestamp())) \
            .replace("'", '"')

    def api_bean(self, phone: str):
        self.url = self.data2str(self.url, phone)
        self.header = self.header if self.header and self.header != '' else {}
        self.header['Referer'] = self.url
        from utils.req import random_user_agent
        self.header['User-Agent'] = random_user_agent()
        self.header = self.data2str(self.header, phone)
        self.data = self.data2str(self.data, phone)


if __name__ == '__main__':
    pass
