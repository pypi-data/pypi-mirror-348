import time
import typing

import httpx


class BrivoAuth(httpx.Auth):
    HEADERS = {'accept': 'application/json'}

    def __init__(self, base_url: str, username: str, password: str):
        self.username = username
        self.password = password
        self.base_url = base_url
        self._access_token = None
        self._token_expires_at = 0

    @staticmethod
    def _handle_response(resp: httpx.Response) -> None:
        ...

    @property
    def authenticated(self) -> bool:
        return self._access_token is not None

    def build_authentication_request(self) -> httpx.Request:
        url = self.base_url + '/v1/login'
        payload = {
            'username': self.username,
            'password': self.password
        }
        return httpx.Request("POST", url, headers=self.HEADERS, json=payload)

    def _update_token(self, response: httpx.Response):
        response.raise_for_status()
        body = response.json()
        self._token_expires_at = time.time() + 900  # 15 minutes
        self._access_token = body['access_token']

    def sync_auth_flow(self, request: httpx.Request) -> typing.Generator[httpx.Request, httpx.Response, None]:
        if self._token_expires_at < time.time():  # if token is expired
            response = yield self.build_authentication_request()
            response.read()
            self._handle_response(response)
            self._update_token(response)
        request.headers['authorization'] = f'Token {self._access_token}'
        yield request

    async def async_auth_flow(self, request: httpx.Request) -> typing.AsyncGenerator[httpx.Request, httpx.Response]:
        if self._token_expires_at < time.time():  # if token is expired
            response = yield self.build_authentication_request()
            await response.aread()
            self._handle_response(response)
            self._update_token(response)
        request.headers['authorization'] = f'Token {self._access_token}'
        yield request
