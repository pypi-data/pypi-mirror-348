from brivo.models.base import BaseBrivoModel


class Company(BaseBrivoModel):
    id: int
    name: str
    img: str # URL to the company logo
    address_1: str
    address_2: str | None
    city: str
    state: str
    zipcode: str
    timezone: str