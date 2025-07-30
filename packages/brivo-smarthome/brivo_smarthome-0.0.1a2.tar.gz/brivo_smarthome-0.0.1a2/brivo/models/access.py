from datetime import datetime
from enum import Enum
from random import randint
from typing import Literal

from pydantic import Field

from brivo.models.base import BaseBrivoModel
from brivo.models.company import Company
from brivo.models.unit import Unit


class UserRole(Enum):
    SUPER_ADMIN = 1
    TECHNICIAN = 2
    ADMIN = 3
    GUEST_MANAGER = 4
    OWNER = 5
    STAFF = 6
    GUEST = 7
    VENDOR = 8
    INSTALLER = 9

    @property
    def name(self):
        return {
            UserRole.SUPER_ADMIN: "Super Admin",
            UserRole.TECHNICIAN: "Technician",
            UserRole.ADMIN: "Admin",
            UserRole.GUEST_MANAGER: "Guest Manager",
            UserRole.OWNER: "Owner",
            UserRole.STAFF: "Staff",
            UserRole.GUEST: "Guest",
            UserRole.VENDOR: "Vendor",
            UserRole.INSTALLER: "Installer",
        }[self]


class Access(BaseBrivoModel):
    id: int
    start_time: datetime = Field(default_factory=datetime.now)
    end_time: datetime | None = None
    type: Literal['Access', 'access_window']
    code: str | None = Field(default_factory=lambda: Access._generate_random_code())
    is_code: bool = True
    is_locking: bool = True
    units: list[Unit] = Field(default_factory=list, validation_alias='property', serialization_alias='property')
    company: list[Company] = Field(default_factory=list)
    first_name: str
    last_name: str
    email: str | None = None
    phone: str | None = None
    role: UserRole = Field(UserRole.GUEST, validation_alias='group', serialization_alias='group')
    delivery_method: Literal['none', 'email', 'sms', 'email_sms'] = 'none'
    is_overridden: bool = False
    alternate_id: str | None = None
    temp_disabled: bool = False
    mobile_pass: str | None = None # Unknown type. guess it's a string
    emergency_state: Literal['not', 'used']
    access_trailing_key: str | None
    has_schedule: bool

    @staticmethod
    def _generate_random_code() -> str:
        return format(randint(0, 9999), '04')

    def randomize_code(self):
        self.code = self._generate_random_code()
