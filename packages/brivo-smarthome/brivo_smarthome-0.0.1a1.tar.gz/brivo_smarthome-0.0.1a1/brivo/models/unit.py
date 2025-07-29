from datetime import datetime

from brivo.brivo_client import BaseBrivoClient


class Unit(BaseBrivoClient):
    id: int
    name: str
    description: str
    address_1: str
    address_2: str
    zipcode: str
    city: str
    state: str
    master_code: str
    created_at: datetime
    updated_at: datetime
    temp: int
    secure: bool
    dry: bool | None
    is_active: bool
    user: int
    co: bool
    smoke: bool
    timezone: str | None
    parent_timezone: str | None