from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.bearer_token import BearerToken
from ...models.credentials import Credentials
from ...models.request_jwt_token_project_access_mode import (
    RequestJwtTokenProjectAccessMode,
)
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    body: Credentials,
    project_filter: Union[Unset, str] = UNSET,
    project_access_mode: Union[Unset, RequestJwtTokenProjectAccessMode] = UNSET,
    annotate_only: Union[Unset, bool] = False,
    login_only: Union[Unset, bool] = False,
    no_permissions: Union[Unset, bool] = False,
    duration: Union[Unset, str] = UNSET,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    params: dict[str, Any] = {}

    params["projectFilter"] = project_filter

    json_project_access_mode: Union[Unset, str] = UNSET
    if not isinstance(project_access_mode, Unset):
        json_project_access_mode = project_access_mode.value

    params["projectAccessMode"] = json_project_access_mode

    params["annotateOnly"] = annotate_only

    params["loginOnly"] = login_only

    params["noPermissions"] = no_permissions

    params["duration"] = duration

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/auth/login",
        "params": params,
    }

    _body = body.to_dict()

    _kwargs["json"] = _body
    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[BearerToken]:
    if response.status_code == 200:
        response_200 = BearerToken.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[BearerToken]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    body: Credentials,
    project_filter: Union[Unset, str] = UNSET,
    project_access_mode: Union[Unset, RequestJwtTokenProjectAccessMode] = UNSET,
    annotate_only: Union[Unset, bool] = False,
    login_only: Union[Unset, bool] = False,
    no_permissions: Union[Unset, bool] = False,
    duration: Union[Unset, str] = UNSET,
) -> Response[BearerToken]:
    """Request a bearer token

    Args:
        project_filter (Union[Unset, str]):
        project_access_mode (Union[Unset, RequestJwtTokenProjectAccessMode]):
        annotate_only (Union[Unset, bool]):  Default: False.
        login_only (Union[Unset, bool]):  Default: False.
        no_permissions (Union[Unset, bool]):  Default: False.
        duration (Union[Unset, str]):
        body (Credentials):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[BearerToken]
    """

    kwargs = _get_kwargs(
        body=body,
        project_filter=project_filter,
        project_access_mode=project_access_mode,
        annotate_only=annotate_only,
        login_only=login_only,
        no_permissions=no_permissions,
        duration=duration,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    body: Credentials,
    project_filter: Union[Unset, str] = UNSET,
    project_access_mode: Union[Unset, RequestJwtTokenProjectAccessMode] = UNSET,
    annotate_only: Union[Unset, bool] = False,
    login_only: Union[Unset, bool] = False,
    no_permissions: Union[Unset, bool] = False,
    duration: Union[Unset, str] = UNSET,
) -> Optional[BearerToken]:
    """Request a bearer token

    Args:
        project_filter (Union[Unset, str]):
        project_access_mode (Union[Unset, RequestJwtTokenProjectAccessMode]):
        annotate_only (Union[Unset, bool]):  Default: False.
        login_only (Union[Unset, bool]):  Default: False.
        no_permissions (Union[Unset, bool]):  Default: False.
        duration (Union[Unset, str]):
        body (Credentials):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        BearerToken
    """

    return sync_detailed(
        client=client,
        body=body,
        project_filter=project_filter,
        project_access_mode=project_access_mode,
        annotate_only=annotate_only,
        login_only=login_only,
        no_permissions=no_permissions,
        duration=duration,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    body: Credentials,
    project_filter: Union[Unset, str] = UNSET,
    project_access_mode: Union[Unset, RequestJwtTokenProjectAccessMode] = UNSET,
    annotate_only: Union[Unset, bool] = False,
    login_only: Union[Unset, bool] = False,
    no_permissions: Union[Unset, bool] = False,
    duration: Union[Unset, str] = UNSET,
) -> Response[BearerToken]:
    """Request a bearer token

    Args:
        project_filter (Union[Unset, str]):
        project_access_mode (Union[Unset, RequestJwtTokenProjectAccessMode]):
        annotate_only (Union[Unset, bool]):  Default: False.
        login_only (Union[Unset, bool]):  Default: False.
        no_permissions (Union[Unset, bool]):  Default: False.
        duration (Union[Unset, str]):
        body (Credentials):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[BearerToken]
    """

    kwargs = _get_kwargs(
        body=body,
        project_filter=project_filter,
        project_access_mode=project_access_mode,
        annotate_only=annotate_only,
        login_only=login_only,
        no_permissions=no_permissions,
        duration=duration,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    body: Credentials,
    project_filter: Union[Unset, str] = UNSET,
    project_access_mode: Union[Unset, RequestJwtTokenProjectAccessMode] = UNSET,
    annotate_only: Union[Unset, bool] = False,
    login_only: Union[Unset, bool] = False,
    no_permissions: Union[Unset, bool] = False,
    duration: Union[Unset, str] = UNSET,
) -> Optional[BearerToken]:
    """Request a bearer token

    Args:
        project_filter (Union[Unset, str]):
        project_access_mode (Union[Unset, RequestJwtTokenProjectAccessMode]):
        annotate_only (Union[Unset, bool]):  Default: False.
        login_only (Union[Unset, bool]):  Default: False.
        no_permissions (Union[Unset, bool]):  Default: False.
        duration (Union[Unset, str]):
        body (Credentials):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        BearerToken
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
            project_filter=project_filter,
            project_access_mode=project_access_mode,
            annotate_only=annotate_only,
            login_only=login_only,
            no_permissions=no_permissions,
            duration=duration,
        )
    ).parsed
