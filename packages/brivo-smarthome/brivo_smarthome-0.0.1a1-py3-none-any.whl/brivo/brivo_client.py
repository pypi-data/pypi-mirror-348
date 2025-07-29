from abc import ABC, abstractmethod
from datetime import datetime
from os import getenv

from brivo.models.auth import BrivoAuth


class BaseBrivoClient(ABC):
    HEADERS = {'accept': 'application/json'}

    def __init__(self, username: str, password: str, base_url: str, company_id: int | None = None):
        base_url = base_url or 'https://api.smarthome.brivo.com'
        username = username or getenv('BRIVO_USERNAME')
        password = password or getenv('BRIVO_PASSWORD')
        self.base_url: str = base_url.rstrip('/')
        self._company_id: int | None = int(company_id) if company_id else company_id
        self.auth: BrivoAuth = BrivoAuth(self.base_url, username, password)

    @abstractmethod
    def _request(self, method: str, endpoint: str, query_params: dict = None, payload: dict = None) -> dict:
        pass

    def company_accesses(self, company_id: int) -> dict:
        """
           Fetches accesses for a given company from the Brivo SmartHome API.

           Args:
               company_id (int): The ID of the company.

           Returns:
               list[Access]: A list of accesses.
           """
        endpoint = f'/v1/companies/{company_id}/accesses'

        return self._request('GET', endpoint)

    def company_alerts(self, company_id: int, page: int) -> dict:
        """
        Fetches alerts for a given company and page from the Brivo SmartHome API.

        Args:
            company_id (int): The ID of the company to fetch alerts for.
            page (int): The page number of paginated results.

        Returns:
            dict: A dictionary with the following structure:
                {
                    "count": int,               # Total number of alerts available
                    "next": str or None,        # URL to the next page of results
                    "previous": str or None,    # URL to the previous page
                    "results": [                # List of alert objects
                        {
                            "message": str,
                            "device": str or None,
                            "deviceId": int,
                            "property": str,
                            "propertyId": int,
                            "type": str,         # "device" or "gateway"
                            "timestamp": str,    # Format: "YYYY-MM-DD HH:MM:SS"
                            "timezone": str      # e.g. "US/Pacific"
                        },
                        ...
                    ]
                }
        """
        endpoint = f'/v3/company/{company_id}/alert'
        query_params = {'page': page}

        return self._request('GET', endpoint, query_params=query_params)

    def create_access(
            self, company: list[int],
            code: str | None,
            first_name: str,
            last_name: str,
            email: str,
            phone: str | None,
            group: int,
            type: str = 'anytime',
            start_time: str = datetime.now().isoformat(),
            end_time: str | None = None,
            delivery_method: str = 'email',
            is_code: bool = True,
            is_locking: bool = True,
            temp_disabled: bool = False,
            mobile_pass: str | None = None,
            resource_type: str = 'Access',
            user: None = None,
    ) -> dict:
        """
        Create a new access.
        """
        payload = {
            "company": company,
            "code": code,
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "phone": phone,
            "group": group,
            "type": type,
            "start_time": start_time,
            "end_time": end_time,
            "delivery_method": delivery_method,
            "is_code": is_code,
            "is_locking": is_locking,
            "temp_disabled": temp_disabled,
            "mobile_pass": mobile_pass,
            "resource_type": resource_type,
            "user": user
        }
        return self._request('POST', '/v1/accesses', payload=payload)

    def me(self) -> dict:
        """
        Fetches the user's information from the Brivo API.
        Returns:
        {
            "id":12345,
            "email":"anthony@brivo.com",
            "first_name":"Anthony",
            "last_name":"DeGarimore",
            "bio":"",
            "phone":"8181234567",
            "is_active":true,
            "is_superuser":false,
            "group":1,
            "last_viewed_company":123,
            "system_message":false,
            "password_last_changed":"2099-01-01T12:34:56.789Z"
        }
        """
        return self._request('GET', '/v1/users/me')

    def my_accesses(self) -> dict:
        """
        Fetches the user's access records from the Brivo API.
        Returns:
        {
            "count":128,
            "results":[
                {
                    "id":12345678,
                    "data_relationship":"company", # or "property"
                    "alternate_id":null,
                    "code":"1234",
                    "delivery_method":"sms",
                    "email":"anthony@brivo.com",
                    "start_time":"2022-10-31T11:00:00Z",
                    "end_time":null,
                    "first_name":"Anthony",
                    "last_name":"DeGarimore",
                    "group":1,
                    "is_code":true,
                    "is_locking":true,
                    "is_overridden":false,
                    "phone":"8181234567",
                    "type":"anytime",
                    "access_trailing_key":null,
                    "links":{
                        "href":"https://api.smarthome.brivo.com/v3/company/access/12345678",
                        "rel":"company", # or "property"
                        "type":"GET"
                    }
                },
                ...
            ]
        }
        """
        endpoint = '/v3/user/access'
        return self._request('GET', endpoint)

class BrivoClient(BaseBrivoClient):
    def __init__(self, username: str = None, password: str = None, base_url: str = None, company_id: int | None = None):
        super().__init__(username, password, base_url, company_id)
        self._company_id = company_id