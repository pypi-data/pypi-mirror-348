import ssl
from typing import Dict, Union

import attr


@attr.s(auto_attribs=True)
class Client:
    """A class for keeping track of data related to the API

    Attributes:
        base_url: The base URL for the API, all requests are made to a relative path to this URL
        cookies: A dictionary of cookies to be sent with every request
        headers: A dictionary of headers to be sent with every request
        timeout: The maximum amount of a time in seconds a request can take. API functions will raise
            httpx.TimeoutException if this is exceeded.
        verify_ssl: Whether or not to verify the SSL certificate of the API server. This should be True in production,
            but can be set to False for testing purposes.
        raise_on_unexpected_status: Whether or not to raise an errors.UnexpectedStatus if the API returns a
            status code that was not documented in the source OpenAPI document.
    """

    base_url: str
    cookies: Dict[str, str] = attr.ib(factory=dict, kw_only=True)
    headers: Dict[str, str] = attr.ib(factory=dict, kw_only=True)
    timeout: float = attr.ib(5.0, kw_only=True)
    verify_ssl: Union[str, bool, ssl.SSLContext] = attr.ib(True, kw_only=True)
    raise_on_unexpected_status: bool = attr.ib(False, kw_only=True)

    def get_headers(self) -> Dict[str, str]:
        """Get headers to be used in all endpoints"""
        return {**self.headers}

    def with_headers(self, headers: Dict[str, str]) -> "Client":
        """Get a new client matching this one with additional headers"""
        return attr.evolve(self, headers={**self.headers, **headers})

    def get_cookies(self) -> Dict[str, str]:
        return {**self.cookies}

    def with_cookies(self, cookies: Dict[str, str]) -> "Client":
        """Get a new client matching this one with additional cookies"""
        return attr.evolve(self, cookies={**self.cookies, **cookies})

    def get_timeout(self) -> float:
        return self.timeout

    def with_timeout(self, timeout: float) -> "Client":
        """Get a new client matching this one with a new timeout (in seconds)"""
        return attr.evolve(self, timeout=timeout)


@attr.s(auto_attribs=True)
class AuthenticatedClient(Client):
    """A Client which has been authenticated for use on secured endpoints"""

    token: str
    prefix: str = "Bearer"
    auth_header_name: str = "Authorization"

    def get_headers(self) -> Dict[str, str]:
        auth_header_value = f"{self.prefix} {self.token}" if self.prefix else self.token
        """Get headers to be used in authenticated endpoints"""
        if self.token is not None:
            return {self.auth_header_name: auth_header_value, **self.headers}
        else:
            return {**self.headers}


import pkg_resources
from httpx import BasicAuth
from httpx import Client as HttpxClient
from httpx import Response as HttpxResponse

from .models import BearerToken, Credentials, RequestJwtTokenProjectAccessMode
from .types import UNSET, Response, Unset


@attr.s(auto_attribs=True)
class SherpaClient(Client):
    """A Client logged"""

    token: str = attr.ib(init=True, default=None)
    prefix: str = "Bearer"
    auth_header_name: str = "Authorization"
    session_cookies: Dict[str, str] = attr.ib(factory=dict, kw_only=True, init=True)

    def get_headers(self) -> Dict[str, str]:
        auth_header_value = f"{self.prefix} {self.token}" if self.prefix else self.token
        """Get headers to be used in authenticated endpoints"""
        if self.token is not None:
            return {self.auth_header_name: auth_header_value, **self.headers}
        else:
            return {**self.headers}

    def get_cookies(self) -> Dict[str, str]:
        """Get cookies to be used in authenticated endpoints"""
        if self.session_cookies:
            return {**self.session_cookies, **self.cookies}
        else:
            return {**self.cookies}

    def login_with_cookie(self, credentials: Credentials):
        """ """
        my_version = pkg_resources.get_distribution("sherpa-client")
        httpx_client = HttpxClient(
            base_url=self.base_url,
            auth=BasicAuth(username=credentials.email, password=credentials.password),
            headers={"User-Agent": f"{my_version.key}/{my_version.parsed_version}"},
        )
        res: HttpxResponse = httpx_client.get("/current_user")
        if res.is_success and res.cookies:
            self.session_cookies = {k: res.cookies[k] for k in res.cookies}
        else:
            res.raise_for_status()

    def login_with_token(
        self,
        credentials: Credentials,
        project_filter: Union[Unset, None, str] = UNSET,
        project_access_mode: Union[Unset, None, RequestJwtTokenProjectAccessMode] = UNSET,
        annotate_only: Union[Unset, None, bool] = False,
        login_only: Union[Unset, None, bool] = False,
        no_permissions: Union[Unset, None, bool] = False,
    ):
        """ """
        from .api.authentication import request_jwt_token

        r: Response[BearerToken] = request_jwt_token.sync_detailed(
            client=self,
            json_body=credentials,
            project_filter=project_filter,
            project_access_mode=project_access_mode,
            annotate_only=annotate_only,
            login_only=login_only,
        )
        if r.is_success:
            self.token = r.parsed.access_token
        else:
            r.raise_for_status()

    def login_with_apikey(self, api_key_header_name: str, token: str):
        """ """
        self.auth_header_name = api_key_header_name
        self.token = token
        self.prefix = None
        httpx_client = HttpxClient(
            base_url=self.base_url,
            headers=self.get_headers(),
        )
        res: HttpxResponse = httpx_client.get("/current_user")
        if not res.is_success:
            res.raise_for_status()
