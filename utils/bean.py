from dataclasses import dataclass
from typing import Optional


@dataclass
class APIBean:
    desc: str
    url: str
    method: str
    identifier: str
    headers: Optional[dict] = None
    params: Optional[dict] = None
    data: Optional[dict] = None
    json: Optional[dict] = None
